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
plt.title("Grafica Signal.dat")				  #Le crea un titulo
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
plt.title("Grafica de la transformada de Fourier")	  #Le pone titulo
plt.ylabel('Transformada')
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
plt.title("Grafica de la transformada inversa")	         #Le pone titulo
plt.savefig('BonillaWFelipe_filtrada.pdf')               #Guarde la imagen como pdf



print('No se puede hacer la transformada de Fourier de incompletos.dat porque los datos no estan muestreados uniformemente y ese es uno de los requisitos para aplicar la transformada de Fourier')
print('\n')



################################################################################################
######################## Interpolaciones
################################################################################################

# Crear funciones para interpolar
Interp2 = interp1d(I[:,0], I[:,1], kind='quadratic')   #Con paquete de scipy hago la interpolacion cuadratica
Interp3 = interp1d(I[:,0], I[:,1], kind='cubic')       #Con paquete de scipy hago la interpolacion cubica

m = 512 					       #Inicializo una variable con los numeros de puntos que me piden
Ix = np.linspace(min(I[:,0]), max(I[:,0]), m)          #Espacio donde se quiere interpolar

# Calcular interpolaciones
I2 = Interp2(Ix)					#Calculo la interpolacion cuadratica
I3 = Interp3(Ix)					#Calculo la interpolacion cubica

# Transformada de Fourier de datos interpolados
I2_FT = transformadaFourier_DFT(I2)			#Con funcion de arriba calculo la transformada de mis datos interpolados cuadraticamente
I3_FT = transformadaFourier_DFT(I3)			#Con funcion de arriba calculo la transformada de mis datos interpolados cubicamente

# Frecuencias para datos interpolados
fmuestreo = 1/(Ix[1]-Ix[0])				#Calcula la frecuencia de muestreo de mis datos interpolados
I_freq = frecuencias(fmuestreo,m)			#A partir de mi funcion de arriba calculo el espectro de frecuencias de los datos interpolados


######################## Grafica  de  tres subplots de la transformada de los datos interpolados
plt.figure(figsize=(6,10))                             #Creeme la figura con este tamano

plt.subplot(3,1,1)				       #Creeme el primer subplot con la transformada de Fourier 
plt.plot(S_Freq, np.abs(S_TF))			       #Grafica de el espectro de frecuencias versus el valor absoluto de la transformada de datos sin interpolar			       
plt.legend(['Signal.dat'])                             #Le pone la leyenda

plt.subplot(3,1,2)				       #Creeme el segundo subplot con la transformada de Fourier con los datos interpolados cuadraticamente
plt.plot(I_freq, np.abs(I2_FT))                        #Grafica de el espectro de frecuencias versus el valor absoluto de la transformada (datos interpolados cuadraticamente)
plt.legend(['Interp Cuadratica'])		       #Le pone la leyenda

plt.subplot(3,1,3)				       #Creeme el tercer subplot con la transformada de Fourier con los datos interpolados cubicamente
plt.plot(I_freq, np.abs(I3_FT))			       #Grafica de el espectro de frecuencias versus el valor absoluto de la transformada (datos interpolados cubicamente)
plt.legend(['Interp Cubica'])			       #Le pone la leyenda


plt.savefig('BonillaWFelipe_TF_interpola.pdf')         #Guarde la imagen como pdf

print('En la interpolacion cubica se incluyen armonicos artificiales de alta frecuencia que no estaban presentes en la senal original. En la interpolacion cuadratica sucede lo mismo pero se incluye mayor cantidad de armonicos y de mayor amplitud. En conclusion las dos interpolaciones le agregan armonicos a la senal.')            #Imprima mensaje que describe las diferencias encontradas
print('\n')

# Nuevas frecuencias de corte
fc1 = 500				#Asigno un valor para una frecuencia de corte							
fc2 = 1000				#Asigno un valor para la otra frecuencia de corte

# Aplicar filtros a las senales I2 e I3
I2_FT_filtro1 = pasa_bajas(fc1, I2_FT, I_freq)	#En estas cuatro lineas aplico la funcion de arriba que me filtra mis datos
I2_FT_filtro2 = pasa_bajas(fc2, I2_FT, I_freq)
I3_FT_filtro1 = pasa_bajas(fc1, I3_FT, I_freq)
I3_FT_filtro2 = pasa_bajas(fc2, I3_FT, I_freq)

# Aplicar transformada Inversa a senales filtradas de I2 e I3 y toca que toma solo las partes reales
I2_filtrado1 = np.real(ifft(I2_FT_filtro1))	#Esto me saca la parte real de la transformada inversa de mis senales filtradas!		
I2_filtrado2 = np.real(ifft(I2_FT_filtro2))	#Se usa el mismo paquete de numpy usado arriba
I3_filtrado1 = np.real(ifft(I3_FT_filtro1))
I3_filtrado2 = np.real(ifft(I3_FT_filtro2))



########################## Grafica de transformadas inversas
plt.figure(figsize=(6,10))                            #Creeme la figura con este tamano

plt.subplot(2,1,1)				      #Creeme el primer subplot
plt.plot(S[:,0], S_filtrada)			      #Ploteeme los tres casos
plt.plot(Ix, I2_filtrado1)			      #Ploteeme la senal filtrada
plt.plot(Ix, I3_filtrado1)			      #Ploteeme la senal con el otro filtro 
plt.legend(['Signal.dat', 'Interp Cuadratica', 'Interp Cubica']) #Le pone la leyenda
plt.title('Filtro pasa bajas a ' + str(fc1))  			 #Le pone el titulo

plt.subplot(2,1,2)						 #Creeme el segundo subplot
plt.plot(S[:,0], S_filtrada)					 #Ploteeme el caso filtrado 
plt.plot(Ix, I2_filtrado2)					 #Ploteeme la senal filtrada
plt.plot(Ix, I3_filtrado2)					 #Ploteeme la senal con el otro filtro 
plt.legend(['Signal.dat', 'Interp Cuadratica', 'Interp Cubica']) #Le pone la leyenda
plt.title('Filtro pasa bajas a ' + str(fc2))			 #Le pone el titulo



plt.savefig('BonillaWFelipe_2Filtros.pdf')			 #Guarde la imagen como pdf

