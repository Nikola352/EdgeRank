class Graph:
    def __init__(self, nodes: list = [], default_weight: float = 0):
        self._size = len(nodes)
        self._nodes = nodes
        self._ids = self._assign_ids()
        self._adj = [{} for _ in range(self._size)]
        self._default_weight = default_weight

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
        self._nodes.append(node)
        self._ids[node] = self._size
        self._size += 1
        self._adj.append({})

    def add_nodes(self, nodes: list):
        for node in nodes:
            self.add_node(node)

    def set_edge_weight_by_id(self, src:int, dest:int, val:float):
        self._adj[src][dest] = val

    def increase_edge_weight_by_id(self, src:int, dest:int, val:float):
        try:
            self._adj[src][dest] += val
        except KeyError:
            self._adj[src][dest] = val

    def set_edge_weight(self, src, dest, val:float):
        self.set_edge_weight_by_id(self._ids[src], self._ids[dest], val)

    def increase_edge_weight(self, src, dest, val:float):
        self.increase_edge_weight_by_id(self._ids[src], self._ids[dest], val)
    
    def get_edge_by_id(self, src:int, dest:int) -> float:
        try:
            return self._adj[src][dest]
        except KeyError:
            return self._default_weight
    
    def get_edge(self, src, dest) -> float:
        return self.get_edge_by_id(self._ids[src], self._ids[dest])
    
    def get_neighbors_by_id(self, node_id:int) -> list:
        return list(self._adj[node_id].keys())
    
    def get_neighbors(self, node) -> list:
        return map(lambda i: self._nodes[i], self.get_neighbors_by_id(self._ids[node]))
    
    def __contains__(self, node) -> bool:
        # return node in self._nodes # O(n)
        return node in self._ids # O(1)