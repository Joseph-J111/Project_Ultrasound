import os
import time
import struct
from PIL import Image, ImageDraw, ImageFont

# --- Configuration ---
FB_DEVICE = "/dev/fb0"
DRIVER_DEVICE = "/dev/DUsound"

def get_fb_info():
    """ Récupère la taille de l'écran via sysfs ou valeurs par défaut """
    # Sur STM32MP1 DK2, la résolution est généralement 480x800
    return (480, 800) 

def read_sensor():
    """ Lecture du driver C """
    try:
        # On ouvre en binaire pour lire l'entier (int) envoyé par le driver C
        with open(DRIVER_DEVICE, "rb") as f:
            data = f.read(4)
            if len(data) == 4:
                # 'i' pour integer (4 octets)
                val = int(struct.unpack('i', data)[0])
                return f"{val} mm"
            return "Format Erreur"
    except Exception:
        return "Erreur Driver"

def main():
    width, height = get_fb_info()
    
    # Couleurs
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    BLUE  = (0, 102, 204)

    # Chargement de la police (adapter le chemin si besoin sur Buildroot)
    try:
        font_large = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf", 60)
        font_small = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSans.ttf", 25)
    except:
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()

    print(f"Lancement de l'affichage sur {FB_DEVICE} ({width}x{height})")

    try:
        # Ouverture du framebuffer en mode écriture binaire
        with open(FB_DEVICE, "wb") as fb:
            while True:
                # 1. Création d'une image vierge (Mode RGB)
                img = Image.new('RGB', (width, height), BLACK)
                draw = ImageDraw.Draw(img)

                # 2. Lecture de la donnée
                display_val = read_sensor()

                # 3. Dessin des textes
                title = "Mesure Ultrason (HC-SR04)"
                
                # Calcul positions pour centrer
                w_t, h_t = draw.textbbox((0, 0), title, font=font_small)[2:]
                draw.text(((width - w_t) // 2, 50), title, font=font_small, fill=BLUE)

                w_v, h_v = draw.textbbox((0, 0), display_val, font=font_large)[2:]
                draw.text(((width - w_v) // 2, (height - h_v) // 2), display_val, font=font_large, fill=WHITE)

                # 4. Conversion et Envoi au Framebuffer
                # Le FB attend souvent du BGR ou du RGB 16/24/32 bits. 
                # Si l'image est inversée ou bleue, on utilise : img.convert('RGB')
                # Pour un FB 32 bits (standard sur MP1), on convertit en 'RGBA' ou 'RGBX'
                raw_data = img.convert('RGBX').tobytes()
                
                fb.seek(0)
                fb.write(raw_data)
                fb.flush()

                time.sleep(0.5) # 2 FPS pour économiser le CPU

    except KeyboardInterrupt:
        print("\nArrêt du programme.")

if __name__ == "__main__":
    main()
