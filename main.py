import pygame
import game
pygame.init()
# prendre la resolution de l'ecran (pour plein ecran):
resolution = [pygame.display.Info().current_w, pygame.display.Info().current_h]

# creation de la fenetre
window = pygame.display.set_mode(size=(900, 500), flags=0)

# couleur de fond
window.fill((0, 255, 0))

# nom de la fenetre
pygame.display.set_caption("Simulation")

clock = pygame.time.Clock()

fullscreen = False

g = game.Game((900, 500))

while True :

    for event in pygame.event.get():
        # detection croix quitter :
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        
    

    g.actualiser(window)

    pygame.display.flip()

    clock.tick(30)  # 60 fps
