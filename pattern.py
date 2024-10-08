import svgwrite as sw
import math

# colors
red = sw.rgb(255,0,0,'%')
green = sw.rgb(0,255,0,'%')
blue = sw.rgb(0,0,255,'%')
black = sw.rgb(0,0,0,'%')
yellow = sw.rgb(255,255,0,'%')
cyan = sw.rgb(0,255,255,'%')
magenta = sw.rgb(255,0,255,'%')

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
    def __init__(self,pt1,pt2,color=red):
        self.color = color
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
    def ang_len(cls,pt1,L,theta,color=red):
        rad = torad(theta)
        pt2x=pt1[0]+L*math.cos(rad)
        pt2y=pt1[1]+L*math.sin(rad)
        pt2=(pt2x,pt2y)
        return cls(pt1,pt2,color)
    
    def x_to_y(self,x):
        y = self.m*x+self.b
        return y
    
    def frac_thru(self,p):
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

    def draw(self,dwg,color=None):
        if (color==None):
            color = self.color
        drawn_line=dwg.line(self.pt1,self.pt2,stroke=color)
        dwg.add(drawn_line)

class FilledTri():
    def __init__(self,pt,L,t,theta,HINGE_T,dir,expL,s,gap,type):
        # make everything an attribute
        self.pt = pt
        self.L = L
        self.t = t
        self.theta = theta
        self.HINGE_T = HINGE_T
        self.dir = dir
        self.expL = expL
        self.s = s
        self.gap = gap

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
        
        self.compromises = []
        self.outlines = []
        self.cuts = []
        self.wingtips = []
        self.triangle_lines = []

        if (type == "compressed"):

            self.pts = [pt]
            for ang in angs:
                # start the next line at the latest point
                self.outlines.append(Line.ang_len(self.pts[-1],L,ang))
                # add the end pt of the just drawn line to the pts list
                self.pts.append(self.outlines[-1].pt2)
            
            frac = t/L
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
            
            # breaks for neighbor aware alg
            self.breaks = [ends[1],ends[2],ends[0]]
        
        if (type=='expanded'):
            self.pts = [pt]
            for ang in angs:
                # start the next line at the latest point
                self.outlines.append(Line.ang_len(self.pts[-1],expL,ang))
                # add the end pt of the just drawn line to the pts list
                self.pts.append(self.outlines[-1].pt2)
            
            frac = t/expL
            wingtip_frac = (t+gap)/expL
        
            frac_pts=[]
            wingtip_frac_pts =[]
            
            for i in range(3):
                frac_pt = self.outlines[i].frac_thru(frac)
                frac_pts.append(frac_pt)
                cut_line = Line.ang_len(frac_pt,expL,cut_angs[i]+theta*theta_sign)
                self.cuts.append(cut_line)

                wingtip_frac_pt = self.outlines[i].frac_thru(wingtip_frac)
                wingtip_frac_pts.append(wingtip_frac_pt)
                wingtip_line = Line.ang_len(wingtip_frac_pt,expL,cut_angs[i]+theta*theta_sign)
                self.wingtips.append(wingtip_line)
            
            # intersection points w wingtip and cut
            ends=[]
            ends.append(self.wingtips[0].intersect(self.cuts[1]))
            ends.append(self.wingtips[1].intersect(self.cuts[2]))
            ends.append(self.wingtips[2].intersect(self.cuts[0]))

            for i in range(3):
                self.wingtips[i] = Line(wingtip_frac_pts[i],ends[i])
                if i<2:
                    self.cuts[i+1] = Line(frac_pts[i+1],ends[i])
                else:
                    self.cuts[0] = Line(frac_pts[0],ends[i])
            
            # creating the triangle
            cl = self.cuts[0].L
            hinge_frac = (cl-HINGE_T)/cl
            for i in range(3):
                end_pt = self.cuts[i].frac_thru(hinge_frac)
                self.triangle_lines.append(Line(ends[i],end_pt))
                self.cuts[i] = Line(frac_pts[i],self.triangle_lines[i].pt2)

    @classmethod
    def compressed(cls,pt,L,t,theta,HINGE_T,dir):
        rad = torad(theta)
        radW30 = torad(theta+30)
        s = (L-3*t)*math.cos(rad)+(3**.5)*(t-L)*math.sin(rad)
        gap = 2*s*math.sin(radW30)
        expL = L+gap
        return cls(pt,L,t,theta,HINGE_T,dir,expL,s,gap,"compressed")

    @classmethod
    def expanded(cls,pt,expL,t,theta,HINGE_T,dir):      
        rad = torad(theta)
        radW30 = torad(theta+30)
        numer = expL+6*t*math.cos(rad)*math.sin(radW30)-2*(3**.5)*t*math.sin(rad)*math.sin(radW30)
        denom = 1+2*math.cos(rad)*math.sin(radW30)-2*(3**.5)*math.sin(rad)*math.sin(radW30)
        L = numer/denom
        s = (L-3*t)*math.cos(rad)+(3**.5)*(t-L)*math.sin(rad)
        gap = 2*s*math.sin(radW30)
        return cls(pt,L,t,theta,HINGE_T,dir,expL,s,gap,"expanded")


    def draw_outline(self,dwg):
        for i in range(3):
            print(f'Triangle: drawing outline {i}')
            self.outlines[i].draw(dwg,black)

    def draw_cuts(self,dwg):
        for line in self.cuts:
            line.draw(dwg)
        for line in self.compromises:
            line.draw(dwg)
        for line in self.wingtips:
            line.draw(dwg)
        for line in self.triangle_lines:
            line.draw(dwg)
    
    def draw_color_cuts(self,dwg):
        colors = [red,green,blue]
        for i in range(3):
            line = self.cuts[i]
            print(f'Triangle: drawing color coded innerline')
            line.draw(dwg,colors[i])

class TriGrid():
    def __init__(self,L,nX,nY):
        self.nX = nX
        self.nY = nY
        self.L = L

        # making grid
        self.xLines = []
        self.yLines = []

        for n in range(nX):
            self.xLines.append(Line.ang_len((n*L,0),L*nY,60))
        for n in range(nY):
            self.yLines.append(Line.ang_len((0,n*L*math.sin(torad(60))),L*nX,0))
        
        # storing info
        self.grid_pts = {}
        self.tris={}

        for i in range(nX):
            grid_pts_row = {}
            tris_row = {}

            for j in range(nY):
                xLine = self.xLines[i]
                yLine = self.yLines[j]

                grid_pts_row[j] = yLine.intersect(xLine)
                tris_row[j] = {"up":None,"down":None}

            self.grid_pts[i]=grid_pts_row
            self.tris[i]=tris_row

    def add_tri(self,x,y,t,theta,HINGE_T,dir,type):
        print(f"grid: adding {dir} tri to {x}, {y} position")
        pt = self.grid_pts[x][y]
        if (type == 'expanded'):
            tri = FilledTri.expanded(pt,self.L,t,theta,HINGE_T,dir)
        elif (type=='compressed'):
            tri = FilledTri.compressed(pt,self.L,t,theta,HINGE_T,dir)
        self.tris[x][y][dir]=tri

    def meld_compressed_neighbors(self):
        # me cut order
        me_cuts = [2,1,0]
        # neighbor cut order
        nei_cuts = [2,0,1]

        for i in range(self.nX):
            for j in range(self.nY):
                print(f"melding neighbors of ({i},{j})")
                # # up tri
                me = self.tris[i][j]["up"]
                if (me):
                    # neighbors 
                    neighbors_keys = [[i,j,'down'],[i-1,j,'down'],[i,j-1,'down']]

                    for k in range(3):
                        keys = neighbors_keys[k]
                        neighbor=self.tris.get(keys[0],{}).get(keys[1],{}).get(keys[2])
                        
                        if (neighbor):
                            # cut numbers, type: Int
                            me_cut = me_cuts[k]
                            nei_cut = nei_cuts[k]

                            # actual cuts, type: Line
                            me_line = me.cuts[me_cut]
                            nei_line = neighbor.cuts[nei_cut]

                            # type: (Float, Float)
                            compromise_line = Line(me_line.pt1,nei_line.pt1)
                            compromise_pt = compromise_line.frac_thru(.5)

                            new_me_line = Line(me.breaks[me_cut],me_line.pt2)
                            new_nei_line = Line(neighbor.breaks[nei_cut],nei_line.pt2)  

                            self.tris[i][j]["up"].cuts[me_cut]=new_me_line
                            self.tris[i][j]["up"].compromises.append(Line(me.breaks[me_cut],compromise_pt))
                            self.tris[keys[0]][keys[1]][keys[2]].cuts[nei_cut]=new_nei_line    
                            self.tris[keys[0]][keys[1]][keys[2]].compromises.append(Line(neighbor.breaks[nei_cut],compromise_pt))                  
             
    def meld_expanded_neighbors(self):
        # me cut order
        me_cuts = [2,1,0]
        # neighbor cut order
        nei_cuts = [2,0,1]

        for i in range(self.nX):
            for j in range(self.nY):
                print(f"melding neighbors of ({i},{j})")
                # # up tri
                me = self.tris[i][j]["up"]
                if (me):
                    # neighbors 
                    neighbors_keys = [[i,j,'down'],[i-1,j,'down'],[i,j-1,'down']]

                    for k in range(3):
                        keys = neighbors_keys[k]
                        neighbor=self.tris.get(keys[0],{}).get(keys[1],{}).get(keys[2])
                        
                        if (neighbor):
                            # cut numbers, type: Int
                            me_cut = me_cuts[k]
                            nei_cut = nei_cuts[k]

                            # actual cuts, type: Line
                            me_line = me.cuts[me_cut]
                            nei_line = neighbor.cuts[nei_cut]

                            # type: (Float, Float)
                            compromise_line = Line(me_line.pt1,nei_line.pt1)
                            compromise_pt = compromise_line.frac_thru(.5)

                            new_me_line = Line(compromise_pt,me_line.pt2)
                            new_nei_line = Line(compromise_pt,nei_line.pt2)  

                            self.tris[i][j]["up"].cuts[me_cut]=new_me_line
                            self.tris[keys[0]][keys[1]][keys[2]].cuts[nei_cut]=new_nei_line  

                            # wingtips

                            me_wingtip = me.wingtips[me_cut]
                            nei_wingtip = neighbor.wingtips[nei_cut]

                            wt_compromise_line = Line(me_wingtip.pt1,nei_wingtip.pt1)
                            wt_compromise_pt = wt_compromise_line.frac_thru(.5)

                            new_me_wt = Line(wt_compromise_pt,me_wingtip.pt2)
                            new_nei_wt = Line(wt_compromise_pt,nei_wingtip.pt2)

                            self.tris[i][j]["up"].wingtips[me_cut]=new_me_wt
                            self.tris[keys[0]][keys[1]][keys[2]].wingtips[nei_cut]=new_nei_wt 
    
    def draw_grid(self,dwg):
        for line in self.xLines:
            line.draw(dwg,black)
        for line in self.yLines:
            line.draw(dwg,black)
    
    def draw_pattern(self,dwg):
        for i in range(self.nX):
            for j in range(self.nY):
                if(self.tris[i][j]["up"]):
                    self.tris[i][j]["up"].draw_outline(dwg)
                    self.tris[i][j]["up"].draw_cuts(dwg)
                if(self.tris[i][j]["down"]):
                    self.tris[i][j]["down"].draw_outline(dwg)
                    self.tris[i][j]["down"].draw_cuts(dwg)
