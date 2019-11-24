import bpy,time
import numpy as np
from numpy import float32
from .ExternalModules.pyrr import matrix44
from .UI.Panels import Keyframe_Nudge
from pathlib import Path

parent = str(Path(__file__).parent)

#n get the dimensions of the View 3d - I guess works only with one view3d .
def get_view_dimensions():
    view_width = None
    view_height = None
    view_posX = None
    view_posY = None
    windows = bpy.context.window_manager.windows
    for window in windows:
        for area in window.screen.areas:
            if area.type        =="VIEW_3D":
                view_width     = area.regions[5].width
                view_height   = area.regions[5].height
                view_posX = area.x
                view_posY = area.y
    return (view_width,view_height),(view_posX,view_posY)

def poke_view():
    poke = bpy.context.preferences.view.ui_scale
    bpy.context.preferences.view.ui_scale = 0.2
    bpy.context.preferences.view.ui_scale = poke


#n Projection and view matrix
view_dimensions = get_view_dimensions()[0]
view_position = get_view_dimensions()[1]
projection = matrix44.create_orthogonal_projection_matrix(0, view_dimensions[0], 0, view_dimensions[1], 0.001, 1000, dtype = float32)
view = matrix44.create_from_translation([0, 0, -0.1], dtype=float32)

start_ui = None
#n Draw handler for the draw function
draw_handler = None
clear           =   False

#n Elements

Panel           = None

lastTime = time.process_time()
nbFrames = 0
fps = 0
message = ""
time1       = None
isOver = False

#n4 the initialization switch !!!
initialized = False
#n4 update projection Matrix switch
viewport_size_change = False


#n1 Draw Function
def draw():
    mouse_x         = bpy.data.scenes[0].mouse_data.mouse_posx
    mouse_y         = bpy.data.scenes[0].mouse_data.mouse_posy
    mouse_event     = bpy.data.scenes[0].mouse_data.mouse_event
    mouse_action    = bpy.data.scenes[0].mouse_data.mouse_action

    global initialized, viewport_size_change, projection, view_position, view_dimensions,clear, \
    fps, nbFrames, lastTime, time1, message, isOver, Panel

    #n1 Initialization 4

    if not initialized:
        initialized = True
        bpy.ops.mouse.get_data('INVOKE_DEFAULT')

        #n Elements

        Panel = Keyframe_Nudge.keyframeNUDGE(370, 405, 275, 275)


    #n2 Draw and Update
    else:
        #n5 Draw:
        if viewport_size_change:
            view_dimensions,view_position = get_view_dimensions()[0],get_view_dimensions()[1]
            projection = matrix44.create_orthogonal_projection_matrix(0, view_dimensions[0], 0, view_dimensions[1], 0.001, 1000, dtype=float32)
            viewport_size_change = False
        else: pass

        ct = np.sin(time.time())

        currentTime = time.process_time()
        nbFrames += 1
        if(currentTime-lastTime) >= 1:
            fps = 1000.0/nbFrames

            nbFrames = 0
            lastTime += 1

        else:pass

        #n7 Update:

        Panel.draw(projection,view)
        isOver = Panel.active(mouse_x, mouse_y, mouse_event, mouse_action,view_position,fps)


        current_view_dimensions, current_view_pos = get_view_dimensions()[0], get_view_dimensions()[1]
        if view_dimensions[0] != current_view_dimensions[0] or view_dimensions[1] != view_dimensions[0]:
            message = "Screen Size Changed"
            viewport_size_change = True

    #n4 Cleanup :
    if clear:
        Panel.cleanup()

        try:
             glDeleteProgram(shader.getShader())

             glDisable(GL_BLEND)
             glDisable(GL_LINE_SMOOTH)
        except:
            pass

        bpy.app.timers.register(in_10_1_second, first_interval=.03)

    #n  Force Blender to redraw the screen

    screen = bpy.context.screen.name
    bpy.data.screens[screen].update_tag()
# Draw Function End


#n Cleanup
def initClear(draw_handler1):
    global clear,draw_handler
    clear = True
    draw_handler = draw_handler1
    bpy.app.timers.register(in_10_1_second, first_interval=.03)

def in_10_1_second() :
    global initialized,clear,main_log,start_ui
    if draw_handler is not None:
        bpy.types.SpaceView3D.draw_handler_remove(draw_handler, 'WINDOW')
    else: pass
    initialized  = False
    clear        = False
    start_ui = False
#n End Cleanup