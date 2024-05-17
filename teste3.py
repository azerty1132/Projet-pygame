import pygame
import sys

# Initialisation de Pygame
pygame.init()

# Constantes pour les couleurs et les dimensions de l'écran
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
LARGEUR_ECRAN = 800
HAUTEUR_ECRAN = 600

# Classe pour les plateformes
class Plateforme(pygame.sprite.Sprite):
    def __init__(self, x, y, largeur, hauteur):
        super().__init__()
        self.image = pygame.Surface((largeur, hauteur))
        self.image.fill((0, 255, 0))  # Couleur verte pour les plateformes
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

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

    def update(self, plateformes):
        # Appliquer la gravité
        self.vitesse_y += self.gravite  # Ajouter la gravité à la vitesse verticale
        self.rect.y += self.vitesse_y

        # Vérifier les collisions avec les plateformes
        collisions = pygame.sprite.spritecollide(self, plateformes, False)
        for plateforme in collisions:
            if self.vitesse_y > 0:
                self.rect.bottom = plateforme.rect.top
                self.vitesse_y = 0
                self.a_sauté = False  # Réinitialiser la variable de saut

        # Vérifier les collisions avec le sol
        if self.rect.bottom >= HAUTEUR_ECRAN:
            self.rect.bottom = HAUTEUR_ECRAN
            self.vitesse_y = 0
            self.a_sauté = False  # Réinitialiser la variable de saut

    def sauter(self):
        if not self.a_sauté:  # Vérifier si le joueur peut sauter
            self.vitesse_y = self.force_saut  # Définir la vitesse de saut
            self.gravite *= -1  # Inverser la gravité lors du saut
            self.a_sauté = True  # Mettre à jour l'état du saut

# Initialiser l'écran
ecran = pygame.display.set_mode((LARGEUR_ECRAN, HAUTEUR_ECRAN))
pygame.display.set_caption("Jeu de Plateforme")

# Créer les plateformes
plateforme = Plateforme(500, 400, 100, 25)
plateforme2 = Plateforme(300, 200, 100, 25)
plateforme3 = Plateforme(200, 300, 150, 25)  # Nouvelle plateforme
plateforme4 = Plateforme(600, 100, 200, 25)  # Nouvelle plateforme

# Créer un joueur
joueur = Joueur()

# Groupe de sprites contenant le joueur et les plateformes
tous_les_sprites = pygame.sprite.Group()
tous_les_sprites.add(joueur, plateforme, plateforme2, plateforme3, plateforme4)  # Ajoute les plateformes au groupe de sprites

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

    # Mettre à jour le joueur avec les collisions des plateformes
    joueur.update(tous_les_sprites)

    # Mettre à jour la position de la caméra pour suivre le joueur
    camera_x = joueur.rect.x - LARGEUR_ECRAN // 2
    camera_y = joueur.rect.y - HAUTEUR_ECRAN
