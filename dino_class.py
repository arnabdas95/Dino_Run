#dino game object class
import pygame, random
CANVAS_WIDTH = 950
CANVAS_HEIGHT = 600

class Dino:
    def __init__(self):
        self.is_running = True
        self.is_jumping = False
        self.is_leaning = False
        self.gravity = 0.1
        self.jump_count = 10
        self.dino_foot_flap = 20
        self.dino_pos_x = 45
        self.dino_pos_y = 300

        self.dino_image = pygame.image.load("assets/images/left11.png").convert_alpha()
        self.dino_r1_image = pygame.image.load("assets/images/left11.png").convert_alpha()
        self.dino_r2_image = pygame.image.load("assets/images/right11.png").convert_alpha()
        self.dino_d_image = pygame.image.load("assets/images/ducking11.png").convert_alpha()

        self.rect = self.dino_image.get_rect()
        self.rect.x = self.dino_pos_x
        self.rect.y = self.dino_pos_y

    def dino_jump(self):
        if self.jump_count >= -10:
            self.neg_value = 1
            if self.jump_count < 0:
                self.neg_value = -1
            self.rect.y -= (self.jump_count ** 2) * self.gravity * self.neg_value
            self.jump_count -= .3
        else:
            self.rect.y += self.gravity
            self.gravity += .8
            if self.rect.y >= self.dino_pos_y:
                self.is_jumping = False
                self.is_running = True
                self.jump_count = 10
                self.gravity = 0.1
                self.rect.y = self.dino_pos_y

    def dino_lean(self):
        self.rect.y = 400

    def dino_lean_up(self):
        self.is_jumping = False
        self.is_running = True
        self.is_leaning = False
        self.rect.y = self.dino_pos_y

    def display_dino(self, screen):
        if self.is_running:
            if self.dino_foot_flap == 0:
                self.dino_foot_flap = 80
            if self.dino_foot_flap < 40:
                screen.blit(self.dino_r1_image, self.rect)
            else:
                screen.blit(self.dino_r2_image, self.rect)
            self.dino_foot_flap -= 1
        elif self.is_leaning:
            screen.blit(self.dino_d_image, self.rect)
        else:
            screen.blit(self.dino_r2_image, self.rect)

    def collition_detection(self, x):
        global GAME_STATE
        if pygame.Rect.colliderect(self.rect, x):
            GAME_OVER_SOUND = pygame.mixer.Sound("assets/game_sounds/game_over.wav")
            pygame.mixer.Sound.play(GAME_OVER_SOUND)
            return 'game_over'
        return 'active'


class Cactus:
    def __init__(self):
        self.cactus_pos_x = CANVAS_WIDTH + random.randint(-250, 50)
        self.cactus_pos_y = CANVAS_HEIGHT - 195
        self.cactus_speed = 3.5
        self.cactus_random_image_number = random.randint(0, 5)
        self.cactus_image = pygame.image.load(f"assets/images/{self.cactus_random_image_number}.png").convert_alpha()
        self.rect = self.cactus_image.get_rect()
        self.rect.x = self.cactus_pos_x
        self.rect.y = self.cactus_pos_y

    def update(self):
        self.rect.x -= self.cactus_speed

    def display(self, screen):
        screen.blit(self.cactus_image, self.rect)


class Bird:
    def __init__(self):
        self.bird_pos_x = CANVAS_WIDTH + random.randint(-400, 150)
        self.bird_pos_y = CANVAS_HEIGHT - 345
        self.bird_speed = 3
        self.bird_random_image_number = random.choice([6, 8])
        self.bird_up_image = pygame.image.load(f"assets/images/{self.bird_random_image_number}.png").convert_alpha()
        self.bird_down_image = pygame.image.load(
            f"assets/images/{self.bird_random_image_number + 1}.png").convert_alpha()
        self.rect = self.bird_up_image.get_rect()
        self.rect.x = self.bird_pos_x
        self.rect.y = self.bird_pos_y
        self.bird_flap = 100

    def update(self):
        self.rect.x -= self.bird_speed

    def display(self, screen):
        if self.bird_flap == 0:
            self.bird_flap = 100
        if self.bird_flap < 50:
            screen.blit(self.bird_up_image, self.rect)
        else:
            screen.blit(self.bird_down_image, self.rect)
        self.bird_flap -= 1


class Clouds:
    def __init__(self, screen):
        self.screen = screen
        self.cloud_x = 740
        self.cloud_y = 30
        self.cloud_image_1 = pygame.image.load("assets/images/c1.png").convert_alpha()
        self.cloud_image_2 = pygame.image.load("assets/images/c2.png").convert_alpha()
        self.choose = random.randint(1, 2)

    def cloud_flight(self):

        if self.cloud_x <= 0:
            self.cloud_x = 800
            self.choose = random.randint(1, 2)

        if self.choose == 1:
            self.cloud_image_2 = pygame.image.load("assets/images/c2.png").convert_alpha()
        else:
            self.cloud_image_2 = pygame.image.load("assets/images/c1.png").convert_alpha()
        self.cloud_x -= 5

    def display_cloud(self):
        self.screen.blit(self.cloud_image_2, (self.cloud_x, self.cloud_y))
