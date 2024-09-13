import pygame
from config import *
from better_sprites import *
import sys


class SpriteSheet:
    def __init__(self, path):
        self.spritesheet = pygame.image.load(path).convert()  # Loading the whole sprite sheet

    def get_image(self, x, y, width, height):  # Cropping the picture by the cord from the sprite sheet
        sprite = pygame.Surface([width, height])
        sprite.blit(self.spritesheet, (0, 0), (x, y, width, height))
        sprite.set_colorkey(WHITE)

        return sprite


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True

        self.terrain_sprite_sheet = SpriteSheet("Sheets/Terrain/TX Tileset Grass.png")
        self.props_sprite_sheet = SpriteSheet("Sheets/Terrain/TX Props.png")
        self.stone_sprite_sheet = SpriteSheet("Sheets/Terrain/TX Tileset Stone Ground.png")

        self.player_sprite_sheet = SpriteSheet("Sheets/Player/TX Player.png")
        self.enemy_sprite_sheet = SpriteSheet("Sheets/Enemy/TX monsters.png")
        """
        Grass - 32, 64
        Stone - 160, 480
        Stone wall - 96, 96
        """

        self.camera_collide = False

    def create_tile_map(self):
        for i, row in enumerate(tile_map):
            for j, column in enumerate(row):
                Grass(self, j, i)
                if column == "B":
                    Block(self, j, i)
                if column == "P":
                    Player(self, j, i)
                if column == "E":
                    Enemy(self, j, i)
                if column == "p":
                    Path(self, j, i)

    def create(self):
        self.sprites = pygame.sprite.LayeredUpdates()  # Create all the sprites with the layerd setting

        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.players = pygame.sprite.LayeredUpdates()

        self.create_tile_map()  # Create the tile map

    def update(self):
        self.sprites.update()  # Update all sprites

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def draw(self):
        self.screen.fill(BLACK)
        self.sprites.draw(self.screen)  # Draw every sprite
        self.clock.tick(FPS)  # Set the fps to the game
        pygame.display.update()  # Update display

    def camera(self):
        if not self.camera_collide:
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_a]:
                for i, sprite in enumerate(self.sprites):
                    sprite.rect.x += PLAYER_STEPS
            elif pressed[pygame.K_d]:
                for i, sprite in enumerate(self.sprites):
                    sprite.rect.x -= PLAYER_STEPS
            elif pressed[pygame.K_w]:
                for i, sprite in enumerate(self.sprites):
                    sprite.rect.y += PLAYER_STEPS
            elif pressed[pygame.K_s]:
                for i, sprite in enumerate(self.sprites):
                    sprite.rect.y -= PLAYER_STEPS

    def main(self):
        while self.running:
            self.update()  # Do not mess up the order
            self.camera()
            self.draw()
            self.events()


game = Game()
game.create()
while game.running:
    game.main()

pygame.quit()
sys.exit()
