import bpy, os
import numpy as np
from ..Keyframe.Tools import *


def gp_Nudge(usr_inp):
    control = usr_inp

    Pencils = bpy.data.grease_pencils
    gp_Nudge_map = {}

    selected_keyframes = []

    layers_with_selectedKf = []
    objects_with_selectedKf = []

    #n Loop through GP objects
    for pencil in Pencils:
        name = pencil.name
        layers = pencil.layers

        gp_Nudge_map[name] = []

        #n Loop through GP object's layers
        for layer in layers:
            layer_name = layer.info
            keyframes = layer.frames

            #n Loop through GP object's keyframes for every layer
            #   populate GP map
            for keyframe in keyframes:
                keyf_frame = keyframe.frame_number
                if keyframe.select:
                    gp_Nudge_map[name].append(keyf_frame)
                    selected_keyframes.append(keyf_frame)

            #n Mark layers with selected keyframes
            if len(selected_keyframes) > 0:
                layers_with_selectedKf.append(layer_name)
            selected_keyframes.clear()

        #n Modify Map - populate object modding list if object has a layer with selected keyframes
        if len(layers_with_selectedKf) > 0:
            objects_with_selectedKf.append(name)
        layers_with_selectedKf.clear()

    #n Remove Pencils with 0 selected keyframes.
    if len(objects_with_selectedKf) > 0:
        non_active_pencils = [pencil.name for pencil in Pencils if pencil.name not in objects_with_selectedKf]
        for pencil in non_active_pencils:
            del gp_Nudge_map[pencil]
    del objects_with_selectedKf

    #n Loop and modify pencils's frames based on generated map
    for pencil in Pencils:
        if pencil.name in gp_Nudge_map.keys():
            selected_kf_x = np.array(gp_Nudge_map[pencil.name])
            new_kf_x = selected_kf_x + control

            layers = pencil.layers
            for layer in layers:
                if not layer.lock:
                    keyframes = layer.frames

                    for keyframe in keyframes:
                        if keyframe.frame_number in selected_kf_x:
                            list_id = int(np.where(selected_kf_x == keyframe.frame_number)[0])

                            keyframe.frame_number = new_kf_x[list_id]
                    layer.select = False

    forceReDraw()


