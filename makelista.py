"""
@author: Sandra Porras
Last update: 16-03-2020
Write in Python 3

"""


import tarfile
import shutil
import os

site='UNAM'
year='2020'



path1='/home/D1_MAXDOAS/DATA/'
path2='/home/D1_MAXDOAS/LEVEL1/'


#Carpetas excluidas
exclude=["Originales", "Josue", "originales","graficas","plots"]


month_start=1
month_end=12
months=[ str(n).zfill(2) for n in range(month_start,month_end+1)]


dic={'ACAT':'1104','ALTZ':'1101','CUAT':'1102',
     'JQRO':'1301','PALN':'1102','TOLU':'1302',
     'UNAM':'1101','VALL':'1103'}


#Se corrige la clave_identificador del equipo en el fichero y la carpeta interna
for root, dirs, files in os.walk(path1+site, topdown=False):
    for name in files:
        for month in months:
            if (year+month) in name  and name.endswith("tar.gz")  and (any(j  in os.path.join(root,name) for j in exclude) != True):
                if name.split('_')[-1].split('.')[0] != dic.get(site):
                    old_dir=os.path.join(root,name)
                    #Variable que guarda el nombre correcto del fichero
                    correct_dir = name.split(".")[0].replace(name.split('_')[-1].split('.')[0], dic.get(site))
                    new_dir=os.path.join(root,correct_dir)
                    os.makedirs(new_dir)
                    
                    
                    ftar=tarfile.open(old_dir,"r:gz")
                    ftar.extractall(new_dir)
                    ftar.close()
                    
                    for i in (os.listdir(new_dir)):
                        #Se cambia  el nombre de la carpeta interna
                        correct_file=os.path.join(new_dir,i.replace(i.split('_')[-1], dic.get(site)))
                        shutil.move(os.path.join(new_dir, i),correct_file)
                    
                       #La siguiente linea puede ser comentada. Muestra los ficheros a los que se les ha cambiado el nombre
                        print(i,"was replace by ", i.replace(i.split('_')[-1], dic.get(site)))
                        
                    #Se crea el fichero corregido 
                    with tarfile.open(new_dir+".tar.gz", "w:gz") as tar:
                        for doc in os.listdir(new_dir):
                            tar.add(os.path.join(new_dir,doc))           
                    tar.close
                    
                    #Se borra el fichero con la clave_identificador incorrecto
                    shutil.rmtree(new_dir)
                    os.remove(old_dir)

                    
                    
                    

#Se crea la lista con los elementos en DATA
lista1=[]
for root, dirs, files in  os.walk(path1+site, topdown=False):
    for name in files:
        for month in months:
            if (year+month) in name  and name.endswith("tar.gz") and (any(j  in os.path.join(root, name) for j in exclude) != True):
                
                lista1.append(os.path.join(root,name))



#Se crea la lista con los elementos en LEVEL1
lista2=[]
for root, dirs, files in  os.walk(path2+site, topdown=False):
    for name in files:
        for month in months:
            if (year+month) in name  and name.endswith("tar.gz"):
                
                #descomentar la siguiente línea si hay carpetas por descartar en LEVEL1

                #and (any(j  in os.path.join(root, name) for j in exclude) != True):
                lista2.append(os.path.join(root,name))

                
listabasename2=[ele.split('/')[-1] for ele in lista2]

listatotdo=[]
for ele in lista1:
        if (ele.split('/')[-1] in listabasename2):
                pass
                #print ('ya esta',ele.split('/')[-1])

        else:
                print ('todavia falta',ele.split('/')[-1])
                listatotdo.append(ele)
                                          
                

f=open(site+'_runscript.sh','w')
for ele in listatotdo:
        f.write('python fromlevel0tolevel1.py %s \n ' % (ele) )
f.close()