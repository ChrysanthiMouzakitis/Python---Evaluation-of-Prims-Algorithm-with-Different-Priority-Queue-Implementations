class Vertex:
    """ A Vertex in a graph. """
    
    def __init__(self, element):
        """ Create a vertex, with data element. """
        self._element = element

    def __str__(self):
        """ Return a string representation of the vertex. """
        return str(self._element)

    def element(self):
        """ Return the data for the vertex. """
        return self._element
    
    def __lt__(self, v):
        """ Return true if this object is less than v.
       
        Args:
            v -- a vertex object
        """
        return self._element < v.element()
    
class Edge:
    
    def __init__(self, v, w, element):
        """ Create an edge between vertices v and w, with label element.

        Args:
            v -- a Vertex object
            w -- a Vertex object
            element -- the label, can be an arbitrarily complex structure.
        """
        self._vertices = (v,w)
        self._element = element

    def __str__(self):
        """ Return a string representation of this edge. """
        return ('(' + str(self._vertices[0]) + '--'
                   + str(self._vertices[1]) + ' : '
                   + str(self._element) + ')')

    def vertices(self):
        """ Return an ordered pair of the vertices of this edge."""
        return self._vertices

    def opposite(self, v):
        """ Return the opposite vertex to v in this edge, or None if this edge not incident on v.  
        
        Args:
            v - a Vertex object
        """
        if self._vertices[0] == v:
            return self._vertices[1]
        elif self._vertices[1] == v:
            return self._vertices[0]
        else:
            return None

    def element(self):
        """ Return the data element for this edge. """
        return self._element

    def start(self):
        """ Return the first vertex in the ordered pair. """
        return self._vertices[0]

    def end(self):
        """ Return the second vertex in the ordered. pair. """
        return self._vertices[1]



class Graph:
   
    def __init__(self):
        self._structure = dict()

    def __str__(self):
        """ Return a string representation of the graph. """
        hstr = ('|V| = ' + str(self.num_vertices())
                + '; |E| = ' + str(self.num_edges()))
        vstr = '\nVertices: '
        for v in self._structure:
            vstr += str(v) + '-'
        edges = self.edges()
        estr = '\nEdges: '
        for e in edges:
            estr += str(e) + ' '
        return hstr + vstr + estr

    #--------------------------------------------------#
    #ADT methods to query the graph
    
    def num_vertices(self):
        """ Return the number of vertices in the graph. """
        return len(self._structure)

    def num_edges(self):
        """ Return the number of edges in the graph. """
        num = 0
        for v in self._structure:
            num += len(self._structure[v])    #the dict of edges for v
        return num //2     #divide by 2, since each edege appears in the
                           #vertex list for both of its vertices

    def vertices(self):
        """ Return a list of all vertices in the graph. """
        return [key for key in self._structure]

    def get_vertex_by_label(self, element):
        for v in self._structure:
            if v.element() == element:
                return v
        return None

    def edges(self):
        """ Return a list of all edges in the graph. """
        edgelist = []
        for v in self._structure:
            for w in self._structure[v]:
                #to avoid duplicates, only return if v is the first vertex
                if self._structure[v][w].start() == v:
                    edgelist.append(self._structure[v][w])
        return edgelist

    def get_edges(self, v):
        """ Return a list of all edges incident on v.
"""
        if v in self._structure:
            edgelist = []
            for w in self._structure[v]:
                edgelist.append(self._structure[v][w])
            return edgelist
        return None

    def get_edge(self, v, w):
        """ Return the edge between v and w, or None, if there is no edge.
        """
        if (self._structure != None
                         and v in self._structure
                         and w in self._structure[v]):
            return self._structure[v][w]
        return None

    def degree(self, v):
        """ Return the degree of vertex v.
        """
        return len(self._structure[v])

    #--------------------------------------------------#
    #ADT methods to modify the graph
    
    def add_vertex(self, element):

        v = Vertex(element)
        self._structure[v] = dict()  # create an empty dict, ready for edges
        return v

    def add_vertex_if_new(self, element):

        for v in self._structure:
            if v.element() == element:
                #print('Already there')
                return v
        return self.add_vertex(element)

    def add_edge(self, v, w, element):

        if not v in self._structure or not w in self._structure:
            return None
        e = Edge(v, w, element)
        self._structure[v][w] = e
        self._structure[w][v] = e
        return e

    def add_edge_pairs(self, elist):
        """ Add all vertex pairs in elist as edges with empty elements. """
        for (v,w) in elist:
            self.add_edge(v,w,None)

    #--------------------------------------------------#
    #Additional methods to explore the graph
        
    def highestdegreevertex(self):
        """ Return the vertex with highest degree. """
        hd = -1
        hdv = None
        for v in self._structure:
            if self.degree(v) > hd:
                hd = self.degree(v)
                hdv = v
        return hdv
    

    
def make_random_graph(n_vertices, m_edges):

    #for random picking of vertices
    import random

    #make sure the number of edges isnt too big
    while m_edges > n_vertices * (n_vertices-1) / 2:
        m_edges = int(input("Please put a smaller number of edges: "))

    #initialise some stuff
    vertices_list = []
    my_graph=Graph()

    #add a vertex n times
    for x in range(n_vertices):
        #make it and add to list
        vertex = my_graph.add_vertex(x)
        vertices_list.append(vertex)
        #if its not the first vertex, connect it to a random one
        if x > 0:
            #pick random form list not including the one u just added
            vertex2 = random.randint(0,x-1)
            #get the vertex
            vertex2 = vertices_list[vertex2]
            #add an edge between them to connect the graph
            value = random.randint(1,20)
            my_graph.add_edge(vertex2, vertex, value)

    #now add edges until number of edges reached
    for y in range(m_edges-(n_vertices-1)):

        #pick two random points
        vertex1 = random.randint(0, n_vertices-1)
        vertex2 = random.randint(0,n_vertices-1)

        #make into vertices
        vertex1 = vertices_list[vertex1]
        vertex2 = vertices_list[vertex2]
        
        #check not the same
        while vertex1 == vertex2:
            vertex2 = random.randint(0, n_vertices-1)
            vertex2 = vertices_list[vertex2]

        #make sure that vertex 1 isnt fully connected before u loop through
        #trying to connect it to something
        max_edges = n_vertices-1
        while my_graph.degree(vertex1) == max_edges:
            vertex1 = random.randint(0,n_vertices-1)
            vertex1 = vertices_list[vertex1]
        
        #make sure theyre not connected, or the same
        #if theyre connected or if the are the same, pick a new second vertex
        check_var = my_graph.get_edge(vertex1, vertex2)
        while check_var != None or vertex2._element == vertex1._element:
            vertex2 = random.randint(0,n_vertices-1)
            vertex2 = vertices_list[vertex2]
            check_var = my_graph.get_edge(vertex1, vertex2)
        
        #finally get a random value and add an edge between the points
        value = random.randint(1,20)
        my_graph.add_edge(vertex2, vertex1, value)

    return my_graph

class Element:
    """ A key, value and index. """
    def __init__(self, k, v, i):
        self._key = k
        self._value = v
        self._index = i

    def __str__(self):
        return f"({self._key}, {self._value}, {self._index})"
    
    def __lt__(self, other):
        return self._key < other._key
    
    def _wipe(self):
        self._key = None
        self._value = None
        self._index = None

class Priority_Queue_Heap:

    def __init__(self):
        self._heap = []

    def __str__(self):
        string = "[ "
        for elem in self._heap:
            string += str(elem) + " "

        string+= "]"
        return string
    
    def length(self):
        return len(self._heap)

    def bubble_up(self, index):

        #while the node has a key smaller than its parent and it isn't at the front of the list
        while self._heap[index]._key < self._heap[(index-1)//2]._key and index !=0:
            #swap their indexes
            self._heap[index]._index ,self._heap[(index-1)//2]._index = self._heap[(index-1)//2]._index ,self._heap[index]._index
            #swap them
            self._heap[index], self._heap[(index-1)//2] = self._heap[(index-1)//2], self._heap[index]
            
            #update current index for next iteration
            index=(index-1)//2

        #return self._heap

    def bubble_down(self, current_i):
        length = len(self._heap) - 1
        while current_i <= (length-1):

            lc = (2*current_i)+1                   #get the kids
            rc = (2*current_i)+2

            if lc > (length -1) and rc > (length -1):      #if no children, break as sorted
                break

            elif lc > (length -1):                          #if no left, therefore only a right
                if self._heap[current_i] > self._heap[rc]:              #if less than right, swap

                    #index swapping
                    self._heap[current_i]._index, self._heap[(2*current_i)+2]._index = self._heap[(2*current_i)+2]._index, self._heap[current_i]._index

                    #normal swapping
                    temp = self._heap[current_i]
                    self._heap[current_i] = self._heap[(2*current_i)+2]
                    self._heap[(2*current_i)+2] = temp
                    

                    current_i = (2*current_i)+2
                else:                                       #else break as done
                    break

            elif rc > (length -1):                          #if no right, and smaller than left, swap
                if self._heap[current_i] > self._heap[lc]:
                    #index swapping
                    self._heap[current_i]._index, self._heap[(2*current_i)+1]._index = self._heap[(2*current_i)+1]._index, self._heap[current_i]._index

                    #normal swapping
                    temp = self._heap[current_i]
                    self._heap[current_i] = self._heap[(2*current_i)+1]
                    self._heap[(2*current_i)+1] = temp

                    current_i = (2*current_i)+1
                else:                                       #else break as done sorting
                    break

            elif self._heap[current_i] > self._heap[lc] and self._heap[current_i] > self._heap[rc]: #if smaller than both left and right

                if self._heap[lc] < self._heap[rc]:                     #if left greater than right, swap with left

                    #index swapping
                    self._heap[current_i]._index, self._heap[(2*current_i)+1]._index = self._heap[(2*current_i)+1]._index, self._heap[current_i]._index

                    #normal swapping
                    temp = self._heap[current_i]
                    self._heap[current_i] = self._heap[(2*current_i)+1]
                    self._heap[(2*current_i)+1] = temp
                    current_i = (2*current_i)+1

                else:                                       #else if right greater than left, swap with right
                    #index swapping
                    self._heap[current_i]._index, self._heap[(2*current_i)+2]._index = self._heap[(2*current_i)+2]._index, self._heap[current_i]._index

                    #normal swapping
                    temp = self._heap[current_i]
                    self._heap[current_i] = self._heap[(2*current_i)+2]
                    self._heap[(2*current_i)+2] = temp

                    current_i = (2*current_i)+2

            elif self._heap[current_i] > self._heap[lc]:            #if smaller than left, swap with left

                #index swapping
                self._heap[current_i]._index, self._heap[(2*current_i)+1]._index = self._heap[(2*current_i)+1]._index, self._heap[current_i]._index

                #normal swapping
                temp = self._heap[current_i]
                self._heap[current_i] = self._heap[(2*current_i)+1]
                self._heap[(2*current_i)+1] = temp

                current_i = (2*current_i)+1

            elif self._heap[current_i] > self._heap[rc]:            #if smaller than right, swap with right
                
                #index swapping
                self._heap[current_i]._index, self._heap[(2*current_i)+2]._index = self._heap[(2*current_i)+2]._index, self._heap[current_i]._index

                #normal swapping
                temp = self._heap[current_i]
                self._heap[current_i] = self._heap[(2*current_i)+2]
                self._heap[(2*current_i)+2] = temp

                current_i = (2*current_i)+2                 #reset new current index to keep sorting
            
            else:
                break

    def add(self, key, item):
        elem = Element(key, item, len(self._heap))
        self._heap.append(elem)
        self.bubble_up(elem._index)
        return elem

    def min(self):
        return self._heap[0]

    def remove_min(self):
        #and their indexes

        self._heap[0]._index, self._heap[-1]._index = self._heap[-1]._index, self._heap[0]._index
        #swap 1st and last
        self._heap[0], self._heap[-1] = self._heap[-1], self._heap[0]
   
        self.bubble_down(0)
        return self._heap.pop()

    def update_key(self, elem, new_key):
        elem._key = new_key

        if elem._key < self._heap[((elem._index)-1)//2]._key:
            self.bubble_up(elem._index)

        else:
            self.bubble_down(elem._index)

    def get_key(self, elem):
        return elem._key

    def remove(self, elem):
        #and their indexes
        indexx= elem._index
        self._heap[elem._index]._index, self._heap[-1]._index = self._heap[-1]._index, self._heap[elem._index]._index
        #swap 1st and last
        self._heap[indexx], self._heap[-1] = self._heap[-1],  self._heap[indexx]
        
        self.bubble_down(indexx)
        return self._heap.pop()


class Priority_Queue_List:

    def __init__(self):
        self._pq_list = []

    def __str__(self):
        string = "[ "
        for elem in self._pq_list:
            string += str(elem) + " "

        string+= "]"
        return string

    def length(self):
        return len(self._pq_list)

    def add(self,key,item):
        element = Element(key, item, len(self._pq_list))
        self._pq_list.append(element)
        return element

    def min(self):
        min_key  = self._pq_list[0]._key
        min_elem = self._pq_list[0]
        for elem in self._pq_list:
            if elem._key < min_key:
                min_key = elem._key
                min_elem = elem
        return min_elem

    def remove_min(self):
        minn_elem = self.min()
        ans = self.remove(minn_elem)
        return minn_elem

    def update_key(self, elem, new_key):
        self._pq_list[self._pq_list.index(elem)] = (new_key,elem)

    def get_key(self, elem):
        return elem._key

    def remove(self,elem):
        save_index_org = elem._index
        other_elem = self._pq_list[-1]
        elem._index, other_elem._index = other_elem._index, elem._index
        self._pq_list[save_index_org] = other_elem
        self._pq_list[-1] = elem
        element = self._pq_list.pop(-1)

import math


def prim_w_list(my_graph):

    pq = Priority_Queue_List()
    locs ={}

    for vertex in my_graph.vertices():
        elem = pq.add(math.inf, (vertex, None))
        locs[vertex] = elem
   
    tree = []

    while pq.length() > 0:
        
        min_elem = pq.remove_min()

        cost = min_elem._key
        vertex = min_elem._value[0]
        edge = min_elem._value[1]

        del locs[vertex]
                
        if edge is not None:
            tree.append(str(edge))

        for edge in my_graph.get_edges(vertex):

            other_vertex = edge.opposite(vertex)

            if other_vertex in locs.keys():
                cost = edge._element

                if cost < pq.get_key(locs[other_vertex]):
                    pq.remove(locs[other_vertex])
                    new = pq.add(cost, (other_vertex,edge))
                    locs[other_vertex] = new

    print("WHAT", tree)

def prim_w_heap(my_graph):

    pq = Priority_Queue_Heap()
    locs ={}

    for vertex in my_graph.vertices():
        elem = pq.add(math.inf, (vertex, None))
        locs[vertex] = elem
   
    tree = []

    while pq.length() > 0:
        
        min_elem = pq.remove_min()

        cost = min_elem._key
        vertex = min_elem._value[0]
        edge = min_elem._value[1]

        del locs[vertex]
                
        if edge is not None:
            tree.append(str(edge))

        for edge in my_graph.get_edges(vertex):

            other_vertex = edge.opposite(vertex)

            if other_vertex in locs.keys():
                cost = edge._element

                if cost < pq.get_key(locs[other_vertex]):
                    pq.remove(locs[other_vertex])
                    new = pq.add(cost, (other_vertex,edge))
                    locs[other_vertex] = new

    print("WHATTTT", tree)


import time

if __name__ == "__main__":
    my_graph = make_random_graph(10,45)
    print("Done graph")
    start_time = time.time()  # get start time
    prim_w_heap(my_graph) # Call Prim
    end_time = time.time()  # Record the end time
    execution_time = end_time - start_time  # Calculate the execution time
    print(f"Execution time for heap: {execution_time} seconds")

    start_time = time.time()  # Record the start time
    prim_w_list(my_graph) # Call the function whose execution time you want to measure
    end_time = time.time()  # Record the end time
    execution_time = end_time - start_time  # Calculate the execution time
    print(f"Execution time for list: {execution_time} seconds")

