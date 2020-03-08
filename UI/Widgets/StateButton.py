from ..Shapes import Text,Rectangle
from ... import small_tools
from bgl import *
from ...ExternalModules.pyrr import Vector3


#n StateButton Button
class StateButton:
    def __init__(self,states,shader):

        self.buttonText = 'PUSH|PULL'

        # Color
        self.color_hover = [0.918, 0.565, 0.522, 1]
        self.color_active = [0.914, 0.882, 0.8, 1]
        self.color_passive = [0.431, 0.341, 0.451, 1]
        self.color_back = [0.2, 0.2, 0.2]

        self.widget_pos = Vector3([0, 0, 0])
        self.parent = Vector3([0,0,0])
        self.pos_plus_parent = Vector3([self.parent.x + self.widget_pos.x, self.parent.y + self.widget_pos.y, 0])

        #n Switches
        self.isOver = False
        self.isClicked = False
        self.stateCounter = 0
        self.states = [*states]
        self.isState = self.states[0]
        self.oneClick = True
        self.outputState = 1
        #n Shader or Shaders
        self.program = shader

        #n Widget Elements
        #n      initialize Elements

        self.rectangle  = Rectangle.Rectangle(105,30,self.program)
        self.rectangle2 = Rectangle.Rectangle(105,4,self.program)
        self.text = Text.Text('Exo','Regular',20)
        self.text2 = Text.Text('Exo','Bold',20)
        self.widget_elements = [self.rectangle,self.rectangle2]
        self.text_elements = [self.text, self.text2 ]

        #n      setup Elements
        self.rectangle.setPos(52.5,15,0)
        self.rectangle.setFillColor(*self.color_back,.2)
        self.rectangle.setLineColor(0.922, 0.231, 0.353,1)
        self.rectangle.setLineWidth(2)

        self.rectangle2.setPos(52.5,0,0)
        self.rectangle2.setLineColor(*self.color_passive)
        self.rectangle2.setFillColor(*self.color_passive)
        self.rectangle2.setLineWidth(2)

        self.text.setParent(*self.pos_plus_parent)
        self.text.setColor(*self.color_passive)

        self.text2.setParent(*self.pos_plus_parent)
        self.text2.setColor(*self.color_passive)

        #n          update matricies befor draw loop
        for i in self.widget_elements:
            i.setParent(*self.pos_plus_parent)
            i.updateMatrix()
        for i in self.text_elements:
            i.setParent(*self.pos_plus_parent)
            i.updatePos()

        #n Widget Data
        self.debugs = [self.isState,self.isOver,self.isClicked]

    #n4 Widget Element Draw
    def draw(self,proj,view):
        glEnable(GL_BLEND)
        glEnable(GL_LINE_SMOOTH)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        #n Draw elements
        if self.isState == self.states[0]:
            self.buttonText = self.states[0]
            if self.isOver is False:
                self.rectangle2.setFillColor(*self.color_passive)
                self.rectangle2.setLineColor(*self.color_passive[:-1],0)
                self.rectangle2.draw(proj,view)
                self.text.setColor(*self.color_passive)
                self.text.setPos(-1, 8.5, 0)
                self.text.draw(self.buttonText)

            elif self.isOver is True:
                if self.isClicked is True:
                    self.rectangle2.setFillColor(*self.color_hover)
                    self.rectangle2.setLineColor(*self.color_hover[:-1], 0)
                    self.rectangle2.draw( proj, view)
                    self.text2.setPos(-1, 8.5, 0)
                    self.text2.setColor(*self.color_active)
                    self.text2.draw(self.buttonText)
                    # self.rectangle2.draw(self.program, proj, view)
                elif self.isClicked is False:
                    self.rectangle2.setFillColor(*self.color_hover)
                    self.rectangle2.setLineColor(*self.color_hover[:-1], 0)
                    self.rectangle2.draw( proj, view)
                    self.text2.setPos(-1, 8.5, 0)
                    self.text2.setColor(*self.color_hover)
                    self.text2.draw(self.buttonText)

        elif self.isState == self.states[1]:
            self.buttonText = self.states[1]
            if self.isOver is False:
                self.rectangle2.setFillColor(*self.color_passive)
                self.rectangle2.setLineColor(*self.color_passive[:-1], 0)
                self.rectangle2.draw( proj, view)
                self.text.setColor(*self.color_passive)
                self.text.draw(self.buttonText)

            elif self.isOver is True:
                if self.isClicked is True:
                    self.rectangle2.setFillColor(*self.color_hover)
                    self.rectangle2.setLineColor(*self.color_hover[:-1], 0)
                    self.rectangle2.draw( proj, view)
                    self.text2.setColor(*self.color_active)
                    self.text2.draw(self.buttonText)

                elif self.isClicked is False:
                    self.rectangle2.setFillColor(*self.color_hover)
                    self.rectangle2.setLineColor(*self.color_hover[:-1], 0)
                    self.rectangle2.draw( proj, view)
                    self.text2.setColor(*self.color_hover)
                    self.text2.draw(self.buttonText)


        # print(f'{"Button State":<20} : {str(self.isState):.>20}')
        glDisable(GL_BLEND)

    def setText(self,string):
        self.buttonText = string

    def active(self,mX,mY,mEvent,mAction):
        mouseX  = mX
        mouseY  = mY
        mouseEvent = mEvent
        mouseAction = mAction
        dimensions = self.rectangle.getPositions()

        #n Update Widget and Elements
        if dimensions[0].x < mouseX < dimensions[1].x and dimensions[0].y < mouseY < dimensions[1].y  :
            self.isOver = True
        else: self.isOver = False

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



        if self.isOver and not self.isClicked:
            pass
        elif self.isOver and self.isClicked:
            if self.oneClick:
                pos_in_list = self.states.index(self.isState)
                self.stateCounter = pos_in_list
                if self.stateCounter>=(len(self.states)-1):
                    self.stateCounter = 0
                    self.isState =self.states[self.stateCounter]
                else:
                    self.stateCounter +=1
                    self.isState = self.states[self.stateCounter]

                self.outputState = self.states.index(self.isState) + 1
                self.oneClick = False
            else:pass

        elif not self.isOver and self.isClicked:
            if mouseAction == "RELEASE":
                self.isClicked = False

        self.debugs = [self.outputState, self.isOver, self.isClicked]

    def cleanup(self):
        for e in self.widget_elements:
            e.clear()

    def getState(self):
       return self.outputState

    def setPos(self, x, y, z):
        self.widget_pos = Vector3([x, y, z])
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
        self.rectangle.setLineColor(*self.color_passive)
        self.rectangle2.setLineColor(*self.color_passive)
        self.rectangle2.setFillColor(*self.color_passive)
        self.text.setColor(*self.color_passive)
        self.text2.setColor(*self.color_passive)

    def debug(self):
        return self.debugs

