import math

def load_graph(input_file):

    file = open(input_file, "r")
    n = int(file.readline())

    # setup graph
    graph = [[0]*n for i in range(0, n)]

    coords_list = []
    for i in range(0, n):
        coords = file.readline()
        coords_arr = coords.split()
        coords_list.append([float(coords_arr[1]), float(coords_arr[2])])

    for i in range(0, n):
        for j in range(i+1, n):
            edge = math.sqrt((coords_list[i][0] - coords_list[j][0])
                             ** 2 + (coords_list[i][1] - coords_list[j][1])**2)
            graph[i][j] = edge
            graph[j][i] = edge

    file.close()
    return graph

