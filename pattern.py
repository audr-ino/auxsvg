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

    def draw(self,dwg,color=sw.rgb(255,0,0,'%')):
        print('Line: drawing line, actually in svg')
        drawn_line=dwg.line(self.pt1,self.pt2,stroke=color)
        dwg.add(drawn_line)

class FilledTri():
    def __init__(self,pt,L,t,theta,dir):

        if (dir=='up'):
            angs = [180,60,300]
            cut_angs = [120,0,240]
            theta_sign = 1
        elif (dir=='down'):
            angs = [60,180,300]
            cut_angs = [120,240,0]
            theta_sign = -1
        else:
            raise Exception('dir arg should be "up" or "down"')
        
        self.pts = [pt]
        self.outlines = []
        for ang in angs:
            # start the next line at the latest point
            self.outlines.append(Line.ang_len(self.pts[-1],L,ang))
            # add the end pt of the just drawn line to the pts list
            self.pts.append(self.outlines[-1].pt2)
        
        frac = t/L
        self.cuts = []
        frac_pts=[]

        for i in range(3):
            frac_pt = self.outlines[i].frac_thru(frac)
            frac_pts.append(frac_pt)
            cut_line = Line.ang_len(frac_pt,L,cut_angs[i]+theta*theta_sign)
            self.cuts.append(cut_line)

        # intersection points with each other
        ends=[]
        ends.append(self.cuts[0].intersect(self.cuts[2]))
        ends.append(self.cuts[1].intersect(self.cuts[0]))
        ends.append(self.cuts[2].intersect(self.cuts[1]))

        for i in range(3):
            self.cuts[i] = Line(frac_pts[i],ends[i])
            self.cuts[i].shorten(HINGE_T)

        # s
        s_line = Line(ends[0],ends[1])
        self.s = s_line.L

        # expansion ratio
        close_A = 3*(3**.5)*.5*(L)**2
        exp_A= 3*(3**.5)*.5*(L+2*self.s*math.sin(torad(30+theta)))**2
        self.E = exp_A/close_A
    
    def draw_outline(self,dwg):
        for i in range(3):
            print(f'Triangle: drawing outline {i}')
            self.outlines[i].draw(dwg)

    def draw_cuts(self,dwg):
        for line in self.cuts:
            print(f'Triangle: drawing innerline')
            line.draw(dwg)

class TriGrid():
    def __init__(self,L,nX,nY):
        self.nX = nX
        self.nY = nY
        self.t = t
        self.theta = theta
        
        # making grid
        self.xLines = []
        self.yLines = []
        self.grid_pts = []
        for n in range(nX):
            self.xLines.append(Line.ang_len((n*L,0),L*nY,60))
        for n in range(nY):
            self.yLines.append(Line.ang_len((0,n*L*math.sin(torad(60))),L*nX,0))
        for xLine in self.xLines:
            for yLine in self.yLines:
                self.grid_pts.append(yLine.intersect(xLine))
    
    def draw_grid(self,dwg):
        for line in self.xLines:
            line.draw(dwg,sw.rgb(0,255,0,'%'))
        for line in self.yLines:
            line.draw(dwg,sw.rgb(0,255,0,'%'))



class PatternDrawing(sw.Drawing):
    def __init__(self,filename,profile):
        print('Drawing initialized')
        super().__init__(filename,profile=profile)
        self.pts=[(0,0)]
        self.lines=[]
        self.tris=[]
    
    def draw_inner(self):
        for tri in self.tris:
            print('PatternDrawing: drawing tri')
            tri.draw_cuts(self)
    
    def draw_oulines(self):
        for tri in self.tris:
            tri.draw_outline(self)


# dwg = PatternDrawing(f'L{L}_t{t}_theta{theta}_cell.svg',profile='tiny')
dwg = PatternDrawing(f'grid_test_cells.svg',profile='tiny')
grid = TriGrid(L,5,5)
# grid.draw_grid(dwg)

for pt in grid.grid_pts:
    dwg.tris.append(FilledTri(pt,L,t,theta,'up'))
    dwg.tris.append(FilledTri(pt,L,t,theta,'down'))

dwg.draw_inner()

dwg.save()

