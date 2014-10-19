'''
By: Deon Hua
Date: 21 April 2013
Description: pyBreakOut! - A version of Atari's original "Breakout" video game
programmed using pyGame. Players can use the left/right arrow keys to move.
Aside from the standard requirements, this game also allows for a second player 
to play using the second (lower) paddle using the mouse's location. It also
scores different coloured blocks differently:
blue - 1 point
green - 2 points
orange - 3 points
yellow - 4 points
red - 5 points
violet - 6 points

Enjoy!
'''

#Import and Initialize
import pygame, pygame.mixer, myBreakOutSprites
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((640, 480))

def main(): 
    '''This function defines the 'mainline logic' for pyBreakOut.'''
    #Display
    pygame.display.set_caption("pyBreakOut!")
    
    #Entities
    background = pygame.Surface(screen.get_size())
    background.fill((255,255,255))
    screen.blit(background, (0,0))
    
    #Form fonts
    myFont = pygame.font.SysFont("arial", 60)
    winner = myFont.render("You Win!", 1, (0,0,0))
    loser = myFont.render("You Lose!", 1, (0,0,0))
    
    #Load Music
    music = pygame.mixer.music.load("music.ogg")
    impact = pygame.mixer.Sound("slap.ogg")
    impact.set_volume(0.4)
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)
    
    #Form lists for each colour of bricks
    violet_bricks = []
    red_bricks = []
    yellow_bricks = []
    orange_bricks = []
    green_bricks = []
    blue_bricks = []
    
    #For loop to create the brick sprites
    for x in range(0,18):
        violet_brick = myBreakOutSprites.Brick(5+35*x,100, (148,0,211))
        red_brick = myBreakOutSprites.Brick(5+35*x,110, (255,0,0))
        yellow_brick = myBreakOutSprites.Brick(5+35*x,120, (255,255,0))
        orange_brick = myBreakOutSprites.Brick(5+35*x,130, (255,165,0))
        green_brick = myBreakOutSprites.Brick(5+35*x,140, (0,255,0))
        blue_brick = myBreakOutSprites.Brick(5+35*x,150, (0,0,255))
        
        #Append the bricks created to its corresponding list.
        violet_bricks.append(violet_brick)
        red_bricks.append(red_brick)
        yellow_bricks.append(yellow_brick)
        orange_bricks.append(orange_brick)
        green_bricks.append(green_brick)
        blue_bricks.append(blue_brick)
        
    #Create groups of sprites for each colour of bricks, from the lists
    violetBrickSprites = pygame.sprite.Group(violet_bricks)
    redBrickSprites = pygame.sprite.Group(red_bricks)
    yellowBrickSprites = pygame.sprite.Group(yellow_bricks)
    orangeBrickSprites = pygame.sprite.Group(orange_bricks)
    greenBrickSprites = pygame.sprite.Group(green_bricks)
    blueBrickSprites = pygame.sprite.Group(blue_bricks)
    
    #Create brickSprites group for all the bricks.
    brickSprites = pygame.sprite.Group(violet_bricks, red_bricks, yellow_bricks\
                                     , orange_bricks, green_bricks, blue_bricks)
        
    #Form other sprites
    paddle = myBreakOutSprites.Paddle(screen, 300, 410)
    paddle2 = myBreakOutSprites.Paddle(screen, 300, 440)    
    ball = myBreakOutSprites.Ball(screen)
    score_keeper = myBreakOutSprites.ScoreKeeper()
    end_zone = myBreakOutSprites.EndZone(screen)
    
    #Form remaining sprite groups.
    paddleSprites = pygame.sprite.Group(paddle, paddle2)    
    
    allSprites = pygame.sprite.Group(paddle, paddle2, ball,score_keeper,end_zone \
                                     , violet_bricks, red_bricks, yellow_bricks\
                                     , orange_bricks, green_bricks, blue_bricks)    

    
    #ACTION
    
    #Assign         
    clock = pygame.time.Clock()
    keepGoing = True
    
    # Hide the mouse pointer
    pygame.mouse.set_visible(False)
    
    #Loop
    while keepGoing:
        
        #Time
        clock.tick(30)
        
        #Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
            #Allows for second use mouse input.
            if event.type == pygame.MOUSEMOTION:
                paddle2.move(pygame.mouse.get_pos())
                
        #Allows for the user to hold down the left/right arrowkeys to move paddle.       
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            paddle.move_left()
        elif keys[pygame.K_RIGHT]:
            paddle.move_right()
            
        #Collision Detection:
        
        #Check to see if ball hit the "endzone"
        if ball.rect.colliderect(end_zone.rect):
            ball.change_direction()
            score_keeper.life_lost()
            impact.play()
        
        #Check to see if ball hit either paddle.            
        if pygame.sprite.spritecollide(ball, paddleSprites, False):
            ball.change_direction()
            impact.play()
            
        #Check to see if ball hit a brick of a colour; rewards points accordingly.
        score_keeper.brick_destroyed(6*len(pygame.sprite.spritecollide(ball, violetBrickSprites, False)))
        score_keeper.brick_destroyed(5*len(pygame.sprite.spritecollide(ball, redBrickSprites, False)))
        score_keeper.brick_destroyed(4*len(pygame.sprite.spritecollide(ball, yellowBrickSprites, False)))
        score_keeper.brick_destroyed(3*len(pygame.sprite.spritecollide(ball, orangeBrickSprites, False)))
        score_keeper.brick_destroyed(2*len(pygame.sprite.spritecollide(ball, greenBrickSprites, False)))
        score_keeper.brick_destroyed(len(pygame.sprite.spritecollide(ball, blueBrickSprites, False)))
        
        #Removes the brick(s) from the screen
        if pygame.sprite.spritecollide(ball, brickSprites, True):
            ball.change_direction()
            impact.play()

        # Check for game over
        if score_keeper.result() == 1:
            keepGoing = False
            screen.blit(loser, (200,200))
        elif score_keeper.result() == 2:
            keepGoing = False
            screen.blit(winner, (200,200))
            
        #Refresh screen
        allSprites.clear(screen, background)
        allSprites.update()
        allSprites.draw(screen)
        pygame.display.flip()
         
    # Unhide mouse pointer
    pygame.mouse.set_visible(True)
    
    #Fade music and delay close.
    pygame.mixer.music.fadeout(3000)    
    pygame.time.delay(3000)    
 
    # Close the game window
    pygame.quit()   
     
# Call the main function
main()
