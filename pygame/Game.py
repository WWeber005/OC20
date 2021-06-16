
import pygame
import math
from player import *
from asteroide import *
from Bossfight import *
from soundmanager import *
from projectile import *

WIDTH, HEIGHT = 800, 800
# create class Game
class Game:
    def __init__(self):
        # define if the game begun or not
        self.is_playing = False
        # generate player
        self.all_players = pygame.sprite.Group()
        self.player = Player(self)
        self.all_players.add(self.player)
        # générer l'evenemt de pluie de comet
        self.spaceship_event = Bossfight(self)
        # définir un groupe d'astéroide
        self.all_asteroides = pygame.sprite.Group()
        # sound
        self.sound_manager = Soundmanager()
        # Establishing font for labels for counters
        self.main_font = pygame.font.Font('fonts/main_font.ttf', 50)
        # score
        self.score = 0
        # créer un attribut qui va enregistrer toute les touche active
        self.pressed = {}
        self.all_explosions = pygame.sprite.Group()
        # define is the game is over or not
        self.is_game_over = False




    def addscore(self, points):
        self.score += points

    def start(self):
        self.is_playing = True
        self.spawn_asteroide(Med_Asteroide)
        self.spawn_asteroide(Med_Asteroide)
        self.spawn_asteroide(Big_Asteroide)
        self.spawn_asteroide((Small_Asteroide))
        self.spawn_asteroide((Small_Asteroide))
        self.spawn_asteroide((Small_Asteroide))


    def game_over(self):
        # remettre le jeu à neuf, retirer les monstre, remettre le joueur a 100 de vie, jeu en attente
        self.all_asteroides = pygame.sprite.Group()
        self.spaceship_event.all_spaceship = pygame.sprite.Group()
        self.player.health = self.player.max_health
        self.spaceship_event.reset_percent()
        # default position
        self.player.rect.x = 250
        self.player.rect.y = 500
        self.is_playing = False
        self.is_game_over = True

    def screen_over(self, screen):
        # bannière game over
        banner_over = pygame.image.load('img/game_over/game_over.png')
        banner_rect = banner_over.get_rect()
        banner_rect.x = math.ceil(screen.get_width() / 5)
        banner_rect.y = math.ceil(screen.get_width() / 9)
        screen.blit(banner_over, (banner_rect.x, banner_rect.y))
        # bannière key escape
        image_escape = pygame.image.load('img/game_over/key.png')
        escape_rect = image_escape.get_rect()
        escape_rect.x = math.ceil(screen.get_width() / 3.3)
        escape_rect.y = math.ceil(screen.get_width() / 2)
        screen.blit(image_escape, (escape_rect.x, escape_rect.y))
        # lives_label = main_font.render(f"Lives: {lives}", 1, (255, 255, 255))
        score_label = self.main_font.render(f"Score: {self.score}", 1, (255, 255, 255))

        # drawing variables
        # screen.blit(lives_label, (10, 10))
        screen.blit(score_label, (WIDTH - score_label.get_width() - 10, 10))




    def update(self, screen):

        # lives_label = main_font.render(f"Lives: {lives}", 1, (255, 255, 255))
        score_label = self.main_font.render(f"Score: {self.score}", 1, (255, 255, 255))

        # drawing variables
        # screen.blit(lives_label, (10, 10))
        screen.blit(score_label, (WIDTH - score_label.get_width() - 10, 10))

        # generate the players'image
        screen.blit(self.player.image, self.player.rect)

        # appliquer l'ensemble des images de mon groupes de projectiles
        self.player.all_projectiles.draw(screen)
        # actualiser la barre de bie du joueur
        self.player.update_health_bar(screen)

        # actualiser la barre d'evenemt du jeu
        self.spaceship_event.update_bar(screen)

        # appliquer l'ensemble desy images de mon groupe de vaisseaux
        self.spaceship_event.all_spaceship.draw(screen)

        # appliquer l'ensemble des images de mon groupes de projectiles enemis
        self.spaceship_event.all_projectiles.draw(screen)


        # récupérer les projectiles du joeur
        for projectile in self.player.all_projectiles:
            projectile.move()

        # récupérer les vaisseaux de notre jeu
        for spacehip in self.spaceship_event.all_spaceship:
            spacehip.update_health_bar_comet(screen)
            spacehip.move_spaceship()
            spacehip.launch_projectile()
        # récupérer les projectiles ennemis
        for projectile_ennemy in self.spaceship_event.all_projectiles:
            projectile_ennemy.launch_projectile_enemy()


        # appliquer l'ensemble des images de mon groupe de monstre
        self.all_asteroides.draw(screen)

        # récupérer les monstres de notre jeu
        for asteroide in self.all_asteroides:
            asteroide.forward()
            asteroide.update_health_bar(screen)


        for explosion in self.all_explosions:
            explosion.animate()

        # appliquer l'ensemble des images de mon groupes d'explosion
        self.all_explosions.draw(screen)



        # verifie si le joueur souhaite tourner à gauche, à droite, devant, ou en arrière et aussi vérifie s'il ne dépace
        # pas lécran !!
        if self.pressed.get(pygame.K_d) and self.player.rect.x + self.player.rect.width < screen.get_width():
            self.player.move_right()
        elif self.pressed.get(pygame.K_a) and self.player.rect.x > -18:
            self.player.move_left()
        elif self.pressed.get(pygame.K_s) and self.player.rect.y < 624:
            self.player.move_back()
        elif self.pressed.get(pygame.K_w) and self.player.rect.y > 0:
            self.player.move_forward()



    def check_collision(self, sprite, group):
        return pygame.sprite.spritecollide(sprite, group, False, pygame.sprite.collide_mask) # on peut remplacer la valeur False par dockil qui est que le joueur meut s'il touvhe le monstre

    def spawn_asteroide(self, asteroide_class_name):
        self.all_asteroides.add(asteroide_class_name.__call__(self)) # call permet d'instensier l'objet
