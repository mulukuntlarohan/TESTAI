import pygame
import random
import json
from collections import deque

# Load configuration from JSON file
def load_config(filename):
    with open(filename, 'r') as f:
        return json.load(f)

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_CELL_SIZE = 100
FPS = 30
BUTTON_HEIGHT = 40
BUTTON_WIDTH = 100

# Load assets
WUMPUS_IMG = pygame.image.load('assets/images/wumpus.png')
AGENT_IMG = pygame.image.load('assets/images/agent.png')
GOLD_IMG = pygame.image.load('assets/images/gold.png')
PIT_IMG = pygame.image.load('assets/images/pit.png')

class Game:
    def __init__(self, config):
        self.grid_size = config['grid_size']
        self.agent_position = tuple(config['agent_start_position'])
        self.gold_position = tuple(config['gold_position'])
        self.wumpus_position = None  # Set by user
        self.pits = set()  # Set by user
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Wumpus World")
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_over = False
        self.mode = "play"
        
        # Buttons
        self.ai_button = pygame.Rect(650, 100, BUTTON_WIDTH, BUTTON_HEIGHT)
        self.wumpus_button = pygame.Rect(650, 150, BUTTON_WIDTH, BUTTON_HEIGHT)
        self.pit_button = pygame.Rect(650, 200, BUTTON_WIDTH, BUTTON_HEIGHT)

    def run(self):
        while self.running:
            self.handle_events()
            self.draw()
            self.clock.tick(FPS)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and not self.game_over:
                if event.key == pygame.K_UP:
                    self.move_agent(0, -1)
                elif event.key == pygame.K_DOWN:
                    self.move_agent(0, 1)
                elif event.key == pygame.K_LEFT:
                    self.move_agent(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    self.move_agent(1, 0)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if self.ai_button.collidepoint(mouse_pos):
                    self.run_ai()
                elif self.wumpus_button.collidepoint(mouse_pos):
                    self.mode = "wumpus"
                elif self.pit_button.collidepoint(mouse_pos):
                    self.mode = "pit"
                elif self.mode == "wumpus":
                    self.wumpus_position = self.get_grid_position(mouse_pos)
                    self.mode = "play"
                elif self.mode == "pit":
                    pit_pos = self.get_grid_position(mouse_pos)
                    if pit_pos != self.agent_position and pit_pos != self.gold_position:
                        self.pits.add(pit_pos)
                    self.mode = "play"

    def get_grid_position(self, mouse_pos):
        x, y = mouse_pos
        grid_x = x // GRID_CELL_SIZE
        grid_y = y // GRID_CELL_SIZE
        return grid_x, grid_y

    def run_ai(self):
        path = self.find_path_to_gold()
        if path:
            for step in path:
                self.agent_position = step
                self.draw()
                pygame.time.delay(100)
                if self.agent_position == self.gold_position:
                    print("Agent found the gold!")
                    break

    def find_path_to_gold(self):
        # BFS for shortest path avoiding pits and the Wumpus
        queue = deque([(self.agent_position, [])])
        visited = set()
        visited.add(self.agent_position)

        while queue:
            current_pos, path = queue.popleft()
            if current_pos == self.gold_position:
                return path

            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                new_x = current_pos[0] + dx
                new_y = current_pos[1] + dy
                new_pos = (new_x, new_y)

                if (0 <= new_x < self.grid_size and 0 <= new_y < self.grid_size and
                        new_pos not in self.pits and new_pos != self.wumpus_position and
                        new_pos not in visited):
                    visited.add(new_pos)
                    queue.append((new_pos, path + [new_pos]))
        return None

    def move_agent(self, dx, dy):
        new_x = self.agent_position[0] + dx
        new_y = self.agent_position[1] + dy

        if 0 <= new_x < self.grid_size and 0 <= new_y < self.grid_size:
            self.agent_position = (new_x, new_y)
            self.check_game_state()

    def check_game_state(self):
        if self.agent_position in self.pits:
            self.game_over = True
            print("You fell into a pit! Game Over.")
        elif self.agent_position == self.wumpus_position:
            self.game_over = True
            print("You encountered the Wumpus! Game Over.")
        elif self.agent_position == self.gold_position:
            self.game_over = True
            print("You collected the gold! You win!")

    def draw(self):
        self.screen.fill((255, 255, 255))
        self.draw_grid()
        self.screen.blit(AGENT_IMG, (self.agent_position[0] * GRID_CELL_SIZE, self.agent_position[1] * GRID_CELL_SIZE))
        if self.wumpus_position:
            self.screen.blit(WUMPUS_IMG, (self.wumpus_position[0] * GRID_CELL_SIZE, self.wumpus_position[1] * GRID_CELL_SIZE))
        self.screen.blit(GOLD_IMG, (self.gold_position[0] * GRID_CELL_SIZE, self.gold_position[1] * GRID_CELL_SIZE))
        for pit in self.pits:
            self.screen.blit(PIT_IMG, (pit[0] * GRID_CELL_SIZE, pit[1] * GRID_CELL_SIZE))

        # Draw buttons
        pygame.draw.rect(self.screen, (0, 255, 0), self.ai_button)
        pygame.draw.rect(self.screen, (255, 0, 0), self.wumpus_button)
        pygame.draw.rect(self.screen, (0, 0, 255), self.pit_button)
        
        font = pygame.font.Font(None, 36)
        self.screen.blit(font.render('AI', True, (255, 255, 255)), (self.ai_button.x + 10, self.ai_button.y + 5))
        self.screen.blit(font.render('Wumpus', True, (255, 255, 255)), (self.wumpus_button.x + 10, self.wumpus_button.y + 5))
        self.screen.blit(font.render('Pit', True, (255, 255, 255)), (self.pit_button.x + 10, self.pit_button.y + 5))

        pygame.display.flip()

    def draw_grid(self):
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                pygame.draw.rect(self.screen, (200, 200, 200), (x * GRID_CELL_SIZE, y * GRID_CELL_SIZE, GRID_CELL_SIZE, GRID_CELL_SIZE), 1)

def main():
    config = load_config('assets/config/game_config.json')
    game = Game(config)
    game.run()

if __name__ == "__main__":
    main()
