import pygame
import random
 
WIDTH = 650
HEIGHT = 400

FPS = 30
BLUE = (0,0,255)
WHITE = (255, 255, 255)
CHIRBIRD = (0, 128, 128)
BLACK=(0,0,0)
GREEN=(65,63,0)
YELLOW=(255,255,0)
PURPLE=(155,255,0)
RED=(255,0,0)
BLUE=(0,255,255)

pygame.init()

x = 50
y = 300
r = 10

score = 0

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()



running = True
motion = "Stop"
state = "Game"

hop = 0
jump = "Fall"
player1 = pygame.image.load('mage1.png').convert()
player1 = pygame.transform.scale(player1, (50, 60))
player2 = pygame.image.load('mage2.png').convert()
player2 = pygame.transform.scale(player2, (50, 60))
player = player1

enemy1 = pygame.image.load('enemybullet.png').convert()
enemy1 = pygame.transform.scale(enemy1, (50, 60))
enemy2 = pygame.image.load('enemybullet.png').convert()
enemy2 = pygame.transform.scale(enemy2, (50, 60))
enemy = enemy2

bullet = pygame.image.load('projectile1.jpg').convert()
bullet = pygame.transform.scale(bullet, (10, 10))

enemyDir = random.randint(1, 2) #1 слева # 2 справа
if enemyDir == 1:
    enemyX = -100
else:
    enemyX = 650
enemyY = 300

enemyX = 650
enemyY = 300

enemySpeed = 3

font = pygame.font.SysFont("arial", 36)


isShot = False

xbullet = []
ybullet = []
dirbullet = []

while running:
    if state == "Dead":
        enemySpeed= 3
        events = pygame.event.get()
        for i in events:
            if i.type == pygame.QUIT:
                pygame.quit()
            if i.key == pygame.K_SPACE:
                state = "Game"
                #спаун врага
                enemyDir = random.randint(1, 2) #1 слева # 2 справа
                if enemyDir == 1:
                    enemyX = -100
                else:
                    enemyX = 700
                enemyY = 300
                score = 0
        
        screen.fill(CHIRBIRD)
        scoreText = font.render(score, 1, (255, 0, 0))
        screen.blit(scoreText, (WIDTH / 2 - scoreText.get_width() / 2, 100))
        Text = font.render("Нажмите пробел", 1, (255, 0, 0))
        screen.blit(Text, (WIDTH / 2 - Text.get_width() / 2, 150))        
        
    if state == "Game":     
        events = pygame.event.get()
        for i in events:
            if i.type == pygame.QUIT:
                pygame.quit()
            if i.type == pygame.KEYDOWN:
                if i.key == pygame.K_LEFT:
                    motion = "Left"
                    player = player2
                if i.key == pygame.K_RIGHT:
                    motion = "Right"
                    player = player1
                if i.key == pygame.K_DOWN:
                    motion = "Down"
                if i.key == pygame.K_UP:
                    motion = "Up"
                if i.key == pygame.K_SPACE:
                    if y == HEIGHT - 100:
                        jump = "HOP"
                if i.key == pygame.K_1:
                    isShot = True
            if i.type == pygame.KEYUP:
                motion = "Stop"
        
        if motion == "Left":
            x = x - 5
        if motion == "Right":
            x = x + 5
            
            
        if jump == "Fall": #падаем
            y = y + 5
            if y > HEIGHT - 100:
                y = HEIGHT - 100
        else: #прыгаем
            if hop < 10:
                y = y - 13
                hop += 1
            else: #закончили прыгать
                hop = 0
                jump = "Fall"
        
        #Враги
        
            enemyY = enemyY + 5
        
        if enemyY > HEIGHT - 100:
            enemyY = HEIGHT - 100
        
        if enemyX > x + 25:
            enemyX -= enemySpeed
        elif enemyX < x - 30:
            enemyX += enemySpeed
        elif enemyY > y and enemyY < y + 50:
            enemyDir = random.randint(1, 2) #1 слева # 2 справа
            if enemyDir == 1:
                enemyX = -100
            else:
                enemyX = 650
            enemyY = 300
            score += 3
            enemySpeed += 0.5
        elif enemyY == y:
            state = "Dead"
            
        
    
        #Пули 
        if isShot == True:
            isShot = False
            score -= 3
            if player == player1:
                xbullet.append(x + 25)
                ybullet.append(y + 25)
                dirbullet.append("R")
            else:
                xbullet.append(x)
                ybullet.append(y + 25)
                dirbullet.append("L")
            
        for i in range(0, len(xbullet)): 
            if  xbullet[i] > (enemyX - 10) and xbullet[i] < (enemyX + 70) and ybullet[i] < enemyY + 50 and ybullet[i] > enemyY:
                enemyDir = random.randint(1, 2) #1 слева # 2 справа
                if enemyDir == 1:
                    enemyX = -100
                else:
                    enemyX = 700
                enemyY = 300
                xbullet[i] = -1
                ybullet[i] = -1
                dirbullet[i] = -1
                score += 5
                enemySpeed += 0.5
        
        while -1 in xbullet:
            xbullet.remove(-1)
            ybullet.remove(-1) 
            dirbullet.remove(-1)
            
        screen.fill(WHITE)
        scoreText = font.render(score, 1, (255, 0, 0))
        screen.blit(scoreText, (WIDTH / 2 - scoreText.get_width() / 2, 100))
        screen.blit(player, (x, y))
        screen.blit(enemy, (enemyX, enemyY))
        
        
        for i in range(0, len(xbullet)):
            if dirbullet[i] == "R":
                xbullet[i] += 5
            else:
                xbullet[i] -= 5
            screen.blit(bullet, (xbullet[i], ybullet[i]))
    
    pygame.display.update()
    clock.tick(FPS)
    