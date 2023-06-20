from data_utils.parse_files import load_statuses, load_comments, load_reactions, load_shares
from data_utils.friends_graph import load_friends_graph
from ranking.affinity_graph import create_affinity_graph
from structures.graph import Graph
from structures.trie import Trie, create_trie
from entity.status import Status
from entity.comment import Comment
from entity.reaction import Reaction
from entity.share import Share
import pickle


def init_statuses(statuses_dir: str) -> tuple[list[Status], dict[int, Status]]:
    status_list = list(map(lambda status_csv: Status(status_csv), load_statuses(statuses_dir)))
    status_dict = {}
    for status in status_list:
        status_dict[status.status_id] = status
    return status_list, status_dict


def init_affinity_graph(friends_dir: str, statuses: dict, comments_dir: str, reactions_dir: str, shares_dir: str) -> Graph:
    friends_graph = load_friends_graph(friends_dir)
    comments = list(map(lambda comment_csv: Comment(comment_csv), load_comments(comments_dir)))
    reactions = list(map(lambda reaction_csv: Reaction(reaction_csv), load_reactions(reactions_dir)))
    shares = list(map(lambda share_csv: Share(share_csv), load_shares(shares_dir)))
    return create_affinity_graph(friends_graph, statuses, comments, reactions, shares)


def load_affinity_graph(friends_dir: str, statuses: dict, comments_dir: str, reactions_dir: str, shares_dir: str) -> Graph:
    try:
        with open('pickle/graph.pkl', "rb") as file:
            affinity_graph = pickle.load(file)
    except FileNotFoundError:
        affinity_graph = init_affinity_graph(friends_dir, statuses, comments_dir, reactions_dir, shares_dir)
        with open('pickle/graph.pkl', "wb") as file:
            pickle.dump(affinity_graph, file)
    return affinity_graph


def load_trie(status_list: list[Status]) -> dict:
    try:
        with open('pickle/trie.pkl', "rb") as file:
            trie = pickle.load(file)
    except FileNotFoundError:
        trie = create_trie(status_list)
        with open('pickle/trie.pkl', "wb") as file:
            pickle.dump(trie, file)
    return trie


def load_data(friends_dir: str, statuses_dir: str, comments_dir: str, reactions_dir: str, shares_dir: str) -> tuple[Graph, Trie, list[Status], dict]:
    status_list, status_dict = init_statuses(statuses_dir)
    affinity_graph = load_affinity_graph(friends_dir, status_dict, comments_dir, reactions_dir, shares_dir)
    trie = load_trie(status_list)
    return affinity_graph, trie, status_list, status_dict
