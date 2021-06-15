import pygame
import random
from asteroide import*
from game import *
from pygame.math import Vector2
from player import *
from projectile import *
from explosion import *

class Projectile_enemy(pygame.sprite.Sprite):
    def __init__(self,game, x, y, vel):
        super().__init__()
        self.velocity = 5
        self.game = game
        self.image = pygame.image.load('img/shoot/red_lazer.png')
        self.image = pygame.transform.scale(self.image, (60, 80))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.vel = Vector2(vel)
        self.attack = 8


    def launch_projectile_enemy(self):

        # le déplacement ne se fait que s'il n'y a pas de collision
        if not self.game.check_collision(self, self.game.all_players):
            self.rect.y += self.velocity
            # si le joueur est en collision avec le projectile
        else:
            # infliger des dégats ( au joeur)
            self.game.sound_manager.playsound('explosion')
            self.game.player.damage(self.attack)
            self.remove()

        # verifier si le projectile n'est plus sur l'ecran
        if self.rect.y >= 810:
            # suprimmer le projectile( en dehors de l'ecran)
            self.game.spaceship_event.all_projectiles.remove(self)

    def remove(self):
        self.game.spaceship_event.all_projectiles.remove(self)

# créer une classe pour gérer cette comet
class Spaceship(pygame.sprite.Sprite):
    def __init__(self, spaceship_event, game, projectiles):
        super().__init__()
        self.game = game
        # définir quelle est l'image associé
        self.image_load = pygame.image.load('img/spaceship/spaceship2-removebg-preview.png')
        self.image = pygame.transform.scale(self.image_load, (120, 120))
        self.rect = self.image.get_rect()
        self.velocity = random.randint(1, 4)
        self.rect.x = random.randint(-10, 500)
        self.rect.y = -80
        self.attack = 20
        self.spaceship_event = spaceship_event
        self.health = 100
        self.max_health = 100
        self.direction = random.randint(0, 1)
        # attribut pour lancer plusieurs projectile
        self.previous_time = pygame.time.get_ticks()
        self.shoot_delay = random.randint(1500, 5000) # milliseconds
        self.projectiles = projectiles
        self.limit = random.randint(50, 150 )


    def update_health_bar_comet(self, surface):
        # définir une couleur pour notre jauge de vie
        bar_color = (111, 210, 46)
        back_bar_color = (60,63,60)
        #définir la position de notre jauge de vie ainsi que sa largeur et son épaisseur
        bar_position = [self.rect.x , self.rect.y - 10, self.health, 5]
        # définir la position de l'arrière plan de la barre de vie
        back_bar_position = [self.rect.x, self.rect.y - 10, self.max_health, 5]

        #dessiner la barre de vie
        pygame.draw.rect(surface, back_bar_color, back_bar_position)
        pygame.draw.rect(surface, bar_color, bar_position)


    def remove(self):
        self.spaceship_event.all_spaceship.remove(self)
        # vérifier si le nombre de vaisseau est de zéro
        if len(self.spaceship_event.all_spaceship) == 0:
            # remettre la barre a 0
            self.spaceship_event.reset_percent()

            self.spaceship_event.game.spawn_asteroide(Big_Asteroide)
            self.spaceship_event.game.spawn_asteroide(Big_Asteroide)
            self.spaceship_event.game.spawn_asteroide(Med_Asteroide)
            self.spaceship_event.game.spawn_asteroide(Med_Asteroide)
            self.spaceship_event.game.spawn_asteroide(Small_Asteroide)


    def move_spaceship(self):
        if not self.rect.y >= self.limit:
            self.rect.y += self.velocity
        if self.direction == 1:
            self.rect.x += self.velocity
            if self.rect.x >= 650:
                self.direction = 0
        if self.direction == 0:
            self.rect.x -= self.velocity
            if self.rect.x <= -10:
                self.direction = 1

    def launch_projectile(self):

        now = pygame.time.get_ticks()
        if now - self.previous_time > self.shoot_delay:
            self.previous_time = now
            vel = Vector2(5, 0)
            # Add the projectile to the group.
            self.projectiles.add(Projectile_enemy(self.game, self.rect.x , self.rect.y + 16, vel))
            self.projectiles.add(Projectile_enemy(self.game, self.rect.x + 52, self.rect.y + 16, vel))


    def damage(self, amount):
        #  Infliger des dégats
        self.health -= amount

        #vérifier si son nombre de points de vie est inférieur ou égale à zéro
        if self.health <= 0:
            explosion = Explosion(self.rect.center, 'spaceship')
            self.game.all_explosions.add(explosion)
            # supprimer et réapparaitre les astéroides
            self.remove()

