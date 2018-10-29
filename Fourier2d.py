import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as img                                #Con esto puedo leer la imagen.png
from scipy.fftpack import ifft2, fft2, fftshift, fftfreq      #Este paquete me sirve para la transformada inversa de fourier, la transformada normal, desplazar el componente de frecuencia cero al centro 								       del espectro y calcular las frecuencias de muestra de la transformada de Fourier todo esto para 2D.
from scipy.interpolate import interp1d          	      #Este paquete lo uso para realizar las interpolaciones

I = img.imread('arbol.png')                                   #Lea y guarde la imagen

I_FT = fft2(I) 						      #Hagale la transformada de Fourier a los datos de su imagen

plt.figure(figsize=(12,6))                                    #Creeme la figura con este tamano
plt.subplot(1,2,1)					      #Creeme el primer subplot
plt.imshow(((np.abs(I_FT))))				      #Grafiqueme la imagen que produce el valor absoluto de la transformada de fourier calculada
plt.colorbar()						      #Pongale la barra de color
plt.grid()						      #Pongale la cuadricula


plt.subplot(1,2,2)					      #Creeme el segundo subplot
plt.imshow((np.log( np.abs(I_FT))[0:80,0:80]) )               #Grafiqueme la imagen producida al realizarle el logaritmo al valor de las transformadas y hagalo entre esos valores
plt.grid()						      #Pongale la cuadricula
plt.colorbar()						      #Pongale la barra de color

plt.savefig('BonillaWFelipe_FT2D.pdf')			      #Guarde la imagen como pdf



#################Crear senal base para poder filtrar(Encuentro este metodo en internet):
width = 0.25                                                   #Se le da un valor para el ancho
m = 10							      #Iniciar m!!!
X,Y = np.meshgrid( np.linspace(-1,1,m), np.linspace(-1,1,m) ) #Crear una cuadricula a partir de una matriz de valores x y una matriz de valores y.(Me deja moverme como coordenadas)
R = np.sqrt(X**2+Y**2)					      #Calculo el valor de la magnitud del vector XY
montana = np.exp(-6*np.exp(-(R**2)/width))		      #Creo mi funcion montana que depende de R y width (Sacada de internet)


##################Crear filtro general:
Filtro = np.ones(np.shape(I))				      #Creo arreglo de unos para guardar despues los datos del filtro

###################### Ubicar las montanas en las posiciones que corresponde para armar el filtro:

Filtro[ 10-m/2:10+m/2,  25-m/2:25+m/2 ] = montana	      #En estas cuatro lineas lo que hago es pararme en esas posiciones de mi arreglo de unos y las convierto en el valor de mi funcion montana
Filtro[ 65-m/2:65+m/2,  65-m/2:65+m/2 ] = montana
Filtro[ 256-10-m/2:256-10+m/2,  256-25-m/2:256-25+m/2 ] = montana
Filtro[ 256-65-m/2:256-65+m/2,  256-65-m/2:256-65+m/2 ] = montana



# Filtrar
I_FT_filtrado = I_FT*Filtro				      #Hagale la transformada de Fourier a los datos y multipliquelos por su mi filtro

plt.figure()						      #Creeme la figura
plt.imshow((np.log(np.abs(I_FT_filtrado))))                   #Grafiqueme la imagen producida al realizarle el logaritmo al valor de las transformadas
plt.colorbar()						      #Pongale la barra de color
plt.grid()						      #Pongale la cuadricula
plt.savefig('BonillaWFelipe_FT2D_filtrada.pdf')		      #Guarde la imagen como pdf


#Transformada inversa
I_filtrado = np.real(ifft2(I_FT_filtrado))		      #Hagale la transformada de Fourier inversa a la del punto anterior y coja sus valores reales

plt.figure()						      #Creeme la figura
plt.imshow( I_filtrado,cmap='gray')			      #Grafiqueme la imagen en la que el filtro elimina el ruido
plt.savefig('BonillaWFelipe_Imagen_filtrada.pdf')	      #Guarde la imagen como pdf




	     

