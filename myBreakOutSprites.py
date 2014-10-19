'''
By: Deon Hua
Date: 21 April 2013
Description: This module contains the Brick, Ball, Paddle, EndZone, and 
ScoreKeeper sprites for Break-Out.
'''
import pygame

class Brick (pygame.sprite.Sprite):
    '''This defines the sprite for the bricks in our Break-Out game.'''
    def __init__(self, left_rect, top_rect, colour):
        ''' This initializer takes the top and left rects; initializes them, and
        takes the colour to set the colour of the brick.'''
        pygame.sprite.Sprite.__init__(self)
        
        #Image Attributes
        self.image = pygame.Surface((34,10))
        self.image = self.image.convert()
        self.image.fill(colour)
        
        #Set the rect attribute
        self.rect = self.image.get_rect()
        self.rect.left = left_rect
        self.rect.top = top_rect
      
class Ball(pygame.sprite.Sprite):
    '''This class defines the sprite for our Ball.'''
    def __init__(self, screen):
        '''This initializer takes a screen surface as a parameter, initializes
        the image and rect attributes, and x,y direction of the ball.'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
 
        # Set the image and rect attributes for the Ball
        self.image = pygame.image.load("ball.png")
        
        self.rect = self.image.get_rect()
        self.rect.center = (screen.get_width()/2, screen.get_height()/2)
 
        # Instance variables to keep track of the screen surface
        # and set the initial x and y vector for the ball.
        self.__screen = screen
        self.__dx = 5
        self.__dy = -2
 
    def change_direction(self):
        '''This method causes the y direction of the ball to reverse.'''
        self.__dy = -self.__dy
        
    def update(self):
        '''This method will be called automatically to reposition the
        ball sprite on the screen.'''
        # Check if we have reached the left or right end of the screen.
        # If not, then keep moving the ball in the same x direction.
        if ((self.rect.left > 0) and (self.__dx < 0)) or\
           ((self.rect.right < self.__screen.get_width()) and (self.__dx > 0)):
            self.rect.left += self.__dx
        # If yes, then reverse the x direction. 
        else:
            self.__dx = -self.__dx
             
        # Check if we have reached the top or bottom of the court.
        # If not, then keep moving the ball in the same y direction.
        if ((self.rect.top-40 > 0) and (self.__dy > 0)) or\
           ((self.rect.bottom < self.__screen.get_height()) and (self.__dy < 0)):
            self.rect.top -= self.__dy
        # If yes, then reverse the y direction. 
        else:
            self.__dy = -self.__dy
            
class Paddle (pygame.sprite.Sprite):
    '''This class defines the sprite for our paddles.'''
    def __init__(self, screen, left_rect, top_rect):
        '''This initializer assigns the image and rect attributes for our paddle
        sprite. It takes three parameters. Screen, a value for the left rect, and
        a value for the top rect.'''
        
        pygame.sprite.Sprite.__init__(self) 
        self.__screen = screen
        
        #Image Attributes
        self.image = pygame.Surface((70,10))
        self.image = self.image.convert()
        self.image.fill((255,100,100)) 
        
        #Set the rect attribute
        self.rect = self.image.get_rect()
        self.rect.top = top_rect
        self.rect.left = left_rect
        
    def move(self, coordinate):
        '''This method moves the paddle to a location depending on the x-coordinate
        of the mouse. It takes the x-coordinate of the tuple passed in.'''
        if coordinate[0] != 0 and coordinate[0] < self.__screen.get_width()-70:
            self.rect.left = coordinate[0]
                 
    def move_left(self):
        '''This method moves the rect of the paddle left (for keyboard input)
        as long as it's not at the left border of the screen, so that it can't
        go off.'''
        if self.rect.left != 0:
            self.rect.left -= 5
            
    def move_right(self):
        '''This method moves the rect of the paddle right (for keyboard input)
        as long as it's not at the right border of the screen, so that it can't
        go off.'''
        if self.rect.right != self.__screen.get_width():
            self.rect.left += 5
          
        
class EndZone (pygame.sprite.Sprite):
    '''This class defines the sprite for our "End Zone" at the bottom of the screen.'''
    def __init__(self, screen):
        '''This initalizer assigns the rect and image attributes to our "End Zone"
        which will always reside near the bottom of our screen (1 pixel above).
        It takes one parameter, screen.'''
        pygame.sprite.Sprite.__init__(self) 
        self.screen = screen
        
        #Image Attributes
        self.image = pygame.Surface((self.screen.get_width(), 1))
        self.image = self.image.convert()
        self.image.fill((255,255,255))
        
        #Set rect
        self.rect = self.image.get_rect()
        self.rect.top = 479

        
class ScoreKeeper (pygame.sprite.Sprite):
    '''This class defines the sprite for the Score Keeper located at the top.'''
    def __init__(self):
        '''This initializer loads the system font "Arial", and
        sets the starting lives to 3'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
 
        # Load our font, and initialize the starting score.
        self.__font = pygame.font.SysFont("Arial",30)
        self.__lives = 3
        self.__score = 0
        
    def life_lost(self):
        '''This method lowers the amount of lives the player has by 1.'''
        self.__lives -= 1
        
    def brick_destroyed (self, number): 
        '''This method adds points to the player's score given a parameter (number).'''
        self.__score += number
        
    def result(self):
        '''This method returns a 1 if the player has lost (no lives left) and a 2
        if the player has won (reached score of 378). Else, it returns a 0.'''
        if self.__lives == 0:
            return 1
        elif self.__score == 378:
            return 2
        else:
            return 0
        
    def update(self):
        '''This method will be called automatically to display 
        the current score at the top of the game window.'''
        message = "Score: %d   Lives: %d" %\
                (self.__score, self.__lives)
        self.image = self.__font.render(message, 1, (0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (320, 15)
        
        
        