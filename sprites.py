from config import *


class Block(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()

        self.game = game
        self._layer = BLOCKS_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE

        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.image = self.game.stone_sprite_sheet.get_image(96, 96, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)


class Ground(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()

        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE

        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.image = self.game.terrain_sprite_sheet.get_image(32, 64, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)


class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE

        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.x_change = 0
        self.y_change = 0

        self.scale = 35
        self.image = self.game.player_sprite_sheet.get_image(0, 64, self.width, self.height)
        self.image = pygame.transform.scale(self.image, (self.scale, self.scale))
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)

        self.direction = "RIGHT"

    def update(self):
        self.move()
        self.rect.x = self.rect.x + self.x_change
        self.rect.y = self.rect.y + self.y_change

        self.x_change = 0
        self.y_change = 0
        print(self.x_change)

    def move(self):
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_a]:
            self.x_change = self.x_change - PLAYER_STEPS
            self.direction = "LEFT"
        elif pressed[pygame.K_d]:
            self.x_change = self.x_change + PLAYER_STEPS
            self.direction = "RIGHT"
        elif pressed[pygame.K_w]:
            self.y_change = self.y_change - PLAYER_STEPS
            self.direction = "UPP"
        elif pressed[pygame.K_s]:
            self.y_change = self.y_change + PLAYER_STEPS
            self.direction = "DOWN"

class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE

        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.x_change = 0
        self.y_change = 0

        self.scale = 35
        self.image = self.game.enemy_sprite_sheet.get_image(32, 64, self.width, self.height)
        self.image = pygame.transform.scale(self.image, (self.scale, self.scale))
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
