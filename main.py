import pygame
import random

scw = 1200
sch = 700
fps = 40
spawnplace_x = scw + (0.1 * scw)
cloudspwnpl_x = scw + 1000
cloudspwnpl_y = sch + 30

black = (0, 0, 0,)
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 203, 254)
red = (255, 0, 0)
yellow = (255, 215, 0)

jet = pygame.image.load("jet.png")
plate = pygame.image.load("plate.png")
cloud = pygame.image.load("cloud.png")
stoneball_images = ['stoneball.png', 'stoneballBig.png', 'stoneballMedium.png']

pygame.mixer.init()
pewsound = pygame.mixer.Sound("pew1.wav")
expl_sounds = ['expl1.wav', 'expl2.wav']
pickupCoin = pygame.mixer.Sound("pickupCoin.wav")
music = pygame.mixer.Sound("technogeek.mp3")
pygame.mixer.music.set_volume(0.4)

import pygame

explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)

    img1 = pygame.image.load('regularExplosion00.png')
    img2 = pygame.image.load('regularExplosion01.png')
    img3 = pygame.image.load('regularExplosion02.png')
    img4 = pygame.image.load('regularExplosion03.png')
    img5 = pygame.image.load('regularExplosion04.png')
    img6 = pygame.image.load('regularExplosion05.png')
    img7 = pygame.image.load('regularExplosion06.png')
    img8 = pygame.image.load('regularExplosion07.png')
    img9 = pygame.image.load('regularExplosion08.png')

    img_lg1 = pygame.transform.scale(img1, (58, 58))
    img_lg2 = pygame.transform.scale(img2, (58, 58))
    img_lg3 = pygame.transform.scale(img3, (58, 58))
    img_lg4 = pygame.transform.scale(img4, (58, 58))
    img_lg5 = pygame.transform.scale(img5, (58, 58))
    img_lg6 = pygame.transform.scale(img6, (58, 58))
    img_lg7 = pygame.transform.scale(img7, (58, 58))
    img_lg8 = pygame.transform.scale(img8, (58, 58))
    img_lg9 = pygame.transform.scale(img9, (58, 58))

    img_sm1 = pygame.transform.scale(img1, (32, 32))
    img_sm2 = pygame.transform.scale(img2, (32, 32))
    img_sm3 = pygame.transform.scale(img3, (32, 32))
    img_sm4 = pygame.transform.scale(img4, (32, 32))
    img_sm5 = pygame.transform.scale(img5, (32, 32))
    img_sm6 = pygame.transform.scale(img6, (32, 32))
    img_sm7 = pygame.transform.scale(img7, (32, 32))
    img_sm8 = pygame.transform.scale(img8, (32, 32))
    img_sm9 = pygame.transform.scale(img9, (32, 32))

    pct1 = pygame.transform.scale(img1, (78, 78))
    pct2 = pygame.transform.scale(img2, (78, 78))
    pct3 = pygame.transform.scale(img3, (78, 78))
    pct4 = pygame.transform.scale(img4, (78, 78))
    pct5 = pygame.transform.scale(img5, (78, 78))
    pct6 = pygame.transform.scale(img6, (78, 78))
    pct7 = pygame.transform.scale(img7, (78, 78))
    pct8 = pygame.transform.scale(img8, (78, 78))
    pct9 = pygame.transform.scale(img9, (78, 78))

    explosion_anim['lg'] = [img_lg1, img_lg2, img_lg3, img_lg4, img_lg5, img_lg6, img_lg7, img_lg8, img_lg9]
    explosion_anim['sm'] = [img_sm1, img_sm2, img_sm3, img_sm4, img_sm5, img_sm6, img_sm7, img_sm8, img_sm9]
    explosion_anim['pl'] = [pct1, pct2, pct3, pct4, pct5, pct6, pct7, pct8, pct9]


class Player (pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = jet
        self.image.set_colorkey(white)
        self.rect = self.image.get_rect()
        self.rect.center = ((scw / 2, sch/2))

        self.shield = 100

        self.shoot_delay = 180
        self.last_shot = pygame.time.get_ticks()

    def update(self):
        keystate = pygame.key.get_pressed()
        self.speedx = 0
        self.speedy = 0

        if keystate[pygame.K_LEFT]:
            self.speedx -= 8
        if keystate[pygame.K_RIGHT]:
            self.speedx += 8
        self.rect.x += self.speedx

        if keystate[pygame.K_UP]:
            self.speedy -= 8
        if keystate[pygame.K_DOWN]:
            self.speedy += 8
        self.rect.y += self.speedy

        if keystate[pygame.K_SPACE]:
            self.shoot()

        if self.rect.right > scw:
            self.rect.right = scw
        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.top >= sch:
            self.rect.bottom = sch
        if self.rect.bottom <= 0:
            self.rect.top = 0

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.rect.centerx, self.rect.bottom)
            sprites.add(bullet)
            bullets.add(bullet)
            pewsound.play()


class Mob (pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = plate
        self.image.set_colorkey(white)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(scw, spawnplace_x)
        self.rect.y = random.randrange(0, sch)
        self.speedx = random.randrange(-1, -8, -1)
        self.speedy = random.randrange(-1, 1)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.right < 0 or self.rect.bottom > sch:
            self.rect.x = random.randrange(scw, spawnplace_x)
            self.rect.y = random.randrange(0, sch)


class Bullet (pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((20, 10))
        self.image.fill(yellow)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedx = 10

    def update(self):
        self.rect.x += self.speedx
        if self.rect.left > scw:
            self.kill()


class Cloud (pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = cloud
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(scw, cloudspwnpl_x)
        self.rect.y = random.randrange(-30, cloudspwnpl_y)
        self.speedx = -4

    def update(self):
        self.rect.x += self.speedx
        if self.rect.right < 0:
            self.rect.right = random.randrange(scw, cloudspwnpl_x)
            self.rect.y = random.randrange(-30, cloudspwnpl_y)


class Stoneball (pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        imageStoneball = random.choice(stoneball_images)
        imageStoneball = pygame.image.load(imageStoneball)

        self.image_orig = imageStoneball
        self.image_orig.set_colorkey(white)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.85 / 2)
        self.rect.x = random.randrange(scw, spawnplace_x)
        self.rect.y = random.randrange(0, sch)
        self.speedx = random.randrange(-1, -8, -1)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        if self.rect.right < 0 or self.rect.bottom > sch:
            self.rect.x = random.randrange(scw, spawnplace_x)
            self.rect.y = random.randrange(0, sch)


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


def newmob():
    mob = Mob()
    sprites.add(mob)
    mobs.add(mob)

def newstoneball():
    stoneball = Stoneball()
    sprites.add(stoneball)
    stoneballs.add(stoneball)

def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    barlength = 100
    barheigth = 10
    fill = (pct / 100) * barlength
    outline_rect = pygame.Rect(x, y, barlength, barheigth)
    fill_rect = pygame.Rect(x, y, fill, barheigth)
    pygame.draw.rect(surf, green, fill_rect)
    if player.shield < 100:
        if player.shield >= 40:
            pygame.draw.rect(surf, yellow, fill_rect)
        if player.shield <= 39:
            pygame.draw.rect(surf, red, fill_rect)
    pygame.draw.rect(surf, white, outline_rect, 2)


font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, black)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)
addText = "Your score: "
addText2 = "Coins:"


pygame.init()
screen = pygame.display.set_mode((scw, sch))
pygame.display.set_caption("Game")
clock = pygame.time.Clock()

sprites = pygame.sprite.Group()
player = Player()
sprites.add(player)

bullets = pygame.sprite.Group()

clouds = pygame.sprite.Group()
for i in range(8):
    cld = Cloud()
    sprites.add(cld)
    clouds.add(cld)

stoneballs = pygame.sprite.Group()
for i in range(3):
    newstoneball()

    score = 0
    coins = 0


n = 20
# now = pygame.time.get_ticks()
# lastUpdate = 0
# if lastUpdate - now > 30000:
#     n += 18
mobs = pygame.sprite.Group()
for i in range(n):
    newmob()

    score = 0

music.play(loops=-1)
running = True
while running:
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:   
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()


    collides = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_rect_ratio(0.9))
    for collide in collides:
        player.shield -= 30
        expl = Explosion(collide.rect.center, 'sm')
        sprites.add(expl)
        newmob()
        if player.shield <= 0:
            explSound = random.choice(expl_sounds)
            explSound = pygame.mixer.Sound(explSound)
            explSound.play()
            
            death_explosion = Explosion(player.rect.center, 'pl')
            sprites.add(death_explosion)
            player.kill()

    collides1 = pygame.sprite.spritecollide(player, stoneballs, True, pygame.sprite.collide_rect_ratio(0.9))
    for collide1 in collides1:
        player.shield -= 40
        expl = Explosion(collide1.rect.center, 'sm')
        sprites.add(expl)
        newstoneball()
        if player.shield <= 0:
            explSound = random.choice(expl_sounds)
            explSound = pygame.mixer.Sound(explSound)
            explSound.play()

            death_explosion = Explosion(player.rect.center, 'pl')
            sprites.add(death_explosion)
            player.kill()



    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        score += 10
        newmob()

        explSound = random.choice(expl_sounds)
        explSound = pygame.mixer.Sound(explSound)
        explSound.play()

        expl = Explosion(hit.rect.center, 'lg')
        sprites.add(expl)

    hitsStoneball = pygame.sprite.groupcollide(stoneballs, bullets, True, True)
    for hit in hitsStoneball:
        score += 40 - hit.radius
        if hit.radius == 20:
            coins += 1
        elif hit.radius == 10:
            coins += 3 
        else:
            coins += 2

        stb = Stoneball()
        sprites.add(stb)
        stoneballs.add(stb)

        pickupCoin.play()

        expl = Explosion(hit.rect.center, 'lg')
        sprites.add(expl)

    screen.fill(blue)

    sprites.update()
    sprites.draw(screen)

    draw_text(screen, str(addText), 18, 60, 10)
    draw_text(screen, str(score), 18, 110, 10 )
    draw_text(screen, str(addText2), 18, 43, 38)
    draw_text(screen, str(coins), 18, 83, 38)

    draw_shield_bar(screen, 20, 66, player.shield)

    if not player.alive() and not death_explosion.alive():
        running = False



    pygame.display.flip()

pygame.quit()

# Уровни сложности - увелич. кол-во мобов; дополнительные враги (с хитами)