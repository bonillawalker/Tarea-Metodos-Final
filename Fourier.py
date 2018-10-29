import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import ifft				  #Este paquete me sirve para sacar la transformada inversa
from scipy.interpolate import interp1d			  #Este paquete lo uso para realizar las interpolaciones

# Cargar datos de las dos senales
S = np.genfromtxt('signal.dat', delimiter=',')            #Guarde los datos de signal.dat
I = np.genfromtxt('incompletos.dat', delimiter=',')	  #Guarde los datos de incompletos.dat


def transformadaFourier_DFT(x):				  #Creo la funcion que me va a calcular la transformada de Fourier y que recibe x
    N = len(x)                                            #Variable que determina la cantidad de datos	
    X = np.zeros(np.shape(x), dtype=complex)		  #Creo un arreglo de ceros para guardar el resultado
    							  
    
    for k in range(N):					  #Creo ciclo que me recorre mi arreglo 
        suma = 0					  #Inicializo mi variable suma con un valor de cero
        for n in range(N):
            suma = suma + x[n]*np.exp(-2*np.pi*1j*k*n/N)  #Formula sacada de wikipedia para calcular la transformada para cada valor (j es numero imaginario!!!)
        X[k] = suma					  #Voy guardando el resultado en mi matriz de ceros
        
    return X						  #Despues de tener mi arreglo completo, la funcion me devuelve un arreglo con los valores de la transform.

def frecuencias(fmuestreo, n):				  #Creo la funcion del espectro de frecuencias
    f = np.zeros((n,))                                    #Arreglo para guardar las frecuencias
    fnyq = fmuestreo/2                                    #Calculo la frecuencia de Nyquist(Encontre que esta frecuencia me representa la frecuencia maxima en toda mi senal)
    resolucionF = fnyq/(n/2)                              #Calculo la resolucion de la frecuencia
    
    if n/2 % 2 == 0: 					  #Condicion1: Si el numero de datos es par haga esto:
        espectroF = np.linspace(resolucionF,fnyq,n/2)     #Cree arreglo desde resolucionf hasta la frecuencia maxima, cada n/2
        f[0:n/2] = espectroF				  #Mi arreglo f de 0 a n/2 tendra un valor de espectro f
        f[n/2:] = -espectroF[::-1]			  #Mi arreglo f de n/2 en adelante es mi arreglo espectrof de atras para delante y negativo (Lo voltea)
        
    else: 					          #Condicion2: Si el numero de datos impar haga esto:
        espectroF = np.linspace(0,fnyq,(n/2)+1)		  #Cree arreglo desde 0 hasta la frecuencia maxima, cada n/2 +1
        f[0:(n/2)+1] = espectroF			  #Mi arreglo f de 0 a n/2 +1 tendra un valor de espectro f
        f[n/2+1:] = -espectroF[1:][::-1]		  #Mi arreglo f de n/2 +1 en adelante tendra los valores del espectrof tambien volteados!!
        
    return f						  #Devuelvame mi arreglo con las frecuencias

def pasa_bajas(fc, TF, Freq):				  #Creo la funcion que me va a filtrar mis datos
    TF_Filtrada = TF 					  #Hago una copia de los datos
    ii = np.abs(Freq)<fc 				  #Busca los indices en donde se disminuye la intensidad de los armonicos
    
    TF_Filtrada[~ii] = TF_Filtrada[~ii]*1e-6              #Formula para disminuir armonicos seleccionados a un valor pequeno (Encontre que ~ sirve para cambiar de verdadero a falso o de falso a verdadero)
    
    return TF_Filtrada					  #Devuelvame los datos filtrados


######################## Grafica de senal
plt.figure()						  #Creeme la figura
plt.plot(S[:,0], S[:,1], '.')                             #Grafica los datos de signal.dat
plt.xlabel('x')						  #Nombre ejes
plt.ylabel('y')
plt.savefig('BonillaWFelipe_signal.pdf')		  #Guarde la imagen como pdf	



fmuestreo = 1.0/(S[1,0] - S[0,0]) 			  #Calcula la frecuencia de muestreo

#Calcular trasformada de Fourier y espectro de frecuencias
S_TF = transformadaFourier_DFT(S[:,1])			  #A partir de mi funcion de arriba calculo la transformada
S_Freq = frecuencias(fmuestreo, np.size(S,0))		  #A partir de mi funcion de arriba calculo el espectro de frecuencias


######################## Grafica  de transformada de Fourier
plt.figure()						  #Creeme la figura
plt.plot(S_Freq, np.abs(S_TF))				  #Grafica de el espectro de frecuencias versus el valor absoluto de la transformada
#plt.xlim([0,500])
plt.grid()					          #Me pone la cuadricula
plt.savefig('BonillaWFelipe_TF.pdf')			  #Guarde la imagen como pdf


print('Frecuencias calculadas con mi propio codigo:')      #Imprima las frecuencias principales de mi senal
print('Las frecuencias principales de la senal son 180, 240, 420') #Sacadas a mano!!!!
print('\n')

# Filtrar senal con pasa bajas
fc = 1000						 #Inicializo el valor de la frecuencia de corte

# Usar la funcion de pasa bajas
S_TF_Filtrada = pasa_bajas(fc, S_TF, S_Freq)		 #Con la funcion de arriba voy a filtrar mis valores
S_filtrada = np.real(ifft(S_TF_Filtrada))                #Esto me saca la parte real de la transformada inversa con un paquete de numpy!


######################## Grafica  de transformada inversa de Fourier despues de filtrar
plt.figure()						 #Creeme la figura						
plt.plot(S[:,0], S_filtrada)				 #Grafica de la senal filtrada
#plt.xlim([0,500])
plt.grid()						 #Me pone la cuadricula
plt.savefig('BonillaWFelipe_filtrada.pdf')               #Guarde la imagen como pdf
