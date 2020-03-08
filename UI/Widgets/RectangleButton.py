from ..Shapes import Text,Rectangle
from ... import  small_tools
from bgl import *
from ...ExternalModules.pyrr import Vector3


#n Rectangle Button
class RectangleButton:
    def __init__(self,dimensions,shader):

        self.buttonText = 'Push|Pull'
        self.dimensions = dimensions
        self.h_dimensions = [dimensions[0]/2,dimensions[1]/2]
        # Color
        self.color_hover = [0.918, 0.565, 0.522, 1]
        self.color_active = [0.914, 0.882, 0.8, 1]
        self.color_passive = [0.431, 0.341, 0.451, 1]
        self.color_back = [0.2, 0.2, 0.2]

        #n position and parent
        self.parent = Vector3([0,0,0])
        self.widget_pos = Vector3([0, 0, 0])
        self.pos_plus_parent = Vector3([self.parent.x + self.widget_pos.x, self.parent.y + self.widget_pos.y, 0])


        #n Switches
        self.isOver = False
        self.isClicked = False

        #n Shader or Shaders
        self.program = shader
        #n Widget Elements
        #n      initialize Elements
        self.text_size = int(dimensions[1]*.6)

        self.rectangle       = Rectangle.Rectangle( dimensions[0],    dimensions[1],self.program)
        self.rectangle2      = Rectangle.Rectangle( dimensions[0]*.05, dimensions[1],self.program)
        self.text            = Text.Text( 'Exo', 'Regular', self.text_size )
        self.text2           = Text.Text( 'Exo', 'Bold',    self.text_size    )
        self.widget_elements = [self.rectangle,self.rectangle2]
        self.text_elements   = [self.text, self.text2,]
        #n      setup Elements

        self.rectangle.setParent(*self.pos_plus_parent)
        self.rectangle.setPos(0,0,0)
        self.rectangle.setFillColor(*self.color_back,.2)
        self.rectangle.setLineColor(*self.color_passive)
        self.rectangle.setLineWidth(2)
        self.rectangle.getPositions()

        self.rectangle2.setParent(*self.pos_plus_parent)
        self.rectangle2.setPos(dimensions[0]/2, 0, -1)
        self.rectangle2.setFillColor(*self.color_hover)
        self.rectangle2.setLineColor(*self.color_hover[:-1],0)
        self.rectangle2.updateMatrix()


        self.text.setParent(*self.pos_plus_parent)
        self.text.setPos(0,0,0)
        self.text.setColor(*self.color_passive)

        self.text2.setParent(*self.pos_plus_parent)
        self.text2.setPos(0,0,0)
        self.text2.setColor(*self.color_passive)

        #n          update matricies befor draw loop
        for i in self.widget_elements:
            i.updateMatrix()

        for i in self.text_elements:
            i.updatePos()
        #n Panel Data
        self.state = 0
        self.debugs = [0,0,0,0,0,0,0,0,0]
        #n Widget Data
        self.clickOnce = True

    #n4 Widget Element Draw
    def draw(self,proj,view):
        active_area = self.rectangle.getPositions()
        glEnable(GL_BLEND)
        glEnable(GL_LINE_SMOOTH)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        #n Draw elements
        if not self.isOver:
            self.rectangle.draw(proj,view)
            self.text.setColor(*self.color_passive)
            self.text.setPos(-self.h_dimensions[0] + 2.7, -self.h_dimensions[1]/2, 0)
            self.text.draw(self.buttonText)
            self.rectangle.setLineColor(*self.color_passive[:-1], .3)

        elif self.isOver:
            if self.isClicked:
                self.rectangle.setFillColor(*self.color_hover)
                self.rectangle.setLineColor(*self.color_hover)
                self.rectangle.draw(proj, view)
                self.text2.setColor(*self.color_active)
                self.text2.setPos(-self.h_dimensions[0]+2.2, -self.h_dimensions[1]/2, 0)
                self.text2.draw(self.buttonText)

            elif not self.isClicked:
                self.rectangle.setFillColor(*self.color_back, .2)
                self.rectangle.setLineColor(*self.color_passive[:-1],.3)
                self.rectangle.draw(proj, view)
                self.text2.setColor(*self.color_hover)
                self.text2.setPos(-self.h_dimensions[0]+2.2, -self.h_dimensions[1]/2, 0)
                self.text2.draw(self.buttonText)
                self.rectangle2.draw(proj,view)

        glDisable(GL_BLEND)



    def active(self,mX,mY,mEvent,mAction):
        mouseX  = mX
        mouseY  = mY
        mouseEvent = mEvent
        mouseAction = mAction
        dimensions = self.rectangle.getPositions()

        if dimensions[0].x < mouseX < dimensions[1].x and dimensions[0].y < mouseY < dimensions[1].y  :
            self.isOver = True
        else:
            self.isOver = False

        if self.isOver:
            if mouseEvent == 'LEFTMOUSE' and  mouseAction == 'PRESS' :
                self.isClicked = True
            elif  mouseAction =='RELEASE' :
                self.isClicked = False
                self.clickOnce = True

        #
        # if self.isOver and not self.isClicked:
        #         self.state = 1
        #         self.clickOnce = True
        # elif self.isOver and self.isClicked:
        #     if self.clickOnce:
        #         self.state = 2
        #         self.clickOnce = False
        # elif not self.isOver and not self.isClicked:
        #     self.state = 0
        #     self.clickOnce = True
        # elif not self.isOver and self.isClicked:
        #     if mouseAction == 'RELEASE':
        #         self.isClicked = False
        #         self.clickOnce = True
        #     self.state = 2
        #     self.clickOnce = False

        if self.isOver:
            if self.clickOnce:
                if self.isClicked:
                    self.state = 2
                    self.clickOnce = False
                else:
                    self.state = 1

            else:
                self.state = 1
                if mouseAction == 'RELEASE':
                    self.isClicked = False
                    self.clickOnce = True

        else:self.state = 0

        self.debugs =[self.isOver, self.state, self.isClicked, self.clickOnce]

    def cleanup(self):
        for e in self.widget_elements:
            e.clear()

    def setText(self,string):
        self.buttonText = string

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
        for i in self.text_elements:
            i.setParent(*self.pos_plus_parent)
            i.updatePos()

    def setColors(self, passive, hover, active, focus):
        self.color_passive = passive
        self.color_hover = hover
        self.color_active = active
        self.color_focus = focus
        self.text.setColor(*self.color_passive)
        self.text2.setColor(*self.color_passive)
        self.rectangle.setFillColor(*self.color_back,.2)
        self.rectangle.setLineColor(*self.color_passive[:-1],.3)
        self.rectangle2.setFillColor(*self.color_hover)
        self.rectangle2.setLineColor(*self.color_hover[:-1],0)

    def debug(self):
        return self.debugs

    def getState(self):
        return self.state