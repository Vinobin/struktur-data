import pygame
import sys

pygame.init()

# ===== WINDOW =====
WIDTH, HEIGHT = 1000, 520
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Kasus 1")

# ===== COLORS (DARK MODE) =====
BG = (30, 30, 30)
PRIMARY = (100, 190, 130)
ACCENT = (150, 210, 170)
TEXT = (240, 240, 240)
PANEL = (50, 50, 50)
BUTTON = (220, 80, 80)
BTN_BLUE = (90, 140, 230)
BTN_GREEN = (100, 190, 130)
HEADER = (70, 60, 120)

# ===== FONT =====
font = pygame.font.SysFont("consolas", 18)
title_font = pygame.font.SysFont("arial", 26, bold=True)

clock = pygame.time.Clock()

# ===== BOX =====
class Box:
    def __init__(self, text, x):
        self.text = text
        self.padding = 20

        text_surface = font.render(self.text, True, TEXT)
        self.width = text_surface.get_width() + self.padding

        self.height = 55
        self.x = x
        self.y = 200
        self.target_x = x

    def update(self):
        self.x += (self.target_x - self.x) * 0.12

    def draw(self):
        color = PRIMARY
        if self == printing:
            color = (255, 170, 100)  # highlight printing

        pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height), border_radius=12)

        label = font.render(self.text, True, (255, 255, 255))
        screen.blit(label, (self.x + 10, self.y + 18))

# ===== DATA =====
docs = ["laporan.pdf", "tugas.docx", "foto.jpg"]

def reset_simulation():
    global queue, doc_index, printing, timer, logs, scroll_offset, paused
    queue = []
    doc_index = 0
    printing = None
    timer = 0
    logs = []
    scroll_offset = 0
    paused = True

reset_simulation()

def add_log(text):
    logs.append(text)

# ===== QUEUE =====
def enqueue():
    global doc_index
    if doc_index < len(docs):
        x = 80
        if queue:
            last = queue[-1]
            x = last.target_x + last.width + 15

        queue.append(Box(docs[doc_index], x))
        add_log(f"enqueue: {docs[doc_index]}")
        doc_index += 1

def dequeue():
    global printing
    if queue and printing is None:
        printing = queue.pop(0)
        printing.target_x = 750
        add_log(f"dequeue: {printing.text}")
        add_log(f"Mencetak: {printing.text}")

def update_positions():
    current_x = 80
    for box in queue:
        box.target_x = current_x
        current_x += box.width + 15

# ===== SCROLL =====
scroll_offset = 0
line_height = 22
max_visible = 5

# ===== BUTTON =====
reset_btn = pygame.Rect(850, 70, 100, 40)
stop_btn = pygame.Rect(720, 70, 100, 40)
play_btn = pygame.Rect(590, 70, 100, 40)

paused = True

# ===== MAIN LOOP =====
running = True
while running:
    screen.fill(BG)
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if reset_btn.collidepoint(mouse_pos):
                reset_simulation()
            if stop_btn.collidepoint(mouse_pos):
                paused = True
            if play_btn.collidepoint(mouse_pos):
                paused = False

        if event.type == pygame.MOUSEWHEEL:
            scroll_offset -= event.y

    if not paused:
        timer += 1

        if timer % 120 == 0:
            enqueue()

        if timer % 200 == 0:
            dequeue()

    update_positions()

    # ===== HEADER =====
    pygame.draw.rect(screen, HEADER, (0, 0, WIDTH, 60))
    title = title_font.render("Antrian Printer Bersama", True, (255, 255, 255))
    screen.blit(title, (30, 15))

    # ===== QUEUE =====
    for box in queue:
        box.update()
        box.draw()

    # ===== PRINTING =====
    if printing:
        printing.update()
        printing.draw()
        if abs(printing.x - printing.target_x) < 1:
            printing = None

    # ===== PRINTER =====
    pygame.draw.rect(screen, ACCENT, (750, 170, 140, 90), border_radius=15)
    label = font.render("PRINTER", True, (0, 0, 0))
    screen.blit(label, (780, 205))

    status = "Paused" if paused else ("Menunggu" if printing is None else "Mencetak...")
    status_text = font.render(f"Status: {status}", True, TEXT)
    screen.blit(status_text, (750, 270))

    # ===== LOG PANEL =====
    log_rect = pygame.Rect(60, 330, 880, 150)
    pygame.draw.rect(screen, PANEL, log_rect, border_radius=12)

    log_title = font.render("Log Proses", True, TEXT)
    screen.blit(log_title, (70, 340))

    max_scroll = max(0, len(logs) - max_visible)
    scroll_offset = max(0, min(scroll_offset, max_scroll))

    clip_rect = pygame.Rect(70, 365, 860, 110)
    screen.set_clip(clip_rect)

    visible_logs = logs[scroll_offset:scroll_offset + max_visible]

    for i, log in enumerate(visible_logs):
        text = font.render(log, True, TEXT)
        screen.blit(text, (70, 370 + i * line_height))

    screen.set_clip(None)

    # ===== BUTTON =====
    pygame.draw.rect(screen, BUTTON, reset_btn, border_radius=10)
    pygame.draw.rect(screen, BTN_BLUE, stop_btn, border_radius=10)
    pygame.draw.rect(screen, BTN_GREEN, play_btn, border_radius=10)

    screen.blit(font.render("Reset", True, (255,255,255)), (870, 80))
    screen.blit(font.render("Stop", True, (255,255,255)), (745, 80))
    screen.blit(font.render("Play", True, (255,255,255)), (615, 80))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()