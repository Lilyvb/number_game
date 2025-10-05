import streamlit as st
import random 
import math
#grid size is now dynamic GRID_SIZE = 10
colors=["#FF5733", "#33FF57", "#3357FF", "#F333FF","#33FFF5", "#FF33F5", "#F5FF33", "#8A33FF","#33FF8A", "#FF8A33", "#338AFF", "#FF338A"]
if "grid" not in st.session_state:
    st.session_state.num = 1
    st.session_state.mult_count = 10
if "selected_cells" not in st.session_state:  #keep track of all the cells which are already clicked by the user
    st.session_state.selected_cells=set()
if "correct_cells" not in st.session_state:  #keep track of the cells that are correct
    st.session_state.correct_cells=set()
if "current_cell" not in st.session_state: #track of which correct cell should the user move next
    st.session_state.current_cell=0  
    

#to creat the grid side and the path
def generate_path(num,step, GRID_SIZE):
   #num is the multiplcation table and step is how many times we multiply it
    # a table is a list of lists [[6,5,4] [9,5,7]...]
    #forloop to make y rows (pink square bracket) and another forloop to make x columns in each row (inside the pink square bracket). Each of the cell contains a 0. When the cell is visited, the number changes from 0 to the multiplication number
    grid=[[0 for j in range(GRID_SIZE)] for i in range(GRID_SIZE)]
    #directions=[up down left right] but we cannot go outside of the grid
    directions=[(0,1),(0,-1),(-1,0),(1,0)]
    path=[]


    #now we are defining all the possible answers and it is going to start but 1 multiply by the number and the number of staps is the multipliactor 
    all_multiples = [num*i for i in range (1,step+1)]

    #i need to know where i am moving next so not x,y (my current position) but nx,ny (my next move). visited==False means "not visited yet"
    def is_move_valid(nx,ny):
        if (nx>=0 and nx<GRID_SIZE) and (ny>=0 and ny<GRID_SIZE) and grid[nx][ny]==0:
            return True
        else:
            return False
        
    #define starting point
    starting_point = [(0,y) for y in range (GRID_SIZE)] + [(x,0) for x in range (1,GRID_SIZE)]
    start=random.choice(starting_point)
    x,y=(start)
    path.append((x,y)) #append is used to integrate something in a path. It can only integrate one thing so if we want to include x,y as a unit, we need extra ()
    grid[x][y]=num
    current_value=num
    for i in range(1,step,1):
        random.shuffle(directions)
        placed=False #we haven't place any multiples yet
        for dx,dy in directions:
            nx=dx+x
            ny=dy+y
            
            if is_move_valid(nx,ny)==True:
                current_value+=num
                grid[nx][ny]=current_value
                path.append((nx,ny))
                x,y=nx,ny
                placed=True
                break # we define where x and y have to move, the new position becomes the new n,y and this will go one until break --> line 38 until all the multiples are used
        if not placed:
            return generate_path(num,step,GRID_SIZE)
        
    if x!=GRID_SIZE-1 and y!=GRID_SIZE-1:
        return generate_path(num,step,GRID_SIZE)
    #now we will fill everything with the distractors --> all the grid is fill with 0, then we define the path and now we need to change the remaining 0 have to be changed into distractors
    real_values=[grid[x][y]for x,y in path]
    for i in range (GRID_SIZE):
        for j in range (GRID_SIZE):
            if grid[i][j]==0: #if it is still 0, it is a distractor
                random_value=random.choice(real_values)
                distractor_value=random.randint(max(1,random_value-5),random_value+5)
                grid[i][j]=distractor_value
    return grid,path
                

    #we need to have an infinite loop of trying all options before finding the correct one
    #the path needs to be continious 
    # #fff to give a colour to the path already chosen

with st.sidebar: #what is the number and how many times. 
    st.session_state.num = st.number_input("Enter a number for the multiplication table:", min_value=1, step=1,value=st.session_state.num)
    st.session_state.mult_count = st.number_input("Enter a number for the multiplication count (max 50):", min_value=10, step=1,value=st.session_state.mult_count)
    if st.button("create grid"):
        min_cells_needed=st.session_state.mult_count+10 #(10 is the number of distractors)
        grid_size=math.ceil(math.sqrt(min_cells_needed)) # we look for the next square number to generate a grid. Ex: if the number is 20, this is not a square number so we have to make a grid of 25 (5x5)
        st.session_state.grid_size=grid_size #No matter the size of the grid we are storing it in a session 
        st.session_state.grid,st.session_state.path=generate_path(st.session_state.num,st.session_state.mult_count,grid_size)
        st.session_state.selected_cells=set()
        st.session_state.correct_cells=set()
        st.session_state.current_cell=0

def handle_click(x,y):
   
    cell=(x,y)
    if cell in st.session_state.selected_cells:
        return #if we have already visited a cell, we are not visiting it again and we'll go back to the path
    st.session_state.selected_cells.add(cell)
    if cell==st.session_state.path[st.session_state.current_cell]:#if cell is the correct cell to be clicked 
        st.session_state.correct_cells.add(cell) #we use add and not append because because it is a function of "set of cell"
        st.session_state.current_cell+=1

        #check if the current step is the last step of the path and congratulate with balloons
        if st.session_state.current_cell==len(st.session_state.path): #--. we are at the end of the path
            st.balloons()

def display_cell(x,y,value,correct,selected):
    if correct==True:
        color="lightgreen"
    elif selected==True:
        color="red"
    else:
        color="#e0e0e0"
    st.markdown(
        f"<div style='background-color: {color};"
        "border-radius: 8px; padding: 12px; text-align: center; font-size: 18px;'>"
        f"{value}"
        "</div>",
        unsafe_allow_html=True
    )
if "grid" in st.session_state:
    st.markdown("### MULTIPLICATION TABLE GRID")
    grid=st.session_state.grid
    path=st.session_state.path
    grid_size=st.session_state.grid_size
    for i in range(grid_size):  #ERROR HERE 
        cols=st.columns(grid_size)
        for j in range(grid_size):
            value=grid[i][j]
            cell=(i,j)
            correct=cell in st.session_state.correct_cells
            selected=cell in st.session_state.selected_cells and not correct
            if correct or selected:
                with cols[j]:
                    display_cell(i,j,value,correct,selected)
            else: 
                if cols[j].button(str(value),key=f"{i}-{j}"):
                    handle_click(i,j)
                    st.rerun()
    if "path" in st.session_state:
        if set(st.session_state.path) ==st.session_state.correct_cells and len(st.session_state.path)>0:
            st.balloons()

                
#to generate a track, we need to 1) check it is valid; 2) we need to backtrack

with st.expander("how to use this app"):
    st.markdown("""
                Enter a number for the multiplication table and follow the path""")

if st.button("show solution"):
    #write the solutions 
    #st.write("correct path is... ")
    st.balloons()
    
#next time handle click --> line 34
#18/07/2025 we haven't called the handle click functions and we haven't implemented the red and green colours
#show solution / help 
