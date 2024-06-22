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
    output = dict()
    in_page = corpus[page]
    len_page = len(in_page)
    number_of_pages = len(corpus)
    equal_prob_all_pages = (1-damping_factor)/number_of_pages
    for key_corpus in corpus:
        output[key_corpus] = equal_prob_all_pages
    for key in in_page:
        output[key] += damping_factor/len_page
    return output


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    output = dict()
    
    for key_corpus in corpus.keys():
        output[key_corpus] = 0.0
    
    next_page = random.choice(list(corpus.keys()))
    output[next_page] += 1 / n
    # print(next_page)
    for _ in range(n):

        page_transition_model = transition_model(corpus, next_page, damping_factor)

        next_page = random.choices(list(page_transition_model.keys()),  weights=list(page_transition_model.values()))[0]

        output[next_page] += 1 / n
    output_sum = sum(output.values())
    # Making Sure it adds up to one
    for key in output.keys():
            output[key] /= output_sum
    # print(sum(output.values()))
    return output


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    ACCURACY = 0.001

    def PR(page, corpus, PageRanks):
        result = 0
        for key in corpus:
            if page in corpus[key]:
                result += PageRanks[key]/len(corpus[key])
        return result
    
    PageRanks = dict()
    
    for key_corpus in corpus.keys():
        PageRanks[key_corpus] = 1/len(corpus)

    keep_going = True
    
    while keep_going:
        
        keep_going = False
        
        for key_corpus in corpus.keys():
            
            prev = PageRanks[key_corpus]
            
            PageRanks[key_corpus] = (1-damping_factor)/len(corpus) + damping_factor * PR(key_corpus, corpus, PageRanks)
            
            if abs(prev - PageRanks[key_corpus]) > ACCURACY:
                keep_going = True
    PageRanks_sum = sum(PageRanks.values())
    
    # Making Sure it adds up to one
    for key in PageRanks.keys():
        PageRanks[key] /= PageRanks_sum
    # print(sum(PageRanks.values()))
    return PageRanks

if __name__ == "__main__":
    main()
