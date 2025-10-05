import pygame
import random
import sys

# 1. Initialization and Setup
pygame.init()

# Define Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Initial Window Dimensions
X_INITIAL = 500
Y_INITIAL = 500

def format_number(number):
    if number.is_integer():
        return(int(number))
    else:
        return(number)

# --- Game State ---
# Controls what is currently displayed on screen
# 0: Show Begin Button and the number array
# 1: Show "Your answer is:" and the result
game_state = 0


number_array = [10, "+", 5, "=", 15]

display_numbers_text = " ".join(map(str, number_array))
# ----------------------------------------------------

# --- Input/Calculation Setup ---
try:
    num = 3#float(input("Enter a number: "))
except ValueError:
    print("Invalid input. Please enter a number.")
    sys.exit()

expressions = [
        [28, "assets/item0.png"],
        [1, "assets/item1.png"],
        [2, "assets/item2.png"],
        [-1, "assets/item3.png"],
        [4, "assets/item4.png"],
        [5, "assets/item5.png"]]
exp = (random.choice(expressions))
constant = num/exp[0]
# -------------------------------

# Create the display surface object, enabling resizing
screen = pygame.display.set_mode((X_INITIAL, Y_INITIAL), pygame.RESIZABLE)
pygame.display.set_caption('Calculator')

# Load Font and Render Text Surfaces
font_title = pygame.font.Font('freesansbold.ttf', 40)
font_side = pygame.font.Font('assets/cambria-math.ttf', 24)
font_button = pygame.font.Font('freesansbold.ttf', 30)
font_array = pygame.font.Font('freesansbold.ttf', 20) # Font for the number array

# --- Text Surfaces for State 0 (Begin Screen) ---
array_text_surface = font_array.render(display_numbers_text, True, BLACK)
array_text_rect = array_text_surface.get_rect()

# --- Text Surfaces for State 1 (Result Screen) ---
title_text_surface = font_title.render('Your answer is:', True, BLACK)
coefficient = font_side.render(str(format_number(constant)), True, BLACK)

# Load Image
try:
    image_path = exp[1]
    image_surface = pygame.image.load(image_path).convert_alpha()
    if image_surface.get_width() > 300 or image_surface.get_height() > 300:
        image_surface = pygame.transform.scale(image_surface, (200, 200))

except pygame.error as e:
    print(f"Error loading image: {e}")
    image_surface = pygame.Surface((200, 200))
    image_surface.fill(GREEN)

# --- Button Class ---
class Button():
    def __init__(self, text, x, y, width, height, color, text_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text_color = text_color
        self.text = font_button.render(text, True, self.text_color)
        self.text_rect = self.text.get_rect(center=self.rect.center)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, border_radius=10)
        surface.blit(self.text, self.text_rect)

    def check_click(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

# --- Button Setup ---
# Center the button in the screen
button_width = 150
button_height = 60
button_x = (X_INITIAL - button_width) // 2
button_y = (Y_INITIAL - button_height) // 2
begin_button = Button("BEGIN", button_x, button_y, button_width, button_height, BLUE, WHITE)

# Position the array text above the button
array_text_rect.centerx = X_INITIAL // 2
array_text_rect.bottom = begin_button.rect.top - 30 # 30 pixels above the button
# --------------------


# 2. Function to Calculate Centering (for Result Screen)
def center_elements(screen_width, screen_height, title_surf, side_surf, image_surf):

    #Calculates positions for the result display:
    #1. Title centered at the top.
    #2. Side text and Image centered side-by-side below the title.

    title_rect = title_surf.get_rect()
    side_rect = side_surf.get_rect()
    image_rect = image_surf.get_rect()

    vertical_spacing = 40
    horizontal_spacing = 0

    # A. Calculate position for the Title (Top Center)
    title_rect.centerx = screen_width // 2
    title_rect.top = 50

    # B. Calculate position for the side-by-side block
    side_block_width = side_rect.width + horizontal_spacing + image_rect.width
    block_start_x = (screen_width - side_block_width) // 2
    block_top_y = title_rect.bottom + vertical_spacing

    # Position the Side Text
    side_rect.left = block_start_x
    side_rect.centery = block_top_y + (image_rect.height // 2)

    # Position the Image (right next to the side text)
    image_rect.left = side_rect.right + horizontal_spacing
    image_rect.top = block_top_y

    return title_rect, side_rect, image_rect

# Initial calculation of positions for Result Screen
screen_width, screen_height = screen.get_size()
title_rect, side_rect, image_rect = center_elements(
    screen_width, screen_height, title_text_surface, coefficient, image_surface
)

# 3. Game Loop
status = True
while status:

    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            status = False

        # Handle Window Resizing
        elif event.type == pygame.VIDEORESIZE:
            screen_width, screen_height = event.size
            screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)

            # Recalculate positions for both screens
            title_rect, side_rect, image_rect = center_elements(
                screen_width, screen_height, title_text_surface, coefficient, image_surface
            )
            # Re-center the button and array text for the new screen size
            begin_button.rect.center = (screen_width // 2, screen_height // 2)
            begin_button.text_rect.center = begin_button.rect.center
            array_text_rect.centerx = screen_width // 2
            array_text_rect.bottom = begin_button.rect.top - 30

        # Handle Mouse Click
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == 0 and event.button == 1: # Left click
                if begin_button.check_click(event.pos):
                    game_state = 1 # Change state to show the answer!

    # Drawing
    screen.fill(WHITE) # Clear screen

    if game_state == 0:
        # State 0: Draw the Number Array Text and the BEGIN button
        screen.blit(array_text_surface, array_text_rect)
        begin_button.draw(screen)

    elif game_state == 1:
        # State 1: Draw the result
        screen.blit(title_text_surface, title_rect)
        screen.blit(coefficient, side_rect)
        screen.blit(image_surface, image_rect)

    # Update the full screen
    pygame.display.flip()

# 4. Quit Pygame
pygame.quit()

