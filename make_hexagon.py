from pattern import TriGrid, FilledTri, todeg, torad
import svgwrite as sw

# units in tenth of mm
HINGE_T = 2.5
L = 100
t=10
theta=0
origin=(200,200)

nX = 5
nY = 5                 
dwg = sw.Drawing(f'new_hexagon.svg',profile='tiny')

# set up grid
grid = TriGrid(L,nX,nY)

t_s = 6
theta_s = todeg(.2142)

t_b = 3
theta_b = todeg(.0952)

# smalls
grid.add_tri(0,3,t_s,theta_s,HINGE_T,'up','compressed')
grid.add_tri(0,3,t_s,theta_s,HINGE_T,'down','compressed')
grid.add_tri(1,3,t_s,theta_s,HINGE_T,'up','compressed')
grid.add_tri(1,3,t_s,theta_s,HINGE_T,'down','compressed')
grid.add_tri(2,3,t_s,theta_s,HINGE_T,'up','compressed')
grid.add_tri(0,2,t_s,theta_s,HINGE_T,'up','compressed')
grid.add_tri(0,2,t_s,theta_s,HINGE_T,'down','compressed')
grid.add_tri(2,2,t_s,theta_s,HINGE_T,'down','compressed')
grid.add_tri(3,2,t_s,theta_s,HINGE_T,'up','compressed')
grid.add_tri(0,1,t_s,theta_s,HINGE_T,'down','compressed')
grid.add_tri(1,1,t_s,theta_s,HINGE_T,'up','compressed')
grid.add_tri(3,1,t_s,theta_s,HINGE_T,'up','compressed')
grid.add_tri(3,1,t_s,theta_s,HINGE_T,'down','compressed')
grid.add_tri(1,0,t_s,theta_s,HINGE_T,'down','compressed')
grid.add_tri(2,0,t_s,theta_s,HINGE_T,'up','compressed')
grid.add_tri(2,0,t_s,theta_s,HINGE_T,'down','compressed')
grid.add_tri(3,0,t_s,theta_s,HINGE_T,'up','compressed')
grid.add_tri(3,0,t_s,theta_s,HINGE_T,'down','compressed')

# bigs
grid.add_tri(1,2,t_b,theta_b,HINGE_T,'up','compressed')
grid.add_tri(1,2,t_b,theta_b,HINGE_T,'down','compressed')
grid.add_tri(2,2,t_b,theta_b,HINGE_T,'up','compressed')
grid.add_tri(1,1,t_b,theta_b,HINGE_T,'down','compressed')
grid.add_tri(2,1,t_b,theta_b,HINGE_T,'up','compressed')
grid.add_tri(2,1,t_b,theta_b,HINGE_T,'down','compressed')


grid.meld_compressed_neighbors()

# draw the grid onto the drawing we set up
# grid.draw_grid(dwg)
grid.draw_pattern(dwg)

dwg.save()

