import svgwrite as sw
import math

class FancyDrawing(sw.Drawing):
    def __init__(self,filename,profile):
        super().__init__(filename,profile=profile)
        self.pts=[(0,0)]
        self.shapes=[]

    def drawAngLine(self,pt,L,deg):

        rad = deg*math.pi/180
        Xf = pt[0] + L*math.cos(rad)
        Yf = pt[1] + L*math.sin(rad)
        line = self.line(pt,(Xf,Yf),stroke=sw.rgb(255,0,0,'%'))
        self.pts.append((Xf,Yf))
        self.add(line)


dwg = FancyDrawing('tri.svg',profile='tiny')

# equilateral triangle
L = 100
dwg.drawAngLine(dwg.pts[-1],L,60)
dwg.drawAngLine(dwg.pts[-1],L,-60)
dwg.drawAngLine(dwg.pts[-1],L,180)

dwg.save()
