
import argparse as ap
import networkx as nx
import matplotlib.pyplot as plt
import steam

import SteamUsr

parser = ap.ArgumentParser()
# name or steamID of root user
parser.add_argument("rootUser", metavar="R", type=str)
# how deep should the graph expand
parser.add_argument("depth", metavar="D", type=int)
args = parser.parse_args()

print(args.rootUser)

f_graph = nx.Graph()

f = open("key.txt", "r")
key = f.read()
f.close()

api = steam.WebAPI(key)

# Handle vanity URLs AND steamID
steamID = args.rootUser
try:
    steamID = int(args.rootUser)
except Exception:
    steamID = api.ISteamUser.ResolveVanityURL(
        vanityurl=str(args.rootUser))["response"]["steamid"]

print(steamID)

root = SteamUsr.SteamUsr(steam_id=steamID, name=str(args.rootUser))

root.populateFriendsList(api, args.depth)

SteamUsr.applyNamesToSteamUsrs(api, root)


def addEdges(itr):
    if len(itr.friends) != 0:
        for friend in itr.friends:
            f_graph.add_edge(itr.steam_id, friend.steam_id)
            addEdges(friend)


addEdges(root)

pos = nx.kamada_kawai_layout(f_graph, center=None, dim=2)
# pos = nx.spectral_layout(f_graph, weight=None)

nx.draw_networkx_nodes(f_graph, pos)
nx.draw_networkx_edges(f_graph, pos)

# # Build the graph
# nx.draw(f_graph)

# Create name labels from steamIDs in the graph
labels = {}

for node in f_graph.nodes:
    for usr in root.friends:
        if usr.steam_id == node:
            labels[node] = usr.name


nx.draw_networkx_labels(f_graph, pos,
                        labels, font_size=14)

plt.show()
