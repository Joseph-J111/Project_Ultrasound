import struct
import time

 #---------------- begin_function -----------------------------

def read_data(file_path) :
    f = open(file_path,'rb') #read binary
    try : 
        while True :
            bytes = f.read(4)
            if len(bytes) < 4:
                return "Erreur : données incomplètes"
            valeur = struct.unpack('<i', bytes)[0]  #f pour float
            return valeur
    
    except IOError :
        return f"Erreur d'ouverture "
    finally :
        f.close()


#-------------------- end_function -------------------------
        #test de la fonction dans terminal
fichier_test = "dev/test_binaire.bin"    #chemin à modifier 
while True : 
 resultat = read_data(fichier_test)
 print(f"Lecture du fichier : {fichier_test} ")
 print(f"Valeur trouvée : {resultat} mm")
 print(f"               Ctrl + C pour stopper ^^")
 time.sleep(1)



