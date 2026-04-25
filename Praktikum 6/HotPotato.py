import pygame
import sys
import math

pygame.init()

WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Kasus 2")

# ===== COLORS =====
BG = (30,30,30)
TEXT = (240,240,240)
PANEL = (50,50,50)
HEADER = (70,60,120)
BTN_GREEN = (100,190,130)
BTN_BLUE = (90,140,230)
BTN_RED = (220,80,80)

font = pygame.font.SysFont("consolas",16)  
title_font = pygame.font.SysFont("arial",26,True)

clock = pygame.time.Clock()

# ===== INPUT =====
input_box = pygame.Rect(50,80,450,35)
user_text = ""
active_input = False

# ===== DATA =====
players_init = []
players = []

colors = [
    (255,100,100),(100,200,255),(255,200,100),
    (180,120,255),(120,255,180),(255,150,200)
]

num = 5

# ===== LOG SCROLL =====
logs = []
log_scroll = 0
max_visible_logs = 8

def reset():
    global players, current_index, counter, logs, paused
    global moving, potato_pos, target_pos, next_index, log_scroll

    players = players_init.copy()
    current_index = 0
    counter = 0
    logs = []
    log_scroll = 0
    paused = True

    moving = False
    potato_pos = None
    target_pos = None
    next_index = 0

def add_log(t):
    logs.append(t)

# ===== BUTTON =====
play_btn = pygame.Rect(550,140,100,40)
stop_btn = pygame.Rect(670,140,100,40)
reset_btn = pygame.Rect(790,140,100,40)

reset()

running = True
while running:
    screen.fill(BG)
    mouse = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            active_input = input_box.collidepoint(mouse)

            if play_btn.collidepoint(mouse):
                paused = False
            if stop_btn.collidepoint(mouse):
                paused = True
            if reset_btn.collidepoint(mouse):
                reset()

        # ===== INPUT SCROLL LOG =====
        if event.type == pygame.MOUSEWHEEL:
            log_scroll -= event.y
            log_scroll = max(0, min(log_scroll, max(0, len(logs) - max_visible_logs)))

        if event.type == pygame.KEYDOWN and active_input:
            if event.key == pygame.K_RETURN:
                names = [x.strip() for x in user_text.split(",") if x.strip()]
                names = names[:10]

                if len(names) >= 2:
                    players_init = names
                    reset()

                user_text = ""

            elif event.key == pygame.K_BACKSPACE:
                user_text = user_text[:-1]
            else:
                user_text += event.unicode

    # ===== POSISI LINGKARAN =====
    center_x, center_y = 300, 350
    radius = 150

    positions = []
    total = len(players)

    for i in range(total):
        angle = 2 * math.pi * i / total
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        positions.append((x,y))

    # ===== LOGIKA =====
    if not paused and len(players) > 1:

        if not moving:
            next_index = (current_index + 1) % len(players)
            potato_pos = positions[current_index]
            target_pos = positions[next_index]
            moving = True

        if moving:
            px, py = potato_pos
            tx, ty = target_pos

            px += (tx - px) * 0.1
            py += (ty - py) * 0.1
            potato_pos = (px, py)

            if abs(px - tx) < 2 and abs(py - ty) < 2:
                current_index = next_index
                add_log(f"oper: {players[current_index]}")
                counter += 1
                moving = False

                if counter == num:
                    out = players.pop(current_index)
                    add_log(f"TERSINGKIR: {out}")
                    counter = 0

                    if current_index >= len(players):
                        current_index = 0

    # ===== HEADER =====
    pygame.draw.rect(screen, HEADER, (0,0,WIDTH,60))
    screen.blit(title_font.render("Permainan Hot Potato",True,(255,255,255)),(30,15))

    # ===== INPUT =====
    pygame.draw.rect(screen,(70,70,70),input_box,border_radius=6)
    screen.blit(font.render(user_text,True,TEXT),(input_box.x+5,input_box.y+8))

    screen.blit(font.render("Nama (pisah koma, max 10)",True,(180,180,180)),(50,120))

    if len(players) == 0:
        msg = font.render("Masukkan nama lalu ENTER (min 2 pemain)",True,(200,200,200))
        screen.blit(msg,(50,170))

    # ===== PEMAIN =====
    for i,p in enumerate(players):
        x,y = positions[i]

        color = colors[i % len(colors)]
        if i == current_index:
            color = (255,170,100)

        pygame.draw.circle(screen,color,(int(x),int(y)),30)

        label = font.render(p, True, (255,255,255))
        text_rect = label.get_rect(center=(x, y))
        screen.blit(label, text_rect)

    # ===== KENTANG =====
    if moving and potato_pos:
        pygame.draw.circle(screen,(255,200,0),(int(potato_pos[0]),int(potato_pos[1]-50)),10)
    elif players:
        px,py = positions[current_index]
        pygame.draw.circle(screen,(255,200,0),(int(px),int(py-50)),10)

    # ===== STATUS =====
    if len(players) == 1:
        status = f"Pemenang: {players[0]}"
    else:
        status = "Paused" if paused else "Berjalan"

    screen.blit(font.render(status,True,TEXT),(650,200))

    # ===== LOG PANEL =====
    panel_rect = pygame.Rect(500,300,450,200)
    pygame.draw.rect(screen,PANEL,panel_rect,border_radius=10)

    screen.blit(font.render("Log Proses",True,TEXT),(510,310))

    # SURFACE KHUSUS (INI KUNCI FIX)
    log_surface = pygame.Surface((430,160))
    log_surface.fill(PANEL)

    start = log_scroll
    end = start + max_visible_logs
    visible_logs = logs[start:end]

    for i, log in enumerate(visible_logs):
       text_img = font.render(log, True, TEXT)
       log_surface.blit(text_img, (0, i * 20))

    # tempel ke panel (biar tidak keluar box)
    screen.blit(log_surface, (510, 335))

    # ===== BUTTON =====
    pygame.draw.rect(screen,BTN_GREEN,play_btn,border_radius=10)
    pygame.draw.rect(screen,BTN_BLUE,stop_btn,border_radius=10)
    pygame.draw.rect(screen,BTN_RED,reset_btn,border_radius=10)

    screen.blit(font.render("Play",True,(255,255,255)),(575,150))
    screen.blit(font.render("Stop",True,(255,255,255)),(695,150))
    screen.blit(font.render("Reset",True,(255,255,255)),(810,150))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()