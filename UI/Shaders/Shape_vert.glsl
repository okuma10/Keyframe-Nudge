#version 330
layout(location = 0) in vec3 vPos;
layout(location = 1) in vec2 vUV;

uniform mat4 mvp;

out vec2 UV;
void main()
{
    gl_Position = mvp * vec4(vPos, 1.);
    UV = vUV;
}
