import pygame
import time
import sys
import os
import easygui

os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()
#okno gry
WIDTH, HEIGHT = 640, 520
screen = pygame.display.set_mode((WIDTH , HEIGHT))
FILL_SCREEN_COLOR = (24, 30, 50)
#pygame.display.set_caption("Pac-Man")

pygame.font.init()
FONT = pygame.font.SysFont("magneto", 20)
FONT_MAIN = pygame.font.SysFont("magneto", 45)

#zalożenia
x = y = 0
m = HEIGHT - 480

#zadanie gabarytów dla pac-mana
W = 32
H = 32

Q = H + m # dla lokalizacji pacmana
M = 2 #dla przemieszczania się

# import grafiki
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
# wstępna grafika
cover_image = "cover.png"
cover_path = os.path.join(desktop_path, cover_image)
cover = pygame.image.load(cover_path).convert_alpha()

# grafika "jedzenie"
food_image = "food.png"
food_path = os.path.join(desktop_path, food_image)
FOOD = pygame.image.load(food_path).convert_alpha()

# grafika pacman
P_R_image = "pacman.png"
P_R_path = os.path.join(desktop_path, P_R_image)
P_R = pygame.image.load(P_R_path)

P_L_image = "pacman_L.png"
P_L_path = os.path.join(desktop_path, P_L_image)
P_L = pygame.image.load(P_L_path)

P_U_image = "pacman_U.png"
P_U_path = os.path.join(desktop_path, P_U_image)
P_U = pygame.image.load(P_U_path)

P_D_image = "pacman_D.png"
P_D_path = os.path.join(desktop_path, P_D_image)
P_D = pygame.image.load(P_D_path)

P_OMNOM_image = "pacman1.png"
P_OMNOM_path = os.path.join(desktop_path, P_OMNOM_image)
P_OMNOM = pygame.image.load(P_OMNOM_path)

P_OMNOM_L_image = "pacman1_L.png"
P_OMNOM_L_path = os.path.join(desktop_path, P_OMNOM_L_image)
P_OMNOM_L = pygame.image.load(P_OMNOM_L_path)

P_OMNOM_U_image = "pacman1_U.png"
P_OMNOM_U_path = os.path.join(desktop_path, P_OMNOM_U_image)
P_OMNOM_U = pygame.image.load(P_OMNOM_U_path)

P_OMNOM_D_image = "pacman1_D.png"
P_OMNOM_D_path = os.path.join(desktop_path, P_OMNOM_D_image)
P_OMNOM_D = pygame.image.load("pacman1_D.png")

#zbiory pomocnicze
walls = []
foods = []

#pasek
class Board(object): 
    def __init__(self):
        self.rect = pygame.Rect(0, 0, WIDTH, m)

#pacman
class Player(object):
    angle = 0
    
    def __init__(self):
        #self.rect = pygame.Rect(32, 32, 16, 16)
        self.img = P_R
        self.rect = self.img.get_rect()
        self.rect.topleft = (W, Q)

    def move(self, dx, dy):

        if dx != 0:
            self.move_single_axis(dx, 0)
        if dy != 0:
            self.move_single_axis(0, dy)
    
    def move_single_axis(self, dx, dy):
        
        self.rect.x += dx
        self.rect.y += dy

        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if dx > 0: 
                    self.rect.right = wall.rect.left
                if dx < 0: 
                    self.rect.left = wall.rect.right
                if dy > 0: 
                    self.rect.bottom = wall.rect.top
                if dy < 0:
                    self.rect.top = wall.rect.bottom
     
    def rotate(self, elapsed_time):
        
        if self.angle == 0:
            
            if round(elapsed_time * 6) % 2 == 0:
                self.img = P_R
            else:
                self.img = P_OMNOM

        elif self.angle == 90:
                       
            if round(elapsed_time * 6) % 2 == 0:
                self.img = P_D
            else:
                self.img = P_OMNOM_D


        elif self.angle == 180:
                        
            if round(elapsed_time * 6) % 2 == 0:
                self.img = P_L
            else:
                self.img = P_OMNOM_L            

        elif self.angle == 270:
                        
            if round(elapsed_time * 6) % 2 == 0:
                self.img = P_U
            else:
                self.img = P_OMNOM_U            
        
        var_x = self.rect.x
        var_y = self.rect.y
        self.rect = self.img.get_rect()
        self.rect.x = var_x
        self.rect.y = var_y

    def eat(self, foods):
        var_x = self.rect.x
        var_y = self.rect.y
        self.rect = self.img.get_rect()
        self.rect.x = var_x
        self.rect.y = var_y
        
        for food in foods:
            f = food.rect.x
            d = food.rect.y            

            if var_x == f and var_y == d:
                foods.remove(food)
            else:
                None          

# class ściana
class Wall(object):
    def __init__(self, pos):
        walls.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], W, H)

# class food
class Food(object):
    def __init__(self, pos):
        foods.append(self)    
        self.img = FOOD
        self.rect = pygame.Rect(pos[0], pos[1], W, H)

# mapa 
mapa = [
    "WWWWWWWWWWWWWWWWWWWW",
    "W   W    F W    WF W",
    "W   W F  WWW  F    W",
    "WF  WWW   W    WWWWW",
    "W       F W F  W F W",
    "W  F  WW WWWW      W",
    "WWWW   W F     W F W",
    "WF W   W   WWWWWW WW",
    "W  W       FWF    FW",
    "WF    FWW   W  WW WW",
    "WWWWWWWWF      WF  W",
    "WF         WW  WW  W",
    "W   WW FW  FW      W",
    "WF   W  W   W FW  FW",
    "WWWWWWWWWWWWWWWWWWWW",
]
#W = wall, F = food
x = 0
y = m
for row in mapa:
    for col in row:
        if col == "W":
            Wall((x, y))
        if col == "F":
            Food((x, y))
        x += W
    y += W
    x = 0   

player = Player()

def draw(screen, walls, foods, player, elapsed_time):
    screen.fill((FILL_SCREEN_COLOR))
    for wall in walls:
        pygame.draw.rect(screen, (60, 70, 145), wall.rect)
         
    for food in foods:
        screen.blit(food.img, food.rect)

    screen.blit(player.img, player.rect)
    pygame.draw.rect(screen, (FILL_SCREEN_COLOR), Board().rect)
    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    screen.blit(time_text, (370, 10))
    count_text = FONT.render(f"Score: {25 - (len(foods))}", 1, "white") 
    screen.blit(count_text, (520, 10))
    task_text = FONT.render(f"Task: eat all purple candies!", 1, "white")
    screen.blit(task_text, (15, 10))
    pygame.display.flip()     

time_sleep = 1
  
def main():
    t = 1 
    
    if t == 1:
        screen.blit(cover, [0,0])
        pygame.display.flip()
        time.sleep(time_sleep)
        t -= 1 
        run = True 

    elif t == 0:
        run = True        

    else:
        run = False

    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0

    while run:

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                run = False
                pygame.quit()
                sys.exit()

    # poruszanie się pacmanem
        key = pygame.key.get_pressed()
        
        if key[pygame.K_LEFT]:
            player.move(-M, 0)
            player.angle = 180
            
        if key[pygame.K_RIGHT]:
            player.move(M, 0)
            player.angle = 0
            
        if key[pygame.K_UP]:
            player.move(0, -M)
            player.angle = 270         

        if key[pygame.K_DOWN]:
            player.move(0, M)
            player.angle = 90

        clock.tick(60)
        elapsed_time = time.time() - start_time 

        draw(screen, walls, foods, player, elapsed_time)
        
        player.rotate(elapsed_time)
        player.eat(foods)
 
        if len(foods) == 0:
            run = False
            time_food = round(elapsed_time)
            screen.fill((FILL_SCREEN_COLOR))
            GJ_text = FONT_MAIN.render(f"Good Job!", 1, "white")
            count_text = FONT.render(f"Your score: {25 - (len(foods))}", 1, "white")
            time_text = FONT.render(f"Time: {time_food}s", 1, "white") 
            screen.blit(count_text, (224, 240))
            screen.blit(GJ_text, (200, 180))
            screen.blit(time_text, (260, 270))
            pygame.display.flip()
            time.sleep(4)
            break
        else:
            continue
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()