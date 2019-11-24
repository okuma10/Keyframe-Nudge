# version 330
in vec2 UV;

//#n3 Stuff
uniform vec2 resolution;
uniform vec2 position;
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

vec4 object;
vec4 stateColor;

out vec4 fragColor;

float line(vec2 uv, vec2 p1, vec2 p2, float width);
float df_circ(in vec2 p, in vec2 c, in float r);
vec2 posOnLine(vec2 p1,vec2 p2, float x);
float dimondDF(vec2 uv);

void main(void)
{
    float aa = resolution.y*.0001;
    float sCprop = .6;
    vec2 uv = UV*resolution;
    vec2 p1 = points.xy; vec2 p2 = points.zw;
    //#n8 position control
    vec2 _p1 = p1 + position;
    vec2 _p2 = p2 + position;
    
    // #n8 line
    float _line = line(uv,_p1,_p2,lineWidth);
    float line_mask = smoothstep(.01-aa, .01+aa, _line);
    
    // #n8 Position On Line
    vec2 pos;
    if(mouse.x < _p1.x+(circleSize*.8)){
        pos = posOnLine(_p1,_p2,_p1.x+(circleSize*.8));
    }
    else if(mouse.x > _p2.x-(circleSize*.8)){
        pos = posOnLine(_p1,_p2,_p2.x-(circleSize*.8));
    }
    else{
        pos = posOnLine(_p1,_p2,mouse.x);
    }
    

    //  dragable daimond
    float scale1 = 0.3 -1 ;
    mat2 scale = mat2(scale1,0,0,scale1);
    float daimond = smoothstep(circleSize+.5, circleSize-.5,dimondDF((uv-pos)*scale));
    float daimond1 = smoothstep(circleSize+.5, circleSize-.5,dimondDF((uv-pos)));
    float inner_daimond = smoothstep((circleSize) + 0.5, (circleSize) - 0.5, dimondDF((uv-pos)*scale)*1+lineWidth*.8);
    float d_outline = daimond - inner_daimond;

    float _daimond;

    // solid fill
    //  at Points
    //  P1
    float p_s =0.8;
    float _p1_daimond = smoothstep( (circleSize*p_s),
                                    (circleSize*p_s)-1,
                                    dimondDF(uv-_p1));
    float _p1_inner_daimond = smoothstep(   (circleSize*p_s),
                                            (circleSize*p_s)-1,
                                            dimondDF(uv-_p1)*1+lineWidth*p_s);
    float _p1_outline = _p1_daimond-_p1_inner_daimond;
    //  P2
    float _p2_daimond = smoothstep( (circleSize*p_s),
                                    (circleSize*p_s)-1,
                                    dimondDF(uv-_p2));
    float _p2_inner_daimond = smoothstep(   (circleSize*p_s),
                                            (circleSize*p_s)-1,
                                            dimondDF(uv-_p2)*1+lineWidth*p_s);
    float _p2_outline = _p2_daimond-_p2_inner_daimond;


    float circleF1 = smoothstep((circleSize*.5)+1,
                                (circleSize*.5)-1,
                                length(uv - _p1)); // mask for line
    float circleF2 = smoothstep((circleSize*.5)+1,
                                (circleSize*.5)-1,
                                length(uv - _p2)); // mask for line
    float circle1 = smoothstep( (lineWidth*.5),
                                (lineWidth*.5)-1,
                                df_circ(uv,_p1,circleSize*.6));
    float circle2 = smoothstep( (lineWidth*.5),
                                (lineWidth*.5)-1,
                                df_circ(uv,_p2,circleSize*.6));

    float pCirc_mask ;
    float slide_mask;

    line_mask = mix(line_mask,0,_p1_daimond + _p2_daimond);
    pCirc_mask = _p1_outline + _p2_outline ;

    // control Silder's color based on state
    if (mouse.z == 1){
        stateColor = overColor;
        slide_mask = mix(slide_mask,1,daimond1 + d_outline);
    }
    else if (mouse.z == 2){
        stateColor = pressColor;
        slide_mask = mix(slide_mask,1,daimond1 + d_outline);
    }
    else{
        stateColor = idleColor;
        slide_mask = mix(slide_mask,1,daimond1);
    }

    // combine objects
    object = mix(vec4(0),idleColor,clamp(line_mask+pCirc_mask, 0., 1.));
    object = mix(object,stateColor,slide_mask);
    float alpha = clamp(line_mask+pCirc_mask+slide_mask,-0.,1.);

    fragColor = vec4(object.rgb,alpha);
}

//  #n2 functions
float line(vec2 uv, vec2 p1, vec2 p2, float width){
    float Length = distance(p1,p2);
    vec2 Slope = (p1-p2)/Length;
    
    vec2 Normal = Slope.yx*vec2(-1,1);
    
    float LineWidth = width*.5-abs(dot(uv-p1,Normal));
    float LineLenght = Length/2-abs(dot(uv-(p1+p2)/2, Slope));
    float Line = clamp(min(LineWidth,LineLenght),0,1);

    return Line;
}

float df_circ(in vec2 p, in vec2 c, in float r)
{
    return abs(r - length(p - c));
}

vec2 posOnLine(vec2 p1,vec2 p2, float x){
    float m = (p2.y-p1.y)/(p2.x-p1.x);
    float c = p1.y- m*p1.x;
    vec2 pos = vec2(x, m*x + c);
    return pos;
}

float dimondDF(vec2 uv){
    uv = abs(uv);
    float c = dot(uv, normalize(vec2(1)));
    return c ;
}
