import pygame
import os
import random
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((500,500))
pygame.display.set_caption('Crackgame!')
ticks = pygame.time.get_ticks()
gameloop = True
font = pygame.font.SysFont('Comic Sans MS', 30)
dt = 0
clock = pygame.time.Clock()
current_directory = os.path.dirname(os.path.realpath(__file__))
gnd = pygame.Rect(0, 400, 500, 100)
in_game = True
player_group = pygame.sprite.Group()
brick_group = pygame.sprite.Group()
things_that_kill_group = pygame.sprite.Group()
time_since_last_obstacle = 1000
score = 0
text = font.render(str(score), False, (0, 0, 0))
SPEED = 230
class background_picture():
    def __init__(self):
        self.image,self.rect = pygame.image.load(current_directory + '\\assets\graphics\\background_picture.png'), pygame.Surface.get_rect(pygame.image.load(current_directory + '\\assets\graphics\\background_picture.png'))
        self.rect.x = 0
        self.rect.x = 0
    def update(self):
        screen.blit(self.image,(self.rect.x,self.rect.y))
class player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image,self.rect = pygame.image.load(current_directory + '\\assets\graphics\\aztec_brick.png'), pygame.Surface.get_rect(pygame.image.load(current_directory + '\\assets\graphics\\aztec_brick.png'))
        self.rect.x = 100
        self.rect.y = 100
    def jump(self):
        if pygame.sprite.groupcollide(player_group,brick_group,False, False) or pygame.Rect.colliderect(self.rect,gnd):
            self.rect.y -= 230
        else:
            pass
    def fall(self):
        if not pygame.Rect.colliderect(self.rect,gnd):
            if not self.check_collision():
                self.rect.y += 350 * dt
    def stomp(self):
        if not pygame.Rect.colliderect(self.rect,gnd):
            if not self.check_collision():
                self.rect.y += 700 * dt
    def check_collision(self):
        #return pygame.Rect.colliderect(self.rect,obstacle)
        return pygame.sprite.groupcollide(player_group,brick_group,False,False)
    def check_collision_deadly(self):
        return pygame.sprite.groupcollide(player_group,things_that_kill_group,False,False)
    def update(self):
        self.fall()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_e]:
            self.jump()
        if keys[pygame.K_q]:
            self.stomp()
class brick(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image,self.rect = pygame.image.load(current_directory + '\\assets\graphics\\background.png'), pygame.Surface.get_rect(pygame.image.load(current_directory + '\\assets\graphics\\background.png'))
        self.rect.x = x
        self.rect.y = y
        things_that_kill_group.add(inner_hitbox(self.rect.x,self.rect.y))
    def update(self):
        self.rect.x -= SPEED * dt
        if self.rect.x < 0:
            brick_group.remove(self)
class spike(pygame.sprite.Sprite):
    def __init__(self,x,y,facing):
        pygame.sprite.Sprite.__init__(self)
        if facing == "left":
            self.image,self.rect = pygame.image.load(current_directory + '\\assets\graphics\spike_left.png'), pygame.Surface.get_rect(pygame.image.load(current_directory + '\\assets\graphics\spike_left.png'))
        elif facing == "right":
            self.image,self.rect = pygame.image.load(current_directory + '\\assets\graphics\spike_right.png'), pygame.Surface.get_rect(pygame.image.load(current_directory + '\\assets\graphics\spike_right.png'))
        elif facing == "up":
            self.image,self.rect = pygame.image.load(current_directory + '\\assets\graphics\spike_up.png'), pygame.Surface.get_rect(pygame.image.load(current_directory + '\\assets\graphics\spike_up.png'))
        else:
            self.image,self.rect = pygame.image.load(current_directory + '\\assets\graphics\spike_down.png'), pygame.Surface.get_rect(pygame.image.load(current_directory + '\\assets\graphics\spike_down.png'))
        self.rect.x = x
        self.rect.y = y
    def update(self):
        self.rect.x -= SPEED * dt
        if self.rect.x < 0:
            things_that_kill_group.remove(self)
class inner_hitbox(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image,self.rect = pygame.image.load(current_directory + '\\assets\graphics\inner_hitbox.png'), pygame.Surface.get_rect(pygame.image.load(current_directory + '\\assets\graphics\inner_hitbox.png'))
        self.rect.x = x 
        self.rect.y = y + 16
    def update(self):
        self.rect.x -= SPEED * dt
        if self.rect.x < 0:
            things_that_kill_group.remove(self)
class ground():
    def __init__(self):
        self.image,self.rect = pygame.image.load(current_directory + '\\assets\graphics\ground.png'), pygame.Surface.get_rect(pygame.image.load(current_directory + '\\assets\graphics\ground.png'))
        self.rect.x = 0
        self.rect.y = 400
    def update(self):
        screen.blit(self.image,(self.rect.x,self.rect.y))
def generate_obstacles(x,y):
    rand = random.randint(1,6)
    print(rand)
    if rand == 1:
        brick_group.add(brick(x-32,y+32))
        brick_group.add(brick(x+32,y-32))
        rand1 = random.randint(1,3)
        if rand1 == 1:
            things_that_kill_group.add(spike(x-64-16,y+32,"left"))
            things_that_kill_group.add(spike(x-64-16,y+64,"left"))
        elif rand1 == 2:
            things_that_kill_group.add(spike(x+32,y+32,"down"))
            things_that_kill_group.add(spike(x+64,y+32,"down"))
        else:
            things_that_kill_group.add(spike(x+90,y-32,"right"))
            things_that_kill_group.add(spike(x+90,y,"right"))
    elif rand == 2:
        brick_group.add(brick(x-32,y-32))
        brick_group.add(brick(x+32,y-32))

        rand2 = random.randint(1,2)
        if rand2 == 1:
            pass
        else:
            things_that_kill_group.add(spike(x+32,y-80,"up"))
    elif rand == 3:
        brick_group.add(brick(x+32,y-32))
        brick_group.add(brick(x-32,y+32))
    elif rand == 4:
        things_that_kill_group.add(spike(x-16,y+64,"up"))
        things_that_kill_group.add(spike(x+16,y+64,"up"))
    elif rand == 5:
        brick_group.add(brick(x,y-32))
        brick_group.add(brick(x,y+32))
        rand5 = random.randint(1,2)
        if rand5 == 1:
            things_that_kill_group.add(spike(x-48,y+64,"left"))
            things_that_kill_group.add(spike(x-48,y+32,"left"))
        if rand5 == 2:
            things_that_kill_group.add(spike(x-48,y-32,"left"))
            things_that_kill_group.add(spike(x-48,y,"left"))
        if rand5 == 3:
            things_that_kill_group.add(spike(x-48,y+64,"right"))
            things_that_kill_group.add(spike(x-48,y+32,"right"))
        if rand5 == 4:
            things_that_kill_group.add(spike(x-48,y-32,"right"))
            things_that_kill_group.add(spike(x-48,y,"right"))
    else:
        brick_group.add(brick(x-32,y-32))
        brick_group.add(brick(x+32,y+32))
obstacle = pygame.Rect(300,40,50,100)
p1 = player()
player_group.add(p1)
background = background_picture()
floor = ground()
while gameloop:
    while in_game:
        ticks = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                in_game = False
                gameloop = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    gameloop = False
        if time_since_last_obstacle > 0:
            if ticks - time_since_last_obstacle > 1000:
                generate_obstacles(450,300)
                score += 1
                text = font.render(str(score), False, (0, 255, 0))
                time_since_last_obstacle = ticks
        screen.fill("white")
        #pygame.draw.rect(screen,"blue",obstacle)
        if p1.check_collision_deadly():
            in_game = False
        else:
            pass
        background.update()
        floor.update()
        player_group.update()
        things_that_kill_group.update()
        brick_group.update()
        player_group.draw(screen)
        things_that_kill_group.draw(screen)
        brick_group.draw(screen)
        screen.blit(text,(100,100))
        pygame.display.flip()
        clock.tick(60)
        dt = clock.tick(60) / 1000
    #hier irgendwas callen was beim death passiert
    score = 0
    player_group.empty()
    brick_group.empty()
    things_that_kill_group.empty()
    p1 = player()
    player_group.add(p1)
    in_game = True
pygame.quit()