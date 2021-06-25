import pygame, sys, random
import dino_class

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.font.init()
FPS = 120
CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
screen = pygame.display.set_mode((CANVAS_WIDTH, CANVAS_HEIGHT))
ICON = pygame.image.load('assets/images/dino_icon.png')
pygame.display.set_icon(ICON)
pygame.display.set_caption('DINO RUN GAME')
BACKGROUND = pygame.image.load("assets/images/day.png").convert()
GROUND = pygame.image.load("assets/images/day_foreground.png").convert()
INTRO = pygame.image.load("assets/images/intro.png").convert()
BIRD_DELAY_SPEED = 700
GAME_STATE = 'ready'
GAME_FONT = pygame.font.Font("freesansbold.ttf", 20)
DUCK = pygame.mixer.Sound("assets/game_sounds/hish.wav")
JUMP = pygame.mixer.Sound("assets/game_sounds/jump.wav")
pygame.mixer.music.load("assets/game_sounds/bgm.mp3")
pygame.mixer.music.play(loops=-1)
CHANGE_BCK = pygame.USEREVENT + 1
ACTIVE_MOVEMENT = pygame.USEREVENT + 2
CLOUD_PLAY = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_BCK, 15000)
pygame.time.set_timer(ACTIVE_MOVEMENT, 8)
pygame.time.set_timer(CLOUD_PLAY, 10000)

ground_x = 0
enemy = []
object = ''
bg_fg = 1
score = 0


# On game start clicking this button will start playing
def start_button():
    global GAME_STATE, score, bg_fg
    mx, my = pygame.mouse.get_pos()
    if 351 <= mx <= 448 and 354 <= my <= 440:
        score = 0
        pygame.mixer.Sound.play(JUMP)
        GAME_STATE = 'active'

    # check the click of mute button
    if 33 <= mx <= 71 and 539 <= my <= 578:
        if pygame.mixer.music.get_busy():
            pygame.mixer.Sound.play(JUMP)
            pygame.mixer.music.stop()
    # check the click of sound button
    if 733 <= mx <= 773 and 538 <= my <= 581:
        pygame.mixer.Sound.play(JUMP)
        pygame.mixer.music.play(loops=-1)


def ready_state():
    display_intro()


# main game starts
def active_state():
    global GAME_STATE, score, scores
    disply_background()
    disply_running_foreground()
    score_update()
    cloud.display_cloud()
    dino_object.display_dino(screen)

    ememy_create()
    if len(enemy) != 0:
        enemy_update()
        display_enemy()
        GAME_STATE = dino_object.collition_detection(object)

    if dino_object.is_jumping:
        dino_object.dino_jump()

    if dino_object.is_leaning:
        dino_object.dino_lean()


def game_over():
    global enemy, score, bg_fg

    enemy.clear()
    display_intro()
    scores = GAME_FONT.render(f"SCORE : {int(score)}", False, (255, 255, 255))
    high_scores = GAME_FONT.render(f"HIGH-SCORE : {get_high_score()}", False, (235, 195, 84))
    over = GAME_FONT.render("Game Over", False, (255, 255, 255))
    screen.blit(over, (CANVAS_WIDTH / 2 - 50, CANVAS_HEIGHT / 2 - 60))
    screen.blit(scores, (CANVAS_WIDTH / 2 - 50, 30))
    screen.blit(high_scores, (CANVAS_WIDTH / 2 - 80, 60))


def score_update():
    global scores, score
    score += .05
    store_high_score()
    scores = GAME_FONT.render(f"SCORE : {int(score)}", False, (255, 255, 255))
    high_scores = GAME_FONT.render(f"HIGH-SCORE : {get_high_score()}", False, (235, 195, 84))
    screen.blit(scores, (100, 30))
    screen.blit(high_scores, (CANVAS_WIDTH - 255, 30))


def ememy_create():
    global enemy, object, score
    if len(enemy) == 0:
        select = random.randint(0, 2)
        if select == 1:
            object = dino_class.Bird()
            enemy.append(object)
            # game speed control birds
            if score > 50:
                object.bird_speed = 4
            if score > 150:
                object.bird_speed = 5
            if score > 350:
                object.bird_speed = 6
            if score > 1500:
                object.bird_speed = 8
        else:
            object = dino_class.Cactus()
            enemy.append(object)
            # game speed control of cactus
            if score > 50:
                object.cactus_speed = 5
            if score > 100:
                object.cactus_speed = 7
            if score > 400:
                object.cactus_speed = 9
            if score > 1000:
                object.cactus_speed = 9.5


def enemy_update():
    global enemy
    for foe in enemy:
        foe.update()
        if foe.rect.x <= -50:
            enemy.pop()


def display_enemy():
    if len(enemy) != 0:
        enemy[0].display(screen)


def disply_background():
    screen.blit(BACKGROUND, (0, 0))


def display_intro():
    screen.blit(INTRO, (0, 0))


def disply_running_foreground():
    global ground_x
    if ground_x <= -800:
        ground_x = 0
    ground_x -= .5

    screen.blit(GROUND, (ground_x, 469))
    screen.blit(GROUND, (800 + ground_x, 469))


# change the background and foreground after some times
def change_bg_fg():
    global bg_fg, BACKGROUND, GROUND
    if bg_fg > 3:
        bg_fg = 1
    else:
        if bg_fg == 1:
            BACKGROUND = pygame.image.load("assets/images/day.png").convert()
            GROUND = pygame.image.load("assets/images/day_foreground.png").convert()

        elif bg_fg == 2:
            BACKGROUND = pygame.image.load("assets/images/evening.png").convert()
            GROUND = pygame.image.load("assets/images/evening_foreground.png").convert()

        else:
            BACKGROUND = pygame.image.load("assets/images/night.png").convert()
            GROUND = pygame.image.load("assets/images/night_goreground.png").convert()
        bg_fg += 1


def store_high_score():
    global score
    h_score = get_high_score()
    s = int(score)
    h = int(h_score)
    if h < s:
        with open("highest_score.txt", "w") as f:
            f.write(str(s))


# retrive high score
def get_high_score():
    try:
        with open("highest_score.txt", "r") as f:
            return f.read()
    except:
        with open("highest_score.txt", "w+") as f:
            f.write('0')
            with open("highest_score.txt", "r") as f:
                return f.read()


# creating dino and cloud
dino_object = dino_class.Dino()
cloud = dino_class.Clouds(screen)
get_high_score()

# game loop
while True:
    if GAME_STATE == 'ready':
        ready_state()

    if GAME_STATE == 'game_over':
        game_over()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                pygame.mixer.Sound.play(JUMP)
                if dino_object.is_running == True:
                    dino_object.is_jumping = True
                    dino_object.is_running = False
                    dino_object.is_leaning = False

            if event.key == pygame.K_DOWN:
                pygame.mixer.Sound.play(DUCK)
                if dino_object.is_running == True:
                    dino_object.is_jumping = False
                    dino_object.is_running = False
                    dino_object.is_leaning = True

            if event.key == pygame.K_RETURN and (GAME_STATE == 'ready' or GAME_STATE == 'game_over'):
                GAME_STATE = "active"
                score = 0

        if event.type == CHANGE_BCK and GAME_STATE == 'active':
            change_bg_fg()
        if event.type == ACTIVE_MOVEMENT and GAME_STATE == 'active':
            active_state()
        if event.type == CLOUD_PLAY and GAME_STATE == 'active':
            cloud.cloud_flight()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                dino_object.dino_lean_up()

        if event.type == pygame.MOUSEBUTTONDOWN and (GAME_STATE == 'ready' or GAME_STATE == 'game_over'):
            if event.button == 1:
                start_button()

    pygame.display.update()
