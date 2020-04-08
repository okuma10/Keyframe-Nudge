import bpy
import numpy as np
from ..Keyframe.Tools import forceReDraw


def gp_come_over():
    timeline_marker = bpy.context.scene.frame_current

    pencils = bpy.data.grease_pencils

    gp_HoldFor_map = {}

    selected_keyframes = []
    layers_with_selectedKf = []
    objects_with_selectedKf = []

    #n1 Populate Map based on selected keyframes, and non selected after selected
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


    #n1 Process grease pencils based on map
    for pencil in pencils:

        #n1 Modify if GP in Map
        if pencil.name in gp_HoldFor_map.keys():
            keys_in_Map = gp_HoldFor_map[pencil.name]
            distance_to_marker = timeline_marker - keys_in_Map[0][0]

            layers = pencil.layers
            for layer in layers:
                keyframes = layer.frames

                #n1 Make sure we do this only if we have keyframes selected.
                if len(keys_in_Map[0]) > 0:

                    #n3 Somewhere here is an issue with non selected keyframes get destroyed by selected ones
                    # by landing on top of them. Look at it ASP
                    #n1 Non selected Loop
                    if len(keys_in_Map[1]) > 0:
                        new_non_selected_pos = np.array(keys_in_Map[1]) + distance_to_marker

                        # modify non selected after selected keyframe's position
                        for keyframe in keyframes:
                            if keyframe.frame_number in keys_in_Map[1]:
                                idx = keys_in_Map[1].index(keyframe.frame_number)
                                keyframe.frame_number = new_non_selected_pos[idx]
                    #n3 End of supposed problem Block
                    
                    #n1 Selected Loop
                    new_selected_pos = np.array(keys_in_Map[0]) + distance_to_marker
                    for keyframe in keyframes:
                        if keyframe.frame_number in keys_in_Map[0]:
                            idx = keys_in_Map[0].index(keyframe.frame_number)
                            keyframe.frame_number = new_selected_pos[idx]
                    layer.select = False
                else:
                    print('There are no Keyframes selected.')

        # Update view
        forceReDraw()