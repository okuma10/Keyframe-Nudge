import numpy
from .ExternalModules.PIL import Image
from bgl import *

class Texture:
    def __init__(self,file_path):
        self.texture = Buffer(GL_INT,1)
        glGenTextures(1, self.texture)
        glBindTexture(GL_TEXTURE_2D, self.texture[0])
        # Set the texture wrapping parameters
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        # Set texture filtering parameters
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        # load image
        image = Image.open(file_path)
        self.image_dimensions = [image.width, image.height]
        # create GL_RGB and GL_RGBA depending on input
        if image.mode == "RGBA":
            image = image.transpose(Image.FLIP_TOP_BOTTOM)
            image_data = numpy.array( list(image.getdata()), numpy.uint16 )
            imageBuffer = Buffer(GL_BYTE, (len(image_data), 3), image_data)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width, image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, imageBuffer)
        elif image.mode == "RGB":
            image = image.transpose(Image.FLIP_TOP_BOTTOM)
            image_data = numpy.array( list(image.getdata()), numpy.uint8 )
            imageBuffer = Buffer(GL_BYTE,(len(image_data),3), image_data)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image.width, image.height, 0, GL_RGB, GL_UNSIGNED_BYTE, imageBuffer)

    def getTexID(self):
        return self.texture

    def getImageDimensions(self):
        return self.image_dimensions

    def Bind(self):
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D,self.texture[0])
