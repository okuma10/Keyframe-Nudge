#version 330
in vec2 UV;

//#n3 Stuff
uniform vec2 resolution;
uniform vec2 pos1;
uniform vec2 size;
uniform vec3 mouse;
uniform vec4 points;


// #n1 colors
uniform vec4 idleColor;
uniform vec4 overColor;
uniform vec4 pressColor;

// #n2 Shape Controls
uniform float lineWidth;
uniform float circleWidth;
uniform float circleSize;
// temps
//in VertexData
//{
//    vec4 v_position;
//    vec3 v_normal;
//    vec2 v_texcoord;
//} inData;


out vec4 fragColor;

mat2 Rotation(float angle);
float sdBox( in vec2 p, in vec2 b );

void main(void)
{
    vec2 uv = (UV*resolution)/resolution.x;
//    uv = inData.v_texcoord;
    vec3 col = vec3(0);
    vec2 uv2 = fract(uv)*4;
    vec2 position = vec2(.5,.5);
    
    
    vec3 images = vec3(0);
//    
//    for(int i=0; i<3; i++)
//    {
//        float box1 = sdBox((uv2-position+vec2(-i, 0))*Rotation(45), vec2(size.x,size.y)*2)*1.5;
//        images += vec3(smoothstep(0.1,0.09,abs(box1)+lineWidth));
//    }
    float box1 = sdBox(uv2-position,vec2(.1,.1)*2);
    images += vec3(smoothstep(0.1,0.09,abs(box1)+lineWidth));
    col = vec3(images);
    
    
    
    fragColor = vec4(uv,.5,1);
}

//////////////////////////////////////////////////////////////////////////////////////////////////////
///                                      Functions                                                 ///
float sdBox( in vec2 p, in vec2 b )
{
    vec2 d = abs(p)-b;
    return length(max(d,vec2(0))) + min(max(d.x,d.y),0.0);
}

mat2 Rotation(float angle)
{
    float rad = radians(angle);
    float c = cos(rad);
    float s = sin(rad);
    
    return mat2(c,-s,s,c);
}


