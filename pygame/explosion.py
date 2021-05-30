import pygame
image_anim = {}
image_anim['big'] = []
image_anim['med'] = []
image_anim['small'] = []
image_anim['spaceship'] = []

path = f"img/explosion/regularExplosion0"
for i in range(9):
    image_path = path + str(i) + '.png'
    image_main = pygame.image.load(image_path)
    # les images pour l'explosion du gros astéroide
    img_big = pygame.transform.scale(image_main, ( 180, 180))
    image_anim['big'].append(img_big)
    # les images pour l'explosion de l'astéroide medium
    img_med = pygame.transform.scale(image_main, (120, 120))
    image_anim['med'].append(img_med)
    # les images pour l'explosion de l'astéroide petit
    img_small = pygame.transform.scale(image_main, (70, 70))
    image_anim['small'].append(img_small)
    # les images pour l'explosion des vaisseaux
    img_spaceship = pygame.transform.scale(image_main, (160, 160))
    image_anim['spaceship'].append(img_spaceship)

# class qui s'occupe de l'animation explosion
class Explosion(pygame.sprite.Sprite):

    def __init__(self, center, name):
        super().__init__()
        self.current_image = 0
        self.name = name
        self.image = image_anim[self.name][self.current_image]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.last_update = pygame.time.get_ticks()
        self.picture_delay = 50




    # animation d'explosion
    def animate(self):


         now = pygame.time.get_ticks()
         if now - self.last_update > self.picture_delay:
             self.previous_time = now
             if now - self.last_update > self.current_image:
                 self.last_update = now
                 self.current_image += 1
                 if self.current_image == len(image_anim[self.name]):
                     self.kill()
                 else:
                     center = self.rect.center
                     self.image = image_anim[self.name][self.current_image]
                     self.rect = self.image.get_rect()
                     self.rect.center = center
        # passer à l'image suivante
        # self.current_image += 1
        #
        # # vérifier si on a atteint la fin de l'animation
        # if self.current_image >= 9:
        #     self.kill()
        #     # remettre l'animation au départ
        #     self.current_image = 0