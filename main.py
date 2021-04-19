import os
import sys

import pygame
import random
from pygame import mixer

# переменные для конфигурации игры
WIDTH = 1200
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

    def draw(self):
        animation(self, self.images, 200, False)
        screen.blit(self.image, self.rect)
        #pygame.draw.rect(screen, GREEN, (self.rect.x, self.rect.y, self.image.get_width(),self.image.get_height()), 2)

class Player(Car):
    def __init__(self):
        super().__init__(7, storage.taxi_images, 0)
        self.image_forward = self.image
        self.image_left = pygame.transform.rotate(self.image, 5)
        self.image_right = pygame.transform.rotate(self.image, -5)
        self.speedx = 0
        self.speedy = 0
        self.rect.x = 610
        self.rect.y = 300

    def update(self):
        print(self.rect.x)
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if any(keystate):
            if keystate[pygame.K_LEFT]:
                #self.image = self.image_left
                self.speedx = -1 * self.speed
            elif keystate[pygame.K_RIGHT]:
                #self.image = self.image_right
                self.speedx = self.speed
            if keystate[pygame.K_UP]:
                self.speedy = -1 * self.speed
            elif keystate[pygame.K_DOWN]:
                self.speedy = self.speed
        else:
            pass
            #self.image = self.image_forward
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.x > 1000:
            self.rect.x = 1000
        if self.rect.x < 50:
            self.rect.x = 50
        if self.rect.y < 200:
            self.rect.y = 200
        if self.rect.y > 600:
            self.rect.y = 600

class TrafficCar(Car):
    def __init__(self, dir, x, y=-100):
        if dir == 0 or dir == 1:
            super().__init__(random.randint(8,9), storage.cars_images[random.randint(0,3)], 1)
        elif dir == 2 or dir == 3:
            super().__init__(2, storage.cars_images[random.randint(0,3)], 0)
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.y += self.speed


class Traffic:
    def __init__(self):
        self.cars = []
        self.coords = [200, 390, 615, 800]
        self.last_update = pygame.time.get_ticks()
        self.speed = 3000

    def update(self):
        for car in self.cars:
            car.update()
            if car.rect.y > 800:
                del car
        now = pygame.time.get_ticks()
        if now - self.last_update > self.speed:
            self.last_update = now
            place = random.randint(0,1)
            car = TrafficCar(place,x=self.coords[place], y=random.randint(300,350)*-1)
            self.cars.append(car)
            all_cars.add(car)
            place = random.randint(2, 3)
            car = TrafficCar(place, x=self.coords[place], y=random.randint(300, 350) * -1)
            self.cars.append(car)
            all_cars.add(car)

    def draw(self):
        for car in self.cars:
            car.draw()

class Road(pygame.sprite.Sprite):
    def __init__(self, x=100, y=0):
        pygame.sprite.Sprite.__init__(self)
        self.image = storage.road_images[random.randint(0,9)]
        self.rect = pygame.Rect(x, y, self.image.get_width(), self.image.get_height())
        self.speed = 5

    def update(self):
        self.rect.y += self.speed
        if self.rect.

    def draw(self):
        screen.blit(self.image, self.rect)


class Roads:
    def __init__(self):
        self.roads = [Road(y=-700), Road(y=0), Road(y=700)]
        for road in self.roads:
            all_roads.add(road)

    def update(self):
        for road in range(len(self.roads)):
            if self.roads[road].rect.y > 1400 - self.roads[road].speed:
                del self.roads[road]
                road = Road(y=-700)
                self.roads.append(road)
                all_roads.add(road)
                break
        all_roads.update()

    def draw(self):
        all_roads.draw(screen)


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


class GameManager:
    def __init__(self):
        self.in_game = True
        self.in_pause = False

    def update(self):
        if self.in_game:
            player.update()
            traffic.update()
            roads.update()
        if self.in_pause:
            pass

    def draw(self):
        if self.in_game:
            roads.draw()
            traffic.draw()
            player.draw()
        if self.in_pause:
            pass


def animation(Entity, images, speed, endless):
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
            new_image = images[Entity.i]
            Entity.image = new_image


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


def load_images(name, count, scaleX, scaleY):
    array = []
    for i in range(count):
        array.append(load_image(str(name) + str(i + 1), scaleX, scaleY))
    return array

all_cars = pygame.sprite.Group()
all_roads = pygame.sprite.Group()
all_humans = pygame.sprite.Group()
storage = Storage()

player = Player()
traffic = Traffic()
roads = Roads()
game_manager = GameManager()

while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    game_manager.update()
    game_manager.draw()
    pygame.display.flip()
sys.exit()
