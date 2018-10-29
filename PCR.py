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
#print(Matriz, np.cov(X.T), sep='\n'*2)					    #Con numpy puedo verificar si los numeros de mi matriz de cov estan bien
print('\n')

#############Parte Autovalores y Autovectores

valores,vectores = np.linalg.eig(Matriz)                                    #Con funcion de numpy saco los autovalores y autovectores

print("La primera matriz es la de autovalores y despues la de los autovectores respectivos para cada autovalor: ")  #Imprimo los autovalores y autovectores
print(valores)
print('\n')
print(vectores)
print('\n')
Ivalores = np.argsort(np.abs(vectores),axis=0)				    #En Ivalores guardo el orden de menor a mayor de cada autovector. La funcion de numpy argsort lo ordena
print('Segun los ', n, 'autovalores, los parametros mas importantes son: ') #Imprima la variable de mayor valor de cada autovector
print(Ivalores[-1,:]+1)
print('\n')


I = np.argsort(valores)[::-1]						    #En I guardo los autovalores ordenados
Icp = I[0:2] 								    #Guardo los Indices de los autovalores mayores que son mis componentes principales

print('Los componentes principales representan el ', 100*(np.sum(valores[Icp]))/np.sum(valores), "% de la varianza")  #Imprima mensaje que muestre el porcentaje de la varianza representada

CP = vectores[:,Icp] 							    #Saqueme los autovectores de los mayores autovalores -> Componentes principales
proyecciones = np.matmul(X,CP)                                              #Encuentreme la proyeccion de cada observacion sobre cada componente principal con paquete de numpy

#######################Graficar
plt.figure()								    #Creeme la figura
plt.plot(proyecciones[Diagnostic=='M',0], proyecciones[Diagnostic=='M',1], 'o', c='red') #Plot de el diagnostico maligno
plt.plot(proyecciones[Diagnostic=='B',0], proyecciones[Diagnostic=='B',1], 'o', c='blue') #Plot de el diagnostico benigno
plt.xlabel('Componente Principal 1')					    #Nombre ejes
plt.ylabel('Componente Principal 2')
plt.legend(['M','B'])							    #Crea la leyenda
plt.savefig('BonillaWFelipe_PCA.pdf')					    #Guarde la imagen como pdf


