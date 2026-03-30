from flask import Flask, render_template
import os

app = Flask(__name__)

# Route 1 : Affiche l'interface graphique (HTML + JS)
@app.route('/')
def index():
	return render_template('index.html') # Envoie le fichier HTML

# Route 2 : Renvoie uniquement le chiffre (Donnée brute)
@app.route('/data')
def get_data():
	try:
    		# Lecture du driver dans le kernelspace [cite: 537, 638, 648]
    		fd = os.open("/dev/DUsound", os.O_RDONLY)
    		distance = os.read(fd, 4).decode().strip()
    		os.close(fd)
    		return distance # Renvoie juste "15.4" par exemple
	except:
    		return "Erreur"
