
import argparse as ap
import networkx as nx
import matplotlib.pyplot as plt
import steam

import SteamUsr

parser = ap.ArgumentParser()
parser.add_argument("rootUser", metavar="R", type=str)

args = parser.parse_args()

print(args.rootUser)

f_graph = nx.Graph()

f = open("key.txt", "r")
key = f.read()
f.close()

api = steam.WebAPI(key)

steamID = api.ISteamUser.ResolveVanityURL(
    vanityurl=str(args.rootUser))["response"]["steamid"]

print(steamID)

root = SteamUsr.SteamUsr(steam_id=steamID, name=str(args.rootUser))
root.populateFriendsList(api)

for friend in root.friends:
    friend.populateFriendsList(api)


SteamUsr.applyNamesToSteamUsrs(api, root)

# TODO: Convert all steamapi library usage to steam offial API
# NOTE: 'ResolveVanityURL will get you a steamID from a username'


def addEdges(itr):
    if len(itr.friends) != 0:
        for friend in itr.friends:
            f_graph.add_edge(itr.steam_id, friend.steam_id)
            addEdges(friend)


addEdges(root)

# # Build the graph
nx.draw(f_graph)

# Create name labels from steamIDs in the graph
labels = {}

for node in f_graph.nodes:
    for usr in root.friends:
        if usr.steam_id == node:
            labels[node] = usr.name

nx.draw_networkx_labels(f_graph, nx.spring_layout(f_graph),
                        labels, font_size=16)

plt.show()
