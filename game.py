import imgui
import numpy as np
from utils.graphics import Object, Camera, Shader
from assets.shaders.shaders import object_shader
from assets.objects.objects import playerProps, backgroundProps, spaceProps, jungleProps, riverProps

class Game:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.screen = 0
        self.camera = Camera(height, width)
        self.shaders = [Shader(object_shader['vertex_shader'], object_shader['fragment_shader'])]
        self.objects = []
        self.maps = [self.create_jungle_map(), self.create_river_map(), self.create_space_map()]
        self.current_map = 0

    def create_space_map(self):
        space = Object(self.shaders[0], spaceProps)
        player = Object(self.shaders[0], playerProps)
        return [space, player]

    def create_jungle_map(self):
        jungle = Object(self.shaders[0], jungleProps)
        player = Object(self.shaders[0], playerProps)
        return [jungle, player]

    def create_river_map(self):
        river = Object(self.shaders[0], riverProps)
        player = Object(self.shaders[0], playerProps)
        return [river, player]

    def InitScreen(self):
        self.objects = self.maps[self.current_map]
        
        # if self.screen == 0:
        #     self.objects = self.maps[self.current_map]
        # if self.screen == 1:
        #     pass
        # if self.screen == 2:
        #     pass

    def ProcessFrame(self, inputs, time):
        if self.screen == -1:
            self.screen = 0
            self.InitScreen()
        if self.screen == 0:
            self.DrawText()
            self.UpdateScene(inputs, time)
            self.DrawScene()
            self.show_switch_map_button()
        if self.screen == 1:
            self.DrawText()
            self.UpdateScene(inputs, time)
            self.DrawScene()

    def DrawText(self):
        if self.screen == 0:
           pass
        if self.screen == 1:
           pass
        if self.screen == 2:
           pass

    def UpdateScene(self, inputs, time):
        if self.screen == 0:
            pass
        if self.screen == 1:
          pass
            
    def DrawScene(self):
        if self.screen == 1:
            for shader in self.shaders:
                self.camera.Update(shader)
 
            for obj in self.objects:
                obj.Draw()
            
    def switch_map(self):
        self.current_map += 1
        if self.current_map >= len(self.maps):
            self.current_map = 0  # Loop back to the first map or handle game completion
        self.InitScreen()
        
    def show_switch_map_button(self):
        imgui.begin("Switch Map", True)
        if imgui.button("Next Map"):
            self.switch_map()
        imgui.end()