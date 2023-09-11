# IMG BACKLINK <a href="https://www.flaticon.com/free-icons/cerberus" title="cerberus icons">Cerberus icons created by max.icons - Flaticon</a>
# <a href="https://www.flaticon.com/free-icons/knight" title="knight icons">Knight icons created by Freepik - Flaticon</a>
# <a href="https://www.flaticon.com/free-icons/info" title="info icons">Info icons created by Freepik - Flaticon</a>
# MUSIC BACKLINK https://www.fiftysounds.com/

import pygame, random

pygame.init()

WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 900
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Monster Wrangler")
icon = pygame.image.load("sword.png")
pygame.display.set_icon(icon)

FPS = 60
clock = pygame.time.Clock()


# Define classes
class Game:
    def __init__(self, player, monster_group):
        # Set game values
        self.score = 0
        self.round_number = 0

        self.round_time = 0
        self.frame_count = 0

        self.player = player
        self.monster_group = monster_group

        # Set the sounds and music
        self.next_level_sound = pygame.mixer.Sound("victory.mp3")
        self.game_over_sound = pygame.mixer.Sound("game_over.mp3")

        # Set a font
        self.font = pygame.font.Font("Maputo.ttf", 24)

        # Set images
        self.background_image = pygame.image.load("map3.jfif")
        self.background_image_rect = self.background_image.get_rect()
        self.background_image_rect.topleft = (0, 100)
        # This images list cooresponds to monster_type attribute 0 - snake, 1 - dragon, 2 - cerberus, 3 - hydra
        self.target_monster_images = [
            pygame.image.load("snake.png"),
            pygame.image.load("dragon.png"),
            pygame.image.load("cerberus.png"),
            pygame.image.load("hydra.png"),
        ]
        self.target_monster_type = random.randint(0, 3)
        self.target_monster_image = self.target_monster_images[self.target_monster_type]

        self.target_monster_rect = self.target_monster_image.get_rect()
        self.target_monster_rect.centerx = WINDOW_WIDTH // 2
        self.target_monster_rect.top = 30

        self.info = pygame.image.load("info.png")
        self.info_rect = self.info.get_rect()
        self.info_rect.bottomleft = (20, WINDOW_HEIGHT - 30)

    def draw(self):
        # Set colors
        WHITE = (255, 255, 255)
        GREEN = (87, 201, 155)  # snake
        RED = (255, 60, 76)  # dragon
        PURPLE = (172, 136, 220)  # cerberus
        GREY = (137, 128, 130)  # hydra

        # Add the monster colors to a list where the index of the color matches target_monster_image
        colors = [GREEN, RED, PURPLE, GREY]
        # Set text
        catch_text = self.font.render("Current catch:", True, WHITE)
        catch_rect = catch_text.get_rect()
        catch_rect.centerx = WINDOW_WIDTH // 2
        catch_rect.top = 5

        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        score_rect = score_text.get_rect()
        score_rect.topleft = (5, 5)

        lives_text = self.font.render(f"Lives: {self.player.lives}", True, WHITE)
        lives_rect = lives_text.get_rect()
        lives_rect.topleft = (5, 35)

        round_text = self.font.render(
            f"Current round: {self.round_number}", True, WHITE
        )
        round_rect = round_text.get_rect()
        round_rect.topleft = (5, 65)

        time_text = self.font.render(f"Round time: {self.round_time}", True, WHITE)
        time_rect = time_text.get_rect()
        time_rect.topright = (WINDOW_WIDTH - 10, 5)

        warp_text = self.font.render(f"Warps: {self.player.warps}", True, WHITE)
        warp_rect = warp_text.get_rect()
        warp_rect.topright = (WINDOW_WIDTH - 10, 35)

        # Blit the HUD
        display_surface.blit(catch_text, catch_rect)
        display_surface.blit(score_text, score_rect)
        display_surface.blit(round_text, round_rect)
        display_surface.blit(lives_text, lives_rect)
        display_surface.blit(time_text, time_rect)
        display_surface.blit(warp_text, warp_rect)
        display_surface.blit(self.info, self.info_rect)

        display_surface.blit(self.target_monster_image, self.target_monster_rect)

        pygame.draw.rect(
            display_surface,
            colors[self.target_monster_type],
            (WINDOW_WIDTH // 2 - 32, 30, 64, 64),
            2,
        )
        pygame.draw.rect(
            display_surface,
            colors[self.target_monster_type],
            (0, 100, WINDOW_WIDTH, WINDOW_HEIGHT - 200),
            10,
        )

    def informations(self):
        # Get game informations and rules
        if self.player.rect.colliderect(self.info_rect):
            pygame.draw.rect(display_surface, (0, 0, 0), (20, 670, 850, 110), 0, 10)
            game_rules = self.font.render(
                "Catch the 'Current catch' monster and avoid the rest.",
                True,
                (255, 255, 255),
            )
            game_rules_rect = game_rules.get_rect()
            game_rules_rect.topleft = (40, 695)

            warp_rules = self.font.render(
                "If you got 'Warps' to use press SPACE and go back to safe space.",
                True,
                (255, 255, 255),
            )
            warp_rules_rect = warp_rules.get_rect()
            warp_rules_rect.topleft = (40, 730)

            display_surface.blit(game_rules, game_rules_rect)
            display_surface.blit(warp_rules, warp_rules_rect)

    def update(self):
        # Count the time
        self.frame_count += 1
        if self.frame_count == FPS:
            self.round_time += 1
            self.frame_count = 0

        self.check_collisions()
        self.informations()

    def check_collisions(self):
        # Check for collision between player and an individual monster
        collided_monster = pygame.sprite.spritecollideany(
            self.player, self.monster_group
        )
        if collided_monster:
            if collided_monster.type == self.target_monster_type:
                self.score += 100 * self.round_number
                # Remove coughted monster
                collided_monster.remove(self.monster_group)
                if self.monster_group:
                    # There are more monster to catch
                    self.player.hit.play()
                    self.choose_new_target()
                else:
                    # The round is complite
                    self.next_level_sound.play()
                    self.player.reset()
                    self.start_new_round()
            # Cought wrong monster
            else:
                self.player.die.play()
                self.player.lives -= 1
                if self.player.lives <= 0:
                    self.game_over_sound.play()
                    self.pause_game(
                        f"Final score: {self.score}.", "Press 'Enter' to play again"
                    )
                    self.rest_game()
                self.player.reset()

    def change_background(self):
        # Add background images
        background_images = [
            pygame.image.load("map3.jfif"),
            pygame.image.load("map4.jfif"),
            pygame.image.load("map5.jfif"),
            pygame.image.load("map6.jfif"),
            pygame.image.load("map7.jfif"),
            pygame.image.load("map8.jfif"),
            pygame.image.load("map9.jfif"),
            pygame.image.load("map10.jfif"),
            pygame.image.load("map11.jfif"),
            pygame.image.load("map12.jfif"),
            pygame.image.load("map13.jfif"),
            pygame.image.load("map14.jfif"),
            pygame.image.load("map15.jfif"),
            pygame.image.load("map17.jfif"),
            pygame.image.load("map18.jfif"),
        ]

        random_img_pos = random.randint(0, 10)
        self.background_image = background_images[random_img_pos]

    def start_new_round(self):
        # Populate the board with the monsters
        # Provide a score bonus based on how quicly the raound was finished
        self.score += int(10000 * self.round_number / (1 + self.round_time))
        self.round_number += 1
        self.change_background()

        self.round_time = 0
        self.frame_count = 0
        self.player.warps += 1

        # Remove any remaining monster from a game reset
        for monster in self.monster_group:
            self.monster_group.remove(monster)

        # Add monsters to the monster group
        for i in range(self.round_number):
            self.monster_group.add(
                Monster(
                    random.randint(0, WINDOW_WIDTH - 64),
                    random.randint(100, WINDOW_HEIGHT - 264),
                    self.target_monster_images[0],
                    0,
                )
            )
            self.monster_group.add(
                Monster(
                    random.randint(0, WINDOW_WIDTH - 64),
                    random.randint(100, WINDOW_HEIGHT - 264),
                    self.target_monster_images[1],
                    1,
                )
            )
            self.monster_group.add(
                Monster(
                    random.randint(0, WINDOW_WIDTH - 64),
                    random.randint(100, WINDOW_HEIGHT - 264),
                    self.target_monster_images[2],
                    2,
                )
            )
            self.monster_group.add(
                Monster(
                    random.randint(0, WINDOW_WIDTH - 64),
                    random.randint(100, WINDOW_HEIGHT - 264),
                    self.target_monster_images[3],
                    3,
                )
            )

        self.choose_new_target()

    def choose_new_target(self):
        target_monster = random.choice(
            self.monster_group.sprites()
        )  # Choose random from Group of sprites
        self.target_monster_type = target_monster.type
        self.target_monster_image = target_monster.image

    def pause_game(self, main_text, sub_text):
        global running
        # Set color
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)
        # Create the main pausse text
        main_text = self.font.render(main_text, True, WHITE)
        main_rect = main_text.get_rect()
        main_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50)

        sub_text = self.font.render(sub_text, True, WHITE)
        sub_rect = sub_text.get_rect()
        sub_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 40)

        # Display the pause text
        display_surface.fill(BLACK)
        display_surface.blit(main_text, main_rect)
        display_surface.blit(sub_text, sub_rect)
        pygame.display.update()

        # Pause the game
        is_paused = True
        while is_paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_paused = False
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        is_paused = False

    def rest_game(self):
        self.score = 0
        self.round_number = 0
        self.round_time = 0
        self.frame_count = 0

        self.player.lives = 5
        self.player.warps = 2
        self.player.reset()

        self.start_new_round()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("knight.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = WINDOW_WIDTH // 2
        self.rect.bottom = WINDOW_HEIGHT

        self.lives = 5
        self.warps = 2
        self.velocity = 8

        self.hit = pygame.mixer.Sound("hit.mp3")
        self.reload = pygame.mixer.Sound("reload.mp3")
        self.die = pygame.mixer.Sound("die.mp3")

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.velocity
        if keys[pygame.K_RIGHT] and self.rect.right < WINDOW_WIDTH:
            self.rect.x += self.velocity
        if keys[pygame.K_UP] and self.rect.top > 100:
            self.rect.y -= self.velocity
        if keys[pygame.K_DOWN] and self.rect.bottom < WINDOW_HEIGHT - 100:
            self.rect.y += self.velocity

    def warp(self):
        if self.warps > 0:
            self.warps -= 1
            self.reload.play()
            self.rect.bottom = WINDOW_HEIGHT

    def reset(self):
        self.rect.centerx = WINDOW_WIDTH // 2
        self.rect.bottom = WINDOW_HEIGHT


class Monster(pygame.sprite.Sprite):
    def __init__(self, x, y, image, monster_type):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        # Monster type is an int 0 - snake, 1 - dragon, 2 - cerberus, 3 - hydra
        self.type = monster_type

        # Set random motion
        self.dx = random.randint(-1, 1)  # sprobowac od -1 do 1
        self.dy = random.randint(-1, 1)
        self.velocity = random.randint(1, 3)

    def update(self):
        self.rect.x += self.dx * self.velocity
        self.rect.y += self.dy * self.velocity
        if self.rect.left <= 0 or self.rect.right >= WINDOW_WIDTH:
            self.dx *= -1
        if self.rect.top <= 100 or self.rect.bottom >= WINDOW_HEIGHT - 100:
            self.dy *= -1


running = True

my_player_group = pygame.sprite.Group()
my_player = Player()
my_player_group.add(my_player)

my_monsters_group = pygame.sprite.Group()

my_game = Game(my_player, my_monsters_group)
my_game.pause_game("Monster Wrangler", "Press 'Enter' to play")
my_game.start_new_round()

# Main game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Player wants to warp
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                my_player.warp()

    display_surface.fill((0, 0, 0))
    display_surface.blit(my_game.background_image, my_game.background_image_rect)

    my_monsters_group.update()
    my_monsters_group.draw(display_surface)

    my_player_group.update()
    my_player_group.draw(display_surface)

    my_game.update()
    my_game.draw()  # Class Game() method

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
