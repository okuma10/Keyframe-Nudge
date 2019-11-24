import bpy,os
from .Tools import *


class Inbetween:
    def __init__(self):
        self.mode = bpy.context.mode
        self.objects = bpy.context.selected_objects
        self.fcurves = []
        self.modify_selected = False
        self.marker_insert = False
        self.between_insert = False
        self.inbetween_map = {}
        self.x_y = [0,0]

    def updateSharedData(self):
        self.mode = bpy.context.mode
        self.inbetween_map.clear()
        self.objects = bpy.context.selected_objects


    #Develop Inbetween
    def developInbetween(self):
        selected_list = []
        act_chan_list = []
        act_group_list = []
        act_chan_list_1kf = []
        act_chan_list_2kf = []
        act_chan_list_3kf = []
        act_group_list_1kf = {}
        act_group_list_2kf = {}
        act_group_list_3kf = {}
        act_obj_list_1kf = []
        act_obj_list_2kf = []
        act_obj_list_3kf = []

        if self.mode == "OBJECT":
            for obj in self.objects:
                if obj.animation_data != None:
                    groups = obj.animation_data.action.groups
                    for group in groups:
                        selected_list.append(group.name)
        elif self.mode == "POSE":
            bones = bpy.context.selected_pose_bones
            for bone in bones:
                selected_list.append(bone.name)

        act_chan_counter = 0
        act_group_counter = 0

        timeline_marker = bpy.data.scenes[0].frame_current
        is_marker_onKeyframe = False
        #n analise situation and create inbetween_map dictionary
        for obj in self.objects:
            if obj.animation_data != None:
                self.inbetween_map[obj.name] = {}
                chan_groups = [cGroup for cGroup in obj.animation_data.action.groups]

                for cGroup in chan_groups:
                    if cGroup.name in selected_list:
                        self.inbetween_map[obj.name][cGroup.name] = {}
                        channels = cGroup.channels

                        for channel in channels:
                            act_group_list_3kf[cGroup.name] = []
                            act_group_list_2kf[cGroup.name] = []
                            act_group_list_1kf[cGroup.name] = []
                            ch_name = f'{channel.array_index}.{channel.data_path.rsplit(".")[-1]}'
                            self.inbetween_map[obj.name][cGroup.name][ch_name] = {}

                            all_keyframes = channel.keyframe_points
                            selected_keyframes = [keyframe for keyframe in all_keyframes if keyframe.select_control_point]
                            no_sel_keyframes = len(selected_keyframes)

                            if not channel.lock:
                                #n If there are no keyframes selected - user wants to add an inbetween at midpoint
                                #   position, based on the left/right keyframes from timeline marker
                                if no_sel_keyframes == 0:
                                    keyframe_co0_list = [keyframe.co.x for keyframe in all_keyframes]
                                    is_marker_onKeyframe = isMarkerOnKeyframe(keyframe_co0_list, timeline_marker)

                                    #n If marker is on a existing keyframe
                                    if isMarkerOnKeyframe(keyframe_co0_list, timeline_marker):
                                        self.marker_insert = False
                                        self.modify_selected = True
                                        self.between_insert = False
                                        left_marker_right = getLeftRight(keyframe_co0_list, timeline_marker)
                                        LR_Keyframes = []
                                        self.inbetween_map[obj.name][cGroup.name][ch_name] = {'time': None, 'value': []}

                                        #n get keyframes.co for keyframes who's coordinates are left/right from marker
                                        for keyframe in all_keyframes:
                                            if keyframe.co.x in left_marker_right or keyframe.co[0] == timeline_marker:
                                                LR_Keyframes.append(keyframe.co)
                                        # n create inbetween_map
                                        time = timeline_marker
                                        if len(LR_Keyframes) == 1:
                                            del self.inbetween_map[obj.name][cGroup.name][ch_name]
                                        elif len(LR_Keyframes) == 2:
                                            A_Range = None  #n1 could come and bite me
                                            B_Range = None
                                            if timeline_marker == LR_Keyframes[0][0]:
                                                A_Range = [LR_Keyframes[0][1], LR_Keyframes[0][1]]
                                                B_Range = [LR_Keyframes[0][1], LR_Keyframes[1][1]]
                                            elif timeline_marker == LR_Keyframes[1][0]:
                                                A_Range = [LR_Keyframes[0][1], LR_Keyframes[1][1]]
                                                B_Range = [LR_Keyframes[1][1], LR_Keyframes[1][1]]
                                            self.inbetween_map[obj.name][cGroup.name][ch_name] = {'time' : time,
                                                                                                  'value': [A_Range,
                                                                                                            B_Range]}
                                        elif len(LR_Keyframes) == 3:
                                            A_Range = [LR_Keyframes[0][1], LR_Keyframes[1][1]]
                                            B_Range = [LR_Keyframes[1][1], LR_Keyframes[2][1]]
                                            self.inbetween_map[obj.name][cGroup.name][ch_name] = {'time' : time,
                                                                                                  'value': [A_Range,
                                                                                                            B_Range]}

                                    #n If marker is not over an existing keyframe
                                    else:
                                        self.marker_insert = True
                                        self.modify_selected = False
                                        self.between_insert = False
                                        left_marker_right = getLeftRight(keyframe_co0_list, timeline_marker)
                                        self.inbetween_map[obj.name][cGroup.name][ch_name] = {'time': [], 'value': []}
                                        for keyframe in all_keyframes:
                                            if keyframe.co[0] in left_marker_right:
                                                self.inbetween_map[obj.name][cGroup.name][ch_name]['time'].append(keyframe.co[0])
                                                self.inbetween_map[obj.name][cGroup.name][ch_name]['value'].append(keyframe.co[1])
                                            else:
                                                pass

                                        if len(self.inbetween_map[obj.name][cGroup.name][ch_name]['time']) < 2:
                                            del self.inbetween_map[obj.name][cGroup.name][ch_name]



                                #n If there is only one keyframe selected - user wants to modify the current keyframe/inbetween
                                #   in regards to it's left/right keyframes
                                elif no_sel_keyframes == 1:
                                    self.marker_insert = False
                                    self.modify_selected = True
                                    self.between_insert = False
                                    act_chan_list_1kf.append(ch_name)

                                    position = selected_keyframes[0].co.x

                                    keyframe_co0_list = [keyframe.co.x for keyframe in all_keyframes]
                                    left_selKey_right = getLeftRight(keyframe_co0_list, position)
                                    LR_Keyframes = []

                                    self.inbetween_map[obj.name][cGroup.name][ch_name] = {'time': None, 'value': []}
                                    #n get keyframes.co for keyframes who's coordinates are left/right from marker
                                    for keyframe in all_keyframes:
                                        if keyframe.co[0] in left_selKey_right or keyframe.co[0] == position:
                                            LR_Keyframes.append(keyframe.co)
                                    if len(LR_Keyframes) == 1:
                                        del self.inbetween_map[obj.name][cGroup.name][ch_name]
                                    elif len(LR_Keyframes) == 2:
                                        if position == LR_Keyframes[0][0]:
                                            time = LR_Keyframes[0][0]
                                            A_Range = [LR_Keyframes[0][1], LR_Keyframes[0][1]]
                                            B_Range = [LR_Keyframes[0][1], LR_Keyframes[1][1]]
                                        elif position == LR_Keyframes[1][0]:
                                            time = LR_Keyframes[1][0]
                                            A_Range = [LR_Keyframes[0][1], LR_Keyframes[1][1]]
                                            B_Range = [LR_Keyframes[1][1], LR_Keyframes[1][1]]
                                        self.inbetween_map[obj.name][cGroup.name][ch_name] = {'time' : time,
                                                                                              'value': [A_Range,
                                                                                                        B_Range]}
                                    elif len(LR_Keyframes) == 3:
                                        time = LR_Keyframes[1][0]
                                        A_Range = [LR_Keyframes[0][1], LR_Keyframes[1][1]]
                                        B_Range = [LR_Keyframes[1][1], LR_Keyframes[2][1]]
                                        self.inbetween_map[obj.name][cGroup.name][ch_name] = {'time' : time,
                                                                                              'value': [A_Range,
                                                                                                        B_Range]}


                                #n if there are two keyframes selected - user wants to add an inbetween in timeline marker's
                                #   position based on the two keyframes selected
                                elif no_sel_keyframes == 2:
                                    self.marker_insert = False
                                    self.modify_selected = False
                                    self.between_insert = True
                                    act_chan_list_2kf.append(ch_name)
                                    self.inbetween_map[obj.name][cGroup.name][ch_name] = {'time' : timeline_marker,
                                                                                          'value': []}

                                    for keyframe in selected_keyframes:
                                        self.inbetween_map[obj.name][cGroup.name][ch_name]['value'].append(keyframe.co[1])

                                #n if there are three keyframes selected - user wants to modify second keyframe based on
                                #   the first and third keyframe in selection
                                elif no_sel_keyframes == 3:
                                    self.marker_insert = False
                                    self.modify_selected = True
                                    self.between_insert = False
                                    act_chan_list_3kf.append(ch_name)
                                    A_Range = [selected_keyframes[0].co[1], selected_keyframes[1].co[1]]
                                    B_Range = [selected_keyframes[1].co[1], selected_keyframes[2].co[1]]
                                    time = selected_keyframes[1].co.x
                                    self.inbetween_map[obj.name][cGroup.name][ch_name] = {'time' : time,
                                                                                          'value': [A_Range, B_Range]}
                                else:
                                    pass

                            if no_sel_keyframes > 0:
                                act_chan_counter += 1
                                act_chan_list.append(ch_name)

                            no_sel_keyframes = 0

                        #GROUP level
                        if act_chan_counter > 0:
                            self.marker_insert = False
                            non_active_channels = [name for name in self.inbetween_map[obj.name][cGroup.name].keys() if name not in act_chan_list]

                            for channel in non_active_channels:
                                del self.inbetween_map[obj.name][cGroup.name][channel]

                            act_group_counter += 1
                            act_group_list.append(cGroup.name)

                            if len(act_chan_list_3kf) > 0:
                                act_group_list_3kf[cGroup.name].extend(act_chan_list_3kf)

                            elif len(act_chan_list_2kf) > 0:
                                act_group_list_2kf[cGroup.name].extend(act_chan_list_2kf)
                                del act_group_list_3kf[cGroup.name]

                            elif len(act_chan_list_1kf) > 0:
                                act_group_list_1kf[cGroup.name].extend(act_chan_list_1kf)
                                del act_group_list_3kf[cGroup.name]
                                del act_group_list_2kf[cGroup.name]

                        else:pass

                        act_chan_counter = 0
                        act_chan_list.clear()
                        act_chan_list_1kf.clear()
                        act_chan_list_2kf.clear()
                        act_chan_list_3kf.clear()

                #OBJECT level
                if act_group_counter > 0:
                    self.marker_insert = False
                    non_active_groups = [name for name in self.inbetween_map[obj.name].keys() if name not in act_group_list]
                    for group in non_active_groups:
                        del self.inbetween_map[obj.name][group]
                        del act_group_list_3kf[group]
                        del act_group_list_2kf[group]
                        del act_group_list_1kf[group]

                    if len(act_group_list_3kf.keys()) > 0:
                        act_obj_list_3kf.append(obj.name)
                        self.modify_selected = True
                        self.between_insert = False
                        _groups = None
                        _3kf_groups = act_group_list_3kf.keys()
                        for obj, groups in self.inbetween_map.items():
                            _groups = list(groups.keys())

                            for group, channels in groups.items():
                                map_chanels = list(channels.keys())

                                chan_list = list(act_group_list_3kf.values())[0]
                                for chan in map_chanels:
                                    if group in act_group_list_3kf.keys() and chan in act_group_list_3kf[group]:
                                        pass
                                    elif group in act_group_list_3kf.keys() and chan not in act_group_list_3kf[group]:
                                        del self.inbetween_map[obj][group][chan]

                        for group in _groups:
                            if group in _3kf_groups:
                                pass
                            else:
                                del self.inbetween_map[obj][group]

                    elif len(act_group_list_2kf.keys()) > 0:
                        act_obj_list_2kf.append(obj.name)

                        self.modify_selected = False
                        self.between_insert = True
                        _groups = None
                        _2kf_groups = act_group_list_2kf.keys()
                        for obj, groups in self.inbetween_map.items():
                            _groups = list(groups.keys())
                            for group, channels in groups.items():
                                map_chanels = list(channels.keys())
                                chan_list = [value for item in act_group_list_2kf.values() for value in item]
                                for chan in map_chanels:
                                    if chan in chan_list:
                                        pass
                                    else:
                                        del self.inbetween_map[obj][group][chan]
                        for group in _groups:
                            if group in _2kf_groups:pass
                            else:
                                del self.inbetween_map[obj][group]



                    elif len(act_group_list_1kf) > 0:
                        act_obj_list_1kf.append(obj.name)
                        self.modify_selected = True
                        self.between_insert = False

                act_group_counter = 0
                act_group_list.clear()

        #GLOBAL
        if len(act_obj_list_3kf) > 0:
            self.marker_insert = False
            self.modify_selected = True
            self.between_insert = False
            non_3kf_obj_list = [item for item in self.inbetween_map.keys() if item not in act_obj_list_3kf]
            for obj in non_3kf_obj_list:
                del self.inbetween_map[obj]

        elif len(act_obj_list_2kf) > 0:
            self.marker_insert = False
            self.modify_selected = False
            self.between_insert = True
            non_2kf_obj_list = [item for item in self.inbetween_map.keys() if item not in act_obj_list_2kf]
            for obj in non_2kf_obj_list:
                del self.inbetween_map[obj]

        elif len(act_obj_list_1kf) > 0:
            self.marker_insert = False
            self.modify_selected = True
            self.between_insert = False
            non_1kf_obj_list = [item for item in self.inbetween_map.keys() if item not in act_obj_list_1kf]
            for obj in non_1kf_obj_list:
                del self.inbetween_map[obj]


    #Execute snippets
    def execute(self, control):

        #n If mode is - Insert at Marker,based on left right,keyframes from marker.
        if self.marker_insert:
            # insert keyframe at marker's position
            for obj in self.objects:
                if obj.name in self.inbetween_map.keys():
                    chan_groups = [group for group in obj.animation_data.action.groups]

                    for group in chan_groups:
                        if group.name in self.inbetween_map[obj.name].keys():
                            channels = [channel for channel in group.channels]

                            for channel in channels:
                                chName = str(channel.array_index) + "." + channel.data_path.rsplit('.')[-1]
                                if chName in self.inbetween_map[obj.name][group.name].keys():
                                    x = int((self.inbetween_map[obj.name][group.name][chName]['time'][0] +self.inbetween_map[obj.name][group.name][chName]['time'][1]) / 2)
                                    y = remapValue([-1, 1], self.inbetween_map[obj.name][group.name][chName]['value'],0)
                                    #insert keyframe to channel
                                    channel.keyframe_points.insert(x, y, options={'NEEDED'}, keyframe_type='KEYFRAME')
                                    for keyframe in channel.keyframe_points:
                                        if keyframe.co[0] == x:
                                            keyframe.type = 'KEYFRAME'
                                else:pass

            forceReDraw()

            #n If mode is - Modify keyframe under timeline marker,or is selected.
        elif self.modify_selected:
            # modfiy selected or at timemarker pos, keyframe
            for obj in self.objects:
                if obj.name in self.inbetween_map.keys():
                    chan_groups = [group for group in obj.animation_data.action.groups]

                    for group in chan_groups:
                        if group.name in self.inbetween_map[obj.name].keys():
                            channels = [channel for channel in group.channels]

                            for channel in channels:
                                chName = str(channel.array_index) + "." + channel.data_path.rsplit(".")[-1]
                                if chName in self.inbetween_map[obj.name][group.name].keys():
                                    if control < 0:
                                        x = int(self.inbetween_map[obj.name][group.name][chName]['time'])
                                        y = remapValue([-1, 0],
                                                       self.inbetween_map[obj.name][group.name][chName]['value'][0],control)
                                        # modify keyframe by replacing it
                                        for keyframe in channel.keyframe_points:
                                            kf_type = keyframe.type
                                            if keyframe.co[0] == self.inbetween_map[obj.name][group.name][chName]['time']:
                                                channel.keyframe_points.insert(x, y, options={'REPLACE'},keyframe_type=kf_type)

                                    elif control > 0:
                                        x = int(self.inbetween_map[obj.name][group.name][chName]['time'])
                                        y = remapValue([0, 1],self.inbetween_map[obj.name][group.name][chName]['value'][1],control)
                                        # modify keyframe by replacing it
                                        for keyframe in channel.keyframe_points:
                                            kf_type = keyframe.type
                                            if keyframe.co[0] == self.inbetween_map[obj.name][group.name][chName]['time']:
                                                channel.keyframe_points.insert(x, y, options={'REPLACE'}, keyframe_type=kf_type)
            forceReDraw()

        #n If mode is - insert keyframe at timeline marker's position.By using value based on two selected keyframes.
        elif self.between_insert:
            #activate insert between two selected keyframes
            for obj in self.objects:
                if obj.name in self.inbetween_map.keys():
                    chan_groups = [group for group in obj.animation_data.action.groups]

                    for group in chan_groups:
                        if group.name in self.inbetween_map[obj.name].keys():
                            channels = [channel for channel in group.channels]

                            for channel in channels:
                                chName = str(channel.array_index) + "." + channel.data_path.rsplit('.')[-1]

                                if chName in self.inbetween_map[obj.name][group.name].keys():
                                    x = int(self.inbetween_map[obj.name][group.name][chName]['time'])
                                    y = remapValue([-1, 1], self.inbetween_map[obj.name][group.name][chName]['value'],
                                                   control)
                                    #create insert keyframe at marker's position
                                    channel.keyframe_points.insert(x, y, options={'NEEDED'}, keyframe_type='KEYFRAME')
                                    for keyframe in channel.keyframe_points:
                                        if keyframe.co.x == x:
                                            keyframe.type = "KEYFRAME"

            forceReDraw()


    def debugPrint(self):
        return self.inbetween_map,[('Marker Insert',self.marker_insert),('Modify Selected',self.modify_selected),('Between Insert',self.between_insert)],self.x_y