from pygame import *
from random import randint
font.init()
from time import time as tm

window = display.set_mode((900,500))
display.set_caption('Шутер')
background = transform.scale(image.load("ogorod.jpg"), (900,500))
game = True

clock = time.Clock()
FPS = 60

lost = 0
score = 0
font1 = font.SysFont('Arial', 70)
win = font1.render('ТЫ ПОБЕДИЛ!', True, (255, 215, 0))
lose = font1.render('ТЫ ПРОИГРАЛ!', False, (255, 215, 0))
font2 = font.SysFont('Arial', 30)


mixer.init()
mixer.music.load('space.ogg')
fire_sound = mixer.Sound('fire.ogg')
# mixer.music.play()



finish = False

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, w, h, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (w,h))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x < 740:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('pyla.png', self.rect.centerx, self.rect.top, 15,20, -15)
        bullets.add(bullet)
class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed 
        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = randint(0, 830)
            lost += 1

class Asteroidi(GameSprite):
    def update(self):
        self.rect.y += self.speed 
        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = randint(0, 830)


class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y <= 0:
            self.kill()

monsters = sprite.Group()
bullets = sprite.Group()
asteroids = sprite.Group()

for i in range(3):
    asteroid = Asteroidi('asteroid.png', randint(0,830), -50, 70, 100,1)
    asteroids.add(asteroid)

for i in range(5):
    enemy = Enemy('homyak2.png', randint(0,830), -50, 40, 60, randint(1,3))
    monsters.add(enemy)
    
num_fire = 0
rel_time = False


player = Player('ohotnik.png', 0, 420, 160,80,10)

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if  num_fire < 5 and rel_time == False:
                    player.fire()
                    fire_sound.play()
                    num_fire += 1
                if num_fire >= 5 and rel_time == False:
                    rel_time = True
                    start = tm()
    if finish != True:
        window.blit(background,(0,0))
        player.update()
        monsters.update()
        monsters.draw(window)
        asteroids.update()
        asteroids.draw(window)
        player.reset()
        text_lose = font2.render('Пропущено:' + str(lost), 1, (255,255,255))
        window.blit(text_lose, (10,50))
        text_score = font2.render('Счёт:' + str(score), 1, (255,255,255))
        window.blit(text_score, (10,10))
        bullets.update()
        bullets.draw(window)
        if rel_time == True:
            end = tm()
            if end - start < 3:
                reluat = font1.render('ИДЁТ ПЕРЕЗАРЯДКА', True, (255, 215, 0))
                window.blit(reluat, (100, 400))
            else:
                num_fire = 0
                rel_time = False
        sprites_list = sprite.groupcollide(monsters, bullets, True, True)
        for x in sprites_list:
            score += 1
            enemy = Enemy('homyak2.png', randint(0,830), -50, 70, 100, randint(1,3))
            monsters.add(enemy)
        if sprite.spritecollide(player, monsters, False) or lost > 3 or sprite.spritecollide(player, asteroids, False):
            finish = True
            window.blit(lose,(200,200))
        if score >= 10:
            finish = True
            window.blit(win, (200,200))
    display.update()
    clock.tick(FPS)
