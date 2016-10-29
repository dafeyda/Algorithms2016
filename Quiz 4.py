class Queue:
    def __init__(self):
        self.items = []

    def empty(self):
        return self.items == []

    def put(self, item):
        self.items.insert(0,item)

    def get(self):
        return self.items.pop()

    def size(self):
        return len(self.items)

    def toList(self):
        return self.items

class Stack:
    def __init__(self):
        self.items = []

    def empty(self):
        return self.items == []

    def push(self, item):
        self.items.insert(0, item)

    def get(self):
        return self.items[0]

    def size(self):
        return len(self.items)

    def toList(self):
        return self.items


class Graph:
    def __init__(self, graph_string):
        info = graph_string.splitlines()
        lines = len(info)
        self.Edges = [Edge] * (lines-1)
        self.verti = 0
        self.directed = False
        self.weighted = False
        for i in range(0, lines):
            chars = info[i].split()
            for x in range(0, len(chars)):
                if (i==0):
                    if(len(chars)==3):
                        self.weighted = True
                    if(chars[0]=='D'):
                        self.directed = True
                    self.verti = int(chars[len(chars)-1])
                else:
                    if(len(chars)==3):
                        self.Edges[i-1]=Edge(int(chars[0]), int(chars[1]), int(chars[2]))
                    else:
                        self.Edges[i-1]=Edge(int(chars[0]), int(chars[1]))
        self.adjacency_list = [[] for y in range(self.verti)]
        self.discovered = [bool]*self.verti
        self.parents = [int]*self.verti
        self.topSort = Stack()
        for i in range(self.verti):
            self.discovered[i]=False
            self.parents[i]=None
        if(self.directed):
            for i in range(0, len(self.Edges)):
                (self.adjacency_list[self.Edges[i].a]).append((self.Edges[i].b, self.Edges[i].w))
        else:
            for i in range(0, len(self.Edges)):
                self.adjacency_list[self.Edges[i].a].append((self.Edges[i].b, self.Edges[i].w))
                self.adjacency_list[self.Edges[i].b].append((self.Edges[i].a, self.Edges[i].w))


class Edge:
    def __init__(self, a, b, w=None):
        self.a = a
        self.b = b
        self.w = w
    def __str__(self):
        return str(self.a)+" "+str(self.b)+" "+str(self.w)

def dfs(graph, start):
    graph.discovered[start]=True
    adjVert=graph.adjacency_list[start]
    for i in range(len(adjVert)):
        end = adjVert[i][0]
        if(graph.discovered[end]==False):
            graph.parents[end]=start
            dfs(graph, end)
    graph.topSort.push(start)


def topsort(graph):
    for i in range (graph.verti):
        if(graph.discovered[i]==False):
            dfs(graph, i)
    return graph.topSort.toList()

def prim(graph, start):
    inTree = [bool]*graph.verti
    distance = [int]*graph.verti
    for i in range(graph.verti):
        inTree[i]=False
        distance[i]=99999
    distance[start]=0
    v = start
    while(inTree[v]==False):
        inTree[v]=True
        adjVert = graph.adjacency_list[v]
        for i in range (len(adjVert)):
            end = adjVert[i][0]
            weight = adjVert[i][1]
            if((weight<distance[end]) and inTree[end]==False):
                distance[end] = weight
                graph.parents[end] = v
        v = 1
        dist = 99999
        for i in range (graph.verti):
            if((inTree[i]==False) and (dist>distance[i])):
                v = i
                dist = distance[i]
    return graph.parents

def dijkstra(graph, start):
    inTree = [bool]*graph.verti
    distance = [int]*graph.verti
    for i in range(graph.verti):
        inTree[i]=False
        distance[i]=99999
    distance[start]=0
    v = start
    while(inTree[v]==False):
        inTree[v]= True
        adjVert = graph.adjacency_list[v]
        for i in range (len(adjVert)):
            end = adjVert[i][0]
            weight = adjVert[i][1]
            if(distance[end] > distance[v]+weight):
                distance[end] = distance[v] + weight
                graph.parents[end] = v
        v = 1
        dist = 99999
        for i in range (graph.verti):
            if((inTree[i]==False) and (dist>distance[i])):
                v = i
                dist = distance[i]
    return (graph.parents, distance)


graph_str = """\
D W 3
0 1 1
1 2 2
2 0 4
"""

print(dijkstra(Graph(graph_str), 0))
print(dijkstra(Graph(graph_str), 1))
print(dijkstra(Graph(graph_str), 2))
