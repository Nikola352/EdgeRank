from structures.graph import Graph
from entity.comment import Comment
from entity.reaction import Reaction
from entity.share import Share
from ranking.edge_rank import time_decay_factor, reaction_score


FREINDS_WEIGHT = 20
COMMENT_WEIGHT = 7
REACTION_WEIGHT = 1
SHARE_WEIGHT = 5


def comment_affinity(comment: Comment) -> float:
    score = reaction_score(
        comment.num_likes, 
        comment.num_loves, 
        comment.num_wows, 
        comment.num_hahas, 
        comment.num_sads, 
        comment.num_angrys, 
        comment.num_special
    )
    if not comment.parent_id:
        score *= 1.5
    return COMMENT_WEIGHT * score * time_decay_factor(comment.date_published)


def reaction_affinity(reaction: Reaction) -> float:
    if reaction.type_of_reaction == "likes":
        score = 1
    elif reaction.type_of_reaction == "loves":
        score = 2.5
    elif reaction.type_of_reaction == "wows":
        score = 2
    elif reaction.type_of_reaction == "hahas":
        score = 2
    elif reaction.type_of_reaction == "sads":
        score = 2
    elif reaction.type_of_reaction == "angrys":
        score = 2
    elif reaction.type_of_reaction == "specials":
        score = 3
    else:
        score = 0
    return REACTION_WEIGHT * score * time_decay_factor(reaction.date_reacted)


def share_affinity(share: Share) -> float:
    return SHARE_WEIGHT * time_decay_factor(share.date_shared)


def add_affinity(affinity_graph: Graph, friends_graph: Graph, statuses: dict, comments: list[Comment], reactions: list[Reaction], shares: list[Share]) -> Graph:
    users = affinity_graph.nodes
    for user1 in users:
        for user2 in users:
            if user1 == user2:
                continue
            if friends_graph.get_edge(user1, user2) > 0:
                affinity_graph.increase_edge_weight(user1, user2, FREINDS_WEIGHT)

    for comment in comments:
        affinity_graph.increase_edge_weight(comment.author, statuses[comment.status_id].author, comment_affinity(comment))

    for reaction in reactions:
        affinity_graph.increase_edge_weight(reaction.reactor, statuses[reaction.status_id].author, reaction_affinity(reaction))

    for share in shares:
        affinity_graph.increase_edge_weight(share.sharer, statuses[share.status_id].author, share_affinity(share))

    for user1 in users:
        for user2 in users:
            if user1 == user2:
                continue
            affinity_graph.increase_edge_weight(user1, user2, 1)

    return affinity_graph


def create_affinity_graph(friends_graph: Graph, statuses: dict, comments: list[Comment], reactions: list[Reaction], shares: list[Share]) -> Graph:
    affinity_graph = Graph(friends_graph.nodes)
    return add_affinity(affinity_graph, friends_graph, statuses, comments, reactions, shares)