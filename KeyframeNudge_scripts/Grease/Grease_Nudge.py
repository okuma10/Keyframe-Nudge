import bpy
from bisect import bisect
#◆◇
#n1 Add scripts:								n1 Rework
#n4 ◆ insert empty frame - Push/Pull	. n1 ◇ insert empty frame .
#n1 ◇ nudge								. n1 ◇ None
#n1 ◇ hold for							. n1 ◇ None
#n1 ◇ come over							. n1 ◇ None
#n1 ◇ inbetween							. n1 ◇ None


def insert_empty_frame(user_input):
	control = user_input

	selected_layers = []
	#n Get the objects that have selected layers
	for pen in bpy.data.grease_pencils:
		layers = [layer for layer in pen.layers]
		for layer in layers:
			if layer.select:
				if layer.id_data.name in selected_layers : pass
				else: selected_layers.append(layer.id_data.name)

	#n Get a list of GP objects based on selected_layers
	pencils = [pen for pen in bpy.data.grease_pencils if pen.name in selected_layers]
	#n Loop trough the list
	for pen in pencils:
		layers = [layer for layer in pen.layers]
		for layer in layers:
			all_frames = [x for x in layer.frames]
			try:
				selected_frames = [x for x in layer.frames if x.select]

				# If we have selected frame/s
				if len(selected_frames) is not 0:
					first_selected = selected_frames[0]
					first_selected_id = None
					for frame in all_frames:
						if frame.frame_number == first_selected.frame_number:
							first_selected_id = all_frames.index(first_selected)

					work_frames = [frame for frame in all_frames[first_selected_id:]]

					while work_frames:
						work_frames[0].frame_number += control
						del work_frames[0]

				# If no selected keyframe
				else:
					print('non selected')
					timeline_position = bpy.data.scenes[0].frame_current
					work_frames = [frame for frame in all_frames if frame.frame_number >= timeline_position]

					while work_frames:
						work_frames[0].frame_number += control
						del work_frames[0]
			except:
				pass

			wm = bpy.context.window_manager
			for window in wm.windows:
				for area in window.screen.areas:
					if area.type == 'VIEW_3D':
						area.tag_redraw()
			pen.update_tag(refresh = {'TIME'})





