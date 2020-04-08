import bpy
import numpy as np
from ..Keyframe.Tools import *

def GP_PushPull(usr_inp):
    control = usr_inp

    Pencils = [pencil for pencil in bpy.data.grease_pencils]
    gp_PushPull_map = {}

    selected_keyframes = []
    layers_with_selectedKf = []
    objects_with_selectedKf = []
    objects_with_selected_layers = []

    marker_position = bpy.context.scene.frame_current

    #n Populate Map
    for pencil in Pencils:
        name = pencil.name
        layers = pencil.layers
        gp_PushPull_map[name] = {'Start Frame': 0, 'Keyframes': {}}
        locked_layers = []

        pencil_s_keyframe_No_list = []
        pencil_keyframe_No_list = []

        for layer in layers:
            layer_name = layer.info
            keyframes = layer.frames
            gp_PushPull_map[name]['Keyframes'][layer_name] = []

            if layer.select: objects_with_selected_layers.append(name)
            if layer.lock:
                locked_layers.append(layer_name)
            else:
                for keyframe in keyframes:
                    keyf_frame = keyframe.frame_number
                    gp_PushPull_map[name]['Keyframes'][layer_name].append(keyframe)

                    if keyframe.select:
                        selected_keyframes.append(keyf_frame)
                        pencil_s_keyframe_No_list.append(keyf_frame)
                    else:
                        pencil_keyframe_No_list.append(keyf_frame)

            #n LAYERS LEVEL
            #n add layer to layers with selected keyframes
            if len(selected_keyframes) > 0:
                layers_with_selectedKf.append(layer_name)
            selected_keyframes.clear()

        #n OBJECT LEVEL
        #n Modify Map, based on locked layers
        for layer in locked_layers:
            del gp_PushPull_map[name]['Keyframes'][layer]

        if len(layers_with_selectedKf) > 0:
            objects_with_selectedKf.append(name)
        layers_with_selectedKf.clear()

        #n Populate Start Frame variable
        if len(pencil_s_keyframe_No_list) > 0:
            frame_no_list = list(set(pencil_s_keyframe_No_list))
            gp_PushPull_map[name]['Start Frame'] = frame_no_list[0]
        else:
            gp_PushPull_map[name]['Start Frame'] = marker_position
            frame_no_list = list(set(pencil_keyframe_No_list))

    #n GLOBAL LEVL
    #n Modify map based on Objects which have layers with selected keyframes
    if len(objects_with_selectedKf) > 0:
        not_active_pencils = [pencil.name for pencil in Pencils if pencil.name not in objects_with_selectedKf]
        for pencil in not_active_pencils:
            del gp_PushPull_map[pencil]
    elif len(objects_with_selected_layers) > 0:
        not_active_pencils = [pencil.name for pencil in Pencils if pencil.name not in objects_with_selected_layers]
        for pencil in not_active_pencils:
            del gp_PushPull_map[pencil]


    #n Execute Push Pull
    for pencil in gp_PushPull_map.items():
        start_frame = pencil[1]['Start Frame']
        layers = pencil[1]['Keyframes']

        for layer in layers.items():
            work_list = []
            keyframes = layer[1]
            for keyframe in keyframes:
                keyframe_number = keyframe.frame_number
                if keyframe_number >= start_frame:
                    work_list.append(keyframe)
            new_pos = np.array([keyframe.frame_number for keyframe in work_list]) + control
            for i in range(0, len(work_list)):
                work_list[i].frame_number = new_pos[i]

            # layer.select = False

    forceReDraw()