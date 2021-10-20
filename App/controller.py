"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
import model
import csv
import time
import datetime


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros

def initCatalog(datatype): 
    """
    Llama la funcion de inicializacion del catalogo del modelo.
    """
    catalog=model.newCatalog(datatype)
    return catalog

# Funciones para la carga de datos

def loadData(catalog): 
    """
    Carga los datos de los archivos y cargar los datos en la
    estructura de datos
    """
    StartTime=time.process_time()
    loadArtists(catalog)
    loadArtworks(catalog)
    StopTime=time.process_time()
    TimeMseg=(StopTime-StartTime)*1000
    print()
    print(f'La carga de datos tardó {TimeMseg} miliseg')
    print()



def loadArtists(catalog):
    """
    Carga los artistas archivo.  .
    """
    artistsfile = cf.data_dir + 'MoMA/Artists-utf8-large.csv'
    input_file = csv.DictReader(open(artistsfile, encoding='utf-8'))
    for artist in input_file:
        model.addArtist(catalog, artist)

def loadArtworks(catalog):
    """
    Carga las obras de arte del archivo.  .
    """
    artworksfile = cf.data_dir + 'MoMA/Artworks-utf8-large.csv'
    input_file = csv.DictReader(open(artworksfile, encoding='utf-8'))
    for artwork in input_file:
        model.addArtwork(catalog, artwork)


# Funciones de ordenamiento

def ObrasAntiguasMedio(medio,catalog): 
    if medio=='':
        print('INGRESE UN MEDIO ADECUADO')
    else:
        return model.ObrasAntiguasMedio(medio,catalog)

def ObrasPorNacionalidad(nacionalidad,catalog):

   return model.ObrasPorNacionalidad(nacionalidad,catalog)

def obrasCronologicoacq(inicio,final,catalog):
    """
    Retorna las obras adquiridas enre las dos fechas utilizando el algoritmo de ordenamiento metodo
    """
    if inicio:
        datelst=inicio.split('-')
        inicio2=datetime.date(int(datelst[0]),int(datelst[1]),int(datelst[2]))
    else:
        print('ERROR, INGRESE UN FORMATO DE FECHA INICIAL ADECUADO')
    
    if final:
        datelst2=final.split('-')
        final2=datetime.date(int(datelst2[0]),int(datelst2[1]),int(datelst2[2]))
    else:
        print('ERROR, INGRESE UN FORMATO DE FECHA FINAL ADECUADO')
    
    ObrasCrono=model.obrasCronologicoacq(inicio2,final2,catalog)
    return ObrasCrono


# Funciones de consulta sobre el catálogo

def artistasCronologico(lista, inicio, final):
    """
    Retorna los artistas que nacieron enre las dos fechas
    """
    ArtistasCrono = model.artistasCronologico(lista, inicio, final)
    return ArtistasCrono

def ObrasArtista(catalog,nombre): 
    """
    Retorna las obras de un artista
    """
    if nombre=='':
        print('ERROR, INGRESE UN NOMBRE DE ARTISTA VALIDO ')
    else:
        return model.ObrasArtista(catalog, nombre)


def Nacionalidad_obras(catalog):
    """
    Lista con contadores de nacionalidad
    """
    lista = model.Nacionalidad_obras(catalog)
    return lista

def Transporte(catalog,depa):
    """
    Retorna el total de obras a transportar, el precio, el peso, las 5 obras más costosas y las 5 más antiguas

    """
    res=model.Transporte(catalog,depa)
    return res