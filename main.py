import pygame
import random
from pygame.locals import *
from sys import exit
import os

pygame.init()

SCREEN_HEIGHT = 500
SCREEN_WIDTH = 500

IMAGE_FOLDER = "assets"

win = pygame.display.set_mode((SCREEN_HEIGHT,SCREEN_WIDTH), pygame.RESIZABLE)

# plays background music on loop
pygame.mixer.init()
pygame.mixer.music.load("assets/background.mp3") 
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1,0.0)

pygame.display.set_caption("First Game")

images = ["0.png","1.png","2.png","3.png","4.png","5.png","6.png","7.png","8.png","9.png","plus.png","minus.png","multiply.png","divide.png", "equal.png"]
random.shuffle(images)
player_x = win.get_width()/2
player_y = win.get_height() - 50
width = 55
height = 60
vel = 5
run = True
equation = []
divided_by_zero = False

# takes an expression that contains addition subraction, multiplication or division
# and returns the solution with 2 decimal points
def Calc(string):
    equation = string
    nums = []
    ops = []
    prev = 0
    
    # Seperate the numbers and operations into different arrays
    for i in range(len(equation)):
        if (equation[i].isnumeric()) == False:
            nums.append(equation[prev:i])
            ops.append(equation[i])
            prev = i+1

    # Calculate the multiplication and division first then the addition and subtraction
    while "*" in ops or "/" in ops:
        for i in range(len(ops)):
            if ops[i] == '*':
                nums[i] = float(nums[i]) * float(nums[i+1])
                ops.pop(i)
                nums.pop(i+1)
                break
            if ops[i] == '/':
                nums[i] = float(nums[i]) / float(nums[i+1])
                ops.pop(i)
                nums.pop(i+1)
                break

    while "+" in ops or "-" in ops:
        for i in range(len(ops)):
            if ops[i] == '+':
                nums[i] = float(nums[i]) + float(nums[i+1])
                ops.pop(i)
                nums.pop(i+1)
                break
            if ops[i] == '-':
                nums[i] = float(nums[i]) - float(nums[i+1])
                ops.pop(i)
                nums.pop(i+1)
                break

    return round(float(nums[0]),2)

# Creates the welcome screen
def show_welcome_screen():
    showing = True
    while showing:
        pygame.time.Clock().tick(60)
        win.fill((255, 255, 255))

        # Title
        title_font = pygame.font.SysFont("monospace", 40)
        title_text = title_font.render("A Simple Calculator", True, (0, 0, 0))
        title_rect = title_text.get_rect(center=(win.get_width() // 2, win.get_height() // 3))
        win.blit(title_text, title_rect)

        # Begin button
        button_font = pygame.font.SysFont("monospace", 34)
        button_text = button_font.render("Begin", True, (255, 255, 255))
        button_width, button_height = 150, 50
        button_x = win.get_width() // 2 - button_width // 2
        button_y = win.get_height() // 2
        button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

        pygame.draw.rect(win, (0, 150, 0), button_rect)
        win.blit(button_text, button_text.get_rect(center=button_rect.center))

        # Exits the welcome screen if the button is pressed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    showing = False  

        pygame.display.update()


# pygame.display
class Number:
    def __init__(self, image_name):

        image_path = os.path.join(IMAGE_FOLDER, image_name)
        self.image = pygame.image.load(image_path)
        # Randomly spreads the falling numbers and operations from the top
        self.x = random.randint(32, win.get_width() - 32)
        self.y = 0
        # Adds different falling speeds
        self.speed = vel + (random.randint(-2,2))
        
        if str(image_name[0]).isnumeric():
            self.value = image_name.strip(".png")
        else:       
            if image_name == 'minus.png':
                self.value = '-'
            elif image_name == 'plus.png':
                self.value = '+'
            elif image_name == 'multiply.png':
                self.value = '*'
            elif image_name == 'divide.png':
                self.value = '/'  
            elif image_name == 'equal.png':
                self.value = '='   

    def move(self):
            self.y += self.speed 

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))

    def off_screen(self):
        return self.y > win.get_height()

    def collide_with_player(self, player_x, player_y, player_w, player_h):
        return (self.x < player_x + player_w and
                self.x + 28 > player_x and
                self.y < player_y + player_h and
                self.y + 30 > player_y)
    
# Cycles through all the objects in the array so it's more even of a spead 
def create_new_object():
    if not images:
        images.extend(["0.png", "1.png", "2.png", "3.png", "4.png", "5.png", "6.png", "7.png", "8.png", "9.png",
                       "plus.png", "minus.png", "multiply.png", "divide.png", "equal.png"])
        random.shuffle(images)
    return Number(images.pop())

# Create 5 falling objects on screen at a time
object_arr = [create_new_object() for _ in range(5)]

show_welcome_screen()

while run:
    pygame.time.Clock().tick(60) 

    # Makes text bigger when on a smaller screen and smaller on a bigger screen
    myfont = pygame.font.SysFont("monospace", (round(64*500/win.get_width())))
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        player_x -= vel

    if keys[pygame.K_RIGHT]:
        player_x += vel

    # Keeps the player at the bottom of the screen when resizing the window 
    player_y = win.get_height() - 60

    win.fill((255,255,255))

    # Display the equation that's being formed on screen
    text = myfont.render(str(''.join(equation)), 1, (0,0,0))
    text_rect = text.get_rect(center=(win.get_width()/2, 50))
    win.blit(text,text_rect)

    player = pygame.image.load("assets/sadcalc.png") 
    win.blit(player,(player_x, player_y))

    # Moves the falling objects
    for i in range(len(object_arr)):
        object = object_arr[i]
        object.move()
        object.draw(win)

        if object.off_screen():
            object_arr[i] = create_new_object()

        if object.collide_with_player(player_x, player_y, width, height):
            pygame.mixer.Channel(0).play(pygame.mixer.Sound('assets/ding.mp3'), maxtime=600)
            # Doesn't let operators be the first thing in the equation
            if len(equation) == 0:
                if object.value.isnumeric():
                    equation.append(object.value)
            # If two operators are selected in a row, then the newest one replaces the previous one
            elif object.value.isnumeric() == False and str(equation[-1]).isnumeric() == False:
                equation[-1] = object.value  
            else: 
                equation.append(object.value)
                
            # Ends the calculation if the equal sign is choosen
            if object.value == "=" and len(equation) != 0:
                expr = ''.join(equation)  
                if len(equation) > 2 and equation[-3:-1] == ['/','0']:
                    pygame.mixer.Channel(2).play(pygame.mixer.Sound('assets/sadtrombone.mp3'), maxtime=10000)
                    divided_by_zero = True
                    run = False
                    continue
                try:
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound('assets/yay.mp3'), maxtime=2000)
                    result = Calc(expr)
                    # Randomly selects an overly complicated formula to display for the solution
                    expressions = [
                        [28, "assets/item0.png"],
                        [1, "assets/item1.png"],
                        [2, "assets/item2.png"],
                        [-1, "assets/item3.png"],
                        [3.5, "assets/item4.png"],
                        [5, "assets/item5.png"]]
                    exp = (random.choice(expressions))
                        
                    constant = result/exp[0]
                    # Transforms answer to int if it's a whole number
                    if result%exp[0] == 0:
                        constant = int(constant)
                    run = False
                except Exception as e:
                    print("Error:", e)
                equation = []

            object_arr[i] = create_new_object()
    
    pygame.display.update()



show_result = True

while show_result:
    pygame.time.Clock().tick(60)
    win.fill((255, 255, 255))

   

    font = pygame.font.SysFont("monospace", 32)
    if divided_by_zero:

        image_rect = pygame.Rect(win.get_width()/2-50, win.get_height()/2-50, 100, 100)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                show_result = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if image_rect.collidepoint(event.pos):
                    show_result = False

        disapoint = pygame.image.load("assets/disapointed.png")
        win.blit(disapoint, (win.get_width()/2-50, win.get_height()/2-50))
        
        
    else:
         # Exits game if Quit button is selected
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                show_result = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    show_result = False
        item_image = pygame.image.load(exp[1])
        # Render constant next to the formula image 
        font_side = pygame.font.Font('assets/cambria-math.ttf', 34)
        constant_text = font_side.render(f"{round(constant, 2)}", True, (0, 0, 0))

        elements = [constant_text, item_image]

        # Compute total width to center the image and constant
        total_width = constant_text.get_width() + item_image.get_width() + 30
        start_x = (win.get_width() - total_width) // 2
        y_center = win.get_height() // 2

        x = start_x
        for elem in elements:
            if isinstance(elem, pygame.Surface):
                rect = elem.get_rect()
                rect.topleft = (x, y_center - rect.height // 2 - 50)
                win.blit(elem, rect)
                x += rect.width

        # Define button properties
        button_font = pygame.font.SysFont("assets/cambria-math.ttf", 28)
        button_text = button_font.render("Exit", True, (255, 255, 255))
        button_width, button_height = 150, 50
        button_x = win.get_width() // 2 - button_width // 2
        button_y = win.get_height() // 2 + 50
        button_rect = pygame.Rect(button_x, button_y, button_width, button_height)


        # Draw the button 
        pygame.draw.rect(win, (200, 0, 0), button_rect) 
        text_rect = button_text.get_rect(center=button_rect.center)
        win.blit(button_text, text_rect)

    pygame.display.update()

pygame.quit()

