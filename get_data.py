import bpy

class MY_OT_MouseProps(bpy.types.PropertyGroup):
    mouse_posx   : bpy.props.FloatProperty(  name= 'Mouse position X')
    mouse_posy   : bpy.props.FloatProperty(  name= 'Mouse position Y')
    mouse_event  : bpy.props.StringProperty( name= 'Mouse Event'     )
    mouse_action : bpy.props.StringProperty( name= 'Mouse Action'     )
    keyboard_input : bpy.props.StringProperty(name = 'Keyboard Input')
    stop_input : bpy.props.BoolProperty(name = 'Mouse is hovering',default = False)
    main_ui : bpy.props.BoolProperty(name="Main Ui Toggle",default = False)

bpy.utils.register_class(MY_OT_MouseProps)
bpy.types.Scene.mouse_data = bpy.props.PointerProperty(type= MY_OT_MouseProps)

class MY_OT_getMouseData(bpy.types.Operator):
    bl_idname = "mouse.get_data"
    bl_label  = "modal get mouse data"

    def __init__(self):
        print(f'{"Getting Mouse Data":-^60}')

    def __del__(self):
        print(f'{"Stopping Mouse Data":-^60}')


    def modal(self, context, event):

        bpy.data.scenes[0].mouse_data.mouse_posx = event.mouse_x
        bpy.data.scenes[0].mouse_data.mouse_posy = event.mouse_y

        bpy.data.scenes[0].mouse_data.mouse_event = event.type

        bpy.data.scenes[0].mouse_data.mouse_action = event.value

        bpy.data.scenes[0].mouse_data.keyboard_input = event.ascii


        if bpy.data.scenes[0].mouse_data.stop_input is False:
            return {'PASS_THROUGH'}
        elif bpy.data.scenes[0].mouse_data.stop_input is True:
            return {'RUNNING_MODAL'}


    def invoke(self, context, event) :
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

bpy.utils.register_class(MY_OT_getMouseData)


def UnregisterModalTest():
    bpy.utils.unregister_class(MY_OT_getMouseData)

# bpy.app.timers.register(UnregisterModalTest, first_interval = 10)