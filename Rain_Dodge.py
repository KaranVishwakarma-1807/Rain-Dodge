#initializing the pygame module
import pygame
import time
import random
pygame.font.init() #initializing the font module
import os


#creating the window(in pixels)
WIDTH, HEIGHT = 1000, 800 
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
#caption for the widown(name for the window)
pygame.display.set_caption("Rain Dodge")


#creating the background
BG = pygame.image.load(os.path.join("./Resource","bg.jpeg")) #define the path of the resource
#to scale the image
BG = pygame.transform.scale(BG, (WIDTH, HEIGHT))


#creating the font obeject
FONT = pygame.font.SysFont("comicsans", 30)


#creating a function to load the bg into the window
def draw(player, elapsed_time, drops):
    WIN.blit(BG, (0,0)) #blit = used to draw images on the screen

    #drawing the time on the screen
    text_time = FONT.render(f"Time: {round(elapsed_time)}s", 1, "black")
    WIN.blit(text_time, (10, 10))

    pygame.draw.rect(WIN, "red", player ) #drawing the player

    #drawing the projectiles on the screen
    for drop in drops:
        pygame.draw.rect(WIN, "dark blue", drop)

    pygame.display.update() #this will update the display


#defining a character
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60
PLAYER_VEL = 5


#defining the projectile
DROP_WIDTH = 10
DROP_HEIGHT = 20
DROP_VEL = 3

#creating a main function where the game logics will be defined
def main():
    run = True 

    #initializing the player
    player =  pygame.Rect(200, HEIGHT-PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT) #React = rectangle

    #creating  a clock to control the frame rate
    clock = pygame.time.Clock()

    #keeping track of time
    start_time = time.time() #gives the current time
    elapsed_time = 0 

    #generating the projectiles
    drop_add_increment = 2000  #time in milliseconds -> adds a new projectile in 2000 milsec
    drop_count = 0 #tells when we should add a new projectile 

    drops = []  #list to hold the projectiles

    hit = False

    #main game loop
    while run:

        clock.tick(60) #60 frames per second

        elapsed_time = time.time() - start_time  #give the remaining time since the start

        drop_count  += clock.tick(60) #increases the count by 1 each 60 frame
        #drop_count  += 1 #increases the count by 1 each frame

        if drop_count >  drop_add_increment: #if the count is greater than the increment
            for _ in range(3): #generates 3 random projectiles
                drop_x = random.randint(0, WIDTH - DROP_WIDTH) 
                drop = pygame.Rect(drop_x, -DROP_HEIGHT,  DROP_WIDTH, DROP_HEIGHT) #initializing the projectile
                drops.append(drop) #adds the projectile to the list

            drop_add_increment = max(200, drop_add_increment - 50)
            drop_count = 0

        for event in pygame.event.get(): #has the list of all kinds of events
            if event.type == pygame.QUIT: #checking if the user hit the cross botton
                run = False
                break

        #moving our character
        keys =  pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >=0: #adding player boundaries
            player.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + player.width <= WIDTH: #adding player boundaries
            player.x += PLAYER_VEL

        #moving the projectiles
        for drop in drops[:]:
            drop.y += DROP_VEL
            if  drop.y > HEIGHT: #if the projectile is out of the screen
                drops.remove(drop)
            elif drop.y  + DROP_HEIGHT >= player.y and drop.colliderect(player):
                drops.remove(drop)
                hit =  True 
                break

        #handling the losing the game
        if hit:
            lost_text = FONT.render("YOU LOST!", 1, "brown")
            WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(1000)
            break

        draw(player, elapsed_time, drops) #calling the draw function

    pygame.quit()  #Quits the game window


#run the main function
if __name__ == '__main__':
    main()
