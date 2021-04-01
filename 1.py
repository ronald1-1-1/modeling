import pygame as pg
import math

dic = {}
with open('config.txt','r') as f:
    for i in f.readlines():
        inp = i.replace(' ','').replace('\n','').split('=')
        dic[inp[0]] = int(inp[1])
class Rocket:
    def __init__(self, angle, rocketM, petrolM, gasSpeed, petrolComRate, image):
        self.rocketM = rocketM
        self.petrolM = petrolM
        self.gasSpeed = gasSpeed
        self.petrolComRate = petrolComRate
        self.angle = angle
        self.image = image
        self.x = 50
        self.y = 100
        self.speedX = 0
        self.speedY = 0

    def blit(self, screen):
        global height
        center = self.image.get_rect().center
        rotated_image = pg.transform.rotate(self.image, -90+self.angle)
        new_rect = rotated_image.get_rect(topleft = (self.x, height-self.y))
        screen.blit(rotated_image, new_rect)
    def gravity(self):
        global fps
        global g 
        self.speedY -= g / fps
    def changeAngle(self):
        self.angle = math.atan2(self.speedY, self.speedX) * 180 / math.pi
    def changeSpeedX(self):
        global fps
        self.speedX += (self.petrolComRate/fps) * \
        (self.gasSpeed * math.cos(self.angle*math.pi/180)) / \
        (self.rocketM - (self.petrolComRate/fps))
        #print(self.speedX)
    def changeSpeedY(self):
        global fps
        self.speedY += (self.petrolComRate/fps) * \
        (self.gasSpeed * math.sin(self.angle*math.pi/180)) / \
        (self.rocketM - (self.petrolComRate/fps))
    def changeCoordinate(self):
        global fps
        self.x += self.speedX / fps
        self.y += self.speedY / fps
        
class Star:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
    def blit(self, screen):
        screen.blit(self.image, self.image.get_rect(topleft = (self.x+20, height-self.y+30)))
        

width = 800
height = 600
fps = 60
planetM = dic['planetM']
planetR = dic['planetR']
g = 6.6720*planetM/planetR/planetR/10**11

background = pg.image.load('back.png')
starImage = pg.image.load('star.png')
pg.init()
screen = pg.display.set_mode((width, height))
clock = pg.time.Clock()
rocket = Rocket(dic['angle'], dic['rocketM'], dic['petrolM'], dic['gasSpeed'], dic['petrolComRate'], pg.image.load('rocket.png'))
print(rocket.angle)
isRun = True
t1 = 0
t2 = 0
second = 0
stars = []
while isRun:
    clock.tick(fps)
    t1 = (t1+1) % 20
    if t1 == 0:
        stars.append(Star(rocket.x, rocket.y, starImage))
    t2 = (t2+1) % fps
    if t2 == 0:
        second += 1
        print('Second:',second)
        print('-Rocket X:', rocket.x)
        print('-Rocket Y:', rocket.y)
        print('-Rocket speed X:', rocket.speedX)
        print('-Rocket speed Y:', rocket.speedY)
        print('-Rocket speed module:', math.sqrt(rocket.speedX**2+rocket.speedY**2))
        print('-Petrol weight:', max(0,rocket.petrolM))
    for e in pg.event.get():
        if e.type == pg.QUIT:
            isRun = False
        
    screen.blit(background, background.get_rect(bottomright = (width, height)))
    if rocket.petrolM > 0:
        rocket.changeSpeedX()
        rocket.changeSpeedY()
        rocket.petrolM -= rocket.petrolComRate / fps
    rocket.gravity()
    rocket.changeAngle()
    rocket.changeCoordinate()
    for i in stars:
        i.blit(screen)
    rocket.blit(screen)
    pg.display.update()
pg.quit()
