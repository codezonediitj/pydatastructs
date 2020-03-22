def deep_walk(G, window_size, embed_size, walks, walk_length):
	    for i in range(walks):
	    	O = shuffle(G.vertices)
	    	for v in O:
	    		W = random_walk(G, v, walks)
	    		SkipGram(T, W, window_size)

#G is an AdjacencyList
def random_walk(G, path_length, rand=random.Random(), start=None):
    """ Returns a truncated random walk.

        path_length: Length of the random walk.
        start: the start node of the random walk.
    """
    if start:
      path = [start]
    else:
      # Sampling is uniform w.r.t V, and not w.r.t E
      path = [rand.choice(list(G.vertices()))]

    while len(path) < path_length:
      cur = path[-1]
      if len(G[cur]) > 0:
          path.append(rand.choice(G[cur]))
      else:
      	  break
    return [str(node) for node in path]

#Accoring to the paper it is not necessary to have Random Walk with Restarts in DeepWalk.