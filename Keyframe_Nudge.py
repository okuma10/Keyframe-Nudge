bl_info = {
  "name" : "Keyframe Nudge",
  "support" : "COMMUNITY",
  "category": "animation",
}

import bpy


def insert_empty_frame(usr_inp):

    area_type = bpy.context.area.type
    bpy.context.area.type = 'GRAPH_EDITOR'

    selected = bpy.context.selected_objects

    bpy.ops.graph.select_leftright(mode='RIGHT')
    
        
    for obj in selected:
        anim = obj.animation_data

        for fc in anim.action.fcurves:
            for keyframe in fc.keyframe_points:
                if keyframe.select_control_point:
                    if keyframe.co[0] == 0.0:
                        keyframe.co[0] = 0
                    else:
                        keyframe.co[0] += usr_inp
                        keyframe.handle_right[0] += usr_inp
                        keyframe.handle_left[0] += usr_inp


    bpy.ops.graph.select_all_toggle()

    bpy.context.area.type = area_type


def keyframe_nudge(usr_inp):
    selected = bpy.context.selected_objects

    for obj in selected:
        anim = obj.animation_data

        for fc in anim.action.fcurves:

            for keyframe in fc.keyframe_points:
                if keyframe.select_control_point:
                    keyframe.co[0] += usr_inp
                    keyframe.handle_right[0] += usr_inp
                    keyframe.handle_left[0] += usr_inp


class Insert_empty_Frame(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "nudge.insert_empty_frame"
    bl_label = "Isert Empty Frame Nudge"
    
    insert_input = bpy.props.FloatProperty(name="Some Floating Point",default = 0.0)

    def execute(self, context):
        insert_input = self.insert_input
        insert_empty_frame(insert_input)
        return {'FINISHED'}


class Keyframe_Nudge(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "nudge.keyframe_nudge"
    bl_label = "Keyframe Nudge"

    nudge_input = bpy.props.FloatProperty(name="Some Floating Point", default=0.0)

    def execute(self, context):
        nudge_input = self.nudge_input
        keyframe_nudge(nudge_input)
        return {'FINISHED'}


class Keyframe_Nudge_Panel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Keyframe Nudge"
    bl_idname = "KEYFRAME_NGE_simple"
    bl_space_type = 'DOPESHEET_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'Nudge_keyframes'

    def draw(self, context):
        layout = self.layout
        
        label= layout.label('+ Empty frames')
        row = layout.row(align=True)
        row.scale_y = 3.0
        row.operator('nudge.insert_empty_frame',text = '1').insert_input = 1
        row.operator('nudge.insert_empty_frame',text = '2').insert_input = 2
        row.operator('nudge.insert_empty_frame',text = '3').insert_input = 3
        row.operator('nudge.insert_empty_frame',text = '4').insert_input = 4
        row.operator('nudge.insert_empty_frame',text = '6').insert_input = 6
        label = layout.label('- Empty frames')
        row = layout.row(align=True)
        row.scale_y = 3.0
        row.operator('nudge.insert_empty_frame',text = '1').insert_input = -1
        row.operator('nudge.insert_empty_frame',text = '2').insert_input = -2
        row.operator('nudge.insert_empty_frame',text = '3').insert_input = -3
        row.operator('nudge.insert_empty_frame',text = '4').insert_input = -4
        row.operator('nudge.insert_empty_frame',text = '6').insert_input = -6
        label = layout.label('+ Nudge Keyframe ')
        row = layout.row(align=True)
        row.scale_y = 3.0
        row.operator('nudge.keyframe_nudge', text = '1').nudge_input = 1
        row.operator('nudge.keyframe_nudge', text = '2').nudge_input = 2
        row.operator('nudge.keyframe_nudge', text = '3').nudge_input = 3
        row.operator('nudge.keyframe_nudge', text = '4').nudge_input = 4
        row.operator('nudge.keyframe_nudge', text = '6').nudge_input = 6
        label = layout.label('- Nudge Keyframe ')
        row = layout.row(align=True)
        row.scale_y = 3.0
        row.operator('nudge.keyframe_nudge', text = '1').nudge_input = -1
        row.operator('nudge.keyframe_nudge', text = '2').nudge_input = -2
        row.operator('nudge.keyframe_nudge', text = '3').nudge_input = -3
        row.operator('nudge.keyframe_nudge', text = '4').nudge_input = -4
        row.operator('nudge.keyframe_nudge', text = '6').nudge_input = -6


def register():
    bpy.utils.register_class(Insert_empty_Frame)
    bpy.utils.register_class(Keyframe_Nudge)
    bpy.utils.register_class(Keyframe_Nudge_Panel)


def unregister():
    bpy.utils.unregister_class(Insert_empty_Frame)
    bpy.utils.unregister_class(Keyframe_Nudge)
    bpy.utils.unregister_class(Keyframe_Nudge_Panel)


if __name__ == "__main__":
    register()

    # test call
    #bpy.ops.nudge.simple_keyframe()
