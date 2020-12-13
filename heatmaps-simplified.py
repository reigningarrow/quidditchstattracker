# -*- coding: utf-8 -*-
"""
Created on Wed Sep 30 22:50:53 2020

@author: Sam
This is a messy code to make a get data to make a heatmap of events for a 
team in a quidditch match

"""
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

#makes sure folder exists
if os.path.exists('./graphs/')==False:
    os.mkdir('./graphs/') #creates folder

root=tk.Tk()   
root.iconbitmap('hoops_icon.ico')      #sets the window icon
root.title('Quidditch Analysis Alpha-Mapping')
#add a menu bar
graphs_menu=tk.Menu(root)
root.config(menu=graphs_menu)
rows=15
cols=30

pitch_frame=tk.Frame(root,width=100,height=50,bg='black',bd=2)

#creates the part of screen for selection of match
selection_frame=tk.Frame(root)
#adds tournament selection button
def select_tournament():
    #clears all data every time you select a new tournament
    clear()
    #sets the tournament name
    selected_tournament.set(cb_tournament.get())
    tournament=cb_tournament.get()
    #adds the list of game names/matchups to a combobox to choose a specific match
    game_list=os.listdir('./games/game_def/'+tournament+'/')
    #adds the list of games to the games combobox
    cb_match['values']=game_list
    #enables the select match buttons
    cb_match['state']='readonly'
    btn_choose_match['state']='normal'
    


def select_match():
    #function to select a specific match
    #need to use the global thing everytime you change the value, i think...
    global df_match
    global playerlist
    #reads the data from the csv file of all the players names and their team
    df_match=pd.read_csv('./games/game_def/'+selected_tournament.get()+'/'+cb_match.get())
    #print(df_match['Name'].tolist())
    playerlist=(df_match['Name'].to_list())
    selected_match.set(cb_match.get())
    player.set('')
    lbl_team.configure(text='Team')
    #gets the list of players from the data in the match and adds it to the combobox
    #cb_player['values']=playerlist
    lbl_team['state']='normal'
    #cb_player['state']='readonly'
    
    #gets the list of players from the data in the match and adds it 
    #to the listbox

    for players in playerlist:
        lstbox_players.insert('end',(players))  
    

selected_tournament=tk.StringVar()
#at the start this gets all the available tournaments and will add them to the combobox
tournament_list= [f.name for f in os.scandir('./games/game_def/') if f.is_dir()]
selected_match=tk.StringVar()
match=tk.StringVar()

#makes so that only files with a specific extension are chosen
def list_files1(directory, extension):
    return (f for f in os.listdir(directory) if f.endswith(extension))
matchlist=list_files1('./games/game_def/', '.csv')

def player_team(event):
    #gets the currently selected players team from the combobox selection
    #this changes each time a new player is selected
    #the try is in there because it throws an error if you 
    #select a different listbox for some reason

    try:
        selected_player=lstbox_players.get(lstbox_players.curselection())
        #selected_player=tk.ANCHOR()
        p_team=(df_match['Team'].to_list())
        #p_team_index=playerlist.index(cb_player.get())
        p_team_index=playerlist.index(selected_player)
        team.set(p_team[p_team_index])
        #player.set(cb_player.get())
        player.set(selected_player)
        #enables the buttons 
        if len(team.get())>14: #if team name is too long use the last word in their name
            team_l=team.get().split(' ')
            lbl_team.configure(text=team_l[-1])
        else:
            team_l=team.get()
            lbl_team.configure(text=team_l)
        #makes the buttons raised to know they're working
        if button[0]['state']!='normal':
            for c in range(rows*cols):
                button[c].config(state='normal',relief='raised')
    except:
        pass

cb_tournament=ttk.Combobox(selection_frame,value=tournament_list,state='readonly',width=30)
btn_tournament=tk.Button(selection_frame,text='Select tournament',command=select_tournament)

btn_tournament.grid(row=0,column=2,sticky='e')
cb_tournament.grid(row=0,column=0,columnspan=2,sticky='w')

ttk.Style().configure('cb_tournament', relief='sunken')

cb_match=ttk.Combobox(selection_frame,value='',state='readonly',width=30)
cb_match['state']='disabled'

#creates widgets
lbl_select_match=tk.Label(selection_frame,text='Choose match')
btn_choose_match=tk.Button(selection_frame,text='Select Match',width=12,command=select_match)

lbl_select_match.grid(row=1,column=0,columnspan=4)
btn_choose_match.grid(row=2,column=2,sticky='ew')
cb_match.        grid(row=2,column=0,columnspan=3,sticky='w')

btn_choose_match['state']='disabled'
#cb_player=ttk.Combobox(selection_frame,value='',state='readonly') 
#cb_player.bind('<<ComboboxSelected>>',player_team) #sets it so it registers a value when the combobox is changed

lstbox_players=tk.Listbox(selection_frame,height=20,width=30)
scrl_players=tk.Scrollbar(selection_frame) #scroll box
scrl_players.configure(command=lstbox_players.yview)

lstbox_players.bind("<<ListboxSelect>>", player_team)
lstbox_players.grid(row=4,column=0,rowspan=21,sticky='nsew')
scrl_players.grid(row=4,column=1,sticky='ns',rowspan=20)

player=tk.StringVar()
team  =tk.StringVar()
team.set('Team')

lbl_select_player=tk.Label(selection_frame,text='Select player to analyse')
lbl_team    =tk.Label(selection_frame,text=team.get(),width=12,justify='left')

lbl_select_player.grid(row=3,column=0,pady=(10,2),sticky='w')
#cb_player.grid(row=4,column=0,sticky='w',padx=(0,20))
lbl_team.grid(row=4,column=2,sticky='w')
#cb_player['state']='disabled'
lbl_team ['state']='disabled'

selection_frame.grid(row=0,column=1,rowspan=3,sticky='nsew')
coords=tk.StringVar()
button_num=tk.IntVar()
button=[]   

idx=tk.IntVar()
  
playername=0


def click(row, col,number):
    #changes all button colours back to system colour 
    #to make sure only one can be highlighted
    for c in range(rows*cols):
        button[c].config(bg="SystemButtonFace")
    label.configure(text=(row, col))          
    coords.set(label.cget('text')) #sets the coordinates to a tuple
    button[number].config(bg='red') #make selected button red
    button_num.set(number)
    #enables buttons again
    btn_goal.config(state='normal')
    btn_shot.config(state='normal')
    btn_pass.config(state='normal')
    btn_pass_end.config(state='normal')
    btn_catch.config(state='normal')
    btn_tackle.config(state='normal')
    btn_block.config(state='normal')
    btn_drop.config(state='normal')
    
    btn_btr.config(state='normal')
    btn_skr.config(state='normal')
    
def add_attempt(method):
    global dataframe
    #dataframe=pd.DataFrame()
    #adds to dataframe
    try:
        #tries to get the last line in the dataframe
        prev_name=dataframe['name'].iloc[-1]
        prev_team=dataframe['team'].iloc[-1]
        prev_event=dataframe['event'].iloc[-1]
        #if theres a catch or pass interaction use that as the pass end as well
        #this is to draw the arrows, this could be simplified but i dont think it affects speed much
        if (method=='catch' or method=='block' or method=='drop') and player.get!=prev_name and prev_event=='pass':
            #creates a dataframe for each new row then appends it to the dataframe
            d2=pd.DataFrame([{'id':idx.get()-1,'name':prev_name,'team':prev_team,'event':'pass end','coords':coords.get()}])
            #d2.set_index('id')
            dataframe=dataframe.append(d2)
    except:
        pass
    #adds the new interaction to a dataframe then appends it to the main dataframe
    d2=pd.DataFrame([{'id':idx.get(),'name':player.get(),'team':team.get(),'event':method,'coords':coords.get()}])
    #d2.set_index('id')
    dataframe=dataframe.append(d2)
    #dataframe.set_index('id',inplace=True)
    #updates the index number so rows dont get row values with multiple numbers
    idx.set(idx.get()+1)

    
    #changes selected button colour back to normal
    button[button_num.get()].config(bg="SystemButtonFace")
    #disables the data buttons so you can't just spam things accidentally
    btn_goal.config(state='disabled')
    btn_shot.config(state='disabled')
    btn_pass.config(state='disabled')
    btn_pass_end.config(state='disabled')
    btn_catch.config(state='disabled')
    btn_tackle.config(state='disabled')
    btn_block.config(state='disabled')
    btn_drop.config(state='disabled')
    
    btn_btr.config(state='disabled')
    btn_skr.config(state='disabled')
    
    btn_remove.config(state='normal')
    btn_reset.config(state='normal')
    save.config(state='normal')
    print(dataframe) 
    #adds the item to listbox
    lstbox_events.insert('end',((idx.get()-1)
                                ,method,str(team.get()),str(player.get()),coords.get()))    
'''
def clear():
    coords.set('')
    button_num.set(0)
    btn_goal.config(state='disabled')
    btn_shot.config(state='disabled')
    btn_pass.config(state='disabled')
    btn_catch.config(state='disabled')
    btn_tackle.config(state='disabled')
    btn_block.config(state='disabled')
    btn_drop.config(state='disabled')
    
    btn_btr.config(state='disabled')
    btn_skr.config(state='disabled')
    for c in range(rows*cols):
        button[c].config(bg="SystemButtonFace")
'''
def clear():
    #delete everything
    global dataframe
    #basically reinitialises the dataframe
    dataframe=pd.DataFrame()
    #dataframe=dataframe.drop(dataframe.iloc[0:0],axis=1) #remove everything from dataframe
    lstbox_events.delete(0,'end') #removes everything from listbox
    #dataframe.reset_index(inplace=True)
    #need to now return the dataframe somehow
    #resets all the data
    coords.set('')
    button_num.set(0)
    btn_goal.config(state='disabled')
    btn_shot.config(state='disabled')
    btn_pass.config(state='disabled')
    btn_pass_end.config(state='disabled')
    btn_catch.config(state='disabled')
    btn_tackle.config(state='disabled')
    btn_block.config(state='disabled')
    btn_drop.config(state='disabled')
    
    btn_btr.config(state='disabled')
    btn_skr.config(state='disabled')
    for c in range(rows*cols):
        button[c].config(bg="SystemButtonFace")
def remove():
    #deletes selected item from the listbox and drops it from the dataframe
    #try:
        #gets the currently selected item in the listbox
        vari=lstbox_events.get(lstbox_events.curselection())
        print(vari)
        #print(lstbox_events.curselection())
        #index = lstbox_events.get(0, "end").index(tk.ANCHOR)
        #deletes the item from the listbox
        lstbox_events.delete(tk.ANCHOR)
        #sets the index of the dataframe to the unique id number
        #then removes the relevant row as vari[0] gets the id number
        dataframe.set_index('id',inplace=True)
        dataframe.drop(index=vari[0],inplace=True)
        #resets the index to not be id cos it gives errors sometimes
        dataframe.reset_index(inplace=True)
    #except:
        #raise Exception("Currently can't remove some of the events in time, working on it")
        print(dataframe)


#Initial setup    
i=0    
#creates buttons and arranges it
for row in range(1,rows+1):
    for col in range(1,cols+1):
        #this creates a king of list of button items with the parameter
        button.append( tk.Button(pitch_frame, text='      ', 
                           command=lambda row=row,col=col,number=i:
                               click(row, col,number)))
        #provides spacing to show pitch markings
        if col==15: #midline    
            button[i].grid(row=row, column=col, sticky="nsew",padx=(0,5))
            
        elif col==10 or col==20: #keeper lines
            button[i].grid(row=row, column=col, sticky="nsew",padx=(0,5))
        elif col==7 or col==23: #hoop lines
            button[i].grid(row=row, column=col, sticky="nsew",padx=(0,5))
            if (row==7 or row==8 or row==9):
                button[i].grid(row=row, column=col, sticky="nsew",padx=(0,12))
            
        else:
            button[i].grid(row=row, column=col, sticky="nsew")
        i+=1
#disables the pitch buttons at the start
for c in range(rows*cols):
        button[c].config(state='disabled',relief='groove')
label = tk.Label(root, text="")


#label.grid(row=10, column=0, columnspan=10, sticky="new")
pitch_frame.grid(row=0,column=3,rowspan=10,sticky='new',pady=(20),padx=(2,0))

#adds frame for all buttons and creates and places buttons
button_grid=tk.Frame(root)
btn_shot=tk.Button(button_grid,text='Goal attempt',width=12,command=lambda: add_attempt('shot'))
btn_goal=tk.Button(button_grid,text='Goal',width=12,command=lambda: add_attempt('goal'))
btn_pass=tk.Button(button_grid,text='Pass start',width=12,command=lambda:add_attempt('pass'))
btn_pass_end=tk.Button(button_grid,text='Pass end point',command=lambda:add_attempt('pass end'))
btn_catch=tk.Button(button_grid,text='Catch',width=12,command=lambda:add_attempt('catch'))
btn_tackle=tk.Button(button_grid,text='Completed tackle',width=16,command=lambda:add_attempt('tackle'))
btn_block=tk.Button(button_grid,text='Block/interception',width=16+1,command=lambda:add_attempt('block'))
btn_drop=tk.Button(button_grid,text='Dropped pass',width=16,command=lambda:add_attempt('drop'))

btn_btr=tk.Button(button_grid,text='Beater engages beater',width=25,command=lambda:add_attempt('beater'))
btn_skr=tk.Button(button_grid,text='Snitch catch attempt',width=25,command=lambda:add_attempt('sk catch'))


btn_shot.grid(row=0,column=0,columnspan=3,sticky='ew')
btn_goal.grid(row=0,column=3,columnspan=3,sticky='ew')
btn_pass.grid(row=0,column=6,columnspan=3,sticky='ew')
btn_pass_end.grid(row=2,columnspan=16,sticky='ew')
btn_catch.grid(row=0,column=9,columnspan=3,sticky='ew')
btn_tackle.grid(row=1,column=0,columnspan=4,sticky='ew')
btn_block.grid(row=1,column=4,columnspan=4,sticky='ew')
btn_drop.grid(row=1,column=8,columnspan=4,sticky='ew')

btn_btr.grid(row=3,column=0,columnspan=6,sticky='ew')
btn_skr.grid(row=3,column=6,columnspan=6,sticky='ew')

button_grid.grid(row=3,column=3,pady=(10,10),sticky='n')

#panel.grid(row=0,column=0,rowspan=rows,columnspan=cols,sticky='nsew')

#get the events stuff all together
evt_frame=tk.Frame(root)
#list box of events and their scroll bars
lstbox_events=tk.Listbox(evt_frame,height=25,width=30)
scrl_evt=tk.Scrollbar(evt_frame) #scroll box
scrl_evt.configure(command=lstbox_events.yview)

scrl_x_evt=tk.Scrollbar(evt_frame,orient=tk.HORIZONTAL) # horizontal scroll box
scrl_x_evt.configure(command=lstbox_events.xview)
lstbox_events.configure(yscrollcommand=scrl_evt.set,xscrollcommand=scrl_x_evt.set)

btn_reset=tk.Button(evt_frame,text='Clear',width=15,command=clear)
btn_remove=tk.Button(evt_frame,text='Remove entry',width=15,command=lambda:remove())


lstbox_events.grid(row=0,column=30,rowspan=21,columnspan=3)
scrl_evt.grid(row=0,column=33,sticky='ns',rowspan=20)
scrl_x_evt.grid(row=21,column=30,sticky='ew',columnspan=3)
btn_remove.grid(row=22,column=30,columnspan=3,pady=(0,10))
btn_reset.grid(row=23,column=30,columnspan=3)


evt_frame.grid(row=0,column=4,rowspan=12,padx=(10,0),sticky='n')

#at the start disable everything
btn_remove.config(state='disabled')
btn_reset.config(state='disabled')

btn_goal.config(state='disabled')
btn_shot.config(state='disabled')
btn_pass.config(state='disabled')
btn_pass_end.config(state='disabled')
btn_catch.config(state='disabled')
btn_tackle.config(state='disabled')
btn_block.config(state='disabled')
btn_drop.config(state='disabled')

btn_btr.config(state='disabled')
btn_skr.config(state='disabled')


def createPitch(color='black',pitch='full'): 
    # in meters
    # Code by @JPJ_dejong
    #modified by @reigningarrow
    
    """
    creates a plot in which the 'length' is the length of the pitch (goal to goal).
    And 'width' is the width of the pitch (sideline to sideline). 
    """
    #get pitch dimensions
    length=60
    width =33
    linecolor=color #white
    if pitch=='full':
        #Create figure
        fig=plt.figure(figsize=(length,width))
        
        #fig.set_size_inches(7, 5)
        ax=fig.add_subplot(1,1,1)
        #ax.set_facecolor('#94B560') #this doesnt work but doesnt need to
        #Pitch Outline & Centre Line
        plt.plot([0,0],[0,width], color=linecolor,linewidth=10)
        plt.plot([0,length],[width,width], color=linecolor,linewidth=10)
        plt.plot([length,length],[width,0], color=linecolor,linewidth=10)
        plt.plot([length,0],[0,0], color=linecolor,linewidth=10)
        #halfway line
        plt.plot([length/2,length/2],[0,width], color=linecolor)
        
        #Edge of keeper zones
        plt.plot([length/2-11,length/2-11],[0,width],color=linecolor)
        plt.plot([length/2+11,length/2+11],[0,width],color=linecolor)
        
        
        #Goal lines
        plt.plot([length/2+16.5,length/2+16.5],[0,width],color=linecolor)
        plt.plot([length/2-16.5,length/2-16.5],[0,width],color=linecolor)
        
        #Right Hoops
        plt.plot([length/2+16.5,length/2+16.5],[width/2-2.5-0.9,width/2-2.5+0.9],color=linecolor,linewidth=20)
        plt.plot([length/2+16.5,length/2+16.5],[width/2-0.9,width/2+0.9],color=linecolor,linewidth=20)
        plt.plot([length/2+16.5,length/2+16.5],[width/2+2.5-0.9,width/2+2.5+0.9],color=linecolor,linewidth=20)
        
        #Left Hoops
        plt.plot([length/2-16.5,length/2-16.5],[width/2-2.5-0.9,width/2-2.5+0.9],color=linecolor,linewidth=20)
        plt.plot([length/2-16.5,length/2-16.5],[width/2-0.9,width/2+0.9],color=linecolor,linewidth=20)
        plt.plot([length/2-16.5,length/2-16.5],[width/2+2.5-0.9,width/2+2.5+0.9],color=linecolor,linewidth=20)
    #if you're using something that only needs to show half the pitch make a half pitch
    elif pitch=='half':
        #Create figure
        fig=plt.figure(figsize=(length/2,width))

        ax=fig.add_subplot(1,1,1)
        ax.set_facecolor('#94B560')
        #Pitch Outline & Centre Line
        plt.plot([0,0],[0,width], color=linecolor)
        plt.plot([0,length/2],[width,width], color=linecolor)

        plt.plot([length/2,0],[0,0], color=linecolor)
        plt.plot([length/2,length/2],[0,width], color=linecolor)
        
        #Edge of keeper zones
        plt.plot([length/2-11,length/2-11],[0,width],color=linecolor)

        #Goal lines
        plt.plot([length/2-16.5,length/2-16.5],[0,width],color=linecolor)
        
        #Left Hoops
        plt.plot([length/2-16.5,length/2-16.5],[width/2-2.5-0.9,width/2-2.5+0.9],color=linecolor,linewidth=20)
        plt.plot([length/2-16.5,length/2-16.5],[width/2-0.9,width/2+0.9],color=linecolor,linewidth=20)
        plt.plot([length/2-16.5,length/2-16.5],[width/2+2.5-0.9,width/2+2.5+0.9],color=linecolor,linewidth=20)

    else:
        #give error if the wrong argument is inputted it shouldn't but just incase
        raise Exception('Only acceptable keywords are "half" and "full"')
    #Tidy Axes
    
    plt.axis('off')
    #plt.show()
    
    return fig,ax


#saves the data
def save_data():
    #for potential future saving to a cloud server
    uname=os.getlogin()
    match=selected_match.get().split('.') #gets the name of the match
    match=match[0]
    #this should create a progress bar, but program seems to freeze
    #whilst saving so eh
    bar = ttk.Progressbar(button_grid, length=400)
    bar.grid(row=4,column=0,columnspan=40,sticky='ew')
    bar['value'] = 0
    it_length=len(dataframe)*2*6
    #goes through each unique value in the team then name columns
    #this means it plots graphs per team and then per person
    for kind in ['team','name']:
        
        for team in dataframe[kind].unique():
            #makes sure there is only data that we want in the dataframe
            #dataframe2=dataframe[dataframe.kind.isin(team)].copy()
            dataframe2=dataframe[dataframe[kind]==team]

            #choose the types of graphs to be looked at individually
            #so shots and goals are grouped
            graphs=[['shot','goal'],['pass','catch','pass end','drop','block'],
                    ['catch','drop'],['block'],['beater'],['sk catch']]
            
            for item in graphs:
                #adds 4 values at the start to make sure the kde plot covers the whole pitch
                x_kde=[-5,-5,65,65]
                y_kde=[-5,40,-5,40]
                #makes sure that we only have data from the events we want
                df=dataframe2[dataframe2.event.isin(item)].copy()
                #if theres no events of the category skip it
                if len(df.index)==0:
                    continue
                #if its a shot map only show half of the pitch
                if item==['shot','goal']:
                    (fig,ax)=createPitch(pitch='half') 
                else:
                    (fig,ax)=createPitch() 
                 #need to do this for each team, each player, each type of interaction
                 #for shots if a shot goes in it should be a different colour
                for i,data in df.iterrows():
                    d2=data
                    data=data['coords'].split() #splits the coordinates into x and y
                    
                    
                    
                    #sets the x and y values so they fit in the pitch image
                    print('x',data[-1],type(data[0]))
                    print('y',data[0],type(data[-1]))
                    
                    y=int(data[0])*33/15
                    x=int(data[-1])*60/30-0.5
                    #if its a shot goal maps all shots to one side
                    if item==['shot','goal']:
                        #print('x coords of shots')
                        #print(x)
                        #if its in the right hand half of the pitch map it
                        #to the left hand side
                        if x>30:
                            x-=(30+16.5)
                            if x<0:
                                x=abs(x)
                            else:
                                x=-1*x
                            x=x+13.5

                        
                    #makes the data look the same way you record it, ie not flipped
                    if (y-33)<0:
                        y=abs(y-33)+1
                    else:
                        y=y-33+1
                    #adds the data for the kde plot
                    x_kde.append(x)
                    y_kde.append(y)
                    if item==['pass','catch','pass end','drop','block']:
                        #if its a pass start don't plot anything wait till the pass end
                         if d2['event']=='pass':
                             continue
                         else:
                             #gets the location of the pass starting location
                             pass_start_loc=dataframe['coords'].iloc[i-1].split()

                             y_start=int(pass_start_loc[0])*33/15
                             x_start=int(pass_start_loc[-1])*60/30-0.5
                         
                             #makes the data look the same way you record it, ie not flipped
                             if (y_start-33)<0:
                                 y_start=abs(y_start-33)+1
                             else:
                                 y_start=y_start-33+1
                                 
                         colour='gray'
                         if d2['event']=='pass end':
                             #as the player isnt at the pass end remove that entry in kde coords
                             if kind!='team':
                                 del x_kde[-1]
                                 del y_kde[-1]
                             try:
                                 #sets the colours for each event
                                 evt=dataframe['event'].iloc[i+1]
                                 if evt=='catch':
                                     colour='black'
                                 elif evt=='block':
                                     colour='red'
                                 elif evt=='drop':
                                     colour='orange'
                             except:
                                 raise Exception("Can't set the colours of the arrows")
                                 #draw the arrows       
                             plt.annotate("", xy = (x, y), xycoords = 'data',
                xytext = (x_start, y_start), textcoords = 'data',
                arrowprops=dict(width=5,headwidth=40,headlength=50,connectionstyle="arc3", color = colour))
                    else:
                        #changes the circle colour based on event type    
                        colour='blue'
                        if d2['event']=='goal':
                            colour='red'
                        elif d2['event']=='drop':
                            colour='orange'
                        #adds circles of size 1 and alpha needs to be changed
                        circle=plt.Circle((x,y),0.9,color=colour,alpha=0.4)
                        #if its a team map add players names     
                        if kind=='team':
                            plt.annotate(d2['name'],(x,y),size=25)
                        
                        ax.add_patch(circle) #adds it to the graph
                #fig.set_facecolor('green')
                #adds the kde plot to the graph
                sns.kdeplot(x_kde, y_kde, shade = "True", cmap='summer', n_levels = 100,alpha=0.75)
                #if the length of the coords is greater than 0, then check if limits cos errors...
                if len(x_kde)>6 and len(y_kde)>6:
                    '''
                    #if its a shot goal graph then only do 1 half of the map
                    if max(x_kde[5:])<30 and item==['shot','goal']:
                        plt.xlim(0,31)
                    elif min(x_kde[5:])>30 and item==['shot','goal']:
                        plt.xlim(29,60)
                    else:
                        plt.xlim(0,60)
                    '''
                    #if its a goal/shot graph make sure it only shows one part of the pitch
                    if item==['shot','goal']:
                        plt.xlim(0,31)
                else:
                    #otherwise set the pitch limits to the full pitch
                    #basically doesn't show the edges of the kde graph as those 4 points are off the pitch
                    plt.xlim(0,60)
                plt.ylim(0,33)
                

                #saves the data and graphs       
                if kind=='team':
                    #makes sure the folder exists
                    if os.path.exists('./graphs/'+selected_tournament.get()+'/'+match
                                +'/'+team+'/')==False:
                        os.makedirs('./graphs/'+selected_tournament.get()+'/'+match
                                +'/'+team+'/')
                    #saves the figure
                    fig.savefig('./graphs/'+selected_tournament.get()+'/'+match
                                +'/'+team+'/'+str(item[0])+'.png', dpi=100) 
                elif kind=='name':
                    if os.path.exists('./graphs/'+selected_tournament.get()+'/'+match
                                +'/'+d2['team']+'/')==False:
                        os.makedirs('./graphs/'+selected_tournament.get()+'/'+match
                                +'/'+d2['team']+'/')
                    fig.savefig('./graphs/'+selected_tournament.get()+'/'+match
                                +'/'+d2['team']+'/'+team+'-'+str(item[0])+'.png', dpi=100,facecolor=fig.get_facecolor())
                plt.show()
                #adds a bit to the end of the bar
                bar['value'] +=1/it_length
                
    print('FINISHED!! :D')
    #basically if its just a totals file dont save it again
    if selected_match.get()!='totals.csv':
        #saves the match data to a csv file
        if os.path.exists('./graphs/'+selected_tournament.get()+'/')==False:
            os.makedirs('./graphs/'+selected_tournament.get()+'/')
        dataframe.to_csv('./graphs/'+selected_tournament.get()+'/'+selected_match.get())
        
        
        #adds the match data to a csv file for the whole tournament
        #if  the files exists add to it, otherwise create the file
        if os.path.isfile('./graphs/'+selected_tournament.get()+'/totals.csv')==True:
            df=pd.read_csv('./graphs/'+selected_tournament.get()+'/totals.csv',index_col=0)
            df=df.append(dataframe)
            df.to_csv('./graphs/'+selected_tournament.get()+'/totals.csv')
        else:
            dataframe.to_csv('./graphs/'+selected_tournament.get()+'/totals.csv')
        
        #adds the data to total csv file and saves it
        if os.path.isfile('./graphs/totals.csv')==True:
            df=pd.read_csv('./graphs/totals.csv',index_col=0)
            df=df.append(dataframe)
            df.to_csv('./graphs/totals.csv')
        else:
            dataframe.to_csv('./graphs/totals.csv')
    
        
    
    bar.grid_forget() #removes the loading bar once done
    clear() #clears the data from the listbox and dataframe

    
    
draw_pitch=tk.Button(text='draw pitch',command=lambda: createPitch(pitch='half'))
#draw_pitch.grid(row=100,column=100)

save=tk.Button(text='Save',width=10,command=lambda:save_data())
save.grid(rows=10,columns=30)
save.config(state='disabled')
def import_data():
    #opens file
    global dataframe
    data=filedialog.askopenfilename(initialdir='.\graphs',title='Import match data',filetypes =[('CSV', '*.csv')])
    #if there is already data stored add to it otherwise create a new dataframe
    try:
        dataframe=dataframe.append(dataframe.read_csv(data,index_col=0))
    except:
        dataframe=pd.read_csv(data,index_col=0)
    #adds each event to the list box 
    for i,row in dataframe.iterrows():
        lstbox_events.insert('end',(row.id,row.event,row.team,row['name'],row.coords))    
    print(dataframe)
    #print(data)
    #gets the tournament and match names
    info=data.split('/')
    tournament_name=info[-2]
    game_name=info[-1].split('.')[0]
    #if you're adding a totals file set the graphs to be saved in a totals folder
    if game_name=='totals':
        selected_tournament.set(tournament_name)
    else:
        selected_tournament.set(tournament_name)
    if tournament_name=='graphs':
        selected_tournament.set('totals')
    #sets the tournament and match names
    
    selected_match.set(game_name+'.csv')
    
    #allows all of the buttons to work
    for c in range(rows*cols):
        button[c].config(state='normal',relief='raised')
    #makes the buttons for the listbox work
    btn_remove.config(state='normal')
    btn_reset.config(state='normal')
    save.config(state='normal')
#file menu
file_menu=tk.Menu(graphs_menu,tearoff=0)
graphs_menu.add_cascade(label='File',menu=file_menu)
file_menu.add_command(label='Import Data',command=import_data)
file_menu.add_command(label='Exit',command=root.quit)

root.mainloop()
#
#https://github.com/tuangauss/DataScienceProjects/blob/master/Python/football_visual.ipynb
#video for this
#https://www.youtube.com/watch?v=oOAnERLiN5U&list=PLedeYskZY0vBOdQ6Uc9eZjZ2-nz1JT3R7&index=6
#making a shot and pass map
#https://github.com/Friends-of-Tracking-Data-FoTD/SoccermaticsForPython/blob/master/7PassHeatMap.py 