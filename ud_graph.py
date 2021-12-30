# Author: Dylan Smith
# Description: Implements an undirected graph ADT. Only one edge between vertices can exist, no loops, edges don't
#               have weight, and vertex names are strings. Methods include adding, removing and getting vertices and
#               edges, performing a depth-first and breadth-first search, determining if a given path is valid, count
#               the number of connected components, and determine if a graph has a cycle.


class UndirectedGraph:
    """
    Class to implement undirected graph
    - duplicate edges not allowed
    - loops not allowed
    - no edge weights
    - vertex names are strings
    """

    def __init__(self, start_edges=None):
        """
        Stores graph info as adjacency list
        """
        self.adj_list = dict()

        # Populate graph with initial vertices and edges (if provided)
        # Before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            for u, v in start_edges:
                self.add_edge(u, v)

    def __str__(self):
        """
        Returns content of the graph in human-readable form
        """
        out = [f'{v}: {self.adj_list[v]}' for v in self.adj_list]
        out = '\n  '.join(out)
        if len(out) < 70:
            out = out.replace('\n  ', ', ')
            return f'GRAPH: {{{out}}}'
        return f'GRAPH: {{\n  {out}}}'

    # ------------------------------------------------------------------ #

    def add_vertex(self, v: str) -> None:
        """
        Adds a new vertex to the graph
        """
        if v not in self.adj_list:
            # Adds new vertex if one by the same name is not already in the graph
            self.adj_list[v] = []
        
    def add_edge(self, u: str, v: str) -> None:
        """
        Adds an edge to the graph
        Adds vertices if one or both are not already in the graph
        """
        if u not in self.adj_list and v != u:
            # Adds u as a vertex if it does not exist
            self.add_vertex(u)
        if v not in self.adj_list and v != u:
            # Adds v as a vertex if it does not exist
            self.add_vertex(v)
        if v != u and v not in self.adj_list.get(u) and u not in self.adj_list.get(v):
            # Creates edge between v and u if they are not same vertex and if the edge does not already exist
            self.adj_list[v].append(u)
            self.adj_list[u].append(v)

    def remove_edge(self, v: str, u: str) -> None:
        """
        Removes specified edge from the graph
        """
        if v and u in self.adj_list and v in self.adj_list.get(u) and u in self.adj_list.get(v):
            # Removes v and u from each other's adjacency list if the vertices exist and an edge between them exists
            self.adj_list[v].remove(u)
            self.adj_list[u].remove(v)

    def remove_vertex(self, v: str) -> None:
        """
        Removes specified vertex and all connected edges from the graph
        """
        if v in self.adj_list:
            # Removes v if it exists in graph
            self.adj_list.pop(v)
            for key in self.adj_list:
                # Removes all edges that existed between v and other vertices
                if v in self.adj_list.get(key):
                    self.adj_list[key].remove(v)

    def get_vertices(self) -> []:
        """
        Returns a list of vertices in the graph (any order)
        """
        keys = []
        for key in self.adj_list:
            # Iterates through keys of dictionary and adds them to list
            keys.append(key)
        return keys

    def get_edges(self) -> []:
        """
        Returns a list of edges in the graph (any order)
        """
        edges = []
        for key in self.adj_list:
            # Iterates through keys of dictionary
            for value in self.adj_list.get(key):
                # Iterates through list of values of each key and makes a tuple of (key, value)
                pair = (key, value)
                if (value, key) not in edges:
                    # Adds tuple to list if the reversed tuple is not already in the list (avoids duplicate edges)
                    edges.append(pair)
        return edges

    def is_valid_path(self, path: []) -> bool:
        """
        Returns true if provided path is valid, False otherwise
        """
        if path == []:
            # Empty path, return True
            return True
        if len(path) == 1:
            # Case of one element path
            if path[0] not in self.adj_list:
                # Vertex not in graph, return False
                return False
        for v in range(len(path) - 1):
            # Case of multi-element path
            if path[v] not in self.adj_list:
                # Vertex not in graph, return False
                return False
            if path[v + 1] not in self.adj_list.get(path[v]):
                # No edge exists between current vertex and next in path, return False
                return False
        return True

    def dfs(self, v_start, v_end=None) -> []:
        """
        Returns a list of vertices visited during DFS search
        Vertices are picked in alphabetical order
        """
        stack = []
        visited = []
        if v_start not in self.adj_list:
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
                for u in self.adj_list[v]:
                    # Add all adjacent vertices to temporary list
                    temp_list.append(u)
                temp_list.sort(reverse=True)  # Sort temp_list in reverse alphabetical order
                for u in temp_list:
                    # Add temp_list to stack, search succession will now be in depth-first alphabetical order
                    stack.append(u)
            if v == v_end:
                # Target of search found, ends search
                break
        return visited

    def bfs(self, v_start, v_end=None) -> []:
        """
        Returns a list of vertices visited during BFS search
        Vertices are picked in alphabetical order
        """
        queue = []
        visited = []
        if v_start not in self.adj_list:
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
                for u in self.adj_list[v]:
                    # Add all adjacent vertices to temporary list
                    temp_list.append(u)
                temp_list.sort()  # Sort temp_list in alphabetical order
                for u in temp_list:
                    # Add temp_list to queue, search succession will now be in breadth-first alphabetical order
                    queue.append(u)
            if v == v_end:
                # Target of search found, ends search
                break
        return visited

    def count_connected_components(self):
        """
        Returns number of connected components in the graph
        """
        visited = []
        count = 0
        for v in self.adj_list:
            # Check all vertices of graph
            if v not in visited:
                # Vertex not in visited, continue processing
                self.count_helper(v, visited)
                count += 1
        return count

    def count_helper(self, v, visited):
        """
        Helper function recursively called to determine connected components
        """
        visited.append(v)
        for u in self.adj_list[v]:
            # Check each vertex adjacent to v
            if u not in visited:
                # Vertex not visited, continue processing
                self.count_helper(u, visited)

    def has_cycle(self):
        """
        Returns True if graph contains a cycle, False otherwise
        """
        visited = []
        for v in self.adj_list:
            # Iterate through all vertices in graph
            if v not in visited:
                # Vertex not previously visited
                if (self.has_Cycle_helper(v, visited, -1)) == True:
                    # Cycle found
                    return True
        return False

    def has_Cycle_helper(self, v, visited, parent):
        """
        Helper function for has_cycle
        """
        visited.append(v)
        for i in self.adj_list[v]:
            # Iterate through all adjacent vertices
            if i not in visited:
                if (self.has_Cycle_helper(i, visited, v)) == True:
                    # Cycle found
                    return True
            elif parent != i:
                # Cycle found
                return True
        return False
