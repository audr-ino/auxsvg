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
dwg = sw.Drawing(f'unitcell_expanded_hexagon.svg',profile='tiny')

# set up grid
grid = TriGrid(L,nX,nY)

# expL = 1.8
t_s = 9
theta_s = todeg(.0952)

#expL = 1.5
t_b = 7.5
theta_b = todeg(.2856)

# smalls
# grid.add_tri(0,3,t_s,theta_s,HINGE_T,'up','expanded')
# grid.add_tri(0,3,t_s,theta_s,HINGE_T,'down','expanded')
# grid.add_tri(1,3,t_s,theta_s,HINGE_T,'up','expanded')
# grid.add_tri(1,3,t_s,theta_s,HINGE_T,'down','expanded')
# grid.add_tri(2,3,t_s,theta_s,HINGE_T,'up','expanded')
# grid.add_tri(0,2,t_s,theta_s,HINGE_T,'up','expanded')
# grid.add_tri(0,2,t_s,theta_s,HINGE_T,'down','expanded')
# grid.add_tri(2,2,t_s,theta_s,HINGE_T,'down','expanded')
# grid.add_tri(3,2,t_s,theta_s,HINGE_T,'up','expanded')
# grid.add_tri(0,1,t_s,theta_s,HINGE_T,'down','expanded')
# grid.add_tri(1,1,t_s,theta_s,HINGE_T,'up','expanded')
# grid.add_tri(3,1,t_s,theta_s,HINGE_T,'up','expanded')
# grid.add_tri(3,1,t_s,theta_s,HINGE_T,'down','expanded')
# grid.add_tri(1,0,t_s,theta_s,HINGE_T,'down','expanded')
# grid.add_tri(2,0,t_s,theta_s,HINGE_T,'up','expanded')
# grid.add_tri(2,0,t_s,theta_s,HINGE_T,'down','expanded')
# grid.add_tri(3,0,t_s,theta_s,HINGE_T,'up','expanded')
# grid.add_tri(3,0,t_s,theta_s,HINGE_T,'down','expanded')

# bigs
grid.add_tri(1,2,t_b,theta_b,HINGE_T,'up','expanded')
grid.add_tri(1,2,t_b,theta_b,HINGE_T,'down','expanded')
grid.add_tri(2,2,t_b,theta_b,HINGE_T,'up','expanded')
grid.add_tri(1,1,t_b,theta_b,HINGE_T,'down','expanded')
grid.add_tri(2,1,t_b,theta_b,HINGE_T,'up','expanded')
grid.add_tri(2,1,t_b,theta_b,HINGE_T,'down','expanded')


grid.meld_expanded_neighbors()

# draw the grid onto the drawing we set up
# grid.draw_grid(dwg)
grid.draw_pattern(dwg)

dwg.save()

