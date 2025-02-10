import imgui
import numpy as np
import random
from utils.graphics import Object, Camera, Shader
from assets.shaders.shaders import object_shader
from assets.objects.objects import playerProps, backgroundProps, spaceProps, jungleProps, riverProps, CreateStone, CreateKeyIcon, CreateHeartIcon

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
        self.screen = -1
        self.camera = Camera(height, width)
        self.shaders = [Shader(object_shader['vertex_shader'], object_shader['fragment_shader'])]
        self.objects = []
        self.maps = [self.create_jungle_map(), self.create_river_map(), self.create_space_map()]
        self.current_map = 0
        # self.player = Object(self.shaders[0], playerProps)
        self.player_on_rock = None
        self.jump_charge_time = 0.0
        self.health = 100
        self.lives = 3
        self.total_time = 0.0
        self.is_game_over = False
        self.is_game_won = False

        # Store hold times for W, A, S, D in a dictionary
        self.keyHoldTimes = {
            'W': 0.0,
            'A': 0.0,
            'S': 0.0,
            'D': 0.0
        }

    def CreateDoorObject(self, name: str, position: np.ndarray, radius: float=40.0):
        """Creates a simple rectangular or circular 'door' object."""
        # If you have a custom function to create geometry, use it here
        # For simplicity, let's re-use a circle from CreateStone
        
        verts, inds = CreateStone(radius=radius, color=[0.7, 0.2, 0.2])
        return Object(self.shaders[0], {
            'name': name,
            'vertices': np.array(verts, dtype=np.float32),
            'indices': np.array(inds, dtype=np.uint32),
            'position': position,
            'rotation_z': 0.0,
            'scale': np.array([1, 1, 1], dtype=np.float32),
            'speed': 0.0,               # Doors are stationary
            'radius': radius,           # For distance checks
            'attached_to_player': False # Not used, but included for consistency
        })

    def create_space_map(self):
        space = Object(self.shaders[0], spaceProps)
        player = Object(self.shaders[0], playerProps)
        player.properties['position'] = np.array([-420, -450, 0], dtype=np.float32)
        objs =  [space, player]
        stone_objs = []

        # Add bottom-left entry "door"
        entry_door = self.CreateDoorObject('entry_door', np.array([-450, -450, 0], dtype=np.float32), radius=30)
        objs.append(entry_door)
        # Add top-right exit "door"
        exit_door = self.CreateDoorObject('exit_door', np.array([450, 450, 0], dtype=np.float32), radius=40)
        objs.append(exit_door)

        # Add random non-overlapping stones
        for _ in range(8):
            r = 40
            pos = random_nonoverlapping_position(objs, r)
            if pos is None:
                # If we can't find a valid spot, just skip or place at a default
                continue

            stone_verts, stone_inds = CreateStone(radius=r, color=[0.7, 0.7, 0.7])
            stone_obj = Object(self.shaders[0], {
                'name': 'stone',
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
                    'name': 'key',
                    'vertices': np.array(key_verts, dtype=np.float32),
                    'indices': np.array(key_inds, dtype=np.uint32),
                    'position': s.properties['position'].copy() + np.array([0, 0, 1], dtype=np.float32),
                    'rotation_z': 0.0,
                    'scale': np.array([1, 1, 1], dtype=np.float32),
                    'speed': s.properties['speed'],
                    'has_key': True,  # custom flag to indicate it's a key
                    'attached_to_player': False
                })
                stone_objs.append(key_obj)

        objs.extend(stone_objs)

        return objs

    def create_jungle_map(self):
        jungle = Object(self.shaders[0], jungleProps)
        player = Object(self.shaders[0], playerProps)
        player.properties['position'] = np.array([-420, -450, 0], dtype=np.float32)
        objs =  [jungle, player]
        stone_objs = []

        # Add bottom-left entry "door"
        entry_door = self.CreateDoorObject('entry_door', np.array([-450, -450, 0], dtype=np.float32), radius=30)
        objs.append(entry_door)
        # Add top-right exit "door"
        exit_door = self.CreateDoorObject('exit_door', np.array([450, 450, 0], dtype=np.float32), radius=40)
        objs.append(exit_door)

        # Add random non-overlapping stones
        for _ in range(8):
            r = 40
            pos = random_nonoverlapping_position(objs, r)
            if pos is None:
                # If we can't find a valid spot, just skip or place at a default
                continue

            stone_verts, stone_inds = CreateStone(radius=r, color=[0.7, 0.7, 0.7])
            stone_obj = Object(self.shaders[0], {
                'name': 'stone',
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
                    'name': 'key',
                    'vertices': np.array(key_verts, dtype=np.float32),
                    'indices': np.array(key_inds, dtype=np.uint32),
                    'position': s.properties['position'].copy() + np.array([0, 0, 1], dtype=np.float32),
                    'rotation_z': 0.0,
                    'scale': np.array([1, 1, 1], dtype=np.float32),
                    'speed': s.properties['speed'],
                    'has_key': True,  # custom flag to indicate it's a key
                    'attached_to_player': False
                })
                stone_objs.append(key_obj)

        objs.extend(stone_objs)

        return objs

    def create_river_map(self):
        river = Object(self.shaders[0], riverProps)
        player = Object(self.shaders[0], playerProps)
        player.properties['position'] = np.array([-420, -450, 0], dtype=np.float32)
        objs =  [river, player]
        stone_objs = []

        # Add bottom-left entry "door"
        entry_door = self.CreateDoorObject('entry_door', np.array([-450, -450, 0], dtype=np.float32), radius=30)
        objs.append(entry_door)
        # Add top-right exit "door"
        exit_door = self.CreateDoorObject('exit_door', np.array([450, 450, 0], dtype=np.float32), radius=40)
        objs.append(exit_door)

        # Add random non-overlapping stones
        for _ in range(8):
            r = 40
            pos = random_nonoverlapping_position(objs, r)
            if pos is None:
                # If we can't find a valid spot, just skip or place at a default
                continue

            stone_verts, stone_inds = CreateStone(radius=r, color=[0.7, 0.7, 0.7])
            stone_obj = Object(self.shaders[0], {
                'name': 'stone',
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
                    'name': 'key',
                    'vertices': np.array(key_verts, dtype=np.float32),
                    'indices': np.array(key_inds, dtype=np.uint32),
                    'position': s.properties['position'].copy() + np.array([0, 0, 1], dtype=np.float32),
                    'rotation_z': 0.0,
                    'scale': np.array([1, 1, 1], dtype=np.float32),
                    'speed': s.properties['speed'],
                    'has_key': True, # custom flag to indicate it's a key
                    'attached_to_player': False
                })
                stone_objs.append(key_obj)

        objs.extend(stone_objs)

        return objs

    def InitScreen(self):
        # self.objects = self.maps[self.current_map]
        
        if self.screen == 0:
            self.current_map = 0
            self.objects = self.maps[0]
        if self.screen == 1:
            self.current_map = 1
            self.objects = self.maps[1]
        if self.screen == 2:
            self.current_map = 2
            self.objects = self.maps[2]

    def ProcessFrame(self, inputs, time):
        if self.screen == -1:
            self.screen = 0
            self.InitScreen()

        # Update hold times for WASD
        delta = time['deltaTime']
        for key in ['W', 'A', 'S', 'D']:
            if key in inputs:  # key is pressed
                self.keyHoldTimes[key] += delta
            else:
                self.keyHoldTimes[key] = 0.0

        self.total_time += delta

        if self.screen == 0:
            self.DrawText()
            self.UpdateScene(inputs, time)
            self.DrawScene()
            self.show_switch_map_button()
        if self.screen == 1:
            self.DrawText()
            self.UpdateScene(inputs, time)
            self.DrawScene()
            # self.show_switch_map_button()
        if self.screen == 2:
            self.DrawText()
            self.UpdateScene(inputs, time)
            self.DrawScene()
            # self.show_switch_map_button()

    def DrawText(self):
        if self.screen == 0:
           pass
        if self.screen == 1:
           pass
        if self.screen == 2:
           pass

    def DrawHUD(self):
        # Position and size the HUD at the very top
        imgui.set_next_window_position(0, 0)
        imgui.set_next_window_size(self.width, 30)  # 30 px in height, adjust as needed

        # Begin a new ImGui window for the HUD
        imgui.begin("HUD", True,
                    flags=imgui.WINDOW_NO_TITLE_BAR | 
                          imgui.WINDOW_NO_RESIZE |
                          imgui.WINDOW_NO_MOVE |
                          imgui.WINDOW_NO_SCROLLBAR |
                          imgui.WINDOW_NO_SAVED_SETTINGS)

        # Health ratio for the bar
        health_ratio = max(0.0, min(1.0, self.health / 100.0))
        # Color transitions from red (low health) to green (full health)
        bar_color = (1.0 - health_ratio, health_ratio, 0.0, 1.0)

        # Draw health bar
        imgui.text_unformatted("Health: ")
        imgui.same_line()
        imgui.push_style_color(imgui.COLOR_PLOT_HISTOGRAM, *bar_color)
        imgui.progress_bar(health_ratio, size=(self.width * 0.3, 0), overlay="")
        imgui.pop_style_color()

        imgui.same_line()
        imgui.text_unformatted(f"                Time: {int(self.total_time)}s")

        # Draw heart icons for lives (using text hearts, but you could use textures if desired)
        imgui.same_line()
        hearts_str = f"                 Lives: {self.lives}"
        imgui.text_unformatted(hearts_str)

        imgui.same_line()
        imgui.text_unformatted(f"                Map: {self.screen + 1}")

        imgui.end()

    def UpdateScene(self, inputs, time):

        # If lives drop to zero, mark game over
        if self.lives <= 0:
            self.is_game_over = True
            return
                
        # Move the player with WASD
        delta = time['deltaTime']
        speed = 100.0  # Adjust as needed
        self.health -= 10*delta  # Reduce health over time

        # Check if health reached zero
        if self.health <= 0:
            self.lives -= 1
            if self.lives > 0:
                self.health = 100
                # Respawn at the bottom-left "entry_door"
                spawn_door = next((o for o in self.objects if o.properties['name'] == 'entry_door'), None)
                if spawn_door:
                    player_obj = next((o for o in self.objects if o.properties['name'] == 'player'), None)
                    if player_obj:
                        player_obj.properties['position'] = spawn_door.properties['position'].copy()
            else:
                self.is_game_over = True
                return

        for obj in self.objects:
            # Assuming 'player' can be identified by a property check or simply check if it has 'velocity'
            if obj is not None and obj.properties['name'] == 'player':
                if 'W' in inputs:
                    obj.properties['position'][1] += speed * delta
                if 'S' in inputs:
                    obj.properties['position'][1] -= speed * delta
                if 'A' in inputs:
                    obj.properties['position'][0] -= speed * delta
                if 'D' in inputs:
                    obj.properties['position'][0] += speed * delta

            # Clamp the player's position to avoid going out of screen bounds
            x, y, z = obj.properties['position']
            x = max(-470.0, min(470.0, x))
            y = max(-450.0, min(440.0, y))
            obj.properties['position'] = np.array([x, y, z], dtype=np.float32)


        # Move stones if they have a 'speed' property
        for obj in self.objects:
            if obj.properties['name'] == 'stone' or obj.properties['name'] == 'key':
                # Move from top to bottom (or vice versa)
                # print(time)
                obj.properties['position'][1] -= obj.properties['speed'] * time['deltaTime']
                # Reset if out of bounds
                if obj.properties['position'][1] < -360 or obj.properties['position'][1] > 360:
                    obj.properties['speed'] = -1 * obj.properties['speed']


        if self.screen == 0:

            jump_key = 'SPACE'  
            min_jump = 50.0
            max_jump = 300.0

            self.player_on_rock = None
            player_obj = next((o for o in self.objects if o.properties['name'] == 'player'), None)
            if player_obj:
                for rock in (o for o in self.objects if o.properties['name'] == 'stone'):
                    dist = np.linalg.norm(player_obj.properties['position'] - rock.properties['position'])
                    if dist < rock.properties['radius']:
                        self.player_on_rock = rock
                        break

            # If on rock, move player along with rock
            if self.player_on_rock is not None and player_obj:
                # The rock moves downward => replicate the same shift
                rock = self.player_on_rock
                player_obj.properties['position'][1] -= rock.properties['speed'] * delta
                
                # Check if there's a key on this same rock
                for key_obj in (o for o in self.objects if o.properties['name'] == 'key'):
                    dist_key_rock = np.linalg.norm(key_obj.properties['position'] - rock.properties['position'])
                    if dist_key_rock < rock.properties['radius']:
                        # Attach key to player
                        key_obj.properties['attached_to_player'] = True

            # If a key is attached to the player, sync its position
            if player_obj:
                x_pos = -40
                for key_obj in (o for o in self.objects if o.properties['name'] == 'key'):
                    if key_obj.properties.get('attached_to_player'):
                        x_pos += 20
                        key_obj.properties['position'] = player_obj.properties['position'] + np.array([x_pos, 7, 2], dtype=np.float32)

            # Accumulate jump charge if jump key is pressed
            if jump_key in inputs:
                self.jump_charge_time += delta
                self.jump_charge_time = min(self.jump_charge_time, 7.0)  # clamp max charge time
            # On jump key release, perform jump
            else:
                if self.jump_charge_time > 0.0:
                    # print(f"Jumping with charge time: {self.jump_charge_time}")
                    distance_factor = self.jump_charge_time * 200.0
                    jump_dist = max(min_jump, min(max_jump, distance_factor))
                    # Use last movement direction or a chosen direction
                    dx = 0.0
                    dy = 0.0
                    # if 'W' in inputs: dy += 1.0
                    # if 'S' in inputs: dy -= 1.0
                    # if 'A' in inputs: dx -= 1.0
                    # if 'D' in inputs: dx += 1.0
                    
                    # Use hold times to define direction
                    dy += self.keyHoldTimes['W']
                    dy -= self.keyHoldTimes['S']
                    dx += self.keyHoldTimes['D']
                    dx -= self.keyHoldTimes['A']
                    # Normalize direction
                    length = (dx**2 + dy**2)**0.5
                    # print(f"Jump direction: {dx}, {dy}")
                    if length > 0.0:
                        dx /= length
                        dy /= length
                    # Apply jump
                    # print(f"Jumping with distance: {jump_dist}")
                    # print(f'self.player.properties["position"]: {player_obj.properties["position"]}')
                    if player_obj:
                        player_obj.properties['position'][0] += dx * jump_dist
                        player_obj.properties['position'][1] += dy * jump_dist
                    # print(f'self.player.properties["position"]: {player_obj.properties["position"]}')

                self.jump_charge_time = 0.0

            # Door logic: if player is near exit_door and has 3 keys, move keys into door slots and switch map
            if player_obj:
                exit_door_obj = next((o for o in self.objects if o.properties['name'] == 'exit_door'), None)
                if exit_door_obj:
                    dist_door = np.linalg.norm(player_obj.properties['position'] - exit_door_obj.properties['position'])
                    if dist_door < exit_door_obj.properties['radius']:
                        # Count attached keys
                        attached_keys = [k for k in self.objects if k.properties.get('attached_to_player')]
                        if len(attached_keys) >= 3:
                            # Position the keys in the door's “slots”
                            slot_offset = -10
                            for k in attached_keys[:3]:
                                slot_offset += 10
                                k.properties['position'] = exit_door_obj.properties['position'] + np.array([slot_offset, 0, 5], dtype=np.float32)
                                k.properties['attached_to_player'] = False
                            # Switch map
                            self.switch_map()

        if self.screen == 1:

            jump_key = 'SPACE'  
            min_jump = 50.0
            max_jump = 300.0

            self.player_on_rock = None
            player_obj = next((o for o in self.objects if o.properties['name'] == 'player'), None)
            if player_obj:
                for rock in (o for o in self.objects if o.properties['name'] == 'stone'):
                    dist = np.linalg.norm(player_obj.properties['position'] - rock.properties['position'])
                    if dist < rock.properties['radius']:
                        self.player_on_rock = rock
                        break

            # If on rock, move player along with rock
            if self.player_on_rock is not None and player_obj:
                # The rock moves downward => replicate the same shift
                rock = self.player_on_rock
                player_obj.properties['position'][1] -= rock.properties['speed'] * delta
                
                # Check if there's a key on this same rock
                for key_obj in (o for o in self.objects if o.properties['name'] == 'key'):
                    dist_key_rock = np.linalg.norm(key_obj.properties['position'] - rock.properties['position'])
                    if dist_key_rock < rock.properties['radius']:
                        # Attach key to player
                        key_obj.properties['attached_to_player'] = True

            # If a key is attached to the player, sync its position
            if player_obj:
                x_pos = -40
                for key_obj in (o for o in self.objects if o.properties['name'] == 'key'):
                    if key_obj.properties.get('attached_to_player'):
                        x_pos += 20
                        key_obj.properties['position'] = player_obj.properties['position'] + np.array([x_pos, 7, 2], dtype=np.float32)

            # Accumulate jump charge if jump key is pressed
            if jump_key in inputs:
                self.jump_charge_time += delta
                self.jump_charge_time = min(self.jump_charge_time, 7.0)  # clamp max charge time
            # On jump key release, perform jump
            else:
                if self.jump_charge_time > 0.0:
                    # print(f"Jumping with charge time: {self.jump_charge_time}")
                    distance_factor = self.jump_charge_time * 200.0
                    jump_dist = max(min_jump, min(max_jump, distance_factor))
                    # Use last movement direction or a chosen direction
                    dx = 0.0
                    dy = 0.0
                    # if 'W' in inputs: dy += 1.0
                    # if 'S' in inputs: dy -= 1.0
                    # if 'A' in inputs: dx -= 1.0
                    # if 'D' in inputs: dx += 1.0
                    
                    # Use hold times to define direction
                    dy += self.keyHoldTimes['W']
                    dy -= self.keyHoldTimes['S']
                    dx += self.keyHoldTimes['D']
                    dx -= self.keyHoldTimes['A']
                    # Normalize direction
                    length = (dx**2 + dy**2)**0.5
                    # print(f"Jump direction: {dx}, {dy}")
                    if length > 0.0:
                        dx /= length
                        dy /= length
                    # Apply jump
                    # print(f"Jumping with distance: {jump_dist}")
                    # print(f'self.player.properties["position"]: {player_obj.properties["position"]}')
                    if player_obj:
                        player_obj.properties['position'][0] += dx * jump_dist
                        player_obj.properties['position'][1] += dy * jump_dist
                    # print(f'self.player.properties["position"]: {player_obj.properties["position"]}')

                self.jump_charge_time = 0.0

            # Door logic: if player is near exit_door and has 3 keys, move keys into door slots and switch map
            if player_obj:
                exit_door_obj = next((o for o in self.objects if o.properties['name'] == 'exit_door'), None)
                if exit_door_obj:
                    dist_door = np.linalg.norm(player_obj.properties['position'] - exit_door_obj.properties['position'])
                    if dist_door < exit_door_obj.properties['radius']:
                        # Count attached keys
                        attached_keys = [k for k in self.objects if k.properties.get('attached_to_player')]
                        if len(attached_keys) >= 3:
                            # Position the keys in the door's “slots”
                            slot_offset = -10
                            for k in attached_keys[:3]:
                                slot_offset += 10
                                k.properties['position'] = exit_door_obj.properties['position'] + np.array([slot_offset, 0, 5], dtype=np.float32)
                                k.properties['attached_to_player'] = False
                            # Switch map
                            self.switch_map()

        if self.screen == 2:

            jump_key = 'SPACE'  
            min_jump = 50.0
            max_jump = 300.0

            self.player_on_rock = None
            player_obj = next((o for o in self.objects if o.properties['name'] == 'player'), None)
            if player_obj:
                for rock in (o for o in self.objects if o.properties['name'] == 'stone'):
                    dist = np.linalg.norm(player_obj.properties['position'] - rock.properties['position'])
                    if dist < rock.properties['radius']:
                        self.player_on_rock = rock
                        break

            # If on rock, move player along with rock
            if self.player_on_rock is not None and player_obj:
                # The rock moves downward => replicate the same shift
                rock = self.player_on_rock
                player_obj.properties['position'][1] -= rock.properties['speed'] * delta
                
                # Check if there's a key on this same rock
                for key_obj in (o for o in self.objects if o.properties['name'] == 'key'):
                    dist_key_rock = np.linalg.norm(key_obj.properties['position'] - rock.properties['position'])
                    if dist_key_rock < rock.properties['radius']:
                        # Attach key to player
                        key_obj.properties['attached_to_player'] = True

            # If a key is attached to the player, sync its position
            if player_obj:
                x_pos = -40
                for key_obj in (o for o in self.objects if o.properties['name'] == 'key'):
                    if key_obj.properties.get('attached_to_player'):
                        x_pos += 20
                        key_obj.properties['position'] = player_obj.properties['position'] + np.array([x_pos, 7, 2], dtype=np.float32)

            # Accumulate jump charge if jump key is pressed
            if jump_key in inputs:
                self.jump_charge_time += delta
                self.jump_charge_time = min(self.jump_charge_time, 7.0)  # clamp max charge time
            # On jump key release, perform jump
            else:
                if self.jump_charge_time > 0.0:
                    # print(f"Jumping with charge time: {self.jump_charge_time}")
                    distance_factor = self.jump_charge_time * 200.0
                    jump_dist = max(min_jump, min(max_jump, distance_factor))
                    # Use last movement direction or a chosen direction
                    dx = 0.0
                    dy = 0.0
                    # if 'W' in inputs: dy += 1.0
                    # if 'S' in inputs: dy -= 1.0
                    # if 'A' in inputs: dx -= 1.0
                    # if 'D' in inputs: dx += 1.0
                    
                    # Use hold times to define direction
                    dy += self.keyHoldTimes['W']
                    dy -= self.keyHoldTimes['S']
                    dx += self.keyHoldTimes['D']
                    dx -= self.keyHoldTimes['A']
                    # Normalize direction
                    length = (dx**2 + dy**2)**0.5
                    # print(f"Jump direction: {dx}, {dy}")
                    if length > 0.0:
                        dx /= length
                        dy /= length
                    # Apply jump
                    # print(f"Jumping with distance: {jump_dist}")
                    # print(f'self.player.properties["position"]: {player_obj.properties["position"]}')
                    if player_obj:
                        player_obj.properties['position'][0] += dx * jump_dist
                        player_obj.properties['position'][1] += dy * jump_dist
                    # print(f'self.player.properties["position"]: {player_obj.properties["position"]}')

                self.jump_charge_time = 0.0

            # Door logic: if player is near exit_door and has 3 keys, move keys into door slots and switch map
            if player_obj:
                exit_door_obj = next((o for o in self.objects if o.properties['name'] == 'exit_door'), None)
                if exit_door_obj:
                    dist_door = np.linalg.norm(player_obj.properties['position'] - exit_door_obj.properties['position'])
                    if dist_door < exit_door_obj.properties['radius']:
                        # Count attached keys
                        attached_keys = [k for k in self.objects if k.properties.get('attached_to_player')]
                        if len(attached_keys) >= 3:
                            # Position the keys in the door's “slots”
                            slot_offset = -10
                            for k in attached_keys[:3]:
                                slot_offset += 10
                                k.properties['position'] = exit_door_obj.properties['position'] + np.array([slot_offset, 0, 5], dtype=np.float32)
                                k.properties['attached_to_player'] = False
                            # Switch map
                            self.switch_map()

            
    def DrawScene(self):
        if self.screen in (0, 1, 2):
            for shader in self.shaders:
                self.camera.Update(shader)
 
            for obj in self.objects:
                obj.Draw()

            self.DrawHUD()
            
    def switch_map(self):
        self.current_map += 1
        self.screen += 1
        if self.current_map >= len(self.maps) or self.screen >= len(self.maps):
            # self.current_map = 0  # Loop back to the first map or handle game completion
            # self.screen = 0
            self.is_game_won = True
        else:
            self.InitScreen()
        
    def show_switch_map_button(self):
        imgui.begin("Switch Map", True)
        if imgui.button("Next Map"):
            self.switch_map()
        imgui.end()