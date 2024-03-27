import pygame
import sys
import serial
import time
import random

# set up hardware
serial_port = '/dev/cu.usbmodem143301'  # Change this to match the port where your Arduino is connected
encoder = {0: b"\x30",  # an attempt to increase serial communication speeds
           1: b"\x31",
           2: b"\x32"
           }

# game parameters
rounds = 10
num_targets = 3
baud_rate = 250000  # Adjust baud rate as needed
scanTime = 20  # seconds
threshold = 10

# Initialize Pygame
pygame.init()
clock = pygame.time.Clock()
screen_width = 2000
screen_height = 1000
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Footbonaht")
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
font = pygame.font.Font(None, 72)

# Pygame start button
button_surface = pygame.Surface((300, 100)) # Create a surface for the button
text = font.render("START", True, (0, 0, 0)) # Render text on the button
text_rect = text.get_rect(center=(button_surface.get_width() / 2, button_surface.get_height() / 2))
button_rect = pygame.Rect(125, 125, 150, 50)

def flash_single(ser, panel):
    cmd = encoder[panel]
    ser.write(cmd)
    ser.readline()
    time.sleep(0.1)  # Wait for a while
    ser.write(b'o\n')
    time.sleep(0.1)  # Wait for a while
    ser.readline()

def update_scoreboard(round, score, t):
    screen.fill(WHITE)

    round_text = font.render(f"Round: {round}", True, BLACK)
    round_rect = round_text.get_rect(center=(screen_width // 2, screen_height * 0.25))
    screen.blit(round_text, round_rect)

    score_text = font.render(f"Score: {score}", True, BLACK)
    score_rect = score_text.get_rect(center=(screen_width // 2, screen_height * 0.5))
    screen.blit(score_text, score_rect)

    react_text = font.render(f"Reaction Time: {t:.2f} seconds", True, BLACK)
    react_rect = score_text.get_rect(center=(screen_width // 2, screen_height * 0.75))
    screen.blit(react_text, react_rect)

    pygame.display.flip()

def final_scoreboard(score, rounds, react_times):

    screen.fill(WHITE)
    go_text = font.render(f"Game over!", True, BLACK)
    go_rect = go_text.get_rect(center=(screen_width // 2, screen_height * 0.25))
    screen.blit(go_text, go_rect)
    pygame.display.flip()
    time.sleep(2)

    screen.fill(WHITE)
    acc = (score / rounds) * 100
    acc_text = font.render(f"Final Score: {score} / {rounds} ({acc:.2f}%)", True, BLACK)
    acc_rect = acc_text.get_rect(center=(screen_width // 2, screen_height * 0.25))
    screen.blit(acc_text, acc_rect)
    avg_react_time = sum(react_times) / len(react_times)
    summ_text = font.render(f"Average Reaction Time: {avg_react_time:.2f} s", True, BLACK)
    summ_rect = summ_text.get_rect(center=(screen_width // 2, screen_height * 0.50))
    screen.blit(summ_text, summ_rect)
    pygame.display.flip()

def main():
    reset = True
    running = True
    ser = serial.Serial(serial_port, baud_rate, timeout=2, writeTimeout=2)
    ser.readline()

    # Main game loop
    while running:
        if reset:
            score = 0
            t = 0
            round = 1
            react_times = []
            running = True
            game_on = False
            reset = False

        # Clear the screen
        screen.fill(WHITE)

        # Get events from the event queue
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Check for the mouse button down event
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Call the on_mouse_button_down() function
                if button_rect.collidepoint(event.pos):
                    game_on = True
                    reset = True

        # button stuff
        button_surface.blit(text, text_rect) # Show the button text
        screen.blit(button_surface, (button_rect.x, button_rect.y)) # Draw the button on the screen

        # Check if the mouse is over the button. This will create the button hover effect
        if button_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(button_surface, (127, 255, 212), (1, 1, 298, 98))
        else:
            pygame.draw.rect(button_surface, (0, 0, 0), (0, 0, 298, 98))
            pygame.draw.rect(button_surface, (255, 255, 255), (1, 1, 298, 98))
            pygame.draw.rect(button_surface, (0, 0, 0), (1, 1, 298, 1), 2)
            pygame.draw.rect(button_surface, (0, 98, 0), (1, 98, 298, 10), 2)

        while game_on:
            # Draw the scoreboard
            update_scoreboard(round, score, t)
            # Generate a random number between 0 and 2
            selected_target = random.randint(0, num_targets - 1)
            print("Strike panel {}!".format(selected_target))

            # Flash LED on selected target
            flash_single(ser, selected_target)

            # Begin scanning panel for ball strike
            scanning = True
            start_time = time.time()
            struck_panel = -1
            while scanning:
                ser.write(b'r\n')  # Send request command
                response = ser.readline().decode().strip()
                if response:
                    t = time.time() - start_time
                    react_times.append(t)
                    values = [int(x) for x in response.split(',')]
                    if max(values) > threshold:
                        scanning = False
                        struck_panel = values.index(max(values))
                    if time.time() - start_time > scanTime:
                        scanning = False
                        struck_panel = -1

            if struck_panel == -1:  # no strike registered
                print("\nNo strike detected!")
            else:  # strike detected
                print("\nPanel {} was struck!".format(struck_panel))
                if struck_panel == selected_target:
                    print("Target hit!")
                    score += 1
                else:
                    print("Target Missed!")

            if round >= rounds:
                game_on = False
                final_scoreboard(score, rounds, react_times)
                time.sleep(10)

            # index round number
            round += 1

        # update screen while game is running
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()