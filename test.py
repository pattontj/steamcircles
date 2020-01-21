import argparse as ap
import steam
import networkx as nx
import matplotlib.pyplot as plt

import SteamUsr

# TODO: Move relevant code to a helper library

# TODO: check if steamID
parser = ap.ArgumentParser()
parser.add_argument("rootUser", metavar="R", type=str)
parser.add_argument("friend", metavar="F", type=str)
args = parser.parse_args()

f = open("key.txt", "r")
key = f.read()
f.close()

api = steam.WebAPI(key)

f_graph = nx.Graph()

# Handle vanity URLs AND steamID
steamID = args.rootUser
try:
    steamID = int(args.rootUser)
except Exception:
    steamID = api.ISteamUser.ResolveVanityURL(
        vanityurl=args.rootUser)["response"]["steamid"]

otherID = args.friend
try:
    otherID = int(args.friend)
except Exception:
    otherID = api.ISteamUser.ResolveVanityURL(
        vanityurl=args.friend)["response"]["steamid"]

# Create class intance of each user
root = SteamUsr.SteamUsr(steam_id=steamID, name=args.rootUser)
other = SteamUsr.SteamUsr(steam_id=otherID, name=args.friend)

# Build friends list one deep
root.populateFriendsList(api)
other.populateFriendsList(api)
# Recursively apply names to users
SteamUsr.applyNamesToSteamUsrs(api, root)
SteamUsr.applyNamesToSteamUsrs(api, other)

# DEBUG
print(len(root.friends))
print(len(other.friends))

# Build the undirected graph
for friend in root.friends:
    f_graph.add_edge(root.steam_id, friend.steam_id)

for friend in other.friends:
    f_graph.add_edge(other.steam_id, friend.steam_id)

# Creates layout of the graph
pos = nx.spring_layout(f_graph)

nx.draw_networkx_nodes(f_graph, pos)
nx.draw_networkx_edges(f_graph, pos)

# Create name labels from steamIDs in the graph
labels = {}

for node in f_graph.nodes:
    for usr in root.friends:
        if usr.steam_id == node:
            labels[node] = usr.name

nx.draw_networkx_labels(f_graph, pos,
                        labels, font_size=16)

# plt.axis("off")
plt.show()
