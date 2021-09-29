import numpy as np

arr = [3,1,2,3,4,5,5,2,1]
valorFila = arr[0]
fila = 0

for i in reversed(arr):
    if(arr[i] < valorFila and arr[i] > 0):
        fila = i  

print(fila)
print(arr[fila])

