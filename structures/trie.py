from entity.status import Status

class Trie:
    class Node:
        def __init__(self) -> None:
            self.children = {}
            self.statuses = {} # {status_id: count of word in status}
            self.total_count = 0

    def __init__(self) -> None:
        self._root = self.Node()
        self._size = 0

    def search(self, s: str) -> dict[str, int]:
        curr = self._root
        for ch in s:
            if ch not in curr.children:
                return {}
            curr = curr.children[ch]
        return curr.statuses
    
    def insert(self, s: str, status_id: str) -> None:
        self._size += 1
        curr = self._root
        for ch in s:
            if ch not in curr.children:
                curr.children[ch] = self.Node()
            curr = curr.children[ch]
        if status_id in curr.statuses:
            curr.statuses[status_id] += 1
        else:
            curr.statuses[status_id] = 1
        curr.total_count += 1 

    def _candidate_util(self, node: Node) -> list[tuple[str, int]]:
        candidates = []
        if node.total_count > 0:
            candidates.append(("", node.total_count))
        for ch in node.children:
            for cand, cnt in self._candidate_util(node.children[ch]):
                candidates.append((ch+cand, cnt))
        return candidates

    def autocomplete_candidates(self, s: str) -> list[tuple[str, int]]:
        curr = self._root
        for ch in s:
            if ch not in curr.children:
                return []
            curr = curr.children[ch]
        candidates = self._candidate_util(curr)
        candidates.sort(key=lambda x: x[1], reverse=True)
        candidates = list(map(lambda x: s+x[0], candidates))
        return candidates

    def __len__(self) -> int:
        return self._size
    

def create_trie(statuses: list[Status]) -> Trie:
    trie = Trie()
    for status in statuses:
        words = status.status_message.split()
        words = ["".join(filter(str.isalnum, word)) for word in words] # remove non-alphanumeric characters
        words = list(filter(lambda word: word != "", words)) # remove empty string
        words = list(map(lambda word: word.lower(), words)) # to lower case
        for word in words:
            trie.insert(word, status.status_id)
    return trie
