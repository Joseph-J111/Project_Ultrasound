from flask import Flask, render_template
import os
import struct

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
    		donnees = os.read(fd, 4)
            distance = struct.unpack('<i', donnees)[0]  #f pour float
    		os.close(fd)
    		return str(distance) # Renvoie juste "15.4" par exemple
	except:
    		return "Erreur"


if __name__ == '__main__':
    # host='0.0.0.0' permet au serveur d'être visible par ton PC sur le réseau
    app.run(host='0.0.0.0', port=5000)
