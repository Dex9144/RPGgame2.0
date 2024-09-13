from config import *
import random
import math
from animate import *
from typing import Union


class Entity(pygame.sprite.Sprite):
    def __init__(self, game, x, y, layer, sheet, sheet_pos):
        super().__init__()
        self._layer = layer

        """ Get our main game, and setup the layer"""
        self.game = game
        self.scale = 40

        self.groups = self.game.sprites
        self.add(self.groups)

        self.scale = TILE_SIZE  # DELETE SCALER

        """ Set up the size and pos"""
        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = CROP_SIZE
        self.height = CROP_SIZE

        """ Set the sprite sheet"""
        self.sheet = sheet

        """ Get image from sheet, set up the cords for rect"""
        self.image = self.sheet.get_image(sheet_pos[0], sheet_pos[1], self.width, self.height)
        self.image = pygame.transform.scale(self.image, (self.scale, self.scale))  # DELETE SCALER
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)

    def collide_with(self, group):
        for sprite in group:
            if self.rect.colliderect(sprite.rect):
                return sprite

        return None


class Player(Entity, pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        sprite_sheet = game.stone_sprite_sheet  # What sheet to use
        sprite_sheet_pos = (96, 96)  # Crop cords
        super().__init__(game, x, y, PLAYER_LAYER, sprite_sheet, sprite_sheet_pos)  # Construct the player

        self.direction = "RIGHT"  # Start direction
        self.is_moving = False  # Is not moving at start

        self.x_change = 0  # Start change x
        self.y_change = 0  # Start change y
        self.scale = 40
        self.animation_counter = 0  # Start counter for animation

        # ALL THE FRAMES, PLANS: STORE IT IN OTHER FILE
        self.right_animation = Animate([
            self.game.player_sprite_sheet.get_image(0, 0, self.width, self.height),
            self.game.player_sprite_sheet.get_image(32, 0, self.width, self.height),
            self.game.player_sprite_sheet.get_image(64, 0, self.width, self.height),
        ])
        self.left_animation = Animate([
            self.game.player_sprite_sheet.get_image(0, 32, self.width, self.height),
            self.game.player_sprite_sheet.get_image(32, 32, self.width, self.height),
            self.game.player_sprite_sheet.get_image(64, 32, self.width, self.height),
        ])
        self.right_idle_animation = Animate([
            self.game.player_sprite_sheet.get_image(0, 64, self.width, self.height),
            self.game.player_sprite_sheet.get_image(32, 64, self.width, self.height)
        ])
        self.left_idle_animation = Animate([
            self.game.player_sprite_sheet.get_image(0, 96, self.width, self.height),
            self.game.player_sprite_sheet.get_image(32, 96, self.width, self.height)
        ])

        # Making the sprite little bigger bc of small image

    def update(self):
        """Setting up methods that need to be run every frame"""

        self.move()
        self.update_movement()
        self.collision()

    def update_movement(self):
        """Makes the player move"""
        # CHANGE THE SPRITES POS BASED ON CHANGE
        self.rect.x = self.rect.x + self.x_change
        self.rect.y = self.rect.y + self.y_change
        # to not accelerate set back the change to 0 every frame
        self.x_change = 0
        self.y_change = 0

    def move(self):
        """Handling players inputs"""
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_a]:
            self.x_change = self.x_change - PLAYER_STEPS
            self.direction = "LEFT"
            self.is_moving = True
        elif pressed[pygame.K_d]:
            self.x_change = self.x_change + PLAYER_STEPS
            self.direction = "RIGHT"
            self.is_moving = True
        elif pressed[pygame.K_w]:
            self.y_change = self.y_change - PLAYER_STEPS
            self.direction = "UP"
            self.is_moving = True
        elif pressed[pygame.K_s]:
            self.y_change = self.y_change + PLAYER_STEPS
            self.direction = "DOWN"
            self.is_moving = True
        else:
            self.is_moving = False

    def animate(self):
        """Animates the character when moving"""
        dt = 0.2  # Lower fl, more time between frame
        dt_idle = 0.1  # idle animation uses only two frames, so I set more time
        if self.direction == "RIGHT":
            if self.is_moving:
                self.right_animation.update_animation(dt)
                self.image = self.right_animation.textures[self.right_animation.i]  # Set the current image
                self.image = pygame.transform.scale(self.image, (self.scale, self.scale))
            else:
                self.right_idle_animation.update_animation(dt_idle)
                self.image = self.right_idle_animation.textures[self.right_idle_animation.i]  # Set the current image
                self.image = pygame.transform.scale(self.image, (self.scale, self.scale))
        if self.direction == "LEFT":
            if self.is_moving:
                self.left_animation.update_animation(dt)
                self.image = self.left_animation.textures[self.left_animation.i]  # Set the current image
                self.image = pygame.transform.scale(self.image, (self.scale, self.scale))
            else:
                self.left_idle_animation.update_animation(dt_idle)
                self.image = self.left_idle_animation.textures[self.left_idle_animation.i]  # Set the current image
                self.image = pygame.transform.scale(self.image, (self.scale, self.scale))

    def collision(self):
        """Makes that you cant clip trough blocks"""
        pressed = pygame.key.get_pressed()

        block_collide = self.collide_with(self.game.blocks)
        enemy_collide = self.collide_with(self.game.enemies)
        if block_collide or enemy_collide:
            self.game.camera_collide = True

            if self.direction == "LEFT":
                self.rect.x += PLAYER_STEPS
            elif self.direction == "RIGHT":
                self.rect.x -= PLAYER_STEPS
            elif self.direction == "UP":
                self.rect.y += PLAYER_STEPS
            elif self.direction == "DOWN":
                self.rect.y -= PLAYER_STEPS

        else:
            self.game.camera_collide = False


class Block(Entity):
    def __init__(self, game, x, y):
        sprite_sheet = game.stone_sprite_sheet  # What sheet to use
        sprite_sheet_pos = (96, 96)
        super().__init__(game, x, y, BLOCKS_LAYER, sprite_sheet, sprite_sheet_pos)  # Construct the block
        self.groups = game.sprites, game.blocks  # Add to both groups
        self.add(*self.groups)  # Add the block to the specified group0s


class Grass(Entity):
    def __init__(self, game, x, y):
        sprite_sheet = game.terrain_sprite_sheet  # What sheet to use
        random_poses = [(32, 0), (64, 64), (32, 96), (96, 64), (32, 64)]
        sprite_sheet_pos = random.choice(random_poses)  # Crop cords
        super().__init__(game, x, y, GROUND_LAYER, sprite_sheet, sprite_sheet_pos)  # Construct the block


class Path(Entity):
    def __init__(self, game, x, y):
        sprite_sheet = game.terrain_sprite_sheet
        sprite_sheet_pos = (0, 128)
        super().__init__(game, x, y, GROUND_LAYER, sprite_sheet, sprite_sheet_pos)


class Enemy(Entity):
    def __init__(self, game, x, y):
        sprite_sheet = game.enemy_sprite_sheet  # What sheet to use
        sprite_sheet_pos = (32, 64)  # Crop cords
        super().__init__(game, x, y, ENEMY_LAYER, sprite_sheet, sprite_sheet_pos)  # Construct the
        self.groups = game.sprites, game.enemies
        self.add(*self.groups)

        self.directions = ["LEFT", "RIGHT", "DOWN", "UPP"]
        self.direction = random.choice(self.directions)
        self.x_change = 0  # Start change x
        self.y_change = 0  # Start change y

        self.max_steps = 30
        self.stall_steps = 80
        self.current_steps = 0

        self.state = "moving"

    def move(self):
        if self.state == "moving":

            if self.direction == "LEFT":
                self.x_change = self.x_change - ENEMY_STEPS
                self.current_steps += 1
            elif self.direction == "RIGHT":
                self.x_change = self.x_change + ENEMY_STEPS
                self.current_steps += 1
            elif self.direction == "UPP":
                self.y_change = self.y_change - ENEMY_STEPS
                self.current_steps += 1
            elif self.direction == "DOWN":
                self.y_change = self.y_change + ENEMY_STEPS
                self.current_steps += 1

        elif self.state == "stalling":

            self.current_steps += 1
            if self.current_steps == self.stall_steps:
                self.state = "moving"
                self.current_steps = 0

    def update_movement(self):
        # CHANGE THE SPRITES POS BASED ON CHANGE
        self.rect.x = self.rect.x + self.x_change
        self.rect.y = self.rect.y + self.y_change
        # to not accelerate set back the change to 0 every frame
        self.x_change = 0
        self.y_change = 0

        if self.current_steps >= self.max_steps:
            if self.state != "stalling":
                directions = self.directions.copy()
                remove_dir = self.direction
                if remove_dir in directions:
                    directions.remove(remove_dir)
                    self.direction = random.choice(directions)
                    self.stall_steps = random.randint(40, 180)
                self.state = "stalling"
                self.current_steps = 0

    def update(self):
        self.update_movement()
        self.move()
        self.collision()

    def collision(self):
        """Makes that you cant clip trough blocks"""
        block_collide = self.collide_with(self.game.blocks)
        player_collide = self.collide_with(self.game.players)
        if block_collide or player_collide:
            if self.direction == "LEFT":
                self.rect.x += ENEMY_STEPS
                self.direction = "RIGHT"
            elif self.direction == "RIGHT":
                self.rect.x -= ENEMY_STEPS
                self.direction = "LEFT"
            elif self.direction == "UP":
                self.rect.y += ENEMY_STEPS
                self.direction = "DOWN"
            elif self.direction == "DOWN":
                self.rect.y -= ENEMY_STEPS
                self.direction = "UP"
