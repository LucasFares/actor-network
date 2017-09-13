import math
import networkx as nx
import matplotlib.pyplot as plot
import csv
import operator

movies = csv.DictReader(open('movie_metadata.csv', encoding='utf-8'), delimiter=',')
graph = nx.Graph()
sortedMovies = sorted(movies, key=lambda score: score['imdb_score'],reverse=True)

#creates network using highest rated movie actors share
for row in sortedMovies:
    graph.add_node(row['actor_1_name'])
    graph.add_node(row['actor_2_name'])
    graph.add_node(row['actor_3_name'])
    graph.add_edge(row['actor_1_name'], row['actor_2_name'], title=row['movie_title'], weight=float(row['imdb_score']))
    graph.add_edge(row['actor_1_name'], row['actor_3_name'], title=row['movie_title'], weight=float(row['imdb_score']))
    graph.add_edge(row['actor_2_name'], row['actor_3_name'], title=row['movie_title'], weight=float(row['imdb_score']))


#sorts on names so that distance equation lines up
deg = sorted(nx.degree_centrality(graph).items(), key=operator.itemgetter(0), reverse=True)
close = sorted(nx.closeness_centrality(graph).items(), key=operator.itemgetter(0), reverse=True)
bet = sorted(nx.betweenness_centrality(graph).items(), key=operator.itemgetter(0), reverse=True)
degMax = max(deg, key=operator.itemgetter(1))[1]
closeMax = max(close, key=operator.itemgetter(1))[1]
betMax = max(bet, key=operator.itemgetter(1))[1]

distance = []
for i in range(len(deg)):
    distance.append( (deg[i][0], math.sqrt((deg[i][1]/degMax)**2+(close[i][1]/closeMax)**2+(bet[i][1]/betMax)**2)) )

#The following prints out pretty results
nx.draw_networkx(graph, with_labels=False, edge_color='gray', node_color='black',node_size=100)
plot.show()
print("Degree: ", sorted(deg, key=operator.itemgetter(1), reverse=True)[:10])
print("Closeness: ", sorted(close, key=operator.itemgetter(1), reverse=True)[:10])
print("Betweenness: ", sorted(bet, key=operator.itemgetter(1), reverse=True)[:10])
print("Distance: ", sorted(distance,key=operator.itemgetter(1), reverse=True)[:10])
print('Eigenvector: ', sorted(nx.eigenvector_centrality(graph).items(), key=operator.itemgetter(1), reverse=True)[:10])
