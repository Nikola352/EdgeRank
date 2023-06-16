from structures.graph import Graph

def load_friends_graph(friends_dir: str) -> Graph:
    names = []
    ids = {}
    friends = []

    curr_id = 0
    with open(friends_dir, "r", encoding="utf-8") as file:
        for line in file.readlines()[1:]:
            row = list(map(lambda x: x.strip(), line.split(',')))
            names.append(row[0])
            ids[row[0]] = curr_id
            curr_id += 1
            friends.append(row[2:])

    g = Graph(names)
    # set edge weight to
    for i, row in enumerate(friends):
        for friend in row:
            g.set_edge_weight(names[i], friend, 1)

    return g