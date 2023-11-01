import svgwrite as sw
import math

# units in tenth of mm
HINGE_T = 5
L = 150
t=10
theta=10
origin=(200,200)

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
        try:
            self.m  = (pt2[1]-pt1[1])/(pt2[0]-pt1[0])
        except ZeroDivisionError:
            self.m = float('inf')
        self.b = pt1[1]-self.m*pt1[0]

    @classmethod
    def ang_len(cls,pt1,L,theta):
        rad = torad(theta)
        pt2x=pt1[0]+L*math.cos(rad)
        pt2y=pt1[1]+L*math.sin(rad)
        pt2=(pt2x,pt2y)
        return cls(pt1,pt2)
    
    def x_to_y(self,x):
        y = self.m*x+self.b
        return y
    
    def frac_thru(self,p):
        print(f'Doing frac_thru on line with theta: {self.theta}')
        rad = torad(self.theta)
        ptX = self.pt1[0]+p*self.L*math.cos(rad)
        ptY = self.pt1[1]+p*self.L*math.sin(rad)
        return (ptX,ptY)
    
    def intersect(self,line):
        # parallel or overlapping
        if(self.m==line.m):
            return None
        elif(self.m==float('inf')):
            x = self.pt1[0]
            y = line.x_to_y(x)
            return (x,y)
        elif(line.m==float('inf')):
            x = line.pt1[0]
            y = self.x_to_y(x)
            return (x,y)
        else:
            x = (self.b-line.b)/(line.m-self.m)
            y = self.x_to_y(x)
            return (x,y)

    def shorten(self,cut):
        # anchors on pt1 and shortens where pt2 is
        rad = torad(self.theta)
        new_L = self.L-cut
        pt2x = self.pt1[0]+new_L*math.cos(rad)
        pt2y = self.pt1[1]+new_L*math.sin(rad)
        self.L = new_L
        self.pt2 = (pt2x,pt2y)

    def draw(self,dwg):
        print('Line: drawing line, actually in svg')
        drawn_line=dwg.line(self.pt1,self.pt2,stroke=sw.rgb(255,0,0,'%'))
        dwg.add(drawn_line)

class FilledTri():
    def __init__(self,pt,L,hx,t,theta):
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

        self.outlines = [line1,line2,line3] 
        # fraction along line
        frac = t/L

        pt1f = line1.frac_thru(frac)
        pt2f = line2.frac_thru(frac)
        pt3f = line3.frac_thru(frac)

        # cuts just go cross each other
        cut1 = Line.ang_len(pt1f,L,angs[0])
        cut2 = Line.ang_len(pt2f,L,angs[1])
        cut3 = Line.ang_len(pt3f,L,angs[2])

        # intersection points with each other
        end1 = cut1.intersect(cut3)
        end2 = cut2.intersect(cut1)
        end3 = cut3.intersect(cut2)

        # update cuts to end where they intersect
        cut1 = Line(pt1f,end1)
        cut2 = Line(pt2f,end2)
        cut3 = Line(pt3f,end3)

        # shorten each cut by the hinge thickness
        cut1.shorten(HINGE_T)
        cut2.shorten(HINGE_T)
        cut3.shorten(HINGE_T)

        self.cuts = [cut1,cut2,cut3]

        # s
        s_line = Line(end1,end2)
        self.s = s_line.L

        # expansion ratio
        close_A = 3*(3**.5)*.5*(L)**2
        exp_A= 3*(3**.5)*.5*(L+2*self.s*math.sin(torad(30+theta)))**2
        self.E = exp_A/close_A
    
    def draw_outline(self,dwg):
        for i in range(3):
            print(f'Triangle: drawing outline {i}')
            self.outlines[i].draw(dwg)
        
    def draw_cell_outline(self,dwg):
        # only the 2nd line will be part of that, for the cell
        self.outlines[1].draw(dwg)

    def draw_cuts(self,dwg):
        for line in self.cuts:
            print(f'Triangle: drawing innerline')
            line.draw(dwg)

class PatternDrawing(sw.Drawing):
    def __init__(self,filename,profile):
        print('Drawing initialized')
        super().__init__(filename,profile=profile)
        self.pts=[(0,0)]
        self.lines=[]
        self.tris=[]
    
    def draw(self):
        for line in self.lines:
            print('PatternDrawing: drawing line')
            line.draw(self)
        for tri in self.tris:
            print('PatternDrawing: drawing tri')
            tri.draw_outline(self)
            tri.draw_cuts(self)
    
    def draw_inner(self):
        for tri in self.tris:
            print('PatternDrawing: drawing tri')
            tri.draw_cuts(self)
    
    def draw_cell(self):
        self.draw_inner()
        for tri in self.tris:
            tri.draw_cell_outline(self)

# dwg = PatternDrawing(f'L{L}_t{t}_theta{theta}_cell.svg',profile='tiny')
dwg = PatternDrawing(f'broken_t_test.svg',profile='tiny')


for i in range(1,6):
    dwg.tris.append(FilledTri(origin,L,i,t,theta))
dwg.tris.append(FilledTri(origin,L,6,t+5,theta))


dwg.draw_cell()
dwg.save()

