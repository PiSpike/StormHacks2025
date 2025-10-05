import pygame
import random
from pygame.locals import *
from sys import exit
import os

pygame.init()
SCREEN_HEIGHT = 500
SCREEN_WIDTH = 500

IMAGE_FOLDER = "assets"

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
        return self.y > 500

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
print("BEFOR")
print(enemies)
print("AGGGGGGG")
i=0
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
            print("Caught:", enemy.value)

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
                run = False
                try:
                    result = Calc(expr)
                    print(result)
                    
                except Exception as e:
                    print("Error:", e)
                equation = []

            enemies[i] = get_new_enemy()

    pygame.display.update()
show_result = True
while show_result:
    pygame.time.Clock().tick(60)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            show_result = False

    win.fill((255, 255, 255))

    # Scalable box centered
    box_width = win.get_width() // 3
    box_height = win.get_height() // 4
    box_x = win.get_width() // 2 - box_width // 2
    box_y = win.get_height() // 2 - box_height // 2

    pygame.draw.rect(win, (0, 0, 0), (box_x - 2, box_y - 2, box_width + 4, box_height + 4))  # Border
    pygame.draw.rect(win, (255, 0, 0), (box_x, box_y, box_width, box_height))

    # Scalable text in center
    font_size = min(box_width, box_height) // 2
    result_font = pygame.font.SysFont("monospace", font_size)
    result_text = result_font.render(str(result), True, (255, 255, 255))
    result_rect = result_text.get_rect(center=(win.get_width() // 2, win.get_height() // 2))
    win.blit(result_text, result_rect)

    pygame.display.update()

pygame.quit()

