import tarfile
import numpy as np
import os
import shutil


#ZZ= #Carpeta de destino final para los archivos corregidos
ZZ= "/home/sandra/Documentos/Servicio_social/zenith"

zenitcorr=ZZ
os.chdir(zenitcorr)
dia=os.listdir(zenitcorr)
for k in dia:
    #se eliminan las carpetas vacías
    if len(os.listdir(k))==0:
        shutil.rmtree(k)
    else:
    #las secuencias se mueven a una única carpeta
        file = os.listdir(k)
        for ii in file:
            allseq=os.listdir(ZZ+"/"+k+"/"+ii)
            for ff in allseq:
                 shutil.move(ZZ+"/"+k+"/"+ii+"/"+ff,ZZ+"/"+k)
            shutil.rmtree(ZZ+"/"+k+"/"+ii)
        
        nfile=os.listdir(k)
    #se empaquetan y comprimen los archivos
        with tarfile.open(k+".tar.gz", "w:gz") as tar:
            for doc in nfile:
                tar.add(k+"/"+doc)
        shutil.rmtree(k) 
