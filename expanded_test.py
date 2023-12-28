from pattern import TriGrid, FilledTri, todeg, torad
import svgwrite as sw

# units in tenth of mm
HINGE_T = 2.5
L = 100
t=10
theta=0
origin=(200,200)

dwg = sw.Drawing(f'expanded_test.svg',profile='tiny')

nX = 5
nY = 5

# set up grid
grid = TriGrid(L,nX,nY)

# add triangles
for i in range(nX):
    for j in range(nY):
        grid.add_tri(i,j,t+3,theta,HINGE_T,'up','expanded')
        grid.add_tri(i,j,t+i,theta,HINGE_T,'down','expanded')


grid.meld_expanded_neighbors()
grid.draw_pattern(dwg)

test = FilledTri.compressed(origin,1,.05,torad(-.0238),HINGE_T,'up')
print(test.expL)

dwg.save()