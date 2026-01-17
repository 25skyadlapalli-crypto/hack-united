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

spike_img = pygame.image.load("assets/spike.png").convert_alpha()
spike_img = pygame.transform.scale(spike_img, (40, 40))
top_spike_img = pygame.transform.flip(spike_img, False, True)

bg_x1 = 0
bg_x2 = WIDTH

player = pygame.Rect(120, 250, 50, 50)
vel_y = 0

current_level = 0
level_xp_thresholds = [10, 25, 50]
xp = 0
speed = BASE_SPEED
question_active = False
game_over = False
current_q = None

fruit_type = random.choice(list(fruit_imgs.keys()))
fruit = pygame.Rect(WIDTH + 300, random.randint(100, HEIGHT - 50), 30, 30)

spikes = []
top_spikes = []
bottom_spikes = []
middle_blocks = []

questions = {
    "apple": {
        0: [
            {"q": "Which vitamin is high in apples?", "options": ["A", "C", "K", "D"], "answer":1},
            {"q": "Approx calories in a medium apple?", "options":["50","95","120","200"],"answer":1},
            {"q": "Apples are rich in which nutrient?", "options":["Fat","Protein","Fiber","Sugar"], "answer":2}
        ],
        1: [
            {"q": "Which antioxidant is in apples?", "options":["Vitamin E","Flavonoids","Iron","Magnesium"], "answer":1},
            {"q": "Eating apples can reduce risk of?", "options":["Heart disease","Cold","Cancer","Flu"],"answer":0},
            {"q": "Apple pectin affects what?", "options":["Vision","Digestion","Hair","Bones"], "answer":1}
        ],
        2: [
            {"q": "Which mineral is in apples?", "options":["Potassium","Calcium","Sodium","Zinc"], "answer":0},
            {"q": "Apples may help regulate?", "options":["Blood sugar","Blood pressure","Heart rate","Sleep"], "answer":0},
            {"q": "High apple intake may reduce?", "options":["Cough","Cholesterol","Fever","Infection"], "answer":1}
        ]
    },
    "banana": {
        0: [
            {"q":"Bananas are rich in which mineral?","options":["Calcium","Potassium","Iron","Zinc"],"answer":1},
            {"q":"Primary sugar in bananas?","options":["Fructose","Sucrose","Glucose","All"],"answer":3},
            {"q":"Bananas provide quick energy due to?","options":["Fiber","Sugar","Protein","Fat"],"answer":1}
        ],
        1: [
            {"q":"Bananas help with muscle cramps because of?","options":["Potassium","Calcium","Vitamin C","Iron"],"answer":0},
            {"q":"Bananas improve digestion due to?","options":["Fiber","Fat","Sugar","Vitamin D"],"answer":0},
            {"q":"Bananas are low in which nutrient?","options":["Protein","Potassium","Vitamin B6","Magnesium"],"answer":0}
        ],
        2: [
            {"q":"Bananas help maintain?","options":["Blood pressure","Heart rate","Vision","Bones"],"answer":0},
            {"q":"Bananas can boost energy levels due to?","options":["Fat","Sugar","Protein","Fiber"],"answer":1},
            {"q":"Bananas contain antioxidants like?","options":["Flavonoids","Vitamin K","Calcium","Iron"],"answer":0}
        ]
    },
    "avocado": {
        0: [
            {"q":"Avocados are rich in?","options":["Unsaturated fats","Saturated fats","Protein","Sugar"],"answer":0},
            {"q":"Avocados are good for?","options":["Heart","Lungs","Brain","Bones"],"answer":0},
            {"q":"Avocados contain which vitamin?","options":["C","D","E","K"],"answer":2}
        ],
        1: [
            {"q":"Avocados help reduce?","options":["Cholesterol","Blood sugar","Weight","Sleep"],"answer":0},
            {"q":"Avocados are high in which mineral?","options":["Potassium","Iron","Calcium","Zinc"],"answer":0},
            {"q":"Avocado fiber helps?","options":["Digestive health","Vision","Sleep","Energy"],"answer":0}
        ],
        2: [
            {"q":"Avocados are beneficial for?","options":["Heart health","Vision","Hair","Nails"],"answer":0},
            {"q":"Avocados provide healthy?","options":["Fats","Sugars","Proteins","Starches"],"answer":0},
            {"q":"Avocado reduces risk of?","options":["Heart disease","Cold","Flu","Obesity"],"answer":0}
        ]
    }
}

def draw_background(speed):
    global bg_x1, bg_x2
    bg_x1 -= speed
    bg_x2 -= speed
    if bg_x1 <= -WIDTH: bg_x1 = WIDTH
    if bg_x2 <= -WIDTH: bg_x2 = WIDTH
    screen.fill((0,0,0))
    screen.blit(backgrounds[current_level], (bg_x1,0))
    screen.blit(backgrounds[current_level], (bg_x2,0))

def spawn_fruit():
    global fruit_type
    fruit_type = random.choice(list(fruit_imgs.keys()))
    fruit.x = WIDTH + random.randint(400, 700)
    fruit.y = random.randint(50, HEIGHT-80)

def spawn_random_spikes():
    num_spikes = 2 + current_level*2
    for _ in range(num_spikes):
        x = WIDTH + random.randint(500, 900)
        y = random.randint(50, HEIGHT-90)
        spikes.append(pygame.Rect(x,y,40,40))

def spawn_middle_blocks():
    num_blocks = 1 + current_level
    for _ in range(num_blocks):
        x = WIDTH + random.randint(500, 900)
        y = random.randint(150, HEIGHT-150)
        middle_blocks.append(pygame.Rect(x,y,60,40))

def create_edge_spikes():
    top_spikes.clear()
    bottom_spikes.clear()
    for x in range(0, WIDTH, 40):
        top_spikes.append(pygame.Rect(x,0,40,40))
        bottom_spikes.append(pygame.Rect(x,HEIGHT-40,40,40))

def reset_game():
    global vel_y, question_active, game_over, xp, current_level
    player.y = 250
    vel_y = 0
    question_active = False
    game_over = False
    xp = 0
    current_level = 0
    spikes.clear()
    middle_blocks.clear()
    spawn_fruit()
    create_edge_spikes()

create_edge_spikes()
spawn_fruit()

spawn_timer = 0
middle_timer = 0
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
                reset_game()

        if event.type == pygame.MOUSEBUTTONDOWN and question_active:
            mx, my = pygame.mouse.get_pos()
            for i in range(4):
                box = pygame.Rect(250, 230 + i*40, 500, 30)
                if box.collidepoint(mx,my):
                    if i == current_q["answer"]:
                        question_active = False
                        xp += 5
                        if current_level < 2 and xp >= level_xp_thresholds[current_level]:
                            current_level += 1
                            create_edge_spikes()
                        spawn_fruit()
                    else:
                        reset_game()

    if not PAUSED:
        vel_y += 1
        player.y += vel_y
        player.y = max(0, min(player.y, HEIGHT-50))

        fruit.x -= BASE_SPEED + current_level*2
        for spike in spikes:
            spike.x -= BASE_SPEED + current_level*2
        for block in middle_blocks:
            block.x -= BASE_SPEED + current_level*2

        spawn_timer += 1
        if spawn_timer > 140:
            spawn_random_spikes()
            spawn_timer = 0

        middle_timer +=1
        if middle_timer > 200:
            spawn_middle_blocks()
            middle_timer = 0

        if player.colliderect(fruit):
            question_active = True
            current_q = random.choice(questions[fruit_type][current_level])

        for obstacle in spikes + top_spikes + bottom_spikes + middle_blocks:
            if player.colliderect(obstacle):
                game_over = True

        spikes = [s for s in spikes if s.x > -50]
        middle_blocks = [b for b in middle_blocks if b.x > -70]

        if fruit.x < -50:
            spawn_fruit()

    draw_background(0 if PAUSED else BASE_SPEED + current_level*2)

    screen.blit(player_img, player)
    screen.blit(fruit_imgs[fruit_type], fruit)

    for spike in bottom_spikes:
        screen.blit(spike_img, spike)
    for spike in top_spikes:
        screen.blit(top_spike_img, spike)
    for spike in spikes:
        screen.blit(spike_img, spike)
    for block in middle_blocks:
        pygame.draw.rect(screen,(120,60,0),block)

    if question_active:
        pygame.draw.rect(screen,(10,10,10),(200,180,600,260))
        screen.blit(FONT.render(current_q["q"],True,(255,255,255)),(220,190))
        for i,opt in enumerate(current_q["options"]):
            pygame.draw.rect(screen,(60,60,60),(250,230+i*40,500,30))
            screen.blit(FONT.render(opt,True,(255,255,255)),(260,235+i*40))

    if game_over:
        pygame.draw.rect(screen,(0,0,0),(0,0,WIDTH,HEIGHT))
        screen.blit(BIG_FONT.render("GAME OVER",True,(255,50,50)),(410,210))
        screen.blit(FONT.render("Press R to restart",True,(200,200,200)),(420,270))

    screen.blit(FONT.render(f"XP: {xp}",True,(255,255,0)),(20,20))
    screen.blit(FONT.render(f"Level: {current_level+1}",True,(255,255,0)),(20,50))

    pygame.display.update()

pygame.quit()
sys.exit()
