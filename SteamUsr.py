import steam as api


class SteamUsr:
    def __init__(self, steam_id, name=None, profile_url=None):
        # holds a 64 len steam ID
        self.steam_id = steam_id
        # holds the webAPI "personaname"
        # if not name:
        #    self.name = api.ISteamUser.GetPlayerSummaries(
        #        steamids=self.steam_id
        #        )["response"]["players"][0]["personaname"]
        # else:
        self.name = name
        self.profile_url = profile_url
        self.friends = []
        # friends_api = api.ISteamUser.GetFriendList(
         #   steamid=steam_id,
         #   relationship="friend",
         #   format="json")

        # for friend in friends_api["friendslist"]["friends"]:
        #    self.friends.append(friend["steamid"])

    def populateFriendsList(self, api):
        friendsList = None
        try:
            friendsList = api.ISteamUser.GetFriendList(
                steamid=self.steam_id, relationship="friend", format="json")
        except Exception:
            pass

        if friendsList:
            for friend in friendsList["friendslist"]["friends"]:
                # print(friend["steamid"])
                self.friends.append(SteamUsr(steam_id=friend["steamid"]))


# Apply names to usrs, submits requests in batches of 20
def applyNamesToSteamUsrs(api, itr):
    # print(itr.name)
    if len(itr.friends) != 0:
        ids = ""
        # loop all friends, collect id
        for friend in itr.friends:
            ids += friend.steam_id + ","
            # For every 20 users, submit req
            if itr.friends.index(friend) % 20 == 0:
                print("submitted request")
                ids = ids[0:-1]
                summaries = api.ISteamUser.GetPlayerSummaries(steamids=ids)
                ids = ""
                for player in summaries["response"]["players"]:
                    for friend in itr.friends:
                        if player["steamid"] == friend.steam_id:
                            friend.name = player["personaname"]
                            applyNamesToSteamUsrs(api, friend)

        ids = ids[0:-1]
        summaries = api.ISteamUser.GetPlayerSummaries(steamids=ids)
        for player in summaries["response"]["players"]:
            for friend in itr.friends:
                if player["steamid"] == friend.steam_id:
                    friend.name = player["personaname"]
                    applyNamesToSteamUsrs(api, friend)
