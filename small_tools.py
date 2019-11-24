import bpy
import numpy as np
from .ExternalModules.pyrr import Vector3

point1   = Vector3([ 50, 100, 0])
point2   = Vector3([100, 150, 0])
control1 = Vector3([ 50, 150, 0])


class QadricBezier:
    def __init__(self, p1, c1, p2 , resolution):
        f = 1 / (resolution + 1) # increment based on resolution

        #n bezier function data
        P1 = p1                 # start point of bezier curve
        P2 = p2                 # end point of bezier curve
        C1 = c1                 # control point of bezier curve
        t = f                   # position of point along bezier curve

        #n final list
        self.point_list = []

        #n  Process
        for i in range(0,resolution):
            x = pow((1 - t), 2) * P1[0] + 2 * (1 - t) * t * C1[0] + pow(t, 2) * P2[0]
            y = pow((1 - t), 2) * P1[1] + 2 * (1 - t) * t * C1[1] + pow(t, 2) * P2[1]
            self.point_list.append((x, y,0))
            t += f

    #n return points
    def getPoints(self):
        return self.point_list


class squareAlongLine:
    def __init__(self, p1, r, angle, center):
        distance = r
        C1 = p1
        Rx = C1[0] + (np.cos(np.deg2rad(angle))*distance)
        Ry = C1[1] + (np.sin(np.deg2rad(angle))*distance)

        radius = np.cos(np.deg2rad(angle))*distance

        #n   x                      y
        #n point 1
        if p1[0] < center[0] and  p1[1] < center[1]: #n if point is to the left and down from center
            if   Rx >= center[0] :                   #  if X reaches or goes beyound the center
                dif  = center[0] - C1[0]             #  find difference between the center.x and Point.x
                Ry   = C1[1] + dif                   #  corner circle center.y = adding difference to Point.y
                Rx   = center[0]                     #  corner circle center.x = object center.y
                radius = dif                         #  cornder circle radius  = the difference
            elif Ry >= center[1] :
                dif  = center[1] - C1[1]
                Rx   = C1[0] + dif
                Ry   = center[1]
                radius = dif
            else:pass

        #n point 2
        elif p1[0] > center[0] and  p1[1] < center[1]:
            if   Rx <= center[0] :
                dif = center[0] - C1[0]
                Ry = C1[1] - dif
                Rx = center[0]
                radius = dif
            elif Ry >= center[1] :
                dif = center[1] - C1[1]
                Rx = C1[0] - dif
                Ry = center[1]
                radius = dif
            else:pass

        #n point 3
        elif p1[0] > center[0] and  p1[1] > center[1]:#pass
            if   Rx <= center[0] :
                dif = center[0] - C1[0]
                Ry = C1[1] + dif
                Rx = center[0]
                radius = dif
            elif Ry <= center[1] :
                dif = center[1] - C1[1]
                Rx = C1[0] + dif
                Ry = center[1]
                radius = dif
            else:pass

        #n point 4
        elif p1[0] < center[0] and  p1[1] > center[1]: # pass
            if   Rx >= center[0] :
                dif = center[0] - C1[0]
                Ry = C1[1] - dif
                Rx = center[0]
                radius = dif
            elif Ry <= center[1] :
                dif = center[1] - C1[1]
                Rx = C1[0] - dif
                Ry = center[1]
                radius = dif
            else:pass
        else:pass

        P1 = (C1[0], Ry, 0)
        P2 = (Rx, C1[1], 0)

        self.point_list = [
                           (Rx,Ry,0),
                           radius
                           ]
    def get_points(self):
            return self.point_list


class ParametricCircle:
    def __init__(self,center, r, resolution,sector=int):
        f = 90/resolution
        t = f
        self.point_list=[]
        if sector == 1:
            t = 0
            x = center[0] + r * np.cos(np.deg2rad(t))
            y = center[1] + r * np.sin(np.deg2rad(t))
            self.point_list.append((x,y,0))

            for i in range(0,resolution):
                x = center[0] + r*np.cos(np.deg2rad(t))
                y = center[1] + r*np.sin(np.deg2rad(t))

                self.point_list.append((x,y,0))
                t += f

            x = center[0] + r * np.cos(np.deg2rad(90))
            y = center[1] + r * np.sin(np.deg2rad(90))
            self.point_list.append((x, y, 0))

        if sector == 2:
            t = 90
            x = center[0] + r * np.cos(np.deg2rad(t))
            y = center[1] + r * np.sin(np.deg2rad(t))
            self.point_list.append((x, y, 0))
            t += f
            for i in range(0, resolution):
                x = center[0] + r * np.cos(np.deg2rad(t))
                y = center[1] + r * np.sin(np.deg2rad(t))

                self.point_list.append((x, y, 0))
                t += f

            x = center[0] + r * np.cos(np.deg2rad(180))
            y = center[1] + r * np.sin(np.deg2rad(180))
            self.point_list.append((x, y, 0))

        if sector == 3:
            t = 180
            x = center[0] + r * np.cos(np.deg2rad(t))
            y = center[1] + r * np.sin(np.deg2rad(t))
            self.point_list.append((x, y, 0))
            t += f
            for i in range(0, resolution):
                x = center[0] + r * np.cos(np.deg2rad(t))
                y = center[1] + r * np.sin(np.deg2rad(t))

                self.point_list.append((x, y, 0))
                t += f

            x = center[0] + r * np.cos(np.deg2rad(270))
            y = center[1] + r * np.sin(np.deg2rad(270))
            self.point_list.append((x, y, 0))

        if sector == 4:
            t = 270
            x = center[0] + r * np.cos(np.deg2rad(t))
            y = center[1] + r * np.sin(np.deg2rad(t))
            self.point_list.append((x, y, 0))
            t += f
            for i in range(0, resolution):
                x = center[0] + r * np.cos(np.deg2rad(t))
                y = center[1] + r * np.sin(np.deg2rad(t))

                self.point_list.append((x, y, 0))
                t += f

            x = center[0] + r * np.cos(np.deg2rad(360))
            y = center[1] + r * np.sin(np.deg2rad(360))
            self.point_list.append((x, y, 0))


    def getPoints(self):
        return self.point_list


class GetThemeColors:
    def __init__(self):
        self.background = None
        self.passive = None
        self.active = None

        current_theme = bpy.context.preferences.themes.items()[0][0]
        outliner = bpy.context.preferences.themes[current_theme].outliner
        view_3d = bpy.context.preferences.themes[current_theme].view_3d
        user_interface = bpy.context.preferences.themes[current_theme].user_interface.wcol_toolbar_item

        self.active = view_3d.object_active
        self.active2 = view_3d.object_selected
        self.text = user_interface.text
        self.passive = view_3d.camera
        self.background = user_interface.inner

def remapRange(a, b, c, d, t):
    oldNormal = (t-a)/(b-a)
    remapedValue = oldNormal*(d-c)+c
    if remapedValue < c:
        remapedValue = c
    elif remapedValue > d:
        remapedValue = d
    return remapedValue




