import pygame
import sys
from collections import deque

pygame.init()

WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Kasus 4")

clock = pygame.time.Clock()

# ===== COLORS =====
BG = (30,30,30)
TEXT = (240,240,240)

NODE = (120,200,255)
VISITED = (255,170,100)
ACTIVE = (255,100,100)
PATH = (80,255,140)

HEADER = (70,60,120)
PANEL = (50,50,50)

BTN_GREEN = (100,190,130)
BTN_BLUE = (90,140,230)
BTN_RED = (220,80,80)

font = pygame.font.SysFont("consolas",16)
title_font = pygame.font.SysFont("arial",26,True)

# ===== GRAPH =====
graph = {
    "A": ["B", "C"],
    "B": ["D", "E"],
    "C": ["F"],
    "D": [],
    "E": ["F"],
    "F": []
}

pos = {
    "A": (500,120),
    "B": (350,220),
    "C": (650,220),
    "D": (250,350),
    "E": (450,350),
    "F": (650,350)
}

# ===== BFS STATE =====
start = "A"
queue = deque()
visited = set()
parent = {}

visited_order = []  

current = None
step = 0

paused = True
finished = False

queue.append(start)
visited.add(start)
parent[start] = None

# ===== BUTTON =====
play_btn = pygame.Rect(50,520,100,40)
pause_btn = pygame.Rect(170,520,100,40)
reset_btn = pygame.Rect(290,520,100,40)

def reset():
    global queue, visited, parent, visited_order, current, paused, finished, step

    queue = deque()
    visited = set()
    parent = {}
    visited_order = []

    queue.append(start)
    visited.add(start)
    parent[start] = None

    current = None
    paused = True
    finished = False
    step = 0

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
                if not finished:
                    paused = False

            if pause_btn.collidepoint(mouse):
                paused = True

            if reset_btn.collidepoint(mouse):
                reset()

    if not paused and not finished:

        if queue:

            current = queue.popleft()
            visited_order.append(current)

            for nb in graph[current]:
                if nb not in visited:
                    visited.add(nb)
                    queue.append(nb)
                    parent[nb] = current

        else:
            finished = True
            paused = True

    for n in graph:
        for nb in graph[n]:

            color = (80,80,80)

          
            if n in visited_order and nb in visited_order:
                if parent.get(nb) == n:
                    color = PATH

            pygame.draw.line(screen,color,pos[n],pos[nb],2)

    # ===== DRAW NODES =====
    for n,p in pos.items():

        color = NODE

        if n in visited:
            color = VISITED

        if n == current:
            color = ACTIVE

        pygame.draw.circle(screen,color,p,25)
        screen.blit(font.render(n,True,TEXT),(p[0]-5,p[1]-8))

    # ===== HEADER =====
    pygame.draw.rect(screen, HEADER, (0,0,WIDTH,60))
    screen.blit(title_font.render("BFS (Breadth-First Search)",True,TEXT),(20,15))

    # ===== QUEUE =====
    pygame.draw.rect(screen,PANEL,(20,80,250,200),border_radius=10)
    screen.blit(font.render("LOG PROSES",True,TEXT),(30,90))

    y = 120
    for q in list(queue):
        screen.blit(font.render(str(q),True,TEXT),(40,y))
        y += 25

    # ===== BUTTON =====
    pygame.draw.rect(screen,BTN_GREEN,play_btn,border_radius=8)
    pygame.draw.rect(screen,BTN_BLUE,pause_btn,border_radius=8)
    pygame.draw.rect(screen,BTN_RED,reset_btn,border_radius=8)

    screen.blit(font.render("PLAY",True,TEXT),(75,530))
    screen.blit(font.render("PAUSE",True,TEXT),(185,530))
    screen.blit(font.render("RESET",True,TEXT),(300,530))

    # ===== STATUS =====
    status = "SELESAI" if finished else ("PAUSED" if paused else "RUNNING")
    screen.blit(font.render(f"STATUS: {status}",True,TEXT),(650,520))

    pygame.display.flip()
    clock.tick(1.2)  

pygame.quit()
sys.exit()