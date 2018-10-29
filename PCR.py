import numpy as np
import matplotlib.pyplot as plt


Data = np.genfromtxt('WDBC.dat', delimiter=',')				    #Cargar todos los datos
Diagnostic = np.genfromtxt('WDBC.dat', delimiter=',', usecols=1, dtype=str) #Cargar los diagnosticos por aparte para que sea mas facil el uso

Id = Data[:,0] 								    #Saqueme los Id
X = Data[:,2:]                                                              #Saqueme solo los datos numericos

