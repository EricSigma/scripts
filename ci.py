import pylab
import numpy as np
import matplotlib.pyplot as plt
import math
import random

# a dos columnas: 3+3/8 (ancho, in)
# a una columna : 6.5   (ancho  in)

golden_mean = (math.sqrt(5)-1.0)/2.0        # Aesthetic ratio
fig_width = 3+3/8 			    			# width  in inches
fig_height = fig_width*golden_mean          # height in inches
fig_size =  [fig_width,fig_height]

params = {'backend': 'ps',
          'axes.titlesize': 8,
          'axes.labelsize': 9,
          'axes.linewidth': 0.5, 
          'axes.grid': True,
          'axes.labelweight': 'normal',  
          'font.family': 'serif',
          'font.size': 8.0,
          'font.weight': 'normal',
          'text.color': 'black',
          'xtick.labelsize': 8,
          'ytick.labelsize': 8,
          'text.usetex': True,
          'legend.fontsize': 8,
          'figure.dpi': 300,
          'figure.figsize': fig_size,
          'savefig.dpi': 300,
         }

pylab.rcParams.update(params)

### DATA ###
threshold = 0.5
width  = 20.0
lenght = 20.0 
threshold2 = threshold*threshold
mass = 70.0
diameter = 0.46
sigma_diameter = 0.003



def aleja(xi,yi,x,y):
     flag = 1
     i=0
     while i<len(x) and flag:
          dist2 = (x[i]-xi)*(x[i]-xi) +(y[i]-yi)*(y[i]-yi)
          if dist2<threshold2:
               flag = 0 
          i+=1
     return flag

def agrega_pedestrian(x,y):
     xi = random.uniform(0.3, lenght-0.3)
     yi = random.uniform(0.3, width-0.3)
     if not aleja(xi,yi,x,y):
     	agrega_pedestrian(x,y)
     else:
     	x+=[xi]
     	y+=[yi]
     return [x,y]

####### MAIN ##################
N = 225
NTypes=29
MaxGroupSize=2
Niter=5


def agrega_grupo(x,y): 
     r=random.uniform(0.4, 0.7)
     theta=random.uniform(0,2*np.pi)
     xi = x[len(x)-1]+r*np.cos(theta)
     yi = y[len(y)-1]+r*np.sin(theta)
     if not aleja(xi,yi,x,y):
          agrega_grupo(x,y)
     else:
     	if xi>0.3 and xi<lenght-0.3 and yi>0.3 and yi<width-0.3:
     		x+=[xi]
     		y+=[yi]
     	else:
     		agrega_grupo(x,y)

     return [x,y]

def list_colors(number_of_colors):
     color = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
                  for i in range(number_of_colors)]
     return color
def mapea_tipo_color(lista_tipos,lista_color):
     i=0
     lista_tipo_color = []
     while i<len(lista_tipos):
          lista_tipo_color+=[lista_color[lista_tipos[i]-1]]
          i+=1
     return lista_tipo_color  

vector_diameter = np.random.normal(diameter, sigma_diameter, N)


for iter in range(1,Niter+1):

     # Inicializo vectores
     x=[]
     y=[]
     types=[]
     for i in range (2,NTypes+1):
          personas=agrega_pedestrian(x,y)
          x=personas[0]
          y=personas[1]
          types+=[i]
          for j in range (0,MaxGroupSize-1):
               personas=agrega_grupo(x,y)
               x=personas[0]
               y=personas[1]
               types+=[i]

     for i in range (len(x),N):
          personas = agrega_pedestrian(x,y)
          x = personas[0]
          y = personas[1]
          types+=[1]


     	###  OUTPUT  ###
     f= open("CI_%d_%d_%d_%d.txt" %(N,NTypes-1,MaxGroupSize,iter),"w+")
     f.write("# LAMMPS data file for big groups\n\n")
     f.write("%d atoms\n\n"%N)
     f.write("%d atom types\n\n"%NTypes)
     f.write("%2.1f \t %2.1f \t xlo xhi \n"%(0.0, lenght)) 			
     f.write("%2.1f \t %2.1f \t ylo yhi \n"%(0.0, width))
     f.write("%2.1f \t %2.1f \t zlo zhi \n\n"%(-1, 1))
     f.write("Atoms\n\n")

     for i in range(0,N):
          f.write("%d %d %2.2f %2.2f %2.4f %2.4f %d \n" % ((i+1), types[i] ,vector_diameter[i],mass ,x[i],y[i],0))
     	###  PLOT  ###

     pylab.grid(False)
     pylab.xlabel('x')
     pylab.ylabel('y')



     vector_color = list_colors(NTypes)  # lista de colores
     vector_color[0]='red'
     vector_color[1]='green'
     vector_color[2]='blue'
     vector_color[3]='yellow'
     vector_color[4]='cyan'


     for i in range(0,NTypes):
          for j in range(0,N):
               if (types[j]==i+1):
                    plt.plot(x[j],y[j],color='%s'%(vector_color[i]),marker='o',markersize='2')  

     pylab.savefig("CI_%d_%d_%d_%d.png" %(N,NTypes-1,MaxGroupSize,iter), dpi=300, bbox_inches='tight')
     plt.clf()


     print('Done %d iteracion'%(iter))