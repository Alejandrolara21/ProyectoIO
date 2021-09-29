import numpy as np

arr = [-3.000000000000107, -17.142857142857125, -20.093023255813953]
valorFila = max(arr)
fila = arr.index(valorFila)

for i in range(len(arr)):   
    if(arr[i] < valorFila and arr[i] > 0):
        valorFila = arr[i]
        fila = i    

print(fila)
