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


def bfs_tree(graph, start):
   verti = graph.verti
   discovered = [bool]*verti
   processed = [bool]*verti
   parent = [int]*verti
   for i in range(verti):
       discovered[i]=False
       processed[i]=False
       parent[i]=None
   discovered[start]=True
   q = Queue()
   q.put(start)
   while(q.empty()==False):
       i = q.get()
       adjVert = graph.adjacency_list[i]
       for x in range(len(adjVert)):
           end = adjVert[x][0]
           if(discovered[end]==False):
               discovered[end]=True
               parent[end]=i
               q.put(end)
       processed[i]=True
   return parent

def bfs_vert(graph, start):
   verti = graph.verti
   discovered = [bool]*verti
   processed = [bool]*verti
   parent = [int]*verti
   for i in range(verti):
       discovered[i]=False
       processed[i]=False
       parent[i]=None
   discovered[start]=True
   q = Queue()
   q.put(start)
   while(q.empty()==False):
       i = q.get()
       adjVert = graph.adjacency_list[i]
       for x in range(len(adjVert)):
           end = adjVert[x][0]
           if(discovered[end]==False):
               discovered[end]=True
               parent[end]=i
               q.put(end)
       processed[i]=True
   connected_stuff = []
   for i in range(verti):
       if(discovered[i]):
           connected_stuff.append(i)
   return connected_stuff

def dfs_tree(graph, start):
    graph.discovered[start]=True
    adjVert=graph.adjacency_list[start]
    for i in range(len(adjVert)):
        end = adjVert[i][0]
        if(graph.discovered[end]==False):
            graph.parents[end]=start
            dfs_tree(graph, end)
    return graph.parents

def dfs_cycle(graph, start):
    graph.discovered[start]=True
    adjVert=graph.adjacency_list[start]
    for i in range(len(adjVert)):
        end = adjVert[i][0]
        if(graph.discovered[end] and (graph.parents[start]!=end)):
            return True
        if(graph.discovered[end]==False):
            graph.parents[end]=start
            dfs_tree(graph, end)
    return False

def has_cycle(graph):
    for i in range(graph.verti):
        if(dfs_cycle(graph, i)==True):
            return True
    return False

def connected_components(graph):
    verti = graph.verti
    discovered = [bool]*verti
    processed = [bool]*verti
    for i in range(verti):
        discovered[i]=False
        processed[i]=False
    components=[]
    for i in range(verti):
        components.append(bfs_vert(graph, i))
    return list(set(tuple(element) for element in components))

def tree_path(parents, start, end):
    path = []
    while((start==end)==False):
        path.insert(0, end)
        end = parents[end]
    path.insert(0, start)
    return path


graph_string = """\
U 7
1 2
1 5
1 6
2 3
2 5
3 4
4 5
"""

print(has_cycle(Graph(graph_string)))