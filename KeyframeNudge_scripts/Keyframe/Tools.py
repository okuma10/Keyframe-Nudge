import bisect,bpy


def remapValue(oldRange, newRange, oldValue):
    a = oldRange[0]
    b = oldRange[1]
    c = newRange[0]
    d = newRange[1]

    newValue = c+(oldValue - a) * (d - c)/(b - a)

    return newValue


def getLeftRight(list,value):
    left  = bisect.bisect_left(list,value)
    right = bisect.bisect_right(list,value)

    if left != len(list):
        if list[left] == list[0]:
            left = 0
        else :left -= 1
    else: left -= 1

    if right >= len(list):
        right -= 1
    else: pass

    return [list[left],list[right]]


def isMarkerOnKeyframe(keyframeCoList, timelineMarkerPos):
    _isMarkerOnKeyframe = False

    if timelineMarkerPos in keyframeCoList:
        _isMarkerOnKeyframe = True
    else:
        _isMarkerOnKeyframe = False

    return _isMarkerOnKeyframe


def forceReDraw():
    areas = bpy.context.screen.areas
    for area in areas:
        area.tag_redraw()