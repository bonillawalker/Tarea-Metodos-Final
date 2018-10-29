import numpy as np
import matplotlib.pyplot as plt


Data = np.genfromtxt('WDBC.dat', delimiter=',')				    #Cargar todos los datos
Diagnostic = np.genfromtxt('WDBC.dat', delimiter=',', usecols=1, dtype=str) #Cargar los diagnosticos por aparte para que sea mas facil el uso

Id = Data[:,0] 								    #Saqueme los Id
X = Data[:,2:]                                                              #Saqueme solo los datos numericos

n = np.size(X,1)							    #Asigno el valor de n como el tamano de x
Matriz = np.zeros((n,n))                                                    #Matriz de ceros para ir guardando los valores

mu = np.mean(X,0)                                                           #Calculo el promedio de las columnas
dif = X-mu 								    #Diferencia de cada dato con su promedio. Le resto a cada valor su promedio


for i in range(n):							    #Creo ciclo que me recorra la matriz
    for j in range(n):
        Matriz[i,j] = np.mean(dif[:,i]*dif[:,j])                            #Para cada valor calcular cada covarianza


print('Matriz de Covarianza:') 				            	    #Imprima la matriz de covarianza para revisar
print(Matriz)
print(Matriz, np.cov(X.T), sep='\n'*2)					    #Con numpy puedo verificar si los numeros de mi matriz de cov estan bien
print('\n')

