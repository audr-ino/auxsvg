import svgwrite as sw
import math

class Triangle():
    def __init__(self,pts):
        self.pts=pts

class FancyDrawing(sw.Drawing):
    def __init__(self,filename,profile):
        super().__init__(filename,profile=profile)
        self.pts=[(0,0)]
        self.shapes=[]

    def drawAngLine(self,pt,L,deg,store=None):
        if (store==None):
            store = self.pts

        rad = deg*math.pi/180
        Xf = pt[0] + L*math.cos(rad)
        Yf = pt[1] + L*math.sin(rad)
        line = self.line(pt,(Xf,Yf),stroke=sw.rgb(255,0,0,'%'))
        store.append((Xf,Yf))
        self.add(line)
    
    # hexants start as normal triangle and go counterclockwise
    def drawEqTri(self,pt,L,hx,store=None):
        if(store==None):
            store = self.shapes
            
        tripts = [pt]
        dwg.drawAngLine(tripts[-1],L,(60*hx),tripts)
        dwg.drawAngLine(tripts[-1],L,(60*hx-120),tripts)
        dwg.drawAngLine(tripts[-1],L,(60*hx+120),tripts)
        store.append(Triangle(tripts[1:]))


dwg = FancyDrawing('tri.svg',profile='tiny')

L = 100
origin=(100,100)
dwg.drawEqTri(origin,L,1)
dwg.drawEqTri(origin,L,3)
dwg.drawEqTri(origin,L,5)

dwg.save()
