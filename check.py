#check.py
#Check the validity of a pick
def checkPick(wk, mon):
    
    if str(wk.get_worksheet(6).find(mon)) == 'None':
        poss = False
    else:
        print(wk.get_worksheet(6).find(mon))
        poss = True
    if str(wk.get_worksheet(8).find(mon)) == 'None':
        avl = True
    else:
        print(wk.get_worksheet(8).find(mon))
        avl = False
    return (avl and poss)
        
