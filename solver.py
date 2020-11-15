#bo is a grid - 9x9 board game with numbers 1-9
import copy
from tests import *

#const
BOX1=(range(0,3),range(0,3))
BOX2=(range(0,3),range(3,6))
BOX3=(range(0,3),range(6,9))
BOX4=(range(3,6),range(0,3))
BOX5=(range(3,6),range(3,6))
BOX6=(range(3,6),range(6,9))
BOX7=(range(6,9),range(0,3))
BOX8=(range(6,9),range(3,6))
BOX9=(range(6,9),range(6,9))

boxes_arr=[BOX1,BOX2,BOX3,BOX4,BOX5,BOX6,BOX7,BOX8,BOX9]

######## HELP FUNCTIONS ########

def check_not_row(bo,pos,num): #pos is tuple (x,y)
    # input pos , board , number and check if num in row, return True if in the row and False if not
    for i in range(9):
        if bo[pos[0]][i] == num and pos[1] != i:
            return True
    else:
        return False

def check_not_col(bo,pos,num): #pos is tuple (x,y)
    # input pos , board , number and check if num in col, return True if in the col and False if not
    for i in range(9):
        if bo[i][pos[1]] == num and pos[0] != i:
            return True
    else:
        return False



def check_not_box(bo,pos,num): #pos is tuple (x,y)
    # input pos , board , number and check if num in box, return True if in the box and False if not
    box=find_box_from_pos(pos)
    num = find_num_in_box(bo,num,box)
    if num==0:
        return False
    else:
        return True


def find_num_in_box(bo, num, box):
    #return num pos if num in the box, 0 else
    for x in box[0]:
        for y in box[1]:
            temp=bo[x][y]
            if temp==num:
                return (x,y)
    return 0

def find_box_from_pos(pos):
    #fins in which box the pos in
    if pos[0] in BOX1[0]:
        if pos[1] in BOX1[1]:
            return BOX1
        if pos[1] in BOX2[1]:
            return BOX2
        if pos[1] in BOX3[1]:
            return BOX3
    elif pos[0] in BOX4[0]:
        if pos[1] in BOX4[1]:
            return BOX4
        if pos[1] in BOX5[1]:
            return BOX5
        if pos[1] in BOX6[1]:
            return BOX6
    else:
        if pos[1] in BOX7[1]:
            return BOX7
        if pos[1] in BOX8[1]:
            return BOX8
        if pos[1] in BOX9[1]:
            return BOX9

def empty_cell(bo):
    for x in range(9):
        for y in range(9):
            if bo[x][y] == 0:
                return (x,y)

    return None

def print_bo(bo):
    for row in bo:
        print (row)

def solved(bo):
    for x in bo:
        for y in x:
            if y==0:
                return False
    return True

def is_changed(bo1,bo2):
    for x1,x2 in zip(bo1,bo2):
        for y1,y2 in zip(x1,x2):
            if y1!=y2:
                return True
    return False


### Algorithms ###
def numbers(bo):
    # passing on all the numbers in the boxes starts from 1.
    pos_arr=[0]*9
    for x in range(1,10): #1-9 for num
        for y in range(9): #0-8 for box num
            pos_arr[y]=find_num_in_box(bo,x,boxes_arr[y])
        row_arr = [*range(9)]
        col_arr = [*range(9)]
        #remove row,col of pos from both arrays.
        for pos in pos_arr:
            if pos!=0:
                if pos[0] in row_arr:
                    row_arr.remove(pos[0])
                if pos[1] in col_arr:
                    col_arr.remove(pos[1])
        #checking from rows and cols arrays if they are in the box range
        for i,pos in enumerate(pos_arr):
            if pos ==0: #box= index+1
                boxnum=boxes_arr[i]
                row_option=[row for row in row_arr if row in boxnum[0]]
                col_option= [col for col in col_arr if col in boxnum[1]]
                if len(row_option)==1 and len(col_option)==1:
                    #if there is only one option for both row and col then this is the only position you can put the number
                    bo[row_option[0]][col_option[0]]=x
                    print_update(x,(row_option[0],col_option[0]))
    return bo

def numbers_in_rows(bo):
    for row in range(9): #9 rows
        num_arr=[*range(1,10)] #nums 1-9
        pos_arr=[]
        for col in range(9): #9 cols
            if bo[row][col]==0:
                pos_arr.append((row,col)) #positions that are empty in this row
            elif bo[row][col] in num_arr:
                num_arr.remove(bo[row][col]) #remove from the nums that are missing in this row
        for num in num_arr: #passing on nums in the missing nums in rows
            pos_ans=[]
            c=0
            for pos in pos_arr: #checking for each pose
                #checkbox and col
                if check_not_box(bo,pos,num)==False and check_not_col(bo, pos, num)==False and check_not_row(bo,pos,num)==False:
                    pos_ans.append(pos)
                    c=c+1
                    if c>1:
                        break
            if c==1:
                bo[pos_ans[0][0]][pos_ans[0][1]]=num
                print_update(num,pos_ans[0])
                pos_arr.remove(pos_ans[0])
            else: #checking the negative way
                for pos1 in pos_arr:
                    neg_ans = True
                    for num1 in num_arr:
                        if num1 != num:
                            if check_not_box(bo, pos1, num1) == False and check_not_col(bo, pos1, num1) == False:
                                neg_ans=False
                                break
                    if neg_ans==True:
                        bo[pos1[0]][pos1[1]]=num
                        print_update(num, pos1)
                        pos_arr.remove(pos1)


    return bo

def numbers_in_cols(bo):
    for col in range(9):
        num_arr=[*range(1,10)]
        pos_arr=[]
        for row in range(9):
            if bo[row][col]==0:
                pos_arr.append((row,col))
            elif bo[row][col] in num_arr:
                num_arr.remove(bo[row][col])
        for num in num_arr:
            pos_ans=[]
            neg_ans = True
            for pos in pos_arr:
                #checkbox and row
                if check_not_box(bo,pos,num)==False and check_not_col(bo, pos, num)==False and check_not_row(bo,pos,num)==False:
                        pos_ans.append(pos)
            if len(pos_ans)==1:
                bo[pos_ans[0][0]][pos_ans[0][1]]=num
                print_update(num, pos_ans[0])
                pos_arr.remove(pos_ans[0])
            else:  # the negative way..
                for pos1 in pos_arr:
                    neg_ans = True
                    for num1 in num_arr:
                        if num1 != num:
                            if check_not_box(bo, pos1, num1) == False and check_not_row(bo, pos1, num1) == False:
                                neg_ans = False
                                break
                    if neg_ans == True:
                        bo[pos1[0]][pos1[1]] = num
                        pos_arr.remove(pos1)
                        print_update(num, pos1)

    return bo

def numbers_in_box(bo):
    for box in boxes_arr:
        num_arr = [*range(1, 10)]
        pos_arr = []
        for row in box[0]:
            for col in box[1]:
                if bo[row][col] == 0:
                    pos_arr.append((row, col))
                elif bo[row][col] in num_arr:
                    num_arr.remove(bo[row][col])
        for num in num_arr:
            pos_ans = []
            neg_ans = True
            for pos in pos_arr:
            # check col and row
                if check_not_box(bo,pos,num)==False and check_not_col(bo, pos, num)==False and check_not_row(bo,pos,num)==False:
                    pos_ans.append(pos)
            if len(pos_ans) == 1:
                bo[pos_ans[0][0]][pos_ans[0][1]]=num
                pos_arr.remove(pos_ans[0])
                print_update(num, pos_ans[0])

            else:  # the negative way..
                for pos in pos_arr:
                    neg_ans = True
                    for num1 in num_arr:
                        if num1 != num:
                            if check_not_row(bo, pos, num1) == False and check_not_col(bo, pos, num1) == False:
                                neg_ans = False
                                break
                    if neg_ans == True:
                        bo[pos[0]][pos[1]] = num
                        pos_arr.remove(pos)
                        print_update(num, pos)

    return bo


def backtracking(bo):
    empty_pos=empty_cell(bo)
    if empty_pos==None:
        return bo
    else:
        for num in range(1,10):
            if check_not_box(bo, empty_pos, num) == False and check_not_col(bo, empty_pos, num) == False and check_not_row(bo, empty_pos, num) == False:
                bo[empty_pos[0]][empty_pos[1]]=num
                if backtracking(bo):
                    print_update(num,empty_pos)
                    return bo
                bo[empty_pos[0]][empty_pos[1]] = 0
    return False


#all together..
def play(bo):
    c=0
    wcount=0
    bo1,bo2=None,None
    print ("original board:")
    print_bo(bo)
    print ("stages:")
    while solved(bo)==False:
        bo1=copy.deepcopy(bo)
        print("numbers " + str(c))
        bo = numbers(bo)
        print_bo(bo)
        print("rows "+str(c))
        bo = numbers_in_rows(bo)
        print_bo(bo)
        print("cols "+str(c))
        bo = numbers_in_cols(bo)
        print_bo(bo)
        print("box "+str(c))
        bo = numbers_in_box(bo)
        print_bo(bo)
        c=c+1
        print("\n")
        bo2=copy.deepcopy(bo)
        if (is_changed(bo1,bo2))==False:
            wcount+=1
        if wcount==2:
            print("backtracking")
            bo=backtracking(bo)

        # print_bo(bo)
    if solved(bo)==True:
        print('Final board')
        print_bo(bo)
        print ("number of rounds without backtracking "+str(c))

def print_update(num,pos):
    print("["+str(pos[0])+"] ["+str(pos[1])+"] = "+str(num))



if __name__ == "__main__":
    num=input("enter number between 1-14:")
    play(boards["board"+num])










