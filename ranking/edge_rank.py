import time

from entity.status import Status
from structures.graph import Graph


TIME_DECAY_FACTOR = 0.5
REACTION_WEIGHT = 1
COMMENT_WEIGHT = 3
SHARE_WEIGHT = 3


def time_decay_factor(current_time: time.struct_time):
    time_delta = time.time() - time.mktime(current_time)
    if time_delta < 3600: # 1 hour
        return 20 * TIME_DECAY_FACTOR ** (time_delta / 3600)
    elif time_delta < 86400: # 1 day
        return 5 * TIME_DECAY_FACTOR ** (time_delta / 86400)
    elif time_delta < 604800: # 1 week
        return TIME_DECAY_FACTOR ** (time_delta / 604800)
    elif time_delta < 2419200: # 1 month
        return 0.5 * TIME_DECAY_FACTOR ** (time_delta / 2419200)
    else: # yearly scale
        return 0.1 * TIME_DECAY_FACTOR ** (time_delta / 31536000)
    

def reaction_score(likes: int, loves: int, wows: int, hahas: int, sads:int, angrys: int, specials: int) -> int:
    return likes + 2.5*loves + 2*wows + 2*hahas + 2*sads + 2*angrys + 3*specials


def status_weight(status: Status):
    score = REACTION_WEIGHT * reaction_score(
        status.num_likes, 
        status.num_loves, 
        status.num_wows, 
        status.num_hahas, 
        status.num_sads, 
        status.num_angrys, 
        status.num_special
    )
    score += COMMENT_WEIGHT * status.num_comments
    score += SHARE_WEIGHT * status.num_shares
    if status.status_type == "photo":
        score *= 1.5
    return score


def edge_rank_score(status: Status, user: str, affinity_graph):
    return affinity_graph[user][status.author] * status_weight(status) * time_decay_factor(status.date_published)


def edge_rank(user: str, statuses: list[Status], affinity_graph: Graph) -> list[Status]:
    return sorted(statuses, key=lambda status: edge_rank_score(status, user, affinity_graph))