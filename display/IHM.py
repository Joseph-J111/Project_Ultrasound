import tkinter as tk


#create the main window
root=tk.Tk()  #prend la librairie de tkinter
root.title("Résultat")

# Create a label to print the distance
label_distance = tk.Label(root, text="Enter your name")
label_distance.pack(pady=30)

root.mainloop()   #permet d'afficher la fenêtre et de la maintenir ouverte quand on lance IHM
