from OpenGL.GL import *
from utils.window_manager import Window
from game import Game
import imgui
from imgui.integrations.glfw import GlfwRenderer

class App:
    def __init__(self, width, height):
        self.window = Window(height, width)
        self.game = Game(height, width)
        self.show_main_menu = True
        imgui.create_context()
        self.impl = GlfwRenderer(self.window.window)

    def RenderLoop(self):

        while self.window.IsOpen():
            inputs, time = self.window.StartFrame(0.0, 0.0, 0.0, 1.0)

            self.impl.process_inputs() 
            imgui.new_frame()

            # If not showing main menu, check game status
            if not self.show_main_menu:
                if self.game.is_game_over:
                    self.show_game_over_screen()
                elif self.game.is_game_won:
                    self.show_you_won_screen()
                else:
                    self.game.ProcessFrame(inputs, time)
                    self.game.show_switch_map_button()
            else:
                self.show_main_menu_screen(inputs)

            imgui.render()
            self.impl.render(imgui.get_draw_data())
            self.window.EndFrame()
        
        self.window.Close()

    def show_you_won_screen(self):
        # Center the window
        center_x = (self.window.windowWidth - 550) / 2
        center_y = (self.window.windowHeight - 400) / 2
        imgui.set_next_window_position(center_x, center_y)
        imgui.set_next_window_size(600, 400)

        imgui.begin("Victory!", True)
        # Make the text larger
        imgui.set_window_font_scale(10.0)
        imgui.text_unformatted("YOU WON!")
        imgui.set_window_font_scale(5.0)  # slightly smaller for the next lines
        imgui.text_unformatted(f"Time taken: {int(self.game.total_time)}s")
        imgui.end()

    def show_game_over_screen(self):
        # Center the window
        center_x = (self.window.windowWidth - 850) / 2
        center_y = (self.window.windowHeight - 600) / 2
        imgui.set_next_window_position(center_x, center_y)
        imgui.set_next_window_size(850, 600)

        imgui.begin("Game Over", True)
        # Make the text larger
        imgui.set_window_font_scale(10.0)
        imgui.text_unformatted("GAME OVER")
        imgui.set_window_font_scale(5.0)
        imgui.text_unformatted("You lost all your lives!")
        if imgui.button("Return to Main Menu", 750, 100):
            self.show_main_menu = True
        imgui.end()
    
    def show_main_menu_screen(self, inputs):
        imgui.begin("Main Menu", True, imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_MOVE)
    
        # Get window size and calculate the center position
        window_width = imgui.get_window_width()
        window_height = imgui.get_window_height()
        button_width = 200
        button_height = 50
        center_x = (window_width - button_width) / 2
        center_y = (window_height - button_height) / 2

        # Set window position to center of the screen
        # imgui.set_window_pos((self.window.windowWidth - window_width) / 2, (self.window.windowHeight - window_height) / 2)
        imgui.set_window_size(400, 300)

        # Center the "NEW GAME" button
        imgui.set_cursor_pos_x(center_x)
        imgui.set_cursor_pos_y(center_y - button_height)
        if imgui.button("NEW GAME", button_width, button_height):
            # print("Game started")
            self.start_new_game()

        # Center the "LOAD GAME" button
        imgui.set_cursor_pos_x(center_x)
        imgui.set_cursor_pos_y(center_y + button_height)
        if imgui.button("LOAD GAME", button_width, button_height):
            self.load_game()

        imgui.end()

    def start_new_game(self):
        self.show_main_menu = False
        self.game = Game(self.window.windowHeight, self.window.windowWidth)
        self.game.screen = 0
        self.game.InitScreen()

    def load_game(self):
        self.show_main_menu = False
        # Load game state from file and initialize the game
        # Example:
        # with open('savegame.txt', 'r') as f:
        #     data = f.read().split(',')
        #     map_number = int(data[0])
        #     lives = int(data[1])
        #     health = int(data[2])
        #     self.game = Game(self.window.windowHeight, self.window.windowWidth)
        #     self.game.current_map = map_number
        #     self.game.lives = lives
        #     self.game.health = health
        self.game.InitScreen()

if __name__ == "__main__":
    app = App(1000, 1000)
    app.RenderLoop()


