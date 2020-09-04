#RENOMBRAMOS LAS VARIABLES
from lifestore_file import lifestore_products
Productos=lifestore_products

from lifestore_file import lifestore_sales
Ventas=lifestore_sales

from lifestore_file import lifestore_searches
Busquedas=lifestore_searches
Categorias=[Productos[0][3]]
for i in range(1,len(Productos)):
  if Productos[i][3]not in Categorias: 
    Categorias.append(Productos[i][3])

Meses=[Ventas[0][3][3:10]]
Years=[Ventas[0][3][6:10]]
for i in range(1,len(Ventas)):
  if Ventas[i][3][3:10] not in Meses: Meses.append(Ventas[i][3][3:10])
  if Ventas[i][3][6:10] not in Years: Years.append(Ventas[i][3][6:10])

#Ventas_Mensuales=[mes/año,unidades vendidas,ingresos]
Ventas_mensuales=[]
for Mes in Meses: Ventas_mensuales.append([Mes,0,0])

"""
Individuales=[id_producto, Nombre, Precio, Categoría, Número de búsquedas, Unidades vendidas, Calificación, Porcentaje de devoluciones,Stock]
"""
Individuales=[] #Se incluyen a todos los productos.
L_Individuales=[] #Sólo se incluyen aquellos con ventas distintas a cero.
for Producto in Productos:
 porproducto=[Producto[0],Producto[1],Producto[2],Producto[3]]
 totalvendido=0
 totalbusquedas=0
 devoluciones=0
 sumascore=0
 for Busqueda in Busquedas:
   if Busqueda[1]==Producto[0]:
     totalbusquedas+=1
 porproducto.append(totalbusquedas) 
 for venta in Ventas:
   if venta[1]==Producto[0]:
    totalvendido+=1
    devoluciones+=venta[4]
    sumascore+=venta[2]
    for pormes in Ventas_mensuales:
      if venta[3][3:10]==pormes[0]: 
        pormes[2]+=Producto[2]
        pormes[1]+=1
 porproducto.append(totalvendido)
 if totalvendido!=0:
    calificacion=sumascore/totalvendido
    dev_p=(devoluciones/totalvendido)*100
    porproducto.append(calificacion)
    porproducto.append(dev_p)
    L_Individuales.append(porproducto)
 else:
    calificacion=999
    dev_p=999
    porproducto.append(calificacion)
    porproducto.append(dev_p)
 porproducto.append(Producto[4])
 Individuales.append(porproducto)  
cero_v=96-len(L_Individuales) #54
no_cero=len(L_Individuales) #42

"""
Grupales=[Categoría, Número de productos, Precio promedio, Unidades vendidas, Devoluciones como porcentaje de ventas, Calificación promedio, Número de búsquedas, Stock]
"""
Grupales=[]
for Categoria in Categorias:
  cantidad=0
  sumaprecio=0
  ventas_c=0
  devoluciones=0
  sumascore=0
  busquedas=0
  stock=0
  for Individual in Individuales:
    if Individual[3]==Categoria:
      cantidad+=1
      sumaprecio+=Individual[2]
      ventas_c+=Individual[5]
      if Individual[6]!=999:
        sumascore+=Individual[6]      
      if Individual[7]!=999:
        devoluciones+=Individual[7]
      busquedas+=Individual[4]
      stock+=Individual[8]
  #cada categoria tiene al menos un producto por lo que cantidad != 0
  precioprom=sumaprecio/cantidad
  calificacion=sumascore/cantidad
  if ventas_c !=0:
    devoluciones_p=(devoluciones/ventas_c)*100
  else:
    devoluciones_p=999
  porcategoria=[Categoria,cantidad,precioprom,ventas_c,devoluciones_p,calificacion,busquedas]
  Grupales.append(porcategoria)

## VENTAS Y BÚSQUEDAS
Mas_vendidos=sorted(Individuales, key=lambda Individuales: Individuales[5],reverse=True)
Menos_vendidos=sorted(L_Individuales, key=lambda L_Individuales: L_Individuales[5])
Mas_buscados=sorted(Individuales, key=lambda Individuales: Individuales[4],reverse=True)
Menos_buscados=sorted(Individuales, key=lambda Individuales: Individuales[4])

MVCategorias=sorted(Grupales, key=lambda Grupales: Grupales[3],reverse=True)
MeVCategorias=sorted(Grupales, key=lambda Grupales: Grupales[3])
MBCategorias=sorted(Grupales, key=lambda Grupales: Grupales[6],reverse=True)
MeBCategorias=sorted(Grupales, key=lambda Grupales: Grupales[6])

## RESEÑAS Y DEVOLUCIONES
# Sólo se consideran los productos con ventas distintas a cero
MCalificados=sorted(L_Individuales, key=lambda L_Individuales: L_Individuales[6],reverse=True)
PCalificados=sorted(L_Individuales, key=lambda L_Individuales: L_Individuales[6])
MDevoluciones=sorted(L_Individuales, key=lambda L_Individuales: L_Individuales[7],reverse=True)
MeDevoluciones=sorted(L_Individuales, key=lambda L_Individuales: L_Individuales[7])

##ESTADÍSICAS
IngresoTotal=0
Anuales=[]
for pormes in Ventas_mensuales:
  pormes.append(pormes[2]/pormes[1]) #pormes[1] siempre distinto a cero
for y in Years:
  IngresoAnual=0
  VentaAnual=0
  for pormes in Ventas_mensuales:  
    if pormes[0][3:7]==y:
      IngresoAnual+=pormes[2]
      VentaAnual+=pormes[1]
  Anuales.append([y,IngresoAnual,VentaAnual])
for year in Anuales:
  IngresoTotal+=year[1]

Meses_unidades=sorted(Ventas_mensuales, key=lambda Ventas_mensuales: Ventas_mensuales[1],reverse=True)
Meses_ingresos=sorted(Ventas_mensuales, key=lambda Ventas_mensuales: Ventas_mensuales[2],reverse=True)

login='''
BIENVENIDO A LIFE STORE
\nRecuerda:\nPara tener acceso a la información debes\npertenecer al cuerpo administrativo.\n\nEn caso contrario se detendrá el programa.
\nLOG IN
'''
print(login)
stats=1
clave=827462
Administradores=['Director','Gerente','Staff','Accionista']
usuario=input("Ingrese su usuario: ")

if usuario in Administradores:
  intentos=3
  while stats!=0 and intentos>0:
    code=input("\nPor favor ingresa la contraseña de acceso: ")
    if int(code)==clave:
      print("\n\n¡Bienvenido al sistema!")
      stats=0
    else:
      intentos-=1
      if intentos==0: print("Parece que se ha agotado el número de intentos,\npor favor reinicie el proceso.")
      else: print ("Contraseña incorrecta, por favor intente de nuevo.\nIntentos restantes:"+str(intentos))
else: print("\n¡Lo sentimos!\nEste usuario no es un administrador.\nLe invitamos a visitar www.lifestore/clientes.com\npara conocer nuestras promociones.\n\nSi usted es un administrador por favor intente de nuevo\no comuníquese con nuestro personal.")    

inicio= """
\nMENÚ PRINCIPAL
¿Qué deseas ver?
1) Productos más vendidos y productos rezagados.
2) Productos por reseña en el servicio.
3) Información Mensual y Anual.
4) Productos sugeridos para promoción.

99) Salir del sistema.
"""
while stats==0 and stats !=99:
  print(inicio)
  stats=float(input("Ingresa sólo el número de tu elección: "))

  while stats == 1:
    print('\n\n1) PRODUCTOS MÁS VENDIDOS Y PRODUCTOS REZAGADOS.\n\nInformación disponible:\n\nGENERAL:\n1. Más vendidos, 2. Menos vendidos, 3. Más buscados, 4. Menos buscados.\n\nPOR CATEGORÍA:\n5. Más vendidos, 6. Menos vendidos, 7. Más buscados, 8. Menos buscados.')
    stats1=float(input("\n¿Cuál deseas? (ingresa el número): "))
    if stats1 == 1:
      unidades=int(input("\n¿Cuántos desea ver?(1~42) "))
      print('\nLOS PRODUCTOS MÁS VENDIDOS FUERON:\n')
      for i in range(unidades):
        print(Mas_vendidos[i][1])
        print('Unidades vendidas: '+str(Mas_vendidos[i][5])+'\n')
      stats=float(input("\nPara más información de esta sección ingresa 1.\nPara regresar al menú principal ingresa 0.\nPara Salir del sistema ingresa 99.\n\nSelección: "))
    elif stats1 == 2:
      vercero=input('¿Deseas ver los productos que no tuvieron ventas? (si/no): ')
      if vercero=="si":
        print('\nLOS PRODUCTOS QUE NO TUVIERON VENTAS FUERON '+str(cero_v)+',\nA saber:')
        for Individual in Individuales:
          if Individual[5]==0:
            print(Individual[1])
            print()
      unidades=int(input("\n¿Cuántos de aquellos con ventas distintas a cero desea ver?(1~54) "))
      print('\nLOS PRODUCTOS CON MENORES VENTAS FUERON:')
      for i in range(unidades):
       print(Menos_vendidos[i][1])
       print('Unidades vendidas: '+str(Menos_vendidos[i][5])+'\n')
      stats=float(input("\nPara más información de esta sección ingresa 1.\nPara regresar al menú principal ingresa 0.\nPara Salir del sistema ingresa 99.\n\nSelección: "))
    elif stats1 == 3:
       unidades=int(input("\n¿Cuántos desea ver?(1~96) "))
       print('\nLOS PRODUCTOS MÁS BUSCADOS FUERON:')
       for i in range(unidades):
        print(Mas_buscados[i][1])
        print('Número de búsquedas: '+str(Mas_buscados[i][4])+'\n')
       stats=float(input("\nPara más información de esta sección ingresa 1.\nPara regresar al menú principal ingresa 0.\nPara Salir del sistema ingresa 99.\n\nSelección: "))
    elif stats1 == 4:
      print('\nLOS 50 PRODUCTOS MENOS BUSCADOS FUERON:')
      for i in range(50):
        print(Menos_buscados[i][1])
        print('Número de búsquedas: '+str(Menos_buscados[i][4])+'\n')
      stats=float(input("\nPara más información de esta sección ingresa 1.\nPara regresar al menú principal ingresa 0.\nPara Salir del sistema ingresa 99.\n\nSelección: "))
    elif stats1 == 5:
      print('\nLAS DOS CATEGORÍAS CON MAYORES VENTAS FUERON:\n')
      for i in range(2):
        print(MVCategorias[i][0])
        print('Unidades vendidas: ', MVCategorias[i][3])
        print()
      stats=float(input("\nPara más información de esta sección ingresa 1.\nPara regresar al menú principal ingresa 0.\nPara Salir del sistema ingresa 99.\n\nSelección: "))
    elif stats1 == 6:
      print('\nLAS TRES CATEGORÍAS CON MENORES VENTAS FUERON:')
      for i in range(3):
       print(MeVCategorias[i][0])
       print('Unidades vendidas: ', MeVCategorias[i][3])
       print()
      stats=float(input("\nPara más información de esta sección ingresa 1.\nPara regresar al menú principal ingresa 0.\nPara Salir del sistema ingresa 99.\n\nSelección: "))
    elif stats1 == 7:
      print('\nLAS DOS CATEGORIAS CON MAYORES BÚSQUEDAS FUERON:')
      for i in range(2):
        print(MBCategorias[i][0])
        print('Número de búsquedas: ', MBCategorias[i][6])
        print()
      stats=float(input("\nPara más información de esta sección ingresa 1.\nPara regresar al menú principal ingresa 0.\nPara Salir del sistema ingresa 99.\n\nSelección: "))
    elif stats1 == 8:
      print('\nLAS DOS CATEGORIAS CON MENORES BÚSQUEDAS FUERON:')
      for i in range(2):
        print(MeBCategorias[i][0])
        print('Número de búsquedas: ', MeBCategorias[i][6])
        print()
      stats=float(input("\nPara más información de esta sección ingresa 1.\nPara regresar al menú principal ingresa 0.\nPara Salir del sistema ingresa 99.\n\nSelección: "))
  
  while stats == 2:
    print('\n\n2) PRODUCTOS POR RESEÑA EN EL SERVICIO.\n\nInformación disponible:\n\n1. Los mejor calificados, 2. Productos con peor calificación.')
    stats2=float(input("\nIngresa el número que deseas: "))
    if stats2 == 1:
      unidades=int(input("\n¿Cuántos desea ver?(1~42) "))
      print('\nLOS PRODUCTOS CON MEJOR CALIFICACIÓN SON:\n')
      for i in range(unidades):
        print(MCalificados[i][1])
        print('Calificación: ', MCalificados[i][6],'\nDevoluciones: ',MCalificados[i][7])
        print()
      stats=float(input("\nPara más información de esta sección ingresa 2.\nPara regresar al menú principal ingresa 0.\nPara Salir del sistema ingresa 99.\n\nSelección: "))
    elif stats2 == 2:
      unidades=int(input("\n¿Cuántos desea ver?(1~42) "))
      print('\nLOS PRODUCTOS CON PEOR CALIFICACIÓN SON:\n ')
      for i in range(unidades):
        print(PCalificados[i][1])
        print('Calificación: ', PCalificados[i][6],'\nDevoluciones: ',PCalificados[i][7])
        print()
      stats=float(input("\nPara más información de esta sección ingresa 2.\nPara regresar al menú principal ingresa 0.\nPara Salir del sistema ingresa 99.\n\nSelección: "))

  while stats == 3:
    print('\n\n3) INFORMACIÓN MENSUAL Y ANUAL.\n\nInformación disponible:\n\n1. Total ingresos,\n2. Totales por año y por mes.\n3. Ventas promedio por mes,\n4. Meses con mayores ventas.')
    stats3=float(input("\nIngresa el número que deseas: "))
    if stats3 == 1:
      print('\nEL INGRESO TOTAL DE LA EMPRESA FUE DE:\n$'+str(IngresoTotal))
      stats=float(input("\nPara más información de esta sección ingresa 3.\nPara regresar al menú principal ingresa 0.\nPara Salir del sistema ingresa 99.\n\nSelección: "))
    elif stats3 == 2:
      print('\nTOTALES POR AÑO:\n')
      for x in Anuales:
        print(str(x[0])+': $'+str(x[1])+' con '+str(x[2])+' unidades vendidas')
      print('\nTOTALES POR MES:\n')
      for v in Ventas_mensuales:
        print(str(v[0])+': '+str(v[1])+' unidades vendidas, $'+str(v[2]))
      stats=float(input("\nPara más información de esta sección ingresa 3.\nPara regresar al menú principal ingresa 0.\nPara Salir del sistema ingresa 99.\n\nSelección: "))
    elif stats3 == 3:
      print('\nVENTAS PROMEDIO POR MES:\n')
      for vp in Ventas_mensuales:
        print(str(vp[0])+': $' +str(vp[3]))
      stats=float(input("\nPara más información de esta sección ingresa 3.\nPara regresar al menú principal ingresa 0.\nPara Salir del sistema ingresa 99.\n\nSelección: "))
    elif stats3 == 4:
      print('\nMESES CON MAYOR NÚMERO DE VENTAS:\nPor unidades vendidas:\n')
      for mmv in Meses_unidades:
        print(str(mmv[0])+': '+str(mmv[1])+' unidades')
      print('\n\nPor ingresos:\n')
      for mmi in Meses_ingresos:
        print(str(mmi[0])+': $'+str(mmi[2]))  
      stats=float(input("\nPara más información de esta sección ingresa 3.\nPara regresar al menú principal ingresa 0.\nPara Salir del sistema ingresa 99.\n\nSelección: "))
  
  while stats == 4:
    print('\n\n4) PRODUCTOS SUGERIDOS PARA PROMOCIÓN.\n\nSegún las ventas registradas, así como\nla cantidad de estos productos en stock,se\ntomaron las siguientes consideraciones:\n\n> Productos sin ventas registradas.\n> Al menos 60 unidades en stock.\n\n Con base en esto, se tiene una lista de\n10 productos candidatos,')
    Prom=[]
    for Individual in Individuales:
      if Individual not in L_Individuales and Individual[8]>=60:
        Prom.append(Individual)
    stats4=int(input('\n¿Cuántos deseas ver? (1~10): '))
    print('\nSe considera invertir en la promoción de:\n')
    for vender in Prom[0:stats4]:   
      print(str(vender[1])+'\nque tuvo ' +str(vender[4])+'  búsquedas y tiene '+str(vender[8])+'  unidades en stock.\n')
    stats=float(input("\nPara regresar al menú principal ingresa 0.\nPara Salir del sistema ingresa 99.\n\nSelección: "))
print('\n¡Ha salido del sistema!')
