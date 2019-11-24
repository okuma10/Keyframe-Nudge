import bpy, os
import numpy as np
from .Tools import forceReDraw

def keyframe_nudge(usr_inp):
    mode = bpy.context.mode
    selected = bpy.context.selected_objects
    nudge_map = {}
    sel_list = []
    #n get selected objects based on mode
    if mode == "POSE":
        for obj in selected:
            if obj.animation_data != None:
                sel_bones = bpy.context.selected_pose_bones
                for bone in sel_bones:
                    sel_list.append(bone.name)
    elif mode == "OBJECT":
        for obj in selected:
            if obj.animation_data != None:
                for group in obj.animation_data.action.groups:
                    sel_list.append(group.name)

    #n Script Data
    control = usr_inp
    sel_keyF_counter = 0
    act_Channels_counter = 0
    act_Groups_counter = 0

    #n generate map
    for obj in selected:
        if obj.animation_data != None:
            nudge_map[obj.name] = {}
            groups = obj.animation_data.action.groups

            for group in groups:
                if group.name in sel_list:  #n Modulate based on selected_list(for correct pose bones)
                    nudge_map[obj.name][group.name] = {}
                    channels = group.channels

                    for channel in channels:
                        ch_name = f'{channel.data_path}.{channel.array_index}'
                        nudge_map[obj.name][group.name][ch_name] = []
                        all_keyframes = channel.keyframe_points
                        sel_keyframes = [keyframe for keyframe in all_keyframes if keyframe.select_control_point]

                        if sel_keyframes:
                            for keyframe in sel_keyframes:
                                sel_keyF_counter += 1
                                nudge_map[obj.name][group.name][ch_name].append(keyframe)
                        else:
                            pass

                        #n modulate based on selected keys
                        if sel_keyF_counter > 0:
                            act_Channels_counter += 1
                        elif sel_keyF_counter == 0:
                            del nudge_map[obj.name][group.name][ch_name]
                        sel_keyF_counter = 0

                    #n modulate based on active channels
                    if act_Channels_counter > 0:
                        act_Groups_counter += 1
                    elif act_Channels_counter == 0:
                        del nudge_map[obj.name][group.name]
                    act_Channels_counter = 0

            #n modulate based on active groups
            if act_Groups_counter > 0:
                pass
            elif act_Groups_counter == 0:
                del nudge_map[obj.name]
            act_Groups_counter = 0

    #n Loop through map and modify keys
    for obj in nudge_map.items():
        for group in obj[1].items():
            for channel in group[1].items():
                for keyframe in channel[1]:
                    keyframe.co.x += control

    #n Loop through selected objects and update fcurves
    for obj in selected:
        if obj.name in nudge_map.keys():
            groups = obj.animation_data.action.groups
            for group in groups:
                channels = group.channels
                for channel in channels:
                    channel.update()

    forceReDraw()


