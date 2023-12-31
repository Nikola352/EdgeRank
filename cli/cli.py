import time
from entity.status import Status
from ranking.edge_rank import edge_rank
from ranking.search import search as search, parse_query
from structures.graph import Graph
from structures.trie import Trie


def login() -> str:
    print("Login")
    print("---------------")
    print("Enter your name:")
    username = input()
    print("---------------")
    return username


def highlight_message(message: str, words: list[str], phrases: list[str]) -> str:
    message_words = message.split()
    reduced_message_words = ["".join(filter(str.isalnum, word)) for word in message_words] # remove non-alphanumeric characters
    reduced_message_words = list(map(lambda word: word.lower(), reduced_message_words)) # to lower case

    for word, reduced_word in zip(message_words, reduced_message_words):
        if reduced_word in words:
            highlighted_word = "\033[1;33m" + word + "\033[0m"
            message_words[message_words.index(word)] = highlighted_word

    message = " ".join(message_words)

    for phrase in phrases:
        if phrase in message:
            message = message.replace(phrase, "\033[1;33m" + phrase + "\033[0m")

    return message


def show_feed(user: str, statuses: list[Status], affinity_graph: Graph):
    print("\033[1;36mPERSONALIZED FEED\033[0m")
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


class EndOfInputException(Exception): pass


def show_autocomplete(query: str, trie: Trie):
    words = query.lower().split()
    last_word = words[-1][:-1]
    candidates = trie.autocomplete_candidates(last_word)

    print(f"\nAUTOCOMPLETE ACTIVATED")
    for i, word in enumerate(candidates):
        print(f'{i+1}. {word}')
    print(f'{len(candidates)+1}. {last_word} (keep the original)')

    valid_input = False
    while not valid_input:
        try:
            idx = input(f"Choose an option (1-{len(candidates)+1}): ")
            idx = int(idx) - 1
            if idx < 0 or idx > len(candidates):
                raise ValueError
            valid_input = True
        except ValueError:
            print("\033[1;31mInvalid option!\033[0m")
    
    if idx == len(candidates):
        words[-1] = last_word
    else:
        words[-1] = candidates[idx]

    return ''.join(words)


def run_search(user: str, statuses: list[Status], trie: Trie, affinity_graph: Graph):
    while True:
        print("\033[1;36mSEARCH\033[0m")
        print("---------------")
        print("Enter a keyword to search for in the feed, or type 'exit' to quit the program:")
        keyword = input()

        if keyword == 'exit':
            break

        if keyword.endswith('*'):
            keyword = show_autocomplete(keyword, trie)

        print("---------------")
        print("Here are the most relevant posts for your search:")

        words, phrases = parse_query(keyword)

        results = search(keyword, statuses, trie, user, affinity_graph)

        for result in results:
            print('====================')
            print(highlight_message(result.status_message, words, phrases))
            # print(result.status_message)
            print("Type:", result.status_type)
            print("Link:", result.status_link)
            print("Published:", time.strftime("%d-%m-%Y %H:%M:%S", result.date_published))
            print("Author:", result.author)
            print("Reactions:", result.num_reactions)
            print("Comments:", result.num_comments)
            print("Shares:", result.num_shares)
            print("====================\n")
        
        print("---------------")
