import pygame
import random
from pygame.locals import *
from sys import exit
pygame.init()

win = pygame.display.set_mode((500,500))
pygame.display.set_caption("First Game")
images = ["0.png","1.png","2.png","3.png","4.png","5.png","6.png","7.png","8.png","9.png"]
# 
x = 250
y = 450
width = 40
height = 60
vel = 5


enemy_x = 250
enemy_y = 0
enemy_width = 60 
enemy_height =40
run = True
class Enemy:
  def __init__(self, image, value):
    self.image = str(image) + '.png'
    self.value = value

equation = []

val1 = random.randint(0,len(images)-1)
val2 = random.randint(0,len(images)-1)
val3 = random.randint(0,len(images)-1)
em1 = Enemy(val1,val1)
em2 = Enemy(val2,val2)
em3 = Enemy(val3,val3)

image_filename = em1.image
img = pygame.image.load(image_filename)
      

i=0
while run:
    
    pygame.time.delay(100)
      
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        x -= vel

    if keys[pygame.K_RIGHT]:
        x += vel

    if keys[pygame.K_UP]:
        y -= vel

    if keys[pygame.K_DOWN]:
        y += vel
        
    enemy_y += vel
    
    win.fill((255,255,255))  # Fills the screen with black
    pygame.draw.rect(win, (255,0,0), (x, y, width, height))   
    win.blit(img, (enemy_x, enemy_y))
    pygame.display.update() 
    if(enemy_y == 500):
      val1 = random.randint(0,len(images)-1)
      val2 = random.randint(0,len(images)-1)
      val3 = random.randint(0,len(images)-1)
      em1 = Enemy(val1,val1)
      em2 = Enemy(val2,val2)
      em3 = Enemy(val3,val3)
      enemy_x = random.randint(0,500)
      enemy_y = 0
      # print("rand is: " + str(random.randint(0,len(images)-1)))
      image_filename = em1.image
      img = pygame.image.load(image_filename)
    if(enemy_x < x +50 and enemy_x > x - 50 and enemy_y < y + 50 and enemy_y > y - 50):
      equation.append(em1.value)
      val1 = random.randint(0,len(images)-1)
      val2 = random.randint(0,len(images)-1)
      val3 = random.randint(0,len(images)-1)
      em1 = Enemy(val1,val1)
      em2 = Enemy(val2,val2)
      em3 = Enemy(val3,val3)
      i+=1
      print(i)
      
      enemy_x = random.randint(0,500)
      enemy_y = 0
      # print("rand is: " + str(random.randint(0,len(images)-1)))
      image_filename = em1.image
      img = pygame.image.load(image_filename)
      print(equation)
pygame.quit()

