import bpy
import numpy as np
from .Tools import *

def PushPull(usr_inp):
    control = usr_inp

    mode = bpy.context.mode
    objects = bpy.context.selected_objects
    sel_list = []

    #n analyze mode and create map modulators
    if mode == "POSE":
        sel_bones = bpy.context.selected_pose_bones
        for bone in sel_bones:
            sel_list.append(bone.name)
    elif mode == "OBJECT":
        selected_objs = bpy.context.selected_objects
        for obj in selected_objs:
            if obj.animation_data != None:
                for group in obj.animation_data.action.groups:
                    sel_list.append(group.name)
                else:
                    pass

    #n Script Data
    push_pull_map = {}
    selection_based = False
    marker_based = False

    timeline_marker = bpy.data.scenes[0].frame_current

    #n Modulators
    selKeyF_counter = 0
    actChan_counter = 0
    actGroup_counter = 0
    actObj_counter = 0

    #n Loop trough every object and push/pull keyframes based on user interaction (selected,non-selected keyframes)
    for obj in objects:
        if obj.animation_data != None:
            push_pull_map[obj.name] = {}
            groups = obj.animation_data.action.groups

            for group in groups:
                if group.name in sel_list:
                    channels = group.channels
                    push_pull_map[obj.name][group.name] = {}

                    for channel in channels:
                        ch_name = f'{channel.data_path}.{channel.array_index}'
                        all_keyframes = channel.keyframe_points
                        selected_keyframes = [keyframe for keyframe in all_keyframes if keyframe.select_control_point]
                        push_pull_map[obj.name][group.name][ch_name] = []
                        if selected_keyframes:
                            non_selected_keyframes = [keyframe for keyframe in all_keyframes if
                                                      keyframe not in selected_keyframes]
                            keyframe_list = [keyframe for keyframe in all_keyframes if
                                             keyframe.co.x >= selected_keyframes[0].co.x]

                            no_of_selected = len(selected_keyframes)

                            #n user has selected a keyframe to push or pull form
                            if no_of_selected:
                                for keyframe in keyframe_list:
                                    selKeyF_counter += 1
                                    push_pull_map[obj.name][group.name][ch_name].append(keyframe)
                        #n modulate based selected keyframes
                        if selKeyF_counter == 0:
                            del push_pull_map[obj.name][group.name][ch_name]
                        else:
                            actChan_counter += 1
                        selKeyF_counter = 0
                    #n modulate based on active channels
                    if actChan_counter == 0:
                        del push_pull_map[obj.name][group.name]
                    else:
                        actGroup_counter += 1
                    actChan_counter = 0

            #n modulate based on active groups
            if actGroup_counter == 0:
                del push_pull_map[obj.name]
            else:
                actObj_counter += 1
    #n if no active objects generate marker based map
    if actObj_counter == 0:
        selection_based = False
        marker_based = True

        for obj in objects:
            if obj.animation_data != None:
                push_pull_map[obj.name] = {}
                groups = obj.animation_data.action.groups

                for group in groups:
                    if group.name in sel_list:
                        channels = group.channels
                        push_pull_map[obj.name][group.name] = {}

                        for channel in channels:
                            ch_name = f'{channel.data_path}.{channel.array_index}'
                            push_pull_map[obj.name][group.name][ch_name] = []
                            all_keyframes = [keyframe for keyframe in channel.keyframe_points if
                                             keyframe.co.x >= timeline_marker]

                            for keyframe in all_keyframes:
                                push_pull_map[obj.name][group.name][ch_name].append(keyframe)

    #n Turn selection based
    else:
        selection_based = True
        marker_based = False

    #n Process maps and change coordinates
    if selection_based:
        for obj in push_pull_map.items():
            if type(obj[1]) != str:
                for group in obj[1].items():
                    for channel in group[1].items():
                        all_keyframe_co = np.array([keyframe.co.x for keyframe in channel[1]]) + control
                        index_count = 0
                        for keyframe in channel[1]:
                            keyframe.co.x = all_keyframe_co[index_count]
                            index_count += 1

    elif marker_based:
        for obj in push_pull_map.items():
            for group in obj[1].items():
                for channel in group[1].items():
                    for keyf in channel[1]:
                        keyf.co.x += control

    for obj in objects:
        if obj.animation_data:
            groups = obj.animation_data.action.groups
            for group in groups:
                channels = group.channels
                for channel in channels:
                    channel.update()
    forceReDraw()
