# Mosey
find interesting walks in London

# Requirements
- [osmnx](https://github.com/gboeing/osmnx)
- [networkx] (https://networkx.org/)
- numpy
- pandas
- plotly

# How it works
1. Define an area (North, East, South, West) via coordinates as your starting grid.
2. Create connected subgraph of all points in grid
3. Define origin and destination points in that grid
3. Generate the shortest path between the two points & plot
4. Use London Tree map to find the the number of trees near each node in the connected subgraph
5. Add that to the meta data of each node in the graph
6. Calculate new route which will minimize the (negative) tree score & plot that


