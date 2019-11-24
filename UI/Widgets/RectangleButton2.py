from ..Shapes import UVRectangle,UVRectangle_Debug
from ... import small_tools
from bgl import *
from ...ExternalModules.pyrr import Vector3


#n FragDrawButton
class RectangleButton2:
    def __init__(self,size, size_shape, shader, shape):

        # Color
        self.color_active = [*small_tools.GetThemeColors().active,1]
        self.color_text = [*small_tools.GetThemeColors().text,1]
        self.color_passive = [*small_tools.GetThemeColors().passive,1]
        self.color_back = [*small_tools.GetThemeColors().background]

        self.widget_pos = Vector3([0, 0, 0])
        self.parent = Vector3([0,0,0])
        self.pos_plus_parent = Vector3([self.parent.x + self.widget_pos.x, self.parent.y + self.widget_pos.y, 0])

        #n Switches
        self.isOver = False
        self.isClicked = False
        self.isState = 0

        #n Shader or Shaders
        self.program = shader
        #n Widget Elements
        self.shape = shape
        #n      initialize Elements

        self.rectangle = UVRectangle.UVRectangle(*size, size_shape,shape,self.program)
        self.widget_elements = [self.rectangle,]

        #n      setup Elements

        self.rectangle.setParent(*self.pos_plus_parent)
        self.rectangle.setPos(*self.widget_pos)
        self.rectangle.setColors(self.color_passive,self.color_active,[0.922, 0.231, 0.353,1.0])

        #n          update matricies befor draw loop
        for i in self.widget_elements:
            i.updateMatrix()
        #n Widget Data
        self.clickOnce = True

    #n4 Widget Element Draw
    def draw(self, proj, view):

        glEnable(GL_BLEND)
        glEnable(GL_LINE_SMOOTH)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        #n setColors
        if self.isOver:
            if self.isClicked:
                self.rectangle.setState(2)
            else:
                self.rectangle.setState(1)
        else:
            self.rectangle.setState(0)

        #n Draw elements
        self.rectangle.draw(proj,view)

        glDisable(GL_BLEND)


    def active(self,mX,mY,mEvent,mAction):
        mouseX  = mX
        mouseY  = mY
        mouseEvent = mEvent
        mouseAction = mAction
        dimensions = self.rectangle.getPositions()
        #n Update Widget and Elements

        if dimensions[0].x < mouseX < dimensions[1].x and dimensions[0].y < mouseY < dimensions[1].y  :
            self.isOver = True
        else:
            self.isOver = False


        if self.isOver:
            if mouseEvent == 'LEFTMOUSE' and  mouseAction == 'PRESS' :
                self.isClicked = True
            elif  mouseAction == 'RELEASE' :
                self.isClicked = False
                self.clickOnce = True


        if self.isOver and self.isClicked:
            if self.clickOnce:
                if self.shape == 0:
                    self.isState = 1
                elif self.shape == 1:
                    self.isState = 2
                self.clickOnce = False
            else:
                self.isState = 0

        elif self.isOver and not self.isClicked:
            self.isState = 0



    def cleanup(self):
        for e in self.widget_elements:
            e.clear()


    def setPos(self, x, y, z):
        self.widget_pos = Vector3([x,y,z])
        self.pos_plus_parent = Vector3([self.parent.x + self.widget_pos.x, self.parent.y + self.widget_pos.y, z])

    def setParent(self, pX, pY, pZ):
        self.parent = Vector3([pX, pY, pZ])
        self.pos_plus_parent = Vector3([self.parent.x + self.widget_pos.x, self.parent.y + self.widget_pos.y, 0])

    def updateElements(self):
        for i in self.widget_elements:
            i.setParent(*self.pos_plus_parent)
            i.updateMatrix()


    def getState(self):
        return self.isState

