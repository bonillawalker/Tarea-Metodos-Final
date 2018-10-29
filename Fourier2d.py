import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as img                                
from scipy.fftpack import ifft2, fft2, fftshift, fftfreq       								       
from scipy.interpolate import interp1d          	      

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



#################Crear senal base para poder filtrar(Encuentro este metodo en internet):
width = 0.9                                                   
m = 10							      
X,Y = np.meshgrid( np.linspace(-1,1,m), np.linspace(-1,1,m) ) 
R = np.sqrt(X**2+Y**2)					      
montana = np.exp(-6*np.exp(-(R**2)/width))		      


##################Crear filtro general:
Filtro = np.ones(np.shape(I))				      

###################### Ubicar las montanas en las posiciones que corresponde para armar el filtro:

Filtro[ 10-m/2:10+m/2,  25-m/2:25+m/2 ] = montana	      
Filtro[ 65-m/2:65+m/2,  65-m/2:65+m/2 ] = montana
Filtro[ 256-10-m/2:256-10+m/2,  256-25-m/2:256-25+m/2 ] = montana
Filtro[ 256-65-m/2:256-65+m/2,  256-65-m/2:256-65+m/2 ] = montana



# Filtrar
I_FT_filtrado = I_FT*Filtro				      

plt.figure()						      
plt.imshow((np.log(np.abs(I_FT_filtrado))))                   
plt.colorbar()						      
plt.grid()						      
plt.savefig('BonillaWFelipe_FT2D_filtrada.pdf')	

#Transformada inversa
I_filtrado = np.real(ifft2(I_FT_filtrado))		      

plt.figure()						      
plt.imshow( I_filtrado,cmap='gray')			      
plt.savefig('BonillaWFelipe_Imagen_filtrada.pdf')	     

