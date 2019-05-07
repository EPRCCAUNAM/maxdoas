import tarfile
import numpy as np
import os
import shutil

#----------------------VARIABLES NECESARIAS------------------------------------------------

ZEN="/home/sandra/Documentos/Servicio_social/zenith"
max_arch=6
temp = "/home/sandra/Documentos/Servicio_social/temp"

DD= "/home/sandra/Documentos/Servicio_social/NON_ZERO_ZENITH_DATA/ACAT/Mediciones_nuevas"
LDD=os.listdir(DD)

ESTACION="VALL"
LAT="19.4837"
LONG="-99.1492"
CLAVE="_1103"

#------------------------------------------------------------------------------------------
#En este ciclo se accede a cada fichero de la carpeta Mediciones_nuevas y se descomprime for dircomp in range(0,len(LDD)):
for dircomp in range(0,len(LDD)):    
    ftar=tarfile.open(DD+"/"+LDD[dircomp],"r:gz")
    ftar.extractall(temp)
    #Se cambia a temp como directorio de trabajo
    os.chdir(temp)
    #Se crea una lista de todos los elementos en temp
    lout=np.array(os.listdir(temp))
    #Se separa el nombre del fichero comprimido para crear una carpeta AAMMDD_CLAVE donde se guardarán las secuencias a corregir
    name1=LDD[dircomp].split("_")
    carpeta1=temp+"/"+name1[4]+name1[3]+name1[2]+CLAVE
    #AAMMDD_CLAVE carpeta con secuencias a corregir
    os.makedirs(carpeta1)
    #AAMMDD_CLAVE carpeta con secuencias sin mediciones
    os.makedirs(carpeta1+"_nondata")
    #SAAMMDD_CLAVE secuencias con angulo cenital fuera del intervalo (-5,5)
    os.makedirs(carpeta1+"_nonzenith")

    #En este ciclo se accede a cada una de las carpetas de las secuencias
    for err in range(len(lout)):
        #Se cambia de directorio de trabajo a la carpeta de la secuencia 
        errdir=os.chdir(temp+"/"+lout[err])
        #Se crea una lista con los archivos de texto dentro de la carpeta
        lerrdir=np.array(os.listdir(errdir))
       

        #Lista auxiliar para archivos Maxdoas_meta.spe
        lismax=[] 
        for doc in range(len(lerrdir)): 
            if len(lerrdir[doc].split("_"))==10 and lerrdir[doc][0]=="M":
                lismax.append(lerrdir[doc])
        
        #Se lee cada archivo Maxdoas_meta.spe en DATOS, que contiene toda su información
        for maxd in range(len(lismax)):
            with open(lismax[maxd]) as f: 
                data =np.array(f.readlines())
            DATOS = [] 
            for i in range(len(data)):
                DATOS.append(data[i].split("\t"))
            
            #Se guarda el índice de los ángulos cenitales
            angulos0=[] 
            for ll in range(len(DATOS)):
                if len(DATOS[ll]) == 29 and float(DATOS[ll][1])==0:
                    angulos0.append(ll) 
            
            #Si el archivo no tienen ángulos cenitales, la secuencia es movida a la carpeta "nondata"
            if len(angulos0)==0:  
                for uu in lerrdir:           
                    #Verifica si el archivo a mover aún está en la carpeta y si es un archivo de texto
                    if  os.path.isfile(uu) and len(uu.split("_"))>1:
                        #Condición que descrimina a los archivos por día/secuencia/hora
                        if ( lismax[maxd].split("_")[8] in uu #secuencia
                            and lismax[maxd].split("_")[3]==uu.split("_")[3] #día
                            and ((lismax[maxd].split("_")[5]==uu.split("_")[5]
                                 #Aquí se evaluan los archivos creados a +10 y -10 minutos de Maxdoas_meta.spe (util si el equipo se ha reiniciado) 
                                 and (int(uu.split("_")[6])<=int(lismax[maxd].split("_")[6])+10
                                          and  int(uu.split("_")[6])>=int(lismax[maxd].split("_")[6])-10)
                                 ) or #hora
                            ((int(lismax[maxd].split("_")[5])+1== int(uu.split("_")[5]) 
                            and int(uu.split("_")[6]) <= 5) #si el archivo se obtuvo una hora con cinco minutos después
                            or (int(lismax[maxd].split("_")[5])-1== int(uu.split("_")[5])
                            and (int(uu.split("_")[6]) >= 55 or int(uu.split("_")[6]) == 0)))) ):  #Si el archivo se obtuvo una hora antes
                            
                            
                            #Filtro para no mover archivos Maxdoas de lismax que no han sido evaluados
                            if ( uu in lismax )== False or( uu in lismax and uu == lismax[maxd]): 
                                #Se mueven los archivos a la carpeta "nondata"
                                shutil.move(temp+"/"+lout[err]+"/"+uu, carpeta1+"_nondata")
            
            
            #Si el archivo sí tiene ángulos cenitales
            else:
                for aa in angulos0:
                    #Se evalúa si el ángulo cenital está fuera del intervalo o que no se hayan registrado mediciones
                    if  (float(DATOS[aa][25])>=5 or float(DATOS[aa][25])<=-5) or DATOS[aa][25]=="nan" :
                        #Condición para ver si el archivo a mover aún está en la carpeta y si es un archivo de texto
                        for vv in lerrdir:    
                            if os.path.isfile(vv) and len(vv.split("_"))>1:
                               
                               #Condición que descrimina a los archivos por día/secuencia/hora
                                if ( lismax[maxd].split("_")[8] in vv 
                                and lismax[maxd].split("_")[3]==vv.split("_")[3] 
                                and ((lismax[maxd].split("_")[5]==vv.split("_")[5] 
                                #Aquí se evaluan los archivos creados a +10 y -10 minutos de Maxdoas_meta.spe (util si el equipo se ha reiniciado)
                                          and (int(vv.split("_")[6])<=int(lismax[maxd].split("_")[6])+10
                                          and  int(vv.split("_")[6])>=int(lismax[maxd].split("_")[6])-10)
                                     ) or
                                ((int(lismax[maxd].split("_")[5])+1== int(vv.split("_")[5]) 
                                and int(vv.split("_")[6]) <= 10) 
                                or (int(lismax[maxd].split("_")[5])-1== int(vv.split("_")[5])
                                and (int(vv.split("_")[6]) >= 50 or int(vv.split("_")[6]) == 0)))) ):
                                    
                                    #Se mueven los archivos a la carpeta "nonzenith"
                                    #Filtro para no mover archivos Maxdoas de lismax que no han sido evaluados
                                    if ( vv in lismax )== False or( vv in lismax and vv == lismax[maxd]): 
                                            #Se mueven los archivos a la carpeta "nonzenith"
                                        shutil.move(temp+"/"+lout[err]+"/"+vv, carpeta1+"_nonzenith")
                #Si el archivo Maxdoas_meta.spe se movió a las carpetas anteriores, se pasa a evaluar otro archivo
                if os.path.isfile(lismax[maxd])==False:
                    pass
                
                #Si el archivo no fue movido, su ángulo cenital es correcto 
                else:
                    #Se editan los datos de estación, latitud y longitud dentro del archivo
                    with open(lismax[maxd], 'r+') as archivo:
                        data =np.array(archivo.readlines())
                    contenido=[] 
                    for linea in range(len(data)):
                        columnas = data[linea].split('\t')
                        if len(columnas)==29:
                            columnas[21]=ESTACION
                            columnas[22]=LAT
                            columnas[23]=LONG
                        contenido.append('\t'.join(columnas))
                    with  open(lismax[maxd], 'w') as archivo:
                        archivo.writelines(contenido)
                    for hh in lerrdir:
                       
                       #Condición para ver si el archivo a mover aún está en la carpeta y si es un archivo de texto
                        if os.path.isfile(hh) and len(hh.split("_"))>1:
                            #Condición que descrimina a los archivos por día/secuencia/hora
                            if ( lismax[maxd].split("_")[8] in hh 
                                    and lismax[maxd].split("_")[3]==hh.split("_")[3] 
                                    and ((lismax[maxd].split("_")[5]==hh.split("_")[5]        
                             #Aquí se evaluan los archivos creados a +10 y -10 minutos de Maxdoas_meta.spe (util si el equipo se ha reiniciado)             
                                              and (int(hh.split("_")[6])<=int(lismax[maxd].split("_")[6])+10
                                          and  int(hh.split("_")[6])>=int(lismax[maxd].split("_")[6])-10) 
                                         ) or
                                    ((int(lismax[maxd].split("_")[5])+1== int(hh.split("_")[5]) 
                                    and int(hh.split("_")[6]) <= 10) 
                                    or (int(lismax[maxd].split("_")[5])-1== int(hh.split("_")[5])
                                    and (int(hh.split("_")[6]) >= 50 or int(hh.split("_")[6])== 0)))) ):
                                #Se mueven los archivos a la carpeta por comprimir
                                if ( hh in lismax )== False or( hh in lismax and hh == lismax[maxd]): 
                                    shutil.move(temp+"/"+lout[err]+"/"+hh, carpeta1)
                                    
                                    
    #Si la carpeta a comprimir no está vacía se mueve a la carpeta ZEN para revisar si las secuencias están completas.
    if len(os.listdir(carpeta1))>0:
        shutil.move(carpeta1,ZEN)
    #Se elimina el contenido de la carpeta temp 
    shutil.rmtree(temp)
    
#Se cambia de directorio de trabajo a la carpeta donde están los archivos corregidos            
ZZ= ZEN
os.chdir(ZZ)

#Se crea una lista de las carpetas que contienen los archivos corregidos
LZZ=os.listdir(ZZ)

#En este ciclo se evalua cada archivo dentro de las carpetas en ZEN: AAMMDD_EST

for zz in range(len(LZZ)): #len(LZZ)
    
    os.rename(ZZ+"/"+LZZ[zz],ZZ+"/"+"20"+LZZ[zz])
    nwd=ZZ+"/"+"20"+LZZ[zz]
    dirz=os.chdir(nwd)
    #Se crea una lista de los archivos contenidos en cada carpeta
    ldirz=os.listdir(dirz)
#Se eliminan los archivos que han sido creados durante la noche, de 20:00 a 7:00
    for ii in ldirz:
        if len(ii)>16 and int(ii.split("_")[5])<7 or int(ii.split("_")[5])>20:  
            os.remove(nwd+"/"+ii)

    lismz=[]  #Se usa una lista auxiliar con los archivos Maxdoas_meta.spe
    for dc in range(0,len(ldirz)):
        if os.path.isfile(ldirz[dc]):
            if  len(ldirz[dc].split("_"))==10 and ldirz[dc][0]=="M": #Se buscan los archivos Maxdoas_meta.spe
                lismz.append(ldirz[dc]) #Se agregan a la lista

    #En este ciclo se evalua cada archivo Maxdoas_meta.spe dentro de la lisma lismz
    for mx in range(len(lismz)):
        
        if os.path.isfile(lismz[mx]) == False: #Si el archivo ha sido movido no se ejecuta el resto del programa
            pass
        else:
            #Se lee la fecha de creación del archivo Maxdoas_meta.spe
            with open(lismz[mx]) as f: 
                data =np.array(f.readlines())
            DATOS = []
            for jj in range(len(data)):
                DATOS.append(data[jj].split("\t"))
            #Se da nombre a una carpeta nueva con AAMMDD_SEQ
            carpeta=(DATOS[1][0][0:10].split(".")[2][:]
             +DATOS[1][0][0:10].split(".")[1]
             +DATOS[1][0][0:10].split(".")[0]
             +"_"+lismz[mx].split("_")[-2])
            #Si la carpeta aun no existe se crea
            if os.path.isdir(carpeta)==False: 
                os.makedirs(carpeta)    
            #Se mueven los archivos a la carpeta AAMMDD_SEQ si coinciden con la fecha de creación y secuencia        
            for tt in range(len(ldirz)):    
                if (len(ldirz[tt])>16) and os.path.isfile(ldirz[tt])  and (( lismz[mx].split("_")[8] )in ldirz[tt] ) and (lismz[mx].split("_")[3] == ldirz[tt].split("_")[3] ) :
                    shutil.move(nwd+"/"+ldirz[tt], carpeta)
    

#Se reinicia el ciclo sobre las carpetas AAMMDD_EST                    
LZZ=os.listdir(ZZ)                    
for zz in range(len(LZZ)):
    dirz=os.chdir(ZZ+"/"+LZZ[zz])
    ldirz=os.listdir(dirz)
    #En este ciclo se verifica que todas las secuencias estén completas
    for ss in ldirz:
        if len(os.listdir(ss))%max_arch !=0: #Los archivos dentro de la carpeta de secuencia debe ser multiplo de max_arc y por lo tanto el residuo debe ser cero
    #Si no se cumple la condición anterior se imprimen las carpetas incompletas

            print(ss, len(os.listdir(ss)))
        else:
		#Si la carpeta AAMMDD_SEQ no coindice en AAMMDD con la carpeta AAMMDD_EST y existe una carpeta AAMMDD_EST, se mueve la carpeta de secuencia a ella
            if (LZZ[zz][0:8] in ss)==False:
                if os.path.isdir(ZZ+"/"+ss[0:8]+LZZ[zz][-5::]):
                    shutil.move(ss, ZZ+"/"+ss[0:8]+LZZ[zz][-5::])
#Si no existe carpeta AAMMDD_EST, se crea y se mueve a ella AAMMDD_SEQ
                else:

                    os.makedirs(ZZ+"/"+ss[0:8]+LZZ[zz][-5::])
                    shutil.move(ss, ZZ+"/"+ss[0:8]+LZZ[zz][-5::])  
                
                
#El último programa a ejecutar comprime las carpetas 
    
"""Al finalizar éste programa se debe ejecutar: Filtro_secuencias"""

