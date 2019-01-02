bl_info = {
    "name" : "Keyframe Nudge",
    "author" : "blenderID:okuma_10",
    "version" : (0, 3, 5),
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
    control = usr_inp
    print('{:=^40}'.format(' START '))
    for obj in selected:
        anim = obj.animation_data
        fcurves = [fc for fc in anim.action.fcurves]
        time_position = bpy.context.scene.frame_current
        if_selected_keyframes = []
        all_keyframes = []


        # ============== find selected keyframes(position) ============
        for fc in fcurves:
            selected_keyframe = [keyframe.co[0] for keyframe in fc.keyframe_points if keyframe.select_control_point]
            fc_all_keyframes = [keyframe for keyframe in fc.keyframe_points]
            try:
                all_keyframes.extend(fc_all_keyframes)
                if_selected_keyframes.extend(selected_keyframe)
            except:
                pass
        if_selected_keyframes = list(set(if_selected_keyframes))
        if_selected_keyframes.sort()

        #======================= second run ===========================

        #==================== create employee list ====================
        all_keyframes_numerate = [keyframe.co[0] for keyframe in all_keyframes]
        all_keyframes_list = list(zip(all_keyframes_numerate,all_keyframes))
        all_keyframes_list.sort(key=lambda x: x[0])
        all_keyframes_list_querry = [x for x,y in all_keyframes_list]

        employee_list = []

        #================= if we have selected keyframes ==============
        if if_selected_keyframes:
            try:
                if if_selected_keyframes[0] in all_keyframes_list_querry:
                    start_index = all_keyframes_list_querry.index(if_selected_keyframes[0])
                    employee_list.extend(all_keyframes_list[start_index:])

            except:
                print('{:!<40}'.format(' EXCEPTION  '))
        #=============== if we don't have selected keyframes ==========
        else:
            if time_position in all_keyframes_list_querry:
                start_index = all_keyframes_list_querry.index(time_position)
                employee_list.extend(all_keyframes_list[start_index:])

            else:
                start_index = bisect(all_keyframes_list_querry,time_position)
                employee_list.extend(all_keyframes_list[start_index:])

        #================ Employee job assingment ===============

        if control > 0:
            employee_list.reverse()

            while employee_list:
                action_list = [keyframe for frame,keyframe in employee_list]
                print(action_list[0].co[0])
                if action_list[0].co[0] == 0.0:
                    print('keyframe 0')
                    action_list[0].co[0] = 0.0

                else:
                    action_list[0].co[0] += control
                    action_list[0].handle_left[0] += control
                    action_list[0].handle_right[0] += control

                del employee_list[0]

        else:
            while employee_list:
                action_list = [keyframe for frame, keyframe in employee_list]
                if action_list[0].co[0] == 0.0:
                    action_list[0].co[0] = 0.0

                else:
                    action_list[0].co[0] += control
                    action_list[0].handle_left[0] += control
                    action_list[0].handle_right[0] += control

                del employee_list[0]


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
        print('{:=^40}'.format(' START '))

        anim = obj.animation_data
        fcurves = [fc for fc in anim.action.fcurves]
        keyframes_list = []
        non_selected_keyframes = []
        all_keyframes_global = []

        # ============ Getting list of the frames that we have keyframes for - globaly ==================================
        for fc in fcurves:
            all_keyframes = [keyframe.co[0] for keyframe in fc.keyframe_points] #<--hitchhikes this itteration
            fc_selected_keyframes = [keyframe.co[0] for keyframe in fc.keyframe_points if keyframe.select_control_point]
            try:
                keyframes_list.extend(fc_selected_keyframes)
                all_keyframes_global.extend(all_keyframes)
            except:
                pass
        keyframes_list = list(set(keyframes_list)) #<----- remove duplicates
        all_keyframes_global = list(set(all_keyframes_global))
        all_keyframes_global.sort()

        #============ Creating list of frame/keyframe tuples of non selected keyframes after selected ====================
        last_index = all_keyframes_global.index(keyframes_list[-1])
        non_selected_keyframes = [keyframe for keyframe in all_keyframes_global[last_index+1:]]
        avoiding_keyframes = {}
        for key in non_selected_keyframes:
            avoiding_keyframes[key] = []

        for fc in fcurves:
            fc_all_keyframes = [keyframe for keyframe in fc.keyframe_points]
            for keyframe in fc_all_keyframes:
                if keyframe.co[0] in avoiding_keyframes.keys():
                    avoiding_keyframes[keyframe.co[0]].append(keyframe)

        avoiding_keyframes_list = [(k,v) for k,v in avoiding_keyframes.items()]
        avoiding_keyframes_list.sort() #<---------------- we now have a workable frame/list of keyframes to push away

        # =========== Creating dictionary of emploied keyframes at the keyframes_list keyframes ==========================
        emploied_keyframes = {}
        for key in keyframes_list:
            emploied_keyframes[key] = []

        for fc in fcurves:
            fc_selected_keyframes = [keyframe for keyframe in fc.keyframe_points if keyframe.select_control_point]
            for keyframe in fc_selected_keyframes:
                if keyframe.co[0] in emploied_keyframes.keys():
                    emploied_keyframes[keyframe.co[0]].append(keyframe)

        emploied_keyframes_list = [(k,v) for k,v in emploied_keyframes.items()]
        emploied_keyframes_list.sort() #<------------------------ we now have workable frame/list of keyframes to work with!

        #===================== Creating keyframe frame/projection tuple list ==============================================
        keyframes_list.sort()
        completed_list = []
        projection = 0.0
        projected_list = []
        projected_list.append(keyframes_list[0])
        while keyframes_list:
            if len(keyframes_list)>1:
                try:
                    current_distance = keyframes_list[1] - projected_list[-1]
                except:
                    print('exception occured!!')

                to_move = control - current_distance
                projection = keyframes_list[1] + to_move


            elif len(keyframes_list) == 1: #at the end there is duplication of the last frame projection,this avoids it
                break

            projected_list.append(projection)

            completed_list.append(keyframes_list.pop(0))
        completed_list.append(keyframes_list.pop(0)) #<------get last number

        projection_coordinates = list(zip(completed_list,projected_list)) #<---- we now have tuple list with keyframe's frame
                                                                                                     #  and it's new position
        #=========================== Task asignment to employee list =======================================================
        #====================push away non selected keyframes after last selected keyframe==================================
        captrue_avoiding_keyframes_list = []
        try:
            distance_from_projection = avoiding_keyframes_list[0][0] - projection_coordinates[-1][1]
            new_first_position = projection_coordinates[-1][1] + control
            to_move = new_first_position - avoiding_keyframes_list[0][0]

            if distance_from_projection < 0:
                avoiding_keyframes_list.reverse()
                while avoiding_keyframes_list:
                    for keyframe in avoiding_keyframes_list[0][1]:
                        keyframe.co[0] += to_move
                        keyframe.handle_left[0] += to_move
                        keyframe.handle_right[0] += to_move
                    captrue_avoiding_keyframes_list.append(avoiding_keyframes_list.pop(0))
            else:
                while avoiding_keyframes_list:
                    for keyframe in avoiding_keyframes_list[0][1]:
                        keyframe.co[0] += to_move
                        keyframe.handle_left[0] += to_move
                        keyframe.handle_right[0] += to_move
                    captrue_avoiding_keyframes_list.append(avoiding_keyframes_list.pop(0))
        except:
            pass

        #========================== give the tasks to the employee keyframes ==============================================
        capture_projection_coordinates = []
        while projection_coordinates:
            if projection_coordinates[0][0] == emploied_keyframes_list[0][0]:
                for keyframe in emploied_keyframes_list[0][1]:
                    to_move = projection_coordinates[0][1] - projection_coordinates[0][0]
                    keyframe.co[0] = projection_coordinates[0][1]
                    keyframe.handle_left[0] += to_move
                    keyframe.handle_right[0] += to_move
            capture_projection_coordinates.append(projection_coordinates.pop(0))
            del emploied_keyframes_list[0]


def come_over_here_nudge():
    selected = bpy.context.selected_objects

    for obj in selected:
        anim = obj.animation_data

        print('{:=^40}'.format(' START '))
        # ========= Get initial data and define global variables ==============
        fc = [fc for fc in anim.action.fcurves]
        time_position = bpy.context.scene.frame_current
        all_selected_keyframes = []
        all_keyframes_list = []

        # ====== get selected keyframe frame position =========
        for fcurve in fc:
            all_keyframes = [keyframe.co[0] for keyframe in fcurve.keyframe_points]
            selected_keyframes = [keyframe.co[0] for keyframe in fcurve.keyframe_points if
                                  keyframe.select_control_point]
            try:
                all_selected_keyframes.extend(selected_keyframes)
                all_keyframes_list.extend(all_keyframes)
            except:
                pass

        all_selected_keyframes = list(set(all_selected_keyframes))
        all_selected_keyframes.sort()
        all_keyframes_list = list(set(all_keyframes_list))
        all_keyframes_list.sort()

        # =============== Create all keyframes frame/keyframe list of tuples population =============
        all_keyframes_pos_population = {}
        for key in all_keyframes_list:
            all_keyframes_pos_population[key] = []
        for fcurve in fc:
            fc_all_keys = [keyframe for keyframe in fcurve.keyframe_points]
            for keyframe in fc_all_keys:
                if keyframe.co[0] in all_keyframes_pos_population.keys():
                    all_keyframes_pos_population[keyframe.co[0]].append(keyframe)

        all_keyframes_pos_population_list = [(k, v) for k, v in all_keyframes_pos_population.items()]
        all_keyframes_pos_population_list.sort()

        # ============= Create keyframe employment list =========
        employed_keyframes_list = []
        index = 0
        # while all_selected_keyframes:
        for item in all_keyframes_pos_population_list:
            try:
                if all_selected_keyframes[0] == item[0]:
                    # employed_keyframes_list.extend(item[1])
                    index = all_keyframes_pos_population_list.index(item)
            except:
                print('exception!')
        print(index)
        for item in all_keyframes_pos_population_list[index:]:
            employed_keyframes_list.extend(item[1])
        print(employed_keyframes_list)
        # ============== Getting distance difference =====================
        distance_to_time = time_position - employed_keyframes_list[0].co[0]
        to_move = distance_to_time
        print(distance_to_time)

        # ============== Task assignment to employees =====================
        if to_move > 0:
            employed_keyframes_list.reverse()
            while employed_keyframes_list:
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
