import hashlib
from typing import Set


def stable_hash(s: str) -> int:
    """Return a stable integer hash for a string."""
    return int(hashlib.sha1(s.encode("utf-8")).hexdigest()[:16], 16)


class Shingling:
    def __init__(self, k: int = 5, keep_space: bool = True):
        """
        k: shingle length (number of characters)
        keep_space: if True, normalize spaces but keep them;
                    if False, remove all whitespace.
        """
        self.k = k
        self.keep_space = keep_space

    def _normalize(self, text: str) -> str:
        t = text.lower()
        if self.keep_space:
            # collapse multiple spaces/newlines to a single space
            t = " ".join(t.split())
        else:
            # remove all whitespace
            t = "".join(t.split())
        return t

    def shingles(self, text: str) -> Set[int]:
        """
        Return a set of hashed k-gram shingles for the given text.
        """
        t = self._normalize(text)
        if not t:
            return set()
        if len(t) <= self.k:
            return {stable_hash(t)}
        return {
            stable_hash(t[i : i + self.k])
            for i in range(len(t) - self.k + 1)
        } 