import configparser  # for config.ini handling
import requests  # for API requests
import datetime  # for handling explicit dates
from dateutil.relativedelta import relativedelta  # needed for calculating months


# format of guild ranks: rank name (str), months needed to advance (int)
class RankThreshold:
    def __init__(self, name, months):
        self.name = name
        self.threshold = months


# format of guild members:
# account name (str, name.1234), rank (str, same as in RankThreshold)
# date joined (datetime object with year, month, day values)
# months (months needed after joining for specific member)
# flag (boolean, stores whether or not user needs to be promoted)
class Member:
    def __init__(self, name, rank, joined):
        self.name = name
        self.rank = rank
        self.dateJoined = joined
        self.flag = False
        self.months = 0

    # checks list of rank thresholds against rank of user to determine months
    def findThreshold(self, ranks):
        for e in ranks:
            if e.name == self.rank:
                return e.threshold

    # checks whether or not user needs to be promoted based on time passed since joining
    def checkFlag(self):
        try:
            if datetime.date.today() > self.dateJoined + relativedelta(months=self.months):
                self.flag = True
        except TypeError:
            self.flag = False  # make sure there are no flags for officers and veterans


# main class, contains rank thresholds, the entire members list
class MembersList:
    def __init__(self):
        self.ranks = []
        self.members = []
        # read config file for IDs and ranks
        self.config = configparser.ConfigParser()
        self.config.optionxform = str
        with open('config.ini', 'r') as cfg:
            self.config.read_file(cfg)
        # fill ranks and members lists
        self.jsonData = self.getJSONData()
        self.getRanks()
        self.getMembersList()

    # fetch full members list from GW2 server
    def getJSONData(self):
        # keys taken from config file
        guildID = self.config['GuildKeys']['GuildID']
        leaderAPIKey = self.config['GuildKeys']['LeaderKey']
        # API request URL
        r = requests.get('https://api.guildwars2.com/v2/guild/' + guildID + '/members?access_token=' + leaderAPIKey)
        return r.json()

    # fetch rank properties from config file
    def getRanks(self):
        for key in self.config['Ranks']:
            rnk = RankThreshold(key, int(self.config['Ranks'][key]))
            self.ranks.append(rnk)

    # fill list of members in this object, complete with properties not taken directly from the server
    def getMembersList(self):
        for member in self.jsonData:
            # convert string date to datetime object
            joinedStr = member['joined']
            newJoined = datetime.date(int(joinedStr[:4]), int(joinedStr[5:7]), int(joinedStr[8:10]))
            # instantiate Member class with data of current member
            newMember = Member(member['name'], member['rank'], newJoined)
            # fill missing properties
            newMember.months = newMember.findThreshold(self.ranks)
            newMember.checkFlag()
            self.members.append(newMember)  # add to list


# if you want to test stuff directly, do it here
if __name__ == '__main__':
    membersList = MembersList()
    membersList.members.sort(key=lambda e: e.dateJoined, reverse=True)
    for member in membersList.members:
        print(member.name)
