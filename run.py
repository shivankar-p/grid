#!/usr/bin/env python

from operator import truediv
import os
import sys
import optparse
import pandas as pd
import networkx as nx

# we need to import some python modules from the $SUMO_HOME/tools directory
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")


import sumolib  # Checks for the binary in environ vars
from sumolib import checkBinary
import traci


command_file = "command.sh"
os.system("bash "+ command_file)


csv_file = "plain.edg.csv"
sumocfg = "grid.sumocfg"
tripInfo = "Before_intervention/TripDetails_before.xml"

net_file = "grid.net.xml"

os.system("bash "+ command_file)


def getConnectedComponent():
    df = pd.read_csv(csv_file, sep=";",engine='python')
    df = df.drop_duplicates(subset=["edge_id"],keep=False)
    adj_list = {}
    x = len(df)
    for i in range(x):
        val = df.iloc[i]
        if( val["edge_from"] in adj_list):
            adj_list[val["edge_from"]].append(val["edge_to"])
    
        else:
            adj_list[val["edge_from"]] = [val["edge_to"]]
        
    G = nx.DiGraph(adj_list)
    return G

def getNumberOfConnectedComponents(G):
    g = nx.number_strongly_connected_components(G) 
    return g

G = getConnectedComponent()

def check_edge(a):
    df = pd.read_csv(csv_file ,sep=";",engine='python')
    df = df.drop_duplicates(subset=["edge_id"],keep=False)    
    df = df.set_index("edge_id")
    edges = list(df.index)
    if a not in edges:
        return False
    
    val = df.loc[a]
    edge_from = val["edge_from"]
    edge_to = val["edge_to"]
    res = G.has_edge(edge_from,edge_to)
    
    if(not res):
        return False
    
    G_copy = G.copy()
    G_copy.remove_edge(edge_from,edge_to)
    
    if(getNumberOfConnectedComponents(G) == getNumberOfConnectedComponents(G_copy)):
        res = True
        G.remove_edge(edge_from,edge_to)
    
    else:
        res = False
    return res


def get_options():
    opt_parser = optparse.OptionParser()
    opt_parser.add_option("--nogui", action="store_true",
                         default=False, help="run the commandline version of sumo")
    options, args = opt_parser.parse_args()
    return options


# contains TraCI control loop
def run():
    step = 0
    flag = 0
    traffic_diff_sort=[]
    traffic_diff={}
    roads_posi=[]
    roads_negi=[]
    finals=[]
    edg_lst=traci.edge.getIDList()
    #print(edg_lst)

    """
    -> positive, | positive
                 V
    """
    for i in edg_lst:
        if(i[0] == ':'):
            continue

        if(i[0] == i[2]):
            if(i[1] > i[3]):
                roads_posi.append(i)
            else:
                roads_negi.append(i)
        else:
            if(i[0] > i[2]):
                roads_negi.append(i)
            else:
                roads_posi.append(i)
    
    
            
    while step<=3600:
        traci.simulationStep()

        if(step%100==0):

            for rd in roads_negi:
                    #print(rd)
                    traffic_1=traci.edge.getLastStepVehicleNumber(rd)
                    #swap
                    neg_rd = rd
                    traffic_diff[neg_rd] = 0
                    rd = list(rd)
                    if(rd[0]==rd[2]):
                        tmp = rd[1]
                        rd[1]=rd[3]
                        rd[3]=tmp
                    else:
                        tmp = rd[0]
                        rd[0]=rd[2]
                        rd[2]=tmp
                    rd = ''.join(rd)
                    traffic_2=traci.edge.getLastStepVehicleNumber(rd)
                    traffic_diff[neg_rd]+=(traffic_1-traffic_2)
                    flag += 1
        step += 1
    #print("chk2")
   
    for rd in roads_negi:
        if(traffic_diff[rd]>0):
            str1 = '0' #'negative'
        else:
            str1 = '1' #'positive'
        traffic_diff_sort.append((abs(traffic_diff[rd]),rd,str1))

    traffic_diff_sort.sort(key=lambda e: e[0],reverse=True)
    #print(len(traffic_diff_sort))

    i=0
    while(len(finals)<5):
        if(check_edge(traffic_diff_sort[i][1])):
            finals.append((traffic_diff_sort[i][0],traffic_diff_sort[i][1],traffic_diff_sort[i][2]))
        i+=1
    
    #print("hemlo")
    f = open("Before_intervention/output.txt","w")
    f2 = open("Road.txt", "a")
    j=0
    while(j<5):
        f2.write(finals[j][1] + '_' + finals[j][2] + '\n')
        f.write('ID of the edge to be made oneway: ' + finals[j][1] + '\n')
        txt = 'Traffic flow difference: '
        f.write(txt)
        f.write('{}'.format(finals[j][0]))
        f.write('\nTraffic flow direction: ' + finals[j][2]+ '\n')
        f.write('\n')
        j+=1
    f.close()
    f2.close()

    traci.close()
    sys.stdout.flush()


# main entry point
if __name__ == "__main__":
    options = get_options()

    # check binary
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')
    # traci starts sumo as a subprocess and then this script connects and runs
    traci.start([sumoBinary, "-c", sumocfg,
                             "--statistic-output", tripInfo])     

    """ net = sumolib.net.readNet('grid_files/grid.net.xml')  
    edges = net.getEdges() """
    #print(len(edges))
    #print(edges)               
    run()