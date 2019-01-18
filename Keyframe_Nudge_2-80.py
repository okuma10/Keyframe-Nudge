bl_info = {
    "name" : "Keyframe Nudge",
    "author" : "blenderID:okuma_10",
    "version" : (0, 4, 1),
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
                if action_list[0].co[0] == 0.0:
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
    # ================================== GET SELECTED OBJECTS ==========================================
    selected_objects = bpy.context.selected_objects

    # ================================ DEFINE GLOBAL VARIABLES =========================================
    control = usr_inp
    Global_all_keyframe_co0 = []  # list of all keyframes 0-coordinates - frame numbers.
    Global_all_selected_keyframes_co0 = []  # list of all selected keyframes 0-coordinates-frames.
    Global_all_keyframes = {}  # dictionary('map') of all keyframes frames/keyframes.
    Global_non_selected_after_selected = []  # list of all frame/keyframe tuples after last
    #                                   selected keyframe.
    employee_list = []  # list of all frame/keyframe tuples to be modified.
    employee_tasks = []  # tuple frame/projection for keyframe position change.
    # ============================= GET ALL INITIAL KEYFRAME DATA ======================================
    for object in selected_objects:
        anim = object.animation_data
        fcurves = [fc for fc in anim.action.fcurves]
        loc_all_keyframe_positions = [keyframe.co[0] for fc in fcurves for keyframe in fc.keyframe_points]
        loc_all_selected_keyframe_positions = [keyframe.co[0] for fc in fcurves for keyframe in fc.keyframe_points if
                                               keyframe.select_control_point]

        # =============================== populate lists ===========================================
        Global_all_keyframe_co0.extend(loc_all_keyframe_positions)
        Global_all_selected_keyframes_co0.extend(loc_all_selected_keyframe_positions)
    # ==================================== CLEAN UP LISTS ==============================================
    Global_all_keyframe_co0 = list(set(Global_all_keyframe_co0))
    Global_all_selected_keyframes_co0 = list(set(Global_all_selected_keyframes_co0))
    Global_all_keyframe_co0.sort()
    Global_all_selected_keyframes_co0.sort()

    # =============================== PREPARE ALL KEYFRAMES MAP ========================================
    for frame in Global_all_keyframe_co0:
        Global_all_keyframes[frame] = []

    # =============================== POPULATE ALL KEYFRAME MAP ========================================
    for object in selected_objects:
        anim = object.animation_data
        fcurves = [fc for fc in anim.action.fcurves]
        local_all_keyframes = [keyframe for fc in fcurves for keyframe in fc.keyframe_points]

        # ============================ append keyframes to map =====================================
        for keyframe in local_all_keyframes:
            if keyframe.co[0] in Global_all_keyframes.keys():
                Global_all_keyframes[keyframe.co[0]].append(keyframe)
            else:
                pass

    # ========================= CONVERT MAP TO FRAME/KEYFRAME TUPLE LIST ===============================
    Global_all_keyframes = [(k, v) for k, v in Global_all_keyframes.items()]
    Global_all_keyframes.sort()

    # ======================== CREATE NON SELECTED AFTER LAST SELECTED LIST ============================
    last_selected_index = Global_all_keyframe_co0.index(Global_all_selected_keyframes_co0[-1])
    Global_non_selected_after_selected.extend(Global_all_keyframes[last_selected_index + 1:])
    # ================================= CREATE EMPLOYEE LIST ===========================================
    first_selected_index = Global_all_keyframe_co0.index(Global_all_selected_keyframes_co0[0])
    employee_list = Global_all_keyframes[first_selected_index:last_selected_index + 1]

    # ======================= CREATE PROJECTION FRAME/PROJECTION TUPLE LIST ============================
    employee_pos = [item[0] for item in employee_list]
    temp_list = []
    projection = []
    while employee_pos:
        distance = 0
        temp_projection = 0
        to_move = 0
        try:
            if len(projection) == 0:
                projection.append(employee_pos[0])
                temp_list.append(employee_pos.pop(0))
            if len(projection) == 1:
                distance = employee_pos[0] - projection[0]
                to_move = control - (distance)
                temp_projection = employee_pos[0] + to_move
                projection.append(temp_projection)
                temp_list.append(employee_pos.pop(0))
            if len(projection) > 1:
                distance = employee_pos[0] - projection[-1]
                to_move = control - (distance)
                temp_projection = employee_pos[0] + to_move
                projection.append(temp_projection)
                temp_list.append(employee_pos.pop(0))
        except:
            print('Exception')

    employee_pos.extend(temp_list)
    temp_list.clear()
    employee_tasks = [(f, p) for f, p in zip(employee_pos, projection)]

    # ======================== MOVE NON SELECTED AFTER SELECTED KEYFEAMES ===============================
    try:
        distance = Global_non_selected_after_selected[0][0] - employee_tasks[-1][1]
        to_move = control - (distance)
        while Global_non_selected_after_selected:
            if control > 0:
                Global_non_selected_after_selected.reverse()
                for keyframe in Global_non_selected_after_selected[0][1]:
                    keyframe.co[0] += to_move
                    keyframe.handle_left[0] += to_move
                    keyframe.handle_right[0] += to_move
                temp_list.append(Global_non_selected_after_selected.pop(0))
            else:
                for keyframe in Global_non_selected_after_selected[0][1]:
                    keyframe.co[0] += to_move
                    keyframe.handle_left[0] += to_move
                    keyframe.handle_right[0] += to_move
                temp_list.append(Global_non_selected_after_selected.pop(0))
    except:
        print('All keyframes are selected')
    # =============================== ASSIGN PROJECTION TO EMPLOYEES =====================================
    while employee_list:
        move_handle = employee_tasks[0][1] - employee_tasks[0][0]

        for keyframe in employee_list[0][1]:
            keyframe.co[0] = employee_tasks[0][1]
            keyframe.handle_left[0] += move_handle
            keyframe.handle_right[0] += move_handle
        del employee_tasks[0]
        del employee_list[0]


def come_over_here_nudge():
    # ========================== GET SELECTED OBJECTS ===========================
    selected_objects = bpy.context.selected_objects

    # ========================= DEFINE GLOBAL VARIABLES =========================
    Global_keyframe_positions = []  # list of frames that we have keyframes on
    Global_all_keyframes = {}  # dictionary map of all keyframes based on their frame position
    Global_all_selected_keyframes = []  # list of all selected keyframes's frame positions
    current_timeline_position = bpy.context.scene.frame_current  # get current time position
    employe_list = []  # list of all keyframes that will be modified

    # ======================= GET KEYFRAME FRAME POSITIONS ======================
    for object in selected_objects:
        anim = object.animation_data
        fcurves = [fcurve for fcurve in anim.action.fcurves]
        all_keyframes = [keyframe.co[0] for fc in fcurves for keyframe in fc.keyframe_points]
        all_selected_keyframes = [keyframe.co[0] for fc in fcurves for keyframe in fc.keyframe_points if
                                  keyframe.select_control_point]

        Global_all_selected_keyframes.extend(all_selected_keyframes)
        Global_keyframe_positions.extend(all_keyframes)

    # =============================== CLEAN UP LISTS =================================
    Global_keyframe_positions = list(set(Global_keyframe_positions))
    Global_keyframe_positions.sort()

    Global_all_selected_keyframes = list(set(Global_all_selected_keyframes))
    Global_all_selected_keyframes.sort()

    # ==================== PEPARE DICTIONARY MAP OF ALL KEYFRAMES ====================
    for frame in Global_keyframe_positions:
        Global_all_keyframes[frame] = []
    # ================================= POPULATE MAP =================================
    for object in selected_objects:
        anim = object.animation_data
        fcurves = [fcurve for fcurve in anim.action.fcurves]
        all_keyframes = [keyframe for fc in fcurves for keyframe in fc.keyframe_points]

        for keyframe in all_keyframes:
            if keyframe.co[0] in Global_all_keyframes.keys():
                Global_all_keyframes[keyframe.co[0]].append(keyframe)

    # ================= CONVERT MAP TO LIST OF TUPLES (frame/keyframes) ================
    Global_all_keyframes = [(k, v) for k, v in Global_all_keyframes.items()]
    Global_all_keyframes.sort()

    # ========================= CREATE EMPLOYE LIST ===================================
    first_selected_index = 0
    for item in Global_all_keyframes:
        if Global_all_selected_keyframes[0] == item[0]:
            first_selected_index = Global_all_keyframes.index(item)
    employe_list.extend(Global_all_keyframes[first_selected_index:])

    # ====================== GET DISTANCE TO TIME POSITION ============================
    distance = current_timeline_position - Global_all_selected_keyframes[0]  # this can be used directly for moving

    # ========================== EMPLOYE JOB ASSIGNMENT ===============================
    if distance > 0:
        employe_list.reverse()
        while employe_list:
            for keyframe in employe_list[0][1]:
                keyframe.co[0] += distance
                keyframe.handle_left[0] += distance
                keyframe.handle_right[0] += distance
            del employe_list[0]
    else:
        while employe_list:
            for keyframe in employe_list[0][1]:
                keyframe.co[0] += distance
                keyframe.handle_left[0] += distance
                keyframe.handle_right[0] += distance
            del employe_list[0]


def add_inbetween(inputpercent):
    def get_next_closest(inplist,query):
        next_closest = min([n for n in inplist if n > query])
        return next_closest
    def get_previous_closest(inplist,query):
        previous_closest = max([n for n in inplist if n<query])
        return previous_closest
    def get_value(min_val,max_val,percent):
        out_value = (percent * (max_val - min_val)) + min_val
        return out_value

    percent = inputpercent
    selected = bpy.context.selected_objects
    current_time = bpy.context.scene.frame_current
    for object in selected:
        anim = object.animation_data
        fcurves = [fcurve for fcurve in anim.action.fcurves]
        for fcurve in fcurves:
            if fcurve.hide == False:
                all_keyframes_querry = [keyframe.co[0] for keyframe in fcurve.keyframe_points]
                all_keyframes = [keyframe for keyframe in fcurve.keyframe_points]
                selected_keyframes = [keyframe for keyframe in fcurve.keyframe_points if keyframe.select_control_point]

                next_key = get_next_closest(all_keyframes_querry, current_time)
                next_index = all_keyframes_querry.index(next_key)
                previous_key = get_previous_closest(all_keyframes_querry, current_time)
                previous_index = all_keyframes_querry.index(previous_key)

                #==========================   IF WE HAVE ONE KEYFRAME SELECTED PER FCURVE ================================
                if len(selected_keyframes) == 1:

                    inbetween_co1 = get_value(all_keyframes[previous_index].co[1], all_keyframes[next_index].co[1], percent)
                    selected_index = all_keyframes_querry.index(selected_keyframes[0].co[0])

                    # y = mx + c     # find a parallel line to prev-next keyframe line passing trough the new keyframe.co
                    m = (all_keyframes[previous_index].co[1] - all_keyframes[next_index].co[1]) / (all_keyframes[previous_index].co[0] - all_keyframes[next_index].co[0])  # m = (y1-y2)/(x1-x2)
                    c = all_keyframes[selected_index].co[1] - m * all_keyframes[selected_index].co[0]
                    handle_left_co = []
                    handle_right_co = []
                    # ===================================== HANDLE LEFT CO ========================================================================
                    h_left_x = ((all_keyframes[selected_index].co[0] - all_keyframes[previous_index].co[0]) * 0.75) + all_keyframes[previous_index].co[0]
                    handle_left_co.append(h_left_x)
                    h_left_y = (m * h_left_x) + c
                    handle_left_co.append(h_left_y)
                    # ==================================== HANDLE RIGHT CO =======================================================================
                    h_right_x = ((all_keyframes[next_index].co[0] - all_keyframes[selected_index].co[0]) * 0.25) + all_keyframes[selected_index].co[0]
                    handle_right_co.append(h_right_x)
                    h_right_y = (m * h_right_x) + c
                    handle_right_co.append(h_right_y)

                    # ================================== MANIPULATE KEYFRAME ===============================================
                    all_keyframes[selected_index].co[1] = inbetween_co1
                    all_keyframes[selected_index].handle_left[0] = float(handle_left_co[0])
                    all_keyframes[selected_index].handle_left[1] = float(handle_left_co[1])
                    all_keyframes[selected_index].handle_right[0] = float(handle_right_co[0])
                    all_keyframes[selected_index].handle_right[1] = float(handle_right_co[1])


                elif len(selected_keyframes) == 2:
                    pass

                elif len(selected_keyframes)>2:
                    break

                # ================================ IF WE HAVE NO KEYFRAME SELECTED =========================================
                else:
                    next_key = get_next_closest(all_keyframes_querry,current_time)
                    next_index = all_keyframes_querry.index(next_key)
                    previous_key = get_previous_closest(all_keyframes_querry,current_time)
                    previous_index = all_keyframes_querry.index(previous_key)
                    inbetween_co0 = ((all_keyframes[next_index].co[0] - all_keyframes[previous_index].co[0])/2)+all_keyframes[previous_index].co[0]
                    inbetween_co1 = get_value(all_keyframes[previous_index].co[1],all_keyframes[next_index].co[1],percent)

                # ===================================== FIND HANDLES CO ====================================================

                    # y = mx + c     # find a parallel line to prev-next keyframe line passing trough the new keyframe.co
                    m = (all_keyframes[previous_index].co[1] - all_keyframes[next_index].co[1]) / (all_keyframes[previous_index].co[0] - all_keyframes[next_index].co[0])  # m = (y1-y2)/(x1-x2)
                    c = inbetween_co1 - m * inbetween_co0
                    handle_left_co = []
                    handle_right_co = []
                    # ===================================== HANDLE LEFT CO ========================================================================
                    h_left_x = ((inbetween_co0 - all_keyframes[previous_index].co[0]) * 0.75) + all_keyframes[previous_index].co[0]
                    handle_left_co.append(h_left_x)
                    h_left_y = (m * h_left_x) + c
                    handle_left_co.append(h_left_y)
                    # ==================================== HANDLE RIGHT CO =======================================================================
                    h_right_x = ((all_keyframes[next_index].co[0] - inbetween_co0) * 0.25) + inbetween_co0
                    handle_right_co.append(h_right_x)
                    h_right_y = (m * h_right_x) + c
                    handle_right_co.append(h_right_y)

                    bpy.context.scene.frame_set(inbetween_co0)
                    new_key = fcurve.keyframe_points.insert(inbetween_co0,inbetween_co1, options={'FAST'})
                    new_key.handle_right[0] = h_right_x
                    new_key.handle_right[1] = h_right_y
                    new_key.handle_left[0] = h_left_x
                    new_key.handle_left[1] = h_left_y
                    fcurve.update()



#=============== Operators ====================
#                   |
class KFN_OT_Insert_empty_Frame(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "nudge.kfn_ot_insert_empty_frame"
    bl_label = "Insert Empty Frame Nudge"
    
    insert_input : bpy.props.FloatProperty(name="Some Floating Point")

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


class KFN_OT_Add_Inbetween(bpy.types.Operator):

    bl_idname = "nudge.kfn_ot_add_inbetween"
    bl_label = "Add Inbetween"

    user_input = bpy.props.FloatProperty()

    def execute(self,context):
        user_input = self.user_input
        add_inbetween(user_input)
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

    def update_inbetween(self,context):
        percent = self.slider
        bpy.ops.nudge.kfn_ot_add_inbetween(user_input=percent)

    bpy.types.Scene.slider =  bpy.props.FloatProperty(name="inbetween",min=0,max=1, update=update_inbetween)
    bpy.types.Scene.nudge_driver = bpy.props.IntProperty(default=2,min=1,max=24)


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

        row = layout.row()
        row.prop(context.scene, 'slider', slider=True)

classes = (
    KFN_OT_Insert_empty_Frame,
    KFN_OT_Keyframe_Nudge,
    KFN_OT_Hold_Keyframe_For,
    KFN_OT_Come_Over_Here,
    KFN_OT_Add_Inbetween,
    KFN_PT_Keyframe_Nudge_Panel)

register, unregister = bpy.utils.register_classes_factory(classes)

if __name__ == "__main__":
    register()
