import bpy, os
import numpy as np
from ...small_tools import rounding_my
from ..Keyframe.Tools import forceReDraw


def gp_spread_to():
    print('I\'m called')
    timeline_marker = bpy.context.scene.frame_current

    pencils = bpy.data.grease_pencils

    gp_HoldFor_map = {}

    selected_keyframes = []
    layers_with_selectedKf = []
    objects_with_selectedKf = []

    isAnySelected = True

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


    # Process Data
    for pencil in pencils:
        if pencil.name in gp_HoldFor_map.keys():
            if gp_HoldFor_map[pencil.name][0]:
                cleanup_indices = []
                clean_non_selected = [keyframe for keyframe in gp_HoldFor_map[pencil.name][1] if
                                      keyframe not in gp_HoldFor_map[pencil.name][0]]
                gp_HoldFor_map[pencil.name][1] = clean_non_selected

                selected_kf_x = np.array(sorted(list(set(gp_HoldFor_map[pencil.name][0]))))
                non_selected_kf_x = np.array(sorted(list(set(gp_HoldFor_map[pencil.name][1]))))

                #n1 Create New Position For Selected
                space_between = timeline_marker - selected_kf_x[0]
                proportion = space_between / (len(selected_kf_x) - 1)

                new_selected_kf_x = np.zeros(len(selected_kf_x))

                for i in range(len(selected_kf_x)):
                    if i == 0:
                        new_selected_kf_x[i] = selected_kf_x[i]
                    elif i == len(selected_kf_x):
                        new_selected_kf_x[i] = timeline_marker
                    else:
                        new_selected_kf_x[i] = new_selected_kf_x[i - 1] + proportion

                # Safeguard if no non_selected
                #n3 Somewhere here we have an issue where non selected get overwritten by selected
                # apparently selected land above the selected and overwrite them. Look at is ASP
                if len(non_selected_kf_x) > 0:
                    #n1 Create New Position For Non Selected
                    initial_distance = non_selected_kf_x[0] - selected_kf_x[-1]
                    select_non_select_distance = new_selected_kf_x[-1] - non_selected_kf_x[0]
                    new_non_selected_kf_x = non_selected_kf_x + select_non_select_distance + initial_distance
                #n1 New Position Creation End
                #n3 End of supposed problem Block
                #n1 new_selected_kf_x,new_non_selected_kf_x

                layers = pencil.layers
                for layer in layers:
                    if not layer.lock:
                        keyframes = layer.frames

                        if len(non_selected_kf_x) > 0:
                            for keyframe in keyframes:
                                if keyframe.frame_number in non_selected_kf_x:
                                    kf_ix = int(np.where(non_selected_kf_x == keyframe.frame_number)[0])
                                    keyframe.frame_number = new_non_selected_kf_x[kf_ix]

                        for keyframe in keyframes:
                            if keyframe.frame_number in selected_kf_x:
                                kf_ix = int(np.where(selected_kf_x == keyframe.frame_number)[0])
                                keyframe.frame_number = rounding_my(new_selected_kf_x[kf_ix])

                    layer.select = False

    forceReDraw()

