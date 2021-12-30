# Author: Dylan Smith
# Description: Implements a directed graph ADT. Only one edge between vertices can exist, no loops, edges have positive
#               weight, and vertex names are integers. Methods include adding and getting vertices, adding, removing,
#               and getting edges, performing a depth-first and breadth-first search, determining if a given path is
#               valid, determine if a graph has a cycle, and performing Dijkstra's algorithm for a given vertex.

class DirectedGraph:
    """
    Class to implement directed weighted graph
    - duplicate edges not allowed
    - loops not allowed
    - only positive edge weights
    - vertex names are integers
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency matrix
        """
        self.v_count = 0
        self.adj_matrix = []

        # Populate graph with initial vertices and edges (if provided)
        # Before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            v_count = 0
            for u, v, _ in start_edges:
                v_count = max(v_count, u, v)
            for _ in range(v_count + 1):
                self.add_vertex()
            for u, v, weight in start_edges:
                self.add_edge(u, v, weight)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        """
        if self.v_count == 0:
            return 'EMPTY GRAPH\n'
        out = '   |'
        out += ' '.join(['{:2}'.format(i) for i in range(self.v_count)]) + '\n'
        out += '-' * (self.v_count * 3 + 3) + '\n'
        for i in range(self.v_count):
            row = self.adj_matrix[i]
            out += '{:2} |'.format(i)
            out += ' '.join(['{:2}'.format(w) for w in row]) + '\n'
        out = f"GRAPH ({self.v_count} vertices):\n{out}"
        return out

    # ------------------------------------------------------------------ #

    def add_vertex(self) -> int:
        """
        Adds a new vertex to the graph
        """
        v = []
        self.v_count += 1
        for i in range(self.v_count):
            # Creates sublist for new vertex
            v.append(0)
        for vertex in self.adj_matrix:
            # Appends new index to each vertex of the graph
            vertex.append(0)
        self.adj_matrix.append(v)
        return self.v_count

    def add_edge(self, src: int, dst: int, weight=1) -> None:
        """
        Adds an edge to the graph
        Src and dst cannot be the same
        Weight must not be negative
        Src and dst must be valid vertices
        """
        if src != dst and weight >= 0 and len(self.adj_matrix) > src and len(self.adj_matrix) > dst:
            # Assigns new edge if valid
            self.adj_matrix[src][dst] = weight

    def remove_edge(self, src: int, dst: int) -> None:
        """
        Removes an edge between src and dst, setting the weight to 0
        """
        if len(self.adj_matrix) > src and len(self.adj_matrix) > dst and src >= 0 and dst >= 0:
            # If src and dst are valid vertices, sets weight of edge to 0, removing it from graph
            self.adj_matrix[src][dst] = 0

    def get_vertices(self) -> []:
        """
        Returns a list of vertices in the graph
        """
        vertices = []
        for v in range(self.v_count):
            # Appends all vertices to list
            vertices.append(v)
        return vertices

    def get_edges(self) -> []:
        """
        Returns the edges of the graph as a list of tuples
        Each tuple is set-up as (source, destination, weight)
        """
        edges = []
        v_count = 0
        for v in self.adj_matrix:
            # Iterate through each vertex
            u_count = 0
            for u in v:
                # Iterate through each possible edge
                if u != 0:
                    # Edge found, create tuple and add to list
                    edge = (v_count, u_count, u)
                    edges.append(edge)
                u_count += 1
            v_count += 1
        return edges

    def is_valid_path(self, path: []) -> bool:
        """
        Returns true if provided path is valid, False otherwise
        """
        if path == []:
            # Path is empty
            return True
        count = 0
        for v in path:
            # Iterate through path
            count += 1
            if count == len(path):
                # End of path reached, path valid
                return True
            u = path[count]
            if self.adj_matrix[v][u] == 0:
                # No edge connecting to next vertex, path invalid
                return False

    def dfs(self, v_start, v_end=None) -> []:
        """
        Returns a list of vertices visited during DFS search
        Vertices are picked in ascending numerical order
        """
        visited = []
        stack = []
        if v_start > len(self.adj_matrix):
            # v_start not in graph
            return visited
        stack.append(v_start)
        while len(stack) != 0:
            # Runs until the stack is empty
            v = stack.pop(len(stack) - 1)
            if v not in visited:
                # Vertex has not been visited, process
                visited.append(v)
                temp_list = []
                count = 0
                for u in self.adj_matrix[v]:
                    # Add all adjacent vertices to temporary list
                    if u != 0:
                        temp_list.append(count)
                    count += 1
                temp_list.sort(reverse=True)  # Sort temp_list in reverse descending order
                for u in temp_list:
                    # Add temp_list to stack, search succession will now be in depth-first ascending order
                    stack.append(u)
            if v == v_end:
                # Target found, end search
                break
        return visited

    def bfs(self, v_start, v_end=None) -> []:
        """
        Returns a list of vertices visited during BFS search
        Vertices are picked in ascending numerical order
        """
        queue = []
        visited = []
        if v_start > len(self.adj_matrix):
            # v_start not in graph
            return visited
        queue.append(v_start)
        while len(queue) != 0:
            # Runs until the queue is empty
            v = queue.pop(0)
            if v not in visited:
                # Vertex has not been visited, process
                visited.append(v)
                temp_list = []
                count = 0
                for u in self.adj_matrix[v]:
                    # Add all adjacent vertices to temporary list
                    if u != 0:
                        temp_list.append(count)
                    count += 1
                temp_list.sort()  # Sort temp_list in ascending order
                for u in temp_list:
                    # Add temp_list to queue, search succession will now be in breadth-first ascending order
                    queue.append(u)
            if v == v_end:
                # Target of search found, ends search
                break
        return visited

    def has_cycle(self):
        """
        Returns True if graph contains a cycle, False otherwise
        """
        visited = []
        count = 0
        for v in self.adj_matrix:
            # Iterate through all vertices in graph
            if count not in visited:
                # Vertex not previously visited
                if (self.has_Cycle_helper(count, visited)) == True:
                    # Cycle found
                    return True
            count += 1
        return False

    def has_Cycle_helper(self, v, visited):
        """
        Helper function for has_cycle
        """
        visited.append(v)
        count = 0
        for i in self.adj_matrix[v]:
            # Iterate through all adjacent vertices
            if count not in visited and i != 0:
                if (self.has_Cycle_helper(count, visited)) == True:
                    # Cycle found
                    return True
            elif count in visited and i != 0:
                # Cycle found
                return True
            count += 1
        visited.pop(len(visited) - 1) # Remove v from visited
        return False

    def dijkstra(self, src: int) -> []:
        """
        Returns the shortest path from src to every other vertex of the graph as a list
        """
        map = []  # Tracks minimum distance to each point from src
        visited = []  # Tracks visited vertices
        for v in range(self.v_count):
            # Initialize map with every point requiring infinite distance to reach
            map.append(float('inf'))
        queue = [(src, 0)]
        while len(queue) != 0:
            # Run until queue empty
            v = queue[0][0]
            d = queue[0][1]
            di = d
            queue.pop(0)
            if d < map[v]:
                # If distance to v is less than current minimum, replace value
                map[v] = d
            vi = 0
            for d in self.adj_matrix[v]:
                # Iterate through all vertices and search for edges
                if d != 0 and vi not in visited:
                    # Edge found, vertex unvisited, add to queue
                    queue.append((vi, di + d))
                elif d != 0 and vi in visited and (di + d) < map[vi]:
                    # Smaller distance found for previously visited vertex
                    queue.append((vi, di + d))
                vi += 1
            visited.append(v)
        return map
