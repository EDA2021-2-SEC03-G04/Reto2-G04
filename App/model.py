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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.DataStructures import mapstructure as ms
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import mergesort as mrgsort
assert cf
import datetime
import time

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def newCatalog(datatype): 
    """
    Inicializa el catálogo de obras de arte. Crea una lista vacia para guardar
    todas las obras, adicionalmente, crea una lista vacia para los artistas.Retorna el catalogo inicializado.
    """

    catalog={'artworks': None, 'artists': None, "artistID" : None, 'nationality': None,'medium':None,'nationalityartworks':None}

    catalog['artworks']=mp.newMap(10000,
                                   maptype='CHAINING',
                                   loadfactor=4.0,
                                   comparefunction=None)
    catalog['artists']=mp.newMap(10000,
                                   maptype='CHAINING',
                                   loadfactor=4.0,
                                   comparefunction=None)
    catalog['artistID']=mp.newMap(10000,
                                   maptype='CHAINING',
                                   loadfactor=4.0,
                                   comparefunction=None)

    catalog['nationality']=mp.newMap(10000,
                                   maptype='PROBING',
                                   loadfactor=0.8,
                                   comparefunction=None)

    catalog['medium']=mp.newMap(10000,
                                   maptype='PROBING',
                                   loadfactor=0.8,
                                   comparefunction=None)
    catalog['nationalityartworks']=mp.newMap(10000,
                                   maptype='CHAINING',
                                   loadfactor=4.0,
                                   comparefunction=None)

    return catalog

# Funciones para agregar informacion al catalogo

def addArtwork(catalog,artwork): 
    #Se adiciona la obra  a la lista de obras
    
    new=newArtwork(artwork['Title'],artwork['DateAcquired'],artwork['ConstituentID'],artwork['Date'],artwork['Medium'],artwork['Dimensions'],
    artwork['Department'],artwork['CreditLine'],artwork['Classification'], artwork['Circumference (cm)'],artwork['Depth (cm)'],artwork['Diameter (cm)'],
    artwork['Height (cm)'],artwork['Length (cm)'],artwork['Weight (kg)'],artwork['Width (cm)'])

    mp.put(catalog['artworks'], artwork['Title'], new)
    mp.put(catalog['medium'],artwork['Medium'],new)




    #Crea el diccionario de Obras por nacionalidad
    Iden = artwork['ConstituentID']
    Iden = Iden.translate({ord(i): None for i in '[]'})
    Iden = Iden.split(',')
    Iden=Iden[0]

    

    Nationality1=mp.get(catalog['artistID'],Iden)




    Nationality=Nationality1['value']['nationality']



    if mp.contains(catalog['nationalityartworks'],Nationality): 
        listavieja=mp.get(catalog['nationalityartworks'],Nationality)
        lt.addLast(listavieja['value'],new)
        mp.put(catalog['nationalityartworks'],Nationality,listavieja['value'])

        
    
    else: 
        lista=lt.newList()
        lt.addLast(lista,new)
        mp.put(catalog['nationalityartworks'],Nationality,lista)





def addArtist(catalog,artist): 
    #Se adiciona el artista  a la lista de artistas
    new=newArtist(artist['DisplayName'],artist['BeginDate'],artist['EndDate'],artist['Nationality'],artist['Gender'],artist['ConstituentID'])

    mp.put(catalog['artists'], artist['DisplayName'], new)
    mp.put(catalog['artistID'], artist['ConstituentID'], new)
    mp.put(catalog['nationality'],artist['Nationality'],artist['ConstituentID'])

# Funciones para creacion de datos

def newArtwork(name,dateacquired,constituentid,date,medium,dimensions,department,creditline,classification,circumference,depth,diameter,height,length,weight,width):
    '''
    Crea un nuevo objeto de obra de arte con atributos de nombre, fecha de adquisición 
    '''

    #Separamos la string de la fecha de adquisición con '-' y lo convertimos a foramto datetime
    #Si la entrada es vacia entonces se pone feha de hoy
    if dateacquired:
        datelst=dateacquired.split('-')
        dateacquired2=datetime.date(int(datelst[0]),int(datelst[1]),int(datelst[2]))
    else:
        dateacquired2=datetime.date.today()

    if date:
        try:
            date=int(date)
        except:
           date=3000 
    else:
        date=3000

    artwork={'name':'','dateacquired':'','constituentid':'','date':'','medium':'','dimensions':'','department':''
    ,'creditline':'','classification':'','circumference':'','depth':'','diameter':'','height':'','length':'','weight':'','width':''}

    artwork['name']=name
    artwork['dateacquired']=dateacquired2
    artwork['constituentid']=constituentid
    artwork['date']=date
    artwork['medium']=medium
    artwork['dimensions']=dimensions
    artwork['department']=department
    artwork['creditline']=creditline
    artwork['classification']=classification 
    artwork['circumference']=circumference
    artwork['depth']=depth
    artwork['diameter']=diameter
    artwork['height']=height
    artwork['length']=length
    artwork['weight']=weight
    artwork['width']=width

    return artwork

def newArtist(name,begindate,enddate,nationality,gender,constituentid):
    '''
    Crea un nuevo objeto de obra de artista con atributos de nombre,fecha de inicio, fecha final
    '''
    artist={'name':'','begindate':'','enddate':'','nationality':'','gender':'','constituentid':''}
    artist['name']=name
    artist['begindate']=begindate
    artist['enddate']=enddate
    artist['nationality']=nationality
    artist['gender']=gender
    artist['constituentid']=constituentid
    
    return artist

# Funciones de consulta

def ObrasAntiguasMedio(medio,catalog): 

    retorno=lt.newList()
    obras=catalog['artworks']
    Obras=mp.valueSet(obras)
    
    print(f'Hay {lt.size(Obras)} Obras')
    print(f'Hay {mp.size(obras)} obras catalog')
    for x in range(lt.size(Obras)): 
        Elto=lt.getElement(Obras,x)
        
        Medio=Elto['medium']
        Fecha=Elto['date']
        Titulo=Elto['name']
       

        if Medio.lower()==medio.lower():
            lt.addLast(retorno,{'medium':Medio,'date':Fecha,'name':Titulo})

    mrgsort.sort(retorno,cmpbydate)

    return retorno

def ObrasPorNacionalidad(nacionalidad,catalog): 
    print()
    print('Hay ' + str(lt.size(mp.keySet(catalog['nationalityartworks']))) + ' nacionalidades distintas')
    print()



    if mp.contains(catalog['nationalityartworks'],nacionalidad):

        return lt.size(mp.get(catalog['nationalityartworks'],nacionalidad)['value'])
    else:
        return 0
        

    









# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento

def cmpbydate(Obra1,Obra2): 

    return Obra1['date']<Obra2['date']
