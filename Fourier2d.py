import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as img                                #Con esto puedo leer la imagen.png
from scipy.fftpack import fft2      
         	      

I = img.imread('arbol.png')                                   

I_FT = fft2(I) 						      

plt.figure(figsize=(12,6))                                    
plt.subplot(1,2,1)					      
plt.imshow(((np.abs(I_FT))))				     
plt.colorbar()						      
plt.grid()						      


plt.subplot(1,2,2)					      
plt.imshow((np.log( np.abs(I_FT))[0:80,0:80]) )              
plt.grid()						      
plt.colorbar()						     

plt.savefig('BonillaWFelipe_FT2D.pdf')			      

