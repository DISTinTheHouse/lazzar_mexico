from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from mainapp.models import CorreosLazzar
from almacen.models import codigo_almacen
from django.db import connection
from django.http import FileResponse, HttpResponseNotFound
from datetime import datetime
import MySQLdb
import pyodbc
import os


DB_HOST = 'as.galio.net' 
DB_USER = 'u129' 
DB_PASS = 'lbrfyg' 
DB_NAME = 'db129lazzar'
DB_PORT = 61129

# CONEXION SQLSERVER BITACOR DE PRODUCCION
server = 'lazzarbodegavpn.dyndns.info'
database = 'CODIGO_BARRAS'
username = 'sa'
password = 'lazzar2018'

def run_query(query=''): 
    datos = [DB_HOST, DB_USER, DB_PASS, DB_NAME, DB_PORT] 
    
    conn = MySQLdb.connect(*datos) # Conectar a la base de datos 
    cursor = conn.cursor()         # Crear un cursor 
    cursor.execute(query)          # Ejecutar una consulta 

    if query.upper().startswith('SELECT'): 
        data = cursor.fetchall()   # Traer los resultados de un select 
    else: 
        conn.commit()              # Hacer efectiva la escritura de datos 
        data = None 
    
    cursor.close()                 # Cerrar el cursor 
    conn.close()                   # Cerrar la conexión 

    return data

# EJECUTA EL QUERY Y RETORNA LA INFORMACIÓN (SQLSERVER)
def run_query_sql(query=''): 
    cadena_conexion = f'DSN=mydsn;SERVER={server};DATABASE={database};UID={username};PWD={password}'
    conexion = pyodbc.connect(cadena_conexion)
    cursor = conexion.cursor()

    cursor.execute(query)
    data = cursor.fetchall()
    
    conexion.commit()  # Siempre es recomendable confirmar los cambios antes de cerrar la conexión.
    conexion.close()       # Cerrar la conexión 

    return data

@login_required(login_url="login")
def pedidos_produccion (request):
    usuario = CorreosLazzar.objects.get(correo=request.user.email)

    if usuario.esvendedor:
        vendedores = CorreosLazzar.objects.filter(esvendedor=usuario.esvendedor)

        return render(request, 'restringido.html', {
            'title': 'Acceso Restringido',
            'vendedores': vendedores,
            'leyenda': False,
        })
    else:
     return render(request, 'pedidos_produccion.html')
    
#Se agrego models.py almacen y se configuro form y pagina - Jesús - 21/09/23
@login_required(login_url="login")
def stock(request):
    almacenes = codigo_almacen.objects.all()

    if request.method == 'POST':
        cod_almacen = request.POST.get('almacen')
        almacen = codigo_almacen.objects.get(cod_almacen=cod_almacen)  # Reemplaza con el modelo adecuado
        resultados = []
        resultados_telas = []
        resultados_prod_terminado = []

        if cod_almacen == '02':

            query = (f"SELECT ICOD as CODIGO, IDESCR as DESCRIPCION, ROUND(SUM(A.ALMCANT-A.ALMASIGNADO), 0) as INVENTARIO "
                +"FROM FINV I INNER JOIN FALM A ON A.ISEQ = I.ISEQ "
                +"WHERE A.ALMNUM = '" + cod_almacen + "' AND A.ALMCANT <> '0' AND A.ALMCANT <> 0 GROUP BY ICOD ;")

            results = run_query(query)
            resultados = list(results)

        if cod_almacen == '03' or '04' or '07' or '11' or '15':
            query_telas = (f"SELECT ICOD, IDESCR, CAJSERIE, FORMAT(CAJCANT,2), CAJOBS FROM fcajas C "
                +"INNER JOIN FINV I ON I.ISEQ = C.ISEQ "
                +"WHERE CAJALM = '" + cod_almacen + "' AND CAJFACTURA = '';")
        
            results = run_query(query_telas)
            resultados_telas = list(results)
        
            if cod_almacen == '00': 
                query_prod_terminado = (f"SELECT ICOD as CODIGO,IDESCR as DESCRIPCION, ROUND(SUM(A.ALMCANT-A.ALMASIGNADO),0 ) as INVENTARIO FROM FINV I INNER JOIN FALM A ON A.ISEQ = I.ISEQ "
                                    +"WHERE ICOD >= 'A' AND ICOD <= 'Z99999999' AND A.ALMNUM = '00' AND A.ALMCANT <> '0' AND A.ALMCANT <> 0 GROUP BY ICOD ")

                results = run_query(query_prod_terminado)
                resultados_prod_terminado = list(results)

                return render(request, "stock.html", {
                        'almacenes': almacenes,
                        'leyenda': True,
                        'resultados_prod_terminado': resultados_prod_terminado,
                        'prod_term': bool(resultados_prod_terminado),
                        })

        return render(request, 'stock.html', {
            'almacenes': almacenes,
            'almacen': almacen,  # Pasa el almacén seleccionado a la plantilla
            'resultados': resultados,
            'resultados_telas': resultados_telas,
            'resultados_prod_terminado': resultados_prod_terminado,
            'avios': bool(resultados),
            'telas': bool(resultados_telas),


        })
    else:
        return render(request, "stock.html", {
            'almacenes': almacenes,
            'leyenda': False,
        })
#Se agrego vista y url para pedidos P - Jesús - 21/09/23
@login_required(login_url="login")
def pedidos_ep(request):
    if request.method == 'POST':
        inicio_fecha = request.POST['inicio_fecha']
        final_fecha = request.POST['final_fecha']

        query = (f"SELECT PENUM, CLINOM, AGDESCR, PEFECHA, PEPAR3, PEFECHAEMPAQUE, PEDESDE, PEVENCE, PEPAR7 FROM FPLIN L "
                 + "INNER JOIN FPENC P ON P.PESEQ = L.PESEQ INNER JOIN FCLI C ON C.CLISEQ = P.CLISEQ INNER JOIN FAG "
                 + "A ON A.AGTNUM = P.PEPAR1 WHERE (PLCANT-PLSURT) <> 0 AND PEFECHA BETWEEN '" + inicio_fecha + "' AND '" + final_fecha + "' AND P.PENUM >= 'P' "
                 + "AND P.PENUM <= 'P99999' AND PESPEDIDO = 1 GROUP BY PENUM ORDER BY PENUM;")
        
        results = run_query(query)
        resultado = list(results)

        return render(request, 'pedidos_ep.html',{
            'leyenda': True,
            'fecha_inicio': inicio_fecha,
            'fecha_final': final_fecha,
            'resultado': resultado,
        })
    else:
        return render(request, 'pedidos_ep.html',{
            'leyenda': False,
        })

login_required(login_url="login")
def produccion_activos(request):

    query = (f"SELECT P.PENUM, MID(I.ICOD,3,12), MID(I.ICOD,3,7), MID(I.ICOD,10,3), I.IDESCR, ROUND(PL.PLCANT-PL.PLSURT, 0), P.PEVENCE FROM FPLIN PL "
            +"INNER JOIN FINV I ON I.ISEQ = PL.ISEQ INNER JOIN FFAM F ON F.FAMTNUM = I.IFAM6 INNER JOIN FPENC P ON P.PESEQ = PL.PESEQ "
            +"WHERE PLTIPMV = 'E' AND P.PEINICIAL = 0 AND P.PEPAR1 = '1PW' ORDER BY P.PENUM, MID(I.ICOD,3,12) ")

    results = run_query(query)
    resultados = list(results)

    return render (request, 'produccion_activos.html',{
        'resultados': resultados,
    })

login_required(login_url="login")
def pedidos_cedicor(request):

    query = (f"SELECT PENUM, MID(I.ICOD,3,12), MID(I.ICOD,3,7), MID(I.ICOD,10,3), IDESCR, ROUND(PLCANT, 0), PEOBS FROM FPENC P INNER JOIN FPLIN L ON L.PESEQ = P.PESEQ "
            +"INNER JOIN FINV I ON I.ISEQ = L.ISEQ WHERE PESPEDIDO = 1 AND PEPAR7 = '7PW' AND PENUM >= 'Q' AND PENUM <= 'Q99999';")
    
    results = run_query(query)
    resultados = list(results)
    
    return render (request, 'pedidos_cedicor.html', {
        'resultados': resultados,
    })