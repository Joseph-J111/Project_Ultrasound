import struct

 #---------------- begin_function -----------------------------

def read_data(file_path) :
    f = open(file_path,'rb') #read binary
    try : 
        while True :
            bytes = f.read(4)
            if len(bytes) < 4:
                return "Erreur : données incomplètes"
            valeur = struct.unpack('<f', bytes)[0]  #f pour float
            return valeur
    
    except IOError :
        return f"Erreur d'ouverture "
    finally :
        f.close()
        
def update_IHM() :
    res=read_data(fichier_test)

    if res is None :
        label_distance.config(text="Données incomplètes", fg="orange")
    elif res == "Erreur d'ouverture":
        label_distance.config(text="Fichier introuvable", fg="red")
    else:
        # On met à jour le texte du label avec la valeur
        label_distance.config(text=f"{res:.2f} cm", fg="black")
    
    # CRITIQUE : On replanifie la mise à jour dans 500ms
    # On passe le NOM de la fonction 'update_gui', on ne l'appelle pas avec ()
    root.after(500, update_IHM)





#-------------------- end_function -------------------------
        #test de la fonction dans terminal
fichier_test = "dev/test_binaire.bin"    #chemin à modifier 
resultat = read_data(fichier_test)
print(f"Lecture du fichier : {fichier_test} ")
print(f"Valeur trouvée : {resultat} cm")

        # test de la fonction dans IHM
import tkinter as tk

#create the main window
root=tk.Tk()  #prend la librairie de tkinter
root.title("Résultat")
root.geometry("300x200")  #taille de la fenêtre

# Create a label to print the distance
label_distance = tk.Label(root, text="En attente ..")
label_distance.pack(pady=30)

root.after(100, update_IHM)  #appel de la fonction après 100ms pour éviter de bloquer l'affichage de la fenêtre
root.mainloop()   #permet d'afficher la fenêtre et de la maintenir ouverte quand on lance IHM


