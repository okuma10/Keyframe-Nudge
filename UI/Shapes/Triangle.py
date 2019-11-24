import numpy as np
from bgl import *
from ...ExternalModules.pyrr import matrix44,Vector3,Vector4

class Triangle:
    def __init__(self,size):

        #n Data
        #   Defaults
        self.parent = Vector3([0,0,0])
        self.position = Vector3([0,0,0])
        self.pos_plus_parent = Vector3([self.parent.x + self.position.x, self.parent.y + self.position.y, 0])
        self.rotation = Vector3([np.deg2rad(0), np.deg2rad(0), np.deg2rad(0)])
        self.scale = Vector3([1,1,1])
        self.line_color = Vector4([0.294, 0.396, 0.518, 1])
        self.fill_color = Vector4([0.467, 0.549, 0.639, 1])

        h_size = size/2
        #n VertexData
        self.verticies = [
                                (0 -h_size , 0 -h_size, 0),
                                (0 +h_size, 0 - h_size, 0),
                                (0                 , 0+h_size,  0),
                                ]

        self.verticies = np.array(self.verticies, dtype=np.float32)
        self.noP = len(self.verticies)
        vBsize = self.verticies.nbytes
        ver_Buf = Buffer(GL_FLOAT, (self.noP,3), self.verticies)

       #n VAO,VBO
        self.VAO,self.VBO = Buffer(GL_INT,1),Buffer(GL_INT,1)
        glGenVertexArrays(1,self.VAO)
        glGenBuffers(1,self.VBO)
        # self.log.print(f'VAO : {self.VAO[0]}  |  {self.VBO[0]} : VBO')
        #n VAO
        glBindVertexArray(self.VAO[0])
        #n VBO
        glBindBuffer(GL_ARRAY_BUFFER,self.VBO[0])
        glBufferData(GL_ARRAY_BUFFER, vBsize, None, GL_STATIC_DRAW)
        glBufferSubData(GL_ARRAY_BUFFER, 0, vBsize, ver_Buf)
        #n      Attributes
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 12, 0)
        glEnableVertexAttribArray(0)

        glBindVertexArray(0)

        #n Matricies
        self.m_matrix = matrix44.create_identity(dtype= np.float32)
        self.t_matrix = matrix44.create_from_translation(self.pos_plus_parent, dtype=np.float32)
        self.r_matrix = matrix44.create_from_eulers(self.rotation, dtype=np.float32)
        self.s_matrix = matrix44.create_from_scale(self.scale, dtype=np.float32)


    def draw(self, program, proj, view):

        model_buffer = Buffer(GL_FLOAT, (4,4), self.m_matrix)
        proj_buffer = Buffer(GL_FLOAT, (4,4),proj)
        view_buffer = Buffer(GL_FLOAT, (4,4), view)

        self.program = program
        self.program.activate()

        self.program.setMat4('model',model_buffer )
        self.program.setMat4('view',   view_buffer)
        self.program.setMat4('projection', proj_buffer)

        glBindVertexArray(self.VAO[0])

        glLineWidth(5)
        self.program.setVec4('Color', *self.line_color)
        glDrawArrays(GL_LINE_LOOP, 0, self.noP)

        self.program.setVec4('Color', *self.fill_color)
        glDrawArrays(GL_TRIANGLES, 0, self.noP)

        glBindVertexArray(0)
        self.program.deactivate()


    def clear(self):
        glDeleteVertexArrays(1,self.VAO)
        glDeleteBuffers(1,self.VBO)


    def setPos(self, x, y, z):
        self.position = Vector3([x, y, z])
        self.pos_plus_parent = Vector3([self.parent.x + self.position.x, self.parent.y + self.position.y, z])
        self.t_matrix = matrix44.create_from_translation(self.pos_plus_parent, dtype=np.float32)


    def setParent(self, pX, pY, pZ):
        self.parent = Vector3([pX, pY, pZ])
        self.pos_plus_parent = Vector3([self.parent.x + self.position.x, self.parent.y + self.position.y, 0])
        self.t_matrix = matrix44.create_from_translation(self.pos_plus_parent, dtype=np.float32)

    def setRot(self, angX, angY, angZ):
        self.rotation = Vector3([np.deg2rad(angX),np.deg2rad(angY),np.deg2rad(angZ)])
        self.r_matrix= matrix44.create_from_eulers(self.rotation, dtype=np.float32)

    def setScale(self, scaleX, scaleY, scaleZ):
        self.scale = Vector3([scaleX, scaleY, scaleZ])
        self.s_matrix = matrix44.create_from_scale(self.scale, dtype=np.float32)

    def setFillColor(self,r,g,b,a):
        self.fill_color = Vector4([r,g,b,a])

    def setLineColor(self,r,g,b,a):
        self.line_color = Vector4([r,g,b,a])

    def updateMatrix(self):
        self.m_matrix = matrix44.multiply(self.s_matrix, matrix44.multiply(self.r_matrix, self.t_matrix))

    def getDimensions(self):
        self.m_matrix = matrix44.multiply(self.s_matrix, matrix44.multiply(self.r_matrix, self.t_matrix))
        vert1 = Vector3(self.verticies[0])
        vert2 = Vector3(self.verticies[1])
        vert3 = Vector3(self.verticies[2])

        new_v1 = Vector3(matrix44.apply_to_vector(self.m_matrix, vert1))
        new_v2 = Vector3(matrix44.apply_to_vector(self.m_matrix, vert2))
        new_v3 = Vector3(matrix44.apply_to_vector(self.m_matrix, vert3))


        width  = new_v2.y  - new_v1.y
        height = new_v3.y  - new_v2.y

        dimensions = (width, height)

        return dimensions

    def getPosition(self):
        return self.pos_plus_parent
