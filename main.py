# Ping Pong Game Built using Pygame
# Developed By Ashish Shevale

import pygame
import random
from time import time as timer

################# FUNCTIONS FOR MODIFYING GAME WINDOW #################

def update_user_position():
    # draw the user paddle on the screen
    window.blit(  user, (user_x, user_y))

def update_computer_position():
    # draw the computer paddle on screen
    window.blit(  computer, (computer_x, computer_y))

def update_ball_position():
    # draw the ball_position of screen
    window.blit(  ball, ( ball_x, ball_y))

def get_computer_collision_point():
    # get the location at which ball will hit the computer paddle
    collision_x = (ball_y - ball_c) / ball_slope
    collision_slope = ball_slope
    collision_c = ball_c
    collision_y = ball_y
    # repeat the following 
    while True:
        # the the ball hits the computer paddle inside the screen,
        if collision_x >= 0 and collision_x <= window_width - ball_radius:
            break
        # if the ball hits the paddle on  right of screen
        if collision_x >= window_width - ball_radius:
            # store this point for calculating the new point after reflection
            collision_x = window_width - ball_radius
        # if ball hits paddle to left of screen,
        elif collision_x <= 0:
            # store this point for calculating new point after relfection
            collision_x = 0
        # calculate the y coordinate for current x coordinate of ball
        collision_y = collision_slope * collision_x + collision_c
        # calcualte new slope after reflection
        collision_slope = -1 / collision_slope
        # calculate new c based on ne slope and y
        collision_c = collision_y - collision_slope * collision_x
        # calculate new x at which the ball will hit paddle
        collision_x = ( collision_y - collision_c) / collision_slope
        
    # return the point at which the ball hits the computer paddle
    return collision_x

def check_collision_with_paddle():
    # check collision with user paddle
    # if ball lies within y range of paddle
    if ball_y + ball_radius >= user_y:
        # and also lies between x range of paddle
        if ball_x >= user_x and ball_x <= user_x + paddle_width:
            # calculate new values for slope and c
            new_slope = -1 / ball_slope
            new_c = ball_y - new_slope * ball_x            
            return new_slope, new_c, True
    # check collision for computer paddle
    # if ball lies in y range of paddle
    if ball_y <= computer_y + paddle_height:
        # and also lies in x range of paddle
        if ball_x + ball_radius >= computer_x or ball_x <= computer_x + paddle_width:
            # calculate new values for slope and c
            new_slope = -1 / ball_slope
            new_c = ball_y - new_slope * ball_x
            return new_slope, new_c, False
    # else return the original values of slope and c
    return ball_slope, ball_c, False
        
###################################################################

# initialize the pygame module
pygame.init()

# create the game window
window = pygame.display.set_mode( (0, 0), pygame.FULLSCREEN )
# set the title for game window
pygame.display.set_caption("Ping Pong")

# variables for storing width and height of window
window_height = window.get_height()
window_width = window.get_width()

# variables for storing width and height of paddle
paddle_height = window_height // 20
paddle_width = window_height // 3
# variable storing the speed with which te paddle moves
paddle_speed = 20

# create the user paddle
user = pygame.image.load("Resources/paddle.png")
user = pygame.transform.scale(user, (paddle_width, paddle_height))
user.convert()

# create variables for storing user paddle positions
user_y = window_height - paddle_height - 10
user_x = window_width // 2
# variable to store what direction the paddle is supossed to move
user_paddle_direction = 0 # 0 -> no movement, 1 -> move down, -1 -> move up

# create the computer paddle
computer = pygame.image.load("Resources/paddle.png")
computer = pygame.transform.scale(computer, (paddle_width, paddle_height))
computer.convert()

# create variables for storing computer paddle
computer_x = window_width // 2
computer_y = 10

# variable indicating whether ball will hit computer next
collision_x = window_width // 2
tolerance = 15

# variables for storing radius of ball
ball_radius = paddle_width // 5

# create the ball the paddle will hit
ball = pygame.image.load("Resources/ball.png")
ball = pygame.transform.scale(ball, ( ball_radius , ball_radius ) )
ball.convert()

# create variables for storing blall position
ball_x = random.randint( 2 * paddle_width , window_width - 2 * paddle_width )
ball_y = random.randint( paddle_height , window_height - paddle_height )
ball_change = 10
'''
for controling motion of ball, we use 3 parameters
    1. position of ball -> ball_x, ball_y
    2. slope of line of path -> ball_slope::value lies from 60 to -60(implies angle lies in -89-89)
    3. direction of ball -> ball_direction :: +1 positive x, -1 negative x

'''
ball_direction = 1
ball_slope = 1
ball_c = ball_y - ball_slope * ball_x

# create a font to display the final score in
font = pygame.font.SysFont(None, 200)
# start the timer for game
begin = timer()

# variable for controlling whether the game is running or quitted
running = True
# repeat the following while the game is running
while running:
    # fill the window with color the remove all objects rendered in it
    window.fill((255, 255, 255))
    # go through all user event and perform appropriate actions
    for event in pygame.event.get():
        # if quit button is pressed,
        if event == pygame.QUIT:
            # toggle variable running so we can exit the game loop
            running = False
        # if the user has pressed some button,
        elif event.type == pygame.KEYDOWN:
            # if the button pressed is the RIGHT arrow
            if event.key == pygame.K_RIGHT:
                # change the direction of paddle to RIGHT
                user_paddle_direction = 1
            # if the button pressed is LEFT arrow,
            elif event.key == pygame.K_LEFT:
                # change the direction o paddle to LEFT
                user_paddle_direction = -1
        # if the key has been released,
        elif event.type == pygame.KEYUP:
            # stop moving the paddle
            user_paddle_direction = 0
            
    # if the paddle is not within the width of the window, stop moving it
    if user_x <= 0 and user_paddle_direction == -1:
        user_paddle_direction = 0
    # if the paddle is not within the height of the window, stop moving it
    if user_x >= window_width - paddle_width and user_paddle_direction == 1:
        user_paddle_direction = 0
    
    # set the new paddle positions using the paddle direction variable
    user_x += user_paddle_direction * paddle_speed
    
    # set new position of ball
    ball_x += ball_direction * ball_change
    ball_y = ball_slope * ball_x + ball_c
    
    # if the ball has hit the vertical sides of window,
    if ball_x <= 0 or ball_x >= window_width - ball_radius:
        # calculate new values for slope, c and direction of ball
        ball_direction *= -1
        ball_slope = -1 / ball_slope
        ball_c = ball_y - ball_x * ball_slope
    # if the ball has hit the vertical sides of window,
    if  ball_y + ball_radius >= window_height or ball_y <= 0:
        # game is over
        break
        
    # update the position of user paddle
    update_user_position()

    # update the position of computer paddle
    update_computer_position()
    
    # update the position of ball
    update_ball_position()
    
    # check if the ball has hit the paddle
    ball_slope, ball_c, computer_turn = check_collision_with_paddle()
    # if it is the users turn to hit,
    if computer_turn == False:
        # calculate where the ball is expected to hit on computers side
        collision_x = get_computer_collision_point()
    # if computer paddle is to the left of where the ball will hit
    if computer_x <= window_width - paddle_width and computer_x <= collision_x:
        # start moving the computer paddle right
        computer_x += 11
    # if computer paddle is to the right of where the ball will hit
    elif computer_x >= 0 and computer_x + paddle_width >= collision_x:
        # start moving the computer paddle left
        computer_x -= 11
    
    # update the window
    pygame.display.update()

# in case the gae is over, calculate how much time the player played
time_taken = int( timer() - begin )
# render this as score on the window
score = font.render("Time " + str(time_taken) + "s!", True, (0, 0, 0) )
# variales to store the height and width of image of score
font_height = score.get_height()
font_width = score.get_width()

while True:
    # display the user position as it was when game got over
    update_user_position()
    # display the user position as it was when game got over
    update_computer_position()
    # display the user position as it was when game got over
    update_ball_position()
    # draw the score in the center of window
    window.blit(score, (window_width // 2 - font_width // 2, window_height // 2 - font_height // 2))
    # update the window
    pygame.display.update()
    
    # if there is any event, quit the loop and exit program
    if len(pygame.event.get()) != 0:
        break
