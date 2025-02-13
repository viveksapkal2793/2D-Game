import numpy as np
from PIL import Image
from OpenGL.GL import *

def CreateCircle(center, radius, colour, points = 10, offset = 0, semi = False):
    vertices = [center[0], center[1], center[2], colour[0], colour[1], colour[2]]
    indices = []

    if semi == True:
        for i in range(points+1):
            vertices += [
                center[0] + radius * np.cos(float(i * np.pi)/points),
                center[1] + radius * np.sin(float(i * np.pi)/points),
                center[2],
                colour[0],
                colour[1],
                colour[2],
                ]
            
            ind1 = i+1
            ind2 = i+2 if i != points else 1
            indices += [0 + offset, ind1 + offset, ind2 + offset]
    else:
        for i in range(points):
            vertices += [
                center[0] + radius * np.cos(float(i * 2* np.pi)/points),
                center[1] + radius * np.sin(float(i * 2* np.pi)/points),
                center[2],
                colour[0],
                colour[1],
                colour[2],
                ]
            
            ind1 = i+1
            ind2 = i+2 if i != points-1 else 1
            indices += [0 + offset, ind1 + offset, ind2 + offset]

    return (vertices, indices)    

def CreateEllipse(center, radius_x, radius_y, color, points=20, offset=0):
    vertices = [center[0], center[1], center[2], color[0], color[1], color[2]]
    indices = []
    for i in range(points):
        angle = 2 * np.pi * i / points
        x = center[0] + radius_x * np.cos(angle)
        y = center[1] + radius_y * np.sin(angle)
        vertices.extend([x, y, center[2], color[0], color[1], color[2]])
        ind1 = i + 1
        ind2 = i + 2 if i != points - 1 else 1
        indices.extend([0 + offset, ind1 + offset, ind2 + offset])
    return vertices, indices

def CreatePlayer():

    vertices, indices = CreateCircle([0.0, 0.0, 0.0], 1.0, [220/255, 183/255, 139/255], 50, 0)

    eye_verts1, eye_inds1 = CreateCircle([0.4, -0.5, 0.05], 0.3, [1,1,1], 20, len(vertices)/6)
    vertices += eye_verts1
    indices += eye_inds1

    eye_verts2, eye_inds2 = CreateCircle([-0.4, -0.5, 0.05], 0.3, [1,1,1], 20, len(vertices)/6)
    vertices += eye_verts2
    indices += eye_inds2

    eye_verts3, eye_inds3 = CreateCircle([-0.4, -0.5, 0.10], 0.12, [0,0,0], 10, len(vertices)/6)
    vertices += eye_verts3
    indices += eye_inds3

    eye_verts4, eye_inds4 = CreateCircle([0.4, -0.5, 0.10], 0.12, [0,0,0], 10, len(vertices)/6)
    vertices += eye_verts4
    indices += eye_inds4

    eye_verts5, eye_inds5 = CreateCircle([0.0, 0.0, 0.2], 1.0, [1,0,0], 25, len(vertices)/6, True)
    vertices += eye_verts5
    indices += eye_inds5

    eye_verts6, eye_inds6 = CreateCircle([0.0, 0.95, 0.3], 0.3, [0.9,0.9,0.9], 20, len(vertices)/6)
    vertices += eye_verts6
    indices += eye_inds6

    return vertices, indices

def CreateSpaceEnemy(base_radius=30, ellipse_radius_x=40, ellipse_radius_y=20, small_circle_radius=5, color1=[0.8, 0.3, 0.3], color2=[0.9, 0.9, 0.4], color3=[0.8, 0.0, 0.8]):
    """
    Creates a UFO shape with a full circle at the bottom, a horizontal ellipse above it,
    and three small circles on top of the ellipse.
    """
    # Define vertices for the full circle (bottom part)
    vertices, indices = CreateCircle([0.0, 0.0, 0.0], base_radius, color1, 20)

    # Define vertices for the horizontal ellipse (middle part)
    ellipse_verts, ellipse_inds = CreateEllipse([0.0, -7.0, 0.1], ellipse_radius_x, ellipse_radius_y, color2, 20, len(vertices)/6)
    vertices += ellipse_verts
    indices += ellipse_inds

    # Define vertices for the three small circles on top of the ellipse
    small_circle_verts1, small_circle_inds1 = CreateCircle([-ellipse_radius_x / 2, -7.0, 0.2], small_circle_radius, color3, 10, len(vertices)/6)
    vertices += small_circle_verts1
    indices += small_circle_inds1

    small_circle_verts2, small_circle_inds2 = CreateCircle([0.0, -7.0, 0.2], small_circle_radius, color3, 10, len(vertices)/6)
    vertices += small_circle_verts2
    indices += small_circle_inds2

    small_circle_verts3, small_circle_inds3 = CreateCircle([ellipse_radius_x / 2, -7.0, 0.2], small_circle_radius, color3, 10, len(vertices)/6)
    vertices += small_circle_verts3
    indices += small_circle_inds3

    # # Combine all vertices and indices
    # vertices = circle_verts + ellipse_verts + small_circle_verts1 + small_circle_verts2 + small_circle_verts3
    # indices = circle_inds + ellipse_inds + small_circle_inds1 + small_circle_inds2 + small_circle_inds3

    return np.array(vertices, dtype=np.float32), np.array(indices, dtype=np.uint32)

def CreateJungleEnemy():

    vertices, indices = CreateCircle([0.0, 0.0, 0.0], 1.0, [180/255, 224/255, 150/255], 50, 0)

    eye_verts1, eye_inds1 = CreateCircle([0.4, -0.5, 0.05], 0.3, [1,1,1], 20, len(vertices)/6)
    vertices += eye_verts1
    indices += eye_inds1

    eye_verts2, eye_inds2 = CreateCircle([-0.4, -0.5, 0.05], 0.3, [1,1,1], 20, len(vertices)/6)
    vertices += eye_verts2
    indices += eye_inds2

    eye_verts3, eye_inds3 = CreateCircle([-0.4, -0.5, 0.10], 0.12, [0,1,0], 10, len(vertices)/6)
    vertices += eye_verts3
    indices += eye_inds3

    eye_verts4, eye_inds4 = CreateCircle([0.4, -0.5, 0.10], 0.12, [0,1,0], 10, len(vertices)/6)
    vertices += eye_verts4
    indices += eye_inds4

    eye_verts5, eye_inds5 = CreateCircle([0.0, 0.0, 0.2], 1.0, [1,0,0], 25, len(vertices)/6, True)
    vertices += eye_verts5
    indices += eye_inds5

    eye_verts6, eye_inds6 = CreateCircle([0.0, 0.95, 0.3], 0.3, [0.9,0.9,0.9], 20, len(vertices)/6)
    vertices += eye_verts6
    indices += eye_inds6

    return vertices, indices

def CreatebeachEnemy():

    vertices, indices = CreateCircle([0.0, 0.0, 0.0], 1.0, [180/255, 224/255, 150/255], 50, 0)

    eye_verts1, eye_inds1 = CreateCircle([0.4, -0.5, 0.05], 0.3, [1,1,1], 20, len(vertices)/6)
    vertices += eye_verts1
    indices += eye_inds1

    eye_verts2, eye_inds2 = CreateCircle([-0.4, -0.5, 0.05], 0.3, [1,1,1], 20, len(vertices)/6)
    vertices += eye_verts2
    indices += eye_inds2

    eye_verts3, eye_inds3 = CreateCircle([-0.4, -0.5, 0.10], 0.12, [0,1,0], 10, len(vertices)/6)
    vertices += eye_verts3
    indices += eye_inds3

    eye_verts4, eye_inds4 = CreateCircle([0.4, -0.5, 0.10], 0.12, [0,1,0], 10, len(vertices)/6)
    vertices += eye_verts4
    indices += eye_inds4

    eye_verts5, eye_inds5 = CreateCircle([0.0, 0.0, 0.2], 1.0, [1,0,0], 25, len(vertices)/6, True)
    vertices += eye_verts5
    indices += eye_inds5

    eye_verts6, eye_inds6 = CreateCircle([0.0, 0.95, 0.3], 0.3, [0.9,0.9,0.9], 20, len(vertices)/6)
    vertices += eye_verts6
    indices += eye_inds6

    return vertices, indices

def CreateBackground():
    grassColour = [0,1,0]
    waterColour = [0,0,1]

    vertices = [
        -500.0, 500.0, -0.9, grassColour[0], grassColour[1], grassColour[2],
        -400.0, 500.0, -0.9, grassColour[0], grassColour[1], grassColour[2],
        -400.0, -500.0, -0.9, grassColour[0], grassColour[1], grassColour[2],
        -500.0, -500.0, -0.9, grassColour[0], grassColour[1], grassColour[2],

        500.0, 500.0, -0.9, grassColour[0], grassColour[1], grassColour[2],
        400.0, 500.0, -0.9, grassColour[0], grassColour[1], grassColour[2],
        400.0, -500.0, -0.9, grassColour[0], grassColour[1], grassColour[2],
        500.0, -500.0, -0.9, grassColour[0], grassColour[1], grassColour[2],

        -400.0, 500.0, -0.9, waterColour[0], waterColour[1], waterColour[2],
        400.0, 500.0, -0.9, waterColour[0], waterColour[1], waterColour[2],
        400.0, -500.0, -0.9, waterColour[0], waterColour[1], waterColour[2],
        -400.0, -500.0, -0.9, waterColour[0], waterColour[1], waterColour[2],
    ]

    indices = [
        0,1,2, 0,3,2,
        8,9,10, 8,11,10,
        4,5,6, 4,7,6
    ]

    return vertices, indices

playerVerts, playerInds = CreatePlayer()
playerProps = {
    'name': 'player',

    'vertices' : np.array(playerVerts, dtype = np.float32),
    
    'indices' : np.array(playerInds, dtype = np.uint32),

    'position' : np.array([0, 0, 0], dtype = np.float32),

    'rotation_z' : 0.0,

    'scale' : np.array([30, 30, 1], dtype = np.float32),

    'sens' : 125,

    'velocity' : np.array([0, 0, 0], dtype = np.float32),

    'radius': 25
}

backgroundVerts, backgroundInds = CreateBackground()
backgroundProps = {
    'name': 'background',

    'vertices' : np.array(backgroundVerts, dtype = np.float32),
    
    'indices' : np.array(backgroundInds, dtype = np.uint32),

    'position' : np.array([0, 0, 0], dtype = np.float32),

    'rotation_z' : 0.0,

    'scale' : np.array([1, 1, 1], dtype = np.float32),

    'boundary' : [500.0, -500.0, 500.0, 500.0],

    'beach_banks': [-400.0, 400.0]
}

# =========================
# NEW: Space biome geometry split
# =========================
def CreateSpaceBiome():
    spaceColour = [0.1, 0.1, 0.1]
    planetColour = [0.5, 0.3, 0.7]
    vertices = [
        # Top quad (planet colour)
        500.0, 500.0, -0.9, planetColour[0], planetColour[1], planetColour[2], 1.0, 1.0,
        500.0, 400.0, -0.9, planetColour[0], planetColour[1], planetColour[2], 1.0, 0.0,
        -500.0, 400.0, -0.9, planetColour[0], planetColour[1], planetColour[2], 0.0, 0.0,
        -500.0, 500.0, -0.9, planetColour[0], planetColour[1], planetColour[2], 0.0, 1.0,
        # Bottom quad (planet colour)
        500.0, -500.0, -0.9, planetColour[0], planetColour[1], planetColour[2], 1.0, 1.0,
        500.0, -400.0, -0.9, planetColour[0], planetColour[1], planetColour[2], 1.0, 0.0,
        -500.0, -400.0, -0.9, planetColour[0], planetColour[1], planetColour[2], 0.0, 0.0,
        -500.0, -500.0, -0.9, planetColour[0], planetColour[1], planetColour[2], 0.0, 1.0,
        # Middle quad (space colour – this will be textured)
        500.0, 400.0, -0.9, spaceColour[0], spaceColour[1], spaceColour[2], 1.0, 1.0,
        500.0, -400.0, -0.9, spaceColour[0], spaceColour[1], spaceColour[2], 1.0, 0.0,
        -500.0, -400.0, -0.9, spaceColour[0], spaceColour[1], spaceColour[2], 0.0, 0.0,
        -500.0, 400.0, -0.9, spaceColour[0], spaceColour[1], spaceColour[2], 0.0, 1.0,
    ]
    indices = [
        0,1,2, 0,3,2,      # top quad
        8,9,10, 8,11,10,   # middle quad
        4,5,6, 4,7,6       # bottom quad
    ]
    return np.array(vertices, dtype=np.float32), np.array(indices, dtype=np.uint32)

def CreateSpaceCliffs():
    # Extract the top & bottom quads (first 8 vertices)
    full_verts, _ = CreateSpaceBiome()
    # Each vertex has 8 floats. Get vertices 0-7.
    cliffs_vertices = full_verts[:8 * 8]
    # Remapped indices for two quads:
    cliffs_indices = np.array([0,1,2, 0,3,2, 4,5,6, 4,7,6], dtype=np.uint32)
    return cliffs_vertices, cliffs_indices

def CreateSpaceMiddle():
    # Extract the middle quad (vertices 8-11)
    full_verts, _ = CreateSpaceBiome()
    middle_vertices = full_verts[8 * 8:]
    middle_indices = np.array([0,1,2, 0,3,2], dtype=np.uint32)
    return middle_vertices, middle_indices

# Create property dictionaries for space map:
spaceCliffsVerts, spaceCliffsInds = CreateSpaceCliffs()
spaceCliffsProps = {
    'name': 'space_cliffs',
    'vertices': np.array(spaceCliffsVerts, dtype=np.float32),
    'indices': np.array(spaceCliffsInds, dtype=np.uint32),
    'position': np.array([0, 0, 0], dtype=np.float32),
    'rotation_z': 0.0,
    'scale': np.array([1, 1, 1], dtype=np.float32),
    'texture_path': "assets/objects/planet.jpg"
}

spaceMiddleVerts, spaceMiddleInds = CreateSpaceMiddle()
spaceMiddleProps = {
    'name': 'space_middle',
    'vertices': np.array(spaceMiddleVerts, dtype=np.float32),
    'indices': np.array(spaceMiddleInds, dtype=np.uint32),
    'position': np.array([0, 0, 0], dtype=np.float32),
    'rotation_z': 0.0,
    'scale': np.array([1, 1, 1], dtype=np.float32),
    'texture_path': "assets/objects/space.jpg"
}

def CreateJungleBiome():
    """
    Example with 8 floats per vertex: x, y, z, r, g, b, u, v
    """
    cliffColour = [0.5, 0.5, 0.0]
    grasslandColour = [0.0, 1.0, 0.0]

    vertices = [
        # Cliff top
        500.0, 500.0, -0.9, cliffColour[0], cliffColour[1], cliffColour[2], 1.0, 1.0,
        500.0, 400.0, -0.9, cliffColour[0], cliffColour[1], cliffColour[2], 1.0, 0.0,
        -500.0, 400.0, -0.9, cliffColour[0], cliffColour[1], cliffColour[2], 0.0, 0.0,
        -500.0, 500.0, -0.9, cliffColour[0], cliffColour[1], cliffColour[2], 0.0, 1.0,

        # Cliff bottom
        500.0, -500.0, -0.9, cliffColour[0], cliffColour[1], cliffColour[2], 1.0, 1.0,
        500.0, -400.0, -0.9, cliffColour[0], cliffColour[1], cliffColour[2], 1.0, 0.0,
        -500.0, -400.0, -0.9, cliffColour[0], cliffColour[1], cliffColour[2], 0.0, 0.0,
        -500.0, -500.0, -0.9, cliffColour[0], cliffColour[1], cliffColour[2], 0.0, 1.0,

        # Central grass (textured)
        500.0, 400.0, -0.9, grasslandColour[0], grasslandColour[1], grasslandColour[2], 1.0, 1.0,
        500.0, -400.0, -0.9, grasslandColour[0], grasslandColour[1], grasslandColour[2], 1.0, 0.0,
        -500.0, -400.0, -0.9, grasslandColour[0], grasslandColour[1], grasslandColour[2], 0.0, 0.0,
        -500.0, 400.0, -0.9, grasslandColour[0], grasslandColour[1], grasslandColour[2], 0.0, 1.0,
    ]

    indices = [
        0,1,2, 0,3,2,
        8,9,10, 8,11,10,
        4,5,6, 4,7,6
    ]

    return np.array(vertices, dtype=np.float32), np.array(indices, dtype=np.uint32)


def CreateJungleCliffs():
    cliffColour = [0.5, 0.5, 0.0]
    vertices = [
        # Top rectangle (without texture coords; 6 floats per vertex)
        500.0, 500.0, -0.9, cliffColour[0], cliffColour[1], cliffColour[2], 1.0, 1.0,
        500.0, 400.0, -0.9, cliffColour[0], cliffColour[1], cliffColour[2], 1.0, 0.0,
        -500.0, 400.0, -0.9, cliffColour[0], cliffColour[1], cliffColour[2], 0.0, 0.0,
        -500.0, 500.0, -0.9, cliffColour[0], cliffColour[1], cliffColour[2], 0.0, 1.0,
        
        # Bottom rectangle
        500.0, -500.0, -0.9, cliffColour[0], cliffColour[1], cliffColour[2], 1.0, 1.0,
        500.0, -400.0, -0.9, cliffColour[0], cliffColour[1], cliffColour[2], 1.0, 0.0,
        -500.0, -400.0, -0.9, cliffColour[0], cliffColour[1], cliffColour[2], 0.0, 0.0,
        -500.0, -500.0, -0.9, cliffColour[0], cliffColour[1], cliffColour[2], 0.0, 1.0,
    ]
    indices = [
        0,1,2, 0,3,2,
        4,5,6, 4,7,6
    ]
    return np.array(vertices, dtype=np.float32), np.array(indices, dtype=np.uint32)

def CreateJungleGrass():
    grasslandColour = [0.0, 1.0, 0.0]
    # Middle rectangle with texture coordinates (8 floats per vertex)
    vertices = [
        500.0, 400.0, -0.9, grasslandColour[0], grasslandColour[1], grasslandColour[2], 1.0, 1.0,
        500.0, -400.0, -0.9, grasslandColour[0], grasslandColour[1], grasslandColour[2], 1.0, 0.0,
        -500.0, -400.0, -0.9, grasslandColour[0], grasslandColour[1], grasslandColour[2], 0.0, 0.0,
        -500.0, 400.0, -0.9, grasslandColour[0], grasslandColour[1], grasslandColour[2], 0.0, 1.0,
    ]
    indices = [
        0,1,2, 0,3,2
    ]
    return np.array(vertices, dtype=np.float32), np.array(indices, dtype=np.uint32)


cliffsVerts, cliffsInds = CreateJungleCliffs()
jungleCliffsProps = {
    'name': 'jungle_cliffs',
    'vertices': cliffsVerts,
    'indices': cliffsInds,
    'position': np.array([0, 0, 0], dtype=np.float32),
    'rotation_z': 0.0,
    'scale': np.array([1, 1, 1], dtype=np.float32),
    'texture_path': "assets/objects/cliff.jpg"
}

# Grass (middle)
grassVerts, grassInds = CreateJungleGrass()
jungleGrassProps = {
    'name': 'jungle_grass',
    'vertices': grassVerts,
    'indices': grassInds,
    'position': np.array([0, 0, 0], dtype=np.float32),
    'rotation_z': 0.0,
    'scale': np.array([1, 1, 1], dtype=np.float32),
    'texture_path': "assets/objects/grass.jpg"  # store path for deferred loading
}


def LoadTexture(file_path):
    """
    Simple texture loader using Pillow + OpenGL.
    """
    image = Image.open(file_path).convert("RGBA")
    img_data = image.tobytes()
    width, height = image.size

    tex_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex_id)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)

    glBindTexture(GL_TEXTURE_2D, 0)
    # print(tex_id)
    return tex_id


def CreatebeachBiome():
    landColour = [0,1,0]
    beachColour = [0,0,1]
    # Define vertices and indices for beach biome
    vertices = [
        # Define vertices for water, rocks, etc.
        500.0, 500.0, -0.9, landColour[0], landColour[1], landColour[2], 1.0, 1.0,
        500.0, 400.0, -0.9, landColour[0], landColour[1], landColour[2], 1.0, 0.0,
        -500.0, 400.0, -0.9, landColour[0], landColour[1], landColour[2], 0.0, 0.0,
        -500.0, 500.0, -0.9, landColour[0], landColour[1], landColour[2], 0.0, 1.0,

        500.0, -500.0, -0.9, landColour[0], landColour[1], landColour[2], 1.0, 1.0,
        500.0, -400.0, -0.9, landColour[0], landColour[1], landColour[2], 1.0, 0.0,
        -500.0, -400.0, -0.9, landColour[0], landColour[1], landColour[2], 0.0, 0.0,
        -500.0, -500.0, -0.9, landColour[0], landColour[1], landColour[2], 0.0, 1.0,

        500.0, 400.0, -0.9, beachColour[0], beachColour[1], beachColour[2], 1.0, 1.0,
        500.0, -400.0, -0.9, beachColour[0], beachColour[1], beachColour[2], 1.0, 0.0,
        -500.0, -400.0, -0.9, beachColour[0], beachColour[1], beachColour[2], 0.0, 0.0,
        -500.0, 400.0, -0.9, beachColour[0], beachColour[1], beachColour[2], 0.0, 1.0,
    ]
    indices = [
        # Define indices for water, rocks, etc.
        0,1,2, 0,3,2,
        8,9,10, 8,11,10,
        4,5,6, 4,7,6
    ]
    return np.array(vertices, dtype=np.float32), np.array(indices, dtype=np.uint32)

def CreatebeachWater():
    beachColour = [0,0,1]
    # Define vertices and indices for beach water
    vertices = [
        # Define vertices for water
        500.0, 400.0, -0.9, beachColour[0], beachColour[1], beachColour[2], 1.0, 1.0,
        500.0, -400.0, -0.9, beachColour[0], beachColour[1], beachColour[2], 1.0, 0.0,
        -500.0, -400.0, -0.9, beachColour[0], beachColour[1], beachColour[2], 0.0, 0.0,
        -500.0, 400.0, -0.9, beachColour[0], beachColour[1], beachColour[2], 0.0, 1.0,
    ]
    indices = [
        # Define indices for water
        0,1,2, 0,3,2
    ]
    return np.array(vertices, dtype=np.float32), np.array(indices, dtype=np.uint32)

def CreatebeachBanks():
    landColour = [0,1,0]
    # Define vertices and indices for beach banks
    vertices = [
        # Define vertices for beach banks
        500.0, 500.0, -0.9, landColour[0], landColour[1], landColour[2], 1.0, 1.0,
        500.0, 400.0, -0.9, landColour[0], landColour[1], landColour[2], 1.0, 0.0,
        -500.0, 400.0, -0.9, landColour[0], landColour[1], landColour[2], 0.0, 0.0,
        -500.0, 500.0, -0.9, landColour[0], landColour[1], landColour[2], 0.0, 1.0,

        500.0, -500.0, -0.9, landColour[0], landColour[1], landColour[2], 1.0, 1.0,
        500.0, -400.0, -0.9, landColour[0], landColour[1], landColour[2], 1.0, 0.0,
        -500.0, -400.0, -0.9, landColour[0], landColour[1], landColour[2], 0.0, 0.0,
        -500.0, -500.0, -0.9, landColour[0], landColour[1], landColour[2], 0.0, 1.0,
    ]
    indices = [
        # Define indices for beach banks
        0,1,2, 0,3,2,
        4,5,6, 4,7,6
    ]
    return np.array(vertices, dtype=np.float32), np.array(indices, dtype=np.uint32)

beachbankverts, beachbankinds = CreatebeachBanks()
beachBankProps = {  
    'name': 'beach_banks',
    'vertices': beachbankverts,
    'indices': beachbankinds,
    'position': np.array([0, 0, 0], dtype=np.float32),
    'rotation_z': 0.0,
    'scale': np.array([1, 1, 1], dtype=np.float32),
    'texture_path': "assets/objects/beach.jpeg"
}

beachwaterverts, beachwaterinds = CreatebeachWater()
beachWaterProps = {
    'name': 'beach_water',
    'vertices': beachwaterverts,
    'indices': beachwaterinds,
    'position': np.array([0, 0, 0], dtype=np.float32),
    'rotation_z': 0.0,
    'scale': np.array([1, 1, 1], dtype=np.float32),
    'texture_path': "assets/objects/river.jpeg"
}

def CreateStone(radius=15, color=[0.7, 0.7, 0.7], center=[0.0, 0.0, 0.0], points=20):
    
    vertices = []
    indices = []
    for i in range(points):
        angle = 2 * np.pi * i / points
        x = center[0] + radius * np.cos(angle)
        y = center[1] + radius * np.sin(angle)
        u = (np.cos(angle) + 1) / 2  # Texture coordinate u
        v = (np.sin(angle) + 1) / 2  # Texture coordinate v
        vertices.extend([x, y, center[2], color[0], color[1], color[2], u, v])
        indices.extend([0, i + 1, (i + 1) % points + 1])
    # Center vertex
    vertices.extend([center[0], center[1], center[2], color[0], color[1], color[2], 0.5, 0.5])
    return vertices, indices

def CreateKeyIcon(radius=5, color=[1.0, 1.0, 0.0], points=12):
    """
    Creates a small circular 'key' graphic.
    Reuse your CreateCircle function, or define your own small circle here.
    """
    verts, inds = CreateCircle([0.0, 0.0, 0.0], radius, color, points)
    return verts, inds

def CreateBoat(base_width=80, top_width=40, height=60, color1=[0.7, 0.7, 0.7], color2=[0.5, 0.5, 0.5]):
    """
    Creates a boat shape with a trapezium at the bottom and a triangle above it.
    """
    half_base_width = base_width / 2
    half_top_width = top_width / 2
    half_height = height / 2

    # Define vertices for the trapezium (bottom part)
    vertices = [
        # Bottom trapezium
        -half_top_width, -half_height, 0.0, color1[0], color1[1], color1[2], 0.0, 0.0,  # Bottom left
        half_top_width, -half_height, 0.0, color1[0], color1[1], color1[2], 1.0, 0.0,   # Bottom right
        half_base_width, 0.0, 0.0, color1[0], color1[1], color1[2], 1.0, 1.0,             # Top right
        -half_base_width, 0.0, 0.0, color1[0], color1[1], color1[2], 0.0, 1.0,            # Top left
    ]

    # Define vertices for the triangle (top part)
    vertices += [
        # Top triangle
        -half_top_width, 0.0, 0.0, color2[0], color2[1], color2[2], 0.0, 0.0,            # Bottom left
        half_top_width, 0.0, 0.0, color2[0], color2[1], color2[2], 1.0, 0.0,             # Bottom right
        0.0, half_height, 0.0, color2[0], color2[1], color2[2], 0.5, 1.0,                # Top center
    ]

    # Define indices for the trapezium and triangle
    indices = [
        0, 1, 2, 0, 2, 3,  # Trapezium
        4, 5, 6             # Triangle
    ]

    return np.array(vertices, dtype=np.float32), np.array(indices, dtype=np.uint32)

def CreateHeartIcon(radius=8, color=[1.0, 0.0, 0.0]):
    """
    Creates a simple heart shape using two circles plus a triangle-like shape.
    You can tweak points for a more detailed heart.
    """
    # Left circle
    left_circle_verts, left_circle_inds = CreateCircle([-0.5, 0.0, 1.0], radius, color, 16, 0)
    # Right circle (shift x by +0.5 so it joins the left circle)
    right_circle_verts, right_circle_inds = CreateCircle([0.5, 0.0, 1.0], radius, color, 16, len(left_circle_verts)//6)
    
    # Triangle portion (approx)
    triangle_verts = [
        0.0, -1.0*radius, 1.0, color[0], color[1], color[2],
        -1.0*radius, 0.0, 1.0, color[0], color[1], color[2],
        1.0*radius, 0.0, 1.0, color[0], color[1], color[2],
    ]
    triangle_inds = [0,1,2]
    # Adjust the triangle indices offset
    tri_offset = (len(left_circle_verts) + len(right_circle_verts)) // 6

    # Combine everything
    verts = left_circle_verts + right_circle_verts + triangle_verts
    inds = left_circle_inds + right_circle_inds + [
        triangle_inds[0] + tri_offset,
        triangle_inds[1] + tri_offset,
        triangle_inds[2] + tri_offset
    ]
    return verts, inds


# Example properties for biomes
spaceVerts, spaceInds = CreateSpaceBiome()
spaceProps = {
    'name': 'spacemap',
    'vertices': np.array(spaceVerts, dtype=np.float32),
    'indices': np.array(spaceInds, dtype=np.uint32),
    'position': np.array([0, 0, 0], dtype=np.float32),
    'rotation_z': 0.0,
    'scale': np.array([1, 1, 1], dtype=np.float32),
}

jungleVerts, jungleInds = CreateJungleBiome()
jungleProps = {
    'name': 'junglemap',
    'vertices': np.array(jungleVerts, dtype=np.float32),
    'indices': np.array(jungleInds, dtype=np.uint32),
    'position': np.array([0, 0, 0], dtype=np.float32),
    'rotation_z': 0.0,
    'scale': np.array([1, 1, 1], dtype=np.float32),

    # If you have a grass texture in "assets/textures/grass.png"
    # 'texture_id': LoadTexture("assets/objects/grass.jpg")
    'texture_path': "assets/objects/grass.jpg" 
}

beachVerts, beachInds = CreatebeachBiome()
beachProps = {
    'name': 'beachmap',
    'vertices': np.array(beachVerts, dtype=np.float32),
    'indices': np.array(beachInds, dtype=np.uint32),
    'position': np.array([0, 0, 0], dtype=np.float32),
    'rotation_z': 0.0,
    'scale': np.array([1, 1, 1], dtype=np.float32),
}