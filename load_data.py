from data_utils.init_data import init_statuses, init_affinity_graph
from structures.trie import create_trie
import pickle, time

STATUSES_DIR = "dataset/original_statuses.csv"
FREINDS_DIR = "dataset/friends.csv"
COMMENTS_DIR = "dataset/original_comments.csv"
REACTIONS_DIR = "dataset/original_reactions.csv"
SHARES_DIR = "dataset/original_shares.csv"
GRAPH_DIR = "pickle/graph.pkl"
TRIE_DIR = "pickle/trie_map.pkl"

def main():
    print("Loading statuses...")
    timer = time.time()
    status_list, status_dict = init_statuses(STATUSES_DIR)
    print("Loaded statuses in", time.time()-timer, "seconds")

    print("Creating affinity graph...")
    timer = time.time()
    affinity_graph = init_affinity_graph(FREINDS_DIR, status_dict, COMMENTS_DIR, REACTIONS_DIR, SHARES_DIR)
    with open(GRAPH_DIR, "wb") as file:
        pickle.dump(affinity_graph, file)
    print("Created affinity graph in", time.time()-timer, "seconds")

    print("Creating trie...")
    timer = time.time()
    trie = create_trie(status_list)
    with open(TRIE_DIR, "wb") as file:
        pickle.dump(trie, file)
    print("Created trie map in", time.time()-timer, "seconds")

if __name__ == "__main__":
    main()