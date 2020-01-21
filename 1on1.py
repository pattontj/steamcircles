import argparse as ap
import steam
import networkx as nx
import matplotlib.pyplot as plt

import SteamUsr


# SUMMARY: 1on1 builds a single deep network of both
#          users friends lists, which displays the
#          mutual friends of each user

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
root.populateFriendsList(api, 1)
other.populateFriendsList(api, 1)
# Recursively apply names to users
SteamUsr.applyNamesToSteamUsrs(api, root)
SteamUsr.applyNamesToSteamUsrs(api, other)

# DEBUG
print(len(root.friends))
print(len(other.friends))


def addEdges(itr):
    if len(itr.friends) != 0:
        for friend in itr.friends:
            f_graph.add_edge(itr.steam_id, friend.steam_id)
            addEdges(friend)


addEdges(root)
addEdges(other)

# # Build the undirected graph
# for friend in root.friends:
#     f_graph.add_edge(root.steam_id, friend.steam_id)

# for friend in other.friends:
#     f_graph.add_edge(other.steam_id, friend.steam_id)

# Creates layout of the graph
#pos = nx.spring_layout(f_graph)
pos = nx.kamada_kawai_layout(f_graph, center=None, dim=2)

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
