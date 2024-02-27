This program determines how many “degrees of separation” apart two actors are.
The path between two actors is a sequence of movies and actors that connects them.
The shortest path is found with BFS search.
 
Usage:
The file people.csv includes actors and their ids, movie.csv has all movies and their ids, and
stars.csv connects actors with the movies they have acted in. 

Start program with: python degrees.py small or python degrees.py large.
Then input two actors from small/people.csv or large/people.csv.