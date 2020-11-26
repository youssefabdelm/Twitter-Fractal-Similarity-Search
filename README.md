# Twitter Fractal Similarity Search
Discover similar users through a fractal search with semantic similarity applied to twitter user bios

![Tree](https://github.com/youssefabdelm/Twitter-Fractal-Similarity-Search/blob/main/tree.png)

# Usage
1. `pip install -r requirements.txt`
2. Enter username
3. Enter similarity threshold (applicable when doing a second-degree traversal), this ignores users that have a bio that is less than X% similar (you specify, e.g. 0.7)
4. Enter degree of separation (only 1 and 2 available for now but eventually I want to make it keep going forever!)


# How does it work?
1. You pick a username
2. I get their bio, and extract a numerical representation of its meaning (embedding/vector) using a language model
3. I download who they are following, and I get each of their bios, and I do the same thing and measure how similar they are to the original user 
4. If it's second degree, and you've picked a high threshold, if the user is above a certain threshold of similarity, I download a list of users they're following, and do the same thing

