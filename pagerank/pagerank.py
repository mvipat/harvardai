import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000
#SAMPLES = 200

def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    corpus = consider_no_link(corpus)
    print(f"modified corpus {corpus}")
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
    pages = dict()
    list_of_pages = corpus.get(page,list())

    print(f"Calculating {page}: {list_of_pages}")
    if len(list_of_pages) > 0:
        count = len(list_of_pages) + 1
        random_probability = (1-damping_factor)/count
        #print(f"Count:{count} random_probability: {random_probability}")
        pages[page] = random_probability
        for page_item in list_of_pages:
            pages[page_item] = (damping_factor/len(list_of_pages))+random_probability
    else :
        for each_page in corpus.keys():
            pages[each_page] = 1 / (len(corpus.keys()))
    
    return pages


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    page_ranks = dict()
    items_list = list(corpus.keys())
    random_page = random.choice(items_list)
    map_next_page_count = dict()
    for sample_index in range(1,SAMPLES):
        #print(f"Random Page {random_page}")
        transition_pages = transition_model(corpus, random_page, damping_factor)
        
        all_value_zero = True
        for page_name,probability in transition_pages.items():
            count_page = map_next_page_count.get(random_page+" "+page_name,0)
            if count_page is None:
                count_page = 0
            if count_page > 0:
                all_value_zero = False
                break

        closest_next = dict()
        for page_name,probability in transition_pages.items():
            #print(f"page_name {page_name}: probability {probability}")
            count_page = map_next_page_count.get(random_page+" "+page_name,0)
            if all_value_zero:
                count_page = int(probability * 100)

            if count_page > 0:
                map_next_page_count[random_page+" "+page_name] = count_page
                closest_next[page_name] = count_page

            current_probability = page_ranks.get(page_name)
            if current_probability is None:
                current_probability = 0
            page_ranks[page_name] = (current_probability+probability)

        sorted_items_by_value = sorted(closest_next.items(), key=lambda item: item[1], reverse=True)
        #print(f"closest_next {closest_next} sorted_items_by_value {sorted_items_by_value}")

        if all_value_zero:
            random_page = random.choice(items_list)
        else :    
            next_random_page = sorted_items_by_value[0][0]
            count_page = map_next_page_count.get(random_page+" "+next_random_page,0)
            if count_page <= 0:
                raise ValueError("Something Wrong")
            else :
                count_page -= 1
                map_next_page_count[random_page+" "+next_random_page] = count_page
                random_page = next_random_page

    for pages in page_ranks.copy():
        page_ranks[pages] = page_ranks[pages] / SAMPLES

    print(f"Transitional Model : Sum of Probability {sum_probability(page_ranks)}")

    return page_ranks

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    page_ranks = create_page_rank(corpus)
    items_list = list(corpus.keys())
    incoming_links = dict()
    for main_page in corpus.keys():
        links = corpus[main_page]
        #print(f"main_page {main_page} links {links}")
        for link in links:
            list_of_pages_for_link = incoming_links.get(link,set())
            #print(f"link {link} list_of_pages_for_link {list_of_pages_for_link}")
            
            list_of_pages_for_link.add(main_page)
            incoming_links[link] = list_of_pages_for_link

    print(f"incoming_links: {incoming_links}")

    random_page = random.choice(items_list)
    value_changed = True
    current_probability = dict()
    while value_changed:
        value_changed = False
        for random_page in corpus.keys():
            #print(f"Random Page {random_page}")

            probability = (1-damping_factor)/len(items_list)

            total_probability = 0
            incoming_links_pages = incoming_links.get(random_page,set())

            for link in incoming_links_pages:
                page_probability = page_ranks[link]
                number_of_links = len(corpus[link])
                #print(f"{link}: {page_probability} {number_of_links}")

                total_probability += page_probability/number_of_links

            calculated_probablity = probability + (damping_factor) * (total_probability)
            current_probability[random_page] = calculated_probablity
        
        updates_required = False
        for check_page in corpus.keys():
            if abs(page_ranks[check_page] - current_probability[check_page]) > 0.001:
                updates_required = True

        if updates_required:
            for check_page in corpus.keys():
                page_ranks[check_page] = current_probability[check_page]
                value_changed = True

    print(f"Iterate Page Rank : Sum of Probability {sum_probability(page_ranks)}")

    return page_ranks

def sum_probability(page_ranks):
    """
    Return sum of probability in page_ranks dictionary.
    """
    sum_probability1 = 0
    for pages in page_ranks.copy():
        sum_probability1 += page_ranks[pages]

    return sum_probability1

def create_page_rank(corpus):
    """
    Initializes a page_ranks dictionary with a intial value of zero for each page.
    """

    page_ranks = dict()
    for page_name in corpus.keys():
        page_ranks[page_name] = 1/(len(corpus.keys()))

    return page_ranks


def consider_no_link(corpus):
    """
    Modifies corpus to add each page as link if the page has no links
    """

    new_corpus = dict()
    for page_name in corpus.keys():
        list_of_pages = corpus.get(page_name,set())
        if len(list_of_pages) == 0:
           list_of_pages = set(corpus.keys())
        
        new_corpus[page_name] = list_of_pages

    return new_corpus
if __name__ == "__main__":
    main()
