import socket
import struct
import tkinter as tk

def receiver(Ip_Pc,port) :
     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((Ip_Pc,port))
        while True :
            data=s.recv(4)
            valeur = struct.unpack('<f', data)[0]
            print(f"Valeur trouvée : {valeur} cm")




#create the main window
root=tk.Tk()  #prend la librairie de tkinter
root.title("Résultat")
root.geometry("300x200")  #taille de la fenêtre

# Create a label to print the distance
label_distance = tk.Label(root, text="En attente ..")
label_distance.pack(pady=30)

root.after(100, receiver)
root.mainloop()   #permet d'afficher la fenêtre et de la maintenir ouverte quand on lance IHM
