import pygame
from pygame.locals import *
import math
from game import *
from pygame import mixer
'''Ce fichier est pour l'ensemble du code'''

'''sprites est une super classe qui permet à l'objet de se déplacer '''

#initialisation de la page du jeu
pygame.init()

# définir une clock
clock = pygame.time.Clock()
FPS = 160


# load music and play
toggle = False
mixer.music.load('music/music.mp3')
mixer.music.play(-1)
music_paused = False


# initialisations de la page
pygame.display.set_caption('shooter Game')
screen = pygame.display.set_mode((800, 800))

# import the background
background = pygame.image.load('img/backrgound/background.jpg')

# importer charger notre boutton play
play_button = pygame.image.load('img/Menu/banner_start.png')
play_button = pygame.transform.scale(play_button, (300, 300))
play_button_rect = play_button.get_rect()
play_button_rect.x = math.ceil(screen.get_width() / 3)
play_button_rect.y = math.ceil(screen.get_width() / 3)
# math.ceil permet de rendre un nombre virgule --> un nombre eniter


# importer et charger le boutton Sound
sound_button = pygame.image.load('img/Menu/sound.png')
sound_button = pygame.transform.scale(sound_button, (105, 59))
sound_button_rect = sound_button.get_rect()
sound_button_rect.x = 650
sound_button_rect.y = 100


# importer la bannière
banner = pygame.image.load('img/bannière/banner.png')
banner_rect = banner.get_rect()
banner_rect.x = math.ceil(screen.get_width() / 12)
banner_rect.y = math.ceil(screen.get_width() / 10)

# charge Game
game = Game()
#charge player
player = Player(game)

# charger la partie progression

running = True
game_over = False

# boucle tant que cette condition est vrai
while running:

    #generate the background
    screen.blit(background, (0,0))

    #vérifier si notre jeu a commencé ou non
    if game.is_playing is True:
        # declencher les instructions de la partie
        game.update(screen)
    # vérifier si notre jeu est fini ( game_over )
    elif game.is_game_over:
        # déclencher les instruction de la fin de partie
        game.screen_over(screen)
    # vérifier si notre jeu n'a pas commencé
    else:
        # ajouter mon ecran de bienvenue avec le bouton de réglages
        screen.blit(play_button, (play_button_rect.x, play_button_rect.y))
        screen.blit(banner, (banner_rect.x, banner_rect.y))
        screen.blit(sound_button, (sound_button_rect.x, sound_button_rect.y))


    # update the screen
    pygame.display.flip()

    for event in pygame.event.get():
        # exit game
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        # detect if player touches a key
        elif event.type == pygame.KEYDOWN:
            # permet que lorsqu'on appuie sur une touche il rentre dans un dictionnaire et
            # premet de vérifier si oui ou non elle est active
            game.pressed[event.key] = True

            #detecter si la touche espace est détecter pour lancer notre projectile
            if event.key == pygame.K_SPACE:
                # adding sound to the firing projectile
                bullet_sound = mixer.Sound('music/lazer.mp3')
                if game.is_playing:
                    game.player.launch_projectile()
                    if game.score == 1000:
                        game.game_over()
                elif game.is_game_over:
                    game.is_game_over = False
                    game.score = 0
                else:
                    pass


        elif event.type == pygame.KEYUP:
            game.pressed[event.key] = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            # vérifier si la souris est sur le boutton de lancement
            if play_button_rect.collidepoint(event.pos):
                if game.is_playing == False and game.is_game_over == False:
                    # démarer la partie
                    game.start()
                    game.sound_manager.playsound('click')

            elif sound_button_rect.collidepoint(event.pos):
                game.sound_manager.playsound('click')
                music_paused = not music_paused
                if music_paused:
                    mixer.music.pause()
                else:
                    mixer.music.play()




    # fixer le nombre de fps sur le jeu
    clock.tick(FPS)



