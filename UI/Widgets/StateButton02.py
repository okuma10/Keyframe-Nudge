from ..Shapes import Text,Rectangle, UVRectangle_Debug
from ... import small_tools
from bgl import *
from ...ExternalModules.pyrr import Vector3


#n StateButton for title
class StateButton02:
    def __init__(self, shader):
        #n Default States
        self.states = ["KEYFRAME","GREASE"]
        self.currentState = 0
        #n Color
        self.color_active   = [*small_tools.GetThemeColors().active, 1]
        self.color_text     = [*small_tools.GetThemeColors().text]
        self.color_passive  = [*small_tools.GetThemeColors().passive]
        self.color_back     = [*small_tools.GetThemeColors().background]

        #n Shader or shaders
        self.program = shader

        #n widget Pos/Parent
        self.widget_pos         = Vector3([0, 0, 0])
        self.parent             = Vector3([0, 0, 0])
        self.pos_plus_parent    = Vector3([self.parent.x + self.widget_pos.x, self.parent.y + self.widget_pos.y, 0])

        #n Widgets and Elements
        #n  -initialize Elements
        self.text_size              = 20
        self.text                   = Text.Text("Exo","Light",self.text_size)
        if self.currentState == 0:
            self.text_dimensions        = self.text.getDimensions(self.states[0])
        elif self.currentState == 1:
            self.text_dimensions = self.text.getDimensions(self.states[1])

        self.rectangle  = Rectangle.Rectangle(self.text_dimensions[0]+5, self.text_dimensions[1]+5, self.program)

        #n  -setup Elements
        self.text_pos = [-self.text_dimensions[0] / 2, -self.text_dimensions[1]/2, 0]
        self.text.setParent(*self.pos_plus_parent)
        self.text.setPos(*self.text_pos)
        self.text.setScale(self.text_size)

        self.rectangle_pos = Vector3([0,0,0])
        self.rectangle.setParent(*self.pos_plus_parent)
        self.rectangle.setPos(*self.rectangle_pos)
        self.rectangle.setFillColor(0,0,0,0)
        self.rectangle.setLineColor(0.04,0.73,0.22,1)


        #n  -widget lists
        self.widget_elements    = [self.rectangle]
        self.text_elements      = [self.text]

        #n Update Element Matricies before draw loop
        for i in self.widget_elements:
            if len(self.widget_elements)>0:
                i.setParent(*self.pos_plus_parent)
                i.updateMatrix()

        for i in self.text_elements:
            if len(self.text_elements)>0:
                i.setParent(*self.pos_plus_parent)
                i.updatePos()

        #n Widget Dada
        self.isOver = False
        self.isClicked = False
        self.OneClick = True
        self.currentState = 0
        self.buttonEvent = 0
        #n  -Debug
        self.debug = False
        self.debug_data = []

    #n4 Draw Loop
    def draw(self,proj,view):
        glEnable(GL_BLEND)
        glEnable(GL_LINE_SMOOTH)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)


        #n Draw
        self.text.setScale(self.text_size)
        if self.buttonEvent == 0:
            self.text.setColor(*self.color_passive,1)
        elif self.buttonEvent == 1:
            self.text.setColor(*self.color_active)
        elif self.buttonEvent == 2:
            self.text.setColor(*self.color_text,1)

        if self.currentState == 0:
            self.text.setPos(-self.text_dimensions[0] / 2, -self.text_dimensions[1] / 2, 0)
            self.text.draw(self.states[0])
        elif self.currentState == 1:
            new_text_size = self.text.getDimensions(self.states[1])
            difference = self.text_dimensions[0]-new_text_size[0]
            self.text.setPos(-self.text_dimensions[0]/2+difference, -self.text_dimensions[1]/2,0)
            self.text.draw(self.states[1])

        if self.debug:
            self.rectangle.draw(proj,view)

        glDisable(GL_BLEND)

    #n2 Active loop
    def active(self, mX, mY, mEvent, mAction):
        mouseX = mX
        mouseY = mY
        mouseEvent = mEvent
        mouseAction = mAction
        dimensions = self.rectangle.getPositions()

        #n Check if mouse is over widget
        if dimensions[0].x < mouseX < dimensions[1].x and dimensions[0].y < mouseY < dimensions[1].y  :
            self.isOver = True
        else:
            self.isOver = False
        #n Check for mosuse clicks and events
        if self.isOver:
            if self.isOver:
                if mouseEvent == 'LEFTMOUSE' and mouseAction == 'PRESS':
                    self.isClicked = True
                elif mouseAction == "RELEASE":
                    self.isClicked = False
                    self.oneClick = True
            else:
                if self.isClicked and mouseAction == "RELEASE":
                    self.isClicked = False
                    self.oneClick = True

        #n Handle states based on `isOver` is `Clicked` switches
        if self.isOver and not self.isClicked:
            self.buttonEvent = 1
        elif self.isOver and self.isClicked:
            self.buttonEvent = 2
            if self.oneClick:
                self.currentState += 1
                if self.currentState > len(self.states)-1:
                    self.currentState = 0
                else:pass
                self.oneClick = False
        elif not self.isOver and self.isClicked:
            self.buttonEvent = 2
            if mouseAction == "RELEASE":
                self.isClicked = False
        elif not self.isOver and not self.isClicked:
            self.buttonEvent = 0



    def cleanup(self):
        for e in self.widget_elements:
            e.clear()

    def setPos(self, x, y, z):
        self.widget_pos = Vector3([x, y, z])
        self.pos_plus_parent = Vector3([self.parent.x + self.widget_pos.x, self.parent.y + self.widget_pos.y, z])

    def setParent(self, pX, pY, pZ):
        self.parent = Vector3([pX, pY, pZ])
        self.pos_plus_parent = Vector3([self.parent.x + self.widget_pos.x, self.parent.y + self.widget_pos.y, 0])

    def updateElements(self):
        for i in self.widget_elements:
            if len(self.widget_elements)>0:
                i.setParent(*self.pos_plus_parent)
                i.setPos(*self.rectangle_pos)
                i.updateMatrix()
        for i in self.text_elements:
            if len(self.text_elements)>0:
                i.setParent(*self.pos_plus_parent)
                i.updatePos()

    def getState(self):
        return self.currentState

    def debugs(self):
        self.debug_data = [self.isOver,self.isClicked]

        return self.debug_data