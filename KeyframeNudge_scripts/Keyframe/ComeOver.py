import bpy
import numpy as np


def comeOver():
    sel_objs = bpy.context.selected_objects             #n Get selected objects
    mode = bpy.context.mode                             #n Get Current Mode
    timeline_marker = bpy.context.scene.frame_current   #n Get Timeline position

    #n Groups/Bones modifier
    selected_list = []
    if mode == "POSE":
        sel_bones = bpy.context.selected_pose_bones
        for bone in sel_bones:
            selected_list.append(bone.name)
    elif mode == "OBJECT":
        for obj in bpy.context.selected_objects:
            if obj.animation_data != None:
                groups = obj.animation_data.action.groups
                for group in groups:
                    selected_list.append(group.name)

    #n Count modifiers
    sel_keyF_counter  = 0
    act_chan_counter  = 0
    act_group_counter = 0

    #n Come Over map
    comeOver_map = {}

    #n Loop Through Selected objects to populate map
    for obj in sel_objs:

        #n Continue with populating map, only if we have animation data for object
        if obj.animation_data != None:
            #n Populate map
            comeOver_map[obj.name] = {}
            groups = obj.animation_data.action.groups

            for group in groups:
                if group.name in selected_list:                 #Modulate map based on selection - Pose Bones
                    comeOver_map[obj.name][group.name] = {}
                    channels = group.channels

                    for channel in channels:
                        ch_name = f'{channel.data_path}.{channel.array_index}'
                        comeOver_map[obj.name][group.name][ch_name] = []
                        keyframes = channel.keyframe_points

                        for keyframe in keyframes:
                            if keyframe.select_control_point:
                                comeOver_map[obj.name][group.name][ch_name].append(keyframe)
                                sel_keyF_counter += 1

                            else:
                                pass
                            #n End of populating the map

                        #n Modify map based on no. of selected keyframes - if 0 remove channel
                        if sel_keyF_counter > 0:
                            act_chan_counter += 1
                        else:
                            del comeOver_map[obj.name][group.name][ch_name]
                        sel_keyF_counter = 0

                    #n Modify map based on no. of active channels - if 0 remove group
                    if act_chan_counter > 0:
                        act_group_counter += 1
                    else:
                        del comeOver_map[obj.name][group.name]
                    act_chan_counter = 0

            #n Modify map based on no. of active groups - if 0 remove object
            if act_group_counter > 0:
                pass
            else:
                del comeOver_map[obj.name]
            act_group_counter = 0

        #n1 Should add a command to blender's own notification system
        else:
            print(f"{'':<4}We don't have animation Data For this object {obj.name}")

    #n Loop trough selected objects again,procede only if object, group and channels in map
    for obj in sel_objs:
        if obj.animation_data != None:  #make sure we are not looping trough non animated objects
            if obj.name in comeOver_map.keys():
                groups = obj.animation_data.action.groups

                for group in groups:
                    if group.name in comeOver_map[obj.name].keys() and group.name in selected_list:  #make sure to proceed onlyif group.name is in selected_list -> modification for Bones
                        channels = group.channels

                        for channel in channels:
                            ch_name = f'{channel.data_path}.{channel.array_index}'
                            if ch_name in comeOver_map[obj.name][group.name].keys():

                                #n if map has 1 selected keyframe - user desires to move selected and all following keyframes to timeline marker position
                                if len(comeOver_map[obj.name][group.name][ch_name]) == 1:
                                    all_keyframes   = channel.keyframe_points
                                    selected_pos    = comeOver_map[obj.name][group.name][ch_name][0].co.x
                                    distance        = timeline_marker - selected_pos
                                    work_keyframes  = [keyframe for keyframe in all_keyframes if keyframe.co.x >= comeOver_map[obj.name][group.name][ch_name][0].co.x]
                                    new_co_X        = np.array([keyframe.co.x for keyframe in work_keyframes]) + distance

                                    for keyframe in work_keyframes:
                                        keyF_index      = work_keyframes.index(keyframe)
                                        keyframe.co.x   = new_co_X[keyF_index]


                                #n if map has more than 1 keyframe - user desires to move only selected keyframes to the timeline position(retainind distance between each other)
                                elif len(comeOver_map[obj.name][group.name][ch_name]) > 1:
                                    selected_pos = comeOver_map[obj.name][group.name][ch_name][0].co.x
                                    distance = timeline_marker - selected_pos
                                    work_keyframes = comeOver_map[obj.name][group.name][ch_name]
                                    new_co_X = np.array([keyframe.co.x for keyframe in work_keyframes]) + distance

                                    for keyframe in work_keyframes:
                                        keyF_index = work_keyframes.index(keyframe)
                                        keyframe.co.x = new_co_X[keyF_index]
                                    print(new_co_X)
                                else:pass
                            #n Make sure to update the channel,to fix handles
                            channel.update()
