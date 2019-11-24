#version 330
in vec2 UV;

uniform vec2 dimensions;
uniform float grid_res;

out vec4 fragColor;

vec3 color = vec3(0.969, 0.718, 0.192);

float cross(vec2 uv, vec2 p, float size, float thickness){
    vec3 color = vec3(0);
    float width = size;
    float height = thickness;
    uv += p;
    if(uv.x>-width && uv.x<width && uv.y< height && uv.y>-height) color += vec3(1);
    if(uv.x>-height && uv.x<height && uv.y< width && uv.y>-width) color += vec3(1);

    return clamp(0,1,color.r);
}


void main(void)
{
    vec2 uv = (2*UV-1)*(dimensions/dimensions.y);

    vec2 U  = mod(gl_FragCoord.xy -.5, int(grid_res));
    vec4 m = vec4( U.x*U.y==.0 );

    color = mix(vec3(0),color,m.x);
    float size1 = .5;
    float size2 = .1;
    color = mix(color, vec3(0.647, 0.369, 0.918), cross(uv, vec2(1),    size1, size2));
    color = mix(color, vec3(0.647, 0.369, 0.918), cross(uv, vec2(-1,1), size1, size2));
    color = mix(color, vec3(0.647, 0.369, 0.918), cross(uv, vec2(1,-1), size1, size2));
    color = mix(color, vec3(0.647, 0.369, 0.918), cross(uv, vec2(0),    size1, size2));
    color = mix(color, vec3(0.647, 0.369, 0.918), cross(uv, vec2(-1),   size1, size2));


    fragColor = vec4(color, color.r);
}


