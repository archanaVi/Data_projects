## Import modules and libraries
#numpy to work with an array (3x3 matrix) as the grid :
import numpy as np
#regex
import re

#----------------------------------------------------------------------------------------------------------------------

##initial global variables

total_boxes=[(i,j) for i in range(3) for j in range(3)] #contains all the available positions at the beginning of the game

empty_boxes = total_boxes.copy() #make a copy that will be updated after each player's move

#game_on_going=True # I comment this variable because it will be initiated when we ask the player if he wants to play

turn=True #variable that will enable to switch turns (=alternate between the two players)

grid=np.array([["-","-","-"],["-","-","-"],["-","-","-"]]) #the empty grid at the beginning of the game

grid_numbers=np.array([["1","2","3"],["4","5","6"],["7","8","9"]]) #the grid that will show the player(s) how the number he is asked to give refers to a position in the grid

#creates a 3x3 matrix that contains 0 where grid contains '-', 1 where grid contains 'O' and 3 where grid contains 'X'
# the purpose is to detect if a row, column or diagonal has 1 available position and 2 filled by the same player : the sum will be 2 only if the 2 filled are 'O' and 6 only if the 2 filled are 'X' 
scores=np.zeros((3,3)) #array scores filled with zeros


##functions

def welcome():
    """
    This function welcomes the player and introduces the rules of the game.
    """
    print('Welcome to our Tic Tac Toe game!')
    print('Here are the numbers corresponding to the grid:')
    print_grid(grid_numbers)
    
def want_to_play():
    """
    This function asks only 5 times if if you wish to play.
    If no correct answer is given then it exits the game to avoid an infinite loop.
    """
    global game_on_going
    global computer_play
    for i in range(5):
        play=input('Do you want to play ? y/n\n')
        if play=='y':
            game_on_going=True
            what_level()
            break
        elif play=='n' or i==4:
            game_on_going=False
            print('Ok. Maybe next time.\n')
            break

def what_level():
    """
    This function ask the level we want to play.
    """
    global computer_play
    while True:
        level=input("Choose Computer's level: easy=0 , hard=1:\n")
        if re.fullmatch('[0-1]',level) :
            level=int(level)
            break 
    if level:
        computer_play=computer_play_hard #if the player choses 1 (equivalent of True), the function called for computer's play will be the easy one (random)
    else:
        computer_play=computer_play_easy #if the player choses 0, the function called for computer's play will be the easy one (random)computer_play=computer_play_hard #if the player choses 1, the function called for computer's play will be the hard one (not random)

def print_grid(array):
    """
    This function prints the grid of the game.
    """
    for i in range(3):
        print('|', end = '')
        for j in range(3):
            print(array[i][j], end='|')
        print('\n')
    print('_'*50)
    print('\n')
    

def computer_play_easy():
    """
    This function plays the "dumb" computer.
    """
    global empty_boxes
    global grid
    import random
    position=random.choice(empty_boxes) # the position is chosen randomly between the available positions
    grid[position[0]][position[1]]="X"  #fills the grid with an X
    empty_boxes.remove(position)  #updates empty_boxes

def computer_play_hard():
    """
    This function plays the "smart" computer.
    """
    global empty_boxes
    global grid
    global scores
    import random
                    
    #we generate a list that contains for the matrix scores, in this order, the sum of :
        #1st row
        #2nd row
        #3rd row
        #1st column
        #2nd column
        #3rd column
        #1st diagonal (trace of matrix)
        #2nd diagonal (trace of flipped matrix = column 0 and 2 inverted)
    lst=np.sum(scores,axis=1,dtype = int).tolist()+np.sum(scores,axis=0, dtype = int).tolist()+[np.trace(scores,dtype = int).tolist(),np.trace(np.flip(scores, axis=1),dtype = int).tolist()]
    #print(lst)
                    
# now we test first if the computer has filled 2 out of 3 in a line (sum=6) and if so chose to play the third position to win the game 
# if not, we test if the opponent filled 2 out of 3 in a line (sum=2) and if so chose to play the third position on that line to prevent the opponent from winning

    if 2 in lst or 6 in lst:
        for i in [6,2]: #I switched 2 and 6 so that the computer tries first to win and then tries to block its opponent
            if i in lst:
                if lst.index(i)==0:
                    y=scores[0].tolist().index(0)
                    grid[0][y]='X'
                    scores[0][y]=3
                    position=(0,y)
                    break
                elif lst.index(i)==1:
                    y=scores[1].tolist().index(0)
                    grid[1][y]='X'
                    scores[1][y]=3
                    position=(1,y)
                    break
                elif lst.index(i)==2:
                    y=scores[2].tolist().index(0)
                    grid[2][y]='X'
                    scores[2][y]=3
                    position=(2,y)
                    break
                elif lst.index(i)==3:
                    y=scores[:,0].tolist().index(0)
                    grid[y][0]='X'
                    scores[y][0]=3
                    position=(y,0)
                    break
                elif lst.index(i)==4:
                    y=scores[:,1].tolist().index(0)
                    grid[y][1]='X'
                    scores[y][1]=3
                    position=(y,1)
                    break
                elif lst.index(i)==5:
                    y=scores[:,2].tolist().index(0)
                    grid[y][2]='X'
                    scores[y][2]=3
                    position=(y,2)
                    break
                elif lst.index(i)==6:
                    y=np.diag(scores).tolist().index(0)
                    grid[y][y]='X'
                    scores[y][y]=3
                    position=(y,y)
                    break
                elif lst.index(i)==7:
                    y=np.diag(np.flip(scores, axis=1)).tolist().index(0)
                    grid[y][2-y]='X'
                    scores[y][2-y]=3
                    position=(y,2-y)
                    break
    #if neither condition is met, the computer plays randomly
    else:
        position=random.choice(empty_boxes) # the position is chosen randomly between the available positions
        grid[position[0]][position[1]]="X"  #fills the grid with an X
        scores[position[0]][position[1]]=3
    empty_boxes.remove(position)  #updates empty_boxes
    

def human_play():
    """
    This function makes a human player play.
    """
    import re
    global total_boxes
    global empty_boxes
    while True:
        coord=input('Choose a number between 1 and 9:  ') #ask which position he choses
        if re.fullmatch('[1-9]',coord) :                  #verifies that the input is actually a number to avoid TypeError when converting to integer
            coord_int=int(coord)
            i=coord_int-1
            position=total_boxes[i]                      #converts it to the tuple containing the row and column numbers of the array
            if position not in empty_boxes:              # verifies if the chosen position is available
                print('Sorry, this box is not available')
            else:
                break
        else :print("You need to give a number between 1 and 9:  ")
    grid[position[0]][position[1]]="O"                    # fills the grid with an O
    scores[position[0]][position[1]]=1                    #updates scores
    empty_boxes.remove(position)                          #updates empty_boxes
    
                    
def detect_winner(grid=grid): 
    """
    This function detects if one of the players has won the game.
    """
    # the variable grid is passed in the argument of the function so that it will be used in the function but not modified by the function (avoid accidental modifiaction of the grid in the function)
    #global variables that will be modified in the function. The modified value will be used by the main program after exiting the function
    global empty_boxes
    global turn
    global game_on_going
    #booleans checking if one row, column or diagonal is filled with the same symbol (X or O but not empty)
    row1=grid[0][0]==grid[0][1]==grid[0][2]!="-"  
    row2=grid[1][0]==grid[1][1]==grid[1][2]!="-" 
    row3=grid[2][0]==grid[2][1]==grid[2][2]!="-" 
    column1=grid[0][0]==grid[1][0]==grid[2][0]!="-" 
    column2=grid[0][1]==grid[1][1]==grid[2][1]!="-" 
    column3=grid[0][2]==grid[1][2]==grid[2][2]!="-" 
    diag1=grid[0][0]==grid[1][1]==grid[2][2]!="-" 
    diag2=grid[2][0]==grid[1][1]==grid[0][2]!="-"
    #if one line is filled : one of the players has won
    if row1 or row2 or row3 or column1 or column2 or column3 or diag1 or diag2:
        print('we have a winner!')
        game_on_going=False # to stop the game
        # then determine who is the winner by printing one element of the filled line (this prevents to code to check twice if a line is filled : once for 3 positions are = to "X" and a second time for 3 positions = to "O" )
        if row1 or column1 or diag1: #we gathered lines with one element in common to shorten the code
            print('the winner is:', grid[0][0])
        elif row2 or column2:
            print('the winner is:', grid[1][1])
        elif row3 or diag2:
            print('the winner is:', grid[2][0])
        elif column3:
            print('the winner is:', grid[0][2])
        return True
    else: return False
                    
#-------------------------------------------------------------------------------------------------------------------------

#introduction to the game
welcome()

#ask if player wants to play
want_to_play()
    
# actual game: 
while game_on_going:

    #calls the play function depending on whose turn it is
    if turn==True:
        computer_play()
    else :
        human_play()
        
    #after each player's play, we print the grid to show what position has been filled
    print_grid(grid)
    #then check if there is a winner
    if detect_winner():
        pass
        #verify if there is a tie
    else:
        if not empty_boxes: # the same as empty_boxes==[] : an empty list is the same as false
             print('game over! no winner!')
             game_on_going=False
    #if the game is still going, we switch turn :
        else:
            turn=not turn




