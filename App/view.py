"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
from DISClib.DataStructures import mapstructure as ms
from DISClib.ADT import map as mp
assert cf
import time


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

# Prints iniciales

def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Mostrar n obras más antiguas para un medio específico")
    print('3- Buscar la cantidad de obras de una nacionalidad')
    print('4-(REQ1) Listar cronológicamente los artistas')
    print('5-(REQ 2) Listar cronológicamente las adquisiciones')
    print('6-(REQ 3) Clasificar las obras de un artista por técnica')
    print("7-(REQ 4) Clasificacion de obras por nacionalidad de sus creadores")
    print("8-(REQ 5) Transportar obras de un departamento")
    print("9-(REQ 6) Artista mas prolifico")


def printEspacio():
    """
    añade espacios entre funciones 
    """

    print("")
    print("=" * 100)
    print("")

def printObrasAntiguasMedio(lista,n,medio): 
    print()
    

    print(f'Hay {min(lt.size(lista),n)} obras con medio {medio}')

    print()
    print()

    print(f'El top {min(lt.size(lista),n)} de obras más antiguas es: ')
    print()
    print()
    for i in range(min(lt.size(lista),n)): 
        Elto=lt.getElement(lista,i)
        Medio=Elto['medium']
        Fecha=Elto['date']
        Titulo=Elto['name']
        print(f'{i+1}) La obra: {Titulo}, con fecha: {Fecha}, y medio: {Medio}')
    printEspacio()

def printObrasNacionalidad(tamaño,nacionalidad):
    print()
    print(f'Hay {tamaño} obras de la nacionalidad {nacionalidad}')
    print()

def printArtistasCrono(lista):

    printEspacio()
    cantidad = lt.size(lista)
    print("Hay " + str(cantidad) + " artistas en el rago seleccioando")
    print()
    print("Top 3 mas viejos: ")
    for x in range(3):
        elemento = lt.getElement(lista, x)
        print(str(x+1) + ") El artista: " + elemento["nombre"] + " nacido en: " + str(elemento["edad"]) + " de nacionalidad: " + elemento["nacionalidad"] + " y de genero: " +  elemento["genero"])

    print()
    print("Top 3 mas viejos: ")
    for x in range(3):
        elemento = lt.getElement(lista, cantidad - x)
        print(str(x+1) + ") El artista: " + elemento["nombre"] + " nacido en: " + str(elemento["edad"]) + " de nacionalidad: " + elemento["nacionalidad"] + " y de genero: " +  elemento["genero"])


def printObrasCronoacq(lista):
    """
    imprime la cantidad de obras adquiridas en un rango de años
    """
    cantidad = len(lista)
    
    print("Hay " + str(cantidad) + " obras adquiridas en el rago seleccioando")
    print()

    
    print("Top 3 mas viejos: ")
    print()
    for x in range(3):
        elemento = lista[x]
        print(str(x+1) + ") la obra: " + elemento["name"] + " adquirida en : " + str(elemento["dateacquired"]) + " con medio: " + elemento["medium"] + " y de dimensiones: " +  elemento["dimensions"] +' creada por: ' + str(elemento['artistname']))
        

    print()
    print("Top 3 mas jóvenes: ")
    print()
    for x in range(3):
        elemento2 = lista[-(x+1)]
        print(str(x+1) + ") la obra: " + elemento2["name"] + " adquirida en : " + str(elemento2["dateacquired"]) + " con medio: " + elemento2["medium"] + " y de dimensiones: " +  elemento2["dimensions"]+ 'creada por: ' + str(elemento2['artistname']))




def printObrasPorTecnica(TotalObras,TotalTecnicas,TecnicaMasUsada,ObrasArtistaTecnica,nombre,ObrasArtistaTecnica2): 
    
    if TecnicaMasUsada=='': 
        TecnicaMasUsada='No hay suficiente información '

    if TotalTecnicas==-1:
        TotalTecnicas=0

        
    print('El artista  ' + str(nombre) + ' Tiene un total de  ' + str(TotalObras) + ' obras  y un total de ' + str(TotalTecnicas) + ' distintas   técnicas utilizadas \n \n')
    print('La técnica más utilizada por '+ str(nombre) + ' es: ' + str(TecnicaMasUsada))
    print()

    print('Obras con la técnica más utilizada: ')
    print()
    for i in range(len(ObrasArtistaTecnica2)): 
      
        elemento=ObrasArtistaTecnica2[i]
        
        print(str(i+1) + ')' + ' La obra: ' + str(elemento['name']) + '  con fecha : '  + str(elemento['date']) + '   dimensiones : ' + str(elemento['dimensions']) + 'y técnica : ' + str(elemento['medium']))
    printEspacio()

def Print_nacionalidad_obras(lista):
    printEspacio()
    
    print("Top 10")

    for x in range(10):
        print( str(x) + " - " + lt.getElement(lista,x)[0] + " con " + str(lt.getElement(lista,x)[1]))

    print()
    print("Obras de " + lt.getElement(lista,0)[0])
    print()

    artistas = catalog["nationalityartworks"]
    grupo = mp.get(artistas, lt.getElement(lista,0)[0])["value"]
    cant = lt.size(grupo)
    for x in range(3):
        obra = lt.getElement(grupo, x)
        print(str(x+1) + ' )' + " La obra de titulo " + obra["name"] + " Hecha en " + str(obra["date"]) + " Con el medio " + obra["medium"] + "Con dimensiones" + obra["dimensions"])

    print()

    for x in range(3):
        obra = lt.getElement(grupo, cant - x)
        print(str(cant - x) + ' )' + " La obra de titulo " + obra["name"] + " Hecha en " + str(obra["date"]) + " Con el medio " + obra["medium"] + "Con dimensiones" + obra["dimensions"])
        

    printEspacio()

def printObrasTransporte(TotalObras, TotalPrecio, TotalPeso,TransportePorCosto, TransportePorFecha): 
    
    print('Hay un total de : ' + str(TotalObras) + ' obras por transportarse, con un precio total de transporte de: ' + str(TotalPrecio) + ' USD, por un peso de: ' + str(TotalPeso) + 'kg')
    print( )
    print('Las 5 obras más costosas por transportar son: ')
    print()
    for i in range(5):
        elemento=lt.getElement(TransportePorCosto,i)
        print(str(i+1) + ')' + ' La obra: ' + str(elemento['name']) + '  con fecha : '  + str(elemento['date']) + '   dimensiones : ' + str(elemento['dimensions']) + ', técnica : ' + str(elemento['medium'])+'y costo de transporte aprox: ' + str(round(elemento['cost']))+' USD' + ' de los artistas con ID : ' + str(elemento['constituentid']))

    print()
    print()

    print('Las 5 obras más antiguas para transportarse son: ')
    print()
    for i in range(5):
        elemento=lt.getElement(TransportePorFecha,i)
        print(str(i+1) + ')' + ' La obra: ' + str(elemento['name']) + '  con fecha : '  + str(elemento['date']) + '   dimensiones : ' + str(elemento['dimensions']) + ', técnica : ' + str(elemento['medium'])+'y costo de transporte aprox: ' + str(round(elemento['cost']))+' USD'  + ' de los artistas con ID : ' + str(elemento['constituentid']))
    print()
    printEspacio()

    

def Print_ArtistasPro(lista):
    printEspacio()
    print("Lista de artistas con mas obras: ")

    for x in range(lt.size(lista)):
        mom = lt.getElement(lista,x)
        print(str(x+1) + ") " + str(mom[0]) + " Con " + str(mom[1]) + " y lista de tecnicas " )#+ str(mom[3]))


    printEspacio()


# carga de datos

def initCatalog(datatype):
    """
    Inicializa el catalogo de obras
    """
    return controller.initCatalog(datatype)

def loadData(catalog):
    """
    Carga las obras en la estructura de datos
    """
    controller.loadData(catalog)

catalog = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar: ')
    if int(inputs[0]) == 1:

        printEspacio()
        print("Cargando información de los archivos ....")
        datatype=''

        catalog=initCatalog(datatype)
        print("Creando el catalogo")
        loadData(catalog)
        print("Se cargaron los datos al catalogo")
        print(f'Se cargaron {mp.size(catalog["artworks"])} obras y {mp.size(catalog["artists"])} artistas')
        print()
        print('Hay ' + str(lt.size(mp.keySet(catalog['medium']))) + ' medios distintos')



        printEspacio()

    elif int(inputs[0]) == 2:
        medio=input('Ingrese el medio a buscar:  ')
        n=input('Ingrese la cantidad de obras más viejas a buscar:  ')
        retorno=controller.ObrasAntiguasMedio(medio,catalog)
        printObrasAntiguasMedio(retorno,int(n),medio)

    elif int(inputs[0])==3:
        nacionalidad= input('Ingrese la nacionalidad a buscar:  ')
        retorno=controller.ObrasPorNacionalidad(nacionalidad,catalog)
        printObrasNacionalidad(retorno,nacionalidad)


    elif int(inputs[0]) == 4:

        printEspacio()
        Año_inicial = int(input("Desde que año quieres buscar?:  "))
        Año_fin = int(input("Hasta que año quieres buscar?:  "))
        
        StartTime=time.process_time()
        
        cantidadArtistas = controller.artistasCronologico(catalog, Año_inicial, Año_fin)
        print()
        
        print('='*20 + ' RESPUESTA REQ 1 ' + '='*20)
        print()
        

        printArtistasCrono(cantidadArtistas) 
        
        StopTime=time.process_time()
        TimeMseg=(StopTime-StartTime)*1000
        print()
        print(f'El REQ1 tardó {TimeMseg} miliseg')


        printEspacio()

    elif int(inputs[0]) == 5:
        FechaInicial = input("desde que fecha quieres buscar?(AAAA-MM-DD):   ")
        FechaFin = input("hasta que fecha quieres buscar?(AAAA-MM-DD):   ")
        print()

        StartTime=time.process_time()
        
        print('='*20 + ' RESPUESTA REQ 2 ' + '='*20)
        print()
       
        CantidadObras=controller.obrasCronologicoacq(FechaInicial,FechaFin,catalog)
        
        printObrasCronoacq(CantidadObras)

        StopTime=time.process_time()
        TimeMseg=(StopTime-StartTime)*1000
        print()
        print(f'El REQ2 tardó {TimeMseg} miliseg')

        printEspacio()

    

    elif int(inputs[0])==6: 
        nombre = input("Qué artista desea consultar ?: ")
        print()

        StartTime=time.process_time()
        
        TotalObras,TotalTecincas,TecnicaMasUsada,ObrasArtistaTecnica,ObrasArtistaTecnica2=controller.ObrasArtista(catalog,nombre)
        print()
        
        print('='*20 + ' RESPUESTA REQ 3 ' + '='*20)
        print()
        
        printObrasPorTecnica(TotalObras,TotalTecincas,TecnicaMasUsada,ObrasArtistaTecnica,nombre,ObrasArtistaTecnica2)

        StopTime=time.process_time()
        TimeMseg=(StopTime-StartTime)*1000
        print()
        print(f'El REQ3 tardó {TimeMseg} miliseg')
        print()



    elif int(inputs[0]) == 7:
        print()
        print("Cargando...")

        StartTime=time.process_time()
        
        Nacionalidad_obras = controller.Nacionalidad_obras(catalog)
        print()
        
        print('='*20 + ' RESPUESTA REQ 4 ' + '='*20)
        print()
        Print_nacionalidad_obras(Nacionalidad_obras)

        StopTime=time.process_time()
        TimeMseg=(StopTime-StartTime)*1000
        print()
        print(f'El REQ4 tardó {TimeMseg} miliseg')
        print()


    elif int(inputs[0]) == 8:
        depa = input("Que departamento deseas transportar?: ")
        StartTime=time.process_time()
        
        TotalObras, TotalPrecio,TotalPeso, TransportePorCosto, TransportePorFecha=controller.Transporte(catalog,depa)
        print()
        
        print('='*20 + ' RESPUESTA REQ 5 ' + '='*20)
        print()
       
        printObrasTransporte(TotalObras, TotalPrecio, TotalPeso,TransportePorCosto, TransportePorFecha) 

        StopTime=time.process_time()
        TimeMseg=(StopTime-StartTime)*1000
        print()
        print(f'El REQ5 tardó {TimeMseg} miliseg')
        print()

    elif int(inputs[0]) == 9:
        print()
        print("Cargando...")
        Año_inicial = int(input("Desde que año quieres buscar?:  "))
        Año_fin = int(input("Hasta que año quieres buscar?:  "))
        Top = int(input("Cuantos artistas quieres ver en el top?:  "))
        
        Lista_artistas = controller.artistasPro(catalog, Año_inicial, Año_fin, Top)
        print()
        
        print('='*20 + ' RESPUESTA REQ 6 ' + '='*20)
        print()
        Print_ArtistasPro(Lista_artistas) 
        
    else:
        sys.exit(0)
sys.exit(0)
