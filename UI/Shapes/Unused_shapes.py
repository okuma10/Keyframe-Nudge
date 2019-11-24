import numpy as np
from ... import small_tools
from bgl import *
from pathlib import Path
from ...ExternalModules.pyrr import matrix44,Vector3,Vector4
# from OpenGL.GL import *

parent = str(Path(__file__).parent)
log_file  = parent+r'\Logs\Shapes'



#n Rounded Corner Rectangle Object
class RRectangle:
    def __init__(self, posx, posy, width, height, radius1, radius2, radius3, radius4, resolution):
        # self.log = Logger.Log(log_file)
        # self.log.removeHandler()
        # self.log.addHandler(parent + r'\Logs\test_Triangle')
        # self.log.clearFile()
        # self.log.clearFile()
        #n non OpenGL stuff
        self.h_width  = width /2    # half width
        self.h_height = height/2    # half height

        r1    = radius1
        r2   = radius2
        r3   = radius3
        r4   = radius4
        res = resolution

        self.position   = Vector3([0,0,0])
        self.rotation   = Vector3([0,0,0])
        self.scale        = Vector3([1,1,1])

        #n Data
        #                X                    Y                 Z
        center      = (posx,posy,0)
        corner_1  = (posx - self.h_width, posy - self.h_height, 0.0)
        corner_2 = (posx + self.h_width, posy - self.h_height, 0.0)
        corner_3 = (posx + self.h_width, posy + self.h_height, 0.0)
        corner_4 = (posx - self.h_width, posy + self.h_height, 0.0)
        #n  vert data

        vertices  = [
                               *small_tools.ParametricCircle(*small_tools.squareAlongLine(corner_1, r1,   45,center).get_points(),resolution,3).getPoints(),
                               *small_tools.ParametricCircle(*small_tools.squareAlongLine(corner_2, r2,  135,center).get_points(),resolution,2).getPoints(),
                               *small_tools.ParametricCircle(*small_tools.squareAlongLine(corner_3, r3,  225,center).get_points(),resolution,3).getPoints(),
                               *small_tools.ParametricCircle(*small_tools.squareAlongLine(corner_4, r4,  315,center).get_points(),resolution,2).getPoints(),
                               ]
        vertices  = np.array(vertices,dtype=np.float32)
        vbSize    = vertices.nbytes
        self.noP  = len(vertices)
        vert_buff = Buffer(GL_FLOAT,(len(vertices),3),vertices)
        # self.log.print(f'{vert_buff.to_list()}')

        #   color data
        self.color_fill = Vector4([0.996, 0.827, 0.188, 0.8],dtype = np.float32)
        self.color_line = Vector4([0.294, 0.482, 0.925, 1.0],dtype = np.float32)

        #n VAO,VBO,Attributes
        #   VAO,VBO
        self.VAO,self.VBO = Buffer(GL_INT,1), Buffer(GL_INT,1)
        #n VAO
        glGenVertexArrays(1, self.VAO)
        glBindVertexArray(self.VAO[0])
        #n VBO
        glGenBuffers   (1, self.VBO)
        glBindBuffer   (GL_ARRAY_BUFFER, self.VBO[0])
        glBufferData   (GL_ARRAY_BUFFER, vbSize, None, GL_STATIC_DRAW)
        glBufferSubData(GL_ARRAY_BUFFER, 0, vbSize, vert_buff)
        #n  Attributes
        #       pos
        glVertexAttribPointer    (0, 3, GL_FLOAT, GL_FALSE, 12, 0)
        glEnableVertexAttribArray(0)
        # self.log.print(f'VAO : {self.VAO[0]} | VBO: {self.VBO[0]}')

        #n clean
        glBindVertexArray(0)

        #n Matricies
        self.t_matrix = matrix44.create_from_translation(self.position, dtype=np.float32)
        self.r_matrix = matrix44.create_from_eulers([np.deg2rad(self.rotation.x), np.deg2rad(self.rotation.y), np.deg2rad(self.rotation.z)], dtype = np.float32)
        self.s_matrix = matrix44.create_from_scale(self.scale, dtype = np.float32)
        self.model_matrix = None

    def draw(self,program,proj,view):
        # self.log.setLevel(2)

        m_buffer = Buffer(GL_FLOAT, (4,4), self.model_matrix)
        p_buffer = Buffer(GL_FLOAT, (4,4), proj)
        v_buffer = Buffer(GL_FLOAT, (4,4), view)

        program.activate()
        glBindVertexArray(self.VAO[0])
       #n Set Matricies
        program.setMat4('model',       m_buffer)
        program.setMat4('view',          v_buffer)
        program.setMat4('projection',p_buffer)


        glLineWidth(5)
        program.setVec4('Color', *self.color_line)
        glDrawArrays(GL_LINE_LOOP, 0, self.noP)
        program.setVec4('Color',*self.color_fill)
        glDrawArrays(GL_TRIANGLE_FAN, 0, self.noP)

        glBindVertexArray(0)
        program.deactivate()


    def clear(self):
        glDeleteVertexArrays(1,self.VAO)
        glDeleteBuffers(1, self.VAO)


    def setPos(self, x, y, z):
        self.position = Vector3([x, y, z])
        self.t_matrix = matrix44.create_from_translation(self.position, dtype = np.float32)

    def setRot(self, angX, angY, angZ):
        self.rotation = Vector3([np.deg2rad(angX),np.deg2rad(angY),np.deg2rad(angZ)])
        self.r_matrix= matrix44.create_from_eulers(self.rotation, dtype=np.float32)

    def setScale(self, scaleX, scaleY, scaleZ):
        self.scale = Vector3([scaleX, scaleY, scaleZ])
        self.s_matrix = matrix44.create_from_scale(self.scale, dtype=np.float32)

    def setFillColor(self,r,g,b,a):
        self.color_fill = Vector4([r,g,b,a],dtype=np.float32)

    def setLineColor(self,r,g,b,a):
        self.color_line = Vector4([r,g,b,a],dtype=np.float32)

    def updateMatrix(self):
        #model = scale * translate * rotate
        self.model_matrix = matrix44.multiply(self.s_matrix, matrix44.multiply(self.r_matrix, self.t_matrix))


#n Rounded Corner with straight lines in beginning and end
class RoundedCorner:
    def __init__(self,r,line_lenght,shader):
        # self.log = Logger.Log(log_file)
        # self.log.removeHandler()
        # self.log.addHandler(log_file)
        # self.log.clearFile()
        # self.log.setLevel(1)
        self.program = shader

        self.parent = Vector3([0, 0, 0])
        self.position = Vector3([0, 0, 0])
        self.pos_plus_parent = Vector3([self.parent.x + self.position.x, self.parent.y + self.position.y, 0])
        self.rotation = Vector3([np.deg2rad(0),np.deg2rad(0),np.deg2rad(0)])
        self.scale = Vector3([1, 1, 1])
        self.line_width = 1
        self.line_color = Vector4([ 0.016, 0.714, 0.345,1.0 ])

        #n Data
        corner = small_tools.ParametricCircle(self.position,r,9,1).getPoints()
        first_corner_vert = Vector3(corner[0])
        last_corner_vert = Vector3(corner[-1])
        start_line=[
                                (first_corner_vert.x, first_corner_vert.y-line_lenght, 0),
                                (first_corner_vert.x, first_corner_vert.y, 0),
                             ]
        end_line = [
                                 (last_corner_vert.x, last_corner_vert.y, 0),
                                 (last_corner_vert.x-line_lenght, last_corner_vert.y, 0),
                             ]

        # self.log.print(f'first vertex of Corner  {first_corner_vert}')
        # self.log.print(f'last vertex of Corner  {last_corner_vert}')
        vertices = [
                            *start_line,
                            *corner,
                            *end_line,
                            ]
        vertices = np.array(vertices,dtype=np.float32)
        # self.log.print(f'corner Data :\n {vertices}')
        vBsize = vertices.nbytes
        self.noP=len(vertices)
        v_buffer = Buffer(GL_FLOAT,(self.noP,3), vertices)

        #n VAO,VBO,Attributes
        self.VAO, self.VBO = Buffer(GL_INT, 1), Buffer(GL_INT, 1)
        glGenVertexArrays(1, self.VAO)
        glGenBuffers(1, self.VBO)
        #n  VAO
        glBindVertexArray(self.VAO[0])
        #n  VBO
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO[0])
        glBufferData(GL_ARRAY_BUFFER, vBsize, None, GL_STATIC_DRAW)
        glBufferSubData(GL_ARRAY_BUFFER, 0, vBsize, v_buffer)
        #n      Attributes
        glVertexAttribPointer(0,3, GL_FLOAT, GL_FALSE, 12, 0)
        glEnableVertexAttribArray(0)

        glBindVertexArray(0)

        #n Matricies
        self.m_matrix = matrix44.create_identity(dtype=np.float32)
        self.t_matrix = matrix44.create_from_translation(self.pos_plus_parent, dtype=np.float32)
        self.r_matrix = matrix44.create_from_eulers(self.rotation, dtype=np.float32)
        self.s_matrix = matrix44.create_from_scale(self.scale, dtype=np.float32)
        # self.log.setLevel(1)
        # self.log.removeHandler()

    def draw(self,proj,view):
        #n Matrix Buffers
        m_buffer = Buffer(GL_FLOAT,(4,4), self.m_matrix)
        v_buffer = Buffer(GL_FLOAT,(4,4), view)
        p_buffer = Buffer(GL_FLOAT,(4,4), proj)

        self.program.activate()
        #n Set Matricies
        self.program.setMat4('model', m_buffer)
        self.program.setMat4('view', v_buffer)
        self.program.setMat4('projection', p_buffer)

        #n Draw
        glBindVertexArray(self.VAO[0])
        glLineWidth(self.line_width)
        self.program.setVec4('Color',*self.line_color)
        glDrawArrays(GL_LINE_STRIP,0,self.noP)

        glBindVertexArray(0)

        glLineWidth(1)
        self.program.deactivate()

    def clear(self):
        glDeleteVertexArrays(1,self.VAO)
        glDeleteBuffers(1,self.VBO)

    def setParent(self,pX,pY,pZ):
        self.parent = Vector3([pX,pY,pZ])
        self.pos_plus_parent = Vector3([self.parent.x + self.position.x, self.parent.y + self.position.y, 0])
        self.t_matrix = matrix44.create_from_translation(self.pos_plus_parent, dtype=np.float32)

    def setPos(self, x, y, z):
        self.position = Vector3([x, y, z])
        self.pos_plus_parent = Vector3([self.parent.x + self.position.x, self.parent.y + self.position.y, z])
        self.t_matrix = matrix44.create_from_translation(self.pos_plus_parent, dtype=np.float32)

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


#n Plus Object
class Plus:
    def __init__(self, size, thickness):
        self.line_width = 1
        self.line_color  = Vector4([ 0.016, 0.714, 0.345,1.0 ])
        self.fill_color    = Vector4([0.467, 0.549, 0.639, 1.0])
        self.position       = Vector3([0,0,0])
        self.rotation       = Vector3([np.deg2rad(0), np.deg2rad(0), np.deg2rad(0)])
        self.scale              = Vector3([1, 1, 1])
        h_size =  size/2
        h_thick = thickness/2
        outter_square = [
                                            Vector3([0-h_size, 0-h_size, 0]),
                                            Vector3([0+h_size, 0-h_size, 0]),
                                            Vector3([0+h_size, 0+h_size, 0]),
                                            Vector3([0-h_size, 0+h_size, 0]),
                                            ]
        inner_square =   [
                                            Vector3([0-h_thick, 0-h_thick, 0]),
                                            Vector3([0+h_thick, 0-h_thick, 0]),
                                            Vector3([0+h_thick, 0+h_thick, 0]),
                                            Vector3([0-h_thick, 0+h_thick, 0]),
                                            ]
        vertices =  [
                                (inner_square[0].x, inner_square[0].y,    0.0),
                                (inner_square[0].x, outter_square[0].y,   0.0),
                                (inner_square[1].x, outter_square[0].y,   0.0),
                                (inner_square[1].x, inner_square[1].y,      0.0),
                                (outter_square[2].x, inner_square[1].y,   0.0),
                                (outter_square[2].x, inner_square[2].y,  0.0),
                                (inner_square[2].x, inner_square[2].y,    0.0),
                                (inner_square[2].x, outter_square[2].y,  0.0),
                                (inner_square[3].x, outter_square[2].y, 0.0),
                                (inner_square[3].x, inner_square[3].y,   0.0),
                                (outter_square[0].x, inner_square[3].y, 0.0),
                                (outter_square[0].x, inner_square[0].y, 0.0),
                                ]
        vertices = np.array(vertices,dtype=np.float32)
        vBsize = vertices.nbytes
        self.noP = len(vertices)
        v_buffer = Buffer(GL_FLOAT, (self.noP, 3), vertices)

        #n VAO,VBO,Attributes
        self.VAO,self.VBO = Buffer(GL_INT, 1),Buffer(GL_INT, 1)
        glGenVertexArrays(1, self.VAO)
        glGenBuffers(1, self.VBO)
        #n  VAO
        glBindVertexArray(self.VAO[0])
        #n  VBO
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO[0])
        glBufferData(GL_ARRAY_BUFFER, vBsize, None, GL_STATIC_DRAW)
        glBufferSubData(GL_ARRAY_BUFFER, 0, vBsize, v_buffer)
        #n      Attributes
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 12, 0)
        glEnableVertexAttribArray(0)

        glBindVertexArray(0)

        #n Matricies
        self.m_matrix = matrix44.create_identity(dtype=np.float32)
        self.t_matrix = matrix44.create_from_translation(self.position, dtype=np.float32)
        self.r_matrix = matrix44.create_from_eulers(self.rotation, dtype=np.float32)
        self.s_matrix = matrix44.create_from_scale(self.scale, dtype=np.float32)

    def draw(self,program,proj,view):
        #n Matrix Buffers
        m_buffer = Buffer(GL_FLOAT,(4,4), self.m_matrix)
        v_buffer = Buffer(GL_FLOAT,(4,4), view)
        p_buffer = Buffer(GL_FLOAT,(4,4), proj)

        program.activate()
        #n Set Matricies
        program.setMat4('model', m_buffer)
        program.setMat4('view', v_buffer)
        program.setMat4('projection', p_buffer)

        #n Draw
        glBindVertexArray(self.VAO[0])
        glLineWidth(self.line_width)
        program.setVec4('Color',*self.line_color)
        glDrawArrays(GL_LINE_LOOP,0,self.noP)
        program.setVec4('Color',*self.fill_color)
        glDrawArrays(GL_TRIANGLE_FAN,0,self.noP)

        glBindVertexArray(0)

        glLineWidth(1)
        program.deactivate()

    def clear(self):
        glDeleteVertexArrays(1,self.VAO)
        glDeleteBuffers(1,self.VBO)

    def setPos(self, x, y, z):
        self.position = Vector3([x, y, z])
        self.t_matrix = matrix44.create_from_translation(self.position, dtype = np.float32)

    def setRot(self, angX, angY, angZ):
        self.rotation = Vector3([np.deg2rad(angX),np.deg2rad(angY),np.deg2rad(angZ)])
        self.r_matrix= matrix44.create_from_eulers(self.rotation, dtype=np.float32)

    def setScale(self, scaleX, scaleY, scaleZ):
        self.scale = Vector3([scaleX, scaleY, scaleZ])
        self.s_matrix = matrix44.create_from_scale(self.scale, dtype=np.float32)

    def setLineColor(self,r,g,b,a):
        self.line_color = Vector4([r,g,b,a])

    def setFillColor(self, r, g, b, a):
        self.fill_color = Vector4([r, g, b, a])

    def setLineWidth(self,width):
        self.line_width = width

    def updateMatrix(self):
        #model = scale * translate * rotate
        self.m_matrix =  matrix44.multiply(self.s_matrix, matrix44.multiply(self.r_matrix, self.t_matrix))

