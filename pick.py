#pick.py
#Given the coach, make a pick and update the roster sheet
def makePicks(coach, roster, pickNum, pkmn):
        teamCell = roster.find(coach)
        myRow = (teamCell.row +3 + pickNum)
        myCol = teamCell.col
        #find the appropriate team using their name and move to proper cell
        roster.update_cell(myRow, myCol, pkmn)

