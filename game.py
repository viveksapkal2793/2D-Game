import imgui
import numpy as np
import random
from utils.graphics import Object, Camera, Shader
from assets.shaders.shaders import object_shader
from assets.objects.objects import playerProps, backgroundProps, spaceProps, jungleProps, riverProps, CreateStone, CreateKeyIcon

def random_nonoverlapping_position(existing_objs, new_radius, max_attempts=1000):
    """Try up to max_attempts to find a position that doesn't overlap existing stones."""
    for _ in range(max_attempts):
        x = random.uniform(-450, 450)
        y = random.uniform(-300, 300)
        center = np.array([x, y, 0], dtype=np.float32)

        overlap = False
        for obj in existing_objs:
            # Only check objects that have a 'radius' property
            if 'radius' in obj.properties:
                dist = np.linalg.norm(center - obj.properties['position'])
                if dist < (new_radius + obj.properties['radius']) or (x < obj.properties['position'][0] + obj.properties['radius'] and x > obj.properties['position'][0] - obj.properties['radius']):
                    overlap = True
                    break
        if not overlap:
            return center
    return None 

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
        objs =  [space, player]
        stone_objs = []

        # Add random non-overlapping stones
        for _ in range(8):
            r = 40
            pos = random_nonoverlapping_position(objs, r)
            if pos is None:
                # If we can't find a valid spot, just skip or place at a default
                continue

            stone_verts, stone_inds = CreateStone(radius=r, color=[0.7, 0.7, 0.7])
            stone_obj = Object(self.shaders[0], {
                'vertices': np.array(stone_verts, dtype=np.float32),
                'indices': np.array(stone_inds, dtype=np.uint32),
                'position': pos,
                'rotation_z': 0.0,
                'scale': np.array([1, 1, 1], dtype=np.float32),
                'speed': random.uniform(50, 120),
                'radius': r
            })
            stone_objs.append(stone_obj)

        # Pick exactly three random stones to hold keys
        if len(stone_objs) >= 3:
            chosen_stones = random.sample(stone_objs, 3)
            for s in chosen_stones:
                key_verts, key_inds = CreateKeyIcon(
                    radius=10,  # small radius for the key
                    color=[1.0, 1.0, 0.0]
                )
                key_obj = Object(self.shaders[0], {
                    'vertices': np.array(key_verts, dtype=np.float32),
                    'indices': np.array(key_inds, dtype=np.uint32),
                    'position': s.properties['position'].copy() + np.array([0, 0, 1], dtype=np.float32),
                    'rotation_z': 0.0,
                    'scale': np.array([1, 1, 1], dtype=np.float32),
                    'speed': s.properties['speed'],
                    'has_key': True  # custom flag to indicate it's a key
                })
                stone_objs.append(key_obj)

        objs.extend(stone_objs)

        return objs

    def create_jungle_map(self):
        jungle = Object(self.shaders[0], jungleProps)
        player = Object(self.shaders[0], playerProps)
        objs =  [jungle, player]
        stone_objs = []

        # Add random non-overlapping stones
        for _ in range(8):
            r = 40
            pos = random_nonoverlapping_position(objs, r)
            if pos is None:
                # If we can't find a valid spot, just skip or place at a default
                continue

            stone_verts, stone_inds = CreateStone(radius=r, color=[0.7, 0.7, 0.7])
            stone_obj = Object(self.shaders[0], {
                'vertices': np.array(stone_verts, dtype=np.float32),
                'indices': np.array(stone_inds, dtype=np.uint32),
                'position': pos,
                'rotation_z': 0.0,
                'scale': np.array([1, 1, 1], dtype=np.float32),
                'speed': random.uniform(50, 120),
                'radius': r
            })
            stone_objs.append(stone_obj)

        # Pick exactly three random stones to hold keys
        if len(stone_objs) >= 3:
            chosen_stones = random.sample(stone_objs, 3)
            for s in chosen_stones:
                key_verts, key_inds = CreateKeyIcon(
                    radius=10,  # small radius for the key
                    color=[1.0, 1.0, 0.0]
                )
                key_obj = Object(self.shaders[0], {
                    'vertices': np.array(key_verts, dtype=np.float32),
                    'indices': np.array(key_inds, dtype=np.uint32),
                    'position': s.properties['position'].copy() + np.array([0, 0, 1], dtype=np.float32),
                    'rotation_z': 0.0,
                    'scale': np.array([1, 1, 1], dtype=np.float32),
                    'speed': s.properties['speed'],
                    'has_key': True  # custom flag to indicate it's a key
                })
                stone_objs.append(key_obj)

        objs.extend(stone_objs)

        return objs

    def create_river_map(self):
        river = Object(self.shaders[0], riverProps)
        player = Object(self.shaders[0], playerProps)
        objs =  [river, player]
        stone_objs = []

        # Add random non-overlapping stones
        for _ in range(8):
            r = 40
            pos = random_nonoverlapping_position(objs, r)
            if pos is None:
                # If we can't find a valid spot, just skip or place at a default
                continue

            stone_verts, stone_inds = CreateStone(radius=r, color=[0.7, 0.7, 0.7])
            stone_obj = Object(self.shaders[0], {
                'vertices': np.array(stone_verts, dtype=np.float32),
                'indices': np.array(stone_inds, dtype=np.uint32),
                'position': pos,
                'rotation_z': 0.0,
                'scale': np.array([1, 1, 1], dtype=np.float32),
                'speed': random.uniform(50, 120),
                'radius': r
            })
            stone_objs.append(stone_obj)

        # Pick exactly three random stones to hold keys
        if len(stone_objs) >= 3:
            chosen_stones = random.sample(stone_objs, 3)
            for s in chosen_stones:
                key_verts, key_inds = CreateKeyIcon(
                    radius=10,  # small radius for the key
                    color=[1.0, 1.0, 0.0]
                )
                key_obj = Object(self.shaders[0], {
                    'vertices': np.array(key_verts, dtype=np.float32),
                    'indices': np.array(key_inds, dtype=np.uint32),
                    'position': s.properties['position'].copy() + np.array([0, 0, 1], dtype=np.float32),
                    'rotation_z': 0.0,
                    'scale': np.array([1, 1, 1], dtype=np.float32),
                    'speed': s.properties['speed'],
                    'has_key': True  # custom flag to indicate it's a key
                })
                stone_objs.append(key_obj)

        objs.extend(stone_objs)

        return objs

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
        # Move stones if they have a 'speed' property
        for obj in self.objects:
            if 'speed' in obj.properties:
                # Move from top to bottom (or vice versa)
                # print(time)
                obj.properties['position'][1] -= obj.properties['speed'] * time['deltaTime']
                # Reset if out of bounds
                if obj.properties['position'][1] < -360 or obj.properties['position'][1] > 360:
                    obj.properties['speed'] = -1 * obj.properties['speed']

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