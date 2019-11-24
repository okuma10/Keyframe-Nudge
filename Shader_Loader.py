from bgl import *
from . import Logger
from pathlib import Path
import numpy as np
# from OpenGL.GL import *

parents = Path(__file__).parents
root_dir = Path(__file__).parent
# for parent in parents:
#     if parent.name == "BlenderDrawDev":
#         root_dir = str(parent)
# print(root_dir)
log_file = str(root_dir) + '\\UI\\Shaders\\shader.log'
shader_log = Logger.Log(log_file)
shader_log.clearFile()


class ShaderLoader:
    def __init__(self):
        self.shader = None
        self.log = shader_log
    def load_shader(self,shader_file):
        shader_source = ""
        with open(shader_file) as f:
            shader_source = f.read()
        f.close()
        return shader_source

    def compile_shader(self,vs,fs):
        self.log.setLevel(1)
        vert_s_name = vs.split("\\")[-1]
        frag_s_name = fs.split("\\")[-1]
        # self.log.print(f'{vertex_s_name}')
        self.log.print(f'{" Compiling Shader ":-^40}')
        self.log.print(f'{ f" vertex : {vert_s_name:>15}":.^40}')
        self.log.print(f'{f" fragment : {frag_s_name:>15} ":.^40}')
        vert_shader_source = self.load_shader(vs)
        frag_shader_source = self.load_shader(fs)


        statusVert    = Buffer(GL_INT,1)
        statusFrag    = Buffer(GL_INT,1)
        statusProgram = Buffer(GL_INT,1)
        program       = glCreateProgram()
        shaderVert    = glCreateShader(GL_VERTEX_SHADER)
        shaderFrag    = glCreateShader(GL_FRAGMENT_SHADER)

        glShaderSource(shaderVert, vert_shader_source)
        glShaderSource(shaderFrag, frag_shader_source)

        glCompileShader(shaderVert)
        glCompileShader(shaderFrag)
        glGetShaderiv(shaderVert, GL_COMPILE_STATUS, statusVert)
        glGetShaderiv(shaderFrag, GL_COMPILE_STATUS, statusFrag)
        if statusVert[0] == GL_TRUE   : self.log.print('Vertex Shader compilation successfull')
        if statusFrag[0] == GL_TRUE   : self.log.print('Fragment Shader compilation successfull')
        if statusVert[0] == GL_FALSE  : self.log.print('Vertex Shader compilation successfull')
        if statusFrag[0] == GL_FALSE  : self.log.print('Fragment Shader compilation successfull')

        glAttachShader(program, shaderVert)
        glAttachShader(program, shaderFrag)
        glLinkProgram(program)
        glGetProgramiv(program,GL_LINK_STATUS, statusProgram)
        if statusProgram[0] == GL_TRUE  : self.log.print('Program Linking Successfull')
        if statusProgram[0] == GL_FALSE :
            self.log.print('Program Linking Failed')

            info_log_Lenght = Buffer(GL_INT, 1)
            glGetProgramiv(program,GL_INFO_LOG_LENGTH,info_log_Lenght)
            self.log.print(f'Error: {info_log_Lenght[0]}')

            info_log = Buffer(GL_BYTE, info_log_Lenght[0]+1)
            glGetProgramInfoLog(program,info_log_Lenght[0],info_log_Lenght,info_log)
            message = []
            for char in info_log.to_list():
                message.append(char)

            message = np.array(message)
            message = message.tostring().decode('ascii')
            self.log.print(f'Error message: {message}')


        self.shader = program

        glDeleteShader(shaderVert)
        glDeleteShader(shaderFrag)

        self.log.print(f'{" Compiling END ":-^40}')
        self.log.setLevel(1)
        self.log.removeHandler()

    def activate(self):
        glUseProgram(self.shader)

    def deactivate(self):
        glUseProgram(0)


    def setVec2(self,location, fv1, fv2):
        glUniform2f(glGetUniformLocation(self.shader, location), fv1, fv2)

    def setVec3(self,location, fv1, fv2, fv3):
        glUniform3f(glGetUniformLocation(self.shader, location), fv1, fv2, fv3)

    def setVec4(self, location, fv1, fv2, fv3, fv4):
        glUniform4f(glGetUniformLocation(self.shader, location), fv1, fv2, fv3, fv4)

    def setMat4(self, location, mat4):
        glUniformMatrix4fv(glGetUniformLocation(self.shader, location), 1, GL_FALSE, mat4)

    def setFloat(self, location, fv1):
        glUniform1f(glGetUniformLocation(self.shader, location), fv1)

    def setInt(self, location, int1):
        glUniform1i(glGetUniformLocation(self.shader, location), int1)


    def getShader(self):
        return self.shader

