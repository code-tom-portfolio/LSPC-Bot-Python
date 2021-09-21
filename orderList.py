#orderList.py
#Taking the list of the seeded round 1 pick and the discord member list, get the list in the right order
def orderList(list1, list2):
    sortedList = []
    #index = 0
    for coach in list1:
        #print('Coach: {}'.format(coach))
        for member in list2:
            tempStr = member.name
            #print('Name: {}'.format(tempStr))
            if tempStr == coach.strip():
                #print('Found a match! {} and {}'.format(coach, tempStr))
                sortedList.append(member)
                #print('List: {}'.format(sortedList))
            #else:
                #print('{} is not {}'.format(coach, tempStr))
    return sortedList
                
