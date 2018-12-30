bl_info = {
    "name" : "Keyframe Nudge",
    "author" : "blenderID:okuma_10",
    "version" : (0, 1, 0),
    "blender" : (2, 80, 0),
    "description" : "Various automate keyframe manipulation scripts",
    "support" : "COMMUNITY",
    "category": "Animation",
}

import bpy
from bisect import bisect

#=============== Functions ====================
#                   |
def insert_empty_frame(usr_inp):
    selected = bpy.context.selected_objects
    im_sick_of_this = bpy.context.scene.frame_current
    control = usr_inp

    for obj in selected:
        anim = obj.animation_data

        for fc in anim.action.fcurves:

            # ================= All Keyframes ====================
            all_keyframes = [keyframe for keyframe in fc.keyframe_points]
            keyframe_list_compare = [keyframe.co[0] for keyframe in all_keyframes]

            # ================= Selected Keyframes ================
            selected_keyframes = [keyframe for keyframe in fc.keyframe_points if keyframe.select_control_point]

            #================== Initial Frame =====================
            initial_time_frame = float(bpy.context.scene.frame_current)
            print(initial_time_frame)
            # ====================== Procedure ====================
            #                           |

            # ============== If user selected Keyframe ============
            # ============ Define list based on selection =========
            if len(selected_keyframes) > 0:
                first_selected_index = all_keyframes.index(selected_keyframes[0])
                working_list = all_keyframes[first_selected_index:]

                # ======================== Body ========================
                if control > 0:
                    working_list.reverse()

                    while len(working_list) > 0:
                        if working_list[-1].co[0] == 0.0:
                            if len(working_list) == 1:
                                working_list[0].co[0] = 0.0
                                # del working_list[0]
                            else:
                                working_list[0].co[0] += control
                                working_list[0].handle_right[0] += control
                                working_list[0].handle_left[0] += control
                                # del working_list[0]

                        else:
                            working_list[0].co[0] += control
                            working_list[0].handle_right[0] += control
                            working_list[0].handle_left[0] += control
                        del working_list[0]

                elif control < 0:
                    while len(working_list):
                        if working_list[0].co[0] == 0.0:
                            working_list[0].co[0] = 0.0

                        else:
                            working_list[0].co[0] += control
                            working_list[0].handle_right[0] += control
                            working_list[0].handle_left[0] += control

                        del working_list[0]

            # ============ If there is no selected keyframe ==============
            else:
                # ======= getting list based on frame position ===========

                working_list2 = []

                if initial_time_frame in keyframe_list_compare:
                    first_key_index = keyframe_list_compare.index(initial_time_frame)

                    working_list2.extend([keyframe for keyframe in all_keyframes[first_key_index:]])

                else:
                    bpy.ops.screen.keyframe_jump(next=True)
                    current_time_frame = float(bpy.context.scene.frame_current)

                    first_key_index = keyframe_list_compare.index(current_time_frame)

                    working_list2.extend([keyframe for keyframe in all_keyframes[first_key_index:]])
                # ======================= Body ==========================

                if control > 0:
                    working_list2.reverse()
                    
                    while len(working_list2) > 0:
                        if working_list2[-1].co[0] == 0.0:
                            if len(working_list2) == 1:
                                working_list2[0].co[0] = 0.0
                                # del working_list[0]
                            else:
                                working_list2[0].co[0] += control
                                working_list2[0].handle_right[0] += control
                                working_list2[0].handle_left[0] += control
                                # del working_list[0]

                        else:
                            working_list2[0].co[0] += control
                            working_list2[0].handle_right[0] += control
                            working_list2[0].handle_left[0] += control
                        del working_list2[0]

                elif control < 0:
                    while len(working_list2) > 0:
                        if working_list2[0].co[0] == 0.0:
                            working_list2[0].co[0] = 0.0
                        else:
                            working_list2[0].co[0] = working_list2[0].co[0] + control
                            working_list2[0].handle_right[0] += control
                            working_list2[0].handle_left[0] += control
                        del working_list2[0]

        bpy.context.scene.frame_set(im_sick_of_this)


def keyframe_nudge(usr_inp):
    selected = bpy.context.selected_objects

    control = usr_inp

    for obj in selected:
        anim = obj.animation_data

        for fc in anim.action.fcurves:
            # =============== Selected Keyframes ==================
            selected_keyframes = [keyframe for keyframe in fc.keyframe_points if keyframe.select_control_point]
            # ===============   Process   =========================
            #                     |
            if len(selected_keyframes) > 1:
                if control > 0:
                    selected_keyframes.reverse()
                    while len(selected_keyframes) > 0:
                        selected_keyframes[0].co[0] += control
                        selected_keyframes[0].handle_right[0] += control
                        selected_keyframes[0].handle_left[0] += control

                        del selected_keyframes[0]

                elif control < 0:
                    while len(selected_keyframes) > 0:
                        selected_keyframes[0].co[0] += control
                        selected_keyframes[0].handle_right[0] += control
                        selected_keyframes[0].handle_left[0] += control

                        del selected_keyframes[0]


            elif len(selected_keyframes) == 1:
                selected_keyframes[0].co[0] += control
                selected_keyframes[0].handle_right[0] += control
                selected_keyframes[0].handle_left[0] += control
            else:
                print('No Keyframes Selected')


def hold_keyframe_for(usr_inp):
    selected = bpy.context.selected_objects

    control = usr_inp

    for obj in selected:
        anim = obj.animation_data

        for fc in anim.action.fcurves:
            # ==================== Full Keyframe List ======================
            #empty for now

            # ==================== Selected Keyframes ======================
            selected_keyframes = [keyframe for keyframe in fc.keyframe_points if keyframe.select_control_point]

            # ==================== Non Selected Keyframes ======================
            not_selected_keyframes = [keyframe for keyframe in fc.keyframe_points if
                                      keyframe.select_control_point == False and keyframe.co[0] >
                                      selected_keyframes[-1].co[0]]

            # ================== Push Away Non Selected Keyframes ===============
            if len(not_selected_keyframes) > 0:
                not_selected_keyframes.reverse()
                for nsk in not_selected_keyframes:
                    nsk.co[0] += 300000
                    nsk.handle_left[0] += 300000
                    nsk.handle_right[0] += 300000

            # ==================== Work ======================
            completed_list = []
            while len(selected_keyframes) > 0:


                if len(selected_keyframes) > 2:
                    # ==================== Finding data for the keyframe to be moved ========================
                    current_distance = selected_keyframes[1].co[0] - selected_keyframes[0].co[0]
                    to_move = control - current_distance
                    projection = selected_keyframes[1].co[0] + to_move

                    projected_frame_to_move_distance_to_next = selected_keyframes[2].co[0] - projection


                    if projected_frame_to_move_distance_to_next > 0:
                        selected_keyframes[1].co[0] += to_move
                        selected_keyframes[1].handle_left[0] += to_move
                        selected_keyframes[1].handle_right[0] += to_move


                    elif projected_frame_to_move_distance_to_next <= 0:

                        friendly_fire_initial_distance = selected_keyframes[2].co[0] - selected_keyframes[1].co[0]
                        push_next_by = friendly_fire_initial_distance + abs(projected_frame_to_move_distance_to_next)


                        # ======= Create a new list of remaining keyframes and reverse them========
                        unprocessed_keyframes = [k for k in selected_keyframes[2:]]
                        unprocessed_keyframes.reverse()


                        while len(unprocessed_keyframes) > 0:
                            unprocessed_keyframes[0].co[0] += push_next_by
                            unprocessed_keyframes[0].handle_left[0] += push_next_by
                            unprocessed_keyframes[0].handle_right[0] += push_next_by

                            unprocessed_keyframes.pop(0)

                        selected_keyframes[1].co[0] += to_move
                        selected_keyframes[1].handle_left[0] += to_move
                        selected_keyframes[1].handle_right[0] += to_move

                if len(selected_keyframes) == 2:  # <-----if there are only 2 keyframes selected or left in list

                    distance_case_2 = selected_keyframes[1].co[0] - selected_keyframes[0].co[0]
                    to_move = control - distance_case_2
                    if distance_case_2 > control:
                        to_move_case_2 = control - distance_case_2
                        selected_keyframes[1].co[0] += to_move_case_2
                        selected_keyframes[1].handle_left[0] += to_move_case_2
                        selected_keyframes[1].handle_right[0] += to_move_case_2
                    else:
                        selected_keyframes[1].co[0] += to_move
                        selected_keyframes[1].handle_left[0] += to_move
                        selected_keyframes[1].handle_right[0] += to_move

                if len(selected_keyframes) == 1:  # <------ if there is only one keyframe selected or left in list
                    selected_keyframes[0].co[0] = selected_keyframes[0].co[0]

                completed_list.append(selected_keyframes.pop(0))


            # =========== Bring Back Not Selected ========
            if len(not_selected_keyframes) > 0:
                not_selected_keyframes.reverse()
                distance_from_last_selected = not_selected_keyframes[0].co[0] - completed_list[-1].co[0]
                push_back_non_selected_by = control - distance_from_last_selected

                for nsk in not_selected_keyframes:
                    nsk.co[0] += push_back_non_selected_by
                    nsk.handle_left[0] += push_back_non_selected_by
                    nsk.handle_right[0] += push_back_non_selected_by


def come_over_here_nudge():
    selected = bpy.context.selected_objects

    for obj in selected:
        anim = obj.animation_data

        #========= Get initial data and define global variables ==============
        fc = [fc for fc in anim.action.fcurves]
        time_position = bpy.context.scene.frame_current
        if_missing_keyframe = []

        # ====== get selected keyframe frame position =========
        for fcurve in fc:

            if not fcurve.hide:
                selected_keyframes = [keyframe for keyframe in fcurve.keyframe_points if keyframe.select_control_point]
                try:
                    if_missing_keyframe.append(selected_keyframes[0].co[0])
                except:
                    pass

        #============= Create keyframe employment list =========
        for fcurve in fc:

            allKeyframes = [keyframe for keyframe in fcurve.keyframe_points]
            keyframe_querry_list = [keyframe.co[0] for keyframe in allKeyframes]
            employed_keyframes_list = []

            try:
                if if_missing_keyframe[0] in keyframe_querry_list:
                    start_index = keyframe_querry_list.index(if_missing_keyframe[0])
                    employed_keyframes_list = [keyframe for keyframe in allKeyframes[start_index:]]
                else:
                    start_index = bisect(keyframe_querry_list,if_missing_keyframe[0])
                    employed_keyframes_list = [keyframe for keyframe in allKeyframes[start_index:]]
            except:
                print('Exceptin!')

            #========== keyframe job assingment =========
            distance_to_time = time_position - if_missing_keyframe[0]
            to_move = distance_to_time

            if to_move > 0:
                while employed_keyframes_list:
                    employed_keyframes_list.reverse()
                    employed_keyframes_list[0].co[0] += to_move
                    employed_keyframes_list[0].handle_left[0] += to_move
                    employed_keyframes_list[0].handle_right[0] += to_move
                    del employed_keyframes_list[0]
            else:
                while employed_keyframes_list:
                    employed_keyframes_list[0].co[0] += to_move
                    employed_keyframes_list[0].handle_left[0] += to_move
                    employed_keyframes_list[0].handle_right[0] += to_move
                    del employed_keyframes_list[0]




#=============== Operators ====================
#                   |
class KFN_OT_Insert_empty_Frame(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "nudge.kfn_ot_insert_empty_frame"
    bl_label = "Insert Empty Frame Nudge"
    
    insert_input = bpy.props.FloatProperty(name="Some Floating Point")

    def execute(self, context):
        insert_input = self.insert_input
        insert_empty_frame(insert_input)
        return {'FINISHED'}


class KFN_OT_Keyframe_Nudge(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "nudge.kfn_ot_keyframe_nudge"
    bl_label = "Keyframe Nudge"

    nudge_input : bpy.props.FloatProperty(name="Some Floating Point", default=0.0)

    def execute(self, context):
        nudge_input = self.nudge_input
        keyframe_nudge(nudge_input)
        return {'FINISHED'}


class KFN_OT_Hold_Keyframe_For(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "nudge.kfn_ot_hold_for"
    bl_label = "Set Keyframe On x frames"

    nudge_input : bpy.props.IntProperty(name='Set keyframe on - driver',default=1,min=1)

    def execute(self, context):
        nudge_input = self.nudge_input
        hold_keyframe_for(nudge_input)
        return {'FINISHED'}


class KFN_OT_Come_Over_Here(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "nudge.kfn_ot_come_over_here"
    bl_label = "Push/Pull to current frame"


    def execute(self, context):
        come_over_here_nudge()
        return {'FINISHED'}

#============== UI Panel ====================
#                 |
class KFN_PT_Keyframe_Nudge_Panel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Keyframe Nudge"
    bl_idname = "KFN_PT_simple"
    bl_space_type = 'DOPESHEET_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'Nudge_keyframes'

    bpy.types.Scene.nudge_driver : bpy.props.IntProperty(default=2,min=1,max=24)


    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.label(text=' Push/Pull ')
        row.label(text=' By Frames')
        row.label(text=' Nudge')

        row = layout.row()
        row_col = row.column(align=True)
        row_col.scale_y = 2
        row_col.operator('nudge.kfn_ot_insert_empty_frame',text= '+').insert_input = context.scene.nudge_driver
        row_col.operator('nudge.kfn_ot_insert_empty_frame',text= '-').insert_input = int("-" + str(context.scene.nudge_driver))

        row_col = row.column(align=True)
        row_col.scale_x = 1
        row_col.scale_y = 4
        row_col.prop(context.scene,'nudge_driver',text='')

        row_col = row.column(align=True)
        row_col.scale_x = 1
        row_col.scale_y = 2
        row_col.operator('nudge.kfn_ot_keyframe_nudge', text='+').nudge_input = context.scene.nudge_driver
        row_col.operator('nudge.kfn_ot_keyframe_nudge', text='-').nudge_input = int("-" + str(context.scene.nudge_driver))

        row = layout.row()
        row.operator('nudge.kfn_ot_come_over_here', text='Come Over')
        row.operator('nudge.kfn_ot_hold_for',text='Hold For').nudge_input = context.scene.nudge_driver
        row.label(text='')

classes = (
    KFN_OT_Insert_empty_Frame,
    KFN_OT_Keyframe_Nudge,
    KFN_OT_Hold_Keyframe_For,
    KFN_OT_Come_Over_Here,
    KFN_PT_Keyframe_Nudge_Panel)

register, unregister = bpy.utils.register_classes_factory(classes)

if __name__ == "__main__":
    register()
