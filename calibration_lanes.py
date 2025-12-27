
import pygame
import sys

# -------------------------------
# Initialize pygame
# -------------------------------
pygame.init()

# -------------------------------
# Window setup
# -------------------------------
WIDTH, HEIGHT = 1000, 800   # adjust if your image is different
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lane Calibration Mode")

clock = pygame.time.Clock()
FPS = 60

# -------------------------------
# Load background image
# -------------------------------
background = pygame.image.load("lanesystem.png").convert_alpha()
bg_rect = background.get_rect(topleft=(0, 0))

# -------------------------------
# Font for mouse coordinates
# -------------------------------
font = pygame.font.SysFont(None, 24)

# -------------------------------
# INITIAL lane rectangle guesses
# (You will MODIFY these values)
# -------------------------------

# Vertical road (A → C)
AL1_RECT = pygame.Rect(440, 0, 40, 287)
AL2_RECT = pygame.Rect(480, 0, 40, 287)
AL3_RECT = pygame.Rect(520, 0, 40, 287)

BL1_RECT = pygame.Rect(440, 420, 40, 380)
BL2_RECT = pygame.Rect(480, 420, 40, 380)
BL3_RECT = pygame.Rect(520, 420, 40, 380)


# LEFT road → Lane D (horizontal → right)
DL1_RECT = pygame.Rect(0, 284, 420, 40)
DL2_RECT = pygame.Rect(0, 340, 420, 40)
DL3_RECT = pygame.Rect(0, 387, 420, 40)

# RIGHT road → Lane C (horizontal ← left)
CL1_RECT = pygame.Rect(572, 285, 480, 40)
CL2_RECT = pygame.Rect(572, 338, 480, 40)
CL3_RECT = pygame.Rect(572, 384, 480, 40)


lane_rects = {
    # Top
    "AL1": AL1_RECT, "AL2": AL2_RECT, "AL3": AL3_RECT,

    # Bottom
    "BL1": BL1_RECT, "BL2": BL2_RECT, "BL3": BL3_RECT,

    # Right
    "CL1": CL1_RECT, "CL2": CL2_RECT, "CL3": CL3_RECT,

    # Left
    "DL1": DL1_RECT, "DL2": DL2_RECT, "DL3": DL3_RECT,
}


# -------------------------------
# Traffic light rectangles
# (Each road has RED + GREEN)
# -------------------------------

# Road A (top → down)
LIGHT_A_GREEN = pygame.Rect(572, 202, 70, 40)
LIGHT_A_RED   = pygame.Rect(572, 247, 70, 40)

# Road B (left → right)
LIGHT_B_GREEN = pygame.Rect(347, 475, 70, 36)
LIGHT_B_RED   = pygame.Rect(356, 433, 70, 36)

# Road C (bottom → up)
LIGHT_C_GREEN = pygame.Rect(620, 432, 36, 70)
LIGHT_C_RED   = pygame.Rect(579, 437, 36, 64)

# Road D (right → left)
LIGHT_D_GREEN = pygame.Rect(341, 222, 36, 64)
LIGHT_D_RED   = pygame.Rect(377, 225, 36, 64)

light_rects = {
    "A": {"GREEN": LIGHT_A_GREEN, "RED": LIGHT_A_RED},
    "B": {"GREEN": LIGHT_B_GREEN, "RED": LIGHT_B_RED},
    "C": {"GREEN": LIGHT_C_GREEN, "RED": LIGHT_C_RED},
    "D": {"GREEN": LIGHT_D_GREEN, "RED": LIGHT_D_RED},
}


# -------------------------------
# Colors
# -------------------------------
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

# -------------------------------
# Main loop
# -------------------------------
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear screen
    screen.fill((0, 0, 0))

    # Draw background
    screen.blit(background, bg_rect)

    # Draw lane overlays
    for lane, rect in lane_rects.items():
        color = YELLOW if lane == "AL2" else RED  # highlight priority lane
        pygame.draw.rect(screen, color, rect, 2)

        # Draw lane label
        label = font.render(lane, True, WHITE)
        screen.blit(label, (rect.x + 5, rect.y + 5))
    # Draw traffic light overlays
    # Draw traffic light overlays
    for road, lights in light_rects.items():
       pygame.draw.rect(screen, (0, 255, 0), lights["GREEN"], 2)
       pygame.draw.rect(screen, (255, 0, 0), lights["RED"], 2)

       label = font.render(f"Light {road}", True, WHITE)
       screen.blit(label, (lights["GREEN"].x - 5, lights["GREEN"].y - 20))


    # Show mouse coordinates
    mouse_x, mouse_y = pygame.mouse.get_pos()
    coord_text = font.render(f"Mouse: ({mouse_x}, {mouse_y})", True, WHITE)
    screen.blit(coord_text, (10, 10))

    # Update display
    pygame.display.flip()
    clock.tick(FPS)

# -------------------------------
# Exit cleanly
# -------------------------------
pygame.quit()
sys.exit()
