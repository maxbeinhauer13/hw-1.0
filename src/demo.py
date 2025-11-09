# demo.py
import os
from pathlib import Path
from typing import List
from .shingling import Shingling

def load_folder(folder_path: str) -> List[str]:
    docs: List[str] = []
    for filename in sorted(os.listdir(folder_path)):
        if filename.lower().endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read().strip()
                if text:
                    docs.append(text)
    return docs

def jaccard(a: set[int], b: set[int]) -> float:
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)

if __name__ == "__main__":
    # where your text files are
    data_folder = Path(__file__).resolve().parents[1] / "data" / "docs16"

    # load the documents
    docs = load_folder(str(data_folder))
    print(f"Loaded {len(docs)} documents.\n")

    # preview them
    for i, text in enumerate(docs, start=1):
        print(f"Document {i}: {len(text)} characters")
        print(text[:200].replace("\n", " "))  # show first 200 characters
        print("-" * 60)

    # create shingle sets
    s = Shingling(k=9)
    shingle_sets = [s.shingles(doc) for doc in docs]

    # compute pairwise Jaccard
    print("\nPairwise Jaccard similarities (top 5):")
    pairs = []
    n = len(shingle_sets)
    for i in range(n):
        for j in range(i + 1, n):
            sim = jaccard(shingle_sets[i], shingle_sets[j])
            pairs.append(((i + 1, j + 1), sim))

    pairs.sort(key=lambda x: x[1], reverse=True)
    for (i, j), sim in pairs[:5]:
        print(f"Docs ({i}, {j}) -> Jaccard = {sim:.3f}")
