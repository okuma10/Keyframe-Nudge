#version 330
in vec2 UV;

uniform int shape;
uniform int state;
uniform float width;
uniform vec4 idleColor;
uniform vec4 overColor;
uniform vec4 pressColor;
uniform vec2 size;
uniform vec2 dimensions;

vec2 uv;
vec3 mask;

out vec4 FragColor;

vec3 rectangle(vec2 uv, vec2 size);
vec3 plus(vec2 uv, vec2 size);

// ------------------- Main function -----------------------------

void main(void)
{
    vec2 uv = (-1. + 2. * UV)*(dimensions) ;
    vec3 color ;

    if(shape == 0){
        mask = plus(uv,size);
    }
    else if(shape == 1){
        mask = rectangle(uv,size.xy);
    }

    if(state == 0){
        if(shape == 0){
            vec3 mask2 = plus(uv,size-width);
            mask = mask*(1-mask2);

        }
        else if(shape == 1){
            vec3 mask2 = rectangle(uv,size-width);
            mask =  mask*(1-mask2);
        }
        color = idleColor.xyz;
    }
    else if (state == 1){
        color = overColor.xyz;
    }
    else if (state == 2){
        color = pressColor.xyz;
    }

    FragColor = vec4(color, mask);
}

//------------------- Shape Functions ---------------------------
vec3 rectangle(vec2 uv, vec2 size){


    float wSize = size.x / 2;
    float hSize = size.y / 2;

    vec3 mask;

    if(uv.x > -wSize && uv.x < wSize && uv.y>-hSize && uv.y <hSize){
        mask = vec3(1.0);
    }
    else{
       mask = vec3(0.0);
    }

    return mask;
}

vec3 plus(vec2 uv, vec2 size){
    vec3 mask;
    mask = rectangle(uv,size);
    mask += rectangle(uv,size.yx);
    return mask;
}