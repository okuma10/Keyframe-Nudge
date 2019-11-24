import bpy, os
import numpy as np

os.system('cls')


def hold_for(usr_inp: int):
    control = usr_inp
    #n get Selected Objects
    sel_objs = bpy.context.selected_objects

    #n Script Data
    hold_map = {}
    selKeyF_counter = 0  #modify hold_map based on selected keyframes
    actChan_counter = 0  #modify hold_map based on active channels   -has selected keyframes
    actGroup_counter = 0  #modify hold_map based on active groups     -has channels with selected keyframes

    #n Get mode and check if it is 'Pose'. Populate selected_pose_bones for modification of hold_map
    mode = bpy.context.mode
    selected_pose_bones = []
    if mode == 'POSE':
        for bone in bpy.context.selected_pose_bones:
            selected_pose_bones.append(bone.name)

    #n Loop through selected objects
    for obj in sel_objs:
        #n if they are animated add them to hold_map and continue building map
        if obj.animation_data != None:
            hold_map[obj.name] = {}

            groups = obj.animation_data.action.groups

            for group in groups:
                hold_map[obj.name][group.name] = {}
                channels = group.channels

                for channel in channels:
                    ch_name = f'{channel.data_path}.{channel.array_index}'
                    hold_map[obj.name][group.name][ch_name] = {"Sel"  : [],
                                                               "noSel": []}
                    selected_keyframes = [keyframe for keyframe in channel.keyframe_points if
                                          keyframe.select_control_point]
                    hold_map[obj.name][group.name][ch_name]['Sel'] = selected_keyframes

                    #n if we have at least 1 keyframe selected add to selKeyF_counter for every keyframe.
                    #   find not selected keyframes and add them to map.
                    if len(selected_keyframes) > 0:
                        for keyframe in selected_keyframes:
                            selKeyF_counter += 1

                        non_selected_keyframes = [keyframe for keyframe in channel.keyframe_points if
                                                  keyframe.co.x > selected_keyframes[-1].co.x]
                        hold_map[obj.name][group.name][ch_name]['noSel'].extend(non_selected_keyframes)

                    #n Modify map based on selected keys
                    if selKeyF_counter > 0:
                        actChan_counter += 1
                    elif selKeyF_counter == 0:
                        del hold_map[obj.name][group.name][ch_name]
                    selKeyF_counter = 0

                #n modify map based on active channels(has selectec keyframes)
                if actChan_counter == len(channels):
                    actGroup_counter += 1
                elif actChan_counter == 0:
                    del hold_map[obj.name][group.name]
                else:
                    actGroup_counter += 1
                actChan_counter = 0

                #n modify map based on selected pose bones if user is in "POSE" mode
                if mode == "POSE":
                    if group.name in selected_pose_bones:
                        pass
                    else:
                        del hold_map[obj.name][group.name]

            #n Modify map based on active groups
            if actGroup_counter > 0:
                pass
            elif actGroup_counter == 0:
                del hold_map[obj.name]
            actGroup_counter = 0


    #n This phase gets all keyframe.co.x values so a general plan for new keyframe.co.x positions.
    all_selected_co = []
    for obj in hold_map.items():

        for group in obj[1].items():

            for channel in group[1].items():

                for keyframe in channel[1]['Sel']:
                    all_selected_co.append(keyframe.co.x)  # Populate all_selected_co list

    all_selected_co = sorted(list(set(all_selected_co)))  # Remove repeating and sort

    #n Prepare for calculating new positions.And calculate new positions
    new_sel_pos = []

    for i in range(len(all_selected_co)):
        if i == 0:
            new_sel_pos.append(all_selected_co[0])
        else:
            new_sel_pos.append(new_sel_pos[i - 1] + control)

    #n In this phase we change selected keyframes.co.x to the calculated new positions
    for obj in hold_map.items():
        for group in obj[1].items():
            for channel in group[1].items():
                last_index_in_channel = 0  # this will help us calculate the new position for non selected keyframes

                #n work on selected keyframes
                for keyframe in channel[1]['Sel']:
                    if keyframe.co.x in all_selected_co:
                        find_index = all_selected_co.index(keyframe.co.x)
                        keyframe.co.x = new_sel_pos[find_index]
                        last_index_in_channel = new_sel_pos[find_index]
                #n work on non selected, if channel has non selected keyframes
                if channel[1]['noSel']:
                    all_non_selected_co = np.array([keyframe.co.x for keyframe in
                                                    channel[1]['noSel']])  # turn to numpy array for easier calculations
                    new_distance = (last_index_in_channel + control) - channel[1]['noSel'][0].co.x
                    new_non_selected_co = all_non_selected_co + new_distance

                    # assigning new positions
                    for keyframe in channel[1]['noSel']:
                        if keyframe.co.x in all_non_selected_co:
                            find_index = np.where(all_non_selected_co == keyframe.co.x)
                            keyframe.co.x = new_non_selected_co[find_index]

    #n Now we loop through the selected objects's fcurves and update them if their index was in the hold_map
    for obj in sel_objs:
        if obj.name in hold_map.keys():
            groups = obj.animation_data.action.groups
            for group in groups:
                if group.name in hold_map[obj.name].keys():
                    channels = group.channels
                    for channel in channels:
                        ch_name = f'{channel.data_path}.{channel.array_index}'
                        if ch_name in hold_map[obj.name][group.name].keys():
                            channel.update()
