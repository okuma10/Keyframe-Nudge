#version 330

in vec2 UV;

uniform vec4 color;
uniform sampler2D maskTexture;
uniform int state;

vec2 uv;
vec2 texUV;
vec3 Texture;

out vec4 fragColor;

void main()
{
    uv = UV;
    vec3 fillColor = color.rgb;

    texUV = uv;

    Texture = texture(maskTexture,texUV).rgb;
    float mask = Texture.r;

    if (state == 2){
        vec3 bgColor = color.rgb;
        mask = mix(1,0,mask);
        fillColor = mix(bgColor,vec3(1),mask);

        fragColor = vec4(fillColor,1);
    }
    else {
        fragColor = vec4(fillColor, mask);
    }
}
