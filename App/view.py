﻿"""
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
        print("Creado el catalogo")
        loadData(catalog)
        print("Se cargaron los datos al catalogo")
        print(f'Se cargaron {mp.size(catalog["artworks"])} obras y {mp.size(catalog["artists"])} artistas')


        printEspacio()

    elif int(inputs[0]) == 2:
        medio=input('Ingrese el medio a buscar:  ')
        n=input('Ingrese la cantidad de obras más viejas a buscar:  ')
        retorno=controller.ObrasAntiguasMedio(medio,catalog)
        printObrasAntiguasMedio(retorno,int(n),medio)

    else:
        sys.exit(0)
sys.exit(0)
