import blf,os,bpy,time
import copy
import numpy as np
from ...ExternalModules.pyrr import matrix44,Matrix44
from ...KeyframeNudge_scripts.Grease import Grease_Nudge,Grease_PushPull,Grease_HoldFor
from ...KeyframeNudge_scripts.Keyframe import Keyframe_Nudge,Inbetween,Hold_For,Push_Pull,Nudge,ComeOver
from ... import Logger, small_tools, Shader_Loader
from ..Shapes import Text, Rectangle, UVRectangleMasked,Unused_shapes
from ..Widgets import RectangleButton, RectangleButton2,\
                        StateButton, TextField,\
                        Slider, StateButton02
from bgl import *
from pathlib import Path

parents = Path(__file__).parents
UI_dir = None

for parent in parents:
    if parent.name == "UI":
        UI_dir = str(parent)

# log_file = r'D:\Nikola\Temp_Logs\Widgets.log'
# log = Logger.Log(log_file)


class keyframeNUDGE:
    def __init__(self,posX,posY,width,height):
        #n Shaders
        self.basic_shader       = Shader_Loader.ShaderLoader()
        self.test_shader        = Shader_Loader.ShaderLoader()
        self.slider_shader      = Shader_Loader.ShaderLoader()
        self.flat_masked_shader = Shader_Loader.ShaderLoader()
        self.debug_shader       = Shader_Loader.ShaderLoader()
        #n   Load Shaders
        self.test_shader.compile_shader         (UI_dir + "/Shaders/Shape_vert.glsl" ,  UI_dir + "/Shaders/Shape_frag.glsl")
        self.slider_shader.compile_shader       (UI_dir + "/Shaders/Shape_vert.glsl" ,  UI_dir + "/Shaders/Slider_frag.glsl")
        self.debug_shader.compile_shader        (UI_dir + "/Shaders/Shape_vert.glsl" ,  UI_dir + "/Shaders/Debug_frag.glsl")
        self.basic_shader.compile_shader        (UI_dir + "/Shaders/flat_vertex.glsl",  UI_dir + "/Shaders/flat_fragment.glsl")
        self.flat_masked_shader.compile_shader  (UI_dir + "/Shaders/Shape_vert.glsl" ,  UI_dir + "/Shaders/flat_tex_mask_frag.glsl")
        #n Colors
        self.color_active = [*small_tools.GetThemeColors().active, 1]
        self.color_text = [*small_tools.GetThemeColors().text,1]
        self.color_passive = [*small_tools.GetThemeColors().passive]
        self.color_back = [*small_tools.GetThemeColors().background]

        #n pos and dimensions
        self.pos = [posX+(width/2),posY-(height/2),0]
        self.dimensions = (width,height)

        #n Shapes
        self.bg = Rectangle.Rectangle(*self.dimensions,self.basic_shader)
        self.translate = UVRectangleMasked.UVRectangleMasked(.09,self.flat_masked_shader)

        self.tLCorner = Unused_shapes.RoundedCorner(9,10,self.basic_shader)
        self.tRCorner = Unused_shapes.RoundedCorner(9,10,self.basic_shader)
        self.bLCorner = Unused_shapes.RoundedCorner(9,10,self.basic_shader)
        self.bRCorner = Unused_shapes.RoundedCorner(9,10,self.basic_shader)

        self.shape_elements = [
                                self.bg,        self.translate,
                                self.tLCorner,  self.tRCorner,
                                self.bLCorner,  self.bRCorner
                               ]
        self.text_elements = []


        #n  shape settings
        self.bgRect_pos = self.bg.getPositions()
        self.bg.setParent(*self.pos)
        self.bg.setPos(0,0,0)
        self.bg.setFillColor(*self.color_passive, 0)

        self.tLCorner.setParent(*self.pos)
        self.tLCorner.setPos(self.bgRect_pos[0].x+10,self.bgRect_pos[1].y-10,0)
        self.tLCorner.setScale(-1,1,1)
        self.tLCorner.setLineColor(*self.color_passive,1)

        self.tRCorner.setParent(*self.pos)
        self.tRCorner.setPos(self.bgRect_pos[1].x-10, self.bgRect_pos[1].y-10, 0)
        self.tRCorner.setScale(1, 1, 1)
        self.tRCorner.setLineColor(*self.color_passive, 1)

        self.bLCorner.setParent(*self.pos)
        self.bLCorner.setPos(self.bgRect_pos[0].x + 10, self.bgRect_pos[0].y + 10, 0)
        self.bLCorner.setScale(-1, -1, 1)
        self.bLCorner.setLineColor(*self.color_passive, 1)

        self.bRCorner.setParent(*self.pos)
        self.bRCorner.setPos(self.bgRect_pos[1].x - 10, self.bgRect_pos[0].y + 10, 0)
        self.bRCorner.setScale(1, -1, 1)
        self.bRCorner.setLineColor(*self.color_passive, 1)

        self.translate.setParent(*self.pos)
        self.translate.setPos(self.dimensions[0]/6,self.dimensions[1]/2,0)
        self.translate.setColors([*self.color_passive,1],self.color_active,self.color_active)

        #n Widgets
        #n  init
        self.StateButton_01 = StateButton.StateButton([r'PUSH | PULL', 'NUDGE'], self.basic_shader)
        self.StateButton_02 = StateButton.StateButton([r'frames', 'seconds'], self.basic_shader)

        self.TitleState     = StateButton02.StateButton02(self.basic_shader)

        self.hold_For       = RectangleButton.RectangleButton([105,30],self.basic_shader)
        self.come_Over      = RectangleButton.RectangleButton([105,30],self.basic_shader)

        self.Push_Button    = RectangleButton2.RectangleButton2([100, 50], [30, 55], self.test_shader, 0)
        self.Pull_Button    = RectangleButton2.RectangleButton2([100, 50], [30, 55], self.test_shader, 1)

        self.Slider         = Slider.Slider(0,0,[220,40])

        self.InputField     = TextField.TextField(self.basic_shader)

        self.widget_elements = [self.StateButton_01,    self.StateButton_02,
                                self.Slider,            self.Push_Button,
                                self.Pull_Button,       self.hold_For,
                                self.come_Over,
                                self.InputField,
                                self.TitleState,
                                ]

        #n  setup
        self.StateButton_01.setParent(*self.pos)
        self.StateButton_01.setPos(-108, 85, 0)
        self.StateButton_02.setParent(*self.pos)
        self.StateButton_02.setPos(2, 85, 0)

        self.TitleState.setParent(*self.pos)
        self.TitleState.setPos(-self.dimensions[0]/7.5,self.dimensions[1]/2,0)

        self.come_Over.setParent(*self.pos)
        self.come_Over.setPos(53,-50,0)
        self.come_Over.setText("COME OVER")

        self.hold_For.setParent(*self.pos)
        self.hold_For.setPos(-53,-50,0)
        self.hold_For.setText("HOLD FOR")

        self.Pull_Button.setParent(*self.pos)
        self.Pull_Button.setPos(-50, -5, 0)

        self.Push_Button.setParent(*self.pos)
        self.Push_Button.setPos(-50, 45, 0)

        self.Slider.setParent(*self.pos)
        self.Slider.setPos(0,-100,0)

        self.InputField.setParent(*self.pos)
        self.InputField.setPos(22,-15,0)

        #n  update
        for i in self.widget_elements:
            i.updateElements()
        for i in self.shape_elements:
            i.updateMatrix()
        for i in self.text_elements:
            if len(self.text_elements)<0:
                i.setParent(*self.text_rectangle_pos)
                i.updatePos()

        #n Element Data
        self.points = self.bg.getPositions()

        #n Panel Data
        self.tr_dim = self.translate.getPositions()  #translate rectangle dimensions
        self._Translate = False
        self.isOTrans = False
        self.panel_state = 0
        self.distX = 0
        self.distY = 0
        self.once = True
        self.debug = []
        self.myproj = None
        #n Button States
        self.frame_seconds      = None
        self.push_nudge         = None
        self.push_state         = None
        self.pull_state         = None
        self.come_over_state    = None
        self.hold_for_state     = None
        self.input              = None
        self.slider_stateVal    = [None,None]
        self.Inbetween_handler  = Inbetween.Inbetween()
        self.inbetween_gen_map_switch = True
        self.slDebug = self.Slider.debug()

    #n Draw Loop
    def draw(self,proj,view):

        glEnable(GL_BLEND)
        glEnable(GL_LINE_SMOOTH)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        #n0 Background
        # self.bg.draw(proj,view)
        self.tLCorner.draw(proj,view)
        self.tRCorner.draw(proj,view)
        self.bLCorner.draw(proj, view)
        self.bRCorner.draw(proj, view)
        #n translate area:
        if self.isOTrans and not self._Translate:
            self.translate.setState(1)
        elif self.isOTrans and self._Translate:
            self.translate.setState(2)
        elif not self.isOTrans and self._Translate:
            self.translate.setState(2)
        elif not self.isOTrans and not self._Translate:
            self.translate.setState(0)
        self.translate.draw(proj,view)


        #n6 Elements
        if self.panel_state == 0:   # Keyframe tools
            self.StateButton_01.draw(proj,view)
            self.StateButton_02.draw(proj,view)
            self.Slider.draw(self.slider_shader,proj,view)
            self.Pull_Button.draw(proj,view)
            self.Push_Button.draw(proj,view)
            self.come_Over.draw(proj,view)
            self.hold_For.draw(proj,view)
            self.InputField.draw(proj,view)
            self.TitleState.draw(proj,view)
        elif self.panel_state ==1: # Grease Pencil tools
            self.StateButton_01.draw(proj, view)
            self.StateButton_02.draw(proj, view)
            self.Pull_Button.draw(proj, view)
            self.Push_Button.draw(proj, view)
            self.come_Over.draw(proj, view)
            self.hold_For.draw(proj, view)
            self.InputField.draw(proj, view)
            self.TitleState.draw(proj, view)


        glDisable(GL_BLEND)

    #n Event Listener for buttons
    def active(self,mouseX, mouseY, mouseEvent, mouseAction, viewPos,fps):
        isOver = False
        isActive = False
        mX = mouseX - viewPos[0]
        mY = mouseY - viewPos[1]
        self.isOTrans = False
        newdistance = [0,0]


        #n Check if mouse is over Panel
        if self.points[0].x < mX < self.points[1].x and self.points[0].y < mY < self.points[1].y+10:
            isOver = True
        else:
            pass
        #n Activate Title StateButton
        self.TitleState.active(mX, mY, mouseEvent, mouseAction)
        self.panel_state = self.TitleState.getState()

        #n if Mouse is over Panel
        if isOver:
            bpy.data.scenes[0].mouse_data.stop_input = True  # deactivate viewport mouse clicks
            #n translate  - n9 if mouse is in translate rectangle area
            if self.tr_dim[0].x < mX < self.tr_dim[1].x and self.tr_dim[0].y < mY < self.tr_dim[1].y:
                self.isOTrans = True
            #n check for clicks in translate Rectangle
            if self.isOTrans:
                if mouseEvent == "LEFTMOUSE" and mouseAction == "PRESS":
                    self._Translate = True
                    if self.once:
                        self.distX = mX - self.pos[0]
                        self.distY = mY - self.pos[1]

                        self.once = False
                elif mouseEvent == "LEFTMOUSE" and mouseAction == "RELEASE":
                    self._Translate = False
                    self.once = True
                    self.points = self.bg.getPositions()
                    self.tr_dim = self.translate.getPositions()


            # #n4 make widgets Active
            self.StateButton_01.active  (mX, mY, mouseEvent, mouseAction)
            self.StateButton_02.active  (mX, mY, mouseEvent, mouseAction)
            self.Slider.active          (mX, mY, mouseEvent, mouseAction)
            self.Pull_Button.active     (mX, mY, mouseEvent, mouseAction)
            self.Push_Button.active     (mX, mY, mouseEvent, mouseAction)
            self.come_Over.active       (mX, mY, mouseEvent, mouseAction)
            self.hold_For.active        (mX, mY, mouseEvent, mouseAction)

            self.frame_seconds = self.StateButton_02.getState()
            self.push_nudge    = self.StateButton_01.getState()

            self.InputField.active      (mX, mY, mouseEvent, mouseAction,self.frame_seconds)



            #n Button actions !!!! -->
            self.input              = self.InputField.getValue()
            self.pull_state         = self.Pull_Button.getState()
            self.push_state         = self.Push_Button.getState()
            self.come_over_state    = self.come_Over.getState()
            self.hold_for_state     = self.hold_For.getState()
            self.slider_stateVal    = self.Slider.getState()

            if self.panel_state == 0:                       #n2 if state is Keyframe
                if self.push_nudge == 1:                    #n2 if nudge/push pull is in push pull
                    self.input = int(self.input)
                    if self.pull_state == 2:                #n2 Push
                        Push_Pull.PushPull(-self.input)
                    if self.push_state == 1:
                        Push_Pull.PushPull(self.input)

                elif self.push_nudge == 2:                  #n2 Nudge
                    self.input = int(self.input)
                    if self.pull_state == 2:
                        Nudge.keyframe_nudge(-self.input)
                    if self.push_state == 1:
                        Nudge.keyframe_nudge(self.input)

                if self.come_over_state == 2:               #n2 Come Over
                    # print('Click! Fix Me!')
                    ComeOver.comeOver()
                if self.hold_for_state == 2:                #n2 Hold For
                    # print('Click!! Fix Me')
                    Hold_For.hold_for(self.input)

                if self.slider_stateVal[0] == 1:                #n2 Inbetween
                    self.Inbetween_handler.updateSharedData()
                    self.Inbetween_handler.developInbetween()
                elif self.slider_stateVal[0] == 2:
                    self.Inbetween_handler.execute(self.slider_stateVal[1])
                if self.slider_stateVal[0] == 1 and mouseAction == "RELEASE":
                    pass


            elif self.panel_state == 1:                     #n4 if state is Grease
                if self.push_nudge == 1:                        #n3 Push Pull
                    self.input = int(self.input)
                    if self.pull_state == 2:
                        Grease_PushPull.GP_PushPull(-self.input)
                    if self.push_state == 1:
                        Grease_PushPull.GP_PushPull(self.input)
                elif self.push_nudge == 2:                       #n3 Nudge
                    self.input = int(self.input)
                    if self.pull_state == 2:
                        Grease_Nudge.gp_Nudge(-self.input)
                    if self.push_state == 1:
                        Grease_Nudge.gp_Nudge(self.input)

                if self.hold_for_state == 2:                       #n3 Hold For
                    Grease_HoldFor.Hold_For(self.input)

            #n End of Actions Block

        else:
            bpy.data.scenes[0].mouse_data.stop_input = False #  make mouse clicks in viewport active


        if not isOver or not self.isOTrans: # mouse is over but not over translate rectangle and if mouse is realeased
            if self._Translate and mouseAction == "RELEASE":
                self._Translate = False
                self.once = True
                self.points = self.bg.getPositions()
                self.tr_dim = self.translate.getPositions()


        #n if Translation is activated
        if self._Translate:
            newdistance[0] = mX-self.distX
            newdistance[1] = mY-self.distY
            self.pos[0] = newdistance[0]
            self.pos[1] = newdistance[1]


            for i in self.shape_elements:
                i.setParent(*self.pos)
                i.updateMatrix()
            for i in self.text_elements:
                if len(self.text_elements)>0:
                    i.setParent(*self.pos)
                    i.updatePos()
            for i in self.widget_elements:
                i.setParent(*self.pos)
                i.updateElements()
        else:pass

        if isOver and not self._Translate:
            isActive = True
        elif isOver and self._Translate:
            isActive = True
        elif not isOver and self._Translate:
            isActive = True
        elif not isOver and not self._Translate:
            isActive = False




        # #n Debug Output
        # self.debug = self.InputField.debugs()
        # self.slDebug = self.Slider.debug()
        # self.inbetween_debug = self.Inbetween_handler.debugPrint()
        # hold_for_debug = self.hold_For.debug()
        # log.removeHandler()
        # log.addHandler(log_file)
        # log.clearFile()
        # log.print(f'''
        # {"Input":^38}{"":^5}{"Other stuff":^22}
        # {"":=^38}
        # |◦{"Mouse Attributes":20} {"":<12} |    {fps:<15.3} : {"FPS":>10}
        # | +- {" " + str(mouseAction) + " " :.^20}  | {"Action":<7} |
        # | +- {" " + str(mouseEvent)+ " " :.^20}  | {"Event":<7} |
        # | +- {mX:.^20}  | {"X":<7} |
        # | +- {mY:.^20}  | {"Y":<7} |
        # |{str(isOver):^34}  |
        # {"":=^38}''')
        #
        # log.print(f"""
        # {"":=^57}
        # | {"Additional Data":^25} | {"State Button 2":25} |
        # ├ {"":-^26}┼{"":-^27}┤
        # | {" "+ str(hold_for_debug[0]) +" ":.^25} | {"isOver":<25} |
        # | {" "+ str(hold_for_debug[1]) +" ":.^25} | {"State":<25} |
        # | {" "+ str(hold_for_debug[2]) +" ":.^25} | {"clickOnce":<25} |
        # | {" "+ str(None) +" ":.^25} | {"None":<25} |
        # | {" "+ str(None) +" ":.^25} | {"None":<25} |
        # | {" "+ str(None) +" ":.^25} | {"None":<25} |
        # {"":=^57}
        # """)

        # log.print(f'X : {self.inbetween_debug[2][0]}, Y : {self.inbetween_debug[2][1]}')
        # log.print('\n')
        # for i in self.inbetween_debug[0].items():
        #     log.print(f'{i[0]} :')
        #
        #     for v in i[1].items():
        #         log.print(f'\t◆ {v[0]} :')
        #         for v2 in v[1].items():
        #             log.print(f'\t\t{v2[0]} : {v2[1]}')
        #
        # log.print('\n')
        # for i in self.inbetween_debug[1]:
        #     log.print(f'{i[0]} : {i[1]}')
        #
        # log.removeHandler()

        return isActive

    def cleanup(self):
        for i in self.widget_elements:
            i.cleanup()