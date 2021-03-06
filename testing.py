# -*- coding: utf-8 -*-
"""
Created on Wed Sep 30 22:50:53 2020

@author: Sam
This is a messy code to make a get data to make a heatmap of events for a 
team in a quidditch match

"""
import tkinter as tk
from tkinter import ttk
import pandas as pd
from PIL import ImageTk,Image 
import matplotlib.pyplot as plt
import numpy as np
import os

if os.path.exists('./graphs/')==False:
    os.mkdir('./graphs/') #creates folder

root=tk.Tk()   

rows=15
cols=30

pitch_frame=tk.Frame(root,width=100,height=50,bg='black',bd=2)
'''
pitch_image=ImageTk.PhotoImage(Image.open('Hoops.png'))
lbl_pitch_img = tk.Label(pitch_frame,image=pitch_image)
#lbl_pitch_img.place(x=0, y=0, relwidth=1, relheight=1)        
lbl_pitch_img.grid(row=0,column=0,rowspan=rows,columnspan=cols)
'''

img = ImageTk.PhotoImage(Image.open('Hoops.png'))
#panel = tk.Label(pitch_frame, image = img)

selection_frame=tk.Frame(root)
#adds tournament selection button
def select_tournament():
    #sets the tournament name
    selected_tournament.set(cb_tournament.get())
    tournament=cb_tournament.get()
    game_list=os.listdir('./games/game_def/'+tournament+'/')
    #adds the list of games to the games combobox
    cb_match['values']=game_list
    cb_match['state']='readonly'
    
selected_tournament=tk.StringVar()
tournament_list= [f.name for f in os.scandir('./games/game_def/') if f.is_dir()]
selected_match=tk.StringVar()

def select_match():
    #function to select a specific match
    global df_match
    global playerlist
    df_match=pd.read_csv('./games/game_def/'+selected_tournament.get()+'/'+cb_match.get())
    #print(df_match['Name'].tolist())
    playerlist=(df_match['Name'].to_list())
    selected_match.set(cb_match.get())
    player.set('')
    lbl_team.configure(text='Team')
    #gets the list of players from the data in the match and adds it to the combobox
    cb_player['values']=playerlist
    lbl_team['state']='normal'
    cb_player['state']='readonly'
    


match=tk.StringVar()

#makes so that only files with a specific extension are chosen
def list_files1(directory, extension):
    return (f for f in os.listdir(directory) if f.endswith(extension))
matchlist=list_files1('./games/game_def/', '.csv')

def player_team(event):
    #gets the currently selected players team from the combobox selection
    #this changes each time a new player is selected
    
    p_team=(df_match['Team'].to_list())
    p_team_index=playerlist.index(cb_player.get())
    team.set(p_team[p_team_index])
    player.set(cb_player.get())
    #enables the buttons 
    if len(team.get())>14: #if team name is too long use the last word in their name
        team_l=team.get().split(' ')
        lbl_team.configure(text=team_l[-1])
    else:
        team_l=team.get()
        lbl_team.configure(text=team_l)

    for c in range(rows*cols):
        button[c].config(state='normal',relief='raised')

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

cb_player=ttk.Combobox(selection_frame,value='',state='readonly') 
cb_player.bind('<<ComboboxSelected>>',player_team) #sets it so it registers a value when the combobox is changed
   
player=tk.StringVar()
team  =tk.StringVar()
team.set('Team')

lbl_select_player=tk.Label(selection_frame,text='Select player to analyse')
lbl_team    =tk.Label(selection_frame,text=team.get(),width=12,justify='left')

lbl_select_player.grid(row=3,column=0,pady=(10,2),sticky='w')
cb_player.grid(row=4,column=0,sticky='w',padx=(0,20))
lbl_team.grid(row=4,column=2,sticky='w')
cb_player['state']='disabled'
lbl_team         ['state']='disabled'

selection_frame.grid(row=0,column=1,rowspan=3,sticky='nsew')
coords=tk.StringVar()
button_num=tk.IntVar()
button=[]   
    
dataframe=pd.DataFrame()   
playername=0
#team='team'

def click(row, col,number):
    for c in range(rows*cols):
        button[c].config(bg="SystemButtonFace")
    label.configure(text=(row, col))          
    coords.set(label.cget('text'))
    button[number].config(bg='red')
    button_num.set(number)

    btn_goal.config(state='normal')
    btn_shot.config(state='normal')
    btn_pass.config(state='normal')
    btn_catch.config(state='normal')
    btn_tackle.config(state='normal')
    btn_block.config(state='normal')
    btn_drop.config(state='normal')
    
    btn_btr.config(state='normal')
    btn_skr.config(state='normal')
    
def add_attempt(method):
    global dataframe
    dataframe=dataframe.append({'name':player.get(),'team':team.get(),'event':method,'coords':coords.get()},ignore_index=True)
    button[button_num.get()].config(bg="SystemButtonFace")
    btn_goal.config(state='disabled')
    btn_shot.config(state='disabled')
    btn_pass.config(state='disabled')
    btn_catch.config(state='disabled')
    btn_tackle.config(state='disabled')
    btn_block.config(state='disabled')
    btn_drop.config(state='disabled')
    
    btn_btr.config(state='disabled')
    btn_skr.config(state='disabled')
    
    btn_remove.config(state='normal')
    btn_reset.config(state='normal')
    print(dataframe)
    lstbox_events.insert('end',(dataframe.tail(1).index.item()
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
    dataframe.iloc[0:0]
    lstbox_events.delete(0,'end')
def remove():
    #deletes selected item from the listbox and drops it from the dataframe
    try:
        vari=lstbox_events.get(lstbox_events.curselection())
        lstbox_events.delete(tk.ANCHOR)  
        dataframe.drop(index=vari[0],inplace=True)
    except:
        raise Exception("Currently can't remove some of the events in time, working on it")
    print(dataframe)
    
i=0    
for row in range(1,rows+1):
    for col in range(1,cols+1):
        button.append( tk.Button(pitch_frame, text='      ', 
                           command=lambda row=row,col=col,number=i:
                               click(row, col,number)))
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
for c in range(rows*cols):
        button[c].config(state='disabled',relief='groove')
label = tk.Label(root, text="")
#lbl_pitch_img.grid(row=0,column=0,rowspan=rows,columnspan=cols)

#label.grid(row=10, column=0, columnspan=10, sticky="new")
pitch_frame.grid(row=1,column=3,rowspan=10,sticky='nsew',pady=(20),padx=(2,0))

button_grid=tk.Frame(root)
btn_shot=tk.Button(button_grid,text='Goal attempt',width=12,command=lambda: add_attempt('shot'))
btn_goal=tk.Button(button_grid,text='Goal',width=12,command=lambda: add_attempt('goal'))
btn_pass=tk.Button(button_grid,text='Pass start',width=12,command=lambda:add_attempt('pass'))
btn_catch=tk.Button(button_grid,text='Catch',width=12,command=lambda:add_attempt('catch'))
btn_tackle=tk.Button(button_grid,text='Completed tackle',width=16,command=lambda:add_attempt('tackle'))
btn_block=tk.Button(button_grid,text='Block/interception',width=16+1,command=lambda:add_attempt('block'))
btn_drop=tk.Button(button_grid,text='Dropped pass',width=16,command=lambda:add_attempt('drop'))

btn_btr=tk.Button(button_grid,text='Beater engages beater',width=25,command=lambda:add_attempt('beater'))
btn_skr=tk.Button(button_grid,text='Snitch catch attempt',width=25,command=lambda:add_attempt('sk catch'))


btn_shot.grid(row=0,column=0,columnspan=3)
btn_goal.grid(row=0,column=3,columnspan=3)
btn_pass.grid(row=0,column=6,columnspan=3)
btn_catch.grid(row=0,column=9,columnspan=3)
btn_tackle.grid(row=1,column=0,columnspan=4)
btn_block.grid(row=1,column=4,columnspan=4)
btn_drop.grid(row=1,column=8,columnspan=4)

btn_btr.grid(row=2,column=0,columnspan=6,sticky='ew')
btn_skr.grid(row=2,column=6,columnspan=6,sticky='ew')

button_grid.grid(row=11,column=3,pady=(10,10))

#panel.grid(row=0,column=0,rowspan=rows,columnspan=cols,sticky='nsew')

#get the events stuff all together
evt_frame=tk.Frame(root)

lstbox_events=tk.Listbox(evt_frame,height=25,width=30)
scrl_evt=tk.Scrollbar(evt_frame) #scroll box
scrl_evt.configure(command=lstbox_events.yview)

scrl_x_evt=tk.Scrollbar(evt_frame,orient=tk.HORIZONTAL) #scroll box
scrl_x_evt.configure(command=lstbox_events.xview)
lstbox_events.configure(yscrollcommand=scrl_evt.set,xscrollcommand=scrl_x_evt.set)

btn_reset=tk.Button(evt_frame,text='Clear',width=15,command=clear)
btn_remove=tk.Button(evt_frame,text='Remove entry',width=15,command=remove)

lstbox_events.grid(row=0,column=30,rowspan=21,columnspan=3)
scrl_evt.grid(row=0,column=33,sticky='ns',rowspan=20)
scrl_x_evt.grid(row=21,column=30,sticky='ew',columnspan=3)
btn_remove.grid(row=22,column=30,columnspan=3,pady=(0,10))
btn_reset.grid(row=23,column=30,columnspan=3)


evt_frame.grid(row=1,column=4,rowspan=12,padx=(10,0))

#at the start disable everything
btn_remove.config(state='disabled')
btn_reset.config(state='disabled')

btn_goal.config(state='disabled')
btn_shot.config(state='disabled')
btn_pass.config(state='disabled')
btn_catch.config(state='disabled')
btn_tackle.config(state='disabled')
btn_block.config(state='disabled')
btn_drop.config(state='disabled')

btn_btr.config(state='disabled')
btn_skr.config(state='disabled')


def createPitch(color='black',pitch='full'): 
    # in meters
    # Code by @JPJ_dejong
    
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
        ax.set_facecolor('#94B560')
        #Pitch Outline & Centre Line
        plt.plot([0,0],[0,width], color=linecolor)
        plt.plot([0,length],[width,width], color=linecolor)
        plt.plot([length,length],[width,0], color=linecolor)
        plt.plot([length,0],[0,0], color=linecolor)
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
        raise Exception('Only acceptable keywords are "half" and "full"')
    #Tidy Axes
    
    plt.axis('off')
    #plt.show()
    
    return fig,ax



def save_data():
    match=selected_match.get().split('.')
    match=match[0]
    bar = ttk.Progressbar(button_grid, length=400)
    bar.grid(row=4,column=0,columnspan=40,sticky='ew')
    bar['value'] = 0
    it_length=len(dataframe)*2*6
    for kind in ['team','name']:
        for team in dataframe[kind].unique():
            if kind=='team':
                o_team=team
            graphs=[['shot','goal'],['pass','catch'],
                    ['block'],['drop'],['beater'],['sk catch']]
            for item in graphs:
                df=dataframe[dataframe.event.isin(item)].copy()
                if len(df.index)==0:
                    continue
                if graphs==['shot','goal']:
                    arr=np.zeros((33,30))
                    arr_goal=np.zeros((33,30))
                    
                else:
                    arr=np.zeros((33,60))
                    arr_goal=np.zeros((33,60))
                    arr_catch=np.zeros((33,60))
                if graphs==['pass','catch']:
                    arr_catch=np.zeros((33,60))
                for graph in ['heat','circle']:
                    if item==['shot','goal']:
                        
                        #(fig,ax)=createPitch(pitch='half') 
                        (fig,ax)=createPitch() 
                        pass
                        #creates the pitch image
                    else:
                        (fig,ax)=createPitch() 
                    #need to do this for each team, each player, each type of interaction
                    #for shots if a shot goes in it should be a different colour
                    for i,data in df.iterrows():
                        d2=data
                        data=data['coords'].split() #splits the coordinates into x and y
                        '''
                        if item==['shot','goal']:
                                if (int(data[-1])-(60/2))<0:
                                    data[-1]=abs(int(data[-1])-(60/2)+1)
                                else:
                                    data[-1]=int(data[-1])-(60/2)+1
                        '''
                        if graph=='circle':
                            print('x',data[0],type(data[0]))
                            print('y',data[-1],type(data[-1]))
                            
                            y=int(data[0])*33/15
                            x=int(data[-1])*60/30-0.5
                            
                            #makes the data look the same way you record it
                            if (y-33)<0:
                                y=abs(y-33)+1
                            else:
                                y=y-33+1
                            if d2['event']=='shot':
                                circle=plt.Circle((x,y),1,color='red',alpha=0.2)
                            elif d2['event']=='catch':
                                circle=plt.Circle((x,y),1,color='orange',alpha=0.2)
                            else:
                                circle=plt.Circle((x,y),1,color='blue',alpha=0.2) #adds circles of size 1 and alpha needs to be changed
                            plt.annotate(d2['name'],(x,y),size=25)
                            ax.add_patch(circle) #adds it to the graph
                        elif graph=='heat':
                            if d2['event']=='shot':
                                arr_goal[int(int(data[0])*33/15)-1][int(int(data[-1])*60/30)-1]+=1
                                arr[int(int(data[0])*33/15)-1][int(int(data[-1])*60/30)-1]+=1
                            elif d2['event']=='catch':
                                arr_catch[int(int(data[0])*33/15)-1][int(int(data[-1])*60/30)-1]+=1
                            else:
                                arr[int(int(data[0])*33/15)-1][int(int(data[-1])*60/30)-1]+=1
                        #print('row')
                        #print('x',x)
                        #print('y',y,'\n')
                        
                    
                    if graph=='heat':
                        if item==['shot','goal']:
                            plt.imshow(arr,cmap='winter',interpolation='spline16'
                                   ,alpha=0.5,extent=(0,60,0,33))
                            plt.imshow(arr_goal,cmap='plasma',interpolation='spline16'
                                   ,alpha=0.5,extent=(0,60,0,33))
                        elif item==['pass','catch']:
                            plt.imshow(arr,cmap='winter',interpolation='spline16'
                                   ,alpha=0.5,extent=(0,60,0,33))
                            plt.imshow(arr_catch,cmap='cividis',interpolation='spline16'
                                   ,alpha=0.5,extent=(0,60,0,33))
                        else:
                            plt.imshow(arr,cmap='hot',interpolation='spline16'
                                   ,alpha=0.5,extent=(0,60,0,33))
                    if kind=='team':
                        if os.path.exists('./graphs/'+selected_tournament.get()+'/'+match
                                    +'/'+team+'/')==False:
                            os.makedirs('./graphs/'+selected_tournament.get()+'/'+match
                                    +'/'+team+'/')
                        fig.savefig('./graphs/'+selected_tournament.get()+'/'+match
                                    +'/'+team+'/'+str(item[0])+'-'+graph+'.png', dpi=100) 
                    elif kind=='name':
                        if os.path.exists('./graphs/'+selected_tournament.get()+'/'+match
                                    +'/'+o_team+'/')==False:
                            os.makedirs('./graphs/'+selected_tournament.get()+'/'+match
                                    +'/'+o_team+'/')
                        fig.savefig('./graphs/'+selected_tournament.get()+'/'+match
                                    +'/'+o_team+'/'+team+str(item[0])+'-'+graph+'.png', dpi=100)
                    plt.show()
                    bar['value'] +=1/it_length
                    
    print('FINISHED!! :D')
    if os.path.exists('./graphs/'+selected_tournament.get()+'/')==False:
        os.makedirs('./graphs/'+selected_tournament.get()+'/')
    dataframe.to_csv('./graphs/'+selected_tournament.get()+'/'+selected_match.get())
    clear()
    bar.grid_forget()
draw_pitch=tk.Button(text='draw pitch',command=lambda: createPitch(pitch='half'))
#draw_pitch.grid(row=100,column=100)

save=tk.Button(text='Save',command=save_data)
save.grid(rows=10,columns=5)


root.mainloop()

#video for this
#https://www.youtube.com/watch?v=oOAnERLiN5U&list=PLedeYskZY0vBOdQ6Uc9eZjZ2-nz1JT3R7&index=6
#making a shot and pass map
#https://github.com/Friends-of-Tracking-Data-FoTD/SoccermaticsForPython/blob/master/7PassHeatMap.py 