import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Kasus 3")

clock = pygame.time.Clock()

# ===== COLORS =====
BG = (30,30,30)
TEXT = (240,240,240)
PANEL = (50,50,50)
HEADER = (70,60,120)

BTN_GREEN = (100,190,130)
BTN_BLUE = (90,140,230)
BTN_RED = (220,80,80)

PRIORITY_COLOR = {
    0: (255,100,100),
    1: (255,170,100),
    2: (255,220,120),
    3: (120,200,255)
}

PRIORITY_TEXT = {
    0: "KRITIS",
    1: "DARURAT",
    2: "MENENGAH",
    3: "RINGAN"
}

font = pygame.font.SysFont("consolas",16)
title_font = pygame.font.SysFont("arial",26,True)

# ===== PRIORITY QUEUE =====
class BPriorityQueue:
    def __init__(self, levels):
        self.queue = [[] for _ in range(levels)]

    def enqueue(self, name, priority):
        self.queue[priority].append(name)

    def dequeue(self):
        for i in range(len(self.queue)):
            if self.queue[i]:
                return self.queue[i].pop(0), i
        return None, None

    def isEmpty(self):
        return all(len(q) == 0 for q in self.queue)

# ===== DATA =====
patients = [
    ("Budi", 3),
    ("Ani", 0),
    ("Citra", 2),
    ("Dedi", 0),
    ("Eka", 1)
]

pq = BPriorityQueue(4)
for n,p in patients:
    pq.enqueue(n,p)

# ===== STATE =====
calling = None
called = []
paused = True
finished = False

target_x, target_y = 720, 260
speed = 0.05

# ===== BUTTON =====
play_btn = pygame.Rect(550,80,100,40)
stop_btn = pygame.Rect(670,80,100,40)
reset_btn = pygame.Rect(790,80,100,40)

def reset():
    global calling, called, pq, paused, finished

    pq = BPriorityQueue(4)
    for n,p in patients:
        pq.enqueue(n,p)

    calling = None
    called = []
    paused = True
    finished = False

def get_next():
    return pq.dequeue()

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

            if stop_btn.collidepoint(mouse):
                paused = True

            if reset_btn.collidepoint(mouse):
                reset()

    # ===== LOGIC =====
    if not paused and not finished:

        if calling is None:
            name, prio = get_next()
            if name:
                calling = [name, prio, 80, 300]

        if calling:
            cx, cy = calling[2], calling[3]

            cx += (target_x - cx) * speed
            cy += (target_y - cy) * speed

            calling[2], calling[3] = cx, cy

            if abs(cx - target_x) < 2:
                called.append(calling)
                calling = None

        # ===== CEK SELESAI =====
        if pq.isEmpty() and calling is None:
            finished = True
            paused = True

    # ===== STATUS =====
    if finished:
        status = "SELESAI"
    elif paused:
        status = "PAUSED"
    else:
        status = "RUNNING"

    # ===== HEADER =====
    pygame.draw.rect(screen, HEADER, (0,0,WIDTH,60))
    screen.blit(title_font.render("Antrian Rumah Sakit (Priority Qeueue)",True,TEXT),(20,15))

    # ===== BUTTON =====
    pygame.draw.rect(screen, BTN_GREEN, play_btn, border_radius=8)
    pygame.draw.rect(screen, BTN_BLUE, stop_btn, border_radius=8)
    pygame.draw.rect(screen, BTN_RED, reset_btn, border_radius=8)

    screen.blit(font.render("PLAY",True,(255,255,255)),(575,90))
    screen.blit(font.render("STOP",True,(255,255,255)),(695,90))
    screen.blit(font.render("RESET",True,(255,255,255)),(805,90))

    # ===== LEGEND =====
    pygame.draw.rect(screen, PANEL, (20,120,300,180), border_radius=10)
    screen.blit(font.render("KETERANGAN PRIORITAS",True,TEXT),(30,130))

    y = 160
    for p in range(4):
        pygame.draw.circle(screen, PRIORITY_COLOR[p], (40,y), 10)
        screen.blit(font.render(f"{PRIORITY_TEXT[p]} ({p})",True,TEXT),(60,y-8))
        y += 30

    # ===== ANTRIAN =====
    screen.blit(font.render("ANTRIAN PASIEN",True,TEXT),(360,120))

    for i,(name,prio) in enumerate(patients):
        if name in [c[0] for c in called]:
            continue

        x = 380
        y = 160 + i*50

        pygame.draw.circle(screen, PRIORITY_COLOR[prio], (x,y), 20)
        screen.blit(font.render(name,True,TEXT),(x+40,y-10))
        screen.blit(font.render(PRIORITY_TEXT[prio],True,(180,180,180)),(x+40,y+10))

    # ===== PASIEN BERGERAK =====
    if calling:
        pygame.draw.circle(
            screen,
            PRIORITY_COLOR[calling[1]],
            (int(calling[2]), int(calling[3])),
            25
        )
        screen.blit(font.render(calling[0],True,TEXT),
                    (int(calling[2])+30,int(calling[3])-10))

    # ===== DOKTER =====
    pygame.draw.rect(screen,(40,40,40),(650,160,300,300),border_radius=10)
    screen.blit(font.render("DOKTER",True,TEXT),(760,140))

    # ===== SELESAI =====
    screen.blit(font.render("SUDAH DILAYANI",True,TEXT),(680,180))

    for i,p in enumerate(called):
        pygame.draw.circle(screen, PRIORITY_COLOR[p[1]], (700,220+i*40), 15)
        screen.blit(font.render(p[0],True,TEXT),(720,210+i*40))

    # ===== STATUS =====
    screen.blit(font.render(f"STATUS: {status}",True,TEXT),(650,480))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()