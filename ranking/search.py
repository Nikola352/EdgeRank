import math
from entity.status import Status
from ranking.edge_rank import edge_rank_score
from structures.graph import Graph
from structures.trie import Trie


WORD_WEIGHT = 100
PHRASE_WEIGHT = 100
COUNT_WEIGHT = 1


def word_score(words: list[str], trie: Trie) -> float:
    score = 0
    for word in words:
        count = trie.search(word)
        score += COUNT_WEIGHT * math.log2(count+1)
        if count > 0:
            score += WORD_WEIGHT
    return score


def lps_table(pattern: str) -> list[int]:
    m = len(pattern)
    lps = [0] * m
    i, j = 1, 0
    while i < m:
        if pattern[i] == pattern[j]:
            j += 1
            lps[i] = j
            i += 1
        else:
            if j != 0:
                j = lps[j-1]
            else:
                lps[i] = 0
                i += 1
    return lps

# returns the count of pattern in text
def kmp_count(text: str, pattern: str) -> int:
    n, m = len(text), len(pattern)
    count = 0
    lps = lps_table(pattern)
    i, j = 0, 0
    while i < n:
        if text[i] == pattern[j]:
            i += 1
            j += 1
        if j == m:
            count += 1
            j = lps[j-1]
        elif i < n and text[i] != pattern[j]:
            if j != 0:
                j = lps[j-1]
            else:
                i += 1
    return count

# TODO: maybe only run kmp instead of trie when the phrase is long enough?
def phrase_score(phrases: list[str], status: Status) -> float:
    score = 0
    for phrase in phrases:
        count = kmp_count(status.status_message, phrase)
        score += COUNT_WEIGHT * math.log2(count+1)
        if count > 0:
            score += PHRASE_WEIGHT
    return score


# returns the score of a status
# words: list of words to search for
# phrases: list of phrases to search for (phrases contain multiple words)
def search_score(status: Status, words: list[str], phrases: list[str], trie_map: dict, user: str, affinity_graph: Graph) -> float:
    return word_score(words, trie_map[status.status_id]) + phrase_score(phrases, status) + math.log10(edge_rank_score(status, user, affinity_graph))


def search(query: str, statuses: list[Status], trie_map: dict, user: str, affinity_graph: Graph) -> list[Status]:
    words, phrases = parse_query(query)
    return sorted(statuses, key=lambda status: search_score(status, words, phrases, trie_map, user, affinity_graph), reverse=True)[:10]


# splits query into to lists:
# phrases: substrings surrounded by quotes ("")
# words: rest of the words in the string split by whitespace
def parse_query(query: str) -> tuple[list[str], list[str]]:
    all_words = query.split()
    words = []
    phrases = []
    current_phrase = None
    for word in all_words:
        if current_phrase:
            if word.endswith('"'):
                current_phrase += " " + word[:-1]
                phrases.append(current_phrase)
                current_phrase = None
            else:
                current_phrase += word
        elif word.startswith('"'):
            if word.endswith('"'):
                current_phrase = word[1:-1]
                phrases.append(current_phrase)
                current_phrase = None
            else:
                current_phrase = word[1:]
        else:
            words.append(word)

    words = ["".join(filter(str.isalnum, word)) for word in words] # remove non-alphanumeric characters
    words = list(filter(lambda word: word != "", words)) # remove empty string
    words = list(map(lambda word: word.lower(), words)) # to lower case

    # Note: do not do any filtering on phrases, just search for the exact substring

    return words, phrases


