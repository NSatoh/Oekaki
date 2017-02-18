#coding:utf-8
'''
Created on 2013/07/22
大きさを指定して、ペンローズタイルのemathソースを生成させたい。
形状は、とりあえず正十角形状。長方形にclipを選べるようにしたいが、これはすぐ実装できるか。

triangleA                triangleB
                            36
     36                     |\               
     /\                     | \             
    /  \                    |B \         triangleA -> A + B           
72 /____\ 72                |裏 /\        triangleB -> B + A裏 + B裏
                            | /A \ 108  
      ／/\                  |/ ／/
    ／ /  \                 |／  /
  ／B / A  \                |B /
／___/______\               | /  
                            |/
                            36
のような感じで、最初はAを10個（表、裏、表、裏、....）用意して正十角形を作り、
そこからA, B を次々細分化していくことで頂点列を得る
重複する頂点の追加をどう制御しようかなあ。
遅いかもしれないが、とりあえず追加しようとする頂点が存在するか逐次チェックさせて、
存在するならその頂点番号を取得させる感じでいいかな。
@author: NSatoh
'''

import math
import copy
import datetime

size = 7 # 何周繰り返して表示するか．7ですでに重い
# そのまま、emathソースのwindow size にもなる。(-size,size)(-size,size)になる。

# 未実装
#clipping = False # clipping したい場合は True、したくない場合はFalse
#clipSizeX = 2 # clip する範囲の横半径
#clipSizeY = 3 # clip する範囲の縦半径

coloring = False # 色分けする場合は、Trueに。色を変えたい場合は以下を適当にいじる。
colorA = "mycolorA"
colorB = "mycolorB"


# 初期値
v = [[0,0]] # vertices; 原点と、正十角形
for i in range(10):
    vAdd = [size*math.cos(math.radians(90+36*i)),size*math.sin(math.radians(90+36*i))]
    v += [vAdd]

triangleA = [[0,2,1],[0,2,3],[0,4,3],[0,4,5],[0,6,5],[0,6,7],[0,8,7],[0,8,9],[0,10,9],[0,10,1]] # vertex の#を指定
triangleB = []

ratioI = (-1+math.sqrt(5))/2 # 内分用の比
ratioII = (3-math.sqrt(5))/2
"""
   /\            /\
  /  \ 1        /  \ ratioI    ratioI + ratioII = 1
 /____\        /____\
   ratioI        ratioII
   
           |\ 1            |\ ratioII
 1+ratioI  | \      ratioI | \
           | /             | /
           |/              |/
"""

def interiorDiv(ptI,ptII,rI,rII): # ptI--ptII を、rI:rII の比に内分する点のリストを返す。rI+rII=1になるように。
    return [ptI[num]*rII+ptII[num]*rI for num in range(2)]

# 細分化の実行
for cnt in range(size):
    nextTriA = []
    nextTriB = []
    for tri in triangleA:
        vAdd = interiorDiv(v[tri[0]],v[tri[1]],ratioI,ratioII)
        if vAdd in v: # 既にある頂点かどうか
            vNum = v.index(vAdd)
        else:
            vNum = len(v)
            v += [vAdd]
        nextTriA += [[tri[2], vNum, tri[1] ]]
        nextTriB += [[vNum, tri[2], tri[0] ]]
    print("completed A --> " + str(cnt))
    for tri in triangleB:
        vAddI = interiorDiv(v[tri[0]],v[tri[1]],ratioII,ratioI)
        vAddII = interiorDiv(v[tri[1]],v[tri[2]],ratioI,ratioII)
        if vAddI in v: # 既にある頂点かどうか
            vNumI = v.index(vAddI)
        else:
            vNumI = len(v)
            v += [vAddI]
        if vAddII in v: # 既にある頂点かどうか
            vNumII = v.index(vAddII)
        else:
            vNumII = len(v)
            v += [vAddII]
        nextTriA += [[vNumII, vNumI, tri[0] ]] # 裏向きA
        nextTriB += [[vNumII, tri[2], tri[0] ]] # B
        nextTriB += [[vNumI, vNumII, tri[1] ]] # 裏向きB
    triangleA = copy.deepcopy(nextTriA)
    triangleB = copy.deepcopy(nextTriB) # 遅そう・・・
    print("completed B --> " + str(cnt))

edges = [] # 重複描画を避けたいので、辺のリストを作る。が、これも遅そうな...
for tri in triangleA:
    e = [tri[0],tri[1]]
    e.sort
    if e not in edges:
        edges += [e]
    e = [tri[2],tri[0]]
    e.sort
    if e not in edges:
        edges += [e]
    #テスト用。以下のedgeは本来不要
    #e = [tri[2],tri[1]]
    #e.sort
    #if e not in edges:
    #    edges += [e]

for tri in triangleB:
    e = [tri[0],tri[1]]
    e.sort
    if e not in edges:
        edges += [e]
    e = [tri[2],tri[0]]
    e.sort
    if e not in edges:
        edges += [e]
    #テスト用。以下のedgeは本来不要
    #e = [tri[2],tri[1]]
    #e.sort
    #if e not in edges:
    #    edges += [e]

print("cpmplete: generating edges")



begin_TeX  = r"% x min: " + str(min([vertex[0] for vertex in v])) + ", x max: " + str(max([vertex[0] for vertex in v])) + "\n"
begin_TeX += r"% y min: " + str(min([vertex[1] for vertex in v])) + ", y max: " + str(max([vertex[1] for vertex in v])) + "\n"
begin_TeX += r"\begin{tikzpicture}" + "\n"

end_TeX = r"""\end{tikzpicture}"""

TeX =""

# カラーリング：emath用の設定のまま．まだps化してない．
coloring = False
if coloring:
    commonEdgeA = []# 面倒だが、三角形を2つつなげて色を塗る必要があるので、共通する辺のリストを作っておく
    for tri in triangleA:
        ce = [tri[1],tri[2]]
        ce.sort()
        commonEdgeA += [ce]
    for i,tri in enumerate(triangleA):
        if commonEdgeA[i] in commonEdgeA[i+1:]:
            triNum = i + 1 + commonEdgeA[i+1:].index(commonEdgeA[i])
            vNum = triangleA[triNum][0]
            output += r"\Nuritubusi<nuriiro="
            output += "%s>{" % colorA
            output += "(%2.6f,%2.6f)(%2.6f,%2.6f)(%2.6f,%2.6f)(%2.6f,%2.6f)" % (v[tri[0]][0],v[tri[0]][1],v[tri[1]][0],v[tri[1]][1],v[vNum][0],v[vNum][1],v[tri[2]][0],v[tri[2]][1])
            output += r"}"+"\n"
    commonEdgeB = []# 面倒だが、三角形を2つつなげて色を塗る必要があるので、共通する辺のリストを作っておく
    for tri in triangleB:
        ce = [tri[1],tri[2]]
        ce.sort()
        commonEdgeB += [ce]
    for i,tri in enumerate(triangleB):
        if commonEdgeB[i] in commonEdgeB[i+1:]:
            triNum = i + 1 + commonEdgeB[i+1:].index(commonEdgeB[i])
            vNum = triangleB[triNum][0]
            output += r"\Nuritubusi<nuriiro="
            output += "%s>{" % colorB
            output += "(%2.6f,%2.6f)(%2.6f,%2.6f)(%2.6f,%2.6f)(%2.6f,%2.6f)" % (v[tri[0]][0],v[tri[0]][1],v[tri[1]][0],v[tri[1]][1],v[vNum][0],v[vNum][1],v[tri[2]][0],v[tri[2]][1])
            output += r"}"+"\n"
    print("cpmplete: coloring")

sc = 1# scale
for e in edges:
    x0 = v[e[0]][0]*sc
    y0 = v[e[0]][1]*sc
    x1 = v[e[1]][0]*sc
    y1 = v[e[1]][1]*sc
    if max(abs(x0), abs(x1), abs(y0), abs(y1)) < 8:# clipping
        TeX += r"\draw "
        TeX += "({0:.6f}, {1:.6f}) -- ({2:.6f}, {3:.6f});".format(x0,y0,x1,y1)
        TeX += "\n"

output = begin_TeX + TeX + end_TeX

now = datetime.datetime.today()
filename = "penrose_%s%s%s_%s%s%s.tex" % (now.year, now.month, now.day, now.hour, now.minute, now.second)
f = open(filename,"w")
f.write(output)
f.close()

print(">>> complete all. ")
