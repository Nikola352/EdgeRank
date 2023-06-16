class Graph:
    def __init__(self, nodes: list = []):
        self._size = len(nodes)
        self._nodes = nodes
        self._ids = self._assign_ids()
        self._mat = [[0] * self._size for _ in range(self._size)]

    def _assign_ids(self):
        ids = {}
        curr_id = 0
        for node in self._nodes:
            ids[node] = curr_id
            curr_id += 1
        return ids
    
    @property
    def nodes(self):
        return self._nodes
    
    def add_node(self, node):
        self._size += 1
        self._nodes.append(node)
        self._ids[node] = self._size - 1
        for row in self._mat:
            row.append(0)
        self._mat.append([0] * self._size)

    def add_nodes(self, nodes: list):
        start_id = self._size
        self._size += len(nodes)
        self._nodes += nodes
        for node in nodes:
            self._ids[node] = start_id
            start_id += 1
        for row in self._mat:
            row += [0] * len(nodes)
        self._mat += [[0] * self._size for _ in range(len(nodes))]

    def set_edge_weight_by_id(self, src:int, dest:int, val:float):
        self._mat[src][dest] = val

    def increase_edge_weight_by_id(self, src:int, dest:int, val:float):
        self._mat[src][dest] += val

    def set_edge_weight(self, src, dest, val:float):
        self.set_edge_weight_by_id(self._ids[src], self._ids[dest], val)

    def increase_edge_weight(self, src, dest, val:float):
        self.increase_edge_weight_by_id(self._ids[src], self._ids[dest], val)
    
    def get_edge_by_id(self, src:int, dest:int) -> float:
        return self._mat[src][dest]
    
    def get_edge(self, src, dest) -> float:
        return self.get_edge_by_id(self._ids[src], self._ids[dest])