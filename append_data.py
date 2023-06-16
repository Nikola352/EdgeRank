from data_utils.friends_graph import load_friends_graph
from data_utils.init_data import init_statuses, init_affinity_graph
from entity.comment import Comment
from entity.reaction import Reaction
from entity.share import Share
from structures.graph import Graph
from structures.trie import create_trie_map
from ranking.affinity_graph import add_affinity
from data_utils.parse_files import *
import pickle, time

STATUSES_DIR = "dataset/test_statuses.csv"
FREINDS_DIR = "dataset/friends.csv"
COMMENTS_DIR = "dataset/test_comments.csv"
REACTIONS_DIR = "dataset/test_reactions.csv"
SHARES_DIR = "dataset/test_shares.csv"
GRAPH_DIR = "pickle/graph.pkl"
TRIE_MAP_DIR = "pickle/trie_map.pkl"

OLD_STATUSES_DIR = "dataset/original_statuses.csv"
NEW_STATUSES_DIR = "dataset/new_statuses.csv"

def main():
    print("Loading existing statuses...")
    timer = time.time()
    status_list, status_dict = init_statuses(OLD_STATUSES_DIR)
    print("Loaded statuses in", time.time()-timer, "seconds")

    print("Loading new statuses...")
    timer = time.time()
    new_status_list, new_status_dict = init_statuses(STATUSES_DIR)
    print("Loaded statuses in", time.time()-timer, "seconds")

    print("Updating statuses...")
    timer = time.time()
    status_list.extend(new_status_list)
    status_dict.update(new_status_dict)
    with open(NEW_STATUSES_DIR, "w") as file:
        for status in status_list:
            file.write(str(status))
    print("Updated statuses in", time.time()-timer, "seconds")

    print("Loading affinity graph...")
    with open(GRAPH_DIR, "rb") as file:
        affinity_graph: Graph = pickle.load(file)
    friends_graph = load_friends_graph(FREINDS_DIR)
    comments = list(map(lambda comment_csv: Comment(comment_csv), load_comments(COMMENTS_DIR)))
    reactions = list(map(lambda reaction_csv: Reaction(reaction_csv), load_reactions(REACTIONS_DIR)))
    shares = list(map(lambda share_csv: Share(share_csv), load_shares(SHARES_DIR)))

    print("Updating affinity graph...")
    timer = time.time()
    affinity_graph.add_nodes(friends_graph.nodes)
    add_affinity(affinity_graph, friends_graph, status_dict, comments, reactions, shares)
    with open(GRAPH_DIR, "wb") as file:
        pickle.dump(affinity_graph, file)
    print("Updated affinity graph in", time.time()-timer, "seconds")

    print("Loading trie map...")
    with open(TRIE_MAP_DIR, "rb") as file:
        trie_map: dict = pickle.load(file)

    print("Updating trie map...")
    timer = time.time()
    new_trie_map = create_trie_map(new_status_list)
    trie_map.update(new_trie_map)
    with open(TRIE_MAP_DIR, "wb") as file:
        pickle.dump(trie_map, file)
    print("Updated trie map in", time.time()-timer, "seconds")

if __name__ == "__main__":
    main()