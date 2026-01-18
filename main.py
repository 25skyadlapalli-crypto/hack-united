import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 1000, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Healthy Runner XP")

clock = pygame.time.Clock()
FONT = pygame.font.SysFont("arial", 20)
BIG_FONT = pygame.font.SysFont("arial", 32)

BASE_SPEED = 5
DEATH_DISPLAY_TIME = 60
INVULN_TIME = 30

death_message = ""
death_timer = 0
invuln_timer = 0

game_complete = False

player_img = pygame.image.load("assets/player.png").convert_alpha()
player_img = pygame.transform.scale(player_img, (80, 80))

backgrounds = [
    pygame.transform.scale(pygame.image.load("assets/cave.png").convert(), (WIDTH, HEIGHT)),
    pygame.transform.scale(pygame.image.load("assets/jungle.png").convert(), (WIDTH, HEIGHT)),
    pygame.transform.scale(pygame.image.load("assets/volcano.png").convert(), (WIDTH, HEIGHT))
]

fruit_imgs = {
    "apple": pygame.transform.scale(pygame.image.load("assets/apple.png").convert_alpha(), (30, 30)),
    "banana": pygame.transform.scale(pygame.image.load("assets/banana.png").convert_alpha(), (30, 30)),
    "avocado": pygame.transform.scale(pygame.image.load("assets/avocado.png").convert_alpha(), (30, 30)),
    "blueberry": pygame.transform.scale(pygame.image.load("assets/blueberry.png").convert_alpha(), (30, 30)),
    "watermelon": pygame.transform.scale(pygame.image.load("assets/watermelon.png").convert_alpha(), (30, 30))
}

spike_img = pygame.transform.scale(
    pygame.image.load("assets/spike.png").convert_alpha(), (30 , 30)
)
top_spike_img = pygame.transform.flip(spike_img, False, True)

square_img = pygame.transform.scale(
    pygame.image.load("assets/square.png").convert_alpha(), (40, 40 )
)

bg_x1 = 0
bg_x2 = WIDTH

player = pygame.Rect(120, 250, 80, 80)
vel_y = 0

current_level = 0
xp = 0
level_xp_thresholds = [10, 25, 50]

question_active = False
current_q = None


fruit_type = random.choice(list(fruit_imgs.keys())[:3])
fruit = pygame.Rect(WIDTH + 300, random.randint(80, HEIGHT - 110), 30, 30)

top_spikes = []
bottom_spikes = []
middle_blocks = []


questions = {
    "apple": {
        0: [
            {"q": "Which vitamin is high in apples?", "options": ["A","C","K","D"], "answer":1},
            {"q": "Apples are rich in?", "options":["Fat","Protein","Fiber","Sugar"], "answer":2},
            {"q": "Calories in an apple?", "options":["50","95","150","200"], "answer":1}
        ],
        1: [
            {"q": "Apple fiber supports?", "options":["Digestion","Vision","Sleep","Bones"], "answer":0},
            {"q": "Apples help lower?", "options":["Cholesterol","Fever","Cough","Pain"], "answer":0},
            {"q": "Apple antioxidants?", "options":["Flavonoids","Iron","Zinc","Calcium"], "answer":0}
        ],
        2: [
            {"q": "Apples regulate?", "options":["Blood sugar","Sleep","Vision","Heart rate"], "answer":0},
            {"q": "Key apple mineral?", "options":["Potassium","Iron","Zinc","Sodium"], "answer":0},
            {"q": "Apple health benefit?", "options":["Heart health","Hearing","Memory","Reflexes"], "answer":0}
        ]
    },
    "banana": {
        0: [
            {"q":"Bananas are rich in?", "options":["Iron","Potassium","Calcium","Zinc"], "answer":1},
            {"q":"Bananas give fast?", "options":["Energy","Fat","Protein","Fiber"], "answer":0},
            {"q":"Bananas contain?", "options":["Sugar","Alcohol","Cholesterol","Trans fat"], "answer":0}
        ],
        1: [
            {"q":"Bananas help prevent?", "options":["Cramps","Flu","Cold","Infection"], "answer":0},
            {"q":"Bananas support?", "options":["Digestion","Vision","Bones","Skin"], "answer":0},
            {"q":"Bananas are low in?", "options":["Fat","Potassium","Fiber","Vitamin B6"], "answer":0}
        ],
        2: [
            {"q":"Bananas regulate?", "options":["Blood pressure","Sleep","Vision","Mood"], "answer":0},
            {"q":"Banana antioxidants?", "options":["Flavonoids","Iron","Zinc","Calcium"], "answer":0},
            {"q":"Bananas best for?", "options":["Energy","Hydration","Weight loss","Sleep"], "answer":0}
        ]
    },
    "avocado": {
        0: [
            {"q":"Avocados contain?", "options":["Healthy fats","Sugar","Trans fats","Starch"], "answer":0},
            {"q":"Avocados support?", "options":["Heart","Lungs","Bones","Eyes"], "answer":0},
            {"q":"Avocados high in?", "options":["Vitamin E","Vitamin D","B12","A"], "answer":0}
        ],
        1: [
            {"q":"Avocados lower?", "options":["Cholesterol","Sleep","Weight","Stress"], "answer":0},
            {"q":"Avocados rich in?", "options":["Potassium","Iron","Zinc","Sodium"], "answer":0},
            {"q":"Avocado fiber helps?", "options":["Digestion","Vision","Sleep","Energy"], "answer":0}
        ],
        2: [
            {"q":"Avocados reduce risk of?", "options":["Heart disease","Flu","Cold","Obesity"], "answer":0},
            {"q":"Avocados provide?", "options":["Unsaturated fats","Sugar","Protein","Starch"], "answer":0},
            {"q":"Avocados improve?", "options":["Heart health","Hearing","Memory","Reflexes"], "answer":0}
        ]
    },
    "blueberry": {
        1: [
            {"q":"Blueberries are rich in?", "options":["Antioxidants","Sugar","Fat","Protein"], "answer":0},
            {"q":"Blueberries support?", "options":["Brain","Heart","Bones","Vision"], "answer":0},
            {"q":"Blueberries help with?", "options":["Memory","Sleep","Hair growth","Digestion"], "answer":0}
        ],
        2: [
            {"q":"Blueberries improve?", "options":["Blood pressure","Vision","Weight loss","Sleep"], "answer":0},
            {"q":"Blueberries provide?", "options":["Vitamins","Cholesterol","Starch","Trans fats"], "answer":0},
            {"q":"Blueberries are best for?", "options":["Brain","Muscles","Bones","Skin"], "answer":0}
        ]
    },
    "watermelon": {
        2: [
            {"q":"Watermelon is high in?", "options":["Water","Sugar","Protein","Fat"], "answer":0},
            {"q":"Watermelon supports?", "options":["Hydration","Vision","Sleep","Bones"], "answer":0},
            {"q":"Watermelon contains?", "options":["Vitamin C","Iron","Calcium","Zinc"], "answer":0}
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
        top_spikes.append(pygame.Rect(x, 0, 30, 30))
        bottom_spikes.append(pygame.Rect(x, HEIGHT - 30, 30, 30))

def spawn_middle_blocks():
    for _ in range(1 + current_level):
        middle_blocks.append(
            pygame.Rect(WIDTH + random.randint(400, 900),
                        random.randint(120, HEIGHT - 180),
                        40 , 40)
        )

def spawn_fruit():
    global fruit_type
    
    available = ["apple", "banana", "avocado"]
    if current_level >= 1:
        available.append("blueberry")
    if current_level >= 2:
        available.append("watermelon")
    fruit_type = random.choice(available)
    fruit.x = WIDTH + random.randint(400, 700)
    fruit.y = random.randint(80, HEIGHT - 110)

def reset_level(message="Boohoo, you hit a spike!"):
    global vel_y, question_active, death_message, death_timer, invuln_timer
    vel_y = 0
    question_active = False
    middle_blocks.clear()
    create_edge_spikes()
    spawn_fruit()
    player.y = 250
    death_message = message
    death_timer = DEATH_DISPLAY_TIME
    invuln_timer = INVULN_TIME

create_edge_spikes()
spawn_fruit()

block_timer = 0
running = True

while running:
    clock.tick(60)
    PAUSED = question_active or death_timer > 0 or game_complete

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN and not PAUSED:
            if event.key == pygame.K_SPACE:
                vel_y = -15

        if event.type == pygame.MOUSEBUTTONDOWN and question_active:
            mx, my = pygame.mouse.get_pos()
            for i in range(4):
                if pygame.Rect(250, 230 + i * 40, 500, 30).collidepoint(mx, my):
                    if i == current_q["answer"]:
                        question_active = False
                       
                        xp += 5 if fruit_type not in ["blueberry","watermelon"] else 10
                        if xp >= 50:
                            game_complete = True
                        elif current_level < 2 and xp >= level_xp_thresholds[current_level]:
                            current_level += 1
                            create_edge_spikes()
                        spawn_fruit()
                    else:
                        reset_level("Boohoo, you got the question wrong! Try again.")

    if not PAUSED:
        vel_y += 1
        player.y += vel_y

        fruit.x -= BASE_SPEED + current_level * 2
        for block in middle_blocks:
            block.x -= BASE_SPEED + current_level * 2

        block_timer += 1
        if block_timer > 180:
            spawn_middle_blocks()
            block_timer = 0

        if player.colliderect(fruit) and not question_active:
            question_active = True
            current_q = random.choice(questions[fruit_type][current_level])
            fruit.x = -100

        if invuln_timer == 0:
            if player.top <= 40 or player.bottom >= HEIGHT - 40:
                reset_level("Boohoo, you hit a spike!")

            for block in middle_blocks:
                if player.colliderect(block):
                    reset_level("Ouch! You crashed into a block!")
                    break

        if invuln_timer > 0:
            invuln_timer -= 1

        middle_blocks[:] = [b for b in middle_blocks if b.x > -70]
        if fruit.x < -150 and not question_active:
            spawn_fruit()

    draw_background(0 if PAUSED else BASE_SPEED + current_level * 2)

    screen.blit(player_img, player)
    screen.blit(fruit_imgs[fruit_type], fruit)

    for s in top_spikes:
        screen.blit(top_spike_img, s)
    for s in bottom_spikes:
        screen.blit(spike_img, s)
    for b in middle_blocks:
        screen.blit(square_img, b)

    if question_active:
        pygame.draw.rect(screen, (10,10,10), (200,180,600,260))
        screen.blit(FONT.render(current_q["q"], True, (255,255,255)), (220,190))
        for i, opt in enumerate(current_q["options"]):
            pygame.draw.rect(screen, (60,60,60), (250,230+i*40,500,30))
            screen.blit(FONT.render(opt, True, (255,255,255)), (260,235+i*40))

    if death_timer > 0:
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0,0,0))
        screen.blit(overlay, (0,0))
        screen.blit(BIG_FONT.render(death_message, True, (255,80,80)),
                    (WIDTH//2 - 260, HEIGHT//2 - 20))
        death_timer -= 1

    if game_complete:
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0,0,0))
        screen.blit(overlay, (0,0))
        screen.blit(
            BIG_FONT.render(
                "YOU WON!!!, make sure you eat your fruits daily!",
                True, (80,255,80)
            ),
            (WIDTH//2 - 450, HEIGHT//2 - 20)
        )

    screen.blit(FONT.render(f"XP: {xp}", True, (255,255,0)), (20,20))
    screen.blit(FONT.render(f"Level: {current_level+1}", True, (255,255,0)), (20,50))

    pygame.display.update()
