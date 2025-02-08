from tkinter.font import Font 
import pygame
from pygame.locals import *
import time

#initialize pygame elements
pygame.init()

# Initialize pygame and create game window  
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pirate's Quantum Treasure")
BIG_FONT = pygame.font.SysFont('Arial', 48)

# Load assets (player sprite, chests, map, font)  
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GOLD = (255, 215, 0)
BROWN = (150, 75, 0)

start_time = 18000
clock = pygame.time.Clock()

#FONT = pygame.font.Font("Copenhagen-z3Z0.ttf")
FONT = pygame.font.SysFont('Arial', 24)
#timer_text = FONT.render("240", True, "black")
timer_text = FONT.render(str(start_time // 1000), True, "black")
timer_text_rect = timer_text.get_rect(center=(SCREEN_WIDTH-40, SCREEN_HEIGHT-575))

# Draw Text for start screen text
def draw_text(text, x, y, font=FONT, color=BROWN):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))


def show_start_screen():
    game_background = pygame.image.load('game_background.png')  
    game_background = pygame.transform.scale(game_background, (SCREEN_WIDTH, SCREEN_HEIGHT))  

    clock = pygame.time.Clock()  
    show_text = True  
    last_toggle_time = pygame.time.get_ticks()  

    waiting = True
    while waiting:
        screen.blit(game_background, (0, 0))  
        draw_text("🏴‍☠️ Pirate's Quantum Treasure 🏴‍☠️", 150, 200, BIG_FONT)  

        # Toggle text every 500ms
        current_time = pygame.time.get_ticks()
        if current_time - last_toggle_time > 500:  
            show_text = not show_text  
            last_toggle_time = current_time  

        if show_text:
            draw_text("Press ENTER to Begin!", 250, 300)  

        pygame.display.flip()  

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                waiting = False  

        clock.tick(30)
                
#pictures to be used
#background = pygame.image.load("background.png")  # Replace with your actual image file
#background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

#correct_img = pygame.image.load("correct.png")  # Image shown when the answer is correct
#incorrect_img = pygame.image.load("incorrect.png")  # Image for incorrect answers

# Set up game variables (player position, timer, quiz status, chests)
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Pirate4.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect(center=(300, 250))

    def move(self, dx, dy, walls):
        if dx or dy:
            new_rect = self.rect.move(dx, dy)
            if not any(new_rect.colliderect(wall) for wall in walls):
                self.rect = new_rect  # Move only if no collision


#player = pygame.Rect((300,250,50,50))
player = Player()
player_group = pygame.sprite.GroupSingle(player)

CHEST_SIZE = 50
big_chests = [
    pygame.Rect(100, 100, CHEST_SIZE, CHEST_SIZE),
    pygame.Rect(500, 200, CHEST_SIZE, CHEST_SIZE),
    pygame.Rect(300, 400, CHEST_SIZE, CHEST_SIZE),
    pygame.Rect(700, 500, CHEST_SIZE, CHEST_SIZE)
]

SMALL_CHEST_SIZE = 30
small_chests = [
    pygame.Rect(120, 150, SMALL_CHEST_SIZE, SMALL_CHEST_SIZE ),
    pygame.Rect(600, 180, SMALL_CHEST_SIZE, SMALL_CHEST_SIZE),
    pygame.Rect(300, 400, SMALL_CHEST_SIZE, SMALL_CHEST_SIZE),
    pygame.Rect(700, 530, SMALL_CHEST_SIZE, SMALL_CHEST_SIZE)
]


class Chest(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("treasure chest.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (100,100))
        self.rect = self.image.get_rect(topleft=(x,y)) #position chest as x,y

chests_large = pygame.sprite.Group(
    Chest(100,100),
    Chest(200,300),
    Chest(500,100),
    Chest(300,600)
)

walls = [
    pygame.Rect(0, -50, SCREEN_WIDTH, 50),
    pygame.Rect(-50, 0, 50, SCREEN_HEIGHT),
    pygame.Rect(SCREEN_WIDTH, 0, 50, SCREEN_HEIGHT),
    pygame.Rect(0, SCREEN_HEIGHT, SCREEN_WIDTH, 50),
]

quiz_questions = [
    {"question": "What is quantum entanglement?", 
     "options": ["A technique used to speed up computation", "A property where qubits are linked, so the state of one affects the other", "The process of converting classical information into quantum information"],
     "answer": "A property where qubits are linked, so the state of one affects the other"},
    
    {"question": "What does quantum decoherence refer to in quantum computing?", 
     "options": ["A method of entangling qubits", "A technique to stabilize qubits", "The process of qubits losing their quantum properties due to external interactions"],
     "answer": "The process of qubits losing their quantum properties due to external interactions"},

    {"question": "How does a quantum computer differ from a classical computer in terms of processing power?", 
     "options": ["Quantum computers use parallel processing to perform computations on multiple data points at once", "Quantum computers are faster because they use classical bits", "Quantum computers cannot perform calculations at all"],
     "answer": "Quantum computers use parallel processing to perform computations on multiple data points at once"},

    {"question": "What is the primary purpose of a quantum gate in quantum computing?", 
     "options": ["To store classical data", "To manipulate qubits and perform computations", "To store classical data"],
     "answer": "To manipulate qubits and perform computations"}
]

small_chest_facts = [
    "Quantum entanglement be a curse most foul, where qubits are tied together in a bond so strong that when ye change one qubit, the other changes too, even if they be far apart. It’s like two pirate ships far from each other, yet when one fires a cannon, the other ship instantly feels the blast. This spooky magic allows for faster communication and calculation, as if the qubits be whispering secret messages.",
    "A quantum decoherence storm be a terrible thing on the high seas. When a quantum computer's qubits are disturbed by their surroundings (like the wind blowing too hard or a storm brewing), they lose their quantum magic and behave like mere classical bits. This loss of coherence can ruin a quantum computation, just as a storm might sink a pirate ship. Quantum pirates must keep their qubits safe from such storms!",
    "The secret of quantum computing lies in its ability to navigate using parallel processing—like having multiple sails that catch the wind from all directions at once! This is thanks to the superposition of qubits, which can explore many possibilities simultaneously. A regular ship can only sail one course at a time, while the quantum ship can chart multiple courses, sailing faster through the seas of computation.",
    "A quantum gate be a tool that pirates use to manipulate qubits. Just as a ship’s wheel changes the direction of the vessel, a quantum gate changes the state of a qubit. These gates perform operations that allow quantum computers to process all that valuable treasure (or data) in ways that classical ships can’t match."
]
quiz_stat = 8

#func to display quiz
def display_quiz(screen, question_data, start_time):
    screen.fill(WHITE)
    FONT = pygame.font.SysFont('Arial', 20)
    
    question_text = FONT.render(question_data["question"], True, "black")
    screen.blit(question_text, (50, 100))

    button_rects = []
    y_offset = 200
    for option in question_data["options"]:
        button_rect = pygame.Rect(50, y_offset, 700, 50)
        pygame.draw.rect(screen, (0, 128, 255), button_rect)
        text = FONT.render(option, True, "white")
        screen.blit(text, (60, y_offset + 10))
        button_rects.append((button_rect, option))
        y_offset += 70

    pygame.display.update()

    # Wait until player selects an answer
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button, option in button_rects:
                    if button.collidepoint(event.pos):
                        if option == question_data["answer"]:
                            print("Correct!")
                        else:
                            print("Incorrect! (-20s)")
                            start_time -= 2000
                        return start_time  # Reset the start time and return to main game loop
        pygame.display.update()

def display_end_screen():
    screen.fill(WHITE)  
    background = pygame.image.load("endscreen_failed.png")  
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(background, (0, 0))
    pygame.display.update()
    pygame.time.delay(3000)  
    pygame.quit()
    exit()


def check_collision(rect, objects):
    """Checks if the given rectangle collides with any object in the list."""
    for obj in objects:
        if rect.colliderect(obj):
            return True
    return False


# WHILE game is running:
run = True
quiz_active = False
current_question = None
button_rects = []
fact_active = False

# IF user collects all code letters:
def display_win_screen():
    screen.fill(WHITE)
    draw_text("🏴‍☠️ Arrr Matey! You found all the treasure! 🏴‍☠️", 200, 250)
    pygame.display.flip()
    pygame.time.delay(3000)
    pygame.quit()
    exit()

show_start_screen()

game_background = pygame.image.load('game_background.png')
game_background = pygame.transform.scale(game_background, (SCREEN_WIDTH, SCREEN_HEIGHT))
while run:
    screen.fill(WHITE)
    screen.blit(game_background, (0, 0))
    #pygame.display.update()


    timer_text = FONT.render(str((int) (start_time/100)), True, "black")
    screen.blit(timer_text, timer_text_rect)
#     Clear screen and draw background  
#     Draw player at current position
    screen.blit(player.image, player.rect)
    #pygame.draw.rect(screen, (255, 0, 0), player)


#     Draw chests on the map  
    chests_large.draw(screen)

#       Draw small chests
    for chest in small_chests:
        pygame.draw.rect(screen, BROWN, chest)

# Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


    # Player movement
    # Check for user input (WASD for movement)  

    key = pygame.key.get_pressed()
    move_x, move_y = 0, 0
    if key[pygame.K_a]:  # Move left
        move_x = -1
    elif key[pygame.K_d]:  # Move right
        move_x = 1
    elif key[pygame.K_w]:  # Move up
        move_y = -1
    elif key[pygame.K_s]:  # Move down
        move_y = 1

    # Try to move the player, check for collisions
    new_player_rect = player.rect.move(move_x, move_y)
    if not check_collision(new_player_rect, walls):
        player.rect = new_player_rect  # Only move if no collision

    # Check player collision to borders
    player.move(move_x, move_y, walls)

    # Check if the new position collides with any walls
    # If no collision, update the player's position
    if not check_collision(player.rect, walls):
        player.move(move_x, move_y, walls)

# Ensure player stays within map boundaries
    # If player collides with a chest:
    # **Check for big chest collision (Quiz)**
    #collided_chest = pygame.sprite.spritecollideany(player_group.sprite, chests_large)
# Check if the player collides with a chest (trigger quiz only once)
# Track the chests that have already been used for quizzes
    used_chests = set()

# Check if the player collides with a chest
    collided_chest = pygame.sprite.spritecollideany(player, chests_large)

# If the player collides with a chest and it hasn't been used yet
    if collided_chest and collided_chest not in used_chests:
        used_chests.add(collided_chest)  # Mark the chest as used
        quiz_active = True
        current_question = quiz_questions[len(used_chests) % len(quiz_questions)]  # Select a new question based on number of used chests
        start_time = display_quiz(screen, current_question, start_time)
        collided_chest.kill()  # Optionally remove chest after quiz


    # Check collisions with small chests (Show Fact)
    if not fact_active:
        for i, chest in enumerate(small_chests[:]):
            if player.rect.colliderect(chest):
                fact_text = small_chest_facts[i]
                fact_active = True
                game_background = pygame.image.load('Fact1.png')
                game_background = pygame.transform.scale(game_background, (SCREEN_WIDTH, SCREEN_HEIGHT))
                small_chests.pop(i)  # Remove small chest after reading fact
                break

    # Game loop to handle 'Enter' key to return to the game
    if fact_active:
        # Clear the screen with the fact image
        screen.blit(game_background, (0, 0))  # Display the fact image as the background

        # Check if the player presses Enter to return to the game
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Enter key pressed
                    fact_active = False  # Hide the fact image and return to the game

    # After checking for the fact display, continue with normal game drawing if not in fact screen
    if not fact_active:
        pass

    if len(big_chests) == 0 and not quiz_active:
        print("Arrr Matey! You found all the treasure!")
        run = False

# win condition

#     Show success message "Arrr Matey! You found the treasure!"  
#     End game 

    start_time -= 1

    if start_time <= 0:
        display_win_screen()
        

    #screen.blit(bg_image, (0, 0))
    pygame.display.update()
    clock.tick(100)


pygame.quit()