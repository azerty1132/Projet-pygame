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
        if not self.a_sauté or pygame.sprite.spritecollide(self, [plateforme], False):
            self.vitesse_y = -15  # Changer la vitesse vers le haut pour simuler le saut
            self.a_sauté = True  # Mettre à jour la variable de saut     
              
# Initialiser l'écran
ecran = pygame.display.set_mode((LARGEUR_ECRAN, HAUTEUR_ECRAN))
pygame.display.set_caption("Jeu de Plateforme")

# Créer une instance de plateforme
x_plateforme = 500  # Coordonnée x de la plateforme
y_plateforme = 400# Coordonnée y de la plateforme
largeur_plateforme = 100  # Largeur de la plateforme
hauteur_plateforme = 25  # Hauteur de la plateforme
plateforme = Plateforme(x_plateforme, y_plateforme, largeur_plateforme, hauteur_plateforme)

# Créer une instance de plateforme
x_plateforme2 = 300  # Coordonnée x de la plateforme
y_plateforme2 = 200# Coordonnée y de la plateforme
largeur_plateforme2 = 100  # Largeur de la plateforme
hauteur_plateforme2 = 25  # Hauteur de la plateforme
plateforme2 = Plateforme(x_plateforme2, y_plateforme2, largeur_plateforme2, hauteur_plateforme2)

# Ajouter la plateforme au groupe de tous les sprites

# Créer un joueur
joueur = Joueur()

# Groupe de sprites contenant le joueur et la plateforme
tous_les_sprites = pygame.sprite.Group()
tous_les_sprites.add(joueur, plateforme,plateforme2)  # Ajoute la plateforme au groupe de sprites

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
    
    # Vérifier la collision entre le joueur et la plateforme
    if pygame.sprite.collide_rect(joueur, plateforme):
        if joueur.rect.bottom <= plateforme.rect.centery:  # Vérifier si le joueur est au-dessus de la plateforme
            if joueur.vitesse_y >= 0 and pygame.key.get_pressed()[pygame.K_SPACE]:  # Vérifier si le joueur descend et appuie sur la touche de saut
                joueur.sauter()
            else:
                # Si une collision est détectée et que le joueur ne saute pas, placer le joueur sur la plateforme et arrêter sa chute
                joueur.rect.bottom = plateforme.rect.top  # Positionner le bas du joueur sur le haut de la plateforme
                joueur.vitesse_y = 0  # Arrêter la vitesse de chute du joueur
    if pygame.sprite.collide_rect(joueur, plateforme2):
    
     if joueur.rect.bottom <= plateforme2.rect.centery:  # Vérifier si le joueur est au-dessus de la deuxième plateforme
        if joueur.vitesse_y >= 0 and pygame.key.get_pressed()[pygame.K_SPACE]:  # Vérifier si le joueur descend et appuie sur la touche de saut
            joueur.sauter()
        else:
            # Si une collision est détectée et que le joueur ne saute pas, placer le joueur sur la deuxième plateforme et arrêter sa chute
            joueur.rect.bottom = plateforme2.rect.top  # Positionner le bas du joueur sur le haut de la deuxième plateforme
            joueur.vitesse_y = 0  # Arrêter la vitesse de chute du joueur

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
