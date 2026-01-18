import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 1000, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Healthy Runner XP")

clock = pygame.time.Clock()
FONT = pygame.font.SysFont("arial", 20)
BIG_FONT = pygame.font.SysFont("arial", 36)

BASE_SPEED = 5

player_img = pygame.image.load("assets/player.png").convert_alpha()
player_img = pygame.transform.scale(player_img, (50, 50))

backgrounds = [
    pygame.transform.scale(pygame.image.load("assets/cave.png").convert(), (WIDTH, HEIGHT)),
    pygame.transform.scale(pygame.image.load("assets/jungle.png").convert(), (WIDTH, HEIGHT)),
    pygame.transform.scale(pygame.image.load("assets/volcano.png").convert(), (WIDTH, HEIGHT))
]

fruit_imgs = {
    "apple": pygame.transform.scale(pygame.image.load("assets/apple.png").convert_alpha(), (30, 30)),
    "banana": pygame.transform.scale(pygame.image.load("assets/banana.png").convert_alpha(), (30, 30)),
    "avocado": pygame.transform.scale(pygame.image.load("assets/avocado.png").convert_alpha(), (30, 30))
}

spike_img = pygame.transform.scale(
    pygame.image.load("assets/spike.png").convert_alpha(), (40, 40)
)
top_spike_img = pygame.transform.flip(spike_img, False, True)

square_img = pygame.transform.scale(
    pygame.image.load("assets/square.png").convert_alpha(), (60, 60)
)

bg_x1 = 0
bg_x2 = WIDTH

player = pygame.Rect(120, 250, 50, 50)
vel_y = 0

current_level = 0
xp = 0
level_xp_thresholds = [10, 25, 50]

checkpoints = {
    0: {"xp": 0, "y": 250},
    1: {"xp": level_xp_thresholds[0], "y": 250},
    2: {"xp": level_xp_thresholds[1], "y": 250},
}

question_active = False
game_over = False
current_q = None

fruit_type = random.choice(list(fruit_imgs.keys()))
fruit = pygame.Rect(WIDTH + 300, random.randint(80, HEIGHT - 110), 30, 30)

top_spikes = []
bottom_spikes = []
middle_blocks = []

questions = {
    "apple": {
        0: [
            {"q": "Which vitamin is high in apples?", "options": ["A","C","K","D"], "answer":1},
            {"q": "Calories in a medium apple?", "options":["50","95","120","200"], "answer":1},
            {"q": "Apples are rich in?", "options":["Fat","Protein","Fiber","Sugar"], "answer":2}
        ],
        1: [
            {"q": "Apple antioxidants are called?", "options":["Iron","Flavonoids","Zinc","Calcium"], "answer":1},
            {"q": "Apples can lower risk of?", "options":["Heart disease","Flu","Cold","Cancer"], "answer":0},
            {"q": "Apple fiber supports?", "options":["Vision","Digestion","Sleep","Bones"], "answer":1}
        ],
        2: [
            {"q": "Apples help regulate?", "options":["Blood sugar","Heart rate","Sleep","Vision"], "answer":0},
            {"q": "Apples may reduce?", "options":["Cholesterol","Fever","Cough","Pain"], "answer":0},
            {"q": "Key mineral in apples?", "options":["Potassium","Iron","Zinc","Sodium"], "answer":0}
        ]
    },
    "banana": {
        0: [
            {"q":"Bananas are rich in?", "options":["Iron","Potassium","Calcium","Zinc"], "answer":1},
            {"q":"Bananas provide fast?", "options":["Protein","Energy","Fat","Fiber"], "answer":1},
            {"q":"Bananas contain?", "options":["Sugar","Trans fat","Cholesterol","Alcohol"], "answer":0}
        ],
        1: [
            {"q":"Bananas help prevent?", "options":["Cramps","Flu","Headache","Cold"], "answer":0},
            {"q":"Bananas support?", "options":["Digestion","Vision","Bones","Skin"], "answer":0},
            {"q":"Bananas are low in?", "options":["Protein","Potassium","Vitamin B6","Fiber"], "answer":0}
        ],
        2: [
            {"q":"Bananas regulate?", "options":["Blood pressure","Heart rate","Sleep","Vision"], "answer":0},
            {"q":"Banana antioxidants?", "options":["Flavonoids","Calcium","Iron","Zinc"], "answer":0},
            {"q":"Bananas are best for?", "options":["Energy","Hydration","Weight loss","Sleep"], "answer":0}
        ]
    },
    "avocado": {
        0: [
            {"q":"Avocados contain?", "options":["Healthy fats","Sugar","Trans fats","Starch"], "answer":0},
            {"q":"Avocados support?", "options":["Heart","Lungs","Bones","Eyes"], "answer":0},
            {"q":"Avocados are high in?", "options":["Vitamin E","Vitamin D","Vitamin B12","Vitamin A"], "answer":0}
        ],
        1: [
            {"q":"Avocados lower?", "options":["Cholesterol","Blood sugar","Weight","Sleep"], "answer":0},
            {"q":"Avocados are rich in?", "options":["Potassium","Iron","Zinc","Sodium"], "answer":0},
            {"q":"Avocado fiber helps?", "options":["Digestion","Vision","Sleep","Energy"], "answer":0}
        ],
        2: [
            {"q":"Avocados reduce risk of?", "options":["Heart disease","Flu","Cold","Obesity"], "answer":0},
            {"q":"Avocados provide?", "options":["Unsaturated fats","Protein","Sugar","Starch"], "answer":0},
            {"q":"Avocados improve?", "options":["Heart health","Vision","Hearing","Memory"], "answer":0}
        ]
    }
}

def draw_background(speed):
    global bg_x1, bg_x2
    bg_x1 -= speed
    bg_x2 -= speed
    if bg_x1 <= -WIDTH:
        bg_x1 = WIDTH
    if bg_x2 <= -WIDTH:
        bg_x2 = WIDTH
    screen.blit(backgrounds[current_level], (bg_x1, 0))
    screen.blit(backgrounds[current_level], (bg_x2, 0))

def create_edge_spikes():
    top_spikes.clear()
    bottom_spikes.clear()
    for x in range(0, WIDTH, 40):
        top_spikes.append(pygame.Rect(x, 0, 40, 40))
        bottom_spikes.append(pygame.Rect(x, HEIGHT - 40, 40, 40))

def spawn_middle_blocks():
    count = 1 + current_level
    for _ in range(count):
        x = WIDTH + random.randint(400, 900)
        y = random.randint(120, HEIGHT - 180)
        middle_blocks.append(pygame.Rect(x, y, 60, 60))

def spawn_fruit():
    global fruit_type
    fruit_type = random.choice(list(fruit_imgs.keys()))
    fruit.x = WIDTH + random.randint(400, 700)
    fruit.y = random.randint(80, HEIGHT - 110)

def reset_to_checkpoint():
    global xp, vel_y, question_active, game_over
    checkpoint = checkpoints[current_level]
    xp = checkpoint["xp"]
    vel_y = 0
    question_active = False
    game_over = False
    middle_blocks.clear()
    create_edge_spikes()
    spawn_fruit()
    player.y = checkpoint["y"]

create_edge_spikes()
spawn_fruit()

block_timer = 0
running = True

while running:
    clock.tick(60)
    PAUSED = question_active or game_over

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if not PAUSED and event.key == pygame.K_SPACE:
                vel_y = -15
            if game_over and event.key == pygame.K_r:
                reset_to_checkpoint()

        if event.type == pygame.MOUSEBUTTONDOWN and question_active:
            mx, my = pygame.mouse.get_pos()
            for i in range(4):
                box = pygame.Rect(250, 230 + i * 40, 500, 30)
                if box.collidepoint(mx, my):
                    if i == current_q["answer"]:
                        question_active = False
                        xp += 5
                        if current_level < 2 and xp >= level_xp_thresholds[current_level]:
                            current_level += 1
                            create_edge_spikes()
                            spawn_fruit()
                    else:
                        reset_to_checkpoint()

    if not PAUSED:
        vel_y += 1
        player.y += vel_y
        player.y = max(40, min(player.y, HEIGHT - 90))

        fruit.x -= BASE_SPEED + current_level * 2
        for block in middle_blocks:
            block.x -= BASE_SPEED + current_level * 2

        block_timer += 1
        if block_timer > 180:
            spawn_middle_blocks()
            block_timer = 0

        if player.colliderect(fruit):
            question_active = True
            current_q = random.choice(questions[fruit_type][current_level])

        for obstacle in top_spikes + bottom_spikes + middle_blocks:
            if player.colliderect(obstacle):
                reset_to_checkpoint()
                break

        middle_blocks[:] = [b for b in middle_blocks if b.x > -70]

        if fruit.x < -50:
            spawn_fruit()

    draw_background(0 if PAUSED else BASE_SPEED + current_level * 2)

    screen.blit(player_img, player)
    screen.blit(fruit_imgs[fruit_type], fruit)

    for spike in top_spikes:
        screen.blit(top_spike_img, spike)
    for spike in bottom_spikes:
        screen.blit(spike_img, spike)
    for block in middle_blocks:
        screen.blit(square_img, block)

    if question_active:
        pygame.draw.rect(screen, (10,10,10), (200,180,600,260))
        screen.blit(FONT.render(current_q["q"], True, (255,255,255)), (220,190))
        for i, opt in enumerate(current_q["options"]):
            pygame.draw.rect(screen, (60,60,60), (250,230+i*40,500,30))
            screen.blit(FONT.render(opt, True, (255,255,255)), (260,235+i*40))

    screen.blit(FONT.render(f"XP: {xp}", True, (255,255,0)), (20,20))
    screen.blit(FONT.render(f"Level: {current_level+1}", True, (255,255,0)), (20,50))

    pygame.display.update()

pygame.quit()
sys.exit()
