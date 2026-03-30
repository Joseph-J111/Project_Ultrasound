import socket
import struct
import time


# ----------------- Server ----------------------------------

def sender( Ip_PC,port,file_path ) :
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create an INET, STREAMing socket
    s.bind((Ip_PC, port))   
    s.listen()

    print(f" attente d'un client")

    conn, addr = s.accept()
    with  conn: 
        while True :
            with open(file_path, "rb") as f:                          #chemin à modifier !!
                bytes = f.read(4) # Lecture des 4 octets binaires
                if len(bytes) == 4:
                    s.sendall(bytes)  #envoie de en binaire de la distance
                    time.sleep(0.5)  # attente pour laisser le temps de calcul / A VERIFIER
            
     

