"""
Edmund Harriss による螺旋．
プラスチック比による長方形分割に正方形が現れることを利用．

"""

# Plastic Number
P_NUM = 1.3247179572

SVG_CIRCLE = '<path d="M {x1},{y1} '
SVG_CIRCLE += 'A {rx}, {ry} {x_axis_rotation} '
SVG_CIRCLE += '{large_arc_flag}, {sweep_flag} '
SVG_CIRCLE += '{x}, {y}" fill="none" stroke="black" stroke-width="4"/>'

SVG_LINE = '<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
SVG_LINE += 'stroke="blue" stroke-width="1"/>'

SVG_RECT = '<rect x="{x}" y="{y}" '
SVG_RECT += 'width="{w}" height="{h}" '
SVG_RECT += 'stroke="blue" stroke-width="1" fill="none"/>'

def dist(A, B):
    return ((A[0] - B[0])**2 + (A[1] - B[1])**2)**0.5

def vector_sum(A, B):
    return [A[i] + B[i] for i in range(len(A))]

def vector(start, terminal):
    # サイズが違ってもとりあえず無視
    return [terminal[i] - start[i] for i in range(len(start))]

def scalar_multiple(vector, k):
    return [component*k for component in vector]

def internal_divide(A, B, s, t):
    """
    ABを s : t に内分する点を返す
    """
    return [t/(s+t)*A[i] + s/(s+t)*B[i] for i in range(len(A))]
    

def perp_vec(vector, sgn=1):
    """
    反時計まわり90度回転 --> sgn=1
      時計まわり90度回転 --> sgn=-1
    """
    return scalar_multiple([-vector[1], vector[0]], sgn)

def harriss(A, B, n, rect_print_flag=True):
    vec_AD = scalar_multiple(perp_vec(vector(A, B)), P_NUM)
    D = vector_sum(A, vec_AD)
    C = vector_sum(B, vec_AD)

    global cnt
    cnt = 0
    
    [svg_hc, svg_rect] = _harriss(A, B, C, D, n, rect_print_flag)

    if rect_print_flag:
        svg_rect += SVG_RECT.format(x=A[0], y=A[1],
                                    w=dist(A,B), h=dist(A,D)) + '\n'
 
    return [svg_hc, svg_rect]

def _harriss(A, B, C, D, n, rect_print_flag):
    """
    D      C      D  R   C
    +--+---+      +--+---+
    |      |      |  |   |
    |      |     P+--+---+Q
    |      | -->  |  S   |　　
    |      |      |      |
    +--+---+      +--+---+
    A      B      A      B

    AB : AD = 1 : PlasticNumber のとき
      RSQD が正方形
      BQPA, PSRD は ABCDと相似(AB --> PS, BQ に対応) 

    長方形の外側に四分円弧BQを描く
    """
    if n < 1:
        return ('', '')

    global cnt
    cnt += 1
    
    P = internal_divide(A, D, 1, P_NUM**2 - 1)
    Q = internal_divide(B, C, 1, P_NUM**2 - 1)
    R = internal_divide(C, D, 1, P_NUM**2 - 1)
    S = internal_divide(Q, P, 1, P_NUM**2 - 1)

    # BQ に四分円弧(harriss curve)
    radius = dist(B,Q) * 1.41421356 * 0.5
    svg_hc = SVG_CIRCLE.format(
          x1=B[0], y1=B[1], rx=radius, ry=radius, 
          x_axis_rotation=0,
          large_arc_flag=0, sweep_flag=1,
          x=Q[0], y=Q[1]
        )
    svg_hc += '\n'

    # 最初の2回だけ消す小細工
    if cnt <= 2:
        svg_hc = ''
        
    # 四角形を描画(だが中身はline)
    svg_rect = ''
    if rect_print_flag:
        svg_rect = SVG_LINE.format(
            x1=P[0], y1=P[1], x2=Q[0], y2=Q[1] 
            ) 
        svg_rect += '\n'
        svg_rect += SVG_LINE.format(
            x1=R[0], y1=R[1], x2=S[0], y2=S[1] 
            ) 
        svg_rect += '\n'

    (next_svg_hc, next_svg_rect) = _harriss(B, Q, P, A, n-1, rect_print_flag)
    svg_hc += next_svg_hc
    svg_rect += next_svg_rect
     
    # こちらだけ描画回数を半分くらいに制限してみた(n-2)
    # わりときれい
    (next_svg_hc, next_svg_rect) = _harriss(P, S, R, D, n-2, rect_print_flag)
    svg_hc += next_svg_hc
    svg_rect += next_svg_rect

    return (svg_hc, svg_rect)


svg_head = '<?xml version="1.0" encoding="utf-8"?>'
svg_head += '''
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
  "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">'''
svg_head += '''
<svg xmlns="http://www.w3.org/2000/svg"
     xmlns:xlink="http://www.w3.org/1999/xlink"
     width="1000" height="1000" viewBox="-700 -700 1400 1400">
'''
svg_foot = '</svg>'


if __name__ == '__main__':
    n = 11
    A = [0,0]
    B = [400,0]
    (svg_hc, svg_rect) = harriss(A, B, n, False)

    svg = svg_head + '\n' + svg_hc + '\n' + svg_rect + '\n' + svg_foot

    f = open("harriss_spiral.svg", "w", encoding="UTF-8")
    f.write(svg)
    f.close()
