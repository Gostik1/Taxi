import os
import sys

import pygame
import random
from pygame import mixer

# переменные для конфигурации игры
WIDTH = 1000
HEIGHT = 700
FPS = 60

# переменные цветовых кодов
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)


# метод для безопасной загрузки в системе
def resource_path(relative):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(relative)


# инициализация элементов движка
pygame.init()
pygame.mixer.init()
pygame.font.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Taxi")
clock = pygame.time.Clock()

running = True

class Car(pygame.sprite.Sprite):
    def __init__(self, speed, images, dir):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        if dir == 1:
            for image in images:
                self.images.append(pygame.transform.rotate(image,180))
        elif dir == 0:
            self.images = images
        self.image = self.images[0]
        self.rect = self.image.get_rect()

        self.last_sprite_update = pygame.time.get_ticks()
        self.i = 0
        self.speed = speed

        #pygame.draw.rect(screen, GREEN, (self.rect.x, self.rect.y, self.image.get_width(),self.image.get_height()), 2)

class Player(Car):
    def __init__(self):
        super().__init__(4 * game_manager.game_speed, storage.taxi_images, 0)
        self.speedx = 0
        self.speedy = 0
        self.rect.x = 610
        self.rect.y = 300
        self.rect.height -= 50

    def update(self):
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if any(keystate):
            if keystate[pygame.K_LEFT]:
                animation(self, self.images, 200, True, 5)
                self.speedx = -1 * self.speed
            elif keystate[pygame.K_RIGHT]:
                animation(self, self.images, 200, True, -5)
                self.speedx = self.speed
            if keystate[pygame.K_UP]:
                self.speedy = -1 * self.speed
            elif keystate[pygame.K_DOWN]:
                self.speedy = self.speed
        else:
            animation(self, self.images, 200, True)

        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.x > 815:
            self.rect.x = 815
        if self.rect.x < 50:
            self.rect.x = 50
        if self.rect.y < 140:
            self.rect.y = 140
        if self.rect.y > 500:
            self.rect.y = 500

    def draw(self):
        screen.blit(self.image, self.rect)
        #pygame.draw.rect(screen, GREEN, (self.rect.x, self.rect.y, self.rect.width, self.rect.height), 2)

class TrafficCar(Car):
    def __init__(self, dir, x, y=-100):
        if dir == 0 or dir == 1:
            super().__init__(random.randint(8,9) * game_manager.game_speed, storage.cars_images[random.randint(0,3)], 1)
        elif dir == 2 or dir == 3:
            super().__init__(2 * game_manager.game_speed, storage.cars_images[random.randint(0,3)], 0)
        self.rect.x = x
        self.rect.y = y


    def update(self):
        self.rect.y += self.speed
        animation(self, self.images, 200, True)
        if self.rect.y > 800:
            all_cars.remove(self)
        if self.rect.colliderect(player.rect):
            print("Collide with car")
            self.kill()

class Traffic:
    def __init__(self):
        self.coords = [165, 320, 505, 675]
        self.last_update = pygame.time.get_ticks()
        self.speed = 4000

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.speed:
            place = random.randint(0,1)
            car = TrafficCar(place,x=self.coords[place], y=random.randint(300,350)*-1)
            all_cars.add(car)
            place = random.randint(2, 3)
            car = TrafficCar(place, x=self.coords[place], y=random.randint(300, 350) * -1)
            all_cars.add(car)
            self.last_update = now

class Human(pygame.sprite.Sprite):
    def __init__(self,images, state=0, dir=0):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.last_sprite_update = pygame.time.get_ticks()
        self.i = 0
        if dir == 1:
            for image in images:
                self.images.append(pygame.transform.rotate(image, 180))
            self.speed = 6 * game_manager.game_speed
        elif dir == 0:
            self.images = images
            self.speed = 4 * game_manager.game_speed
        if state == 0:
            self.images = self.images[:-2]
            self.image = self.images[0]
            self.rect = self.image.get_rect()
            self.rect.x = random.randint(45, 50) + (785 * random.randint(0, 1))
        elif state == 1:
            self.image = self.images[-1]
            self.rect = self.image.get_rect()
            self.rect.x = 100 + (660 * dir)
            self.speed = 5 * game_manager.game_speed
        self.rect.y = -100
        self.state = state
        self.dir = dir

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 800:
            self.kill()
        if self.rect.colliderect(player.rect):
            if self.state == 1:
                if self.dir == 1:
                    score_board.scores += 1
                elif self.dir == 0:
                    score_board.scores += 2
                self.kill()
            if self.state == 0:
                print("-1 Life")
                self.kill()
        if self.state == 0:
            animation(self, self.images, 200, True)


class Humans:
    def __init__(self):
        self.speed = 500
        self.coords = [165, 320, 505, 675]
        self.last_update = pygame.time.get_ticks()

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.speed:
            place = random.randint(0, 1)
            human = Human(images=storage.humans_images[random.randint(0,3)], state=random.randint(0,1)*random.randint(0,1), dir=random.randint(0,1))
            all_humans.add(human)
            self.last_update = now

class Road(pygame.sprite.Sprite):
    def __init__(self, x=0, y=0):
        pygame.sprite.Sprite.__init__(self)
        self.image = storage.road_images[random.randint(0,9)]
        self.rect = pygame.Rect(x, y, self.image.get_width(), self.image.get_height())
        self.speed = 5 * game_manager.game_speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 1395:
            self.rect.y = -700
    def draw(self):
        screen.blit(self.image, self.rect)
        pygame.draw.rect(screen, GREEN, (self.rect.x, self.rect.y, self.image.get_width(), self.image.get_height()), 2)


class ScoreBoard:
    def __init__(self):
        self.scores = 0

    def draw(self):
        print_text(f"SCORES: {self.scores}", storage.font,WHITE, 50,50)

class Storage:
    def __init__(self):
        self.taxi_images = load_images("taxi",6, 125, 250)
        self.road_images = load_images("road",10, 1000, 700)
        self.cars_images = [load_images("car_blue", 6, 125, 250),
                            load_images("car_green", 6, 125, 250),
                            load_images("car_lightblue", 6, 125, 250),
                            load_images("car_red", 6, 125, 250)]
        self.humans_images = [load_images("human_v1_", 7, 100, 100),
                              load_images("human_v2_", 7, 100, 100),
                              load_images("human_v3_", 7, 100, 100),
                              load_images("human_v4_", 7, 100, 100),]
        self.font = pygame.font.Font(resource_path(os.path.join("venv\\Sprites\\", "TaxiDriver.ttf")), 24)

class Debug:
    def __init__(self):
        pass

    def update(self):
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_m]:
            print(pygame.mouse.get_pos())



class GameManager:
    def __init__(self):
        self.in_game = True
        self.in_pause = False
        self.game_speed = 2

    def update(self):
        debug.update()
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_ESCAPE]:
            self.in_game = not self.in_game
            self.in_pause = not self.in_pause
        if self.in_game:
            player.update()
            traffic.update()
            humans.update()
            all_cars.update()
            all_humans.update()
            all_roads.update()
        if self.in_pause:
            pass


    def draw(self):
        if self.in_game:
            screen.blit(bg, bg.get_rect())
            all_roads.draw(screen)
            all_cars.draw(screen)
            all_humans.draw(screen)
            player.draw()
            score_board.draw()
        if self.in_pause:
            all_roads.draw(screen)
            all_cars.draw(screen)
            all_humans.draw(screen)
            player.draw()
            score_board.draw()


def animation(Entity, images, speed, endless, angle=0):
    now = pygame.time.get_ticks()
    is_alive = True
    if now - Entity.last_sprite_update > speed:
        Entity.i += 1
        if Entity.i > len(images) - 1:
            if endless:
                Entity.i = 0
            else:
                Entity.i = 0
                try:
                    Entity.kill()
                except Exception:
                    pass
                is_alive = False
                return is_alive
        if is_alive:
            Entity.last_sprite_update = now
            if angle == 0:
                Entity.image = images[Entity.i]
            else:
                Entity.image = pygame.transform.rotate(images[Entity.i], angle)
            return is_alive


def mouse_in_rect(rect):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    return rect.left < mouse_x < rect.left + rect.width and rect.top < mouse_y < rect.top + rect.height


def load_image(name, scaleX, scaleY):
    try:
        return pygame.transform.scale(
            pygame.image.load(resource_path(os.path.join("venv\\Sprites\\", str(name) + ".png"))).convert_alpha(),
            (scaleX, scaleY))
    except Warning:
        print(Warning)

def print_text(text, font, color, x, y):
    screen.blit(font.render(text, True, color),pygame.Rect((x, y), (100, 100)))

def load_images(name, count, scaleX, scaleY):
    array = []
    for i in range(count):
        array.append(load_image(str(name) + str(i + 1), scaleX, scaleY))
    return array

storage = Storage()
bg = pygame.transform.scale(storage.cars_images[0][1], (2000,2000))
all_cars = pygame.sprite.Group()
all_roads = pygame.sprite.Group()
all_humans = pygame.sprite.Group()
game_manager = GameManager()
for road in [Road(y=-700), Road(y=0), Road(y=700)]:
    all_roads.add(road)
all_humans = pygame.sprite.Group()

debug = Debug()
score_board = ScoreBoard()
player = Player()
traffic = Traffic()
humans = Humans()


while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_manager.in_game = not game_manager.in_game
                game_manager.in_pause = not game_manager.in_pause
    game_manager.update()
    game_manager.draw()
    pygame.display.flip()
sys.exit()
