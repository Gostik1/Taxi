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




class Car:
    def __init__(self, image, speed):
        self.image = image
        self.rect = self.image.get_rect()
        self.speed = speed

    def draw(self):
        screen.blit(self.image, self.rect)
        #pygame.draw.rect(screen, GREEN, (self.rect.x, self.rect.y, self.image.get_width(),self.image.get_height()), 2)

class Player(Car):
    def __init__(self):
        super().__init__(storage.player_image, 7)
        self.image_forward = self.image
        self.image_left = pygame.transform.rotate(self.image, 5)
        self.image_right = pygame.transform.rotate(self.image, -5)
        self.speedx = 0
        self.speedy = 0
        self.rect.x = 610
        self.rect.y = 600

    def update(self):
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if any(keystate):
            if keystate[pygame.K_LEFT]:
                self.image = self.image_left
                self.speedx = -1 * self.speed
            elif keystate[pygame.K_RIGHT]:
                self.image = self.image_right
                self.speedx = self.speed
            if keystate[pygame.K_UP]:
                self.speedy = -1 * self.speed
            elif keystate[pygame.K_DOWN]:
                self.speedy = self.speed
        else:
            self.image = self.image_forward
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.x > 855:
            self.rect.x = 855
        if self.rect.x < 360:
            self.rect.x = 360
        if self.rect.y < 200:
            self.rect.y = 200
        if self.rect.y > 600:
            self.rect.y = 600

class TrafficCar(Car):
    def __init__(self, dir, x):
        if dir == 0:
            super().__init__(pygame.transform.rotate(storage.player_image,180), 6)
        elif dir == 1:
            super().__init__(storage.player_image, 2)
        self.rect.x = x
        self.rect.y = -100

    def update(self):
        self.rect.y += self.speed

class Traffic:
    def __init__(self):
        self.cars = [TrafficCar(1, 660)]
        self.directions = {0:[450, 560], 1:[666,770]}
        self.last_update = pygame.time.get_ticks()
        self.speed = 1000
        self.i = 0

    def update(self):
        for car in self.cars:
            car.update()
            if car.rect.y > 800:
                del car
        now = pygame.time.get_ticks()
        if now - self.last_update > self.speed:
            self.last_update = now
            self.i += 1
            dir = random.randint(0, 1)
            self.cars.append(TrafficCar(dir,self.directions[dir][random.randint(0,1)]))

    def draw(self):
        for car in self.cars:
            car.draw()

class Road:
    def __init__(self, x=370, y=0):
        self.image = storage.road_image
        self.rect = pygame.Rect(x, y, storage.road_rect.width, storage.road_rect.height)
        self.speed = 5

    def update(self):
        self.rect.y += self.speed

    def draw(self):
        screen.blit(self.image, self.rect)


class Roads:
    def __init__(self):
        self.roads = [Road(y=-520), Road(y=0), Road(y=520)]

    def update(self):
        for road in range(len(self.roads)):
            if self.roads[road].rect.y > 1020:
                del self.roads[road]
                self.roads.append(Road(y=-520))
                break
            self.roads[road].update()

    def draw(self):
        for road in self.roads:
            road.draw()


class Storage:
    def __init__(self):
        self.player_image = load_image("player", 46, 102)

        self.road_image = load_image("road", 520, 520)
        self.road_rect = self.road_image.get_rect()

        self.grass_image = load_image("grass", WIDTH, HEIGHT)
        self.grass_rect = self.grass_image.get_rect()


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
            screen.blit(storage.grass_image, storage.grass_rect)
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
