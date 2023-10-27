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
    return todeg(math.atan2(delY,delX))

class Line(object):
    def __init__(self,pt1,pt2):
        self.pt1 = pt1
        self.pt2 = pt2
        self.L = len_btwn(pt1,pt2)
        self.theta = ang_btwn(pt1,pt2)

    @classmethod
    def ang_len(cls,pt1,L,theta):
        rad = torad(theta)
        pt2x=pt1[0]+L*math.cos(rad)
        pt2y=pt1[1]+L*math.sin(rad)
        pt2=(pt2x,pt2y)
        return cls(pt1,pt2)
    
    def x_to_y(self,x):
        rad = torad(self.theta)
        m = math.tan(rad)
        xo = self.pt1[0]
        yo = self.pt1[1]
        y = m*(x-xo)+yo
        return y
    
    def frac_thru(self,p):
        print(f'Doing frac_thru on line with theta: {self.theta}')
        rad = torad(self.theta)
        ptX = self.pt1[0]+p*self.L*math.cos(rad)
        ptY = self.pt1[1]+p*self.L*math.sin(rad)
        return (ptX,ptY)

    def draw(self,dwg):
        print('Line: drawing line, actually in svg')
        drawn_line=dwg.line(self.pt1,self.pt2,stroke=sw.rgb(255,0,0,'%'))
        dwg.add(drawn_line)
    
class Triangle():
    def __init__(self,pts,innerlines=[]):
        self.pts=pts
        self.lines=[]
        self.innerlines=innerlines
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
    
    @classmethod
    def fillout(cls,pt,L,hx,t,theta):
        pt1 = pt

        theta_up = torad(60*hx)
        theta_down = torad(60*hx-120)

        pt2x = pt1[0]+L*math.cos(theta_up)
        pt2y = pt1[1]+L*math.sin(theta_up)
        pt2=(pt2x,pt2y)

        pt3x = pt2[0]+L*math.cos(theta_down)
        pt3y = pt2[1]+L*math.sin(theta_down)
        pt3=(pt3x,pt3y)

        # if hx is even, inner triange rotates ccw
        if(hx%2==0):
            pt_order = [pt1,pt3,pt2]
            angs = [0+60*hx-theta,120+60*hx-theta,240+60*hx-theta]

        # if hx is odd, inner triangle rotates cw
        else:
            pt_order = [pt1,pt2,pt3]
            angs = [-60+60*hx+theta,180+60*hx+theta,60+60*hx+theta]

        line1 = Line(pt_order[0],pt_order[1])
        line2 = Line(pt_order[1],pt_order[2])
        line3 = Line(pt_order[2],pt_order[0])

        # fraction along line
        frac = t/L

        pt1f = line1.frac_thru(frac)
        pt2f = line2.frac_thru(frac)
        pt3f = line3.frac_thru(frac)

        cut1 = Line.ang_len(pt1f,L/2,angs[0])
        cut2 = Line.ang_len(pt2f,L/2,angs[1])
        cut3 = Line.ang_len(pt3f,L/2,angs[2])

        return cls([pt1,pt2,pt3],innerlines=[cut1,cut2,cut3])
    
    def draw_outline(self,dwg):
        # draw outline
        for i in range(3):
            print(f'Triangle: drawing outline {i}')
            self.lines[i].draw(dwg)

    def draw_innerlines(self,dwg):
        # draw outline
        for line in self.innerlines:
            print(f'Triangle: drawing innerline')
            line.draw(dwg)

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
            shape.draw_outline(self)
            shape.draw_innerlines(self)
    
    def draw_inner(self):
        for shape in self.shapes:
            print('FancyDrawing: drawing shape')
            shape.draw_innerlines(self)


L = 100
t=10
theta=10
origin=(100,100)

dwg = FancyDrawing('tri.svg',profile='tiny')

for i in range(1,7):
    dwg.shapes.append(Triangle.fillout(origin,L,i,t,theta))


dwg.draw_inner()
dwg.save()

