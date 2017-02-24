import math

"""
Gosper curve (flowsnake)

Replacement rules:
  A ==> A-B--B+A++AA+B-
  B ==> +A-BB--B-A++A+B

  In this case both A and B mean to move forward,
  + means to turn left 60 degrees and
  - means to turn right 60 degrees
  (Using a "turtle"-style program such as Logo.)
"""

def make_polyline(v_list, color='black', width=0.5):
    polyline = '<polyline points="'
    
    for v in v_list:
        polyline += '{0},{1} '.format(v[0], -v[1])
        
    polyline += '" stroke="{color}" '.format(color=color)
    polyline += 'stroke-width="{width}" '.format(width=width)
    polyline += 'fill="none" />'.format(color=color, width=width)
    polyline += '\n'

    return polyline

def dist(A, B):
    return ((A[0] - B[0])**2 + (A[1] - B[1])**2)**0.5

def vector_sum(A, B):
    return [A[i] + B[i] for i in range(len(A))]

def vector(start, terminal):
    # サイズが違ってもとりあえず無視
    return [terminal[i] - start[i] for i in range(len(start))]

def scalar_multiple(vector, k):
    return [component*k for component in vector]    

def rotate(vector, angle):
    c = math.cos(math.radians(angle))
    s = math.sin(math.radians(angle))
    return [c*vector[0] - s*vector[1], s*vector[0] + c*vector[1]]

def init_vector(P, Q, sgn=1):
    k = (7**0.5) /7
    v = scalar_multiple(vector(P, Q), k)
    c = (7**0.5)*5/14    # 5 / 2sqrt(7) 
    s = sgn*(21**0.5)/14 # sqrt(3) / 2sqrt(7) 
    return [c*v[0] - s*v[1], s*v[0] + c*v[1]]


def flowsnake(A, B, n):

    points = [A]
    points += _flowsnake_A(A, B, 0, n)

    return points

def _flowsnake_A(P, Q, n, n_max):
    """
    A ==> A-B--B+A++AA+B-
    """
    if n >= n_max:
        return [Q]

    else:
        _vec = init_vector(P, Q)
        _A0 = []   # なんとかならんかこれ
        _A1 = P[:]
     
        def forward():
            nonlocal _vec, _A0, _A1
            _A0 = _A1[:]
            _A1 = vector_sum(_A0, _vec)
     
        def rot_p():
            nonlocal _vec
            _vec = rotate(_vec, 60)
            
        def rot_n():
            nonlocal _vec
            _vec = rotate(_vec, -60)
     
        points = []
     
        # [A]-B--B+A++AA+B-
        forward()
        points += _flowsnake_A(_A0, _A1, n+1, n_max)
        
        # A-[B]--B+A++AA+B-
        rot_n()
        forward()
        points += _flowsnake_B(_A0,_A1, n+1, n_max)
     
        # A-B--[B]+A++AA+B-
        rot_n()
        rot_n()
        forward()
        points += _flowsnake_B(_A0,_A1, n+1, n_max)
        
        # A-B--B+[A]++AA+B-
        rot_p()
        forward()
        points += _flowsnake_A(_A0,_A1, n+1, n_max)
     
        # A-B--B+A++[A]A+B-
        rot_p()
        rot_p()
        forward()
        points += _flowsnake_A(_A0,_A1, n+1, n_max)
     
        # A-B--B+A++A[A]+B-
        forward()
        points += _flowsnake_A(_A0,_A1, n+1, n_max)
     
        # A-B--B+A++AA+[B]-
        rot_p()
        forward()
        points += _flowsnake_B(_A0,_A1, n+1, n_max)    
     
        return points


def _flowsnake_B(P, Q, n, n_max):
    """
    B ==> +A-BB--B-A++A+B
    """
    if n >= n_max:
        return [Q]

    else:
        _vec = init_vector(P, Q)
        _A0 = [] # なんとかならんかこれ
        _A1 = P[:]        
     
        def forward():
            nonlocal _vec, _A0, _A1
            _A0 = _A1[:]
            _A1 = vector_sum(_A0, _vec)
     
        def rot_p():
            nonlocal _vec
            _vec = rotate(_vec, 60)
            
        def rot_n():
            nonlocal _vec
            _vec = rotate(_vec, -60)
     
        points = []
     
        # +[A]-BB--B-A++A+B
        rot_p()
        forward()
        points += _flowsnake_A(_A0, _A1, n+1, n_max)
        
        # +A-[B]B--B-A++A+B
        rot_n()
        forward()
        points += _flowsnake_B(_A0,_A1, n+1, n_max)
     
        # +A-B[B]--B-A++A+B
        forward()
        points += _flowsnake_B(_A0,_A1, n+1, n_max)
        
        # +A-BB--[B]-A++A+B
        rot_n()
        rot_n()
        forward()
        points += _flowsnake_B(_A0,_A1, n+1, n_max)
     
        # +A-BB--B-[A]++A+B
        rot_n()
        forward()
        points += _flowsnake_A(_A0,_A1, n+1, n_max)
     
        # +A-BB--B-A++[A]+B
        rot_p()
        rot_p()
        forward()
        points += _flowsnake_A(_A0,_A1, n+1, n_max)
     
        # +A-BB--B-A++A+[B]
        rot_p()
        forward()
        points += _flowsnake_B(_A0,_A1, n+1, n_max)    
     
        return points


svg = '<?xml version="1.0" encoding="utf-8"?>'
svg += '''
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
  "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">'''
svg += '''
<svg xmlns="http://www.w3.org/2000/svg"
     xmlns:xlink="http://www.w3.org/1999/xlink"
     width="3000" height="3000" viewBox="-1000 -1000 2000 2000">
'''

v1 = [800, 300]
v2 = [200, 300]
v3 = [500, 300 - 300*(3**0.5)]

#svg+= make_polyline(flowsnake(v1,v2,0),color='blue', width=0.5)
#svg+= make_polyline(flowsnake(v1,v2,1),color='red', width=1)
svg+= make_polyline(flowsnake(v1,v2,3),color='green', width=1.5)
svg+= make_polyline(flowsnake(v2,v3,3),color='red', width=2)
svg+= make_polyline(flowsnake(v3,v1,3),color='blue', width=2.5)
#v_list1 = flowsnake(v1,v2,3)
#v_list2 = flowsnake(v1,v3,3)
#v_list3 = flowsnake(v3,v2,3)
#v_list = v_list1 + v_list2 + v_list3
#svg+= make_polyline(v_list,color='black', width=1.5)

svg += '</svg>'

f = open("flowsnake3.svg", "w", encoding="UTF-8")
f.write(svg)
f.close()
