import pygame
import random
import time
import os
import sys

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Constants
WINDOW_WIDTH, WINDOW_HEIGHT = 500, 800
BLOCK_SIZE = 20
FPS = 60

# Colors (index corresponds to your original color list)
COLORS = [
    (0, 0, 0),           # Black
    (0, 191, 255),       # DeepSkyBlue3
    (0, 0, 139),         # DodgerBlue4
    (255, 165, 0),       # Orange
    (255, 215, 0),       # Gold
    (0, 100, 0),         # Green4
    (147, 112, 219),     # MediumPurple2
    (178, 34, 34),       # Firebrick3
    (231, 92, 36),       # Custom color matching bg
    (245, 245, 245)      # Snow2
]

# Fonts
FONT_SMALL = pygame.font.SysFont('fixedsys', 16)
FONT_MEDIUM = pygame.font.SysFont('fixedsys', 30)
FONT_LARGE = pygame.font.SysFont('fixedsys', 40)

# Load Images
try:
    BG_IMAGE = pygame.image.load('bg.png')
    BG_IMAGE = pygame.transform.scale(BG_IMAGE, (WINDOW_WIDTH, WINDOW_HEIGHT))
except pygame.error as e:
    print(f"Error loading bg.png: {e}")
    sys.exit()

# Initialize Screen
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("TETRIS")
clock = pygame.time.Clock()

# Load Background Music (Optional)
# Uncomment and ensure you have a 'music.wav' file
# try:
#     pygame.mixer.music.load('music.wav')
#     pygame.mixer.music.play(-1)
# except pygame.error:
#     pass

# Leaderboard File
LEADERBOARD_FILE = "leaderboard.txt"

# Shapes Definitions
SHAPES = {
    'square': [[1, 1],
               [1, 1]],
    'horizontal': [[1, 1, 1, 1]],
    'vertical': [[1],
                [1],
                [1],
                [1]],
    'Lleft': [[1, 0, 0],
              [1, 1, 1]],
    'Lright': [[0, 0, 1],
               [1, 1, 1]],
    'Zright': [[0, 1, 1],
               [1, 1, 0]],
    'Zleft': [[1, 1, 0],
              [0, 1, 1]],
    'T': [[0, 1, 0],
          [1, 1, 1]]
}

# Global Variables
delay = 0.06
grid = [
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [8,0,0,0,0,0,0,0,0,0,0,0,0,8],
    [8,0,0,0,0,0,0,0,0,0,0,0,0,8],
    [8,0,0,0,0,0,0,0,0,0,0,0,0,8],
    [8,0,0,0,0,0,0,0,0,0,0,0,0,8],
    [8,0,0,0,0,0,0,0,0,0,0,0,0,8],
    [8,0,0,0,0,0,0,0,0,0,0,0,0,8],
    [8,0,0,0,0,0,0,0,0,0,0,0,0,8],
    [8,0,0,0,0,0,0,0,0,0,0,0,0,8],
    [8,0,0,0,0,0,0,0,0,0,0,0,0,8],
    [8,0,0,0,0,0,0,0,0,0,0,0,0,8],
    [8,0,0,0,0,0,0,0,0,0,0,0,0,8],
    [8,0,0,0,0,0,0,0,0,0,0,0,0,8],
    [8,0,0,0,0,0,0,0,0,0,0,0,0,8],
    [8,0,0,0,0,0,0,0,0,0,0,0,0,8],
    [8,0,0,0,0,0,0,0,0,0,0,0,0,8],
    [8,0,0,0,0,0,0,0,0,0,0,0,0,8],
    [8,0,0,0,0,0,0,0,0,0,0,0,0,8],
    [8,0,0,0,0,0,0,0,0,0,0,0,0,8],
    [8,0,0,0,0,0,0,0,0,0,0,0,0,8],
    [8,8,8,8,8,8,8,8,8,8,8,8,8,8],
]
shapes_list = list(SHAPES.values())

score = 0
run = True
pause = True
p = 0
wiggle = False
event_clear = False
first_run = True
name = ''
has_run = False
temp_surface = None

# Fonts
pygame.font.init()
font_large = pygame.font.SysFont('fixedsys', 40)
font_medium = pygame.font.SysFont('fixedsys', 30)
font_small = pygame.font.SysFont('fixedsys', 16)

# Load Sounds (Optional)
# Uncomment and ensure you have 'beep.wav' and 'beep2.wav'
# try:
#     beep_sound = pygame.mixer.Sound('beep.wav')
#     beep2_sound = pygame.mixer.Sound('beep2.wav')
# except pygame.error:
#     beep_sound = None
#     beep2_sound = None

# Shape Class
class Shape:
    def __init__(self):
        self.x = 6
        self.y = 0
        self.color = random.randint(1,7)
        self.counter = 0
        self.shape = random.choice(shapes_list)
        self.height = len(self.shape)
        self.width = len(self.shape[0])

    def move_left(self, grid):
        if self.x > 0 and self.can_move(grid, dx=-1):
            self.x -= 1

    def move_right(self, grid):
        if self.x < 13 - self.width and self.can_move(grid, dx=1):
            self.x += 1

    def draw_shape(self, grid):
        for y in range(self.height):
            for x in range(self.width):
                if self.shape[y][x] == 1:
                    grid[self.y + y][self.x + x] = self.color

    def erase_shape(self, grid):
        for y in range(self.height):
            for x in range(self.width):
                if self.shape[y][x] == 1:
                    grid[self.y + y][self.x + x] = 0

    def can_move(self, grid, dy=1, dx=0):
        for y in range(self.height):
            for x in range(self.width):
                if self.shape[y][x] == 1:
                    new_x = self.x + x + dx
                    new_y = self.y + y + dy
                    if new_x < 0 or new_x >= 14 or new_y >= 24:
                        return False
                    if grid[new_y][new_x] != 0:
                        return False
        return True

    def rotate(self, grid):
        global wiggle
        self.counter +=1
        if self.counter >10:
            wiggle = True
        rotated_shape = list(zip(*self.shape[::-1]))
        rotated_shape = [list(row) for row in rotated_shape]
        new_height = len(rotated_shape)
        new_width = len(rotated_shape[0])
        if self.x + new_width > 14:
            return
        # Check collision
        for y in range(new_height):
            for x in range(new_width):
                if rotated_shape[y][x] == 1:
                    if self.y + y >= len(grid) or self.x + x >= len(grid[0]) or self.y + y < 0 or self.x + x <0:
                        return
                    if grid[self.y + y][self.x + x] !=0:
                        return
        self.erase_shape(grid)
        self.shape = rotated_shape
        self.height = new_height
        self.width = new_width
        self.draw_shape(grid)
        # Play sound if implemented
        # if beep_sound:
        #     beep_sound.play()

# Functions
def draw_grid_pygame(grid, upcoming_shape):
    screen.blit(BG_IMAGE, (0,0))

    # Draw Grid
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            color_num = grid[y][x]
            color = COLORS[color_num]
            pygame.draw.rect(screen, color, (50 + x*BLOCK_SIZE, 50 + y*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(screen, (40,40,40), (50 + x*BLOCK_SIZE, 50 + y*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),1)

    # Draw Upcoming Shape
    draw_upcoming(upcoming_shape)

    # Draw Score
    score_text = font_medium.render(f"Score: {score}", True, (255,255,255))
    screen.blit(score_text, (50, 30))

def draw_upcoming(shape):
    top = 270
    right = 350
    for y in range(shape.height):
        for x in range(shape.width):
            if shape.shape[y][x] == 1:
                color = COLORS[shape.color]
                rect = pygame.Rect(right + x*BLOCK_SIZE, top + y*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, (40,40,40), rect,1)

def del_row(grid):
    global delay, score, event_clear
    rows_to_delete = []
    for y in range(len(grid)):
        if all(cell !=0 and cell !=9 for cell in grid[y]):
            rows_to_delete.append(y)

    for y in rows_to_delete:
        del grid[y]
        grid.insert(0, [8]+[0]*12+[8])
        score += 100
        # Play sound if implemented
        # if beep_sound:
        #     beep_sound.play()
        if score % 300 ==0 and delay >0.01:
            delay -=0.01
        if score %500 ==0 and score !=0:
            # Add indestructible row
            grid.pop(-2)
            grid.insert(1, [8]*14)
            score +=100
            # Play sound if implemented
            # if beep2_sound:
            #     beep2_sound.play()

def load_leaderboard():
    if not os.path.exists(LEADERBOARD_FILE):
        with open(LEADERBOARD_FILE, 'w') as f:
            f.write("AAA,100,BBB,90,CCC,80,DDD,70,EEE,60")
    with open(LEADERBOARD_FILE, 'r') as f:
        data = f.read().strip().split(',')
    leaderboard = []
    for i in range(0, len(data),2):
        try:
            leaderboard.append((data[i], int(data[i+1])))
        except IndexError:
            continue
    return leaderboard

def save_leaderboard(name, score):
    leaderboard = load_leaderboard()
    leaderboard.append((name, score))
    leaderboard = sorted(leaderboard, key=lambda x: x[1], reverse=True)[:5]
    with open(LEADERBOARD_FILE, 'w') as f:
        for entry in leaderboard:
            f.write(f"{entry[0]},{entry[1]},")

def render_text(text, font, color, surface, x, y, center=False):
    lines = text.split('\n')
    for i, line in enumerate(lines):
        textobj = font.render(line, True, color)
        textrect = textobj.get_rect()
        if center:
            textrect.center = (x, y + i * 20)
        else:
            textrect.topleft = (x, y + i * 20)
        surface.blit(textobj, textrect)

def main_menu_screen():
    global run, has_run, name
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and has_run:
                    return
        screen.fill((0,0,0))
        screen.blit(BG_IMAGE, (0,0))
        render_text("PRESS SPACE TO START", font_medium, (255,255,255), screen, WINDOW_WIDTH//2, 150, center=True)
        render_text("HIGHSCORES", font_large, (255,255,255), screen, WINDOW_WIDTH//2, 200, center=True)
        leaderboard = load_leaderboard()
        for idx, (player, pts) in enumerate(leaderboard):
            render_text(f"{player}: {pts}", font_medium, (255,255,255), screen, 90, 280 + idx*30)
        # Controls
        controls = "CONTROLS:\n← or a TO GO LEFT\n→ or d TO GO RIGHT\n↑ or w TO ROTATE\np TO PAUSE THE GAME\n(Game pauses for 3 seconds after unpause)"
        controls_lines = controls.split('\n')
        for i, line in enumerate(controls_lines):
            render_text(line, font_small, (255,255,255), screen, 50, 650 + i*20)
        # Buttons for Credits and Details
        mouse = pygame.mouse.get_pos()
        click = False
        if pygame.mouse.get_pressed()[0]:
            click = True
        # Credits Button
        if 20 <= mouse[0] <= 120 and 468 <= mouse[1] <= 500:
            pygame.draw.rect(screen, (100,100,100), (20,468,100,32))
            if click:
                credits_screen()
        else:
            pygame.draw.rect(screen, (150,150,150), (20,468,100,32))
        render_text("CREDITS", font_medium, (0,0,0), screen, 70, 480, center=True)
        # Details Button
        if 280 <= mouse[0] <= 380 and 468 <= mouse[1] <= 500:
            pygame.draw.rect(screen, (100,100,100), (280,468,100,32))
            if click:
                details_screen()
        else:
            pygame.draw.rect(screen, (150,150,150), (280,468,100,32))
        render_text("DETAILS", font_medium, (0,0,0), screen, 330, 480, center=True)
        pygame.display.update()
        clock.tick(FPS)

def credits_screen():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                return
        screen.fill((0,0,0))
        screen.blit(BG_IMAGE, (0,0))
        render_text("MADE BY:", font_large, (255,255,255), screen, 40, 320)
        render_text("AYESH AHMAD", font_large, (255,255,255), screen, 40, 350)
        # DONE Button
        mouse = pygame.mouse.get_pos()
        click = False
        if pygame.mouse.get_pressed()[0]:
            click = True
        if 160 <= mouse[0] <= 240 and 470 <= mouse[1] <= 500:
            pygame.draw.rect(screen, (100,100,100), (160,470,80,30))
            if click:
                return
        else:
            pygame.draw.rect(screen, (150,150,150), (160,470,80,30))
        render_text("DONE", font_medium, (0,0,0), screen, 200, 485, center=True)
        pygame.display.update()
        clock.tick(FPS)

def details_screen():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                return
        screen.fill((0,0,0))
        screen.blit(BG_IMAGE, (0,0))
        # Game Objective
        render_text("GAME OBJECTIVE", font_large, (255,255,255), screen, 35, 50)
        objective = ("In Tetris, your goal is to stack the blocks\ninto multiple rows and destroy them.\n\nA row is destroyed when it is full.\n\n"
                     "Collect as many points as you can before the\ngame is over to secure your position on\nthe leaderboard.\n\n"
                     "Destroying each row awards you 100 points")
        objective_lines = objective.split('\n')
        for i, line in enumerate(objective_lines):
            render_text(line, font_small, (255,255,255), screen, 35, 80 + i*20)
        # Game Obstacles
        render_text("GAME OBSTACLES", font_large, (255,255,255), screen, 35, 270)
        obstacles = ("Throughout the game you will be presented\nwith certain obstacles.\n\nEvery 300 "
                     "points, the game will become faster.\n\nEvery 500 points, an indestructible row "
                     "will be added to the bottom of the grid,\nthus reducing your space")
        obstacles_lines = obstacles.split('\n')
        for i, line in enumerate(obstacles_lines):
            render_text(line, font_small, (255,255,255), screen, 35, 300 + i*20)
        # Cheats
        render_text("CHEATS", font_large, (255,255,255), screen, 120, 470)
        cheats = ("Press 'x' to skip the upcoming block.\n\nPress 'z' to slow down the game.\n"
                  "(Visible effect at score>300)\n\nPress 'c' to destroy the bottom row\n\nPress 'ESC' "
                  "to activate the boss key.")
        cheats_lines = cheats.split('\n')
        for i, line in enumerate(cheats_lines):
            render_text(line, font_small, (255,255,255), screen, 25, 500 + i*20)
        # DONE Button
        mouse = pygame.mouse.get_pos()
        click = False
        if pygame.mouse.get_pressed()[0]:
            click = True
        if 160 <= mouse[0] <= 240 and 655 <= mouse[1] <= 685:
            pygame.draw.rect(screen, (100,100,100), (160,655,80,30))
            if click:
                return
        else:
            pygame.draw.rect(screen, (150,150,150), (160,655,80,30))
        render_text("DONE", font_medium, (0,0,0), screen, 200, 670, center=True)
        pygame.display.update()
        clock.tick(FPS)

def input_name_screen():
    global name, has_run
    active = True
    user_text = ''
    while active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if len(user_text) ==3:
                        name = user_text
                        has_run = True
                        active = False
                elif event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                else:
                    if len(user_text) <3 and event.unicode.isalnum():
                        user_text += event.unicode.upper()
        screen.fill((0,0,0))
        screen.blit(BG_IMAGE, (0,0))
        render_text("ENTER YOUR NAME", font_large, (255,255,255), screen, WINDOW_WIDTH//2, 400, center=True)
        render_text("(3 LETTERS ONLY)", font_small, (255,255,255), screen, WINDOW_WIDTH//2, 450, center=True)
        # Input Box
        pygame.draw.rect(screen, (255,255,255), (WINDOW_WIDTH//2 -50, 500, 100, 40),2)
        render_text(user_text, font_large, (255,255,255), screen, WINDOW_WIDTH//2, 520, center=True)
        pygame.display.update()
        clock.tick(FPS)

def game_over_screen():
    global score, name
    save_leaderboard(name, score)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.fill((0,0,0))
        screen.blit(BG_IMAGE, (0,0))
        render_text("Game Over!", font_large, (255,0,0), screen, WINDOW_WIDTH//2, 300, center=True)
        render_text(f"Score: {score}", font_medium, (255,255,255), screen, WINDOW_WIDTH//2, 350, center=True)
        render_text("Press Enter to Restart", font_small, (255,255,255), screen, WINDOW_WIDTH//2, 400, center=True)
        pygame.display.update()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            main()

def pause_screen():
    global pause, p
    pause_menu = True
    pause_start_time = time.time()
    while pause_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.fill((0,0,0))
        render_text("PAUSED", font_large, (255,255,255), screen, WINDOW_WIDTH//2, 400, center=True)
        render_text("PRESS 'p' TO RESUME.\nYOU WILL BE GIVEN\nTHREE SECONDS UPON\n     RESUMING.", font_small, (255,255,255), screen, WINDOW_WIDTH//2, 450, center=True)
        pygame.display.update()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_p]:
            pause_menu = False
            pause = False
            p =1
        # Implement the 3-second pause after resuming
        if not pause_menu and pause == False:
            time.sleep(3)
        clock.tick(FPS)

def main():
    global delay, grid, score, run, pause, p, wiggle, event_clear, first_run, name, has_run
    run = True
    pause = True
    p =0
    wiggle = False
    event_clear = False
    score =0
    grid = [
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [8,0,0,0,0,0,0,0,0,0,0,0,0,8],
        [8,0,0,0,0,0,0,0,0,0,0,0,0,8],
        [8,0,0,0,0,0,0,0,0,0,0,0,0,8],
        [8,0,0,0,0,0,0,0,0,0,0,0,0,8],
        [8,0,0,0,0,0,0,0,0,0,0,0,0,8],
        [8,0,0,0,0,0,0,0,0,0,0,0,0,8],
        [8,0,0,0,0,0,0,0,0,0,0,0,0,8],
        [8,0,0,0,0,0,0,0,0,0,0,0,0,8],
        [8,0,0,0,0,0,0,0,0,0,0,0,0,8],
        [8,0,0,0,0,0,0,0,0,0,0,0,0,8],
        [8,0,0,0,0,0,0,0,0,0,0,0,0,8],
        [8,0,0,0,0,0,0,0,0,0,0,0,0,8],
        [8,0,0,0,0,0,0,0,0,0,0,0,0,8],
        [8,0,0,0,0,0,0,0,0,0,0,0,0,8],
        [8,0,0,0,0,0,0,0,0,0,0,0,0,8],
        [8,0,0,0,0,0,0,0,0,0,0,0,0,8],
        [8,0,0,0,0,0,0,0,0,0,0,0,0,8],
        [8,0,0,0,0,0,0,0,0,0,0,0,0,8],
        [8,8,8,8,8,8,8,8,8,8,8,8,8,8],
    ]
    shape = Shape()
    nshape = Shape()
    pause = True
    first_run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    shape.move_left(grid)
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    shape.move_right(grid)
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    shape.rotate(grid)
                if event.key == pygame.K_p:
                    pause = True
                if event.key == pygame.K_x:
                    nshape = Shape()
                if event.key == pygame.K_z:
                    delay =0.07
                if event.key == pygame.K_c:
                    # Clear bottom row
                    for x in range(len(grid[-2])):
                        grid[-2][x] =0
                    score +=100
        if not pause:
            if shape.y ==23 - shape.height +1 or not shape.can_move(grid):
                if shape.y ==0:
                    game_over_screen()
                else:
                    shape.draw_shape(grid)
                    shape = nshape
                    nshape = Shape()
                    del_row(grid)
            if shape.can_move(grid):
                shape.y +=1
            else:
                shape.draw_shape(grid)
                shape = nshape
                nshape = Shape()
                del_row(grid)
            score +=1
            draw_grid_pygame(grid, nshape)
            pygame.display.update()
            time.sleep(delay)
        else:
            pause_screen()
        clock.tick(FPS)

# Start the game
def start_game():
    main_menu_screen()
    input_name_screen()
    main()

if __name__ == "__main__":
    start_game()
