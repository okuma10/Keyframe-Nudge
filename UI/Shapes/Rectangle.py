import numpy as np
from bgl import *
from ...ExternalModules.pyrr import matrix44,Vector3,Vector4



#n Normal Rectangle
class Rectangle:
    def __init__(self,width,height,program):
        self.program = program
        self.line_width  =  1
        self.fill_color     =  Vector4([0.467, 0.549, 0.639, 1.0],dtype=np.float32)
        self.line_color   =  Vector4([0.294, 0.396, 0.518, 1.0],dtype=np.float32)
        self.parent          = Vector3([0,0,0])
        self.position        =  Vector3([0, 0, 0])
        self.pos_plus_parent = Vector3([self.parent.x + self.position.x, self.parent.y + self.position.y, 0])
        self.rotation        =  Vector3([np.deg2rad(0),np.deg2rad(0),np.deg2rad(0)])
        self.scale              =  Vector3([1, 1, 1])

        self.h_width  = width/2
        self.h_height = height/2

        #n Data
        self.vertices = [
                            (0-self.h_width, 0-self.h_height, 0),
                            (0+self.h_width, 0-self.h_height, 0),
                            (0+self.h_width, 0+self.h_height, 0),
                            (0-self.h_width, 0+self.h_height, 0),
                            ]
        self.vertices=np.array(self.vertices, dtype=np.float32)
        vBsize = self.vertices.nbytes
        self.noP = len(self.vertices)
        v_Buffer = Buffer(GL_FLOAT, (self.noP, 3), self.vertices)

        #n VAO VBO
        self.VAO,self.VBO = Buffer(GL_INT, 1),Buffer(GL_INT, 1)
        glGenVertexArrays(1, self.VAO)
        glGenBuffers(1, self.VBO)
        #n  setup
        glBindVertexArray(self.VAO[0])
        glBindBuffer(GL_ARRAY_BUFFER,self.VBO[0])
        glBufferData(GL_ARRAY_BUFFER, vBsize, None, GL_STATIC_DRAW)
        glBufferSubData(GL_ARRAY_BUFFER, 0, vBsize, v_Buffer)
        #n      Attributes
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 12, 0)
        glEnableVertexAttribArray(0)

        glBindVertexArray(0)

        self.m_matrix = matrix44.create_identity(dtype=np.float32)
        self.t_matrix   = matrix44.create_from_translation(self.pos_plus_parent, dtype=np.float32)
        self.r_matrix   = matrix44.create_from_eulers(self.rotation, dtype=np.float32)
        self.s_matrix   = matrix44.create_from_scale(self.scale, dtype=np.float32)
        self.view           = matrix44.create_identity(dtype=np.float32)
        self.proj             = matrix44.create_identity(dtype=np.float32)

    def draw(self,proj,view):
        glEnable(GL_BLEND)
        glEnable(GL_LINE_SMOOTH)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        self.view = view
        self.proj = proj
        m_buffer = Buffer(GL_FLOAT,(4,4),self.m_matrix)
        p_buffer = Buffer(GL_FLOAT,(4,4),self.proj)
        v_buffer = Buffer(GL_FLOAT,(4,4),self.view)

        self.program.activate()

        self.program.setMat4('model', m_buffer)
        self.program.setMat4('view', v_buffer)
        self.program.setMat4('projection', p_buffer)

        glBindVertexArray(self.VAO[0])

        glLineWidth(self.line_width)
        self.program.setVec4('Color', *self.line_color)
        glDrawArrays(GL_LINE_LOOP,0,self.noP)
        self.program.setVec4('Color', *self.fill_color)
        glDrawArrays(GL_TRIANGLE_FAN,0,self.noP)

        glLineWidth(1)
        glBindVertexArray(0)
        self.program.deactivate()


    def clear(self):
        glDeleteVertexArrays(1,self.VAO)
        glDeleteBuffers(1,self.VBO)


    def setPos(self, x, y, z):
        self.position = Vector3([x,y,z])
        self.pos_plus_parent = Vector3([self.parent.x + self.position.x, self.parent.y + self.position.y, z])
        self.t_matrix = matrix44.create_from_translation(self.pos_plus_parent, dtype = np.float32)


    def setParent(self,pX,pY,pZ):
        self.parent = Vector3([pX,pY,pZ])
        self.pos_plus_parent = Vector3([self.parent.x + self.position.x, self.parent.y + self.position.y, 0])
        self.t_matrix = matrix44.create_from_translation(self.pos_plus_parent, dtype=np.float32)


    def setRot(self, angX, angY, angZ):
        self.rotation = Vector3([np.deg2rad(angX),np.deg2rad(angY),np.deg2rad(angZ)])
        self.r_matrix= matrix44.create_from_eulers(self.rotation, dtype=np.float32)

    def setScale(self, scaleX, scaleY, scaleZ):
        self.scale = Vector3([scaleX, scaleY, scaleZ])
        self.s_matrix = matrix44.create_from_scale(self.scale, dtype=np.float32)

    def setFillColor(self,r,g,b,a):
        self.fill_color = Vector4([r,g,b,a],dtype=np.float32)

    def setLineColor(self,r,g,b,a):
        self.line_color = Vector4([r,g,b,a],dtype=np.float32)

    def setLineWidth(self,width):
        self.line_width = width

    def updateMatrix(self):
        #model = scale * translate * rotate
        self.m_matrix = matrix44.multiply(self.s_matrix, matrix44.multiply(self.r_matrix, self.t_matrix))

    def getPositions(self):
        v_1 = self.vertices[0]
        v_2 = self.vertices[2]

        mV_1 =  Vector3 (matrix44.apply_to_vector(self.m_matrix, v_1))
        mV_2 =  Vector3(matrix44.apply_to_vector(self.m_matrix, v_2))

        return (mV_1, mV_2)

    def getParentPos(self):
        return self.pos_plus_parent

    def changeDimensions(self,width,height):
        self.vertices = [
            (0 - self.h_width, 0 - self.h_height, 0),
            (0 + self.h_width, 0 - self.h_height, 0),
            (0 + self.h_width, 0 + self.h_height, 0),
            (0 - self.h_width, 0 + self.h_height, 0),
        ]
        self.vertices = np.array(self.vertices, dtype=np.float32)
        vBsize = self.vertices.nbytes

        v_Buffer = Buffer(GL_FLOAT, (self.noP, 3), self.vertices)

        glBindVertexArray(self.VAO[0])

        glBindBuffer(GL_ARRAY_BUFFER, self.VBO[0])
        glBufferData(GL_ARRAY_BUFFER, vBsize, None, GL_STATIC_DRAW)
        glBufferSubData(GL_ARRAY_BUFFER, 0, vBsize, v_Buffer)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 12, 0)
        glEnableVertexAttribArray(0)

        glBindVertexArray(0)



