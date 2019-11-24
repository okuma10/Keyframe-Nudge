import numpy as np
from bgl import *
from ...ExternalModules.pyrr import matrix44,Vector3,Vector4


#n Line
class Line:
    def __init__(self,lenght):
        self.position     =  Vector3([0,0,0])
        self.parent = Vector3([0, 0, 0])
        self.rotation     =  Vector3([np.deg2rad(0), np.deg2rad(0), np.deg2rad(0)])
        self.scale            =  Vector3([1,1,1])
        self.line_color = Vector4([0.294, 0.396, 0.518, 1.0])
        self.line_width = 1

        h_lenght = lenght/2
        #n Data
        vertices = [
                                (0-h_lenght, 0, 0),
                                (0+h_lenght, 0, 0),
                                ]
        vertices = np.array(vertices, dtype=np.float32)
        self.noP = len(vertices)
        vBsize = vertices.nbytes
        v_Buffer = Buffer(GL_FLOAT,(self.noP, 3), vertices)

        #n VAO,VBO
        self.VAO, self.VBO = Buffer(GL_INT,1), Buffer(GL_INT,1)
        glGenVertexArrays(1,self.VAO)
        glBindVertexArray(self.VAO[0])
        #n VBO
        glGenBuffers(1,self.VBO)
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO[0])
        glBufferData(GL_ARRAY_BUFFER, vBsize, None, GL_STATIC_DRAW)
        glBufferSubData(GL_ARRAY_BUFFER, 0, vBsize, v_Buffer)
        #n Attributes
        # self.log.print(glGetError())
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 12, 0)
        glEnableVertexAttribArray(0)

        glBindVertexArray(0)

        self.m_matrix = matrix44.create_identity(dtype=np.float32)
        self.t_matrix = matrix44.create_from_translation(self.position, dtype=np.float32)
        self.r_matrix = matrix44.create_from_eulers(self.rotation, dtype=np.float32)
        self.s_matrix = matrix44.create_from_scale(self.scale, dtype=np.float32)


    def draw(self,program,proj,view):
        m_buffer = Buffer(GL_FLOAT,(4,4), self.m_matrix)
        v_buffer   = Buffer(GL_FLOAT,(4,4), view)
        p_buffer   = Buffer(GL_FLOAT,(4,4), proj)

        self.program = program
        self.program.activate()

        self.program.setMat4('model', m_buffer)
        self.program.setMat4('view', v_buffer)
        self.program.setMat4('projection', p_buffer)

        glBindVertexArray(self.VAO[0])
        glLineWidth(self.line_width)
        self.program.setVec4('Color', *self.line_color)
        glDrawArrays(GL_LINE_LOOP, 0, self.noP)

        glLineWidth(1)
        glBindVertexArray(0)
        self.program.deactivate()

    def clear(self):
        glDeleteVertexArrays(1,self.VAO)
        glDeleteBuffers(1,self.VBO)


    def setPos(self, x, y, z):
        self.position = Vector3([x, y, z])
        pos_plus_parent = Vector3([self.parent.x + self.position.x, self.parent.y + self.position.y, z])
        self.t_matrix = matrix44.create_from_translation(pos_plus_parent, dtype=np.float32)

    def setParent(self, pX, pY, pZ):
        self.parent = Vector3([pX, pY, pZ])

    def setRot(self, angX, angY, angZ):
        self.rotation = Vector3([np.deg2rad(angX),np.deg2rad(angY),np.deg2rad(angZ)])
        self.r_matrix= matrix44.create_from_eulers(self.rotation, dtype=np.float32)

    def setScale(self, scaleX, scaleY, scaleZ):
        self.scale = Vector3([scaleX, scaleY, scaleZ])
        self.s_matrix = matrix44.create_from_scale(self.scale, dtype=np.float32)

    def setLineColor(self,r,g,b,a):
        self.line_color = Vector4([r,g,b,a])

    def setLineWidth(self,width):
        self.line_width = width

    def updateMatrix(self):
        #model = scale * translate * rotate
        self.m_matrix =  matrix44.multiply(self.s_matrix, matrix44.multiply(self.r_matrix, self.t_matrix))

