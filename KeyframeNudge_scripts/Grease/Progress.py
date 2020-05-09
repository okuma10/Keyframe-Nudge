
#◆◇
#n1 Add scripts:								n1 Rework
#n4 ◆ insert empty frame - Push/Pull	. n1 ◆ insert empty frame .
#n4 ◆ nudge								. n1 ◇ None
#n4 ◆ hold for							. n1 ◇ None
#n4 ◆ come over							. n1 ◇ None


#n1 !!!! Important!!!!
#   we have issue with keyframes getting eaten by the process part.
#   I suspect it's because we are directly assigning keyframe positions to the keyframes
#   I should find a way to keep each keyframe in memmory and only apply them when the process is done.

#n1 !!! Grease Nudge Issue !!!
#   Grease Nudge is giving out an error on line 67:
#       list_id = int(np.where(selected_kf_x == keyframe.frame_number)[0])
#       TypeError: only size-1 arrays can be converted to Python scalars
#   Investigate the issue with Visual Studio Code






