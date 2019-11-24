import bpy
from ..Shapes import Text,Triangle,Rectangle,Line
from ... import small_tools
from bgl import *
from ...ExternalModules.pyrr import Vector3


#n TextField
class TextField:
    def __init__(self, shader):
        #n Data
        self.numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                        'NUMPAD_1', 'NUMPAD_2', 'NUMPAD_3', 'NUMPAD_4', 'NUMPAD_5', 'NUMPAD_6', 'NUMPAD_7', 'NUMPAD_8',
                        'NUMPAD_9', 'NUMPAD_0',
                        'NUMPAD_PERIOD', 'PERIOD',
                        ]
        #n Text
        self._text = '00'
        self._decimal_text = '0'
        self.string_input = self._text
        self.text_size = 100
        self.control = 0

        #n Color
        self.color_active = [*small_tools.GetThemeColors().active, 1]
        self.color_active2 = [*small_tools.GetThemeColors().active2, 1]
        self.color_text = [*small_tools.GetThemeColors().text]
        self.color_passive = [*small_tools.GetThemeColors().passive]
        self.color_back = [*small_tools.GetThemeColors().background]

        #n Position and Parent
        self.parent = Vector3([0, 0, 0])
        self.widget_pos = Vector3([0, 0, 0])
        self.pos_plus_parent = Vector3([self.parent.x + self.widget_pos.x, self.parent.y + self.widget_pos.y, 0])

        #n Switches
        self.isOver = False
        self.isOverPlus = False
        self.isOverMinus = False
        self.isEdited = False
        self.minusClick = False
        self.plusClick = False
        self.isDecimal = False
        self.isImput = 0

        #n Shader or Shaders
        self.program = shader

        #n Elements
        self.text = Text.Text('Bonn', 'Regular', self.text_size)
        self.text2 = Text.Text('Bonn', 'Regular', self.text_size)
        self.field_size = self.text.getDimensions(self._text)
        self.text_dimensions = self.text.getDimensions(self._text)
        self.line = Line.Line(self.field_size[1])
        self.minus_triangle = Triangle.Triangle(50)
        self.plus_triangle = Triangle.Triangle(50)
        self.text_rectangle = Rectangle.Rectangle(self.field_size[0], self.field_size[1], self.program)

        #n      Setup

        self.text.setParent(*self.pos_plus_parent)
        self.text.setPos(0, 0, 0)
        self.text.setColor(*self.color_passive, 1.0)

        self.text2.setParent(*self.pos_plus_parent)
        self.text2.setPos(0, 0, 0)
        self.text2.setColor(*self.color_passive, 1.0)

        self.text_rectangle.setParent(*self.pos_plus_parent)
        self.text_rectangle.setPos(32.5, 39, 0)
        self.text_rectangle.setLineColor(0.149, 0.871, 0.506, 1)
        self.text_rectangle.setFillColor(*self.color_passive, 0.0)
        self.text_rectangle.updateMatrix()

        self.line.setParent(*self.pos_plus_parent)
        self.line.setPos(0, self.field_size[1] / 2, 0)
        self.line.setLineColor(*self.color_active2)
        self.line.setRot(0, 90, 0)
        self.line.setLineWidth(3)
        self.line.updateMatrix()

        self.minus_triangle.setParent(*self.pos_plus_parent)
        self.minus_triangle.setPos(-10, (self.field_size[1] / 2), 0)
        self.minus_triangle.setRot(0, 270, 0)
        self.minus_triangle.setScale(1, .25, 1)
        self.minus_triangle.setLineColor(*self.color_passive, 0.0)
        self.minus_triangle.setFillColor(*self.color_active)

        self.plus_triangle.setParent(*self.pos_plus_parent)
        self.plus_triangle.setPos(self.field_size[0] + 10, (self.field_size[1] / 2), 0)
        self.plus_triangle.setRot(0, 270, 0)
        self.plus_triangle.setScale(1, -.25, 1)
        self.plus_triangle.setLineColor(*self.color_passive, 0.0)
        self.plus_triangle.setFillColor(*self.color_active)

        #n plus-minus triangles dimensions
        self.text_field_dimensions = self.text.getDimensions('00')
        self.minus_dimensions = self.minus_triangle.getDimensions()
        self.plus_dimensions = self.plus_triangle.getDimensions()
        self.plus_pos = self.plus_triangle.getPosition()
        self.minus_pos = self.minus_triangle.getPosition()

        minus_width, minus_height = self.minus_dimensions[1] + 10, self.text_field_dimensions[1]
        plus_width, plus_height = self.plus_dimensions[1] + 10, self.text_field_dimensions[1]

        self.minus_rectangle = Rectangle.Rectangle(minus_width, minus_height, self.program)
        self.minus_rectangle.setParent(*self.pos_plus_parent)
        self.minus_rectangle.setPos(*self.minus_pos)
        self.minus_rectangle.setLineColor(0.149, 0.871, 0.506, 1)
        self.minus_rectangle.setFillColor(*self.color_active[:-1], .0)
        self.minus_rectangle.setLineWidth(1)

        self.plus_rectangle = Rectangle.Rectangle(plus_width, plus_height, self.program)
        self.plus_rectangle.setParent(*self.pos_plus_parent)
        self.plus_rectangle.setPos(*self.plus_pos)
        self.plus_rectangle.setLineColor(0.149, 0.871, 0.506, 1)
        self.plus_rectangle.setFillColor(*self.color_active[:-1], .0)
        self.plus_rectangle.setLineWidth(1)

        self.widget_elements = [self.text_rectangle,
                                self.line,
                                self.minus_triangle,
                                self.plus_triangle,
                                self.plus_rectangle,
                                self.minus_rectangle,
                                ]

        self.text_elements = [self.text, self.text2]

        for i in self.widget_elements:
            i.setParent(*self.pos_plus_parent)
            i.updateMatrix()
        for i in self.text_elements:
            i.setParent(*self.pos_plus_parent)
            i.updatePos()

        self.debug = False
        self.debug1 = []
        self.debut_text_pos = None

    #n Draw Loop
    def draw(self, proj, view):

        active_area = self.text_rectangle.getPositions()
        active_width = active_area[1].x - active_area[0].x
        current_text = self.text.getDimensions(self._text)
        current_text_end_pos = active_area[0].x + current_text[0]
        right_align_offset = active_area[1].x - current_text_end_pos
        self.debut_text_pos = [current_text[0],active_width]

        glEnable(GL_BLEND)
        glEnable(GL_LINE_SMOOTH)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        #n debug
        if self.debug:
            self.minus_rectangle.draw(proj, view)
            self.plus_rectangle.draw(proj, view)
            self.text_rectangle.draw(proj, view)

        #n 0
        if len(self._text) == 1:
            self.text.setPos(active_width/2-current_text[0]/2, 0, 0)
            self.line.setPos(active_width/2-current_text[0]/2, self.field_size[1] / 2, 0)
            self.line.setLineWidth(3)
            self.line.updateMatrix()

            if not self.isOver and not self.isEdited:
                self.text.setColor(*self.color_passive, 1.0)
                self.text.draw(self._text)

            elif self.isOver and self.isEdited:
                self.text.setColor(*self.color_active2)
                self.text.draw(self._text)
                self.line.draw(self.program, proj, view)

            elif not self.isOver and self.isEdited:
                self.text.setColor(*self.color_active2)
                self.text.draw(self._text)
                self.line.draw(self.program, proj, view)

            elif self.isOver and not self.isEdited:
                self.minus_triangle.draw(self.program, proj, view)
                self.plus_triangle.draw(self.program, proj, view)
                self.text.setColor(*self.color_active)
                self.text.draw(self._text)

        #n 00
        elif len(self._text) == 2:
            self.text.setPos(active_width/2-current_text[0]/2, 0, 0)
            self.line.setPos(active_width/2-current_text[0]/2, self.field_size[1] / 2, 0)
            self.line.setLineWidth(3)
            self.line.updateMatrix()

            if not self.isOver and not self.isEdited:
                self.text.setColor(*self.color_passive, 1.0)
                self.text.draw(self._text)

            elif self.isOver and self.isEdited:
                self.text.setColor(*self.color_active2)
                self.text.draw(self._text)
                self.line.draw(self.program, proj, view)

            elif not self.isOver and self.isEdited:
                self.text.setColor(*self.color_active2)
                self.text.draw(self._text)
                self.line.draw(self.program, proj, view)

            elif self.isOver and not self.isEdited:
                self.minus_triangle.draw(self.program, proj, view)
                self.plus_triangle.draw(self.program, proj, view)
                self.text.setColor(*self.color_active)
                self.text.draw(self._text)

        elif len(self._text) == 0:
            if self.isEdited and self.isOver:
                self.line.setPos(self.field_size[0], self.field_size[1] / 2, 0)
                self.line.setLineColor(*self.color_active2)
                self.line.setLineWidth(1)
                self.line.updateMatrix()
                self.line.draw(self.program, proj, view)

            elif self.isOver and not self.isEdited:
                self.line.setPos(self.field_size[0], self.field_size[1] / 2, 0)
                self.line.setLineColor(*self.color_active)
                self.line.setLineWidth(2)
                self.line.updateMatrix()
                self.line.draw(self.program, proj, view)

                self.text.setPos((self.field_size[0] / 2) - (self.text_size / 10), 0, 0)
                self.text.draw("!")

                self.minus_triangle.setLineColor(*self.color_active[:-1], 0.0)
                self.plus_triangle.setLineColor(*self.color_active[:-1], 0.0)
                self.minus_triangle.draw(self.program, proj, view)
                self.plus_triangle.draw(self.program, proj, view)

            elif not self.isOver and not self.isEdited:
                self.line.setPos(self.field_size[0], self.field_size[1] / 2, 0)
                self.line.setLineColor(*self.color_active)
                self.line.setLineWidth(2)
                self.line.updateMatrix()
                self.line.draw(self.program, proj, view)

                self.text.setPos((self.field_size[0] / 2) - (self.text_size / 10), 0, 0)
                self.text.draw("0")
            elif not self.isOver and self.isEdited:
                self.line.setPos(self.field_size[0], self.field_size[1] / 2, 0)
                self.line.setLineColor(*self.color_active2)
                self.line.setLineWidth(1)
                self.line.updateMatrix()
                self.line.draw(self.program, proj, view)

        if self.control == 2:
            self.text2.setPos(self.field_size[0], 0, 0)
            self.text2.setScale(int(self.text_size * .4))
            self.text2.draw(self._decimal_text)
            self.text2.setScale(self.text_size)
        else:
            pass

        if self.plusClick:
            self.plus_triangle.setFillColor(*self.color_text, 1)
        elif self.minusClick:
            self.minus_triangle.setFillColor(*self.color_text, 1)
        else:
            self.minus_triangle.setFillColor(*self.color_active)
            self.plus_triangle.setFillColor(*self.color_active)

        # glDisable(GL_BLEND)


    def active(self, mX, mY, mEvent, mAction, control):
        mouseX = mX
        mouseY = mY
        mouseEvent = mEvent
        mouseAction = mAction
        keyboard = bpy.data.scenes[0].mouse_data.keyboard_input
        dimensions = (self.minus_rectangle.getPositions()[1], self.plus_rectangle.getPositions()[0])
        self.control = control

        if dimensions[0].x < mouseX < dimensions[1].x and dimensions[1].y < mouseY < dimensions[0].y:
            self.isOver = True
        else:
            self.isOver = False

        if self.isOver and not self.isEdited:
            #n Look for triangles
            if self.minus_rectangle.getPositions()[0].x > mouseX:
                self.isOverMinus = True

            elif self.plus_rectangle.getPositions()[1].x < mouseX:
                self.isOverPlus = True
            else:
                self.isOverPlus = False
                self.isOverMinus = False

            #n If click
            if mouseEvent == 'LEFTMOUSE' and mouseAction == 'PRESS':
                if self.isOverMinus:
                    self.minusClick = True

                elif self.isOverPlus:
                    self.plusClick = True

                else:
                    self.isEdited = True
                    self.isImput = False

            elif mouseEvent == 'LEFTMOUSE' and mouseAction == 'RELEASE':
                self.minusClick = False
                self.plusClick = False

        elif not self.isOver and self.isEdited:
            if mouseEvent == 'RET':
                self.isEdited = False
            elif mouseEvent == 'NUMPAD_ENTER':
                self.isEdited = False

        elif self.isOver and self.isEdited:
            if mouseEvent == 'RET':
                self.isEdited = False
            elif mouseEvent == 'NUMPAD_ENTER':
                self.isEdited = False


        elif not self.isOver and not self.isEdited:
            pass
        else:
            pass

        #n Input Logic
        if self.isEdited:
            if mouseEvent == "BACK_SPACE" and mouseAction == "PRESS":
                if self.control == 2:
                    if len(self._decimal_text) > 0:
                        if len(self._text) > 1:
                            self.isDecimal = True
                        elif len(self._text) is not 0:
                            self.isDecimal = False

                if self.isDecimal:
                    if len(self._decimal_text) is 0:
                        self.isDecimal = False
                    else:
                        pass

                if self.isDecimal:
                    if self.isImput < 1:
                        self._decimal_text = ""
                        self.isImput += 1
                else:
                    if self.isImput < 1:
                        self._text = self._text[:-1]
                        self.isImput += 1

            elif keyboard in self.numbers and mouseAction == 'PRESS':
                if len(self._decimal_text) >= 1:
                    self.isDecimal = False

                if keyboard.startswith('NUMPAD'):
                    key1 = keyboard
                    key1 = key1.split('_')[1]

                    if self.isDecimal is True:
                        if self.isImput < 1:
                            self._decimal_text += key1
                            self.isImput += 1
                        else:
                            pass
                    else:
                        if self.isImput < 1:
                            if len(self._text) < 2:
                                self._text += key1
                            self.isImput += 1
                        else:
                            pass

                else:
                    if self.isDecimal is True:
                        if self.isImput < 1:
                            self._decimal_text += keyboard
                            self.isImput += 1
                    else:
                        if self.isImput < 1:
                            if len(self._text) < 2:
                                self._text += keyboard
                            self.isImput += 1
                        else:
                            pass

            elif keyboard == '.' and mouseAction == 'PRESS':
                self.isDecimal = True

            elif mouseAction == 'RELEASE':
                self.isImput = False



        if self.minusClick:
            if not self.isImput:
                number = int(self._text)
                if number <= 0:
                    pass
                else:
                    number -= 1
                self._text = str(number)
                self.isImput = True
            else:
                pass

        elif self.plusClick:
            if not self.isImput:
                if len(self._text) != 0:
                    number = int(self._text)
                    number += 1
                    self._text = str(number)
                self.isImput = True
            else:
                pass
        # log.removeHandler()

        if mouseAction == "RELEASE":
            self.isImput = False


    def cleanup(self):
        for e in self.widget_elements:
            e.clear()


    def getValue(self):
        value = 0
        if self.control == 2:
            if len(self._text) > 0:
                value = int(self._text)
            else:
                value = 0
        elif self.control == 1:
            if len(self._text) > 0:
                if len(self._decimal_text) == 1:
                    value = int(self._text) + float("." + self._decimal_text)
                else:
                    value = int(self._text)

        return value


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

    def debugs(self):
        self.debug1 = [self._text,self.debut_text_pos]
        return self.debug1