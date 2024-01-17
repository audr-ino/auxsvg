from pattern import TriGrid, FilledTri, todeg, torad
import svgwrite as sw

# units in tenth of mm
HINGE_T = 2.5
L = 100
origin=(200,200)

dwg = sw.Drawing(f'unit_cell.svg',profile='tiny')

nX = 5
nY = 5  

# set up grid
grid = TriGrid(L,nX,nY)

t_s = 6
theta_s = todeg(.2142)

# bigs
grid.add_tri(1,2,t_s,theta_s,HINGE_T,'up','compressed')
grid.add_tri(1,2,t_s,theta_s,HINGE_T,'down','compressed')
grid.add_tri(2,2,t_s,theta_s,HINGE_T,'up','compressed')
grid.add_tri(1,1,t_s,theta_s,HINGE_T,'down','compressed')
grid.add_tri(2,1,t_s,theta_s,HINGE_T,'up','compressed')
grid.add_tri(2,1,t_s,theta_s,HINGE_T,'down','compressed')

grid.meld_compressed_neighbors()

# draw the grid onto the drawing we set up
# grid.draw_grid(dwg)

grid.draw_pattern(dwg)

dwg.save()