bl_info = {
    "name"       : "keyframe.NUDGE",
    "author"     : "okuma_10",
    "version"    : (0, 9, 0),
    "blender"    : (2, 80, 0),
    "location"   : "View3D",
    "description": "Scripts to speed up animation workflow",
    "category"   : "Animation",
}

import importlib
if "bpy" in locals():
    importlib.reload(Main)
else:
    from . import Main,get_data,testfield



import bpy
on_off          = False
draw_handler    = None
area_no =  None

#n Operator
class A_OT_RunMyScript(bpy.types.Operator):
    bl_idname = "run.my_script"
    bl_label = "Runs My script"

    def __init__(self):
        print(f'\n{" START ":=^40}')

    def __del__(self):
        print(f'{" END ":=^40}\n')

    def execute(self, context):
        global  on_off,draw_handler,area_no
        area_pos = (context.area.x,context.area.y)

        on_off = not on_off

        if on_off:
            for i,area in enumerate(bpy.data.window_managers[0].windows[0].screen.areas):
                if area.x == area_pos[0] and area.y == area_pos[1]:
                    area_no = i
            the_area = bpy.data.window_managers[0].windows[0].screen.areas[area_no]
            print(the_area.type)
            print(area_no)
            print(area_pos)
            print(the_area.x,the_area.y)

            if context.area.x == area_pos[0]:
                draw_handler = context.area.spaces[0].draw_handler_add(Main.draw, (), 'WINDOW', 'POST_PIXEL')

            Main.poke_view()
            importlib.reload(get_data)
        else:
            area_no = None
            Main.initClear(draw_handler)

        return {'FINISHED'}


#n Button
class B_PT_MyScriptButton(bpy.types.Panel):
    bl_label = "RunScript"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'keyframe.NUDGE'

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row_col = row.column(align=True)
        row_col.scale_y = 1
        row_col.scale_x = 2
        row_col.operator('run.my_script', text='keyframe.Nudge')

classes = (
			A_OT_RunMyScript,
			B_PT_MyScriptButton,
		   )
register,unregister = bpy.utils.register_classes_factory(classes)

if __name__ == "__main__":
	register()

