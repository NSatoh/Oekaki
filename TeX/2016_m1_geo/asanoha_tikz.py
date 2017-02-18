from math import *

clip_x = 2
clip_y = 1.5
size = 0.52
TeX  = r"\begin{tikzpicture}" + "\n"
TeX += r"  \clip ({0},{1}) rectangle ({2},{3});".format(-clip_x,-clip_y,clip_x,clip_y)
TeX += "\n"

TeX += r"  \draw (0, {0}) -- (0, -{0});".format(clip_y) + "\n"

dx = size * sin(radians(60))


# vertical lines
x = dx
while x < clip_x:
    TeX += r"  \draw ({0:.6f}, {1}) -- ({0:.6f}, -{1});".format(x, clip_y) + "\n"
    TeX += r"  \draw (-{0:.6f}, {1}) -- (-{0:.6f}, -{1});".format(x, clip_y) + "\n"
    x += dx
    
# NE and SE lines
y0 = -clip_x * tan(radians(30))
y1 = -y0
TeX += r"  \draw (-{0}, {1:.6f}) -- ({0}, {2:.6f});".format(clip_x,y0,y1) + "\n"
TeX += r"  \draw (-{0}, {2:.6f}) -- ({0}, {1:.6f});".format(clip_x,y0,y1) + "\n"

dy = size
y2, y3 = y0,y1

y0 += dy
y1 += dy
y2 += -dy
y3 += -dy
while y0 < clip_y:
    TeX += r"  \draw (-{0}, {1:.6f}) -- ({0}, {2:.6f});".format(clip_x,y0,y1) + "\n"
    TeX += r"  \draw (-{0}, {1:.6f}) -- ({0}, {2:.6f});".format(clip_x,y2,y3) + "\n"
    TeX += r"  \draw (-{0}, {2:.6f}) -- ({0}, {1:.6f});".format(clip_x,y0,y1) + "\n"
    TeX += r"  \draw (-{0}, {2:.6f}) -- ({0}, {1:.6f});".format(clip_x,y2,y3) + "\n"
    y0 += dy
    y1 += dy
    y2 += -dy
    y3 += -dy

# other lines
x0 = 0
y0 = 0
dx = size * sin(radians(60)) * 2
dy = size * 0.5
l = size * sin(radians(60)) * 2 / 3

TeX += r"  \draw ({0:.6f},{2:.6f}) -- ({1:.6f},{2:.6f});".format(x0-l, x0+l, y0) + "\n"
TeX += r"  \draw ({0:.6f},{2:.6f}) -- ({1:.6f},{3:.6f});".format(x0-l*0.5, x0+l*0.5, y0-dy, y0+dy) + "\n"
TeX += r"  \draw ({0:.6f},{2:.6f}) -- ({1:.6f},{3:.6f});".format(x0-l*0.5, x0+l*0.5, y0+dy, y0-dy) + "\n"

x1 = x0
y1 = y0
x0 += dx
x1 += -dx

while y0 < clip_y + dy:
    while x0 < clip_x + l:
        TeX += r"  \draw ({0:.6f},{2:.6f}) -- ({1:.6f},{2:.6f});".format(x0-l, x0+l, y0) + "\n"
        TeX += r"  \draw ({0:.6f},{2:.6f}) -- ({1:.6f},{3:.6f});".format(x0-l*0.5, x0+l*0.5, y0-dy, y0+dy) + "\n"
        TeX += r"  \draw ({0:.6f},{2:.6f}) -- ({1:.6f},{3:.6f});".format(x0-l*0.5, x0+l*0.5, y0+dy, y0-dy) + "\n"
        TeX += r"  \draw ({0:.6f},{2:.6f}) -- ({1:.6f},{2:.6f});".format(x1-l, x1+l, y1) + "\n"
        TeX += r"  \draw ({0:.6f},{2:.6f}) -- ({1:.6f},{3:.6f});".format(x1-l*0.5, x1+l*0.5, y1-dy, y1+dy) + "\n"
        TeX += r"  \draw ({0:.6f},{2:.6f}) -- ({1:.6f},{3:.6f});".format(x1-l*0.5, x1+l*0.5, y1+dy, y1-dy) + "\n"        
        x0 += dx
        x1 += -dx

    x0, x1 = x1-dx*0.5, x0+dx*0.5
    y0 += dy
    y1 += -dy

TeX += r"\end{tikzpicture}"
print(TeX)
