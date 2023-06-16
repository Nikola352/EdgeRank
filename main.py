import time
from data_utils.init_data import load_data
from ranking.edge_rank import edge_rank
from ranking.search import search

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

    timer = time.time()
    results = edge_rank("Shirley Bell", status_list, graph)
    print(time.time() - timer)

    with open("t.txt", "a") as file:
        for result in results:
            file.write(result.status_id + '\n')
            file.write(result.status_message + '\n\n')

    timer = time.time()
    results = search('exposed "donald trump"', status_list, trie_map, "", graph)

    with open("t.txt", "a") as file:
        for result in results:
            file.write(result.status_id + '\n')
            file.write(result.status_message + '\n\n')

if __name__ == "__main__":
    main()