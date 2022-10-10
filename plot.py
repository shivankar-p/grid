from tkinter import E
import matplotlib.pyplot as plt

f = open("Road.txt", "r")
edges = f.readlines()

mapping = {}

for edge in edges:

    swap_edge = list(edge)
    if(swap_edge[0]==swap_edge[2]):
        tmp = swap_edge[1]
        swap_edge[1]=swap_edge[3]
        swap_edge[3]=tmp
    else:
        tmp = swap_edge[0]
        swap_edge[0]=swap_edge[2]
        swap_edge[2]=tmp
        
    swap_edge = ''.join(swap_edge)
    if(edge in mapping):
        mapping[edge]+=1
    elif(swap_edge in mapping):
        mapping[swap_edge]+=1
    else:
        mapping[edge]=1

x = list(mapping.keys())
y = list(mapping.values())

y, x = zip(*sorted(zip(y, x), reverse=True))

plt.bar(range(len(mapping)), y, tick_label=x)
plt.xticks(rotation = 90)
plt.show()

