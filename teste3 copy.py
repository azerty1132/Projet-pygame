import pygame
import sys

# Initialisation de Pygame
pygame.init()

# Constantes pour les couleurs et les dimensions de l'écran
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
SOL_COULEUR = (100, 100, 100)  # Couleur du sol
LARGEUR_ECRAN = 800
HAUTEUR_ECRAN = 600
SOL_HAUTEUR = 50  # Hauteur du sol

# Facteur de rapprochement de la caméra (20%)
CAMERA_PROXIMITE = 0.2

class Joueur(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(BLANC)
        self.rect = self.image.get_rect()
        self.rect.center = (LARGEUR_ECRAN // 2, HAUTEUR_ECRAN // 2)
        self.vitesse_y = 0  # Initialisation de la vitesse verticale à zéro
        self.gravite = 0.6  # Valeur de la gravité ajustée
        self.force_saut = -12  # Valeur de la force de saut ajustée
        self.a_sauté = False  # Variable pour suivre si le joueur a déjà sauté

    def update(self):
        # Appliquer la gravité
        self.vitesse_y += self.gravite  # Ajouter la gravité à la vitesse verticale
        self.rect.y += self.vitesse_y

        # Vérifier les collisions avec le sol
        if self.rect.bottom >= HAUTEUR_ECRAN - SOL_HAUTEUR:  # Collision avec le sol
            self.rect.bottom = HAUTEUR_ECRAN - SOL_HAUTEUR
            self.vitesse_y = 0
            self.a_sauté = False  # Réinitialiser la variable de saut

    def sauter(self):
        if not self.a_sauté:  # Vérifier si le joueur peut sauter
            self.vitesse_y = self.force_saut  # Définir la vitesse de saut
            self.a_sauté = True  # Mettre à jour l'état du saut

# Initialiser l'écran
ecran = pygame.display.set_mode((LARGEUR_ECRAN, HAUTEUR_ECRAN))
pygame.display.set_caption("Jeu de Plateforme")

# Charger l'image de fond
image_fond_original = pygame.image.load("c:/Users/lpayen/Desktop/IA/Projet pygame/image/istockphoto-1372132668-612x612.jpg").convert()
# Agrandir l'image de fond pour qu'elle couvre une zone plus grande que l'écran
largeur_fond = image_fond_original.get_width() * 2
hauteur_fond = image_fond_original.get_height() * 2
image_fond = pygame.transform.scale(image_fond_original, (largeur_fond, hauteur_fond))

# Créer un joueur
joueur = Joueur()

# Groupe de sprites contenant le joueur
tous_les_sprites = pygame.sprite.Group()
tous_les_sprites.add(joueur)  # Ajouter le joueur au groupe de sprites

# Drapeaux pour les touches enfoncées
gauche_pressee = False
droite_pressee = False

# Position de défilement de la caméra
camera_x = 0
camera_y = 0

# Boucle de jeu
continuer = True
while continuer:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            continuer = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                joueur.sauter()
            elif event.key == pygame.K_d:  # Détection de la touche D enfoncée
                droite_pressee = True
            elif event.key == pygame.K_q:  # Détection de la touche Q enfoncée
                gauche_pressee = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_d:  # Détection de la touche D relâchée
                droite_pressee = False
            elif event.key == pygame.K_q:  # Détection de la touche Q relâchée
                gauche_pressee = False

    # Déplacement du joueur
    if droite_pressee:
        joueur.rect.x += 5
    if gauche_pressee:
        joueur.rect.x -= 5

    # Mettre à jour le joueur
    joueur.update()

    # Mettre à jour la position de la caméra pour suivre le joueur
    camera_x = joueur.rect.x - int(LARGEUR_ECRAN * (1 - CAMERA_PROXIMITE) // 2)
    camera_y = joueur.rect.y - int(HAUTEUR_ECRAN * (1 - CAMERA_PROXIMITE) // 2)

    # Dessiner l'écran avec le décalage de la caméra
    ecran.blit(image_fond, (-camera_x, -camera_y))  # Afficher l'image de fond
    pygame.draw.rect(ecran, SOL_COULEUR, (0, HAUTEUR_ECRAN - SOL_HAUTEUR, LARGEUR_ECRAN, SOL_HAUTEUR))  # Dessiner le sol
    for sprite in tous_les_sprites:
        ecran.blit(sprite.image, (sprite.rect.x - camera_x, sprite.rect.y - camera_y))

    # Rafraîchir l'écran
    pygame.display.flip()

    # Limiter le nombre de trames par seconde
    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()
