import socket
import struct
import tkinter as tk    #pour IHM

import sys

# sys.argv[0] is the name of script
# sys.argv[1] is IP
# sys.argv[2] is Port

if len(sys.argv) < 3:
    print("Usage: python3 receiver.py <IP_CARTE> <PORT>")
    sys.exit(1)

Ip_Pc = sys.argv[1]
port = int(sys.argv[2])

#init the socket
s=socket.socket(socket.AF_INET, socket.SOCK_STREAM);
s.connect((Ip_PC,port))
s.setblocking(False)

def receiver(Ip_Pc,port,s) :
        try :
            data=s.recv(4)
            if len(data) == 4 : 
                valeur = struct.unpack('<f', data)[0]
                print(f"Valeur trouvée : {valeur} cm")
        except BlockingIOError:
            pass
        root.after(100, update_distance)
    



#create the main window
root=tk.Tk()  #prend la librairie de tkinter
root.title("Résultat")
root.geometry("300x200")  #taille de la fenêtre

# Create a label to print the distance
label_distance = tk.Label(root, text="En attente ..")
label_distance.pack(pady=30)


root.after(100, receiver,Ip_Pc,port,s)

root.mainloop()   #permet d'afficher la fenêtre et de la maintenir ouverte quand on lance IHM
