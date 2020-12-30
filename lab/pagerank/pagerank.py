import os
import random
import re
import sys
import numpy as np

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    if len(corpus[page]) == 0:
        prob_distribution = dict.fromkeys(corpus.keys(), 1/len(corpus))
    else:
        prob_distribution = dict.fromkeys(corpus.keys(), (1-damping_factor)/len(corpus))
        for p in corpus[page]:
            prob_distribution[p] += damping_factor/len(corpus[page])
    return prob_distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pagerank = dict.fromkeys(corpus, 0)
    nextpage = random.choice(list(corpus.keys()))
    pagerank[nextpage] += 1
    for i in range(n - 1):
        pro_distri = transition_model(corpus, nextpage, damping_factor)
        x = random.uniform(0, 1)
        cumu_p = 0
        for page, p in pro_distri.items():
            cumu_p += p
            if cumu_p > x:
                break
        nextpage = page
        pagerank[nextpage] += 1
    for page in pagerank.keys():
        pagerank[page] /= n
    
    print(f"sample check : {sum(pagerank.values())}")
    return pagerank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    N = len(corpus)
    pagerank = dict.fromkeys(corpus.keys(), 1/N)
    numlinks = {p:len(corpus[p]) for p in corpus.keys()}

    flag = True
    while flag:
        flag = False
        newrank = {}
        for p in pagerank.keys():
            x = sum([pagerank[i] / numlinks[i] for i in pagerank.keys() if p in corpus[i] and numlinks[i] > 0])
            newrank[p] = (1 - damping_factor) / N + damping_factor * x
            if abs(newrank[p] - pagerank[p]) > 1e-3:
                flag = True
        for p in pagerank.keys():
            pagerank[p] = newrank[p]
    print(f"iterate check : {sum(pagerank.values())}")
    return pagerank


if __name__ == "__main__":
    main()
