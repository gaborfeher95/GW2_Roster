import MembersList
import csv  # for .csv handling


# class for table creation
class CreateCSV:
    def __init__(self):
        self.membersList = MembersList.MembersList()  # instantiate lists
        self.membersList.members.sort(key=lambda e: e.dateJoined, reverse=True)  # sort by date joined descending

    # create .csv listing only the members who need to be promoted based on time spent in guild
    def listPromotable(self):
        with open('members_list.csv', 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',')
            for member in self.membersList.members:
                cells = [member.name, member.rank, str(member.dateJoined)]
                if member.flag:
                    csv_writer.writerow(cells)


# create files with CreateCSV methods under this
if __name__ == '__main__':
    createCSV = CreateCSV()
    createCSV.listPromotable()
