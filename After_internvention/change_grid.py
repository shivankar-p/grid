from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET




edge_file = open('../Before_intervention/output.txt', 'r')
lines = edge_file.readlines()

i = 0
id_lst = []
dir_lst = []

while (i < len(lines)):
    id = lines[i].split(": ")[1]
    i+=2
    dir = lines[i].split(": ")[1]
    i += 2
    id_lst.append(id[:len(id)-1])
    dir_lst.append(dir[:len(dir)-1])


def swap(a, b, c):
    tmp = c[a]
    c = list(c)
    c[a] = c[b]
    c[b] = tmp
    c = ''.join(c)
    return c





with open('../grid_files/grid.net.xml', 'r') as f:
    data = f.read()

Bs_data = BeautifulSoup(data, "xml")

for i in range(len(id_lst)):
    if(id_lst[i][0] == id_lst[i][2]):
        if(dir[i] == 'positive'):
            for tag in Bs_data.find_all('edge', {'id':id_lst[i]}):
                tag["from"] = id_lst[i][0]+max(id_lst[i][1], id_lst[i][3])
                tag["to"] = id_lst[i][0]+min(id_lst[i][1], id_lst[i][3])

            id_lst[i] = swap(1, 3, id_lst[i])

            for tag in Bs_data.find_all('edge', {'id':id_lst[i]}):
                tag["from"] = id_lst[i][0]+max(id_lst[i][1], id_lst[i][3])
                tag["to"] = id_lst[i][0]+min(id_lst[i][1], id_lst[i][3])
            
        else:
            for tag in Bs_data.find_all('edge', {'id':id_lst[i]}):
                tag["from"] = id_lst[i][0]+min(id_lst[i][1], id_lst[i][3])
                tag["to"] = id_lst[i][0]+max(id_lst[i][1], id_lst[i][3])

            id_lst[i] = swap(1, 3, id_lst[i])

            for tag in Bs_data.find_all('edge', {'id':id_lst[i]}):
                tag["from"] = id_lst[i][0]+min(id_lst[i][1], id_lst[i][3])
                tag["to"] = id_lst[i][0]+max(id_lst[i][1], id_lst[i][3])


    else:
        if(dir[i] == 'positive'):
            for tag in Bs_data.find_all('edge', {'id':id_lst[i]}):
                tag["from"] = min(id_lst[i][1], id_lst[i][3])+id_lst[i][1]
                tag["to"] = max(id_lst[i][1], id_lst[i][3])+id_lst[i][1]
            
            id_lst[i] = swap(0, 2, id_lst[i])

            for tag in Bs_data.find_all('edge', {'id':id_lst[i]}):
                tag["from"] = min(id_lst[i][1], id_lst[i][3])+id_lst[i][1]
                tag["to"] = max(id_lst[i][1], id_lst[i][3])+id_lst[i][1]

        else:
            for tag in Bs_data.find_all('edge', {'id':id_lst[i]}):
                tag["from"] = max(id_lst[i][1], id_lst[i][3])+id_lst[i][1]
                tag["to"] = min(id_lst[i][1], id_lst[i][3])+id_lst[i][1]

            id_lst[i] = swap(0, 2, id_lst[i])

            for tag in Bs_data.find_all('edge', {'id':id_lst[i]}):
                tag["from"] = min(id_lst[i][1], id_lst[i][3])+id_lst[i][1]
                tag["to"] = max(id_lst[i][1], id_lst[i][3])+id_lst[i][1]




""" for tag in Bs_data.find_all('edge', {'id':'B2B3'}):
    for lane in tag.find_all('lane', {'id':'B2B3_0'}):
        lane['index'] = "1" """

changed_grid = open('changed_grid.net.xml', 'w')
changed_grid.write(Bs_data.prettify())


    
    