import numpy as np

P = np.random.randint(20, size=15)
#P = np.flip(np.arange(20))
print("Array before:", P)

for i in range(1, P.size):
    a = P[i]
    j = i-1
    while j > -1 and a < P[j]:
        P[j+1] = P[j]
        j = j -1
    P[j+1] = a
    print("Step:", P)

print("Array after:", P)