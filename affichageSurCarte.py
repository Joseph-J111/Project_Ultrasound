import pygame
import os
import sys

# 1. Configuration pour l'écran de la carte (Framebuffer)
os.environ["SDL_VIDEODRIVER"] = "fbcon"
os.environ["SDL_FBDEV"] = "/dev/fb0"

def main():
    # Initialisation
    pygame.init()
    pygame.mouse.set_visible(False) # On cache la souris sur l'écran LCD
    
    # Adaptation automatique à la taille de l'écran de la carte
    info = pygame.display.Info()
    ecran_taille = (info.current_w, info.current_h)
    fenetre = pygame.display.set_mode(ecran_taille, pygame.FULLSCREEN)
    
    clock = pygame.time.Clock()
    
    # COULEURS
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    BLUE  = (0, 102, 204)

    # OPTIMISATION : On prépare les objets fixes HORS de la boucle
    # Si 'freesans' n'est pas sur Buildroot, pygame prendra la police par défaut
    font_path = pygame.font.match_font('freesans', 'dejavusans', 'liberationsans')
    bigText = pygame.font.Font(font_path, 60) 
    titleText = pygame.font.Font(font_path, 30)

    loop = True
    while loop:
        # 2. Gestion des événements (pour pouvoir quitter avec Ctrl+C)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = False

        # 3. Lecture du Driver
        try:
            fd = os.open("/dev/DUsound", os.O_RDONLY)
            # On lit les 4 octets, on décode et on nettoie les espaces/retours à la ligne
            distance_str = os.read(fd, 4).decode('utf-8').strip()
            os.close(fd)
            display_val = f"{distance_str} cm"
        except Exception as e:
            display_val = "Erreur Driver"

        # 4. DESSIN
        fenetre.fill(BLACK) # On efface l'écran

        # Affichage du titre
        surf_title = titleText.render("Mesure Ultrason (HC-SR04)", True, BLUE)
        fenetre.blit(surf_title, (ecran_taille[0]//2 - surf_title.get_width()//2, 50))

        # Affichage de la valeur (au centre)
        surf_val = bigText.render(display_val, True, WHITE)
        pos_val = surf_val.get_rect(center=(ecran_taille[0]//2, ecran_taille[1]//2))
        fenetre.blit(surf_val, pos_val)

        # 5. MISE À JOUR
        pygame.display.flip()
        
        # 10 FPS suffisent largement pour un capteur ultrason (évite de chauffer le CPU)
        clock.tick(2)

    pygame.quit()

if __name__ == '__main__':
    main()
