import pygame as pg
from PIL import Image, ImageDraw, ImageFont
from npc import *
from settings import *




class ObjectRenderer:
    def __init__(self, game):

        #self.font = ImageFont.truetype("arial.ttf", 28, encoding="unic")
        self.game = game
        self.screen = game.screen
        self.wall_textures = self.load_wall_textures()
        self.sky_image = self.get_texture('resources/textures/sky.png', (WIDTH, HALF_HEIGHT))
        self.sky_offset = 0
        self.blood_screen = self.get_texture('resources/textures/blood_screen.png', RES)
        self.digit_size = 70
        self.digit_images = [self.get_texture(f'resources/textures/digits/{i}.png', [self.digit_size] * 2)
                             for i in range(12)]
        self.digits = dict(zip(map(str, range(12)), self.digit_images))
        self.game_over_image = self.get_texture('resources/textures/game_over.png', RES)
        self.win_image = self.get_texture('resources/textures/win.png', RES)

    def draw(self):
        self.draw_background()
        self.render_game_objects()
        self.draw_player_health()
        self.draw_kill_rate()


    def win(self):
        self.screen.blit(self.win_image, (0, 0))

    def game_over(self):
        self.screen.blit(self.game_over_image, (0, 0))

    def draw_player_health(self):
        health = str(self.game.player.health)
        health_width = len(health) * self.digit_size
        health_x = (1600 - health_width) // 2  # Calculate the x-coordinate for centering health digits
        health_y = 20  # Set the desired y-coordinate for the health display

        for i, char in enumerate(health):
            digit_x = health_x + i * self.digit_size
            # Check if the digit goes out of the screen boundaries
            if digit_x + self.digit_size > 1600:
                break  # Exit the loop if it goes out of bounds
            self.screen.blit(self.digits[char], (digit_x, health_y))  # Adjusted x and y coordinates

        # Position the '10' indicator at the end of the health digits
        self.screen.blit(self.digits['10'], (health_x + health_width, health_y))

    def draw_kill_rate(self):
        kill_rate = str(self.game.player.kill_count)
        kill_rate_width = len(kill_rate) * self.digit_size
        kill_rate_x = 100  # Calculate the x-coordinate for centering kill rate digits
        kill_rate_y = 20  # Set the desired y-coordinate for the kill rate display

        for i, char in enumerate(kill_rate):
            digit_x = kill_rate_x + i * (self.digit_size)
            # Check if the digit goes out of the screen boundaries
            if digit_x + self.digit_size > 1600:
                break  # Exit the loop if it goes out of bounds
            self.screen.blit(self.digits[char], (digit_x, kill_rate_y))  # Adjusted x and y coordinates

        # Position the '11' indicator at the end of the kill rate digits
        self.screen.blit(self.digits['11'], (kill_rate_x-70,kill_rate_y))

    def player_damage(self):
        self.screen.blit(self.blood_screen, (0, 0))

    def draw_background(self):
        self.sky_offset = (self.sky_offset + 4.5 * self.game.player.rel) % WIDTH
        self.screen.blit(self.sky_image, (-self.sky_offset, 0))
        self.screen.blit(self.sky_image, (-self.sky_offset + WIDTH, 0))
        # floor
        pg.draw.rect(self.screen, FLOOR_COLOR, (0, HALF_HEIGHT, WIDTH, HEIGHT))

    def render_game_objects(self):
        list_objects = sorted(self.game.raycasting.objects_to_render, key=lambda t: t[0], reverse=True)
        for depth, image, pos in list_objects:
            self.screen.blit(image, pos)

    @staticmethod
    def get_texture(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        texture = pg.image.load(path).convert_alpha()
        return pg.transform.scale(texture, res)

    def load_wall_textures(self):
        return {
            1: self.get_texture('resources/textures/1.png'),
            2: self.get_texture('resources/textures/2.png'),
            3: self.get_texture('resources/textures/3.png'),
            4: self.get_texture('resources/textures/4.png'),
            5: self.get_texture('resources/textures/5.png'),
        }


