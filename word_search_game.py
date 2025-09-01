import pygame
import random
import string
import math

# --- Constants and Configuration ---

# Screen Dimensions
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 750
UI_WIDTH = 250

# Grid Configuration
GRID_SIZE = 15  # 15x15 grid
CELL_SIZE = 40
GRID_WIDTH = GRID_SIZE * CELL_SIZE
GRID_HEIGHT = GRID_SIZE * CELL_SIZE
GRID_X_OFFSET = 50
GRID_Y_OFFSET = 50

# Colors (Creative Theme: "Cosmic Neon")
COLOR_BACKGROUND = (5, 10, 20)      # Deep space blue
COLOR_GRID_LINES = (40, 60, 80)     # Faint nebula lines
COLOR_LETTER = (200, 220, 255)      # Bright star white
COLOR_WORD_LIST = (220, 220, 220)   # Info panel text
COLOR_HIGHLIGHT = (0, 150, 255, 100) # Semi-transparent selection blue (with alpha)
COLOR_FOUND = (0, 255, 150, 150)    # Semi-transparent found green (with alpha)
COLOR_TITLE = (0, 255, 150)         # Neon green for titles
COLOR_STRIKETHROUGH = (255, 50, 50) # Red for found words

# Fonts
pygame.font.init()
FONT_LETTER = pygame.font.SysFont('Consolas', 28, bold=True)
FONT_UI = pygame.font.SysFont('Calibri', 24)
FONT_TITLE = pygame.font.SysFont('Impact', 40)
FONT_WIN = pygame.font.SysFont('Impact', 80)

# Word List (Theme: Space Exploration)
WORDS_TO_FIND = [
    "PLANET", "STAR", "GALAXY", "NEBULA", "COSMOS", "ROCKET", "ORBIT",
    "ASTEROID", "COMET", "ALIEN", "SATURN", "JUPITER", "VENUS"
]

# --- Helper Functions ---

def generate_word_search(words, size):
    """Generates the grid and places the words."""
    grid = [['' for _ in range(size)] for _ in range(size)]
    placed_words = {}

    # Directions: (row_change, col_change)
    # N, NE, E, SE, S, SW, W, NW
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]

    for word in sorted(words, key=len, reverse=True):
        word = word.upper()
        placed = False
        attempts = 0
        while not placed and attempts < 100:
            attempts += 1
            direction = random.choice(directions)
            row_start = random.randint(0, size - 1)
            col_start = random.randint(0, size - 1)

            row_end = row_start + (len(word) - 1) * direction[0]
            col_end = col_start + (len(word) - 1) * direction[1]

            if 0 <= row_end < size and 0 <= col_end < size:
                # Check if the path is clear
                can_place = True
                temp_coords = []
                for i in range(len(word)):
                    r = row_start + i * direction[0]
                    c = col_start + i * direction[1]
                    temp_coords.append((r, c))
                    if grid[r][c] != '' and grid[r][c] != word[i]:
                        can_place = False
                        break
                
                # If clear, place the word
                if can_place:
                    for i in range(len(word)):
                        r, c = temp_coords[i]
                        grid[r][c] = word[i]
                    placed_words[word] = {'start': (row_start, col_start), 'end': (row_end, col_end), 'found': False}
                    placed = True
    
    # Fill remaining empty cells with random letters
    for r in range(size):
        for c in range(size):
            if grid[r][c] == '':
                grid[r][c] = random.choice(string.ascii_uppercase)
                
    return grid, placed_words

def get_cell_from_mouse(pos):
    """Converts mouse coordinates to grid cell coordinates."""
    x, y = pos
    if GRID_X_OFFSET <= x < GRID_X_OFFSET + GRID_WIDTH and \
       GRID_Y_OFFSET <= y < GRID_Y_OFFSET + GRID_HEIGHT:
        row = (y - GRID_Y_OFFSET) // CELL_SIZE
        col = (x - GRID_X_OFFSET) // CELL_SIZE
        return row, col
    return None

def get_cells_in_line(start_cell, end_cell):
    """Gets all cells in a straight or diagonal line between two cells."""
    if start_cell is None or end_cell is None:
        return []

    r1, c1 = start_cell
    r2, c2 = end_cell
    
    cells = []
    dr = r2 - r1
    dc = c2 - c1
    
    # Check for straight or perfect diagonal lines
    if dr == 0 or dc == 0 or abs(dr) == abs(dc):
        steps = max(abs(dr), abs(dc))
        if steps == 0:
            return [(r1, c1)]
            
        r_step = dr // steps
        c_step = dc // steps
        
        for i in range(steps + 1):
            cells.append((r1 + i * r_step, c1 + i * c_step))
        return cells
    return []

# --- Drawing Functions ---

def draw_grid(screen, grid):
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            rect = pygame.Rect(
                GRID_X_OFFSET + c * CELL_SIZE,
                GRID_Y_OFFSET + r * CELL_SIZE,
                CELL_SIZE, CELL_SIZE
            )
            pygame.draw.rect(screen, COLOR_GRID_LINES, rect, 1)
            letter_surf = FONT_LETTER.render(grid[r][c], True, COLOR_LETTER)
            letter_rect = letter_surf.get_rect(center=rect.center)
            screen.blit(letter_surf, letter_rect)

def draw_ui(screen, word_data):
    # Draw UI background
    ui_rect = pygame.Rect(SCREEN_WIDTH - UI_WIDTH, 0, UI_WIDTH, SCREEN_HEIGHT)
    pygame.draw.rect(screen, (10, 20, 40), ui_rect)
    pygame.draw.line(screen, COLOR_TITLE, (SCREEN_WIDTH - UI_WIDTH, 0), (SCREEN_WIDTH - UI_WIDTH, SCREEN_HEIGHT), 3)

    # Draw Title
    title_surf = FONT_TITLE.render("WORDS TO FIND", True, COLOR_TITLE)
    screen.blit(title_surf, (SCREEN_WIDTH - UI_WIDTH + 20, 20))

    # Draw Word List
    y_pos = 80
    for word, data in word_data.items():
        color = COLOR_STRIKETHROUGH if data['found'] else COLOR_WORD_LIST
        word_surf = FONT_UI.render(word, True, color)
        screen.blit(word_surf, (SCREEN_WIDTH - UI_WIDTH + 30, y_pos))
        if data['found']:
            pygame.draw.line(
                screen, COLOR_STRIKETHROUGH,
                (SCREEN_WIDTH - UI_WIDTH + 25, y_pos + 12),
                (SCREEN_WIDTH - UI_WIDTH + 35 + word_surf.get_width(), y_pos + 12),
                3
            )
        y_pos += 30

def draw_selection(screen, selected_cells):
    if not selected_cells:
        return
    highlight_surf = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
    highlight_surf.fill(COLOR_HIGHLIGHT)
    for r, c in selected_cells:
        screen.blit(highlight_surf, (GRID_X_OFFSET + c * CELL_SIZE, GRID_Y_OFFSET + r * CELL_SIZE))

def draw_found_words(screen, word_data):
    for word, data in word_data.items():
        if data['found']:
            start_pos = (
                GRID_X_OFFSET + data['start'][1] * CELL_SIZE + CELL_SIZE // 2,
                GRID_Y_OFFSET + data['start'][0] * CELL_SIZE + CELL_SIZE // 2
            )
            end_pos = (
                GRID_X_OFFSET + data['end'][1] * CELL_SIZE + CELL_SIZE // 2,
                GRID_Y_OFFSET + data['end'][0] * CELL_SIZE + CELL_SIZE // 2
            )
            # Draw a thick, semi-transparent line over the found word
            pygame.draw.line(screen, COLOR_FOUND, start_pos, end_pos, 15)

def draw_win_screen(screen):
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))
    
    win_text = FONT_WIN.render("YOU WIN!", True, COLOR_TITLE)
    win_rect = win_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50))
    screen.blit(win_text, win_rect)
    
    sub_text = FONT_UI.render("Congratulations, Space Explorer!", True, COLOR_WORD_LIST)
    sub_rect = sub_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 30))
    screen.blit(sub_text, sub_rect)


# --- Main Game ---

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Cosmic Word Search")
    clock = pygame.time.Clock()

    grid, word_data = generate_word_search(WORDS_TO_FIND, GRID_SIZE)
    
    selecting = False
    start_cell = None
    end_cell = None
    selected_cells = []
    
    game_over = False

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if game_over:
                continue

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Left click
                    start_cell = get_cell_from_mouse(event.pos)
                    if start_cell:
                        selecting = True
                        end_cell = start_cell
            
            if event.type == pygame.MOUSEMOTION:
                if selecting:
                    end_cell = get_cell_from_mouse(event.pos) or end_cell
            
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and selecting:
                    selecting = False
                    
                    # Form the word from selected cells
                    current_selection_cells = get_cells_in_line(start_cell, end_cell)
                    if current_selection_cells:
                        selected_word = "".join([grid[r][c] for r, c in current_selection_cells])
                        
                        # Check if the word or its reverse is in our list
                        if selected_word in word_data and not word_data[selected_word]['found']:
                            word_data[selected_word]['found'] = True
                        elif selected_word[::-1] in word_data and not word_data[selected_word[::-1]]['found']:
                            word_data[selected_word[::-1]]['found'] = True

                    start_cell, end_cell = None, None
        
        # --- Update selection visualization ---
        if selecting:
            selected_cells = get_cells_in_line(start_cell, end_cell)
        else:
            selected_cells = []

        # --- Check for win condition ---
        if not game_over and all(data['found'] for data in word_data.values()):
            game_over = True

        # --- Drawing ---
        screen.fill(COLOR_BACKGROUND)
        
        draw_grid(screen, grid)
        draw_found_words(screen, word_data)
        draw_selection(screen, selected_cells)
        draw_ui(screen, word_data)
        
        if game_over:
            draw_win_screen(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()