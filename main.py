import time
from data_utils.init_data import load_data

def main():
    timer = time.time()
    graph, trie_map, status_list, status_dict = load_data(
        "dataset/friends.csv",
        "dataset/test_statuses.csv",
        "dataset/test_comments.csv",
        "dataset/test_reactions.csv",
        "dataset/test_shares.csv"
    )
    print(time.time() - timer)

if __name__ == "__main__":
    main()