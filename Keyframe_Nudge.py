bl_info = {
    "name" : "Keyframe Nudge",
    "author" : "blenderID:okuma_10",
    "version" : (0, 3, 6),
    "location" : "Graph Editor > N - hotkey ",
    "description" : "Various automate keyframe manipulation scripts",
    "support" : "COMMUNITY",
    "category": "Animation",
}
#=============== Imports ======================
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
    #================================== GET SELECTED OBJECTS ==========================================
    selected_objects = bpy.context.selected_objects

    #================================ DEFINE GLOBAL VARIABLES =========================================
    control = usr_inp
    Global_all_keyframe_co0 = []                 # list of all keyframes 0-coordinates - frame numbers.
    Global_all_selected_keyframes_co0 = []       # list of all selected keyframes 0-coordinates-frames.
    Global_all_keyframes = {}                    # dictionary('map') of all keyframes frames/keyframes.
    Global_non_selected_after_selected = []      # list of all frame/keyframe tuples after last
                                                 #                                   selected keyframe.
    employee_list = []                           # list of all frame/keyframe tuples to be modified.
    employee_tasks = []                          # tuple frame/projection for keyframe position change.
    #============================= GET ALL INITIAL KEYFRAME DATA ======================================
    for object in selected_objects:
        anim = object.animation_data
        fcurves = [fc for fc in anim.action.fcurves]
        loc_all_keyframe_positions = [keyframe.co[0] for fc in fcurves for keyframe in fc.keyframe_points]
        loc_all_selected_keyframe_positions = [keyframe.co[0] for fc in fcurves for keyframe in fc.keyframe_points if keyframe.select_control_point]

        #=============================== populate lists ===========================================
        Global_all_keyframe_co0.extend(loc_all_keyframe_positions)
        Global_all_selected_keyframes_co0.extend(loc_all_selected_keyframe_positions)
    #==================================== CLEAN UP LISTS ==============================================
    Global_all_keyframe_co0 = list(set(Global_all_keyframe_co0))
    Global_all_selected_keyframes_co0 = list(set(Global_all_selected_keyframes_co0))
    Global_all_keyframe_co0.sort()
    Global_all_selected_keyframes_co0.sort()

    #=============================== PREPARE ALL KEYFRAMES MAP ========================================
    for frame in Global_all_keyframe_co0:
        Global_all_keyframes[frame] = []

    #=============================== POPULATE ALL KEYFRAME MAP ========================================
    for object in selected_objects:
        anim = object.animation_data
        fcurves = [fc for fc in anim.action.fcurves]
        local_all_keyframes = [keyframe for fc in fcurves for keyframe in fc.keyframe_points]

        #============================ append keyframes to map =====================================
        for keyframe in local_all_keyframes:
            if keyframe.co[0] in Global_all_keyframes.keys():
                Global_all_keyframes[keyframe.co[0]].append(keyframe)
            else: pass

    #========================= CONVERT MAP TO FRAME/KEYFRAME TUPLE LIST ===============================
    Global_all_keyframes = [(k,v) for k,v in Global_all_keyframes.items()]
    Global_all_keyframes.sort()

    #======================== CREATE NON SELECTED AFTER LAST SELECTED LIST ============================
    last_selected_index = Global_all_keyframe_co0.index(Global_all_selected_keyframes_co0[-1])
    Global_non_selected_after_selected.extend(Global_all_keyframes[last_selected_index+1:])
    #================================= CREATE EMPLOYEE LIST ===========================================
    first_selected_index = Global_all_keyframe_co0.index(Global_all_selected_keyframes_co0[0])
    employee_list = Global_all_keyframes[first_selected_index:last_selected_index+1]

    #======================= CREATE PROJECTION FRAME/PROJECTION TUPLE LIST ============================
    employee_pos = [item[0] for item in employee_list ]
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
    employee_tasks = [(f,p) for f,p in zip(employee_pos,projection)]

    #======================== MOVE NON SELECTED AFTER SELECTED KEYFEAMES ===============================
    try:
        distance =  Global_non_selected_after_selected[0][0] - employee_tasks[-1][1]
        to_move = control - (distance)
        while Global_non_selected_after_selected:
            if control > 0 :
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
    #=============================== ASSIGN PROJECTION TO EMPLOYEES =====================================
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

    # ================= CONVERT MAP TO LIST OF TUPLES (frame/keyframe) ================
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


#=============== Operators ====================
#                   |
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


class Hold_Keyframe_For(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "nudge.hold_for"
    bl_label = "Set Keyframe On x frames"

    nudge_input = bpy.props.IntProperty(name='Set keyframe on - driver',default=1,min=1)

    def execute(self, context):
        nudge_input = self.nudge_input
        hold_keyframe_for(nudge_input)
        return {'FINISHED'}


class Come_Over_Here(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "nudge.come_over_here"
    bl_label = "Push/Pull to current frame"


    def execute(self, context):
        come_over_here_nudge()
        return {'FINISHED'}

#============== UI Panel ====================
#                 |
class Keyframe_Nudge_Panel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Keyframe Nudge"
    bl_idname = "KEYFRAME_NGE_simple"
    bl_space_type = 'DOPESHEET_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'Nudge_keyframes'

    bpy.types.Scene.nudge_driver = bpy.props.IntProperty(default=2,min=1,max=24)


    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.scale_y = 0.3
        row.label(' Push/Pull ')
        row.label(' By Frames')
        row.label(' Nudge')

        row = layout.row()

        row_col = row.column(align=True)
        row_col.scale_y = 2
        row_col.scale_x = 2
        row_col.operator('nudge.insert_empty_frame',text = '+').insert_input = context.scene.nudge_driver
        row_col.operator('nudge.insert_empty_frame',text = '-').insert_input = int("-" + str(context.scene.nudge_driver))

        row_col = row.column(align=True)
        row_col.scale_x = 2
        row_col.scale_y = 4
        row_col.prop(context.scene,'nudge_driver',text='')

        row_col = row.column(align=True)
        row_col.scale_x = 2
        row_col.scale_y = 2
        row_col.operator('nudge.keyframe_nudge', text='+').nudge_input = context.scene.nudge_driver
        row_col.operator('nudge.keyframe_nudge', text='-').nudge_input = int("-" + str(context.scene.nudge_driver))

        row = layout.row()
        row.operator('nudge.come_over_here', text='Come Over')
        row.operator('nudge.hold_for',text='Hold For').nudge_input = context.scene.nudge_driver
        row.label(text='')

def register():
    bpy.utils.register_class(Insert_empty_Frame)
    bpy.utils.register_class(Keyframe_Nudge)
    bpy.utils.register_class(Hold_Keyframe_For)
    bpy.utils.register_class(Come_Over_Here)
    bpy.utils.register_class(Keyframe_Nudge_Panel)


def unregister():
    bpy.utils.unregister_class(Insert_empty_Frame)
    bpy.utils.unregister_class(Keyframe_Nudge)
    bpy.utils.unregister_class(Hold_Keyframe_For)
    bpy.utils.unregister_class(Come_Over_Here)
    bpy.utils.unregister_class(Keyframe_Nudge_Panel)


if __name__ == "__main__":
    register()