import ctypes
import numpy as np
import copy
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader

class VBO:
    def __init__(self, vertices):
        self.ID = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.ID)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
    def Use(self):
        glBindBuffer(GL_ARRAY_BUFFER, self.ID)
    def Delete(self):
        glDeleteBuffers(1, (self.ID,))

class IBO:
    def __init__(self, indices):
        self.ID = glGenBuffers(1)
        self.count = len(indices)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ID)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)
    def Use(self):
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ID)
    def Delete(self):
        glDeleteBuffers(1, (self.ID,))

class VAO:
    def __init__(self, vbo : VBO, floats_per_vertex: int):
        """
        floats_per_vertex can be 6 or 8 depending on if we're including texture coords.
        """
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        vbo.Use()

        if floats_per_vertex == 8:
            # position (x,y,z), color (r,g,b), texcoord (u,v)
            stride = 8 * ctypes.sizeof(ctypes.c_float)

            # layout(location=0) => position
            glEnableVertexAttribArray(0)
            glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(0))

            # layout(location=1) => color
            glEnableVertexAttribArray(1)
            glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(3 * ctypes.sizeof(ctypes.c_float)))

            # layout(location=2) => UV
            glEnableVertexAttribArray(2)
            glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(6 * ctypes.sizeof(ctypes.c_float)))
        else:
            # Assume floats_per_vertex == 6 => position (x,y,z), color (r,g,b)
            stride = 6 * ctypes.sizeof(ctypes.c_float)

            glEnableVertexAttribArray(0)
            glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(0))

            glEnableVertexAttribArray(1)
            glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(3 * ctypes.sizeof(ctypes.c_float)))

            # layout(location=2) is not used => no texture coords

    def Use(self):
        glBindVertexArray(self.vao)

    def Delete(self):
        glDeleteVertexArrays(1, (self.vao,))

class Shader:
    def __init__(self, vertex_shader, fragment_shader):
        self.ID = compileProgram(
            compileShader(vertex_shader, GL_VERTEX_SHADER),
            compileShader(fragment_shader, GL_FRAGMENT_SHADER)
        )
        self.Use()

    def Use(self):
        glUseProgram(self.ID)

    def Delete(self):
        glDeleteProgram((self.ID,))

class Camera:
    def __init__(self, height, width):
        self.height = height
        self.width = width

    def Update(self, shader):
        shader.Use()
        # Orthographic-like projection
        camMatrix = np.array([
            [2.0/self.width, 0,0,0],
            [0,2.0/self.height,0,0],
            [0,0,-1/100,0],
            [0,0,0,1]
        ], dtype = np.float32)

        camMatrixLocation = glGetUniformLocation(shader.ID, "camMatrix")
        glUniformMatrix4fv(camMatrixLocation, 1, GL_TRUE, camMatrix)

class Object:
    def __init__(self, shader, properties):
        self.properties = copy.deepcopy(properties)

        vertices = self.properties['vertices']
        indices = self.properties['indices']

        # Determine if we have 6 or 8 floats/vertex
        # Just check one vertex to guess total
        # e.g. len(vertices) / number_of_verts
        # But simpler: if len(vertices) % 8 == 0 => 8 floats
        # else => 6 floats
        floats_per_vertex = 6
        if len(vertices) % 8 == 0:
            floats_per_vertex = 8

        self.vbo = VBO(vertices)
        self.ibo = IBO(indices)
        self.vao = VAO(self.vbo, floats_per_vertex)

        self.shader = shader
        # Remove them from properties to keep them out of draw loops
        self.properties.pop('vertices')
        self.properties.pop('indices')

    def Draw(self):
        position = self.properties['position']
        rotation_z = self.properties['rotation_z']
        scale = self.properties['scale']

        # Model matrix
        translation_matrix = np.array([
            [1,0,0, position[0]],
            [0,1,0, position[1]],
            [0,0,1, position[2]],
            [0,0,0,1]
        ], dtype = np.float32)

        rotation_z_matrix = np.array([
            [np.cos(rotation_z), -np.sin(rotation_z), 0, 0],
            [np.sin(rotation_z),  np.cos(rotation_z), 0, 0],
            [0,0,1,0],
            [0,0,0,1]
        ], dtype = np.float32)

        scale_matrix = np.array([
            [scale[0],0,0,0],
            [0,scale[1],0,0],
            [0,0,scale[2],0],
            [0,0,0,1]
        ], dtype = np.float32)

        model_matrix = translation_matrix @ rotation_z_matrix @ scale_matrix

        self.shader.Use()
        modelMatrixLocation = glGetUniformLocation(self.shader.ID, "modelMatrix")
        glUniformMatrix4fv(modelMatrixLocation, 1, GL_TRUE, model_matrix)

        # If the object has a texture, bind it
        texture_id = self.properties.get('texture_id', 0)
        if texture_id:
            glActiveTexture(GL_TEXTURE0)
            glBindTexture(GL_TEXTURE_2D, texture_id)

            textureLocation = glGetUniformLocation(self.shader.ID, "myTexture")
            glUniform1i(textureLocation, 0)

            useTextureLocation = glGetUniformLocation(self.shader.ID, "useTexture")
            glUniform1i(useTextureLocation, 1)
        else:
            # No texture
            useTextureLocation = glGetUniformLocation(self.shader.ID, "useTexture")
            glUniform1i(useTextureLocation, 0)

        self.vao.Use()
        self.ibo.Use()
        glDrawElements(GL_TRIANGLES, self.ibo.count, GL_UNSIGNED_INT, None)

        if texture_id:
            glBindTexture(GL_TEXTURE_2D, 0)