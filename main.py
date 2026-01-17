import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 1000, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fuel Run")

clock = pygame.time.Clock()
FONT = pygame.font.SysFont("arial", 20)
BIG_FONT = pygame.font.SysFont("arial", 36)

player_img = pygame.transform.scale(
    pygame.image.load("assets/player.png").convert_alpha(), (50, 50)
)

backgrounds = [
    pygame.transform.scale(pygame.image.load("assets/cave.png").convert(), (WIDTH, HEIGHT)),
    pygame.transform.scale(pygame.image.load("assets/jungle.png").convert(), (WIDTH, HEIGHT)),
    pygame.transform.scale(pygame.image.load("assets/volcano.png").convert(), (WIDTH, HEIGHT))
]

spike_img = pygame.transform.scale(
    pygame.image.load("assets/spike.png").convert_alpha(), (40, 40)
)
top_spike_img = pygame.transform.flip(spike_img, False, True)

square_img = pygame.transform.scale(
    pygame.image.load("assets/square.png").convert_alpha(), (60, 60)
)

fruit_imgs = {
    "apple": pygame.transform.scale(pygame.image.load("assets/apple.png").convert_alpha(), (30, 30)),
    "banana": pygame.transform.scale(pygame.image.load("assets/banana.png").convert_alpha(), (30, 30)),
    "avocado": pygame.transform.scale(pygame.image.load("assets/avocado.png").convert_alpha(), (30, 30)),
    "blueberry": pygame.transform.scale(pygame.image.load("assets/blueberry.png").convert_alpha(), (30, 30)),
    "watermelon": pygame.transform.scale(pygame.image.load("assets/watermelon.png").convert_alpha(), (35, 35))
}

fruit_xp = {
    "apple": 5,
    "banana": 5,
    "avocado": 6,
    "blueberry": 10,
    "watermelon": 15
}

questions = {
    "apple": {
        0: [
            {"q":"Apples are high in?", "o":["Fat","Fiber","Protein","Salt"], "a":1},
            {"q":"Calories in apple?", "o":["50","95","200","300"], "a":1},
            {"q":"Apples help digestion due to?", "o":["Fiber","Sugar","Fat","Protein"], "a":0}
        ],
        1: [
            {"q":"Apple antioxidants?", "o":["Iron","Flavonoids","Zinc","Calcium"], "a":1},
            {"q":"Apple pectin helps?", "o":["Vision","Digestion","Sleep","Bones"], "a":1},
            {"q":"Apples reduce risk of?", "o":["Heart disease","Flu","Cold","Fever"], "a":0}
        ],
        2: [
            {"q":"Apples help regulate?", "o":["Blood sugar","Sleep","Hearing","Vision"], "a":0},
            {"q":"Apples may lower?", "o":["Cholesterol","Pain","Fever","Infection"], "a":0},
            {"q":"Main mineral in apples?", "o":["Potassium","Iron","Zinc","Sodium"], "a":0}
        ]
    },

    "banana": {
        0: [
            {"q":"Bananas are rich in?", "o":["Iron","Potassium","Zinc","Calcium"], "a":1},
            {"q":"Bananas give fast?", "o":["Protein","Energy","Fat","Fiber"], "a":1},
            {"q":"Bananas contain?", "o":["Sugar","Trans fat","Alcohol","Cholesterol"], "a":0}
        ],
        1: [
            {"q":"Bananas help prevent?", "o":["Cramps","Colds","Fever","Cough"], "a":0},
            {"q":"Bananas support?", "o":["Digestion","Vision","Bones","Skin"], "a":0},
            {"q":"Bananas low in?", "o":["Protein","Potassium","Fiber","Vitamin B6"], "a":0}
        ],
        2: [
            {"q":"Bananas regulate?", "o":["Blood pressure","Sleep","Vision","Memory"], "a":0},
            {"q":"Bananas contain antioxidants?", "o":["Flavonoids","Iron","Zinc","Calcium"], "a":0},
            {"q":"Bananas best for?", "o":["Energy","Weight loss","Sleep","Hydration"], "a":0}
        ]
    },

    "avocado": {
        0: [
            {"q":"Avocados contain?", "o":["Healthy fats","Sugar","Trans fats","Starch"], "a":0},
            {"q":"Avocados help?", "o":["Heart","Lungs","Bones","Eyes"], "a":0},
            {"q":"Avocados rich in?", "o":["Vitamin E","Vitamin D","B12","A"], "a":0}
        ],
        1: [
            {"q":"Avocados lower?", "o":["Cholesterol","Blood sugar","Weight","Sleep"], "a":0},
            {"q":"Avocados high in?", "o":["Potassium","Iron","Zinc","Sodium"], "a":0},
            {"q":"Avocado fiber helps?", "o":["Digestion","Vision","Sleep","Energy"], "a":0}
        ],
        2: [
            {"q":"Avocados reduce risk of?", "o":["Heart disease","Flu","Cold","Obesity"], "a":0},
            {"q":"Avocados provide?", "o":["Unsaturated fats","Protein","Sugar","Starch"], "a":0},
            {"q":"Avocados improve?", "o":["Heart health","Vision","Hearing","Memory"], "a":0}
        ]
    },

    "blueberry": {
        1: [
            {"q":"Blueberries are high in?", "o":["Antioxidants","Fat","Protein","Salt"], "a":0},
            {"q":"Blueberries support?", "o":["Brain health","Bones","Muscles","Skin"], "a":0},
            {"q":"Blueberries improve?", "o":["Memory","Sleep","Hearing","Vision"], "a":0}
        ],
        2: [
            {"q":"Blueberries reduce?", "o":["Oxidative stress","Pain","Fever","Infection"], "a":0},
            {"q":"Blueberries linked to?", "o":["Heart health","Lung strength","Bone mass","Muscle size"], "a":0},
            {"q":"Blueberries benefit?", "o":["Cognitive function","Digestion","Sleep","Hydration"], "a":0}
        ]
    },

    "watermelon": {
        2: [
            {"q":"Watermelon is high in?", "o":["Water","Fat","Protein","Fiber"], "a":0},
            {"q":"Watermelon helps with?", "o":["Hydration","Sleep","Muscle gain","Digestion"], "a":0},
            {"q":"Watermelon contains?", "o":["Lycopene","Trans fat","Caffeine","Cholesterol"], "a":0}
        ]
    }
}

player = pygame.Rect(120, 250, 50, 50)
vel_y = 0
xp = 0
level = 0
speed = 5

bg_x1, bg_x2 = 0, WIDTH
top_spikes, bottom_spikes, blocks = [], [], []

fruit = pygame.Rect(WIDTH + 400, 200, 30, 30)
fruit_type = "apple"
question_active = False
current_q = None
game_over = False
game_complete = False

def available_fruits():
    if level == 0:
        return ["apple","banana","avocado"]
    if level == 1:
        return ["apple","banana","avocado","blueberry"]
    return ["apple","banana","avocado","blueberry","watermelon"]

def spawn_fruit():
    global fruit_type
    fruit_type = random.choice(available_fruits())
    fruit.x = WIDTH + random.randint(300, 700)
    fruit.y = random.randint(80, HEIGHT - 110)

def create_edges():
    top_spikes.clear()
    bottom_spikes.clear()
    for x in range(0, WIDTH, 40):
        top_spikes.append(pygame.Rect(x, 0, 40, 40))
        bottom_spikes.append(pygame.Rect(x, HEIGHT - 40, 40, 40))

def spawn_block():
    blocks.append(
        pygame.Rect(WIDTH + 600, random.randint(140, HEIGHT - 200), 60, 60)
    )

spawn_fruit()
create_edges()
block_timer = 0

while True:
    clock.tick(60)
    paused = question_active or game_over or game_complete

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit(); sys.exit()

        if e.type == pygame.KEYDOWN and not paused:
            if e.key == pygame.K_SPACE:
                vel_y = -15

        if e.type == pygame.MOUSEBUTTONDOWN and question_active:
            mx, my = pygame.mouse.get_pos()
            for i in range(4):
                if pygame.Rect(250, 230+i*40, 500, 30).collidepoint(mx,my):
                    if i == current_q["a"]:
                        xp += fruit_xp[fruit_type]
                        question_active = False
                        spawn_fruit()
                        if xp >= (level+1)*25:
                            level += 1
                            if level > 2:
                                game_complete = True
                    else:
                        game_over = True

    if not paused:
        vel_y += 1
        player.y += vel_y
        player.y = max(40, min(player.y, HEIGHT - 90))

        fruit.x -= speed + level*2
        for b in blocks:
            b.x -= speed + level*2

        block_timer += 1
        if block_timer > 180:
            spawn_block()
            block_timer = 0

        if player.colliderect(fruit):
            question_active = True
            current_q = random.choice(questions[fruit_type][level])

        for o in top_spikes + bottom_spikes + blocks:
            if player.colliderect(o):
                game_over = True

        blocks[:] = [b for b in blocks if b.x > -70]

    bg_x1 -= speed + level*2
    bg_x2 -= speed + level*2
    if bg_x1 <= -WIDTH: bg_x1 = WIDTH
    if bg_x2 <= -WIDTH: bg_x2 = WIDTH

    screen.blit(backgrounds[level], (bg_x1,0))
    screen.blit(backgrounds[level], (bg_x2,0))
    screen.blit(player_img, player)
    screen.blit(fruit_imgs[fruit_type], fruit)

    for s in top_spikes:
        screen.blit(top_spike_img, s)
    for s in bottom_spikes:
        screen.blit(spike_img, s)
    for b in blocks:
        screen.blit(square_img, b)

    if question_active:
        pygame.draw.rect(screen,(10,10,10),(200,180,600,260))
        screen.blit(FONT.render(current_q["q"],True,(255,255,255)),(220,190))
        for i,o in enumerate(current_q["o"]):
            pygame.draw.rect(screen,(60,60,60),(250,230+i*40,500,30))
            screen.blit(FONT.render(o,True,(255,255,255)),(260,235+i*40))

    if game_complete:
        msg = "Time to change your life and be healthy!" if xp >= 60 else "Be Disappointed."
        screen.blit(BIG_FONT.render(msg,True,(255,255,0)),(180,230))

    pygame.display.update()
