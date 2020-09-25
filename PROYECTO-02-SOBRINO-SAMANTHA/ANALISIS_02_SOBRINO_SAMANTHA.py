# -*- coding: utf-8 -*-
'''
VARIABLES EN LA BASE DE DATOS ORIGINAL:
register_id
direction
origin
destination
year
date
product
transport_mode
company_name
total_value
'''

import csv #Módulo para el manejo de datos csv.
lista_movimientos=[] #Lista vacía que utilizaremos posteriormente

#Abrimos el archivo csv con un "with" para trabajar con el.
with open('synergy_logistics_database.csv','r',encoding='utf-8-sig') as base_csv:
  lector=csv.DictReader(base_csv,delimiter=',') #Leemos al información como diccionarios
  for linea in lector: lista_movimientos.append(linea) #guardamos los diccionarios en la lista creada anteriormente.

### OPCIÓN 1. Rutas de importación y exportación.
#Crearemos una función para hacer el proceso más eficiente.
def rutas(direccion):  #el parámetro de la función será la dirección del movimiento.
    rutas=[] #listas vacías que se utilizarán:
    rutas_valores=[]
    for ruta in lista_movimientos: #creamos un ciclo for para revisar cada movimiento.
        if ruta["direction"]==direccion: #usamos un if para que sólo se tome en cuenta a las que corresponden a la dirección que se pidió en la función.
            ruta_actual=[ruta['direction'],ruta['origin'],ruta['destination']] #asignamos a la ruta actual los datos que la identifican usando las claves del diccionario.
            if ruta_actual not in rutas: #creamos una lista de todas las rutas distintas de esta dirección.
                rutas.append(ruta_actual)
                recuento=0 #iniciamos contadores en cero
                valor=0
                for movimiento in lista_movimientos: #con un for revisamos y almacenamos la información que corresponde a todas las veces que cada ruta fue usada.
                    if ruta_actual==[movimiento['direction'],movimiento['origin'],movimiento['destination']]: #debemos considerar los tres elementos que identifican a la ruta como única.
                        recuento+=1 #contamos cuántas veces fue usada esta ruta
                        valor+=int(movimiento['total_value']) #acumulamos el valor de cada movimiento de la ruta
                val_promedio=valor/recuento #calculamos el promedio por movimiento de la ruta.
                ruta_val= {'origen':ruta['origin'],'destino':ruta['destination'],'recuento':recuento,'total':valor,'valor_promedio':val_promedio} #creamos un diccionario con los datos que calculamos para la ruta actual.
                rutas_valores.append(ruta_val) #hacemos una lista de diccionarios que contiene la información de todas las rutas de esta dirección.
    print("\n\n-->"+str(direccion)) #Imprimos de qué dirección se trata para mejor presentación.
    print(str(len(rutas))+" rutas distintas.") #Para un análisis más detallado, queremos visualizar cuántas rutas totales hay para esta dirección. Esto lo hacemoe mediante la función len.
    #Ordenamos de mayor a menor la lista de rutas según cada uno de los criterios:
        #Demanda (recuento):
    Mas_demandadas=sorted(rutas_valores, key=lambda rutas_valores: rutas_valores['recuento'],reverse=True)
    print("\nLAS 10 RUTAS MÁS DEMANDADAS FUERON:") #Imprimimos títulos para cada lista.
    for i in range(10): #con un for y la función range imprimimos las 10 rutas que se solicitaron.
        print("Origen: " + str(Mas_demandadas[i]['origen'])+", Destino: " + str(Mas_demandadas[i]['destino'])+", con "+ str(Mas_demandadas[i]['recuento'])+" movimientos.")
        #Valor Total
    Mas_valor=sorted(rutas_valores, key=lambda rutas_valores: rutas_valores['total'],reverse=True)
    print("\nLAS 10 RUTAS CON TOTALES MÁS ALTOS FUERON:")
    for i in range(10):
        print("Origen: " + str(Mas_valor[i]['origen'])+", Destino: " + str(Mas_valor[i]['destino'])+", con un total de $"+ str(Mas_valor[i]['total']))
        #Valor promedio por movimiento:
    Mayor_promedio=sorted(rutas_valores, key=lambda rutas_valores: rutas_valores['valor_promedio'],reverse=True)
    print("\nLAS 10 RUTAS CON VALOR PROMEDIO MÁS ALTO:")
    for i in range(10):
        print("Origen: " + str(Mayor_promedio[i]['origen'])+", Destino: " + str(Mayor_promedio[i]['destino'])+", con promedio por movimiento de $"+ str(Mayor_promedio[i]['valor_promedio']))


### OPCIÓN 2. Medio de transporte utilizado.
#Debido a la gran similitud en los procesos, sólo se comentarán las diferencias importantes.
def transporte(direccion):
    medios=[]
    medios_valores=[]
    for medio in lista_movimientos:
        if medio["direction"]==direccion:
            medio_actual=[medio['direction'],medio['transport_mode']] #Los elementos importantes de identificación son nuevamente la dirección y, por supuesto, el medio de transporte.
            if medio_actual not in medios:
                medios.append(medio_actual) #Lista con todos los medios de transporte diferentes.
                recuento=0
                valor=0
                for movimiento in lista_movimientos:
                    if medio_actual==[movimiento['direction'],movimiento['transport_mode']]:
                        recuento+=1
                        valor+=int(movimiento['total_value'])
                val_promedio=valor/recuento
                medio_val= {'medio_transporte':medio['transport_mode'],'recuento':recuento,'total':valor,'valor_promedio':val_promedio}
                medios_valores.append(medio_val)    #Lista de diccionarios con la información a analizar.
    
    ##Imprimimos todos los datos que queremos visualizar.
    print("\n\n-->"+str(direccion))
    ##Nuevamente ordenamos con una función sorted con llave lambda y de mayor a menos usando "reverse=True", la lista de información que creamos.
    Mas_usados=sorted(medios_valores, key=lambda medios_valores: medios_valores['recuento'],reverse=True)
    print("\nLOS 3 MEDIOS DE TRANSPORTE MÁS USADOS SON:")
    for i in range(3):
        print(str(Mas_usados[i]['medio_transporte'])+", con "+ str(Mas_usados[i]['recuento'])+" movimientos.")
    Mas_valor=sorted(medios_valores, key=lambda medios_valores: medios_valores['total'],reverse=True)
    print("\nLOS 3 MEDIOS DE TRANSPORTE CON MAYOR VALOR TOTAL SON:")
    for i in range(3):
        print(str(Mas_valor[i]['medio_transporte'])+", con un total de $"+ str(Mas_valor[i]['total']))
    Mayor_promedio=sorted(medios_valores, key=lambda medios_valores: medios_valores['valor_promedio'],reverse=True)
    print("\nLOS 3 MEDIOS DE TRANSPORTE CON PROMEDIO POR MOVIMIENTO MÁS ALTO SON:")
    for i in range(3):
        print(str(Mayor_promedio[i]['medio_transporte'])+", con un promedio por movimiento de $"+ str(Mayor_promedio[i]['valor_promedio']))

####OPCIÓN 3. Valor total de exportaciones e importaciones.
# Considerando:
#importación -->  país de destino.
#exportación --> país de origen.

#Tal y como se hizo en la opción anterior, sólo se comentarán las diferencias importantes.
def valores(direccion): #Definimos la función con parámetro direction
    #La primera parte de la función es casi igual a la función creada para la opción 1,
    #pero ahora sólo se considera el valor total.
    rutas=[] #listas vacías que necesitaremos posteriormente.
    rutas_valores=[]
    for ruta in lista_movimientos:
        if ruta["direction"]==direccion:
            ruta_actual=[ruta['direction'],ruta['origin'],ruta['destination']]
            if ruta_actual not in rutas:
                rutas.append(ruta_actual)
                valor=0
                for movimiento in lista_movimientos:
                    if ruta_actual==[movimiento['direction'],movimiento['origin'],movimiento['destination']]:
                        valor+=int(movimiento['total_value'])
                ruta_val= {'origen':ruta['origin'],'destino':ruta['destination'],'total':valor}
                rutas_valores.append(ruta_val)
    paises=[] #En este caso, nos interesa la información por país, por lo que creamos una lista con todos los países distintos.
    datos_paises=[] #esta lista contendrá los datos de todos los países.
    total_paises=0  #Calculamos el valot total generado por todos los países con movimientos en la dirección seleccionada.
    ### creamos las listas de manera análoga a los procesos anteriores:
    for mov in rutas_valores:
        #Existe una diferencia en la información de la ruta que tomaremos en cuenta, por lo que usamos un if
        if direccion=="Exports": 
            pais=mov['origen'] #Si la dirección es Exportaciones, consideramos el ORIGEN de la ruta
            if pais not in paises:
                paises.append(pais) #lista de países que servirá de referencia
                valor=0
                for ruta in rutas_valores:
                    if pais==ruta['origen']:
                        valor+=int(ruta['total'])
                total_paises+=valor
                datos={'pais':pais,'total':valor}
                datos_paises.append(datos) #lista de diccionarios que contienen la información de los países.
        else: #Si la dirección es Imports.
            pais=mov['destino'] #Si la dirección es Importaciones, consideramos el DESTINO de la ruta
            if pais not in paises:
                paises.append(pais)
                valor=0
                for ruta in rutas_valores:
                    if pais==ruta['destino']:
                        valor+=int(ruta['total'])
                total_paises+=valor
                datos={'pais':pais,'total':valor}
                datos_paises.append(datos)   

    ##Imprimimos todos los datos que queremos visualizar. 
    print("\n\n-->"+str(direccion))
    print("->Existen "+str(len(paises))+" paises con movimientos en esta dirección.")
    print("->El 80% del total es igual a $"+str(total_paises*0.8)+",\npor lo que los países a considerar son:\n")
    ##Nuevamente ordenamos con una función sorted con llave lambda y de mayor a menos usando "reverse=True", la lista de información que creamos.
    Mas_valor=sorted(datos_paises, key=lambda datos_paises: datos_paises['total'],reverse=True)
    ##Usaremos un ciclo para imprimir únicamente los países que representan el 80% del total del valor.
    i=0 #contador para ir avanzando en la lista
    suma=0 #valor total generado por los países que se van incluyendo en la lista.
    while suma<(total_paises*0.8): #Se agregarán países a la lista hasta que su suma de totales sobrepase el 80% del total calculado.
        print("Pais: " + str(Mas_valor[i]['pais'])+", con un total de $"+ str(Mas_valor[i]['total']))
        suma+=Mas_valor[i]['total']  #Se va agregando a la suma el total de cada país cada que es agregago.
        i+=1 #para que el ciclo vaya avanzando.

###Ahora que las funciones están definidas, preparamos el inicio del sistema para proporcionar la información que se solicite.
inicio= """
BIENVENIDO A SYNERGY LOGISTICS
\nMENÚ PRINCIPAL
¿Qué opción desea visualizar?
1) Rutas de importación y exportación.
2) Medio de transporte utilizado.
3) Valor total de exportaciones e importaciones.

99) Salir.
"""
stats=0 #para que se inicie automáticamente. No incluimos un inicio de sesión con contraseña.
print('inicio')

while stats==0 and stats !=99: #Ciclo para que el sistema funcione repetidamente hasta que el usuario decida salir del sistema.
  print(inicio)
  stats=float(input("\nIngresa sólo el número de tu elección: ")) #para permitir al usuario elegir.

 ##En cada opción permitimos que el usuario seleccione la información que desea ver, pueda repetir el proceso o salga del sistema.
  while stats == 1:
      ver=float(input("\nInformación disponible:\n1.Exportaciones,\n2.Importaciones,\n3.Ambas,\n\nSeleción: "))
      if ver==1: rutas("Exports")
      elif ver==2: rutas("Imports")
      elif ver==3:
          rutas("Exports")
          rutas("Imports")
      #para poder regresar al inicio, visualizar más información de esta opción o salir directamente del sistema.
      stats=float(input("\nPara más información de esta sección ingresa 1.\nPara regresar al menú principal ingresa 0.\nPara Salir del sistema ingresa 99.\n\nSelección: "))
          
  while stats == 2:
      ver=float(input("\nInformación disponible:\n1.Exportaciones,\n2.Importaciones,\n3.Ambas,\n\nSeleción: "))
      if ver==1: transporte("Exports")
      elif ver==2: transporte("Imports")  
      elif ver==3:
          transporte("Exports")
          transporte("Imports")  
      stats=float(input("\nPara más información de esta sección ingresa 2.\nPara regresar al menú principal ingresa 0.\nPara Salir del sistema ingresa 99.\n\nSelección: "))

  while stats == 3:
      ver=float(input("\nInformación disponible:\n1.Exportaciones,\n2.Importaciones,\n3.Ambas,\n\nSeleción: "))
      if ver==1: valores("Exports")
      elif ver==2: valores("Imports")  
      elif ver==3:
          valores("Exports")
          valores("Imports") 
      stats=float(input("\nPara más información de esta sección ingresa 3.\nPara regresar al menú principal ingresa 0.\nPara Salir del sistema ingresa 99.\n\nSelección: "))
print('¡Ha salido del sistema!') #mensaje de confirmación de salida.