import blf
from pathlib import Path
from ...ExternalModules.pyrr import Vector3

# find root dir
root_dir = None
tree_dir = Path(__file__).parents
for up_dir in tree_dir:
    if up_dir.name == "BlenderDrawDev":
        root_dir = up_dir
    else:pass
parent = str(Path(__file__).parent)
log_file  = parent + '\\Logs\\Shapes'


#n Text Object
class Text:
    def __init__(self,font,type,size):

        dir = '\\UI\\Fonts\\'
        font1 = 'EXO2.0-'
        font2 = 'bonn_'
        bold = 'Bold'
        extraBold = 'ExtraBold'
        regular = 'Regular'
        light =  'Light'
        format = ['.otf','.ttf']

        self.font_info  = {
                                        'font_id': None,
                                        'font_handler': None,
                                        'loaded_font' :None
                                        }
        filepath = None
        if font == 'Exo':
            if type == 'Bold':
                filepath = parent[:-10] + dir + font1 + bold + format[0]
                self.font_info['loaded_font'] = filepath
            elif type == 'ExtraBold':
                filepath = parent[:-10] + dir + font1 + extraBold + format[0]
                self.font_info['loaded_font'] = filepath
            elif type == 'Regular':
                filepath = parent[:-10] + dir + font1 + regular + format[0]
                self.font_info['loaded_font'] = filepath
            elif type == 'Light':
                filepath = parent[:-10] + dir + font1 + light + format[0]
                self.font_info['loaded_font'] = filepath

        elif font == 'Bonn':
            if type == 'Bold':
                filepath = parent[:-10] + dir + font2 + bold + format[1]
            elif type == 'ExtraBold':
                print('This font does not have Extra Bold')
                filepath = None
            elif type == 'Regular':
                filepath = parent[:-10] + dir + font2 + regular + format[1]
            elif type == 'Light':
                filepath = parent[:-10] + dir + font2 + light + format[1]

        self.parent = Vector3([0,0,0])
        self.position = Vector3([0,0,0])
        self.pos_pus_parent = Vector3([
                            self.parent.x + self.position.x,
                            self.parent.y + self.position.y,
                            self.parent.z + self.position.z,
                         ])

        self.font_info['font_id'] = blf.load(filepath)
        blf.size(self.font_info['font_id'], size, 72)
        blf.enable(self.font_info['font_id'],1)


    def setPos(self, x, y, z):
        self.position = Vector3([x,y,z])
        self.pos_pus_parent = Vector3([
                            self.parent.x + self.position.x,
                            self.parent.y + self.position.y,
                            self.parent.z + self.position.z,
                         ])
        blf.position(self.font_info['font_id'], *self.pos_pus_parent)

    def setColor(self, R, G, B, A):
        blf.color(self.font_info['font_id'], R, G, B, A)

    def setRot(self, angle):
        blf.rotation(self.font_info['font_id'], angle)

    def setScale(self, scale):
        blf.size(self.font_info['font_id'], scale, 72)

    def draw(self, text=str):
        blf.position(self.font_info['font_id'],*self.pos_pus_parent)
        blf.draw(self.font_info['font_id'], text)

    def getDimensions(self,text_string):
        dimensions = blf.dimensions(self.font_info['font_id'],text_string)
        return dimensions

    def setParent(self,pX,pY,pZ):
        self.parent = Vector3([pX,pY,pZ])
        self.pos_pus_parent = Vector3([
            self.parent.x + self.position.x,
            self.parent.y + self.position.y,
            self.parent.z + self.position.z,
        ])
        blf.position(self.font_info['font_id'], *self.pos_pus_parent)

    def updatePos(self):
        self.pos_pus_parent = Vector3([
            self.parent.x + self.position.x,
            self.parent.y + self.position.y,
            self.parent.z + self.position.z,
        ])
        blf.position(self.font_info['font_id'], *self.pos_pus_parent)

    def getFontInfo(self):
        return self.font_info