import os
import random
import re
import sys

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
    transition = {}
    if corpus[page] == None:
        size = len(corpus.keys())
        for i in corpus.keys():
            transition[i] = 1 / size
    else:
        size = len(corpus.keys())
        for i in corpus.keys():
            transition[i] = (1 - damping_factor) / size
        size = len(corpus[page])
        for i in corpus[page]:
            transition[i] += damping_factor / size

    return transition


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    output = {}
    choice = random.choice(list(corpus.keys()))
    output[choice] = 1
    for _ in range(n - 1):
        transition = transition_model(corpus,choice,damping_factor)
        choice = random.choices(list(transition.keys()), weights = list(transition.values()))
        choice = choice[0]
        if choice not in output.keys():
            output[choice] = 1
        else:
            output[choice] += 1
    for i in output.keys():
        output[i] /= n
    return output


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pagerank = {}
    N = len(corpus.keys())
    for i in corpus.keys():
        pagerank[i] = 1 / N

    while True:
        count = 0
        for key in corpus:
            new = (1 - damping_factor) / N
            k = 0
            for page in corpus:
                if key in corpus[page]:
                    numlinks = len(corpus[page])
                    k += pagerank[page] / numlinks
            k *= damping_factor
            new += k
            if abs(new - pagerank[key]) < 0.001:
                count += 1
            pagerank[key] = new
        if count == N:
            break
    return pagerank


if __name__ == "__main__":
    main()
