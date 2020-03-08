from ..Shapes import Text,UVRectangle2
from ... import small_tools
from bgl import *
from ...ExternalModules.pyrr import Vector3


class Slider:
    def __init__(self, posx, posy, size):
        #n Color
        self.color_hover = [0.918, 0.565, 0.522, 1]
        self.color_active = [0.914, 0.882, 0.8, 1]
        self.color_passive = [0.431, 0.341, 0.451, 1]
        self.color_back = [0.2, 0.2, 0.2]

        #n Position
        self.parent = Vector3([0,0,0])
        self.widget_pos = Vector3([posx, posy, 0])
        self.pos_plus_parent = Vector3([self.parent.x + self.widget_pos.x, self.parent.y + self.widget_pos.y, 0.0])
        #n Shader or Shaders


        #n  initialize Elements:
        self.size = size
        self.rectangle = UVRectangle2.UVRectangle2(*self.size)
        self.text = Text.Text("Exo","Light",int(self.size[1]*.4))
        self.widget_elements = [self.rectangle, ]
        self.widget_text     = [self.text, ]

        #n      setup Elements:
        self.rectangle.setParent(*self.pos_plus_parent)
        self.rectangle.setPos(0,0,0)
        self.rectangle.setColors(self.color_passive, self.color_hover, self.color_active)

        self.text.setParent(*self.pos_plus_parent)
        self.text.setPos(-self.size[0]/2,0,0)
        self.text.setColor(*self.color_passive)


        #n          update matricies before draw loop
        for i in self.widget_elements:
            i.updateMatrix()
        for i in self.widget_text:
            i.updatePos()

        #n Elements Data
        self.points = self.rectangle.getPositions()
        self.state = 0
        self.value = 0

        #n Triggers
        self.isOver = False
        self.isClicked = False
        self.debugs = [self.isOver,self.isClicked,self.state,[]]

    def draw(self, shader,proj,view):
        glEnable(GL_BLEND)
        glEnable(GL_LINE_SMOOTH)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # draw!
        self.text.setPos(-self.size[0]/2+self.size[0]/12, self.size[1]/12,0)
        self.text.setScale(int(self.size[1]*.4))
        self.text.setColor(*self.color_passive)
        self.text.draw("inbetween")
        self.rectangle.draw(shader, proj, view)
        # end Draw!
        glDisable(GL_BLEND)

    def active(self,mX, mY, mouseEvent, mouseAction):
        mouseX = mX
        mouseY = mY
        mX_in_rect, mY_in_rect = self.size[0]/2, self.size[1]/2
        p1 = self.points[0]+self.pos_plus_parent
        p2 = self.points[1]+self.pos_plus_parent

        if p1.x< mouseX <p2.x and p1.y< mouseY <p2.y:

            self.isOver = True
            if mouseEvent == "LEFTMOUSE" and mouseAction == "PRESS":
                self.isClicked = True

            elif mouseAction == "RELEASE":
                self.isClicked = False

        else:
            self.isOver = False
            if  mouseAction == "RELEASE":
                self.isClicked = False

        if self.isOver and not self.isClicked:
            self.state = 1
        elif self.isOver and self.isClicked:
            self.state = 2
        elif not self.isOver and not self.isClicked:
            self.state = 0
        elif not self.isOver and self.isClicked:
            self.state = 2

        if self.state == 2:
            mX_in_rect = mouseX - p1.x
            mY_in_rect = mouseY - p2.y
            mouse_map = mX_in_rect - self.points[1].x
            self.value = small_tools.remapRange(self.points[0].x,self.points[1].x, -1, 1, mouse_map)


        elif self.state == 0 or self.state == 1:
            mX_in_rect, mY_in_rect = self.size[0]/2, self.size[1]/2
            self.value = 0
        self.rectangle.setMouse(mX_in_rect, mY_in_rect, self.state)

        d = [(self.points[0].x, mX_in_rect - self.points[1].x ,self.points[1].x)]
        self.debugs[3] = d

    def cleanup(self):
        for e in self.widget_elements:
            e.clear()

    def getState(self):
        return [self.state, self.value]

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
        for i in self.widget_text:
            i.setParent(*self.pos_plus_parent)
            i.updatePos()


    def setColors(self, passive, hover, active, focus):
        self.color_passive = passive
        self.color_hover = hover
        self.color_active = active
        self.color_focus = focus
        self.rectangle.setColors(self.color_passive, self.color_hover, self.color_active)


    def debug(self):
        return self.debugs

