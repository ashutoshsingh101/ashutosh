import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np



# x = np.random.normal(10,.5,10)
# X,Y =  np.meshgrid(x,x)
# np.random.seed(1)

# Z = 0.5*X - 0.3*Y +8*np.random.normal(size= X.shape)
# fig = plt.figure(figsize = (15,15))
# ax = fig.gca(projection='3d')
# surf = ax.plot_surface(X, Y, Z, cmap=plt.cm.coolwarm,
#                        rstride=1, cstride=1)

# ax.set_xlabel('X')
# ax.set_ylabel('Y')
# ax.set_zlabel('Z')

# plt.savefig('3d.png',type= 'png')
a = [1,2,3,4,5,6,7,8,9,10]
x = np.random.normal(10,.5,10)
y = np.random.normal(15,.5,10)
fig = plt.figure(figsize = (10,10))

plt.plot(a,x,'-o',color = 'red')
plt.savefig('1d.png',type= 'png')