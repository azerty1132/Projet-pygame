import pygame
import sys

# Initialisation de Pygame
pygame.init()

# Constantes pour les couleurs et les dimensions de l'écran
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
VERT = (0, 255, 0)
LARGEUR_ECRAN = 800
HAUTEUR_ECRAN = 600

# Classe pour les plateformes
class Plateforme(pygame.sprite.Sprite):
    def __init__(self, x, y, largeur, hauteur):
        super().__init__()
        self.image = pygame.Surface((largeur, hauteur))
        self.image.fill(VERT)  # Couleur verte pour les plateformes
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Classe pour le joueur
class Joueur(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(BLANC)
        self.rect = self.image.get_rect()
        self.rect.center = (LARGEUR_ECRAN // 2, HAUTEUR_ECRAN // 2)
        self.vitesse_y = 0
        self.a_sauté = False  # Variable pour suivre si le joueur a déjà sauté

    def update(self):
        # Appliquer la gravité
        self.vitesse_y += 0.5
        self.rect.y += self.vitesse_y

        # Vérifier les collisions avec le sol
        if self.rect.bottom >= HAUTEUR_ECRAN:
            self.rect.bottom = HAUTEUR_ECRAN
            self.vitesse_y = 0
            self.a_sauté = False  # Réinitialiser la variable de saut

    def sauter(self):
        if not self.a_sauté:
            self.vitesse_y = -15  # Changer la vitesse vers le haut pour simuler le saut
            self.a_sauté = True  # Mettre à jour la variable de saut

# Initialiser l'écran
ecran = pygame.display.set_mode((LARGEUR_ECRAN, HAUTEUR_ECRAN))
pygame.display.set_caption("Jeu de Plateforme")

# Créer des instances de plateformes
plateformes = [
    Plateforme(500, 400, 100, 25),
    Plateforme(300, 200, 100, 25)
]

# Créer un joueur
joueur = Joueur()

# Groupe de sprites contenant le joueur et les plateformes
tous_les_sprites = pygame.sprite.Group()
tous_les_sprites.add(joueur)
for plateforme in plateformes:
    tous_les_sprites.add(plateforme)

# Drapeaux pour les touches enfoncées
gauche_pressee = False
droite_pressee = False

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

    # Vérifier les collisions avec les plateformes
    joueur.au_sol = False
    for plateforme in plateformes:
        if pygame.sprite.collide_rect(joueur, plateforme):
            if joueur.rect.bottom <= plateforme.rect.top and joueur.vitesse_y >= 0:
                joueur.rect.bottom = plateforme.rect.top
                joueur.vitesse_y = 0
                joueur.a_sauté = False

    # Mettre à jour le joueur
    tous_les_sprites.update()

    # Dessiner l'écran
    ecran.fill(NOIR)
    tous_les_sprites.draw(ecran)

    # Rafraîchir l'écran
    pygame.display.flip()

    # Limiter le nombre de trames par seconde
    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()
