﻿"""
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


from DISClib.DataStructures.arraylist import addLast, newList
import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.DataStructures import mapstructure as ms
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import mergesort as mrgsort
assert cf
import datetime
import itertools
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

    catalog={'artworks': None, 'artists': None, "artistID" : None, 'nationality': None,'medium':None,'nationalityartworks':None,'artworksIDSingleArtist':None,'artworksDateAcqYearMonth':None,'artworksbyDepartment':None}

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
    
    catalog['artworksDateAcqYearMonth']=mp.newMap(10000,
                                   maptype='CHAINING',
                                   loadfactor=4.0,
                                   comparefunction=None)
    
    catalog['artworksbyDepartment']=mp.newMap(10000,
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
   
    for ArtistID in Iden: 
        
        
        if mp.contains(catalog['artworksIDSingleArtist'],ArtistID): 
            listavieja2=mp.get(catalog['artworksIDSingleArtist'],ArtistID)
            lt.addLast(listavieja2['value'],new)
            mp.put(catalog['artworksIDSingleArtist'],ArtistID,listavieja2['value'])
            

        
    
        else: 
            lista2=lt.newList()
            lt.addLast(lista2,new)
            mp.put(catalog['artworksIDSingleArtist'],ArtistID,lista2)
            
    
    #Crea un diccionario con las llaver del date Acquired Año-Mes (una lista de todas las obras de esta fecha dentro de cada llave):
    dateacquiredstr=artwork['DateAcquired']

    if dateacquiredstr:
        datelst=dateacquiredstr.split('-')
        dateacquired2=datetime.date(int(datelst[0]),int(datelst[1]),int(datelst[2]))
    else:
        dateacquired2=datetime.date.today()

    Year=dateacquired2.year
    Month=dateacquired2.month
    ShortDate=str(Year)+'-'+str(Month)

    if mp.contains(catalog['artworksDateAcqYearMonth'],ShortDate):
        listavieja3=mp.get(catalog['artworksDateAcqYearMonth'],ShortDate)
        #lt.addLast(listavieja3['value'],new)
        listavieja3['value'].append(new)
        mp.put(catalog['artworksDateAcqYearMonth'],ShortDate,listavieja3['value'])

    else: 
        #lista3=lt.newList()
        lista3=[]
        #lt.addLast(lista3,new)
        lista3.append(new)
        mp.put(catalog['artworksDateAcqYearMonth'],ShortDate,lista3)



    #Crea un diccionario con las llaves del Departamaneto con value (una lista de todas las obras de este departamento):
    Department=artwork['Department']
    

    if mp.contains(catalog['artworksbyDepartment'],Department):
        listavieja4=mp.get(catalog['artworksbyDepartment'],Department)
        lt.addLast(listavieja4['value'],new)
        #listavieja4['value'].append(new)
        mp.put(catalog['artworksbyDepartment'],Department,listavieja4['value'])

    else: 
        lista4=lt.newList()
        #lista4=[]
        lt.addLast(lista4,new)
        #lista4.append(new)
        mp.put(catalog['artworksbyDepartment'],Department,lista4)

    
                






    





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

    # Se abre el mapa necesario y se crea la lista de retorno
    artistas = lista["artists"]
    llaves = mp.keySet(artistas)
    retorno = lt.newList()


    for x in range(lt.size(llaves)):

        #por cada artista se revisa si su fecha de nacimiento esta dentro de los parametros
        grupo = mp.get(artistas, lt.getElement(llaves, x))["value"]
        edad = int(grupo["begindate"])
        

        if edad != 0 and edad != None and edad >= inicio and edad <= final:


            #se saca la info del artista y se añade a la lista de retorno
            nombre = grupo["name"]
            muerte = int(grupo["enddate"])
            genero = grupo["gender"]
            nacionalidad = grupo["nationality"]
            
            agregar = {"nombre" : nombre, "edad" : edad, "muerte" : muerte, "genero" : genero, "nacionalidad" : nacionalidad}
            lt.addLast(retorno, agregar)
    
    #se ordena la lista
    mrgsort.sort(retorno, compArtistasByBegindate)

    return retorno

def obrasCronologicoacq(inicio,final,catalog):
    '''
    Retorna las primeras tres y últimas 3 obras adquiridas en el rango de fechas inicio-final
    '''
    
    #Extrae el map con llaves artistID y values info del artista
    Artistas=catalog['artistID']
    #Pone las fechas iniciales en formate datetime
    YearInit=inicio.year
    MonthInit=inicio.month

    FechaInit=str(YearInit)+'-'+str(MonthInit)
    #Pone las fechas finales en formato datetime
    YearFinal=final.year
    MonthFinal=final.month

    FechaFinal=str(YearFinal)+'-'+str(MonthFinal)

    ObrasAux=[]
    for año in range(YearInit,YearFinal+1):
        for mes in range(MonthInit,MonthFinal+1): 
            FechaAux=str(año)+'-'+str(mes)
            if mp.contains(catalog['artworksDateAcqYearMonth'],FechaAux):
                ObrasAuxRango=mp.get(catalog['artworksDateAcqYearMonth'],FechaAux)['value']
                ObrasAux.append(ObrasAuxRango)
            

        
    ObrasAuxflat = list(itertools.chain(*ObrasAux))

    ObrasAuxflat2=lt.newList()

    for Obra in ObrasAuxflat[::-1]: 
        #print(Obra)
        lt.addLast(ObrasAuxflat2,Obra)




    

    mrgsort.sort(ObrasAuxflat2, cmpArtworkByDateAcquired)

    for i in range(lt.size(ObrasAuxflat2)):
        Obra=lt.getElement(ObrasAuxflat2,i)
        ObrasAuxflat[i]=Obra



    for Obra in ObrasAuxflat:


        FechaReal=Obra['dateacquired']
        

        if  FechaReal < inicio: 
            ObrasAuxflat.remove(Obra)
        else: 
            break
    
    
    for Obra in ObrasAuxflat[::-1]:

        FechaReal=Obra['dateacquired']
        

        if  FechaReal > final: 
            ObrasAuxflat.remove(Obra)
        else: 
            break

    
    for i in range(3):
        nombre=''
        Obra=ObrasAuxflat[i]
        ConstidObra=Obra['constituentid']
        ConstidObra=ConstidObra.translate({ord(z): None for z in '[]'})
        ConstidObra=ConstidObra.split(',')
        ConstidObra=ConstidObra[0]

        
        nombree=mp.get(Artistas,ConstidObra)['value']
        nombre=nombree['name']

        Obra['artistname']=nombre
        ObrasAuxflat[i]=Obra
    
    for i in range(3):
        l=len(ObrasAuxflat)-(i+1)
        nombre=''
        Obra=ObrasAuxflat[l]
        ConstidObra=Obra['constituentid']
        ConstidObra=ConstidObra.translate({ord(z): None for z in '[]'})
        ConstidObra=ConstidObra.split(',')
        ConstidObra=ConstidObra[0]

        nombree=mp.get(Artistas,ConstidObra)['value']
        nombre=nombree['name']
    
        Obra['artistname']=nombre
        ObrasAuxflat[l]=Obra

    return ObrasAuxflat


def Nacionalidad_obras(catalog):
    """
    Lista con la nacionalidad
    """

    #se bisca el mapa con nacionalidad - obra
    artistas = catalog["nationalityartworks"]
    llaves = mp.keySet(artistas)
    retorno = lt.newList()

    
    for x in range(lt.size(llaves)):

        #añade a una lista el la nacionalidad y el numero de obras que tiene
        grupo = mp.get(artistas, lt.getElement(llaves, x))["value"]
        mom = [lt.getElement(llaves, x),int(lt.size(grupo))]
        lt.addLast(retorno, mom)

    #Se ordenan los valores
    mrgsort.sort(retorno, compArtwrkByNatio)

    return retorno

        




def ObrasArtista(catalog,nombre): 

    #Saca los indices de artistas y artistsID
    Artistas=catalog['artists']
    #Obtiene el constituend ID del artista
    IDArtistamap=mp.get(Artistas,nombre)['value']
    IDArtista=IDArtistamap['constituentid']
    #Obtiene todas las obras del artista
    Obras=mp.get(catalog['artworksIDSingleArtist'],IDArtista)['value']
    ObrasLista=Obras
    #Saca el número total de obras del artista buscado
    TotalObras=len(ObrasLista)
    #Crea una lista y un diccionario auxiliares
    ObrasArtistaTecnica=[]
    Tecnicas={}

    #Recorre la lista de obras del artista y va contando las técnicas que tiene
    for i in range(len(ObrasLista)): 
        Obra=lt.getElement(ObrasLista,i)
        TecnicaObra=Obra['medium']
        Tecnicas[TecnicaObra]=Tecnicas.get(i, 0) + 1
        
    #Saca el total de técnicas del artista y la más usada y cuántas tiene
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
    #Saca los repetidos de la lista
    seen = set()
    ObrasArtistaTecnica2 = []
    for d in ObrasArtistaTecnica:
        t = tuple(sorted(d.items()))
        if t not in seen:
            seen.add(t)
            ObrasArtistaTecnica2.append(d)

    
    return TotalObras,TotalTecnicas-1,TecnicaMasUsada, ObrasArtistaTecnica,ObrasArtistaTecnica2

def Transporte(catalog,depa): 

    '''
    Calcula el costo e inforación asociada a transportar un departamento del museo
    '''
    #Obtiene las obras del catalogo
    ObrasTotal=catalog['artworksbyDepartment']
    ObrasDepto=mp.get(ObrasTotal,depa)['value']
    #Crea una nueva lista para las obras del departamento a transportar
    ObrasDepto1=lt.newList()
    ObrasDepto2=lt.newList()
    #Acumulación del precio de transporte por obra
    TotalPrecio=0
    #Acumulación del peso total de las obras
    TotalPeso=0
    #Iniciliza los precios máximos y sus correspondientes obras y las fechas mínimas con sus correspondientes obras
    maxC1=-1
    maxC2=-1
    maxC3=-1
    maxC4=-1
    maxC5=-1

    eltoC1={'name':'','dateacquired':'','constituentid':'','date':'','medium':'','dimensions':'','department':''
    ,'creditline':'','classification':'','circumference':'','depth':'','diameter':'','height':'','length':'','weight':'','width':''}

    eltoC2=eltoC3=eltoC4=eltoC5=eltoP1=eltoP2=eltoP3=eltoP4=eltoP5=eltoC1


    maxP1=2030
    maxP2=2030
    maxP3=2030
    maxP4=2030
    maxP5=2030


    #Recorre todas las obras del catálogo para ver calcular su precio
    for i in range(lt.size(ObrasDepto)-1):
        
        #Obtiene la obra
        Obra=lt.getElement(ObrasDepto,i+1)
        #Obtiene la fecha de la obra
        fecha=int(Obra['date'])

        if fecha:
            fecha=int(fecha)
        else:
            fecha=2021
        
        #Función que calcula el costo de transporte de una obra
        costo=CalcularCosto(Obra)
        #Función que calcula el peso de una obra
        peso=CalcularPeso(Obra)
        #Se le añade el atributo 'costo' a cada obra
        Obra['cost']=costo
        #Se acumulan el precio y el peso
        TotalPrecio+=costo
        TotalPeso+=peso
        
        #Se van actualizando las obras con precio máximo y las obras con fecha mínima
        if costo>maxC1:
            eltoC5=eltoC4
            maxC5=maxC4

            eltoC4=eltoC3
            maxC4=maxC3

            eltoC3=eltoC2
            maxC3=maxC2

            eltoC2=eltoC1
            maxC2=maxC1
            

            eltoC1=Obra
            maxC1=costo
       
        elif costo>maxC2:

            eltoC5=eltoC4
            maxC5=maxC4

            eltoC4=eltoC3
            maxC4=maxC3

            eltoC3=eltoC2
            maxC3=maxC2



            eltoC2=Obra
            maxC2=costo
        elif costo>maxC3:

            eltoC5=eltoC4
            maxC5=maxC4

            eltoC4=eltoC3
            maxC4=maxC3


            eltoC3=Obra
            maxC3=costo
        elif costo>maxC4:
            eltoC4=Obra
            maxC4=costo
        elif costo>maxC5:
            eltoC5=Obra
            maxC5=costo




        if fecha < maxP1:

            eltoP5=eltoP4
            maxP5=maxP4

            eltoP4=eltoP3
            maxP4=maxP3

            eltoP3=eltoP2
            maxP3=maxP2

            eltoP2=eltoP1
            maxP2=maxP1


            eltoP1=Obra
            maxP1=fecha
        elif fecha<maxP2:
            eltoP5=eltoP4
            maxP5=maxP4

            eltoP4=eltoP3
            maxP4=maxP3

            eltoP3=eltoP2
            maxP3=maxP2



            eltoP2=Obra
            maxP2=fecha
        elif fecha<maxP3:

            eltoP5=eltoP4
            maxP5=maxP4

            eltoP4=eltoP3
            maxP4=maxP3



            eltoP3=Obra
            maxP3=fecha
        elif fecha<maxP4:

            eltoP5=eltoP4
            maxP5=maxP4



            eltoP4=Obra
            maxP4=fecha
        elif fecha<maxP5:

            eltoP5=Obra
            maxP5=fecha
    
    #Se calcula el total de obras del departamento
    TotalObras=lt.size(ObrasDepto)

    #Se guardan en listas las obras con precio máximo y las obras con fecha mínima
    lt.addLast(ObrasDepto1,eltoC1)
    lt.addLast(ObrasDepto1,eltoC2)
    lt.addLast(ObrasDepto1,eltoC3)
    lt.addLast(ObrasDepto1,eltoC4)
    lt.addLast(ObrasDepto1,eltoC5)

    lt.addLast(ObrasDepto2,eltoP1)
    lt.addLast(ObrasDepto2,eltoP2)
    lt.addLast(ObrasDepto2,eltoP3)
    lt.addLast(ObrasDepto2,eltoP4)
    lt.addLast(ObrasDepto2,eltoP5)

    return TotalObras, TotalPrecio,TotalPeso,ObrasDepto1, ObrasDepto2
        






def artistasPro(catalog, inicio, fin, top):
    
    artistas = catalog["artists"]
    Obras_por_id = catalog["artworksIDSingleArtist"]
    llaves = mp.keySet(artistas)
    retorno = lt.newList()
    errores = 0


    for x in range(lt.size(llaves)):

        #por cada artista se revisa si su fecha de nacimiento esta dentro de los parametros
        grupo = mp.get(artistas, lt.getElement(llaves, x))["value"]

        edad = int(grupo["begindate"])
        

        if edad != 0 and edad != None and edad >= inicio and edad <= fin:


            codigo = grupo["constituentid"]
            try:
                obras = mp.get(Obras_por_id, codigo)["value"]
                lt.addLast(retorno, [ lt.getElement(llaves, x), int(lt.size(obras)), codigo])
            except:
                errores += 1

    mrgsort.sort(retorno, compArtsOrbas)
    top_Li = lt.newList()

    cant = 0
    posiciones = 1
    while cant < top:
        mom = lt.getElement(retorno, posiciones)
        if not lt.isPresent(top_Li, mom):
            lt.addLast(top_Li, mom)
            cant +=1
        posiciones += 1

    
    top_Li_compl = lt.newList()
    for x in range(lt.size(top_Li)):

        mom = lt.getElement(top_Li, x+1)
        grupos = mp.get(Obras_por_id, mom[2])["value"]
        espacio = lt.newList()
        presentes = lt.newList()

        for y in range(lt.size(grupos)):

            obra = lt.getElement(grupos, y)
            medio = obra["medium"]
            

            try:

                if lt.isPresent(presentes, medio):

                    posi = lt.isPresent(presentes, medio) 
                    val = lt.getElement(espacio, posi)[1] + 1
                    lt.changeInfo(espacio, posi, [medio, val])
                else:
                    lt.addLast(espacio, [medio, 1])
                    lt.addLast(presentes, medio)
            except:
                errores += 1
                
        mrgsort.sort(espacio, compArtMetodos)
        mejor = lt.getElement(espacio, 1)
        mom.append(mejor)
        lt.addLast(top_Li_compl, mom)
    
    if lt.getElement(top_Li_compl, 1)[1] == lt.getElement(top_Li_compl, 2)[1]:
        print("Top 1 y 2 misma cantidad")
        if lt.getElement(top_Li_compl, 1)[3][1] < lt.getElement(top_Li_compl, 2)[3][1]:
            lt.exchange(top_Li_compl, 1, 2)

    

    return top_Li_compl









# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento

def cmpbydate(Obra1,Obra2): 

    return Obra1['date']<Obra2['date']

def compArtistasByBegindate(art1, art2):
    """
    compara artistas por su fecha de nacmiento 
    """
    return art1["edad"] < art2["edad"]

def cmpArtworkByDateAcquired(artwork1,artwork2): 
    """
    Devuelve verdadero (True) si el 'DateAcquired' de artwork1 es menores que el de artwork2
    Args:
    artwork1: informacion de la primera obra que incluye su valor 'DateAcquired'
    artwork2: informacion de la segunda obra que incluye su valor 'DateAcquired'
    """
    return artwork1['dateacquired']<artwork2['dateacquired']

def compArtwrkByNatio(A1, A2):
    """
    compara la cantidad de obras en una nacionalidad
    """
    return A1[1] > A2[1]

def CalcularCosto(Obra):

    '''
    Retorna el costo aproximado de transpotar una obra de arte
    '''
   
    depth=Obra['depth']
    height=Obra['height']
    weight=Obra['weight']
    width=Obra['width']
    precio=0
    if weight or (height and width) or (height and width and depth):
        if weight:
            precio1=float(weight)*72
            precio=precio1
        if (height and width):
            precio2=(float(height)*float(width)*72)/(100**2)
            precio=max(precio,precio2)
        
        if (height and width and depth):
            precio3=(float(height)*float(width)*float(depth)*72)/(100**3)
            precio=max(precio,precio3)

        

    else:
         precio=42

    return precio

def CalcularPeso(Obra): 
    '''
    Retorna el peso aproximado de una obra 
    '''
    weight=Obra['weight']

    if weight:
        Peso=float(weight)
    else:
        Peso=0
    return Peso


def compPrecio(obra1,obra2):
    '''
    Compara por precio de transporte en orden descendente 
    '''
    return float(obra1['cost']) > float(obra2["cost"])

def compFecha(obra1,obra2):
    '''
    Compara por precio de transporte en orden descendente 
    '''
    return int(obra1['date']) < int(obra2["date"])

def compArtsOrbas(A1, A2):
    """
    compara la cantidad de obras de un artista
    """
    return A1[1] > A2[1]

def compArtMetodos(A1, A2):
    """
    compara la cantidad de obras de un artista
    """
    return A1[1] > A2[1]
