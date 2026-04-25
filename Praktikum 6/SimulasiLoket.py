import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Kasus 5")

clock = pygame.time.Clock()

# ===== COLORS =====
BG = (20,20,20)
TEXT = (240,240,240)

PANEL = (45,45,45)
HEADER = (70,60,120)

GREEN = (100,200,140)   
RED = (230,80,80)       
YELLOW = (255,200,100) 
BLUE = (90,150,255)   

font = pygame.font.SysFont("consolas",14)
title = pygame.font.SysFont("arial",22,True)

# ===== SYSTEM =====
queue = []
served = []

time = 0
next_id = 1
paused = True

SERVICE_TIME = 200
ARRIVAL_PROB = 0.02

agents = [
    {"busy": False, "t": 0, "p": None},
    {"busy": False, "t": 0, "p": None}
]


QUEUE_BOX = (20,80,300,500)
AGENT_BOX = (340,80,320,500)
STATS_BOX = (680,80,300,500)

QUEUE_SLOTS = [(120,170),(120,240),(120,310),(120,380),(120,450)]

AGENT_POS = [(370,220),(370,380)]

# ===== BUTTONS =====
play_btn = pygame.Rect(650,15,80,30)
pause_btn = pygame.Rect(740,15,80,30)
reset_btn = pygame.Rect(830,15,80,30)

def spawn():
    global next_id
    queue.append({
        "id": next_id,
        "x": 80,
        "y": 120,
        "arrival": time,
        "state": "R1"
    })
    next_id += 1

def move(p,tx,ty):
    p["x"] += (tx - p["x"]) * 0.06
    p["y"] += (ty - p["y"]) * 0.06

def reset():
    global queue, served, time, next_id, paused
    queue.clear()
    served.clear()
    time = 0
    next_id = 1
    paused = True

reset()

running = True
while running:
    screen.fill(BG)
    mouse = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if play_btn.collidepoint(mouse):
                paused = False
            if pause_btn.collidepoint(mouse):
                paused = True
            if reset_btn.collidepoint(mouse):
                reset()

    # ===== SIMULATION =====
    if not paused:
        time += 1

        if random.random() < ARRIVAL_PROB:
            spawn()

     
        for i,p in enumerate(queue):
            if i < len(QUEUE_SLOTS):
                move(p,*QUEUE_SLOTS[i])

        for a in agents:

            # R2 START
            if not a["busy"] and queue:
                p = queue.pop(0)
                a["busy"] = True
                a["t"] = SERVICE_TIME
                a["p"] = p
                p["state"] = "R2"

            # R3 FINISH
            if a["busy"]:
                a["t"] -= 1

                if a["t"] <= 0:
                    a["busy"] = False

                    if a["p"]:
                        a["p"]["state"] = "R3"
                        served.append(a["p"])
                    a["p"] = None

    # ===== HEADER =====
    pygame.draw.rect(screen,HEADER,(0,0,WIDTH,60))
    screen.blit(title.render("Simulasi Loket Tiket Bandara",True,TEXT),(20,18))

    # ===== BUTTONS =====
    pygame.draw.rect(screen,GREEN,play_btn, border_radius=6)
    pygame.draw.rect(screen,BLUE,pause_btn, border_radius=6)
    pygame.draw.rect(screen,RED,reset_btn, border_radius=6)

    screen.blit(font.render("PLAY",True,TEXT),(play_btn.x+10,play_btn.y+8))
    screen.blit(font.render("PAUSE",True,TEXT),(pause_btn.x+5,pause_btn.y+8))
    screen.blit(font.render("RESET",True,TEXT),(reset_btn.x+5,reset_btn.y+8))

    # ===== QUEUE =====
    pygame.draw.rect(screen,PANEL,QUEUE_BOX,border_radius=10)
    screen.blit(font.render("QUEUE (R1)",True,TEXT),(30,90))

    for slot in QUEUE_SLOTS:
        pygame.draw.circle(screen,(80,80,80),slot,10,2)

    for p in queue:

        color = YELLOW
        if p["state"] == "R2":
            color = BLUE
        elif p["state"] == "R3":
            color = GREEN

        pygame.draw.circle(screen,color,(int(p["x"]),int(p["y"])),14)

        txt = font.render(str(p["id"]),True,(0,0,0))
        rect = txt.get_rect(center=(p["x"],p["y"]))
        screen.blit(txt,rect)

    # ===== AGENTS =====
    pygame.draw.rect(screen,PANEL,AGENT_BOX,border_radius=10)
    screen.blit(font.render("LOKET (R2/R3)",True,TEXT),(350,90))

    for i,a in enumerate(agents):
        x,y = AGENT_POS[i]

        color = GREEN if not a["busy"] else RED
        pygame.draw.rect(screen,color,(x,y,120,60),border_radius=8)

    
        label = "FREE (R3)"
        if a["busy"]:
            label = "MELAYANI (R2)"

        screen.blit(font.render(label,True,TEXT),(x,y-20))

        if a["p"]:
            screen.blit(font.render(f"P{a['p']['id']}",True,TEXT),(x+10,y+20))

    # ===== STATS =====
    pygame.draw.rect(screen,PANEL,STATS_BOX,border_radius=10)
    screen.blit(font.render("STATISTIK",True,TEXT),(690,90))

    avg = sum([time - p["arrival"] for p in served]) / len(served) if served else 0

    screen.blit(font.render(f"Time: {time}",True,TEXT),(690,140))
    screen.blit(font.render(f"Served: {len(served)}",True,TEXT),(690,170))
    screen.blit(font.render(f"Avg Wait: {avg:.2f}",True,TEXT),(690,200))

    screen.blit(font.render("R1=ENQUEUE",True,TEXT),(690,260))
    screen.blit(font.render("R2=DEQUEUE",True,TEXT),(690,285))
    screen.blit(font.render("R3=FREE",True,TEXT),(690,310))

    status = "PAUSED" if paused else "RUNNING"
    screen.blit(font.render(status,True,TEXT),(690,360))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()