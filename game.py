# Import external libraries.
import random
import pygame
import pygame_gui

import time

from collections import deque

# Import Pygame GUI elements directly for ease of access.
from pygame_gui import UIManager, PackageResource
from pygame_gui.elements import UIWindow
from pygame_gui.elements import UITextEntryLine
from pygame_gui.elements import UITextBox
from pygame_gui.elements import UIImage
from pygame_gui.windows import UIMessageWindow

# Import the rest of our code.
import utilities
import config
import commands
import player
import scenes

# Create a player object using the player's save data.
player_data = player.Player()

# ...Load it again, just to be safe.
player_data = player.Player()

# We'll use this empty string later to store our response history.
response_history = ""

title_screen_image = pygame.image.load('media/images/titlescreen.png')
mines_image = pygame.image.load('media/images/mines.png')
busstop_image = pygame.image.load('media/images/busstop.png')

# Check to see if the player is in a scripted sequence.
if player_data.scene is not None: # If they are, give them a response based upon their current scene.
    if player_data.scene == config.scene_id_newgame:
        response = scenes.Introduction(None)
        response_history += response
else: # If they aren't, give them a generic response.
    if player_data.location != config.location_id_canada:
        response = "Welcome back, {}. You are still {:,} slimes in debt.<br><br>What would you like to do now?".format(player_data.name, player_data.debt)
        response_history += response
    else:
        response = "Welcome back, {}. You are still safe and sound in Canada.<br><br>What would you like to do now?".format(player_data.name)
        response_history += response

class Window(UIWindow):
    def __init__(self, rect, ui_manager):
        super().__init__(rect, ui_manager)

        #self.text_block = UITextBox(response, pygame.Rect((25, 25), (845, 380)), self.ui_manager, container = self)

        #self.text_entry = UITextEntryLine(pygame.Rect((50, 550), (700, 50)), self.ui_manager, container = self)     

class Options:
    def __init__(self):
        self.resolution = (800, 600)

class Game:
    def __init__(self):
        # Start up Pygame.
        pygame.init()

        # Title the window our game runs in.
        pygame.display.set_caption(config.game_name)
        
        self.options = Options()

        # Define the dimensions of our game's window.
        self.window_surface = pygame.display.set_mode(self.options.resolution)
        self.window_surface.blit(pygame.image.load("media/images/background.png"), (0, 0))

        self.start_up = True
        self.enter_mines = False
        self.enter_busstop = False

        self.background_surface = None

        self.ui_manager = UIManager(self.options.resolution, PackageResource(package='media.themes', resource='theme.json'))

        self.text_block = None
        self.text_entry = None

        self.message_window = None

        self.recreate_ui()

        self.clock = pygame.time.Clock()
        self.time_delta_stack = deque([])
        self.running = True

    def recreate_ui(self):
        self.ui_manager.set_window_resolution(self.options.resolution)
        self.ui_manager.clear_and_reset()

        self.background_surface = pygame.Surface(self.options.resolution)

        if self.start_up == True:
            self.image = UIImage(pygame.Rect((0, 0), self.options.resolution), title_screen_image, self.ui_manager)
        elif self.enter_mines == True:
            self.image = UIImage(pygame.Rect((0, 0), self.options.resolution), mines_image, self.ui_manager)
        elif self.enter_busstop == True:
            self.image = UIImage(pygame.Rect((0, 0), self.options.resolution), busstop_image, self.ui_manager)
        else: 
            self.background_surface.fill(self.ui_manager.get_theme().get_colour('dark_bg'))
            self.background_surface.blit(pygame.image.load("media/images/background.png"), (0, 0))
            
            global response_history
            response = response_history
            response_history = response
            self.text_entry = UITextEntryLine(pygame.Rect((50, 550), (700, 50)), self.ui_manager, object_id = "#text_entry")
            self.text_block = UITextBox(response, pygame.Rect((50, 25), (700, 500)), self.ui_manager, object_id = "#text_block")

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            self.ui_manager.process_events(event)            

            if event.type==pygame.KEYDOWN:
                if event.key== pygame.K_UP:              
                    if self.start_up == True:
                        self.start_up = False
                        self.recreate_ui()
                    if self.enter_mines == True:
                        self.enter_mines = False
                        self.recreate_ui()
                    if self.enter_busstop == True:
                        self.enter_busstop = False
                        self.recreate_ui()
            if event.type == pygame.USEREVENT:
                if (event.user_type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == '#text_entry'):
                    if event.text != "":
                        # Turn the user's input into a string.
                        message = event.text

                        # Begin the response message. Start with repeating the user's input.
                        response = "<b><i>> {message}</i></b>".format(message = message)

                        # Create a player object using the player's save data.
                        player_data = player.Player()

                        # Check to see if the player is in a scripted sequence.
                        if player_data.scene is not None: # If they are...
                            if player_data.scene == config.scene_id_newgame: # If the player has started the game for the first time.
                                command_response = scenes.Introduction(message)
                                response += ("<br>" * 4) + command_response
                        else: # If they aren't...
                            command_response = utilities.parse_message(message)
                            response += ("<br>" * 4) + command_response

                        # End the response with some decoration. ^_^
                        response += ("<br>" * 4) + ("-" * 20) + ("<br>" * 4)

                        # Add this response to our response history, and then send the entire history to be rendered.
                        global response_history
                        response += response_history
                        response_history = response
                        # Render the response.
                        self.text_entry.set_text("")
                        self.text_block.kill()
                        self.text_block = UITextBox(response, pygame.Rect((50, 25), (700, 500)), self.ui_manager, object_id = "#text_block")
                        
                        if command_response == "You enter the Mines.":
                            self.enter_mines = True
                            self.recreate_ui()
                        if command_response == "You enter a Bus Stop.":
                            self.enter_busstop = True
                            self.recreate_ui()
    def run(self):
        while self.running:
            time_delta = self.clock.tick() / 1000
            
            # Check for inputs from the player.
            self.process_events()

            # Respond to inputs.
            self.ui_manager.update(time_delta)

            # Draw the graphics.
            self.window_surface.blit(self.background_surface, (0, 0))
            self.ui_manager.draw_ui(self.window_surface)

            pygame.display.update()

# Start the game.
if __name__ == '__main__':
    app = Game()
    app.run()