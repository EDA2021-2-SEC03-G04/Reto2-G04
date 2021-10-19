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


from DISClib.DataStructures.arraylist import addLast
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

    catalog['artworksIDSingleArtist']=mp.newMap(10000,
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
        #print(type(listavieja['value']))
        #print(listavieja['value'])

        
    
    else: 
        lista=lt.newList()
        lt.addLast(lista,new)
        mp.put(catalog['nationalityartworks'],Nationality,lista)
        #print(type(lista))
        #print(lista)
        


    #Crea el diccionario de Obras por Medio
    Medio=artwork['Medium']

    if mp.contains(catalog['medium'],Medio):
        listavieja=mp.get(catalog['medium'],Medio)
        lt.addLast(listavieja['value'],new)
        mp.put(catalog['medium'],Medio,listavieja['value'])
    else: 
        lista=lt.newList()
        lt.addLast(lista,new)
        mp.put(catalog['medium'],Medio,lista)


    Iden = artwork['ConstituentID']
    Iden = Iden.translate({ord(i): None for i in '[]'})
    Iden = Iden.split(',')

    #Crea un diccionario con las llaves del ID de artistas y con value todas las obras en la que ese artista participa
    i=0
    for ArtistID in Iden: 
        #print(Iden)
        #print(ArtistID)
        i=i+1
        if mp.contains(catalog['artworksIDSingleArtist'],ArtistID): 
            listavieja2=mp.get(catalog['artworksIDSingleArtist'],ArtistID)
            #print(type(listavieja2['value']))
            lt.addLast(listavieja2['value'],new)
            mp.put(catalog['artworksIDSingleArtist'],ArtistID,listavieja2['value'])
            

        
    
        else: 
            lista2=lt.newList()
            #print(type(lista2))
            lt.addLast(lista2,new)
            mp.put(catalog['artworksIDSingleArtist'],ArtistID,lista2)
            #print(lista)
            #print(type(lista2))
            #print(i)
            



    





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
        

def artistasCronologico(lista, inicio, final):
    """
    Retorna una lista con los artistas ordenados por epoca
    """

    artistas = lista["artists"]
    llaves = mp.keySet(artistas)
    retorno = lt.newList()


    for x in range(lt.size(llaves)):

        grupo = mp.get(artistas, lt.getElement(llaves, x))["value"]
        edad = int(grupo["begindate"])
        

        if edad != 0 and edad != None and edad >= inicio and edad <= final:

            nombre = grupo["name"]
            muerte = int(grupo["enddate"])
            genero = grupo["gender"]
            nacionalidad = grupo["nationality"]
            
            agregar = {"nombre" : nombre, "edad" : edad, "muerte" : muerte, "genero" : genero, "nacionalidad" : nacionalidad}
            lt.addLast(retorno, agregar)
    
    mrgsort.sort(retorno, compArtistasByBegindate)

    return retorno

def ObrasArtista(catalog,nombre): 

    #Saca los indices de artistas y artistsID
    Artistas=catalog['artists']
    #Obtiene el constituend ID del artista
    IDArtistamap=mp.get(Artistas,nombre)['value']
    IDArtista=IDArtistamap['constituentid']

    #print(IDArtista)

    #TotalObras,TotalTecnicas,TecnicaMasUsada,ObrasArtistaTecnica=controller.ObrasArtista()

    Obras=mp.get(catalog['artworksIDSingleArtist'],IDArtista)['value']
    #print(type(Obras))
    #print()
    #print()
    #print(Obras)
    ObrasLista=Obras
    #print(type(ObrasLista))
    #print(ObrasLista)
    #print()
    

    TotalObras=len(ObrasLista)


    ObrasArtistaTecnica=[]
    Tecnicas={}

    for i in range(len(ObrasLista)): 
        Obra=lt.getElement(ObrasLista,i)
        #print(Obra)
        #print(type(Obra))
        #print( )
        #print(Obra.keys())
        TecnicaObra=Obra['medium']
        Tecnicas[TecnicaObra]=Tecnicas.get(i, 0) + 1
        
    
    TotalTecnicas=len(Tecnicas)
    if TotalTecnicas==0:
        maxim=0
        TecnicaMasUsada='No hay suficiente información'
    else: 
        maxim=max(Tecnicas.values())
        TecnicaMasUsada=str(list(Tecnicas.keys())[list(Tecnicas.values()).index(maxim)])

    
    #Crea la lista de obras del artista con la técnica más usada
    for i in range(lt.size(ObrasLista)):
        Obra=lt.getElement(ObrasLista,i) 
        if Obra['medium']==TecnicaMasUsada:
            ObrasArtistaTecnica.append(Obra)


    #TotalObras=len(list(dict.fromkeys(ObrasLista)))
    TotalObras=lt.size(ObrasLista)
    #print('YYYYYY')
    #print(type(ObrasArtistaTecnica))
    #ObrasArtistaTecnica2=list(set(ObrasArtistaTecnica))


    seen = set()
    ObrasArtistaTecnica2 = []
    for d in ObrasArtistaTecnica:
        t = tuple(sorted(d.items()))
        if t not in seen:
            seen.add(t)
            ObrasArtistaTecnica2.append(d)

    

   # print(ObrasArtistaTecnica)
    #print(type(ObrasArtistaTecnica))
    #print('AAAAAAAAAA POR QUÉ NO FUNCIONA')
    

    


    return TotalObras,TotalTecnicas-1,TecnicaMasUsada, ObrasArtistaTecnica,ObrasArtistaTecnica2


        



   







    










    return True


    









# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento

def cmpbydate(Obra1,Obra2): 

    return Obra1['date']<Obra2['date']

def compArtistasByBegindate(art1, art2):
    """
    compara artistas por su fecha de nacmiento 
    """
    return art1["edad"] < art2["edad"]
