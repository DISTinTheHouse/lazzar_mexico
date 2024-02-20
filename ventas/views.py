from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from mainapp.models import CorreosLazzar
import MySQLdb
import pyodbc

from django.http import FileResponse, HttpResponseNotFound
import os
from datetime import datetime

DB_HOST = 'as.galio.net' 
DB_USER = 'u129' 
DB_PASS = 'lbrfyg' 
DB_NAME = 'db129lazzar'
DB_PORT = 61129

# CONEXION SQLSERVER BITACOR DE PRODUCCION
# server = 'lazzarbodegavpn.dyndns.info'
# database = 'CODIGO_BARRAS'
# username = 'sa'
# password = 'lazzar2018'

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
# def run_query_sql(query=''): 
#     cadena_conexion = f'DSN=mydsn;SERVER={server};DATABASE={database};UID={username};PWD={password}'
#     conexion = pyodbc.connect(cadena_conexion)
#     cursor = conexion.cursor()

#     cursor.execute(query)
#     data = cursor.fetchall()
    
#     conexion.commit()  # Siempre es recomendable confirmar los cambios antes de cerrar la conexión.
#     conexion.close()       # Cerrar la conexión 

#     return data

@login_required(login_url="login")
def facturas(request):
    usuario = CorreosLazzar.objects.get(correo = request.user.email)

    return render(request, 'facturacion.html',{
        'title':'Facturación',
        'leyenda':False,
        'usuario': usuario
    })

@login_required(login_url="login")
def facturas_fecha(request):
    usuario = CorreosLazzar.objects.get(correo = request.user.email)

    if request.method == 'POST':
        start_fecha = request.POST['start_date']
        end_fecha = request.POST['end_date']

        query = (f"SELECT F.DNUM, F.DREFER, I.IDESCR, CAST(M.PLCANT AS SIGNED) AS PLCANT, C.CLINOM, C.CLICONT, CLITEL, CLITEL4, A.AGDESCR, AA.AGDESCR FROM FDOC F "
        + "INNER JOIN fpenc P ON PENUM = F.DREFER LEFT JOIN FPLIN M ON P.PESEQ = M.PESEQ LEFT JOIN FINV I ON I.ISEQ = M.ISEQ LEFT JOIN "
        + "FCLI C ON C.CLISEQ = F.CLISEQ INNER JOIN FAG A ON A.AGTNUM = P.PEPAR1 INNER JOIN FAG AA ON AA.AGTNUM = P.PEPAR4 WHERE "
        + "F.dfecha BETWEEN '" + start_fecha + "' AND '" + end_fecha + "' AND F.DITIPMV = 'F' AND F.DCANCELADA = 0 ORDER BY F.DNUM;") 

        results = run_query(query) 

        resultado = list(results)

    return render(request, 'facturacion.html',{
        'title':'Facturación',
        'resultado':resultado,
        'leyenda':True,
        'fecha_Ini':start_fecha,
        'fecha_Fin':end_fecha,
        'usuario': usuario
    })

@login_required(login_url="login")
def chats(request):
    usuario = CorreosLazzar.objects.get(correo = request.user.email)

    return render(request, 'chats.html',{
        'title':'Pedidos por Chat',
        'leyenda':False,
        'usuario': usuario
    })

@login_required(login_url="login")
def chats_fecha(request):

    usuario = CorreosLazzar.objects.get(correo = request.user.email)

    if request.method == 'POST':
        start_fecha = request.POST['start_date']
        end_fecha = request.POST['end_date']

        query = (f"SELECT PENUM, CLINOM, PEBRUTO, PEIVA, PECANT, AGDESCR FROM FPENC P INNER JOIN FCLI C ON C.CLISEQ = P.CLISEQ "
                 + "INNER JOIN FAG A ON A.AGTNUM = P.PEPAR1 WHERE PENUM BETWEEN 'P' AND 'P999999' AND PEFECHA BETWEEN '" + start_fecha 
                 + "' AND '" + end_fecha + "' AND PEPAR4 = '4CO';") 

        results = run_query(query) 

        resultado = list(results)

    return render(request, 'chats.html',{
        'title':'Pedidos por Chat',
        'resultado':resultado,
        'leyenda':True,
        'fecha_Ini':start_fecha,
        'fecha_Fin':end_fecha,
        'usuario': usuario
    })

@login_required(login_url="login")
def correos(request):
    usuario = CorreosLazzar.objects.get(correo = request.user.email)

    return render(request, 'correos.html',{
        'title':'Correos por pedidos',
        'leyenda':False,
        'usuario': usuario
    })

@login_required(login_url="login")
def correos_fecha(request):
    usuario = CorreosLazzar.objects.get(correo = request.user.email)

    if request.method == 'POST':
        start_fecha = request.POST['start_date']
        end_fecha = request.POST['end_date']

        query = (f"SELECT PENUM, CLINOM, CLITEL4 FROM FPENC P INNER JOIN FCLI C ON C.CLISEQ = P.CLISEQ WHERE PENUM BETWEEN 'P' AND 'P999999' "
                 + "AND PEFECHA BETWEEN '" + start_fecha + "' AND '" + end_fecha + "';") 

        results = run_query(query) 

        resultado = list(results)

    return render(request, 'correos.html',{
        'title':'Correos por pedidos',
        'resultado':resultado,
        'leyenda':True,
        'fecha_Ini':start_fecha,
        'fecha_Fin':end_fecha,
        'usuario': usuario
    })

@login_required(login_url="login")
def comercial(request):

    usuario = CorreosLazzar.objects.get(correo = request.user.email)

    return render(request, 'comercial.html',{
        'usuario': usuario
    })

@login_required(login_url="login")
def status(request):
    usuario = CorreosLazzar.objects.get(correo = request.user.email)

    return render(request, 'status_pedido.html',{
        'title':'Estatus del Pedido',
        'leyenda':False,
        'usuario': usuario
    })

@login_required(login_url="login")
def status_pedido(request):
    usuario = CorreosLazzar.objects.get(correo = request.user.email)
    ventas = request.user.groups.filter(name='ventas').exists() #Admin-Groups Jesus Ibarra 19/12/2023
    acceso_total = request.user.groups.filter(name='acceso_total').exists()
    mesa_control = request.user.groups.filter(name='mesa_control').exists() # End Admin-Groups
    submitted = '0'
    vendedores = []

    #if not usuario.esvendedor:
         #mensaje = "No tienes pedidos activos."
         #return render(request, 'status_pedido_index.html', {'mensaje': mensaje})

    if usuario.admin_group:
            vendedores = CorreosLazzar.objects.filter(group_Proscai = usuario.group_Proscai).values_list()

    if usuario.administrador:
            vendedores = CorreosLazzar.objects.filter(esvendedor = usuario.administrador).values_list()

    resumenresultado = None

    if request.method == 'POST':
        agente = request.POST['agente']
        submitted = '1'
        

        if agente == "todos":

            largo = len(vendedores)
            i = 1
            consulta = ""
            
            for vendedor in vendedores:
                if i == largo:
                    consulta = consulta + "PEPAR1 = '1" + vendedor[3] + "'"
                    i += 1
                else:
                    consulta = consulta + "PEPAR1 = '1" + vendedor[3] + "' OR "
                    i += 1

            query = (f"SELECT PENUM, PEFECHA, PEDESDE, PEVENCE, (SELECT FORMAT(IFNULL(SUM(N.PLCANT),0),0) FROM FPLIN N "
                    + "INNER JOIN FINV I ON I.ISEQ = N.ISEQ "
                    + "WHERE N.PESEQ = L.PESEQ AND I.ICOD >= 'A' AND I.ICOD <= 'Z999999') AS PIEZAS, CONCAT('$', FORMAT(PEBRUTO, 2)), CLINOM, PEPAR1, "
                    + "(SELECT A.AGDESCR FROM FAG A WHERE A.AGTNUM = P.PEPAR1) AS VENDEDOR FROM FPLIN L "
                    + "INNER JOIN FPENC P ON P.PESEQ = L.PESEQ INNER JOIN FCLI C ON C.CLISEQ = P.CLISEQ "
                    + "WHERE (PLCANT - PLSURT) <> 0 AND (" + consulta + ") AND P.PENUM >= 'P' AND P.PENUM "
                    + "<= 'P99999' AND PESPEDIDO = 1 GROUP BY P.PENUM;") 
            
            res_query = (f"SELECT (SELECT COUNT(*) FROM FPENC N WHERE N.PESEQ = L.PESEQ) AS TOTAL_PEDIDOS, "
                        + "(SELECT IFNULL(SUM(N.PLCANT),0) FROM FPLIN N INNER JOIN FINV I ON I.ISEQ = N.ISEQ "
                        + "WHERE N.PESEQ = L.PESEQ AND I.ICOD >= 'A' AND I.ICOD <= 'Z999999') AS TOTAL_PIEZAS, "
                        + "P.PEPAR1, (SELECT A.AGDESCR FROM FAG A WHERE A.AGTNUM = P.PEPAR1) AS VENDEDOR "
                        + "FROM FPLIN L INNER JOIN FPENC P ON P.PESEQ = L.PESEQ "
                        + "WHERE (PLCANT - PLSURT) <> 0 AND (" + consulta + ") AND P.PENUM >= 'P' "
                        + "AND P.PENUM <= 'P99999' AND PESPEDIDO = 1 GROUP BY P.PENUM ORDER BY P.PEPAR1;")
            
        else:
            query = (f"SELECT PENUM, PEFECHA, PEDESDE, PEVENCE, (SELECT FORMAT(IFNULL(SUM(N.PLCANT),0),0) FROM FPLIN N "
                    + "INNER JOIN FINV I ON I.ISEQ = N.ISEQ "
                    + "WHERE N.PESEQ = L.PESEQ AND I.ICOD >= 'A' AND I.ICOD <= 'Z999999') AS PIEZAS, CONCAT('$', FORMAT(PEBRUTO, 2)), CLINOM, PEPAR1, "
                    + "(SELECT A.AGDESCR FROM FAG A WHERE A.AGTNUM = P.PEPAR1) AS VENDEDOR FROM FPLIN L "
                    + "INNER JOIN FPENC P ON P.PESEQ = L.PESEQ INNER JOIN FCLI C ON C.CLISEQ = P.CLISEQ "
                    + "WHERE (PLCANT - PLSURT) <> 0 AND PEPAR1 = '1" + agente + "' AND P.PENUM >= 'P' AND P.PENUM "
                    + "<= 'P99999' AND PESPEDIDO = 1 GROUP BY P.PENUM;")
            
            res_query = (f"SELECT (SELECT COUNT(*) FROM FPENC N WHERE N.PESEQ = L.PESEQ) AS TOTAL_PEDIDOS, "
                        + "(SELECT IFNULL(SUM(N.PLCANT),0) FROM FPLIN N INNER JOIN FINV I ON I.ISEQ = N.ISEQ  WHERE N.PESEQ = L.PESEQ "
                        + "AND I.ICOD >= 'A' AND I.ICOD <= 'Z999999') AS TOTAL_PIEZAS, P.PEPAR1, "
                        + "(SELECT A.AGDESCR FROM FAG A WHERE A.AGTNUM = P.PEPAR1) AS VENDEDOR FROM FPLIN L "
                        + "INNER JOIN FPENC P ON P.PESEQ = L.PESEQ WHERE (PLCANT - PLSURT) <> 0 AND PEPAR1 = '1" + agente 
                        + "' AND P.PENUM >= 'P' AND P.PENUM <= 'P99999' AND PESPEDIDO = 1 GROUP BY P.PENUM ORDER BY P.PEPAR1;") 

        results = run_query(query) 

        if len(results) >= 0:
                result_ped = list(results)
                #resumenresultado = list(results)
        else:
                result_ped = 0
                #resumenresultado = []

        res_results = run_query(res_query) 

        if len(res_results) >= 0:
            resumenresultados = list(res_results)
            totales_por_vendedor = {}

            for item in resumenresultados:
                vendedor = item[3]
                if item[1] is None:
                    piezas = 0
                else:
                    piezas = item[1]
                
                pedido = item[0]

                # Si el vendedor ya existe en el diccionario, actualiza las piezas y pedidos
                if vendedor in totales_por_vendedor:
                    totales_por_vendedor[vendedor]['piezas'] += piezas
                    totales_por_vendedor[vendedor]['pedido'] += pedido
                # Si el vendedor no existe en el diccionario, crea una nueva entrada
                else:
                    totales_por_vendedor[vendedor] = {'vendedor': [vendedor], 'piezas': piezas, 'pedido': pedido}
            
            listado = list(totales_por_vendedor.values())
        else:
            resumenresultados = 0

        return render(request, 'status_pedido.html',{
                'title':'Estatus del Pedido',
                'result_ped':result_ped,
                'leyenda':True,
                'usuario': usuario,
                'vendedores':vendedores,
                'resumenresultado': listado,
                'ventas': ventas, #Admin-Groups Jesus Ibarra 19/12/2023
                'acceso_total': acceso_total,
                'mesa_control': mesa_control, # End Admin-Groups
        })
    

    else:
        query = (f"SELECT PENUM, PEFECHA, PEDESDE, PEVENCE, (SELECT FORMAT(IFNULL(SUM(N.PLCANT),0),0) FROM FPLIN N "
                    + "INNER JOIN FINV I ON I.ISEQ = N.ISEQ "
                    + "WHERE N.PESEQ = L.PESEQ AND I.ICOD >= 'A' AND I.ICOD <= 'Z999999') AS PIEZAS, CONCAT('$', FORMAT(PEBRUTO, 2)), CLINOM, PEPAR1, "
                    + "(SELECT A.AGDESCR FROM FAG A WHERE A.AGTNUM = P.PEPAR1) AS VENDEDOR FROM FPLIN L "
                    + "INNER JOIN FPENC P ON P.PESEQ = L.PESEQ INNER JOIN FCLI C ON C.CLISEQ = P.CLISEQ "
                    + "WHERE (PLCANT - PLSURT) <> 0 AND PEPAR1 = '1" + usuario.cod_Proscai + "' AND P.PENUM >= 'P' AND P.PENUM "
                    + "<= 'P99999' AND PESPEDIDO = 1 GROUP BY P.PENUM;")
        
        res_query = (f"SELECT (SELECT COUNT(*) FROM FPENC N WHERE N.PESEQ = L.PESEQ) AS TOTAL_PEDIDOS, "
                        + "(SELECT IFNULL(SUM(N.PLCANT),0) FROM FPLIN N INNER JOIN FINV I ON I.ISEQ = N.ISEQ  WHERE N.PESEQ = L.PESEQ "
                        + "AND I.ICOD >= 'A' AND I.ICOD <= 'Z999999') AS TOTAL_PIEZAS, P.PEPAR1, "
                        + "(SELECT A.AGDESCR FROM FAG A WHERE A.AGTNUM = P.PEPAR1) AS VENDEDOR FROM FPLIN L "
                        + "INNER JOIN FPENC P ON P.PESEQ = L.PESEQ WHERE (PLCANT - PLSURT) <> 0 AND PEPAR1 = '1" + usuario.cod_Proscai 
                        + "' AND P.PENUM >= 'P' AND P.PENUM <= 'P99999' AND PESPEDIDO = 1 GROUP BY P.PENUM ORDER BY P.PEPAR1;")

        results = run_query(query) 

        if len(results) >= 0:
                result_ped = list(results)
        else:
                result_ped = 0

        res_results = run_query(res_query) 

        if len(res_results) >= 0:
            resumenresultados = list(res_results)
            totales_por_vendedor = {}

            for item in resumenresultados:
                vendedor = item[3] 
                piezas = item[1]
                pedido = item[0]

                # Si el vendedor ya existe en el diccionario, actualiza las piezas y pedidos
                if vendedor in totales_por_vendedor:
                    totales_por_vendedor[vendedor]['piezas'] += piezas
                    totales_por_vendedor[vendedor]['pedido'] += pedido
                # Si el vendedor no existe en el diccionario, crea una nueva entrada
                else:
                    totales_por_vendedor[vendedor] = {'vendedor': [vendedor], 'piezas': piezas, 'pedido': pedido}
            
            listado = list(totales_por_vendedor.values())
        else:
            resumenresultados = 0

        if usuario.admin_group:
            vendedores = CorreosLazzar.objects.filter(group_Proscai = usuario.group_Proscai).values_list()

        if usuario.administrador:
            vendedor = CorreosLazzar.objects.filter(esvendedor = usuario.administrador).values_list()

            return render(request, 'status_pedido.html',{
                'title':'Estatus del Pedido',
                'result_ped':result_ped,
                'leyenda':True,
                'usuario': usuario,
                'vendedores':vendedores,
                'resumenresultado': listado,
                'submitted': submitted,
                'ventas': ventas, #Admin-Groups Jesus Ibarra 19/12/2023
                'acceso_total': acceso_total,
                'mesa_control': mesa_control, # End Admin-Groups
            })
        else:
            return render(request, 'status_pedido.html',{
                'title':'Estatus del Pedido',
                'result_ped':result_ped,
                'leyenda':True,
                'usuario': usuario,
                'vendedores':vendedores,
                'resumenresultado': listado,
                'submitted': submitted,
                'ventas': ventas, #Admin-Groups Jesus Ibarra 19/12/2023
                'acceso_total': acceso_total,
                'mesa_control': mesa_control, # End Admin-Groups
            })

@login_required(login_url="login")
def cartera(request):
    usuario = CorreosLazzar.objects.get(correo = request.user.email)
    ventas = request.user.groups.filter(name='ventas').exists() #Admin-Groups Jesus Ibarra 19/12/2023
    acceso_total = request.user.groups.filter(name='acceso_total').exists()
    mesa_control = request.user.groups.filter(name='mesa_control').exists() # End Admin-Groups
    vendedores = []

    #if not usuario.esvendedor:
         #mensaje = "No tienes cartera de clientes."
         #return render(request, 'status_pedido_index.html', {'mensaje': mensaje})

    if usuario.admin_group:
            vendedores = CorreosLazzar.objects.filter(group_Proscai = usuario.group_Proscai).values_list()

    if usuario.administrador:
            vendedores = CorreosLazzar.objects.filter(esvendedor = usuario.administrador).values_list()

    resumenresultado = None

    if request.method == 'POST':
        agente = request.POST['agente']

        if agente == "todos":

            largo = len(vendedores)
            i = 1
            consulta = ""
            
            for vendedor in vendedores:
                if i == largo:
                    consulta = consulta + "CLIPAR1 = '1" + vendedor[3] + "'"
                    i += 1
                else:
                    consulta = consulta + "CLIPAR1 = '1" + vendedor[3] + "' OR "
                    i += 1

            query = (f"SELECT CLICOD, CLINOM, CLICONT, CLITEL, CLITEL4, "
                    + "(SELECT MAX(P.PEFECHA) FROM FPENC P WHERE P.CLISEQ = C.CLISEQ AND P.PENUM >= 'P' AND P.PENUM <= 'P99999'), "
                    + "AGDESCR FROM FCLI C INNER JOIN FAG A ON A.AGTNUM = C.CLIPAR1 WHERE (" + consulta + ") "
                    + "ORDER BY CLICOD AND CLIPAR1;") 
            
            res_query = (f"SELECT AGDESCR, COUNT(CLINOM) FROM FCLI C INNER JOIN FAG A ON A.AGTNUM = C.CLIPAR1 "
                        + "WHERE (" + consulta + ") GROUP BY CLIPAR1;")

        else:
            query = (f"SELECT CLICOD, CLINOM, CLICONT, CLITEL, CLITEL4, "
                    + "(SELECT MAX(P.PEFECHA) FROM FPENC P WHERE P.CLISEQ = C.CLISEQ AND P.PENUM >= 'P' AND P.PENUM <= 'P99999'), "
                    + "AGDESCR FROM FCLI C INNER JOIN FAG A ON A.AGTNUM = C.CLIPAR1 WHERE CLIPAR1 = '1" + agente + "' ORDER BY CLICOD;")
            
            res_query = (f"SELECT AGDESCR, COUNT(CLINOM) FROM FCLI C INNER JOIN FAG A ON A.AGTNUM = C.CLIPAR1 "
                        + "WHERE CLIPAR1 = '1" + agente + "' GROUP BY CLIPAR1;") 

        results = run_query(query) 

        if len(results) >= 0:
                result_ped = list(results)
                #resumenresultado = list(results)
        else:
                result_ped = 0
                #resumenresultado = []

        res_results = run_query(res_query) 

        if len(res_results) >= 0:
            resumenresultados = list(res_results)
            totales_por_vendedor = {}

            for item in resumenresultados:
                vendedor = item[0] 
                cliente = item[1]

                # Si el vendedor ya existe en el diccionario, actualiza las piezas y pedidos
                if vendedor in totales_por_vendedor:
                    totales_por_vendedor[vendedor]['cliente'] += cliente
                # Si el vendedor no existe en el diccionario, crea una nueva entrada
                else:
                    totales_por_vendedor[vendedor] = {'vendedor': [vendedor], 'cliente': cliente}
            
            listado = list(totales_por_vendedor.values())
        else:
            resumenresultados = 0
        
        return render(request, 'cartera.html',{
                'title':'Estatus del Pedido',
                'result_ped':result_ped,
                'leyenda':True,
                'usuario': usuario,
                'vendedores':vendedores,
                'resumenresultado': listado,
                'ventas': ventas, #Admin-Groups Jesus Ibarra 19/12/2023
                'acceso_total': acceso_total,
                'mesa_control': mesa_control, # End Admin-Groups
        })
    
    else:
        query = (f"SELECT CLICOD, CLINOM, CLICONT, CLITEL, CLITEL4, "
                + "(SELECT MAX(P.PEFECHA) FROM FPENC P WHERE P.CLISEQ = C.CLISEQ AND P.PENUM >= 'P' AND P.PENUM <= 'P99999'), "
                + "AGDESCR FROM FCLI C INNER JOIN FAG A ON A.AGTNUM = C.CLIPAR1 WHERE CLIPAR1 = '1" + usuario.cod_Proscai 
                + "' ORDER BY CLICOD;")
        
        res_query = (f"SELECT AGDESCR, COUNT(CLINOM) FROM FCLI C INNER JOIN FAG A ON A.AGTNUM = C.CLIPAR1 "
                        + "WHERE CLIPAR1 = '1" + usuario.cod_Proscai + "' GROUP BY CLIPAR1;") 

        results = run_query(query) 

        if len(results) >= 0:
                result_ped = list(results)
        else:
                result_ped = 0

        res_results = run_query(res_query) 

        if len(res_results) >= 0:
            resumenresultados = list(res_results)
            totales_por_vendedor = {}

            for item in resumenresultados:
                vendedor = item[0] 
                cliente = item[1]

                # Si el vendedor ya existe en el diccionario, actualiza las piezas y pedidos
                if vendedor in totales_por_vendedor:
                    totales_por_vendedor[vendedor]['cliente'] += cliente
                # Si el vendedor no existe en el diccionario, crea una nueva entrada
                else:
                    totales_por_vendedor[vendedor] = {'vendedor': [vendedor], 'cliente': cliente}
            
            listado = list(totales_por_vendedor.values())
        else:
            resumenresultados = 0

        if usuario.admin_group:
            vendedores = CorreosLazzar.objects.filter(group_Proscai = usuario.group_Proscai).values_list()

        if usuario.administrador:
            vendedores = CorreosLazzar.objects.filter(esvendedor = usuario.administrador).values_list()

            return render(request, 'cartera.html',{
                'title':'Estatus del Pedido',
                'result_ped':result_ped,
                'leyenda':True,
                'usuario': usuario,
                'vendedores':vendedores,
                'resumenresultado': listado,
                'ventas': ventas, #Admin-Groups Jesus Ibarra 19/12/2023
                'acceso_total': acceso_total,
                'mesa_control': mesa_control, # End Admin-Groups
            })
        else:
            return render(request, 'cartera.html',{
                'title':'Estatus del Pedido',
                'result_ped':result_ped,
                'leyenda':True,
                'usuario': usuario,
                'vendedores':vendedores,
                'resumenresultado': listado,
                'ventas': ventas, #Admin-Groups Jesus Ibarra 19/12/2023
                'acceso_total': acceso_total,
                'mesa_control': mesa_control, # End Admin-Groups
            })
        
@login_required(login_url="login") 
def pedido_cliente(request):
    ventas = request.user.groups.filter(name='ventas').exists() #Admin-Groups Jesus Ibarra 19/12/2023
    acceso_total = request.user.groups.filter(name='acceso_total').exists()
    mesa_control = request.user.groups.filter(name='mesa_control').exists() # End Admin-Groups
    if request.method == 'POST':
            codigo = request.POST['variable']
    else:
            codigo = 'detboton'

    query = (f"SELECT P.PENUM, P.PEFECHA, P.PEDESDE, P.PEVENCE,(SELECT CAST(SUM(PLCANT) AS SIGNED) FROM FPLIN L "
            + "INNER JOIN FINV I ON I.ISEQ = L.ISEQ WHERE L.PESEQ = P.PESEQ AND ICOD >= '1' AND ICOD <= 'Z999999') AS PIEZAS, "
            + "CONCAT('$', FORMAT(PEBRUTO, 2)), CLINOM, (SELECT AGDESCR FROM FAG A WHERE A.AGTNUM = P.PEPAR1) AS VENDEDOR FROM FPENC P "
            + "INNER JOIN FCLI C ON C.CLISEQ = P.CLISEQ WHERE C.CLICOD = '" + codigo + "' AND P.PENUM >= 'P' AND P.PENUM <= 'P99999' "
            + "ORDER BY P.PENUM;")
    
    query_detalle = (f"SELECT P.PENUM, I.ICOD, I.IDESCR, L.PLCANT, L.PLSURT, (L.PLCANT-L.PLSURT), "
                    + "CONCAT('$', FORMAT(PLPRECI, 2)), CONCAT('$', FORMAT(L.PLCANT*PLPRECI, 2)) FROM FPENC P "
                + "INNER JOIN FPLIN L ON L.PESEQ = P.PESEQ INNER JOIN FINV I ON I.ISEQ = L.ISEQ "
                + "INNER JOIN FCLI C ON C.CLISEQ = P.CLISEQ WHERE C.CLICOD = '" + codigo 
                + "' AND P.PENUM >= 'P' AND P.PENUM <= 'P99999' ORDER BY P.PENUM;")
    
    total_query = (f"SELECT P.PENUM, SUM(L.PLCANT), SUM(L.PLSURT), SUM((L.PLCANT-L.PLSURT)), "
                   + "CONCAT('$', FORMAT(P.PEBRUTO, 2)) FROM FPENC P "
                   + "INNER JOIN FPLIN L ON L.PESEQ = P.PESEQ INNER JOIN FINV I ON I.ISEQ = L.ISEQ "
                   + "INNER JOIN FCLI C ON C.CLISEQ = P.CLISEQ WHERE C.CLICOD = '" + codigo
                   + "' AND P.PENUM >= 'P' AND P.PENUM <= 'P99999' GROUP BY P.PENUM;")

    results = run_query(query)
    resultado = list(results)

    results_detalle = run_query(query_detalle)
    resultado_detalle = list(results_detalle)

    total_cli = run_query(total_query)
    totales_cli = list(total_cli)

    return render(request, 'pedidos_cliente.html', {
    'title':codigo,
    'resultado': resultado,
    'detalle': resultado_detalle,
    'totales_cli': totales_cli,
    'leyenda': bool(resultado),
    'ventas': ventas, #Admin-Groups Jesus Ibarra 19/12/2023
    'acceso_total': acceso_total,
    'mesa_control': mesa_control, # End Admin-Groups
}) 

@login_required(login_url="login")
def existencias(request):
    usuario = CorreosLazzar.objects.get(correo=request.user.email)
    vendedores = None

    if usuario.admin_group:
        vendedores = CorreosLazzar.objects.filter(group_Proscai=usuario.group_Proscai).values_list()

    return render(request, 'existencias.html', {'vendedores': vendedores, 'usuario': usuario})

@login_required(login_url="login")
def status_pedido_index(request):
    usuario = CorreosLazzar.objects.get(correo=request.user.email)
    vendedores = None

    if usuario.admin_group:
        vendedores = CorreosLazzar.objects.filter(group_Proscai=usuario.group_Proscai).values_list()

    return render(request, 'status_pedido_index.html', {'vendedores': vendedores, 'usuario': usuario})

@login_required(login_url="login")
def embarque(request):
    now = datetime.now()
    usuario = CorreosLazzar.objects.get(correo = request.user.email)
    ventas = request.user.groups.filter(name='ventas').exists() #Admin-Groups Jesus Ibarra 19/12/2023
    acceso_total = request.user.groups.filter(name='acceso_total').exists()
    mesa_control = request.user.groups.filter(name='mesa_control').exists() # End Admin-Groups

    if usuario.admin_group:
            vendedores = CorreosLazzar.objects.filter(group_Proscai = usuario.group_Proscai).values_list()

    if usuario.administrador:
            vendedores = CorreosLazzar.objects.filter(esvendedor = usuario.administrador).values_list()

    if request.method == 'POST':
        agente = request.POST['agente']
        fecha = request.POST['start_date']
        fecha_final = request.POST['end_date']

        if agente == "todos":

            largo = len(vendedores)
            i = 1
            consulta = ""
            
            for vendedor in vendedores:
                if i == largo:
                    consulta = consulta + "D.DPAR1 = '1" + vendedor[3] + "'"
                    i += 1
                else:
                    consulta = consulta + "D.DPAR1 = '1" + vendedor[3] + "' OR "
                    i += 1

            query = (f"SELECT D.DREFER, D.DFECHA, C.CLINOM, D.DNUM, CONCAT('$', FORMAT(DBRUTO, 2)) AS MONTO, DTALON, "    #MODIFICACIÓN DE QUERY POR ERROR MES OCTUBRE / SE OPTIMIZÓ Y DISMINUYO EL TIEMPO DE CARGA / JESÚS IBARRA 15/DIC/2023
                    + "C4.COML4 AS GUIA, A.AGDESCR AS VENDEDOR,"
                    + "FORMAT(SUM(N.AICANTF), 0) AS TOTAL "
                    + "FROM FDOC D "
                    + "INNER JOIN FCLI C ON C.CLISEQ = D.CLISEQ "
                    + "LEFT JOIN FCOMENT C4 ON C4.COMDNUM = D.DNUM "
                    + "INNER JOIN FAG A ON A.AGTNUM = D.DPAR1 "
                    + "LEFT JOIN FAXINV N ON N.DSEQ = D.DSEQ "
                    + f"WHERE D.DFECHA BETWEEN '" + fecha + "' AND '" + fecha_final + "' AND D.DNUM >= 'F0' AND D.DNUM <= 'FE99999999' "
                    + f"AND  (" + consulta + ") AND D.DCANCELADA = 0 "
                    + "GROUP BY D.DREFER, D.DFECHA, C.CLINOM, D.DNUM, DBRUTO, DTALON, C4.COML4, A.AGDESCR "
                    + "ORDER BY D.DFECHA")
            
        else: 
            query = (f"SELECT D.DREFER, D.DFECHA, C.CLINOM, D.DNUM, CONCAT('$', FORMAT(DBRUTO, 2)), DTALON, "
                    + "(SELECT COML4 FROM FCOMENT C WHERE C.COMDNUM = D.DNUM) AS GUIA,  " 
                    + "(SELECT A.AGDESCR FROM FAG A WHERE A.AGTNUM = D.DPAR1) AS VENDEDOR,"
                    + "(SELECT FORMAT(SUM(N.AICANTF), 0) FROM FAXINV N WHERE N.DSEQ = D.DSEQ) "
                    + "FROM FDOC D "
                    + "INNER JOIN FCLI C ON C.CLISEQ = D.CLISEQ "
                    + "WHERE D.DFECHA BETWEEN '" + fecha + "' AND '" + fecha_final + "' AND D.DNUM >= 'F0' AND D.DNUM <= 'FE99999999' "
                    + "AND D.DPAR1 = '1" + agente + "' AND D.DCANCELADA = 0 "
                    + "ORDER BY D.DFECHA; ") 

        results = run_query(query) 

        if len(results) >= 0:
                result_ped = list(results)
        else:
                result_ped = 0

        return render(request, 'embarque.html',{
                'title':'Pedidos embarcados',
                'result_ped':result_ped,
                'start_date':fecha,
                'end_fecha':fecha_final,
                'leyenda':True,
                'usuario': usuario,
                'vendedores':vendedores,
                'now': now,
                'ventas': ventas, #Admin-Groups Jesus Ibarra 19/12/2023
                'acceso_total': acceso_total,
                'mesa_control': mesa_control, # End Admin-Groups
        })
    
    else:
        query = (f"SELECT DREFER, DFECHA, C.CLINOM, DNUM, CONCAT('$', FORMAT(DBRUTO, 2)), DTALON, (SELECT COML4 FROM FCOMENT C WHERE C.COMDNUM = D.DNUM) AS GUIA, "
                    + "(SELECT A.AGDESCR FROM FAG A WHERE A.AGTNUM = D.DPAR1) AS VENDEDOR, "
                    + "(SELECT FORMAT(SUM(N.AICANTF), 0) FROM FAXINV N WHERE N.DSEQ = D.DSEQ) "
                    + "FROM FDOC D "
                    + "LEFT JOIN FCLI C ON C.CLISEQ = D.CLISEQ "
                    + "WHERE D.DFECHA = date(now()) AND D.DNUM >= 'F0' AND D.DNUM <= 'FE99999999' "
                    + "AND D.DPAR1 = '1" + usuario.cod_Proscai + "' AND D.DCANCELADA = 0 "
                    + "ORDER BY DFECHA; ") 

        results = run_query(query) 

        if len(results) >= 0:
                result_ped = list(results)
        else:
                result_ped = 0

        if usuario.admin_group:
            vendedores = CorreosLazzar.objects.filter(group_Proscai = usuario.group_Proscai).values_list()

        if usuario.administrador:
            vendedores = CorreosLazzar.objects.filter(esvendedor = usuario.administrador).values_list()

           
            return render(request, 'embarque.html',{
                'title':'Estatus del Pedido',
                'result_ped':result_ped,
                'leyenda':True,
                'usuario': usuario,
                'vendedores':vendedores,
                'now': now,
                'ventas': ventas, #Admin-Groups Jesus Ibarra 19/12/2023
                'acceso_total': acceso_total,
                'mesa_control': mesa_control, # End Admin-Groups
            })
        
        else:
            # Mayer: Corrección variable vendedores, se pasaba como nulo y ahora se le asigan el codigo del vendedor - 08/09/2023
            vendedores = usuario.cod_Proscai

            return render(request, 'embarque.html',{
                'title':'Estatus del Pedido',
                'result_ped':result_ped,
                'leyenda':True,
                'usuario': usuario,
                'vendedores':vendedores,
                'now': now,
                'ventas': ventas, #Admin-Groups Jesus Ibarra 19/12/2023
                'acceso_total': acceso_total,
                'mesa_control': mesa_control, # End Admin-Groups
            })
        
@login_required(login_url="login")
def embarque_vender(request):
    now = datetime.now()
    usuario = CorreosLazzar.objects.get(correo = request.user.email)
    ventas = request.user.groups.filter(name='ventas').exists() #Admin-Groups Jesus Ibarra 19/12/2023
    acceso_total = request.user.groups.filter(name='acceso_total').exists()
    mesa_control = request.user.groups.filter(name='mesa_control').exists() # End Admin-Groups

    if usuario.vender_group:
            vendedores = CorreosLazzar.objects.filter(cod_Proscai = usuario.cod_Proscai).values_list()

    if request.method == 'POST':
        fecha = request.POST['start_date']
        # Mayer: Se agrega la segunda fecha para el query - 08/09/2023
        fechaFin = request.POST['end_date']

        largo = len(vendedores)
        i = 1
        consulta = ""
            
        for vendedor in vendedores:
                if i == largo:
                    consulta = consulta + "D.DPAR1 = '1" + vendedor[3] + "'"
                    i += 1
                else:
                    consulta = consulta + "D.DPAR1 = '1" + vendedor[3] + "' OR "
                    i += 1

        # Mayer: Se corrige el query - 08/09/2023
        # """ query = (f"SELECT DREFER, DNUM, CONCAT('$', FORMAT(DBRUTO, 2)), DTALON, (SELECT COML4 FROM FCOMENT C WHERE C.COMDNUM = D.DNUM) AS GUIA, "
        #             + "(SELECT A.AGDESCR FROM FAG A WHERE A.AGTNUM = D.DPAR1) AS VENDEDOR FROM FDOC D WHERE " 
        #             + "D.DFECHA = '" + fecha + "' AND D.DNUM >= 'F0' AND D.DNUM <= 'FE99999999' "
        #             + "AND (" + consulta + ") AND D.DCANCELADA = 0;") """
        
        query = ("SELECT DREFER, DFECHA, C.CLINOM, DNUM, CONCAT('$', FORMAT(DBRUTO, 2)), DTALON, "
                + "(SELECT COML4 FROM FCOMENT C WHERE C.COMDNUM = D.DNUM) AS GUIA, "
                + "(SELECT A.AGDESCR FROM FAG A WHERE A.AGTNUM = D.DPAR1) AS VENDEDOR, "
                + "(SELECT FORMAT(SUM(N.AICANTF), 0) FROM FAXINV N WHERE N.DSEQ = D.DSEQ) "
                + "FROM FDOC D "
                + "LEFT JOIN FCLI C ON C.CLISEQ = D.CLISEQ "
                + "WHERE D.DFECHA >= '" + fecha + "' AND D.DFECHA <= '" + fechaFin + "' AND D.DNUM >= 'F0' AND D.DNUM <= 'FE99999999' "
                + "AND (" + consulta + ") AND D.DCANCELADA = 0;")
            
    else:
        # Mayer: Se corrige el query - 08/09/2023
        # """ query = (f"SELECT DREFER, DNUM, CONCAT('$', FORMAT(DBRUTO, 2)), DTALON, (SELECT COML4 FROM FCOMENT C WHERE C.COMDNUM = D.DNUM) AS GUIA, "
        #         + "(SELECT A.AGDESCR FROM FAG A WHERE A.AGTNUM = D.DPAR1) AS VENDEDOR FROM FDOC D "
        #         + "WHERE D.DFECHA = '" + fecha + "' AND D.DNUM >= 'F0' AND D.DNUM <= 'FE99999999' ")  """

        
        query = ("SELECT DREFER, DFECHA, C.CLINOM, DNUM, CONCAT('$', FORMAT(DBRUTO, 2)), DTALON, "
                + "(SELECT COML4 FROM FCOMENT C WHERE C.COMDNUM = D.DNUM) AS GUIA, "
                + "(SELECT A.AGDESCR FROM FAG A WHERE A.AGTNUM = D.DPAR1) AS VENDEDOR, "
                + "(SELECT FORMAT(SUM(N.AICANTF), 0) FROM FAXINV N WHERE N.DSEQ = D.DSEQ) "
                + "FROM FDOC D "
                + "LEFT JOIN FCLI C ON C.CLISEQ = D.CLISEQ "
                + "WHERE D.DFECHA >= '" + fecha + "' AND D.DFECHA <= '" + fechaFin + "' AND D.DNUM >= 'F0' AND D.DNUM <= 'FE99999999' "
                + "AND (" + consulta + ") AND D.DCANCELADA = 0;")

    results = run_query(query) 

    if len(results) >= 0:
                result_ped = list(results)
    else:
                result_ped = 0

    return render(request, 'embarque.html',{
                'title':'Pedidos embarcados',
                'result_ped':result_ped,
                'leyenda':True,
                'usuario': usuario,
                'vendedores':vendedores,
                'now': now,
                'ventas': ventas, #Admin-Groups Jesus Ibarra 19/12/2023
                'acceso_total': acceso_total,
                'mesa_control': mesa_control, # End Admin-Groups
        })
    
@login_required(login_url="login")
def detalle_activos_ventas(request):
    ventas = request.user.groups.filter(name='ventas').exists() #Admin-Groups Jesus Ibarra 19/12/2023
    acceso_total = request.user.groups.filter(name='acceso_total').exists()
    mesa_control = request.user.groups.filter(name='mesa_control').exists() # End Admin-Groups
    if request.method == 'POST':
        folio = request.POST['variable']
    else:
        folio = 'detboton'

    query = (f"SELECT P.PEFECHA, P.PEFECHAEMPAQUE, P.PEDESDE, P.PEVENCE FROM FPENC P " 
            + "WHERE P.PENUM = '" + folio + "' ")
    results = run_query(query)
    fecha = list(results)

    #------CODIGOS PENDIENTES DE SURIR-------
    # query = (f"SELECT MID(I.ICOD,3,10) AS CODIGO, I.IDESCR AS DESCRIPCION, (L.PLCANT-PLSURT-PLASIGNADO) AS PENDIENTE FROM FPENC P "
    #         + "INNER JOIN FPLIN L ON L.PESEQ = P.PESEQ INNER JOIN FINV I ON I.ISEQ = L.ISEQ WHERE P.PENUM = '"
    #         + folio + "' AND (L.PLCANT-PLSURT-PLASIGNADO) != 0 AND I.ICOD >= '1';")
    
    # results = run_query(query)
    # codigos = list (results)

    # existencias = []
    # total_pendiente = 0

    # for codigo in codigos:
    #     query_exis = (f"SELECT existencia FROM Exitencia WHERE CODIGO = '{codigo[0]}'")
    #     exis_cod = run_query_sql(query_exis)

    #     if len(exis_cod) > 0:
    #         for exis in exis_cod:
    #             exis_val = exis[0]
    #     else:  
    #         exis_val = 0



    #     query = (f"SELECT PL.PLCANT-PL.PLSURT AS PENDIENTE, P.PENUM, MIN(P.PEVENCE) FROM FPLIN PL "
    #             + f"INNER JOIN FINV I ON I.ISEQ = PL.ISEQ INNER JOIN FFAM F ON F.FAMTNUM = I.IFAM6 "
    #             + f"INNER JOIN FPENC P ON P.PESEQ = PL.PESEQ WHERE MID(I.ICOD,3,10) = '{codigo[0]}' "
    #             + f"AND (PL.PLCANT-PL.PLSURT) > 0 AND PLTIPMV = 'E' AND P.PEINICIAL = 0 AND P.PEPAR1 = '1PW';")
        
    #     total_pendiente += codigo[2]

    #     results = run_query(query)
    #     producciones = list(results)

    #     if producciones[0][0] is None:
    #         query = (f"SELECT PL.PLCANT-PL.PLSURT AS PENDIENTE, P.PENUM, MIN(P.PEVENCE) FROM FPLIN PL "
    #                 + f"INNER JOIN FINV I ON I.ISEQ = PL.ISEQ INNER JOIN FFAM F ON F.FAMTNUM = I.IFAM6 "
    #                 + f"INNER JOIN FPENC P ON P.PESEQ = PL.PESEQ WHERE MID(I.ICOD,3,10) = '{codigo[0]}' "
    #                 + f" AND (PL.PLCANT-PL.PLSURT) > 0 AND PLTIPMV = 'O' AND P.PEINICIAL = 0 AND P.PEPAR1 = '1PW';")

    #         results = run_query(query)
    #         compras = list(results)

    #         existencia_data = {
    #             'codigo': codigo[0],
    #             'descripcion': codigo[1],
    #             'pendiente': codigo[2],
    #             'existencia': exis_val,
    #             'pendiente_produccion': compras[0][0],
    #             'oren': compras[0][1],
    #             'fecha': compras[0][2]
    #         }
            
    #     else:
    #         existencia_data = {
    #             'codigo': codigo[0],
    #             'descripcion': codigo[1],
    #             'pendiente': codigo[2],
    #             'existencia': exis_val,
    #             'pendiente_produccion': producciones[0][0],
    #             'oren': producciones[0][1],
    #             'fecha': producciones[0][2]
    #         }

        # Agregar los datos de existencia a la lista existencias
        # existencias.append(existencia_data)

    # ---------bordados-----------------
    query = (f"SELECT P.PENUM, P.PEFECHA, P.PEDESDE, P.PEVENCE," 
            +   "(SELECT C.COML1 FROM FCOMENT C WHERE C.COMSEQFACT = concat(10,P.PESEQ)) AS COMENT_1,"
            +   "(SELECT C.COML2 FROM FCOMENT C WHERE C.COMSEQFACT = concat(10,P.PESEQ)) AS COMENT_2,"
            +   "(SELECT C.COML3 FROM FCOMENT C WHERE C.COMSEQFACT = concat(10,P.PESEQ)) AS COMENT_3,"
            +   "(SELECT C.COML4 FROM FCOMENT C WHERE C.COMSEQFACT = concat(10,P.PESEQ)) AS COMENT_4 "
            +   "FROM FPENC P "
            +   "WHERE P.PEOTROTXT = '" + folio 
            +   "' AND P.PEPAR0 >= '7' "
            +   " AND P.PEPAR0 <= '8ZZZZZ' "
            +   "AND P.PENUM >= 'E' "
            +   "AND P.PENUM <= 'E999999999';")

    results = run_query(query)
    segresultado = list(results)

    largo = len(segresultado)
    i = 1
    consulta = ""

    if largo > 0:
        for orden in segresultado:
            if i == largo:
                consulta = consulta + "P.PENUM = '" + orden[0].strip() + "'"
                i += 1
            else:
                consulta = consulta + "P.PENUM = '" + orden[0].strip() + "' OR "
                i += 1

        detalle_bord = (f"SELECT P.PENUM, I.ICOD, I.IDESCR, L.PLCANT, L.PLSURT, (L.PLCANT-L.PLSURT) FROM FPENC P "
                + "INNER JOIN FPLIN L ON L.PESEQ = P.PESEQ INNER JOIN FINV I ON I.ISEQ = L.ISEQ WHERE "
                + "(" + consulta + ") ORDER BY P.PENUM;")
    
        ops_bord = run_query(detalle_bord)
        detalle_bordados = list(ops_bord)

        total_query_bor = (f"SELECT P.PENUM, SUM(L.PLCANT), SUM(L.PLSURT), SUM((L.PLCANT-L.PLSURT)) FROM FPENC P "
                + "INNER JOIN FPLIN L ON L.PESEQ = P.PESEQ INNER JOIN FINV I ON I.ISEQ = L.ISEQ WHERE "
                + "(" + consulta + ") GROUP BY P.PENUM;")
        
        total_bor = run_query(total_query_bor)
        totales_bor = list(total_bor)
    else:
        detalle_bordados = None
        totales_bor = None

# ---------ALMACEN-----------------
    query = (f"SELECT P.PENUM, (SELECT C.COML5 FROM FCOMENT C WHERE C.COMSEQFACT = concat(10,P.PESEQ)) AS ALMACEN "
                + "FROM FPENC P WHERE P.PENUM = '" + folio + "';")
        
    res_comentario = run_query(query)
    almacen = list (res_comentario)
        
    total_alm = 0
    total_surt = 0
    total_pendi = 0

    query_alm = (f"SELECT P.PENUM, I.ICOD, I.IDESCR, L.PLCANT, L.PLSURT, (L.PLCANT-L.PLSURT) FROM FPENC P "
                    + "INNER JOIN FPLIN L ON L.PESEQ = P.PESEQ INNER JOIN FINV I ON I.ISEQ = L.ISEQ WHERE "
                    + "P.PENUM = '" + folio + "' ORDER BY I.ICOD;")

    alm = run_query(query_alm)
    detalle_alm = list(alm)

    for item_alm in detalle_alm:
        total_alm += item_alm[3]

    total_surt = sum(item[4] for item in detalle_alm)
    total_pendi = sum(item[5] for item in detalle_alm)


    return render(request, 'detalle_activos_ventas.html', {
        'title': folio,
        'fecha': fecha,
        # 'existencias': existencias,
        # 'total_pendiente': total_pendiente,
        'totales_bor': totales_bor,
        'detalle_bordados': detalle_bordados,
        'segresultado': segresultado,
        'almacen':almacen,
        'total_surt':total_surt,
        'total_alm':total_alm,
        'total_pendi':total_pendi,
        'detalle_alm':detalle_alm,
        'ventas': ventas, #Admin-Groups Jesus Ibarra 19/12/2023
        'acceso_total': acceso_total,
        'mesa_control': mesa_control, # End Admin-Groups
    })


# Mayer Vista Pedidos Ingresados - 08/09/2023
@login_required(login_url="login")
def ingresados(request):
    now = datetime.now()
    usuario = CorreosLazzar.objects.get(correo = request.user.email)
    ventas = request.user.groups.filter(name='ventas').exists() #Admin-Groups Jesus Ibarra 19/12/2023
    acceso_total = request.user.groups.filter(name='acceso_total').exists()
    mesa_control = request.user.groups.filter(name='mesa_control').exists() # End Admin-Groups

    if usuario.admin_group:
            vendedores = CorreosLazzar.objects.filter(group_Proscai = usuario.group_Proscai).values_list()

    if usuario.administrador:
            vendedores = CorreosLazzar.objects.filter(esvendedor = usuario.administrador).values_list()

    if request.method == 'POST':
        agente = request.POST['agente']
        fecha = request.POST['start_date']
        fechafin = request.POST['end_date']

        if fecha == "" or fechafin == "":
             return render(request, 'ingresados.html',{
                'title':'Pedidos ingresados',
                'usuario': usuario,
                'leyenda':False,
                'now': now,
                'ventas': ventas, #Admin-Groups Jesus Ibarra 19/12/2023
                'acceso_total': acceso_total,
                'mesa_control': mesa_control, # End Admin-Groups
            })

        if agente == "todos":

            largo = len(vendedores)
            i = 1
            consulta = ""
            
            for vendedor in vendedores:
                if i == largo:
                    consulta = consulta + "P.PEPAR1 = '1" + vendedor[3] + "'"
                    i += 1
                else:
                    consulta = consulta + "P.PEPAR1 = '1" + vendedor[3] + "' OR "
                    i += 1

            query = (f"SELECT PENUM, PEFECHA, (SELECT FORMAT(IFNULL(SUM(N.PLCANT),0),0) FROM FPLIN N "
                + "INNER JOIN FINV I ON I.ISEQ = N.ISEQ WHERE N.PESEQ = L.PESEQ AND I.ICOD >= 'A' "
                + "AND I.ICOD <= 'Z999999') AS PIEZAS, CONCAT('$', FORMAT(PEBRUTO, 2)), CLINOM, PEPAR1, "
                + "(SELECT A.AGDESCR FROM FAG A WHERE A.AGTNUM = P.PEPAR1) AS VENDEDOR FROM FPLIN L "
                + "INNER JOIN FPENC P ON P.PESEQ = L.PESEQ INNER JOIN FCLI C ON C.CLISEQ = P.CLISEQ "
                + "WHERE PEFECHA >= '" + fecha + "' AND PEFECHA <= '" + fechafin 
                + "' AND (" + consulta + ") AND P.PENUM >= 'P' AND P.PENUM <= "
                + "'P99999' AND PESPEDIDO = 1 GROUP BY P.PENUM;")
            
        else:
            query = (f"SELECT PENUM, PEFECHA, (SELECT FORMAT(IFNULL(SUM(N.PLCANT),0),0) FROM FPLIN N "
                + "INNER JOIN FINV I ON I.ISEQ = N.ISEQ WHERE N.PESEQ = L.PESEQ AND I.ICOD >= 'A' "
                + "AND I.ICOD <= 'Z999999') AS PIEZAS, CONCAT('$', FORMAT(PEBRUTO, 2)), CLINOM, PEPAR1, "
                + "(SELECT A.AGDESCR FROM FAG A WHERE A.AGTNUM = P.PEPAR1) AS VENDEDOR FROM FPLIN L "
                + "INNER JOIN FPENC P ON P.PESEQ = L.PESEQ INNER JOIN FCLI C ON C.CLISEQ = P.CLISEQ "
                + "WHERE PEFECHA >= '" + fecha + "' AND PEFECHA <= '" + fechafin 
                + "' AND P.PEPAR1 = '1" + agente + "' AND P.PENUM >= 'P' AND P.PENUM <= "
                + "'P99999' AND PESPEDIDO = 1 GROUP BY P.PENUM; ")

        results = run_query(query) 

        if len(results) >= 0:
                result_ped = list(results)
        else:
                result_ped = 0

        return render(request, 'ingresados.html',{
                'title':'Pedidos ingresados',
                'result_ped':result_ped,
                'leyenda':True,
                'usuario': usuario,
                'vendedores':vendedores,
                'now': now,
                'ventas': ventas, #Admin-Groups Jesus Ibarra 19/12/2023
                'acceso_total': acceso_total,
                'mesa_control': mesa_control, # End Admin-Groups
        })
    
    else:
        vendedores = usuario.cod_Proscai

        query = (f"SELECT PENUM, PEFECHA, (SELECT FORMAT(IFNULL(SUM(N.PLCANT),0),0) FROM FPLIN N "
                + "INNER JOIN FINV I ON I.ISEQ = N.ISEQ WHERE N.PESEQ = L.PESEQ AND I.ICOD >= 'A' "
                + "AND I.ICOD <= 'Z999999') AS PIEZAS, CONCAT('$', FORMAT(PEBRUTO, 2)), CLINOM, PEPAR1, "
                + "(SELECT A.AGDESCR FROM FAG A WHERE A.AGTNUM = P.PEPAR1) AS VENDEDOR FROM FPLIN L "
                + "INNER JOIN FPENC P ON P.PESEQ = L.PESEQ INNER JOIN FCLI C ON C.CLISEQ = P.CLISEQ "
                + "WHERE PEFECHA = date(now()) AND (PEPAR1 = '1" + usuario.cod_Proscai
                + "') AND P.PENUM >= 'P' AND P.PENUM <= 'P99999' AND PESPEDIDO = 1 GROUP BY P.PENUM;") 

        results = run_query(query) 

        if len(results) >= 0:
                result_ped = list(results)
        else:
                result_ped = 0

        if usuario.admin_group:
            vendedores = CorreosLazzar.objects.filter(group_Proscai = usuario.group_Proscai).values_list()

        if usuario.administrador:
            vendedores = CorreosLazzar.objects.filter(esvendedor = usuario.administrador).values_list()

           
            return render(request, 'ingresados.html',{
                'title':'Pedidos ingresados',
                'result_ped':result_ped,
                'leyenda':True,
                'usuario': usuario,
                'vendedores':vendedores,
                'now': now,
                'ventas': ventas, #Admin-Groups Jesus Ibarra 19/12/2023
                'acceso_total': acceso_total,
                'mesa_control': mesa_control, # End Admin-Groups
            })
        
        else:
            return render(request, 'ingresados.html',{
                'title':'Pedidos ingresados',
                'result_ped':result_ped,
                'leyenda':True,
                'usuario': usuario,
                'vendedores':vendedores,
                'now': now,
                'ventas': ventas, #Admin-Groups Jesus Ibarra 19/12/2023
                'acceso_total': acceso_total,
                'mesa_control': mesa_control, # End Admin-Groups
            })
            

# Mayer Vista Pedidos Ingresados por vendedor - 08/09/2023    
@login_required(login_url="login")
def ingresados_vender(request):
    now = datetime.now()
    usuario = CorreosLazzar.objects.get(correo = request.user.email)
    ventas = request.user.groups.filter(name='ventas').exists() #Admin-Groups Jesus Ibarra 19/12/2023
    acceso_total = request.user.groups.filter(name='acceso_total').exists()
    mesa_control = request.user.groups.filter(name='mesa_control').exists() # End Admin-Groups
    if usuario.vender_group:
            vendedores = CorreosLazzar.objects.filter(cod_Proscai = usuario.cod_Proscai).values_list()

    if request.method == 'POST':
        fecha = request.POST['start_date']
        fechafin = request.POST['end_date']

        if fecha == "" or fechafin == "":
             return render(request, 'ingresados.html',{
                'title':'Pedidos imgresados',
                'usuario': usuario,
                'leyenda':False,
                'now': now,
                'ventas': ventas, #Admin-Groups Jesus Ibarra 19/12/2023
                'acceso_total': acceso_total,
                'mesa_control': mesa_control, # End Admin-Groups
            })
        
        largo = len(vendedores)
        i = 1
        consulta = ""
            
        for vendedor in vendedores:
                if i == largo:
                    consulta = consulta + "P.PEPAR1 = '1" + vendedor[3] + "'"
                    i += 1
                else:
                    consulta = consulta + "P.PEPAR1 = '1" + vendedor[3] + "' OR "
                    i += 1

        query = (f"SELECT PENUM, PEFECHA, (SELECT FORMAT(IFNULL(SUM(N.PLCANT),0),0) FROM FPLIN N "
                + "INNER JOIN FINV I ON I.ISEQ = N.ISEQ WHERE N.PESEQ = L.PESEQ AND I.ICOD >= 'A' "
                + "AND I.ICOD <= 'Z999999') AS PIEZAS, CONCAT('$', FORMAT(PEBRUTO, 2)), CLINOM, PEPAR1, "
                + "(SELECT A.AGDESCR FROM FAG A WHERE A.AGTNUM = P.PEPAR1) AS VENDEDOR FROM FPLIN L "
                + "INNER JOIN FPENC P ON P.PESEQ = L.PESEQ INNER JOIN FCLI C ON C.CLISEQ = P.CLISEQ "
                + "WHERE PEFECHA >= '" + fecha + "'  AND PEFECHA <= '" + fechafin 
                + "' AND (" + consulta + ") AND P.PENUM >= 'P' AND P.PENUM <= "
                + "'P99999' AND PESPEDIDO = 1 GROUP BY P.PENUM;")
            
    else:
        query = (f"SELECT PENUM, PEFECHA, (SELECT FORMAT(IFNULL(SUM(N.PLCANT),0),0) FROM FPLIN N "
                + "INNER JOIN FINV I ON I.ISEQ = N.ISEQ WHERE N.PESEQ = L.PESEQ AND I.ICOD >= 'A' "
                + "AND I.ICOD <= 'Z999999') AS PIEZAS, CONCAT('$', FORMAT(PEBRUTO, 2)), CLINOM, PEPAR1, "
                + "(SELECT A.AGDESCR FROM FAG A WHERE A.AGTNUM = P.PEPAR1) AS VENDEDOR FROM FPLIN L "
                + "INNER JOIN FPENC P ON P.PESEQ = L.PESEQ INNER JOIN FCLI C ON C.CLISEQ = P.CLISEQ "
                + "WHERE PEFECHA >= '" + fecha + "'  AND PEFECHA <= '" + fechafin 
                + "' AND (" + consulta + ") AND P.PENUM >= 'P' AND P.PENUM <= "
                + "'P99999' AND PESPEDIDO = 1 GROUP BY P.PENUM;")

    results = run_query(query) 

    if len(results) >= 0:
                result_ped = list(results)
    else:
                result_ped = 0

    return render(request, 'ingresados.html',{
                'title':'Pedidos embarcados',
                'result_ped':result_ped,
                'leyenda':True,
                'usuario': usuario,
                'vendedores':vendedores,
                'now': now,
                'ventas': ventas, #Admin-Groups Jesus Ibarra 19/12/2023
                'acceso_total': acceso_total,
                'mesa_control': mesa_control, # End Admin-Groups
        })

@login_required (login_url="login")
def embarque_pedido(request):
    ventas = request.user.groups.filter(name='ventas').exists() #Admin-Groups Jesus Ibarra 19/12/2023
    acceso_total = request.user.groups.filter(name='acceso_total').exists()
    mesa_control = request.user.groups.filter(name='mesa_control').exists() # End Admin-Groups
    pedido = []

    if request.method == 'POST':
        pedido = request.POST.get('pedido', None)

        query = ("SELECT DREFER, DFECHA, C.CLINOM, DNUM, CONCAT('$', FORMAT(DBRUTO, 2)), DTALON, "
                + "(SELECT COML4 FROM FCOMENT C WHERE C.COMDNUM = D.DNUM) AS GUIA, "
                + "(SELECT A.AGDESCR FROM FAG A WHERE A.AGTNUM = D.DPAR1) AS VENDEDOR, "
                + "(SELECT FORMAT(SUM(N.AICANTF), 0) FROM FAXINV N WHERE N.DSEQ = D.DSEQ) "
                + "FROM FDOC D "
                + "INNER JOIN FCLI C ON C.CLISEQ = D.CLISEQ "
                + "AND D.DNUM >= 'F0' AND D.DNUM <= 'FE99999999' "
                + f"WHERE DREFER = '" + pedido + "' "
                + "ORDER BY DFECHA; ")
    
        results = run_query(query)
        resultado = list(results)

        return render(request, 'embarque_pedido.html', {
        'leyenda': True,
        'resultado': resultado,
        'pedido': pedido,
        'ventas': ventas, #Admin-Groups Jesus Ibarra 19/12/2023
        'acceso_total': acceso_total,
        'mesa_control': mesa_control, # End Admin-Groups
        })
    else:
         return render(request, 'embarque_pedido.html', {
              'leyenda': False,
              'ventas': ventas, #Admin-Groups Jesus Ibarra 19/12/2023
              'acceso_total': acceso_total,
              'mesa_control': mesa_control, # End Admin-Groups
         })

@login_required(login_url="login")
def embarque_muestras (request):
    now = datetime.now()
    usuario = CorreosLazzar.objects.get(correo = request.user.email)
    ventas = request.user.groups.filter(name='ventas').exists() #Admin-Groups Jesus Ibarra 19/12/2023
    acceso_total = request.user.groups.filter(name='acceso_total').exists()
    mesa_control = request.user.groups.filter(name='mesa_control').exists() # End Admin-Groups

    if usuario.admin_group:
         vendedores = CorreosLazzar.objects.filter(group_Proscai = usuario.group_Proscai).values_list()

    if usuario.administrador:
         vendedores = CorreosLazzar.objects.filter(esvendedor = usuario.administrador).values_list()

    if request.method == 'POST':
        agente = request.POST['agente']
        desde = request.POST['desde']
        hasta = request.POST['hasta']
    
        if desde == "" or hasta == "":
            return render(request, 'embarque_muestras.html',{
                 'leyenda': False,
                 'vendedores': vendedores,
                 'usuario': usuario,
                 'now': now,
                 'ventas': ventas, #Admin-Groups Jesus Ibarra 09/01/2024
                'acceso_total': acceso_total,
                'mesa_control': mesa_control, # End Admin-Groups
            })
        
        if agente == "todos":
        
            largo = len(vendedores)
            i = 1
            consulta = ""

            for vendedor in vendedores:
                if i == largo:
                    consulta = consulta + "P.PEPAR1 = '1" + vendedor[3] + "'"
                    i += 1
                else:
                    consulta = consulta + "P.PEPAR1 = '1" + vendedor[3] + "' OR "
                    i += 1

            query = (
            f"SELECT P.PEFECHA, D.DFECHA, P.PENUM, DTALON, T.COML4, "  # FECHA, F.SURITDO, FOLIO, CLIENTE
            + "CASE WHEN CLINOM = 'CLIENTE MUESTRAS' THEN(SELECT C.COML2 FROM FCOMENT C WHERE C.COMSEQFACT = CONCAT(10, PESEQ)) ELSE CLINOM END AS CLIENTE, "
            + "IFNULL(AGDESCR,'NO TIENE VENDEDOR'), "  # VENDEDOR
            + "IF((P.PEPZAS - P.PEPZASSURT) = 0, 'COMPLETO', "
            + "IF(P.PEPZASSURT > 0, 'PARCIAL', 'NO SURTIDO')) AS ESTADO, "  # ESTADO
            + "FORMAT("
            + "IFNULL("
            + "   (SELECT SUM(PLSURT) FROM FPLIN L WHERE L.PESEQ = P.PESEQ GROUP BY P.PENUM), 0"  # PZ ENVIADAS
            + "), 0) AS PLSURT, "
            + "(SELECT SUM(AICANT) AS 'PIEZAS RECIBIDAS' FROM FDOC Z "  # PZ RECIBIDAS
            + "INNER JOIN FAXINV A ON A.DSEQ = Z.DSEQ "
            + "WHERE Z.DNUM >= 'TR' AND DNUM <= 'TR99999' AND AIALMACEN = 00 AND DREFER = P.PENUM), "
            + "IFNULL(GROUP_CONCAT(D.DNUM), '') AS DOCUMENTOS, "
            + "(SELECT C.COML1 FROM FCOMENT C WHERE C.COMSEQFACT = CONCAT(10, P.PESEQ)) AS COMENT_1 "  # COMENT_1
            + "FROM FPENC P "
            + "LEFT JOIN FDOC D ON D.DREFER = P.PENUM "
            + "INNER JOIN FCLI C ON C.CLISEQ = P.CLISEQ "
            + "LEFT JOIN FAG A ON A.AGTNUM = P.PEPAR1 "
            + "LEFT JOIN FCOMENT T ON T.COMDNUM = D.DNUM "
            + "WHERE P.PEFECHA BETWEEN '" + desde + "' AND '" + hasta + "' "
            + "AND (" + consulta + ") AND P.PENUM BETWEEN 'M' AND 'M99999' "
            + "AND P.PESPEDIDO = 1 AND (D.DNUM >= 'F' AND D.DNUM <= 'FM9999999' OR D.DNUM IS NULL) "
            + "GROUP BY P.PENUM;"
            )
        else:
            query = (
            f"SELECT P.PEFECHA, D.DFECHA, P.PENUM, DTALON, T.COML4, "  # FECHA, F.SURITDO, FOLIO, CLIENTE
            + "CASE WHEN CLINOM = 'CLIENTE MUESTRAS' THEN(SELECT C.COML2 FROM FCOMENT C WHERE C.COMSEQFACT = CONCAT(10, PESEQ)) ELSE CLINOM END AS CLIENTE, "
            + "IFNULL(AGDESCR,'NO TIENE VENDEDOR'), "  # VENDEDOR
            + "IF((P.PEPZAS - P.PEPZASSURT) = 0, 'COMPLETO', "
            + "IF(P.PEPZASSURT > 0, 'PARCIAL', 'NO SURTIDO')) AS ESTADO, "  # ESTADO
            + "FORMAT("
            + "IFNULL("
            + "   (SELECT SUM(PLSURT) FROM FPLIN L WHERE L.PESEQ = P.PESEQ GROUP BY P.PENUM), 0"  # PZ ENVIADAS
            + "), 0) AS PLSURT, "
            + "(SELECT SUM(AICANT) AS 'PIEZAS RECIBIDAS' FROM FDOC Z "  # PZ RECIBIDAS
            + "INNER JOIN FAXINV A ON A.DSEQ = Z.DSEQ "
            + "WHERE Z.DNUM >= 'TR' AND DNUM <= 'TR99999' AND AIALMACEN = 00 AND DREFER = P.PENUM), "
            + "IFNULL(GROUP_CONCAT(D.DNUM), '') AS DOCUMENTOS, "
            + "(SELECT C.COML1 FROM FCOMENT C WHERE C.COMSEQFACT = CONCAT(10, P.PESEQ)) AS COMENT_1 "  # COMENT_1
            + "FROM FPENC P "
            + "LEFT JOIN FDOC D ON D.DREFER = P.PENUM "
            + "LEFT JOIN FCOMENT T ON T.COMDNUM = D.DNUM "
            + "INNER JOIN FCLI C ON C.CLISEQ = P.CLISEQ "
            + "LEFT JOIN FAG A ON A.AGTNUM = P.PEPAR1 "
            + "WHERE P.PEFECHA BETWEEN '" + desde + "' AND '" + hasta + "' "
            + "AND P.PEPAR1 = '1" + agente + "' AND P.PENUM BETWEEN 'M' AND 'M99999' "
            + "AND P.PESPEDIDO = 1 AND (D.DNUM >= 'F' AND D.DNUM <= 'FM9999999' OR D.DNUM IS NULL) "
            + "GROUP BY P.PENUM;"
            )
        
        results = run_query(query)

        if len(results) >= 0:
            respuesta = list(results)
        else:
            respuesta = 0
        
        return render (request, 'embarque_muestras.html',{
            'leyenda':bool(respuesta),
            'desde':desde,
            'hasta':hasta,
            'respuesta':respuesta,
            'vendedores': vendedores,
            'usuario': usuario,
            'ventas': ventas, #Admin-Groups Jesus Ibarra 19/12/2023
            'acceso_total': acceso_total,
            'mesa_control': mesa_control, # End Admin-Groups
        })
    else:
        vendedores = usuario.cod_Proscai

        query = (
            f"SELECT P.PEFECHA, D.DFECHA, P.PENUM, DTALON, T.COML4, "  # FECHA, F.SURITDO, FOLIO, CLIENTE
            + "CASE WHEN CLINOM = 'CLIENTE MUESTRAS' THEN(SELECT C.COML2 FROM FCOMENT C WHERE C.COMSEQFACT = CONCAT(10, PESEQ)) ELSE CLINOM END AS CLIENTE, "
            + "IFNULL(AGDESCR,'NO TIENE VENDEDOR'), "  # VENDEDOR
            + "IF((P.PEPZAS - P.PEPZASSURT) = 0, 'COMPLETO', "
            + "IF(P.PEPZASSURT > 0, 'PARCIAL', 'NO SURTIDO')) AS ESTADO, "  # ESTADO
            + "FORMAT("
            + "IFNULL("
            + "   (SELECT SUM(PLSURT) FROM FPLIN L WHERE L.PESEQ = P.PESEQ GROUP BY P.PENUM), 0"  # PZ ENVIADAS
            + "), 0) AS PLSURT, "
            + "(SELECT SUM(AICANT) AS 'PIEZAS RECIBIDAS' FROM FDOC Z "  # PZ RECIBIDAS
            + "INNER JOIN FAXINV A ON A.DSEQ = Z.DSEQ "
            + "WHERE Z.DNUM >= 'TR' AND DNUM <= 'TR99999' AND AIALMACEN = 00 AND DREFER = P.PENUM), "
            + "IFNULL(GROUP_CONCAT(D.DNUM), '') AS DOCUMENTOS, "
            + "(SELECT C.COML1 FROM FCOMENT C WHERE C.COMSEQFACT = CONCAT(10, P.PESEQ)) AS COMENT_1 "  # COMENT_1
            + "FROM FPENC P "
            + "LEFT JOIN FDOC D ON D.DREFER = P.PENUM "
            + "LEFT JOIN FCOMENT T ON T.COMDNUM = D.DNUM "
            + "INNER JOIN FCLI C ON C.CLISEQ = P.CLISEQ "
            + "LEFT JOIN FAG A ON A.AGTNUM = P.PEPAR1 "
            + "WHERE P.PEFECHA = date(now()) AND (PEPAR1 = '1" + usuario.cod_Proscai
            + "') AND P.PENUM BETWEEN 'M' AND 'M99999' "
            + "AND P.PESPEDIDO = 1 AND (D.DNUM >= 'F' AND D.DNUM <= 'FM9999999' OR D.DNUM IS NULL) "
            + "GROUP BY P.PENUM;"
        )

        results = run_query(query) 

        if len(results) >= 0:
                respuesta = list(results)
        else:
                respuesta = 0

        if usuario.admin_group:
            vendedores = CorreosLazzar.objects.filter(group_Proscai = usuario.group_Proscai).values_list()

        if usuario.administrador:
            vendedores = CorreosLazzar.objects.filter(esvendedor = usuario.administrador).values_list()
        

            return render(request, 'embarque_muestras.html',{
                    'leyenda':True,
                    'respuesta': respuesta,
                    'usuario': usuario,
                    'vendedores': vendedores,
                    'now': now,
                    'ventas': ventas, #Admin-Groups Jesus Ibarra 19/12/2023
                    'acceso_total': acceso_total,
                    'mesa_control': mesa_control, # End Admin-Groups
            })
        else:
             return render(request, 'embarque_muestras.html',{
                'leyenda':False,
                'respuesta': respuesta,
                'usuario': usuario,
                'vendedores': vendedores,
                'now': now,
                'ventas': ventas, #Admin-Groups Jesus Ibarra 19/12/2023
                'acceso_total': acceso_total,
                'mesa_control': mesa_control, # End Admin-Groups
        })
        
@login_required(login_url='login')
def embarque_muestras_vendedor(request):
    now = datetime.now()
    usuario = CorreosLazzar.objects.get(correo=request.user.email)
    ventas = request.user.groups.filter(name='ventas').exists()  # Admin-Groups Jesus Ibarra 19/12/2023
    acceso_total = request.user.groups.filter(name='acceso_total').exists()
    mesa_control = request.user.groups.filter(name='mesa_control').exists()  # End Admin-Groups

    if usuario.vender_group:
        vendedores = CorreosLazzar.objects.filter(cod_Proscai=usuario.cod_Proscai).values_list()

    if request.method == 'POST':
        desde = request.POST['desde']
        hasta = request.POST['hasta']

        if desde == "" or hasta == "":
            return render(request, 'embarque_muestras.html', {
                'usuario': usuario,
                'leyenda': False,
                'now': now,
                'ventas': ventas,  # Admin-Groups Jesus Ibarra 19/12/2023
                'acceso_total': acceso_total,
                'mesa_control': mesa_control,  # End Admin-Groups
            })

        largo = len(vendedores)
        i = 1
        consulta = ""

        for vendedor in vendedores:
            if i == largo:
                consulta = consulta + "P.PEPAR1 = '1" + vendedor[3] + "'"
                i += 1
            else:
                consulta = consulta + "P.PEPAR1 = '1" + vendedor[3] + "' OR "
                i += 1

        query = (
            f"SELECT P.PEFECHA, D.DFECHA, P.PENUM, DTALON, T.COML4, "  # FECHA, F.SURITDO, FOLIO, CLIENTE
            + "CASE WHEN CLINOM = 'CLIENTE MUESTRAS' THEN(SELECT C.COML2 FROM FCOMENT C WHERE C.COMSEQFACT = CONCAT(10, PESEQ)) ELSE CLINOM END AS CLIENTE, "
            + "IFNULL(AGDESCR,'NO TIENE VENDEDOR'), "  # VENDEDOR
            + "IF((P.PEPZAS - P.PEPZASSURT) = 0, 'COMPLETO', "
            + "IF(P.PEPZASSURT > 0, 'PARCIAL', 'NO SURTIDO')) AS ESTADO, "  # ESTADO
            + "FORMAT("
            + "IFNULL("
            + "(SELECT SUM(PLSURT) FROM FPLIN L WHERE L.PESEQ = P.PESEQ GROUP BY P.PENUM), 0"  # PZ ENVIADAS
            + "), 0) AS PLSURT, "
            + "(SELECT SUM(AICANT) AS 'PIEZAS RECIBIDAS' FROM FDOC Z "  # PZ RECIBIDAS
            + "INNER JOIN FAXINV A ON A.DSEQ = Z.DSEQ "
            + "WHERE Z.DNUM >= 'TR' AND DNUM <= 'TR99999' AND AIALMACEN = 00 AND DREFER = P.PENUM), "
            + "IFNULL(GROUP_CONCAT(D.DNUM), '') AS DOCUMENTOS, "
            + "(SELECT C.COML1 FROM FCOMENT C WHERE C.COMSEQFACT = CONCAT(10, P.PESEQ)) AS COMENT_1 "  # COMENT_1
            + "FROM FPENC P "
            + "LEFT JOIN FDOC D ON D.DREFER = P.PENUM "
            + "LEFT JOIN FCOMENT T ON T.COMDNUM = D.DNUM "
            + "INNER JOIN FCLI C ON C.CLISEQ = P.CLISEQ "
            + "LEFT JOIN FAG A ON A.AGTNUM = P.PEPAR1 "
            + "WHERE P.PEFECHA BETWEEN '" + desde + "' AND '" + hasta + "' "
            + "AND (" + consulta + ") AND P.PENUM BETWEEN 'M' AND 'M99999' "
            + "AND P.PESPEDIDO = 1 AND (D.DNUM >= 'F' AND D.DNUM <= 'FM9999999' OR D.DNUM IS NULL) "
            + "GROUP BY P.PENUM;"
        )
    else:
        query = (
            f"SELECT P.PEFECHA, D.DFECHA, P.PENUM, DTALON, T.COML4, "  # FECHA, F.SURITDO, FOLIO, CLIENTE
            + "CASE WHEN CLINOM = 'CLIENTE MUESTRAS' THEN(SELECT C.COML2 FROM FCOMENT C WHERE C.COMSEQFACT = CONCAT(10, PESEQ)) ELSE CLINOM END AS CLIENTE, "
            + "IFNULL(AGDESCR,'NO TIENE VENDEDOR'), "  # VENDEDOR
            + "IF((P.PEPZAS - P.PEPZASSURT) = 0, 'COMPLETO', "
            + "IF(P.PEPZASSURT > 0, 'PARCIAL', 'NO SURTIDO')) AS ESTADO, "  # ESTADO
            + "FORMAT("
            + "IFNULL("
            + "(SELECT SUM(PLSURT) FROM FPLIN L WHERE L.PESEQ = P.PESEQ GROUP BY P.PENUM), 0"  # PZ ENVIADAS
            + "), 0) AS PLSURT, "
            + "(SELECT SUM(AICANT) AS 'PIEZAS RECIBIDAS' FROM FDOC Z "  # PZ RECIBIDAS
            + "INNER JOIN FAXINV A ON A.DSEQ = Z.DSEQ "
            + "WHERE Z.DNUM >= 'TR' AND DNUM <= 'TR99999' AND AIALMACEN = 00 AND DREFER = P.PENUM), "
            + "IFNULL(GROUP_CONCAT(D.DNUM), '') AS DOCUMENTOS, "
            + "(SELECT C.COML1 FROM FCOMENT C WHERE C.COMSEQFACT = CONCAT(10, P.PESEQ)) AS COMENT_1 "  # COMENT_1
            + "FROM FPENC P "
            + "LEFT JOIN FDOC D ON D.DREFER = P.PENUM "
            + "LEFT JOIN FCOMENT T ON T.COMDNUM = D.DNUM "
            + "INNER JOIN FCLI C ON C.CLISEQ = P.CLISEQ "
            + "LEFT JOIN FAG A ON A.AGTNUM = P.PEPAR1 "
            + "WHERE P.PEFECHA BETWEEN '" + desde + "' AND '" + hasta + "' "
            + "AND (" + consulta + ") AND P.PENUM BETWEEN 'M' AND 'M99999' "
            + "AND P.PESPEDIDO = 1 AND (D.DNUM >= 'F' AND D.DNUM <= 'FM9999999' OR D.DNUM IS NULL) "
            + "GROUP BY P.PENUM;"
        )
    results = run_query(query)

    if len(results) >= 0:
        respuesta = list(results)
    else:
        respuesta = 0

    return render(request, 'embarque_muestras.html', {
        'respuesta': respuesta,
        'usuario': usuario,
        'leyenda': True,
        'vendedores': vendedores,
        'now': now,
        'ventas': ventas,  # Admin-Groups Jesus Ibarra 19/12/2023
        'acceso_total': acceso_total,
        'mesa_control': mesa_control,  # End Admin-Groups
    })
