import time
from data_utils.init_data import load_data
from cli import cli


def main():
    print("Welcome to EdgeRank!")

    print("Loading data...")
    timer = time.time()
    graph, trie, status_list, status_dict = load_data(
        "dataset/friends.csv",
        "dataset/test_statuses.csv",
        "dataset/test_comments.csv",
        "dataset/test_reactions.csv",
        "dataset/test_shares.csv"
    )
    print("Data loaded in", time.time() - timer, "seconds")

    user = cli.login()
    cli.show_feed(user, status_list, graph)
    cli.run_search(user, status_list, trie, graph)


if __name__ == "__main__":
    main()