object_shader = {
    "vertex_shader": '''
        #version 330 core

        layout(location = 0) in vec3 vertexPosition;
        layout(location = 1) in vec3 vertexColour;
        layout(location = 2) in vec2 vertexUV; // used only if we have 8 floats

        out vec3 fragmentColour;
        out vec2 fragUV;

        uniform mat4 modelMatrix;
        uniform mat4 camMatrix;

        void main() {
            fragmentColour = vertexColour;
            fragUV = vertexUV;
            gl_Position = camMatrix * modelMatrix * vec4(vertexPosition, 1.0);
        }
    ''',

    "fragment_shader": '''
        #version 330 core

        in vec3 fragmentColour;
        in vec2 fragUV;
        out vec4 outputColour;

        uniform sampler2D myTexture;
        uniform int useTexture;

        void main() {
            if (useTexture == 1) {
                outputColour = texture(myTexture, fragUV);
            } else {
                outputColour = vec4(fragmentColour, 1.0);
            }
        }
    '''
}