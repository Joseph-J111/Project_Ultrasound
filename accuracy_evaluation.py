import time
mesures = []

# 2. Lecture de 100 mesures
for i in range(100):
    f = open("/dev/DUsound", "rb")
    donnees = f.read(4) # On lit 4 octets (la taille d'un int en C)
    
    # Transformation des octets en nombre entier
    # 'little' car l'ARM de la STM32 range les octets dans cet ordre
    valeur = int.from_bytes(donnees, "little")
    
    mesures.append(valeur)
    print("Mesure", i, ":", valeur)
    
    time.sleep(0.1)

    f.close()
    

# 3. Calcul de la moyenne (division entière //)
somme = 0
for m in mesures:
    somme = somme + m
moyenne = somme // 100

# 4. Calcul de la variance
somme_carres = 0
for m in mesures:
    somme_carres = somme_carres + (m * m)

moyenne_carres = somme_carres // 100
variance = moyenne_carres - (moyenne * moyenne)

# 5. Affichage des résultats
print("------------------------")
print("Moyenne :", moyenne)
print("Variance :", variance)
