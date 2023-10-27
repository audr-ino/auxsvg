import svgwrite as sw
import math

def torad(deg):
    return deg * math.pi/180

def todeg(rad):
    return rad * 180/math.pi

def len_btwn(pt1,pt2):
    delX = pt2[0]-pt1[0]
    delY = pt2[1]-pt1[1]
    return (delX**2+delY**2)**(1/2)

# angle if you start at pt1 and go to pt2
def ang_btwn(pt1,pt2):
    delX = pt2[0]-pt1[0]
    delY = pt2[1]-pt1[1]
    return todeg(math.atan(delY/delX))

class Line(object):
    def __init__(self,pt1,pt2):
        self.pt1 = pt1
        self.pt2 = pt2
        self.L = len_btwn(pt1,pt2)
        self.theta = ang_btwn(pt1,pt2)

    @classmethod
    def ang_len(cls,pt1,L,theta):
        rad = torad(theta)
        pt2=(0,0)
        pt2[0]=pt1[0]+L*math.cos(rad)
        pt2[1]=pt1[1]+L*math.sin(rad)
        return cls(pt1,pt2)
    
    def x_to_y(self,x):
        rad = torad(self.theta)
        m = math.tan(rad)
        xo = self.pt1[0]
        yo = self.pt1[1]
        y = m*(x-xo)+yo
        return y
    
    def frac_thru(self,p):
        rad = torad(self.theta)
        ptX = self.pt1[0]+p*self.L*math.cos(rad)
        ptY = self.pt1[1]+p*self.L*math.sin(rad)
        return (ptX,ptY)

    def draw(self,dwg):
        print('Line: drawing line, actually in svg')
        drawn_line=dwg.line(self.pt1,self.pt2,stroke=sw.rgb(255,0,0,'%'))
        dwg.add(drawn_line)
    
class Triangle():
    def __init__(self,pts):
        self.pts=pts
        self.lines=[]
        self.lines.append(Line(pts[0],pts[1]))
        self.lines.append(Line(pts[1],pts[2]))
        self.lines.append(Line(pts[2],pts[0]))

    def __str__(self):
        return f'Triangle with points {self.pts}'
    
    @classmethod
    def equilateral(cls,pt,L,hx):
        pt1 = pt

        theta_up = torad(60*hx)
        theta_down = torad(60*hx-120)

        pt2x = pt1[0]+L*math.cos(theta_up)
        pt2y = pt1[1]+L*math.sin(theta_up)
        pt2=(pt2x,pt2y)

        pt3x = pt2[0]+L*math.cos(theta_down)
        pt3y = pt2[1]+L*math.sin(theta_down)
        pt3=(pt3x,pt3y)

        return cls([pt1,pt2,pt3])
    
    def draw(self,dwg):
        for i in range(3):
            print(f'Triangle: drawing line {i}')
            self.lines[i].draw(dwg)

class FancyDrawing(sw.Drawing):
    def __init__(self,filename,profile):
        print('Drawing initialized')
        super().__init__(filename,profile=profile)
        self.pts=[(0,0)]
        self.lines=[]
        self.shapes=[]
    
    def draw(self):
        for line in self.lines:
            print('FancyDrawing: drawing line')
            line.draw(self)
        for shape in self.shapes:
            print('FancyDrawing: drawing shape')
            shape.draw(self)



L = 100
origin=(100,100)

dwg = FancyDrawing('tri.svg',profile='tiny')

dwg.shapes.append(Triangle.equilateral(origin,L,1))
dwg.shapes.append(Triangle.equilateral(origin,L,3))
dwg.shapes.append(Triangle.equilateral(origin,L,5))

dwg.draw()
dwg.save()

