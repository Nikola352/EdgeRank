import time
from entity.status import Status
from ranking.edge_rank import edge_rank
from ranking.search import search as post_search
from structures.graph import Graph


def login() -> str:
    print("Login")
    print("---------------")
    print("Enter your name:")
    username = input()
    print("---------------")
    return username


def show_feed(user: str, statuses: list[Status], affinity_graph: Graph):
    print("Personalized feed")
    print("---------------")
    print("Here are the most relevant posts in your feed:")

    results = edge_rank(user, statuses, affinity_graph)

    for result in results:
        print('====================')
        print(result.status_message)
        print("Type:", result.status_type)
        print("Link:", result.status_link)
        print("Published:", time.strftime("%d-%m-%Y %H:%M:%S", result.date_published))
        print("Author:", result.author)
        print("Reactions:", result.num_reactions)
        print("Comments:", result.num_comments)
        print("Shares:", result.num_shares)
        print("====================\n")
    
    print("---------------")


def search(user: str, statuses: list[Status], trie_map: dict[str, list[Status]], affinity_graph: Graph):
    while True:
        print("Search")
        print("---------------")
        print("Enter a keyword to search for in the feed, or type 'exit' to quit the program:")
        keyword = input()

        if keyword == 'exit':
            break

        print("---------------")
        print("Here are the most relevant posts for your search:")

        results = post_search(keyword, statuses, trie_map, user, affinity_graph)

        for result in results:
            print('====================')
            print(result.status_message)
            print("Type:", result.status_type)
            print("Link:", result.status_link)
            print("Published:", time.strftime("%d-%m-%Y %H:%M:%S", result.date_published))
            print("Author:", result.author)
            print("Reactions:", result.num_reactions)
            print("Comments:", result.num_comments)
            print("Shares:", result.num_shares)
            print("====================\n")
        
        print("---------------")
