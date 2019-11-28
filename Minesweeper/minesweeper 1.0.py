from tkinter import *
from random import randint
import time

width=9
height=9
difficulty=10
time_elapsed=0
game_ongoing=True
max_score=width*height-difficulty
matrix=[]
matrix_row=[]
my_button=[]
button_row=[]
click_counter=0
game_window=Tk()
game_window.resizable(False, False)
game_window.title("Minesweeper")
game_frame=Label(game_window, text="")
game_title=Label(game_window, text="")
mine_frame=Label(game_window, text="")
num_colors=['','#000ea8','#008ca8','#00a840','#7ba836','#a8a800','#a85400','#a80000','#540000']
flag_image=PhotoImage(file="flagicon.gif")
fitted_flag_image=flag_image.subsample(20,20)
mine_image=PhotoImage(file="mineicon.gif")
fitted_mine_image=mine_image.subsample(20,20)

class Buttons:
    def __init__(self,i,j,has_mine):
        self.mine=has_mine
        self.xcoor=i
        self.ycoor=j
        self.clicked=False
        self.num_mines=0
        self.has_flag=False
        
    def button_reveal(self):
        global click_counter
        global game_title
        global game_ongoing
        global fitted_mine_image
        if (self.num_mines==0):
            empty_block_reveal(self.xcoor,self.ycoor)             
           
        if (self.mine):
            game_ongoing=False           
            game_title["text"]=str("YOU LOSE")
            for i in range (height):
                for j in range (width):
                    if(self.has_flag):
                        my_button[i][j].config(image='', width=4, height=1)                     
                    if (matrix[i][j].mine):
                        my_button[i][j].config(image=fitted_mine_image, width=32, height=20)
                    my_button[i][j].config(command=0, relief=SUNKEN)

        else:
            if not(self.num_mines==0):
                click_counter+=1
                matrix[self.xcoor][self.ycoor].clicked=True
                if(self.has_flag):
                    my_button[self.xcoor][self.ycoor].config(image='', width=4, height=1)
                my_button[self.xcoor][self.ycoor]["text"]=str(self.num_mines)
                my_button[self.xcoor][self.ycoor].config(command=0,relief=SUNKEN,fg=num_colors[matrix[self.xcoor][self.ycoor].num_mines])
                my_button[self.xcoor][self.ycoor].bind("<Button-3>", lambda e:None)

        check_win()
        
    def set_flag(self, event):
        global fitted_flag_image
        if not(self.has_flag):
            self.has_flag=True
            my_button[self.xcoor][self.ycoor].config(image=fitted_flag_image, width=32, height=20)
        else:
            self.has_flag=False
            my_button[self.xcoor][self.ycoor].config(image='', width=4, height=1)

def set_matrix():
    global matrix
    global matrix_row
    matrix=[]
    for i in range (height):
        matrix_row=[]
        for j in range (width):
            matrix_row.append(Buttons(i,j,False))
        matrix.append(matrix_row)

def set_buttons():
    global my_button
    global button_row
    my_button=[]
    for i in range (height):
        button_row=[]
        for j in range (width):
            b=Button(mine_frame, text="", width = 4, command = lambda r=i,c=j: matrix[r][c].button_reveal())
            b.grid(row=i, column=j, sticky=W)
            b.bind("<Button-3>", matrix[i][j].set_flag)
            button_row.append(b)
        my_button.append(button_row)

def mine_generator():
    counter=0
    while counter<difficulty:
        mine_ycoor=randint(0,height-1)
        mine_xcoor=randint(0,width-1)        
        if not(matrix[mine_ycoor][mine_xcoor].mine):
            matrix[mine_ycoor][mine_xcoor].mine=True
            matrix[mine_ycoor][mine_xcoor].num_mines=10
            counter+=1

def mine_counter():
    for i in range (height):
        for j in range (width):
            if not(matrix[i][j].mine):
                if ((j+1)<width):
                    if (matrix[i][j+1].mine):
                        matrix[i][j].num_mines+=1
                if ((i-1)>=0):
                    if (matrix[i-1][j].mine):
                        matrix[i][j].num_mines+=1
                if ((i+1)<height):
                    if (matrix[i+1][j].mine):
                        matrix[i][j].num_mines+=1
                if ((j-1)>=0):
                    if (matrix[i][j-1].mine):
                        matrix[i][j].num_mines+=1
                if ((i+1)<height and (j-1)>=0):
                    if (matrix[i+1][j-1].mine):
                        matrix[i][j].num_mines+=1
                if ((i+1)<height and (j+1)<width):
                    if (matrix[i+1][j+1].mine):
                        matrix[i][j].num_mines+=1
                if ((i-1)>=0 and j<width-1):
                    if (matrix[i-1][j+1].mine):
                        matrix[i][j].num_mines+=1
                if ((i-1)>=0 and(j-1)>=0):   
                    if (matrix[i-1][j-1].mine):
                        matrix[i][j].num_mines+=1  

def empty_block_reveal(i, j):
    global click_counter 
    global num_colors
    if ((matrix[i][j].num_mines<=8) and matrix[i][j].clicked==False):
        click_counter+=1
        if(matrix[i][j].has_flag):
            my_button[i][j].config(image='', width=4, height=1)        
        my_button[i][j].config(command=0,relief=SUNKEN)
        my_button[i][j].bind("<Button-3>", lambda e:None)
        matrix[i][j].clicked=True
        if(matrix[i][j].num_mines==0):
            if ((j+1)<width):
                empty_block_reveal(i,j+1)
            if ((i-1)>=0):
                empty_block_reveal(i-1,j)
            if ((i+1)<height):
                empty_block_reveal(i+1,j)
            if ((j-1)>=0):
                empty_block_reveal(i,j-1)
            if ((i+1)<height and (j-1)>=0):
                empty_block_reveal(i+1,j-1)
            if ((i+1)<height and (j+1)<width):
                empty_block_reveal(i+1,j+1)
            if ((i-1)>=0 and j<width-1):
                empty_block_reveal(i-1,j+1)
            if ((i-1)>=0 and(j-1)>=0):   
                empty_block_reveal(i-1,j-1)  
        else:
            my_button[i][j]["text"]=str(matrix[i][j].num_mines)
            my_button[i][j].config(fg=num_colors[matrix[i][j].num_mines])
    check_win()

def check_win():
    global click_counter
    global game_title
    global game_ongoing
    global fitted_mine_image
    global game_frame
    global width
    global height
    global difficulty
    if (click_counter==max_score):
        game_ongoing=False
        game_title["text"]=str("YOU WIN")
        for i in range (height):
            for j in range (width):
                if (matrix[i][j].mine):
                    if(matrix[i][j].has_flag):
                        my_button[i][j].config(image='', width=4, height=1)                    
                    my_button[i][j].config(image=fitted_mine_image, width=32, height=20)
                my_button[i][j].config(command=0)
                my_button[i][j].config(relief=SUNKEN)  

def main_menu():
    global game_title
    global game_frame
    global width
    global height
    global difficulty
    difficulty_label=""
    
    game_board_reset()
    game_frame=Frame(game_window)
    game_frame.grid(row=1, column=0, sticky=N)
    
    if (width==9 and height==9 and difficulty==10):
        difficulty_label=" Beginner"
    if (width==16 and height==16 and difficulty==40):
        difficulty_label=" Intermediate"
    if (width==30 and height==16 and difficulty==99):
        difficulty_label=" Expert"            
    
    game_title=Label(game_window, text="Welcome to Minesweeper\n\n Game is set to"+difficulty_label+":\n "+str(width)+"x"+str(height)+" grid with "+str(difficulty)+" mines\n")    
    game_title.grid(row=0, column=0, sticky=N)
    
    mainmenuoptions_frame=Frame(game_frame)
    mainmenuoptions_frame.grid(row=1, column=0, sticky=S)
    
    Button(mainmenuoptions_frame, text="Enter", width = 11, command = game_restart).grid(row=0, column=0, sticky=S)
    Button(mainmenuoptions_frame, text="Settings", width = 11, command = settings).grid(row=0, column=1, sticky=S)
    Button(mainmenuoptions_frame, text="Exit", width = 11, command = exit).grid(row=0, column=3, sticky=S)

def set_timer():
    global game_frame
    global time_elapsed
    time_elapsed=0
    timer=Label(game_frame, text=("Time Elapsed: "+str(time_elapsed)))
    def start_timer():
        global game_ongoing
        global time_elapsed
        timer.grid(row=1, column=0, sticky=N)
        if(game_ongoing):
            timer["text"]=("Time Elapsed: "+str(time_elapsed))
            time_elapsed+=1 
            timer.after(1000, start_timer)  
        else:
            timer["text"]=("Total Time Elapsed: "+str(time_elapsed-1))
    start_timer()

def game_restart():
    global click_counter
    global game_title
    global mine_frame
    global game_frame
    global game_ongoing

    game_board_reset()
    click_counter=0
    game_ongoing=True
    
    game_frame=Frame(game_window)
    game_frame.grid(row=1, column=0, sticky=N)    
    
    game_title=Label(game_frame, text="")
    game_title.grid(row=0, column=0, sticky=N)
    mine_frame=Frame(game_frame)
    mine_frame.grid(row=2, column=0, sticky=N)    
    ingameoptions_frame=Frame(game_frame)
    ingameoptions_frame.grid(row=3,column=0, sticky=S)
    
    set_matrix()
    set_buttons()
    mine_generator()
    mine_counter()
    set_timer()
    
    Button(ingameoptions_frame, text="Restart", width = 10, command = game_restart).grid(row=0, column=0, sticky=S)
    Button(ingameoptions_frame, text="Main Menu", width = 10, command = main_menu).grid(row=0, column=1, sticky=S)

def settings():
    global game_title
    global game_frame
    
    game_board_reset()
    game_title=Label(game_window, text="Game Settings")
    game_title.grid(row=0, column=0, sticky=N)    
    game_frame=Frame(game_window)
    game_frame.grid(row=1, column=0, sticky=N)
    settings_frame=Frame(game_frame)
    settings_frame.grid(row=0, column=0, sticky=N)
    more_settings=Frame(game_frame)
    more_settings.grid(row=1,column=0, sticky=N)
    
    
    Button(settings_frame, text="Beginner", width = 12, command = lambda: classic_settings(0)).grid(row=0, column=0, sticky=S)
    Button(settings_frame, text="Intermediate", width = 12, command = lambda: classic_settings(1)).grid(row=1, column=0, sticky=S)  
    Button(settings_frame, text="Expert", width = 12, command = lambda: classic_settings(69420)).grid(row=2, column=0, sticky=S)  
    Button(more_settings, text="Custom", width = 10, command = dimension_settings).grid(row=0, column=0, sticky=S)  
    Button(more_settings, text="Main Menu", width = 10, command = main_menu).grid(row=1, column=0, sticky=S)  
    
    Label(settings_frame, text="9x9, 10 Mines").grid(row=0, column=1, sticky=S)
    Label(settings_frame, text="16x16, 40 Mines").grid(row=1, column=1, sticky=S)
    Label(settings_frame, text="30x16, 99 Mines").grid(row=2, column=1, sticky=S)
    
def classic_settings(setting):
    global width
    global height
    global difficulty    
    if setting==0:
        width=9
        height=9
        difficulty=10
        game_restart()
    if setting==1:
        width=16
        height=16
        difficulty=40
        game_restart()
    if setting==69420:
        width=30
        height=16
        difficulty=99 
        game_restart()

def dimension_settings():
    global game_title
    global game_frame
    global width
    global height    
    
    def set_width(Event):
        global width
        user_input=width_entry.get()
        try: 
            user_input=int(user_input)
            if(user_input>2 and user_input<51):
                width=user_input
                width_label["text"]=str("New width = "+str(width))
            else:
                game_title["text"]=str("Please enter a width greater than 2 and less than 51")
        except ValueError:
            game_title["text"]=str("Please enter a number greater than 2 and less than 51") 
        width_entry.delete(0, "end")
    
    def set_height(Event):
        global height
        user_input=height_entry.get()
        try: 
            user_input=int(user_input)
            if(user_input>2 and user_input<51):
                height=user_input
                height_label["text"]=str("New height = "+str(height))
            else:
                game_title["text"]=str("Please enter a height greater than 2 and less than 51")
        except ValueError:
            game_title["text"]=str("Please enter a number greater than 2 and less than 51") 
        height_entry.delete(0, "end")      
        
    game_board_reset()
    game_frame=Frame(game_window)
    game_frame.grid(row=1, column=0, sticky=N)     
    game_title=Label(game_window, text="Dimension Settings\n\n Press 'enter' after entry to update dimension\n Press 'Set Mines' to set mines")
    game_title.grid(row=0, column=0, sticky=N)
    settings_frame=Frame(game_frame)
    settings_frame.grid(row=1, column=0, sticky=N)
    settings_options_frame=Frame(game_frame)
    settings_options_frame.grid(row=2, column=0, sticky=N)
    
    width_label=Label(settings_frame, text="Current width = "+str(width))
    width_label.grid(row=0)
    width_entry=Entry(settings_frame)
    width_entry.bind("<Return>", set_width)
    width_entry.grid(row=0, column=1, sticky=N)
    
    height_label=Label(settings_frame, text="Current height = "+str(height))
    height_label.grid(row=1)
    height_entry=Entry(settings_frame)
    height_entry.bind("<Return>", set_height)
    height_entry.grid(row=1, column=1, sticky=N)
    
    Button(settings_options_frame, text="Settings", width = 10 , command = settings).grid(row=0, column=0, sticky=S)  
    Button(settings_options_frame, text="Set Mines", width = 10, command = difficulty_settings).grid(row=0, column=1, sticky=S)   

def difficulty_settings():
    global game_frame
    global game_title
    global width
    global height
    global difficulty
    
    def set_difficulty(Event):
        global difficulty
        user_input=difficulty_entry.get()
        try: 
            user_input=int(user_input)
            if(user_input>0 and user_input<width*height-1):
                difficulty=user_input
                difficulty_label["text"]=str("New number of mines = "+str(difficulty))
            else:
                game_title["text"]=str("Please enter a number of mines greater than 1 and less than "+str(width*height-1))
        except ValueError:
            game_title["text"]=str("Please enter a number greater than 1 and less than "+str(width*height-1)) 
        difficulty_entry.delete(0, "end")   
    
    game_board_reset()
    game_title=Label(game_window, text="Mine Settings\n\n Press 'enter' after entry to update number of mines\n Press 'Start Game' to start the game")
    game_title.grid(row=0, column=0, sticky=N)
    game_frame=Frame(game_window)
    game_frame.grid(row=1, column=0, sticky=N)    
    difficulty_frame=Frame(game_frame)
    difficulty_frame.grid(row=0)
    difficulty_options_frame=Frame(game_frame)
    difficulty_options_frame.grid(row=1)
    
    if(difficulty>width*height-1):
        difficulty=2
    
    difficulty_label=Label(difficulty_frame, text="Current number of mines = "+str(difficulty))
    difficulty_label.grid(row=0)    
    difficulty_entry=Entry(difficulty_frame)
    difficulty_entry.bind("<Return>", set_difficulty)
    difficulty_entry.grid(row=0, column=1, sticky=N)
    
    Button(difficulty_options_frame, text="Settings", width = 10 , command = settings).grid(row=0, column=0, sticky=S)
    Button(difficulty_options_frame, text="Start Game", width = 10, command = game_restart).grid(row=0, column=1, sticky=S)

def game_board_reset():
    global game_title
    global mine_frame
    global game_frame
    global max_score
    global width
    global height
    global difficulty
    global click_counter
    max_score=width*height-difficulty
    click_counter=0
    game_title.destroy()
    game_frame.destroy()
    mine_frame.destroy()

main_menu()

game_window.mainloop()