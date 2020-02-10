import bpy
import numpy as np
from ..Keyframe.Tools import *

def Hold_For(usr_inp):
    #n <-- initial data from Belnder -->
    control = usr_inp

    pencils = bpy.data.grease_pencils
    #n <-- global variable declaration -->
    gp_HoldFor_map = {}

    selected_keyframes = []
    layers_with_selectedKf = []
    objects_with_selectedKf = []

    #n <--  Initial data collection -->
    for pencil in pencils:
        name = pencil.name
        gp_HoldFor_map[name] = [[], []]
        layers = pencil.layers

        for layer in layers:
            layer_name = layer.info
            keyframes_selected = [keyframe.frame_number for keyframe in layer.frames if keyframe.select]

            if len(keyframes_selected) > 0:
                keyframes_non_selected = [keyframe.frame_number for keyframe in layer.frames if
                                          keyframe.select == False and keyframe.frame_number > keyframes_selected[-1]]

                for keyframe in keyframes_selected:
                    gp_HoldFor_map[name][0].append(keyframe)
                    selected_keyframes.append(keyframe)

                for keyframe in keyframes_non_selected:
                    gp_HoldFor_map[name][1].append(keyframe)

            # Mark layers with selected keyframes
            if len(selected_keyframes) > 0:
                layers_with_selectedKf.append(layer_name)
            selected_keyframes.clear()

        # Modify Map - populate object moding list if object has a layer with selected keyframes
        if len(layers_with_selectedKf) > 0:
            objects_with_selectedKf.append(name)
        layers_with_selectedKf.clear()

    # Remove Pencils with 0 selected keyframes.
    if len(objects_with_selectedKf) > 0:
        non_active_pencils = [pencil.name for pencil in pencils if pencil.name not in objects_with_selectedKf]
        for pencil in non_active_pencils:
            del gp_HoldFor_map[pencil]
    del objects_with_selectedKf

    #n <--  Process Data  -->
    for pencil in pencils:
        if pencil.name in gp_HoldFor_map.keys():
            if gp_HoldFor_map[pencil.name][0]:
                # Cleanup data
                clean_non_selected = [keyframe for keyframe in gp_HoldFor_map[pencil.name][1] if
                                      keyframe not in gp_HoldFor_map[pencil.name][0]]
                gp_HoldFor_map[pencil.name][1] = clean_non_selected

                selected_kf_x = np.array(sorted(list(set(gp_HoldFor_map[pencil.name][0]))))
                non_selected_kf_x = np.array(sorted(list(set(gp_HoldFor_map[pencil.name][1]))))

                # Create new position for selected keyframes for based on user input
                new_selected_kef_x = []
                start_frame = selected_kf_x[0]
                for i in range(len(selected_kf_x)):
                    if start_frame == selected_kf_x[0]:
                        new_selected_kef_x.append(start_frame)
                        start_frame += control
                    else:
                        new_selected_kef_x.append(start_frame)
                        start_frame += control

                # Create new position for non selected keyframes based on new last selected position
                if len(non_selected_kf_x)>0:
                    distance = new_selected_kef_x[-1] - non_selected_kf_x[0] + control
                    new_non_selected_kef_x = non_selected_kf_x + distance

                # Assign new data to old positions
                layers = pencil.layers
                for layer in layers:
                    if not layer.lock:
                        keyframes = layer.frames

                        for keyframe in keyframes:
                            # for selected
                            if keyframe.frame_number in selected_kf_x:
                                kf_ix = int(np.where(selected_kf_x == keyframe.frame_number)[0])
                                keyframe.frame_number = new_selected_kef_x[kf_ix]

                            # for non selected
                            elif len(non_selected_kf_x)>0:
                                if keyframe.frame_number in non_selected_kf_x:
                                    kf_ix = int(np.where(non_selected_kf_x == keyframe.frame_number)[0])
                                    keyframe.frame_number = new_non_selected_kef_x[kf_ix]

            # if no selected keyframes , report error
            else:
                print(f'No keyframes selected for object {pencil.name}')

    forceReDraw()