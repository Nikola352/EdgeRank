from typing import Union
from entity.status import Status

class Trie:
    class Node:
        def __init__(self, count:int=0):
            self.children = {}
            self.count = count

    def __init__(self) -> None:
        self._root = self.Node()

    def search(self, s: str) -> Union[int, None]:
        curr = self._root
        for ch in s:
            if ch not in curr.children:
                return None
            curr = curr.children[ch]
        return curr.count
    
    def insert(self, s: str) -> None:
        curr = self._root
        for ch in s[:-1]:
            if ch not in curr.children:
                curr.children[ch] = self.Node()
            curr = curr.children[ch]
        if s[-1] not in curr.children:
            curr.children[s[-1]] = self.Node(1)
        else:
            curr.children[s[-1]].count += 1

def create_trie(status: Status) -> Trie:
    trie = Trie()
    words = status.status_message.split()
    words = ["".join(filter(str.isalnum, word)) for word in words] # remove non-alphanumeric characters
    words = list(filter(lambda word: word != "", words)) # remove empty string
    words = list(map(lambda word: word.lower(), words)) # to lower case
    for word in words:
        trie.insert(word)
    return trie

def create_trie_map(statuses: list) -> dict:
    trie_map = {}
    for status in statuses:
        trie_map[status.status_id] = create_trie(status)
    return trie_map