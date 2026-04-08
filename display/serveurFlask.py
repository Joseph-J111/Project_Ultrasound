from flask import Flask, render_template
import os
import struct

app = Flask(__name__)

# Route 1 : Affiche l'interface graphique (HTML + JS)
@app.route('/')
def index():
    return render_template('index.html')

# Route 2 : Renvoie uniquement le chiffre (Donnée brute)
@app.route('/data')
def get_data():
    try:
        
        fd = os.open("/dev/DUsound", os.O_RDONLY)
        donnees = os.read(fd, 4)
        distance = struct.unpack('<i', donnees)[0] 
        os.close(fd)
        return str(distance)
    except Exception as e:
        # Toujours aligné avec le contenu du try
        return f"Erreur : {str(e)}"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
