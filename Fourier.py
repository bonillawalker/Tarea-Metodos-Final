import numpy as np
import matplotlib.pyplot as plt

# Cargar datos de las dos senales
S = np.genfromtxt('signal.dat', delimiter=',')            
I = np.genfromtxt('incompletos.dat', delimiter=',')	  

######################## Grafica de senal
plt.figure()						  
plt.plot(S[:,0], S[:,1], '.')                             
plt.xlabel('x')						  
plt.ylabel('y')
plt.savefig('BonillaWFelipe_signal.pdf')		  
