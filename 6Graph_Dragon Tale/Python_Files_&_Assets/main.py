import time

import pygame
import os
from pygame import mixer
import random

pygame.font.init()
pygame.init()
mixer.init()

# Notes
    # Change assets
    # Scale down players and enemies


WIDTH, HEIGHT = 1200, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dragon Tale")

# Enemy Image Load
enemy1 = pygame.image.load(os.path.join("assets", "enemy1.png"))
enemy1 = pygame.transform.scale(enemy1, (70, 50))

enemy2 = pygame.image.load(os.path.join("assets", "enemy2.png"))
enemy2 = pygame.transform.scale(enemy2, (120, 110))

enemy3 = pygame.image.load(os.path.join("assets", "enemy3.png"))
enemy3 = pygame.transform.scale(enemy3, (70, 50))

# Player Image Load
player_ship = pygame.image.load(os.path.join("assets", "player.png"))
player_ship = pygame.transform.scale(player_ship, (80, 70))

# Bullets
bullet_1 = pygame.image.load(os.path.join("assets", "enemy_bullet_1.png"))
bullet_1 = pygame.transform.scale(bullet_1, (70, 60))

bullet_2 = pygame.image.load(os.path.join("assets", "enemy_bullet_2.png"))
bullet_2 = pygame.transform.scale(bullet_2, (130, 120))

bullet_3 = pygame.image.load(os.path.join("assets", "enemy_bullet_3.png"))
bullet_3 = pygame.transform.scale(bullet_3, (100, 90))


player_bullet = pygame.image.load(os.path.join("assets", "player_bullet.png"))
player_bullet = pygame.transform.scale(player_bullet, (70, 60))

# Background
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background_sunset.png")), (WIDTH, HEIGHT))
BG_1 = pygame.transform.scale(BG, (WIDTH, HEIGHT))

BG1 = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background_day.png")), (WIDTH, HEIGHT))
BG1_1 = pygame.transform.scale(BG1, (WIDTH, HEIGHT))

BG2 = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background_night.png")), (WIDTH, HEIGHT))
BG2_1 = pygame.transform.scale(BG2, (WIDTH, HEIGHT))

position = 0


def background_1():
    global position

    WIN.fill((0, 0, 0))

    WIN.blit(BG_1, (0, position))
    WIN.blit(BG_1, (0, -BG_1.get_height() + position))

    position += 3

    if abs(position) > BG_1.get_height():
        position = 0


def background_2():
    global position

    WIN.fill((0, 0, 0))

    WIN.blit(BG1_1, (0, position))
    WIN.blit(BG1_1, (0, -BG1_1.get_height() + position))

    position += 3

    if abs(position) > BG1_1.get_height():
        position = 0


def background_3():
    global position

    WIN.fill((0, 0, 0))

    WIN.blit(BG2_1, (0, position))
    WIN.blit(BG2_1, (0, -BG2_1.get_height() + position))

    position += 3

    if abs(position) > BG2_1.get_height():
        position = 0

# Music
mixer.music.load('assets/background_theme.ogg')
pygame.mixer.music.play(-1)

player_fireball_sfx = pygame.mixer.Sound("assets/player_fireball.mp3")


class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return not(self.y <= height and self.y >= 0)

    def collision(self, obj):
        return collide(self, obj)


class Ship:
    # Fire Cooldown
    COOLDOWN = 40

    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    # Firing Mechanic
    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    def shoot_1(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x+5, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1
            pygame.mixer.Sound.play(player_fireball_sfx)

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()


class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = player_ship
        self.laser_img = player_bullet
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    def move_lasers(self, vel, objs, score=1):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        file = open("text.txt", "a")
                        score = str(score)
                        file.write(score+",")
                        file.close()
                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window):
        pygame.draw.rect(window, (255,0,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0,255,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health/self.max_health), 10))


class Enemy(Ship):
    COLOR_MAP = {
                "enemy1": (enemy1, bullet_1),
                "enemy2": (enemy2, bullet_2),
                "enemy3": (enemy3, bullet_3)
                }

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x-20, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1


def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y

    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

def main():
    run = True
    FPS = 60
    level = 0
    lives = 5
    sum = 0
    cooldown = 0

    main_font = pygame.font.SysFont("Times New Roman", 50)
    lost_font = pygame.font.SysFont("Times New Roman", 60)

    enemies = []
    wave_length = 5
    enemy_vel = 1

    player_vel = 10
    laser_vel = 5

    player = Player(300, 630)

    clock = pygame.time.Clock()

    lost = False
    lost_count = 0

    def redraw_window():
        if level == 1 or level == 4 or level == 7:
            background_1()
        elif level == 2 or level == 5 or level == 8:
            background_2()
        elif level == 3 or level == 6 or level == 9:
            background_3()

        # draw text (base health label)
        level_label = main_font.render(f"Level: {level}", 1, (255,255,255))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

        base_health_label = main_font.render(f"Base Life: {lives}", 5, (255, 255, 255))  # arrangement
        WIN.blit(base_health_label, (base_health_label.get_width()-230, 10))

        score_label = main_font.render(f"Score: {sum}", 1, (255,255,255))
        WIN.blit(score_label, (score_label.get_width()-150, 80))

        for enemy in enemies:
            enemy.draw(WIN)

        player.draw(WIN)

        if lost:
            points = open('text.txt', 'w')
            points.write("")
            points.close()

            lost_label = lost_font.render("You Lost!!", 1, (255,255,255))
            WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 350))

        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()


        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS * 3:
                run = False
            else:
                continue

        if len(enemies) == 0:
            level += 1
            wave_length += 5
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH-100), random.randrange(-1500, -100), random.choice(["enemy1",
                                                                                                             "enemy2",
                                                                                                             "enemy3"]))
                enemies.append(enemy)

        timer_interval = 500  # 0.5 seconds
        timer_event = pygame.USEREVENT + 1
        pygame.time.set_timer(timer_event, timer_interval)



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            #if event.type == pygame.KEYDOWN:
               # if event.key == pygame.K_SPACE:
                #    pygame.mixer.Sound.play(player_fireball_sfx)


        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - player_vel > 0: # left
            player.x -= player_vel
        if keys[pygame.K_d] and player.x + player_vel + player.get_width() < WIDTH: # right
            player.x += player_vel
        if keys[pygame.K_w] and player.y - player_vel > 0: # up
            player.y -= player_vel
        if keys[pygame.K_s] and player.y + player_vel + player.get_height() + 15 < HEIGHT: # down
            player.y += player_vel
        if keys[pygame.K_SPACE]:
            player.shoot_1()

        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player)

            if random.randrange(0, 2*60) == 1:
                enemy.shoot()

            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)
            elif enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)

        player.move_lasers(-laser_vel, enemies)

        score = open('text.txt', 'r')

        lines = score.readlines()
        sum = 0

        for line in lines:
            for c in line:
                if c.isdigit() == True:
                    sum = sum + int(c)

        score.close()


# Game Start
def main_menu():
    point_reset = open('text.txt', "w")
    point_reset.write("")
    point_reset.close()

    title_font = pygame.font.SysFont("Times New Roman", 70)
    controls_font = pygame.font.SysFont("Times New Roman", 50)

    run = True
    while run:
        WIN.blit(BG, (0, 0))

        title_label = title_font.render("PRESS THE MOUSE TO BEGIN", 1, (0,0,0))
        WIN.blit(title_label, (WIDTH / 2 - title_label.get_width()/2, 350))

        controls_label = controls_font.render("Controls: W, A, S, D", 1, (0,0,0))
        WIN.blit(controls_label, (WIDTH/2 - controls_label.get_width()/2, 550))

        controls_label1 = controls_font.render("Spacebar to fire", 1, (0,0,0))
        WIN.blit(controls_label1, (WIDTH / 2 - controls_label1.get_width() / 2, 650))

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
    pygame.quit()


main_menu()
