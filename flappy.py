import pygame
import random

pygame.init()

WIDTH = 288
HEIGHT = 512

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

clock = pygame.time.Clock()

#background = pygame.image.load("background.png").convert()
#floor = pygame.image.load("floor.png").convert_alpha()
#bird = pygame.image.load("bird.png").convert_alpha()

background = pygame.image.load("background.jpeg").convert()
floor = pygame.image.load("floor.jpeg").convert_alpha()
bird_img = pygame.image.load("bird.png").convert_alpha()


class Bird:
    def __init__(self):
        self.x = 50
        self.y = 200
        self.gravity = 0.35 # original 0.25
        self.lift = -12 # original -4
        self.velocity = 0
        self.image = bird_img

    def show(self):
        screen.blit(self.image, (self.x, self.y))

    def up(self):
        self.velocity += self.lift

    def update(self):
        self.velocity += self.gravity
        self.velocity *= 0.9
        self.y += self.velocity
    
    def position(self):
        return self.x, self.y


class Pipe:
    min = 10
    max = 300
    pos_gap = random.randint(min, max) 
    p1 = None
    p2 = None

    def __init__(self):
        self.x = WIDTH
        self.y = 0 # fixed value
        self.speed = -3 # original -4
        self.width = 52
        self.height = 200 
        self.gap = 150 # espacio entre las tuberías

    def show(self):
        # dibuja la primera tubería
        self.p1 = pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y, self.width, self.pos_gap))
        # dibuja la segunda tubería
        self.p2 = pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y + self.pos_gap + self.gap, self.width, WIDTH))

    def update(self):
        self.x += self.speed
        
        if (self.x + self.width < 0):
            self.x = WIDTH
            self.y = 0
            self.pos_gap = random.randint(self.min, self.max) 
    
    def position(self):
        return self.p1, self.p2

bird = Bird()
pipe = Pipe()

score = 0
font = pygame.font.Font(None, 36)



def show_score():
    score_text = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

def show_bird_y():
    bird_y = int(bird.y)
    bird_y_text = font.render("Bird Y: " + str(bird_y), True, (255, 255, 255))
    screen.blit(bird_y_text, (10, 50))

def check_collision(bird, pipe): # esta funcion hay que mejorarla pero va queriendo
    x, y = bird.position()
    p1, p2 = pipe.position()
    
    #print(p1.bottom)
    #print(p2.top)

    bird_rec = pygame.Rect(x+20, y+25, 60, 50) #Rect(left, top, width, height)
    borde = 2  # Grosor de la línea en píxeles
    pygame.draw.rect(screen, (255, 255, 255), bird_rec, borde) # esto para ver el rectangulo
    
    # Comprueba si hay una colisión entre los dos rectángulos
    if pipe.p1.colliderect(bird_rec) or pipe.p2.colliderect(bird_rec):
        print("pipe left: " +  str(p1.left))
        print("bird positions: Rect(left, top, width, height)")
        print(bird_rec) #Rect(left, top, width, height)
        if pipe.p1.colliderect(bird_rec):
            print("Colision con el tubo de arriba")
            print("p1.bottom: " + str(p1.bottom))
            print("bird top: " + str(bird_rec.top))
        else: 
            print("Colision con el tubo de abajo")
            print("p2.top: " + str(p2.top))
            print("bird bottom: " + str(bird_rec.bottom))
        
        print("score: " + str(score))
        
        print("gave over bro!")
        return True

game_over = False

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE: # si aprieto espacio el pajaro salta
                bird.up()

    screen.blit(background, (0, 0))

    #pygame.draw.circle(screen, (255, 0, 0), (0, 0), 10)

    bird.show()
    bird.update()

    pipe.show()
    pipe.update()

    screen.blit(floor, (0, 450))

    if check_collision(bird, pipe):
        game_over = True

    # Actualizar el puntaje
    score += 1

    # Dibujar el puntaje en la pantalla
    show_score()
    show_bird_y()

    pygame.display.update()
    clock.tick(60)

pygame.quit()
