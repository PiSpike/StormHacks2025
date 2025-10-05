import pygame
import random
from pygame.locals import *
from sys import exit
import os

pygame.init()
SCREEN_HEIGHT = 500
SCREEN_WIDTH = 500

IMAGE_FOLDER = "assets"


pygame.mixer.init()
pygame.mixer.music.load("assets/background.mp3") 
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1,0.0)
def Calc(string):
    equation = string
    nums = []
    ops = []
    prev = 0
    for i in range(len(equation)):
        if (equation[i].isnumeric()) == False:
            nums.append(equation[prev:i])
            ops.append(equation[i])
            prev = i+1

    while "*" in ops or "/" in ops:
        for i in range(len(ops)):
            # print(len(ops))
            # print("i = " + str(i))

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
            # print(nums)
            # print(ops)

            
    while "+" in ops or "-" in ops:
        for i in range(len(ops)):
            # print(len(ops))
            # print("i = :" + str(i))

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
            # print(nums)
    return round(float(nums[0]),2)

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

        pygame.draw.rect(win, (0, 150, 0), button_rect)  # Green button
        win.blit(button_text, button_text.get_rect(center=button_rect.center))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    showing = False  # Exit the welcome screen

        pygame.display.update()

def spawn_enemy():

    if i >= len(images):
            random.shuffle(images)
            i = 0

win = pygame.display.set_mode((SCREEN_HEIGHT,SCREEN_WIDTH), pygame.RESIZABLE)
pygame.display.set_caption("First Game")
images = ["0.png","1.png","2.png","3.png","4.png","5.png","6.png","7.png","8.png","9.png","plus.png","minus.png","multiply.png","divide.png", "equal.png"]
random.shuffle(images)
player_x = win.get_width()/2
player_y = win.get_height() - 50
width = 40
height = 50
vel = 5


enemy_x = win.get_width()/2
enemy_y = 0
enemy_width = 32 
enemy_height = 32
run = True
class Enemy:
    def __init__(self, image_name):
        image_path = os.path.join(IMAGE_FOLDER, image_name)  # <- Here
        self.image = pygame.image.load(image_path)
        self.x = random.randint(32, win.get_width() - 32)
        self.y = 0
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
                self.x + 40 > player_x and
                self.y < player_y + player_h and
                self.y + 40 > player_y)
equation = []
def get_new_enemy():
    if not images:
        images.extend(["0.png", "1.png", "2.png", "3.png", "4.png", "5.png", "6.png", "7.png", "8.png", "9.png",
                       "plus.png", "minus.png", "multiply.png", "divide.png", "equal.png"])
        random.shuffle(images)
    return Enemy(images.pop())

enemies = [get_new_enemy() for _ in range(5)]

i=0
show_welcome_screen()
while run:
    myfont = pygame.font.SysFont("monospace", (round(64*500/win.get_width())))

# render text
    
    pygame.time.Clock().tick(60) 
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        player_x -= vel

    if keys[pygame.K_RIGHT]:
        player_x += vel

    # if keys[pygame.K_UP]:
    #     y -= vel

    # if keys[pygame.K_DOWN]:
    #     y += vel
        
    player_y = win.get_height() - 50


    
    win.fill((255,255,255))  # Fills the screen with black
    text = myfont.render(str(''.join(equation)), 1, (0,0,0))
    text_rect = text.get_rect(center=(win.get_width()/2, 50))
    win.blit(text,text_rect)
    pygame.draw.rect(win, (255,0,0), (player_x, player_y, width, height))   
    for i in range(len(enemies)):
        enemy = enemies[i]
        enemy.move()
        enemy.draw(win)

        # Off screen -> replace
        if enemy.off_screen():
            enemies[i] = get_new_enemy()

        # Collision
        if enemy.collide_with_player(player_x, player_y, width, height):
            pygame.mixer.Channel(0).play(pygame.mixer.Sound('assets/ding.mp3'), maxtime=600)
            if len(equation) == 0:
                if enemy.value.isnumeric():
                    equation.append(enemy.value)
            elif enemy.value.isnumeric() == False and str(equation[-1]).isnumeric() == False:
                equation[-1] = enemy.value  
            else: 
                equation.append(enemy.value)
                

            if enemy.value == "=" and len(equation) != 0:
                expr = ''.join(equation)  
                print("Evaluating:", expr)
                
                try:
                    result = Calc(expr)
                    print(result)
                    expressions = [
                        [28, "assets/item0.png"],
                        [1, "assets/item1.png"],
                        [2, "assets/item2.png"],
                        [-1, "assets/item3.png"],
                        [3.5, "assets/item4.png"],
                        [5, "assets/item5.png"]]
                    exp = (random.choice(expressions))
                        
                    constant = result/exp[0]
                    if result%exp[0] == 0:
                        constant = int(constant)
                    run = False
                except Exception as e:
                    print("Error:", e)
                equation = []

            enemies[i] = get_new_enemy()

    pygame.display.update()




# Load one item image and scale it
# Load item image at original size
item_image = pygame.image.load(exp[1])

show_result = True
while show_result:
    pygame.time.Clock().tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            show_result = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                show_result = False
    win.fill((255, 255, 255))

    # Fonts
    font = pygame.font.SysFont("monospace", 32)

    # Render text elements
    font_side = pygame.font.Font('assets/cambria-math.ttf', 34)
    constant_text = font_side.render(f"{round(constant, 2)}", True, (0, 0, 0))


    # Surfaces list: text and image
    elements = [constant_text, item_image]

    # Compute total width
    total_width = constant_text.get_width() + item_image.get_width() + 30
    start_x = (win.get_width() - total_width) // 2
    y_center = win.get_height() // 2

    # Blit all elements, keeping vertical center aligned
    x = start_x
    for elem in elements:
        if isinstance(elem, pygame.Surface):
            rect = elem.get_rect()
            rect.topleft = (x, y_center - rect.height // 2 - 50)
            win.blit(elem, rect)
            x += rect.width   # spacing between elements
    # Define button properties
    button_font = pygame.font.SysFont("assets/cambria-math.ttf", 28)
    button_text = button_font.render("Exit", True, (255, 255, 255))
    button_width, button_height = 150, 50
    button_x = win.get_width() // 2 - button_width // 2
    button_y = win.get_height() // 2 + 50
    button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

    # Inside your show_result loop, after filling screen and before pygame.display.update():

    # Draw the button rectangle
    pygame.draw.rect(win, (200, 0, 0), button_rect)  # Red button background

    # Draw the button text centered inside the button
    text_rect = button_text.get_rect(center=button_rect.center)
    win.blit(button_text, text_rect)
    pygame.display.update()

pygame.quit()

