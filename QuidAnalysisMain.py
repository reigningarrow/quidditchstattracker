# -*- coding: utf-8 -*-
"""
Created on Tue Sep  8 13:06:45 2020

@author: Sam
Program for recording quidditch stats using tkinter and pandas
"""

#TODO make main window-analysis window, add option to go to new window as a menu bar or button
#TODO if possible add video
#TODO add new window to view stats
#Potential TODO change save files to add to new tab instead of a new file every time

#add data to new tab
# import pandas as pd
# import numpy as np
# from openpyxl import load_workbook

# path = r"C:\Users\fedel\Desktop\excelData\PhD_data.xlsx"

# book = load_workbook(path)
# writer = pd.ExcelWriter(path, engine = 'openpyxl')
# writer.book = book

# x3 = np.random.randn(100, 2)
# df3 = pd.DataFrame(x3)

# x4 = np.random.randn(100, 2)
# df4 = pd.DataFrame(x4)

# df3.to_excel(writer, sheet_name = 'x3')
# df4.to_excel(writer, sheet_name = 'x4')
# writer.save()
# writer.close()


import tkinter as tk
import pandas as pd
import os 
import time   
import shutil   
from tkinter import messagebox 
from tkinter import ttk
from tkinter import filedialog

root=tk.Tk()
#sets root window basic info
root.iconbitmap('hoops_icon.ico')      #sets the window icon
root.title('Quidditch Analysis Alpha')  #sets window title       
root.geometry('470x690')  
    
#add a menu bar
main_menu=tk.Menu(root)
root.config(menu=main_menu)

#ensures that the folders exist
if os.path.exists('./games/')==False:
    os.mkdir('./games/') #creates folder
if os.path.exists('./games/game_def/')==False:
    #if there is no folder called games to store it, make one
    os.mkdir('./games/game_def/') #creates folder
if os.path.exists('./games/player/')==False:
    os.mkdir('./games/player/')
if os.path.exists('./games/team/')==False:
    os.mkdir('./games/team/')
if os.path.exists('./games/tournament/')==False:
    os.mkdir('./games/tournament/')
if os.path.exists('./games/season_results')==False:
    os.mkdir('./games/season_results') #creates folder


    

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

cb_tournament=ttk.Combobox(root,value=tournament_list,state='readonly',width=50)
btn_tournament=tk.Button(root,text='Select tournament',command=select_tournament)

btn_tournament.grid(row=0,column=1,sticky='e')
cb_tournament.grid(row=0,column=0,columnspan=2,sticky='w')

ttk.Style().configure('cb_tournament', relief='sunken')
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
    btn_select_player['state']='normal'
    lbl_team['state']='normal'
    opt_position['state']='normal'
    cb_player['state']='readonly'

infoframe=tk.Frame(root)
match=tk.StringVar()

#makes so that only files with a specific extension are chosen
def list_files1(directory, extension):
    return (f for f in os.listdir(directory) if f.endswith(extension))
matchlist=list_files1('./games/game_def/', '.csv')

cb_match=ttk.Combobox(infoframe,value='',state='readonly',width=55)
cb_match['state']='disabled'
#creates widgets
lbl_select_match=tk.Label(infoframe,text='Choose match')
btn_choose_match=tk.Button(infoframe,text='Select Match',width=12,command=select_match)

lbl_select_match.grid(row=0,column=0,columnspan=4)
btn_choose_match.grid(row=1,column=3)
cb_match.        grid(row=1,column=0,columnspan=3,sticky='w')


#select player
selected_player=tk.StringVar()
selected_team=tk.StringVar()
selected_pos=tk.StringVar()
def select_player():
    #resets all values to 0
    goals_allowed.set(0)
    chaser_data.fromkeys(chaser_data,0)
    beater_data.fromkeys(beater_data,0)
    seeker_data.fromkeys(seeker_data,0)
    cards.fromkeys(cards,0)
    pitchtime.set(0)
    gamespeed.set(cb_gamespeed.get())
    cb_gamespeed['state']='disabled'
    #removes frames
    chaserframe.grid_forget()
    beaterframe.grid_forget()
    seekerframe.grid_forget()
    #displays relevant frame
    
    try:
    #sets the selected player
        p_team=(df_match['Team'].to_list())
        p_team_index=playerlist.index(cb_player.get())
        selected_player.set(cb_player.get())
        selected_team.set(p_team[p_team_index])
        selected_pos.set(pos.get())
        #depending on the position show relevant buttons
        if pos.get()=='Keeper/Chaser' or pos.get()=='Chaser':
            chaserframe.grid(row=6,column=0,columnspan=3, pady=(5,0))
        elif pos.get()=='Beater':
            beaterframe.grid(row=6,column=0,columnspan=3, pady=(5,0))
            btn_bt_sop.grid(row=4,column=0,columnspan=12,pady=(20,0))

        elif pos.get()=='Seeker':
            seekerframe.grid(row=6,column=0,columnspan=3, pady=(5,0))
            btn_goal_allowed['state']='disabled'
            
        #checks that user has entered a valid option before enabling buttons    
        if pos.get() in ['Keeper/Chaser','Chaser','Beater','Seeker']:
            for child in cardframe.winfo_children():
                child.configure(state='normal')
                btn_on_pitch['state']='normal'        
        btn_off_pitch['state']='disabled'
        btn_goal_allowed['state']='disabled'
        btn_save_results['state']='normal'
        btn_on_pitch['state']='normal'

    except:
        messagebox.showerror('Error Occured','An error has occured when trying to select a player')
def player_team(event):
    #gets the currently selected players team from the combobox selection
    #this changes each time a new player is selected
    try:
        p_team=(df_match['Team'].to_list())
        p_team_index=playerlist.index(cb_player.get())
        team.set(p_team[p_team_index])
        #enables the buttons 
        if len(team.get())>14: #if team name is too long use the last word in their name
            team_l=team.get().split(' ')
            lbl_team.configure(text=team_l[-1])
        else:
            team_l=team.get()
            lbl_team.configure(text=team_l)
        opt_position['state']='normal'
        opt_position.config(bg='white')

    except:
        messagebox.showerror('Error Occured','An error has occured when trying to select a player')

cb_player=ttk.Combobox(infoframe,value='',state='readonly') 
cb_player.bind('<<ComboboxSelected>>',player_team) #sets it so it registers a value when the combobox is changed
pos=tk.StringVar()     
player=tk.StringVar()
team  =tk.StringVar()
team.set('Team')
poslist=['Keeper/Chaser','Chaser','Beater','Seeker']
pos.set(poslist[0])
lbl_select_player=tk.Label(infoframe,text='Select player to analyse')
btn_select_player=tk.Button(infoframe,text='Select Player',command=select_player,width=12)
opt_position=tk.OptionMenu(infoframe,pos,*poslist)
lbl_team    =tk.Label(infoframe,text=team.get(),width=12,justify='left')

opt_position.config(relief=tk.GROOVE,width=12,justify='left')

lbl_select_player.grid(row=3,column=0,pady=(10,2),sticky='w')
cb_player.grid(row=4,column=0,sticky='w',padx=(0,20))
btn_select_player.grid(row=4,column=3,sticky='w')
opt_position.grid(row=4,column=1,sticky='w')
lbl_team.grid(row=4,column=2,sticky='w')
cb_player['state']='disabled'
btn_select_player['state']='disabled'
opt_position     ['state']='disabled'
lbl_team         ['state']='disabled'

pitchtime=tk.IntVar()
speeds=[0.25,0.5,0.75,1,1.25,1.5,1.75,2]
gamespeed=tk.DoubleVar()
lbl_gamespeed=tk.Label(infoframe,text='Game speed: ')
cb_gamespeed=ttk.Combobox(infoframe,value=speeds,width=5)
cb_gamespeed.current(3)

lbl_gamespeed.grid(row=3,column=2,pady=(10,2))
cb_gamespeed.grid(row=3,column=3,pady=(10,2))
def pitch_time(startstop):
    #gets the amount of time a player is on pitch.
    #if start start timer -time.time() is due to calculating the total time elapsed later
    if startstop=='start':
        #starts timer
        pitchtime.set(pitchtime.get()-time.time())
        #disabled buttons to get rid of potential errors
        btn_off_pitch['state']='normal'
        btn_on_pitch['state']='disabled'
        btn_goal_allowed['state']='normal'
        btn_reset['state']='disabled'
        btn_save_results['state']='disabled'
        
        for child in cardframe.winfo_children():
            child.configure(state='disable')
        btn_goal_allowed['state']='normal'

        #turns relevant buttons on or off
        if pos.get()=='Keeper/Chaser' or pos.get()=='Chaser':
            for child in chaserframe.winfo_children():
                child.configure(state='normal')

        elif pos.get()=='Beater':             
            for child in beaterframe.winfo_children():
                child.configure(state='normal')
            if beater_data['control gained']>beater_data['control lost']:
                timers('control gained')
            else:
                btn_bt_ctrl_lost['state']='disabled'
                btn_bt_nb_gn['state']='disabled'
            if beater_data['bubble created']>beater_data['bubble lost']:
                timers('bubble created')
            if snitch_on.get()==1:
                #if snitch is on pitch start snitch timer
                timers('snitch on')
                btn_bt_snitch_catch['state']='disabled'

            elif snitch_on.get()==0:
                #if snitch isnt on pitch make sure the buttons are removed
                btn_bt_snitch_catch.grid_forget()
                btn_bt_bubble_broken.grid_forget()
                btn_bt_bubble_created.grid_forget()
                btn_bt_bubble_lost.grid_forget()
        elif pos.get()=='Seeker':

            for child in seekerframe.winfo_children():
                child.configure(state='normal')
            btn_sk_catch['state']='disabled'
            btn_goal_allowed['state']='disabled'
            btn_sk_atk_stp['state']='disabled'        
            btn_sk_def_stp['state']='disabled'
            #restarts seeker timers if applicable
            if seeker_atk.get()==1:
                timers('attack')
                seeker_atk.set(1)
            elif seeker_def.get()==1:
                timers('def')


    if startstop=='stop':
        pitchtime.set(pitchtime.get()+time.time())
        btn_off_pitch['state']='disabled'
        btn_on_pitch['state']='normal'
        btn_goal_allowed['state']='disabled'
        btn_reset['state']='normal'
        btn_save_results['state']='normal'
        for child in cardframe.winfo_children():
            child.configure(state='normal')
        btn_goal_allowed['state']='disabled'
        if pos.get()=='Keeper/Chaser' or pos.get()=='Chaser':
            for child in chaserframe.winfo_children():
                child.configure(state='disabled')
            
        elif pos.get()=='Beater':
            if beater_data['control gained']>beater_data['control lost']:
                    timers('control lost')
            if beater_data['bubble created']>beater_data['bubble lost']:
                timers('bubble lost')
            for child in beaterframe.winfo_children():
                child.configure(state='disabled')
            if snitch_on.get()==1:
                timers('snitch off')
                btn_bt_snitch_catch['state']='normal'



        elif pos.get()=='Seeker':
            #stops seeker timers
            if seeker_atk.get()==1:
                timers('attack stop')
                seeker_atk.set(1)
            elif seeker_def.get()==1:
                timers('def stop')
                seeker_def.set(1)
            for child in seekerframe.winfo_children():                
                child.configure(state='disabled')
            btn_sk_catch['state']='normal'



infoframe.grid(row=2,column=0,columnspan=3)
#on pitch off pitch
btn_on_pitch =tk.Button(root,text='On pitch/Brooms up',width=28,command=lambda: pitch_time('start'))
btn_off_pitch=tk.Button(root,text='Off pitch/Brooms down',width=28,command=lambda: pitch_time('stop'))
#makes sure you can't press anything when no player is selected
btn_off_pitch['state']='disabled'
btn_on_pitch['state'] ='disabled'


btn_on_pitch.grid(row=5,column=0,pady=(10,0))
btn_off_pitch.grid(row=5,column=1,pady=(10,0))

chaserframe=tk.Frame(root,borderwidth=1)

#creates a dictionary of values of info to be gathered
chaser_data={'drive goal':0,'drive attempt':0,'completed drive percent':0,'shot percent':0,'shot goal':0,'shot target':0,'shot miss':0,
             'shot attempt':0,'assist':0,'short pass percent':0,'short pass complete':0,'short pass miss':0,'short pass':0,
             'long pass percent':0,'long pass complete':0,'long pass miss':0,'long pass':0,'catch percent':0,'catch-':0,'drop catch':0,'targeted':0,
             'broken tackle':0,'block':0,
             'intercept':0,'completed tackle':0,'partial tackle':0,'turnover forced':0}
#dictionary of extra stuff that didnt need buttons
chaser_extra={'shot goal':'shot attempt','shot target':'shot attempt',
              'shot miss':'shot attempt','short pass complete':'short pass','short pass miss':'short pass',
              'long pass complete':'long pass','long pass miss':'long pass','catch-':'targeted','drop catch':'targeted'} 


def add_value(name):
    #adds values to the chaser data
    chaser_data[name]=chaser_data[name]+1
    if name in chaser_extra:
       chaser_data[chaser_extra[name]]= chaser_data[chaser_extra[name]]+1

#creates buttons and labels for chaser frame
button_width=30
lbl_ch_offence      =tk.Label(chaserframe,text='Offence')
btn_ch_drive_goal   =tk.Button(chaserframe,text='Drive goal',width=int(button_width/2+2),command=lambda: add_value('drive goal'))
btn_ch_drive_attempt=tk.Button(chaserframe,text='Drive attempt',width=int(button_width/2+2),command=lambda: add_value('drive attempt'))
btn_ch_shot_goal    =tk.Button(chaserframe,text='Shot goal',width=int(button_width/3+1),command=lambda: add_value('shot goal'))
btn_ch_shot_tgt     =tk.Button(chaserframe,text='Shot on target',width=int(button_width/3+1),command=lambda:add_value('shot target'))
btn_ch_shot_miss    =tk.Button(chaserframe,text='Shot miss',width=int(button_width/3+1),command=lambda:add_value('shot miss'))
btn_ch_assist       =tk.Button(chaserframe,text='Assist',width=button_width+6,command=lambda:add_value('assist'))
btn_ch_s_pass_cpt   =tk.Button(chaserframe,text= 'Short pass completed',width=int(button_width/2+2),command=lambda:add_value('short pass complete'))
btn_ch_s_pass_miss  =tk.Button(chaserframe,text='Short pass missed',width=int(button_width/2+2),command=lambda:add_value('short pass miss'))
btn_ch_l_pass_cpt   =tk.Button(chaserframe,text='Long pass complete',width=int(button_width/2+2),command=lambda:add_value('long pass complete'))
btn_ch_l_pass_miss  =tk.Button(chaserframe,text='Long pass missed',width=int(button_width/2+2),command=lambda:add_value('long pass miss'))
btn_ch_catch        =tk.Button(chaserframe,text='Catch',width=int(button_width/2+2),command=lambda:add_value('catch-'))
btn_ch_drp_catch    =tk.Button(chaserframe,text='Drop catch',width=int(button_width/2+2),command=lambda:add_value('drop catch'))
btn_ch_brk_tkl      =tk.Button(chaserframe,text='Broken tackle',width=button_width+6,command=lambda:add_value('broken tackle'))
lbl_ch_defence      =tk.Label(chaserframe,text='Defence')
btn_ch_pass_blk     =tk.Button(chaserframe,text='Pass/Shot block',width=int(button_width/2+2),command=lambda:add_value('block'))
btn_ch_intercept    =tk.Button(chaserframe,text='Interception',width=int(button_width/2+2),command=lambda:add_value('intercept'))
btn_ch_tackle_cpt   =tk.Button(chaserframe,text='Full tackle',width=int(button_width/2+2),command=lambda:add_value('completed tackle'))
btn_ch_tackle_ptl   =tk.Button(chaserframe,text='Partial tackle',width=int(button_width/2+2),command=lambda:add_value('partial tackle'))
btn_ch_turnover_fcd =tk.Button(chaserframe,text='Turnover forced',width=button_width+6,command=lambda:add_value('turnover forced'))

#adds buttons to frame 
lbl_ch_offence.grid(row=0,column=0,columnspan=12)
btn_ch_drive_goal.grid(row=1,column=0,columnspan=6)
btn_ch_drive_attempt.grid(row=1,column=6,columnspan=6)
btn_ch_shot_goal.grid(row=2,column=0,columnspan=4)
btn_ch_shot_miss.grid(row=2,column=4,columnspan=4)
btn_ch_shot_tgt.grid(row=2,column=8,columnspan=4)
btn_ch_assist.grid(row=3,column=0,columnspan=12)
btn_ch_s_pass_cpt.grid(row=4,column=0,columnspan=6)
btn_ch_s_pass_miss.grid(row=4,column=6,columnspan=6)
btn_ch_l_pass_cpt.grid(row=5,column=0,columnspan=6)
btn_ch_l_pass_miss.grid(row=5,column=6,columnspan=6)
btn_ch_catch.grid(row=6,column=0,columnspan=6)
btn_ch_drp_catch.grid(row=6,column=6,columnspan=6)
btn_ch_brk_tkl.grid(row=7,column=0,columnspan=12)

lbl_ch_defence.grid(row=8,column=0,columnspan=12,pady=(5,0))
btn_ch_pass_blk.grid(row=9,column=0,columnspan=6)
btn_ch_intercept.grid(row=9,column=6,columnspan=6)
btn_ch_tackle_cpt.grid(row=10,column=0,columnspan=6)
btn_ch_tackle_ptl.grid(row=10,column=6,columnspan=6)
btn_ch_turnover_fcd.grid(row=11,column=0,columnspan=12)

#chaserframe.grid(row=5,column=0,columnspan=3, pady=(20,0))
#beater data
beaterframe=tk.Frame(root)
beater_data={'control gained':0,'control lost':0,'control time':0,'control percent':0,
             'no bludgers forced':0,'no bludgers own':0,'forced pass':0,'forced turnover':0,
             'team goal':0,'shot block':0,'catch':0,'snitch catch':0,'bubble created':0,
             'bubble broken':0,'bubble lost':0,'bubble duration':0,'bubble percent':0}

def bt_add_value(name):
    beater_data[name]=beater_data[name]+1
    try:
        timers(name)
    except:
        pass
    if name=='snitch catch':
        #set snitch on to 0
        #as brooms down bubble timer already stopped        
        snitch_on.set(0)
        #disable buttons once snitch is caught
        btn_bt_bubble_broken['state']='disabled'
        btn_bt_bubble_created['state']='disabled'
        btn_bt_bubble_lost['state']='disabled'
        btn_bt_snitch_catch['state']='disabled'


snitch_on=tk.IntVar()    
def sop():
    snitch_on.set(1)
    #for when snitch is on pitch
    #puts snitch on pitch buttons on screen
    btn_bt_snitch_catch.grid(row=5,column=0,columnspan=12)
    btn_bt_bubble_created.grid(row=4,column=0,columnspan=4,pady=(20,0))
    btn_bt_bubble_broken.grid(row=4,column=4,columnspan=4,pady=(20,0))
    btn_bt_bubble_lost.grid(row=4,column=8,columnspan=4,pady=(20,0))
    #removes snitch button
    btn_bt_sop.grid_forget()
    #makes it so that you can't start lose a bubble before snitch is on pitch
    btn_bt_bubble_lost['state']='disabled'
    btn_bt_snitch_catch['state']='disabled'
    #starts snitch timer
    timers('snitch on')
#adds beater buttons
btn_bt_ctrl_gain=tk.Button(beaterframe,text='Control gained',width=int(button_width/2+2),command=lambda: bt_add_value('control gained'))
btn_bt_ctrl_lost=tk.Button(beaterframe,text='Control lost',  width=int(button_width/2+2),command=lambda: bt_add_value('control lost'))
btn_bt_nb_gn    =tk.Button(beaterframe,text='No bludger forced',width=int(button_width/2+2),command=lambda: bt_add_value('no bludgers forced'))
btn_bt_nb_lst   =tk.Button(beaterframe,text='No bludgers (own)',width=int(button_width/2+2),command=lambda: bt_add_value('no bludgers own'))
btn_bt_fc_pass  =tk.Button(beaterframe,text='Pass forced',width=int(button_width/2+2),command=lambda: bt_add_value('forced pass'))
btn_bt_fc_turn  =tk.Button(beaterframe,text='Force turnover',width=int(button_width/2+2),command=lambda: bt_add_value('forced turnover'))
btn_bt_shot_block=tk.Button(beaterframe,text='shot/pass block',width=int(button_width/2+2),command=lambda: bt_add_value('shot block'))
btn_bt_catch     =tk.Button(beaterframe,text='Bludger catch',width=int(button_width/2+2),command=lambda: bt_add_value('catch'))
btn_bt_snitch_catch=tk.Button(beaterframe,text='Snitch catch',width=button_width+6,command=lambda: bt_add_value('snitch catch'))
btn_bt_bubble_created=tk.Button(beaterframe,text='Bubble created',width=int(button_width/3+1),command=lambda: bt_add_value('bubble created'))
btn_bt_bubble_broken=tk.Button(beaterframe,text='Bubble broken',width=int(button_width/3+1),command=lambda: bt_add_value('bubble broken'))
btn_bt_bubble_lost=tk.Button(beaterframe,text='Bubble lost',width=int(button_width/3+1),command=lambda: bt_add_value('bubble lost'))

btn_bt_team_goal=tk.Button(beaterframe,text='Team goal',width=button_width+6,command=lambda: bt_add_value('team goal'))
btn_bt_sop=tk.Button(beaterframe,text='Snitch on Pitch',width=button_width+6,command=sop)

btn_bt_ctrl_gain.grid(row=0,column=0,columnspan=6)
btn_bt_ctrl_lost.grid(row=0,column=6,columnspan=6)
btn_bt_nb_gn.grid(row=1,column=0,columnspan=6)
btn_bt_nb_lst.grid(row=1,column=6,columnspan=6)
btn_bt_fc_pass.grid(row=2,column=0,columnspan=6)
btn_bt_fc_turn.grid(row=2,column=6,columnspan=6)
btn_bt_shot_block.grid(row=3,column=0,columnspan=6)
btn_bt_catch.grid(row=3,column=6,columnspan=6)

btn_bt_team_goal.grid(row=6,column=0,columnspan=12,pady=(10,0))
btn_bt_sop.grid(row=4,column=0,columnspan=12,pady=(20,0))

#beaterframe.grid(row=10,column=0,columnspan=3)

#seekerframe
seekerframe=tk.Frame(root)
seeker_data={'time attacking':0,'time defending':0,'catch attempt':0,'snitch catch':0}
seeker_atk=tk.IntVar()
seeker_def=tk.IntVar()
seeker_atk.set(5)
seeker_def.set(5)
snitch_time=tk.IntVar()
def sk_add_value(name):
    #function for adding to the seeker stats
    seeker_data[name]=seeker_data[name]+1
    if seeker_data[name]=='snitch catch':
        seeker_data['catch_attempt']=seeker_data['catch_attempt']+1
def timers(timer):
    #function for allowing the measure of durations
    if timer=='attack':
        seeker_data['time attacking']=seeker_data['time attacking']-time.time()  
        btn_sk_atk_stp['state']='normal'        
        btn_sk_atk['state']='disabled'
        btn_sk_def_stp['state']='disabled'
        btn_sk_def['state']    ='disabled'

        seeker_atk.set(1)
    elif timer=='attack stop':
        seeker_data['time attacking']=time.time()+seeker_data['time attacking']
        btn_sk_atk_stp['state']='disabled'        
        btn_sk_atk['state']    ='normal'
        btn_sk_def_stp['state']='disabled'
        btn_sk_def['state']    ='normal'

        seeker_atk.set(0)
    if timer=='def':
        seeker_data['time defending']=seeker_data['time defending']-time.time()
        btn_sk_def_stp['state']='normal'
        btn_sk_def['state']    ='disabled'
        btn_sk_atk_stp['state']='disabled'        
        btn_sk_atk['state']='disabled'

        seeker_def.set(1)
    elif timer=='def stop':
        seeker_data['time defending']=seeker_data['time defending']+time.time()
        btn_sk_def_stp['state']='disabled'
        btn_sk_def['state']    ='normal'
        btn_sk_atk_stp['state']='disabled'      
        btn_sk_atk['state']='normal'

        seeker_def.set(0)
    #beater timer things
    elif timer=='control gained':
        #if control gained start timer and disable the gained button
        beater_data['control time']=beater_data['control time']-time.time()
        btn_bt_ctrl_gain['state']='disabled'
        btn_bt_ctrl_lost['state']='normal'
        btn_bt_nb_gn['state']='normal'
        btn_bt_nb_lst['state']='disabled'
    elif timer=='control lost':
        beater_data['control time']=beater_data['control time']+time.time()
        btn_bt_ctrl_gain['state']='normal'
        btn_bt_ctrl_lost['state']='disabled'
        btn_bt_nb_gn['state']='disabled'
        btn_bt_nb_lst['state']='normal'

    elif timer=='bubble created':
        beater_data['bubble duration']=beater_data['bubble duration']-time.time()
        btn_bt_bubble_created['state']='disabled'
        btn_bt_bubble_lost['state']='normal'
        btn_bt_bubble_broken['state']='disabled'
    elif timer=='bubble lost':
        beater_data['bubble duration']=beater_data['bubble duration']+time.time()
        btn_bt_bubble_created['state']='normal'
        btn_bt_bubble_lost['state']='disabled'
        btn_bt_bubble_broken['state']='normal'
    elif timer=='snitch on':
        snitch_time.set(snitch_time.get()-time.time())
    elif timer=='snitch off':
        snitch_time.set(snitch_time.get()+time.time())
    
#snitch buttons
btn_sk_atk    =tk.Button(seekerframe,text='Attack start',width=int(button_width/2+2),command=lambda: timers('attack'))
btn_sk_atk_stp=tk.Button(seekerframe,text='Attack stop',width=int(button_width/2+2),command=lambda:timers('attack stop'))
btn_sk_def    =tk.Button(seekerframe,text='Defence start',width=int(button_width/2+2),command=lambda: timers('def'))
btn_sk_def_stp=tk.Button(seekerframe,text='Defence stop',width=int(button_width/2+2),command=lambda: timers('def stop'))
btn_sk_attempt=tk.Button(seekerframe,text='Catch attempt',width=int(button_width/2+2),command=lambda:sk_add_value('catch attempt'))
btn_sk_catch  =tk.Button(seekerframe,text='Snitch catch',width=int(button_width/2+2),command=lambda:sk_add_value('snitch catch'))

btn_sk_atk.grid(row=0,column=0)
btn_sk_atk_stp.grid(row=0,column=1)
btn_sk_def.grid(row=1,column=0)
btn_sk_def_stp.grid(row=1,column=1)
btn_sk_attempt.grid(row=2,column=0)
btn_sk_catch.grid(row=2,column=1)


btn_sk_atk_stp['state']='disabled'        
btn_sk_def_stp['state']='disabled'

#bt_turnover=tk.StringVar()
#create frame for cards
cardframe=tk.Frame(root)
cards={'blue':0,'yellow':0,'red':0}
def card_fn(data):
    cards[data]=cards[data]+1
    if selected_pos.get()=='Beater':
        bt_turnover=0
        #if beater and they have control do they turn over control with the card?
        if beater_data['control gained']>beater_data['control lost']:
            bt_turnover=(messagebox.askyesno('Bludger Turnover','Is there a bludger turnover?'))
        if bt_turnover==1:
            beater_data['control lost']=beater_data['control lost']+1
    #if getting the card would lead to a double yellow, make it a red card        
    if cards['yellow']==2:
        cards['red']=1
    #if player gets a red card they're out of the game
    if cards['red']==1:
        for child in cardframe.winfo_children():
            child.configure(state='disable')
        btn_on_pitch['state']='disabled'

goals_allowed=tk.IntVar()
def goals():
    goals_allowed.set(goals_allowed.get()+1)
    
#add buttons for cardsframe
btn_blue_cd=tk.Button(cardframe,text='Blue card',width=int(button_width/3+1),command=lambda: card_fn('blue'))
btn_yellow_cd=tk.Button(cardframe,text='Yellow card',width=int(button_width/3+1),command=lambda: card_fn('yellow'))
btn_red_cd=tk.Button(cardframe,text='Red card',width=int(button_width/3+1),command=lambda: card_fn('red'))

btn_goal_allowed=tk.Button(cardframe,text='Goal allowed',width=button_width+6,command=goals)
btn_goal_allowed['state']='disabled'
#place buttons in frame
btn_goal_allowed.grid(row=0,column=0,columnspan=3)
btn_blue_cd.grid(row=1,column=0)
btn_yellow_cd.grid(row=1,column=1)
btn_red_cd.grid(row=1,column=2)

cardframe.grid(row=10,column=0,columnspan=4,pady=(20,0))
#disables buttons at the start
frames=[chaserframe,beaterframe,seekerframe,cardframe]
for frame in frames:
    for child in frame.winfo_children():
        child.configure(state='disable')

def score(data,position):
    #calculates the score for the game
    score=0
    if position=='Keeper/Chaser' or position=='Chaser':
        score=(data['drive goal']+data['shot goal']-0.1*data['shot miss']
                -0.1*(data['drive attempt']-data['drive goal'])+0.2*data['shot target']
                +0.5*data['assist']+0.2*data['short pass complete']-0.05*data['short pass miss']
                +0.3*data['long pass complete']-0.1*data['long pass miss']
                +0.1*data['catch-']-0.05*data['drop catch']+0.05*data['broken tackle']
                +0.05*data['block']+0.8*data['intercept']+0.8*data['turnover forced']
                +0.5*data['completed tackle']+0.25*data['partial tackle'])
        if data['drive attempt']>0:
            if data['completed drive percent']>0.75:
                score+=2.5
            elif data['completed drive percent']<0.3:
                score+=-2
        if data['shot attempt']>0:
            if data['shot percent']>0.75:
                score+=2.5
            elif data['shot percent']<0.3:
                score+=-2
        if data['short pass']>0:
            if data['short pass percent']>0.75:
                score+=2
            elif data['short pass percent']<0.3:
                score+=-1.
        if data['long pass']>0:
            if data['long pass percent']>0.75:
                score+=4
            elif data['long pass percent']<0.3:
                score+=-2.

        if data['targeted']>0:
            if data['catch percent']>0.75:
                score+=2
            elif data['catch percent']<0.3:
                score+=-1.5
            
    if position=='Beater':
        score=(0.5*data['control gained']-0.4*data['control lost']
               +2*data['no bludgers forced']-1.5*data['no bludgers own']
               +1*data['forced pass']+2*data['forced turnover']
               +0.8*data['team goal']+0.25*data['shot block']+1.3*data['catch']
               +5*data['snitch catch']+2*data['bubble broken'])
        #adds a different score per 10 percent interval of control
        if data['control percent']>0.6:
            #each digit corresponds to a score if the thing in the max equals an interval of 10%
            score += int('0467899'[max(int(data['control percent'])//10-5,0)])
        elif data['control percent']<0.4:
            score += -1*int('543200'[max(int(data['control percent'])//10-5,0)])
        if data['bubble percent']>0.6:
            score += int('0235999'[max(int(data['bubble percent'])//10-5,0)])
        elif data['bubble percent']<0.4:
            score += -1*int('752100'[max(int(data['bubble percent'])//10-5,0)])
            
    if position=='Seeker':
        score=(500/data['time attacking']+0.01*data['time defending']
               +2*data['catch attempt']+10*data['snitch catch'])  

    #calculates negative points for cards        
    score+=-1.5*data['blue']-0.5*data['goals allowed']
    if data['red']==1 and data['yellow']==2:
         score+=-5*data['red']
    else:
         score+=-3*data['yellow']-5*data['red']
    return(score)

def create_summary(directory,group_cols):
    #creates a summarised total
    matchlist=list(list_files1(directory, '.xlsx'))
    #basically so the totals doesn't keep getting added each time
    df_match=pd.DataFrame()
    if 'Totals.xlsx' in matchlist: 
        matchlist.remove('Totals.xlsx')
    for match in matchlist:
        #append all the data from each match to a dataframe
        df_match=df_match.append(pd.read_excel(directory+match).to_dict('records'))
    df_all=pd.DataFrame(df_match)
    #groups the dataframes
    try:
        cols_agg={'Score':'sum','Effectiveness':'sum','Pitch Time':'sum','drive goal':'sum','drive attempt':'sum','completed drive percent':'mean',
          'shot percent':'mean','shot goal':'sum','shot target':'sum','shot miss':'sum',
             'shot attempt':'sum','assist':'sum','short pass percent':'mean','short pass complete':'sum','short pass miss':'sum','short pass':'sum',
             'long pass percent':'mean','long pass complete':'sum','long pass miss':'sum','long pass':'sum',
             'catch percent':'mean','catch-':'sum','drop catch':'sum','targeted':'sum','broken tackle':'sum','block':'sum',
             'intercept':'sum','completed tackle':'sum','partial tackle':'sum','turnover forced':'sum',
             'control gained':'sum','control lost':'sum','control percent':'mean',
             'no bludgers forced':'sum','no bludgers own':'sum','forced pass':'sum','forced turnover':'sum',
             'team goal':'sum','shot block':'sum','catch':'sum','snitch catch':'sum','bubble created':'sum',
             'bubble broken':'sum','bubble lost':'sum','bubble percent':'mean',
             'time attacking':'sum','time defending':'sum','catch attempt':'sum','snitch catch':'sum',
             'blue':'sum','yellow':'sum','red':'sum'}
        df_summary=df_all.groupby(group_cols).agg(cols_agg)
    except:
        df_summary=df_all.groupby(group_cols).sum()
        
    df_avg=df_all.groupby(group_cols).mean()
    #df_summary.to_excel(directory+'Totals.xlsx',index=True)
    with pd.ExcelWriter(directory+'Totals.xlsx') as writer:  
        df_summary.to_excel(writer, sheet_name='Totals',index=True)
        df_avg.to_excel    (writer, sheet_name='Averages',index=True)

    
    
def save():
    #adds the data to the dataframe and resets variables
    #add try statement to save
    cb_gamespeed['state']='normal'
    tot_pitchtime=pitchtime.get()*gamespeed.get()
    
    initial_data={'Name':selected_player.get(),'Team':selected_team.get(),
                  'Position':selected_pos.get(),'Score':0,'Effectiveness':0,
                  'Pitch Time':tot_pitchtime}

    if selected_pos.get()=='Keeper/Chaser' or selected_pos.get()=='Chaser':
        if chaser_data['drive attempt']>0:
            chaser_data['completed drive percent']=round((chaser_data['drive goal']/chaser_data['drive attempt'])*100,2)
        if chaser_data['shot attempt']>0:
            chaser_data['shot percent']=round((chaser_data['shot goal']/chaser_data['shot attempt'])*100,2)
        if chaser_data['short pass']>0:
            chaser_data['short pass percent']=round((chaser_data['short pass complete']/chaser_data['short pass'])*100,2)
        if chaser_data['long pass']>0:
            chaser_data['long pass percent']=round((chaser_data['long pass complete']/chaser_data['long pass'])*100,2)
        if chaser_data['targeted']>0:
            chaser_data['catch percent']=round((chaser_data['catch-']/chaser_data['targeted'])*100,2)
        
        data={**initial_data,**chaser_data,**cards}
    elif selected_pos.get()=='Beater':
        data={**initial_data,**beater_data,**cards}
        data['control percent']=round(((data['control time']*gamespeed.get())/data['Pitch Time'])*100,2)
        if data['control percent']>100: #just incase this happens ensures 100% is the max value
            data['control percent']=100
        if snitch_time.get()>0: #if they were on pitch during snitch on pitch
            data['bubble percent']=round(((data['bubble duration']*gamespeed.get())/(snitch_time.get()*gamespeed.get()))*100,2)
            if data['bubble percent']>100:
                data['bubble percent']=100
        #we dont need these now so delete them        
        del data['control time']
        del data['bubble duration']
        
    elif selected_pos.get()=='Seeker':
        seeker_data['time attacking']=seeker_data['time attacking']*gamespeed.get()
        seeker_data['time defending']=seeker_data['time defending']*gamespeed.get()
        data={**initial_data,**seeker_data,**cards}
        
    data['goals allowed']=goals_allowed.get()
    data['Score']=round(score(data,selected_pos.get()),2)
    data['Effectiveness']=round(data['Score']/data['Pitch Time'],3)
    data['Pitch Time']= time.strftime("%M:%S", time.gmtime(pitchtime.get()*gamespeed.get()))
    if data['Position']=='Seeker':
        #changes times to be understandable, but turns it into a s
        data['time attacking']= time.strftime("%M:%S", time.gmtime(data['time attacking']*gamespeed.get()))
        data['time defending']= time.strftime("%M:%S", time.gmtime(data['time defending']*gamespeed.get()))

    game=selected_match.get().split('.')
    game=game[0]
    #save game to tournament directory
    if os.path.exists('./games/tournament/'+selected_tournament.get()+'/')==False:
        os.mkdir('./games/tournament/'+selected_tournament.get()+'/')

    if os.path.isfile('./games/tournament/'+selected_tournament.get()+'/'+game+'.xlsx')==True:
        #changes the dataframe into a list of dictionaries
        main_data=pd.read_excel('./games/tournament/'+selected_tournament.get()+'/'+game+'.xlsx').to_dict('records')
        main_data.append(data)
    else:
        main_data=[]
        main_data.append(data)
    match_df=pd.DataFrame(main_data)
    match_df.to_excel('./games/tournament/'+selected_tournament.get()+'/'+game+'.xlsx',index=False)
    teams=selected_match.get().split('_')
    if teams[0]==selected_team.get():
        team_against=teams[2]
    else:
        team_against=teams[0]
    create_summary('./games/tournament/'+selected_tournament.get()+'/', ['Name','Team','Position'])
   
    #save to player directory
    player_data={'Tournament':selected_tournament.get(),'Team against':team_against}
    
    #combines all the stats into one dictionary
    player_data={**player_data,**data}
    team_data=player_data.copy()
    del player_data['Name'] #the file about the player doesn't need their name every time
    player_dir='./games/player/'
    if os.path.exists(player_dir)==False:
          os.mkdir(player_dir)
    if os.path.isfile(player_dir+selected_player.get()+'.xlsx')==True:
        #changes the dataframe into a list of dictionaries
        main_data=pd.read_excel(player_dir+selected_player.get()+'.xlsx').to_dict('records')
        main_data.append(player_data)
    else:
        main_data=[]
        main_data.append(player_data)
    match_df=pd.DataFrame(main_data)
    match_df.to_excel(player_dir+selected_player.get()+'.xlsx',index=False)
      
    #save to team directory
    team_dir='./games/team/'+selected_team.get()+'/'
    #deletes unwanted columns
    del team_data['Team']
    del team_data['Tournament']
    #if folder for the team doesn't exist create one
    if os.path.exists(team_dir)==False:
        os.mkdir(team_dir)
        #makes sure the tournament folder exists to store results
    if os.path.exists(team_dir+selected_tournament.get()+'/')==False:
        os.mkdir(team_dir+selected_tournament.get()+'/')
        #if the file already exists load data and add the new data to it
    if os.path.isfile(team_dir+selected_tournament.get()+'/'+game+'.xlsx')==True:
        main_data=pd.read_excel(team_dir+selected_tournament.get()+'/'+game+'.xlsx').to_dict('records')
        main_data.append(team_data)
    else:
        main_data=[]
        main_data.append(team_data)
    #save data to excel sheet    
    match_df=pd.DataFrame(main_data)
    match_df.to_excel(team_dir+selected_tournament.get()+'/'+game+'.xlsx',index=False)
    #create team summary for each tournament
    create_summary(team_dir+selected_tournament.get()+'/', ['Name','Position'])
    
    #create totals sheets-per season
    tournament_list= [f.name for f in os.scandir('./games/tournament/') if f.is_dir()] #gets list of tournaments
    years=[item.split('-', 1)[1] for item in tournament_list] #gets the year of each tournament
    years=list(set(years)) #removes duplicate years
    
    for season in years:
        #for each season get all of the totals from the tournaments in that year
        season_stats=pd.DataFrame()
        for tournament in tournament_list: 
            #print('tournament- ',tournament)
            #print('filepath- ','./games/tournament/'+tournament+'/'+'Totals.xlsx')
            #print('tournament year-',tournament.split('-',1)[1])
            #print('season-         ',season)
            if tournament.split('-',1)[1]==season:
                #print('tournament matches year')
                try:
                    season_stats=season_stats.append(pd.read_excel('./games/tournament/'+tournament+'/'+'Totals.xlsx').to_dict('records'))
                    season_stats=season_stats.fillna(method='ffill')
                except Exception as exception:
                    messagebox.showerror('Error saving season stats',
                                         'There has been an error reading the season statistics \n'+
                                         exception)
        #print(season)
        #print('season_stats-')
        #print(season_stats)
        #group whole season stats by player and position
        try:   
            season_avg=season_stats.groupby(['Name','Position']).mean()
            
            try:
                cols_agg={'Score':'sum','Effectiveness':'sum','Pitch Time':'sum','drive goal':'sum','drive attempt':'sum','completed drive percent':'mean',
          'shot percent':'mean','shot goal':'sum','shot target':'sum','shot miss':'sum',
             'shot attempt':'sum','assist':'sum','short pass percent':'mean','short pass complete':'sum','short pass miss':'sum','short pass':'sum',
             'long pass percent':'mean','long pass complete':'sum','long pass miss':'sum','long pass':'sum',
             'catch percent':'mean','catch-':'sum','drop catch':'sum','targeted':'sum','broken tackle':'sum','block':'sum',
             'intercept':'sum','completed tackle':'sum','partial tackle':'sum','turnover forced':'sum',
             'control gained':'sum','control lost':'sum','control percent':'mean',
             'no bludgers forced':'sum','no bludgers own':'sum','forced pass':'sum','forced turnover':'sum',
             'team goal':'sum','shot block':'sum','catch':'sum','snitch catch':'sum','bubble created':'sum',
             'bubble broken':'sum','bubble lost':'sum','bubble percent':'mean',
             'time attacking':'sum','time defending':'sum','catch attempt':'sum','snitch catch':'sum',
             'blue':'sum','yellow':'sum','red':'sum'}
                season_stats=season_stats.groupby(['Name','Position']).agg(cols_agg)
            except:
                season_stats=season_stats.groupby(['Name','Position']).sum()

        except Exception as exception:
            messagebox.showerror('Error Grouping Stats','There has been an error grouping the season statistics \n'+
                                 exception)
        with pd.ExcelWriter('./games/season_results/'+season+'.xlsx') as writer:  
            season_avg.to_excel  (writer, sheet_name='Totals',index=True)
            season_stats.to_excel(writer, sheet_name='Averages',index=True)

        #season_stats.to_excel('./games/season_results/'+season+'.xlsx',index=True)

    #reset values
    goals_allowed.set(0)
    chaser_data.fromkeys(chaser_data,0)
    beater_data.fromkeys(beater_data,0)
    seeker_data.fromkeys(seeker_data,0)
    cards.fromkeys(cards,0)
    pitchtime.set(0)
    
def reset():
    #resets all values to 0
    pitch_time('stop')
    goals_allowed.set(0)
    chaser_data.fromkeys(chaser_data,0)
    beater_data.fromkeys(beater_data,0)
    seeker_data.fromkeys(seeker_data,0)
    cards.fromkeys(cards,0)
    pitchtime.set(0)
    cb_gamespeed['state']='normal'

    for child in cardframe.winfo_children():
        child.configure(state='normal')
    btn_goal_allowed['state']='disabled'

    
    
btn_save_results=tk.Button(root,text='Save player',width=30,command=save)
btn_save_results.grid(row=11,column=0,columnspan=4,pady=(20,20))

btn_reset=tk.Button(root,text='Reset',width=30,command=reset)
btn_reset.grid(row=12,column=0,columnspan=4)
btn_save_results['state']='disabled'



def file_exists(path,file_name):
    #if file exists add a number to the end of the file rather than overwriting
    if os.path.isfile(path+file_name):
        expand = 1
        while True:
            expand += 1
            new_file_name = file_name.split(".")[0] + str(expand) +'.'+file_name.split('.')[1]
            if os.path.isfile(path+new_file_name):
                continue
            else:
                file_name = new_file_name
                break
    
    return(file_name)

def window_add_match():
    #use this to increment the dataframe- df.loc[df.name.isin('playername'), 'value to increment'] += 1
    ##############################################################################   
    #creates the add match window                                                
    wd_add_match=tk.Toplevel() #add this to only open with command
    wd_add_match.title('Add New Match')
    wd_add_match.geometry('630x530')               #sets default window size
    wd_add_match.iconbitmap('hoops_icon.ico')      #sets the window icon
    lbl_error=tk.Label(wd_add_match,text=' ')

    def add_match():  
        # a lazy error label
        #if the entry boxes are filled in
        if (not ent_tournament.get()=='' and not ent_team1.get()=='' 
            and not ent_team2.get()=='' and not lstbx_team1.size()==0 
            and not lstbx_team2.size()==0 and not len(ent_year.get())==0
            and not '-' in ent_year.get()):
            #create dataframe 
            df_match=pd.DataFrame(columns=['Name','Team'])
        
            #when add match button is pressed creates a dataframe of all players in that match and their team
            df_match.style.set_table_attributes("style='display:inline'").set_caption(ent_tournament.get())
            
            for n in range(lstbx_team1.size()): #iterates across all items in the listbox
                item=lstbx_team1.get(n) #gets currently selected item
                #print('team 1')
                #print(item)
                #adds player to the dataframe
                df_match=df_match.append({'Name':(item),
                                          'Team':ent_team1.get()},ignore_index=True)
                
            for n in range(lstbx_team2.size()): #iterates across all items in the listbox
                item=lstbx_team2.get(n)  #gets currently selected item
                #print('team 2')
                #print(item)

                #adds player to the dataframe
                df_match=df_match.append({'Name':item,
                                              'Team':ent_team2.get()},ignore_index=True)
                                          
            tournament=ent_tournament.get().upper()+'-'+ent_year.get()
            #makes the folder for the tournament if it doesnt exist
            if os.path.exists('./games/game_def/'+tournament+'/')==False:
                os.mkdir('./games/game_def/'+tournament+'/')
            
            #creates the name of the match
            match_name=ent_team1.get()+'_vs_'+ent_team2.get()+'_.csv'
            #checks if the file already exists and if so adds a number to the end of the filename
            if os.path.isfile('./games/game_def/'+tournament+'/'+match_name)==True:
                file_check=messagebox.askyesno('Save File','File already exists \n would you like to overwrite?')
                if file_check==0:
                    tournament=file_exists('./games/game_def/',ent_tournament.get()+'.csv')
            
            #saves the file to the correct folder
            df_match.to_csv('./games/game_def/'+tournament+'/'+match_name,index=False)        
            
            #deletes all data on the screen    
            lstbx_team1.delete(0,tk.END)
            lstbx_team2.delete(0,tk.END)
            ent_team1.delete(0,tk.END)
            ent_team2.delete(0,tk.END)
            ent_add_player_t1.delete(0,tk.END)
            ent_add_player_t2.delete(0,tk.END)
            ent_tournament.delete(0,tk.END)
            ent_year.delete(0,tk.END)
            df_match.drop(df_match.index, inplace=True)
            #clears the error message
            lbl_error.config(text='')
            #updates the combobox in the record stats screen
            cb_tournament['values']= [f.name for f in os.scandir('./games/game_def/') if f.is_dir()]

        else:
            #if fields not filled in show error message
            lbl_error.config(text='Error: A field is empty not saving match data',fg='red')
            lbl_error.grid(row=99,column=0,columnspan=3)
            
            error_dict={'Team 1':lstbx_team1.size(),'Team 2':lstbx_team2.size(),
                        'Team 1 name':len(ent_team1.get()),'Team 2 name':len(ent_team2.get())
                        ,'Tournament name':len(ent_tournament.get()),'Season':len(ent_year.get())}
            for error in error_dict:
                if error_dict[error]==0:
                    error_message=f'{error} error. \n This field is empty'
                    messagebox.showwarning('Add Match Error',error_message)
            if '-' in ent_year.get():
                messagebox.showwarning('Add Match Error','The entry for season must not contain a - in it')
    
    def add_player_t1():
        #when the add player button is pressed it adds the player to the list box
        #if entry box isnt filled in dont do anything
        if not ent_add_player_t1.get()=='':
            lstbx_team1.insert('end',(ent_add_player_t1.get()))
            ent_add_player_t1.delete(0,tk.END)
            
    
    def delete_t1():
        #deletes the selected item from the listbox
        lstbx_team1.delete(tk.ANCHOR) #tk.anchor is the current item selected
        
    #gets and places label and entry box for match name    
    lbl_tournament=tk.Label(wd_add_match,text='Tournament')
    ent_tournament=tk.Entry(wd_add_match,width=50)
    lbl_year      =tk.Label(wd_add_match,text='Season',width=6)
    ent_year      =tk.Entry(wd_add_match,width=6)
    
    ent_tournament.grid(row=0,column=1,pady=(10,20))
    lbl_tournament.grid(row=0,column=0,pady=(10,20))
    lbl_year.grid(row=0,column=2,pady=(10,20))
    ent_year.grid(row=0,column=3,pady=(10,20))

    # creates displays the add players label
    lbl_add_player=tk.Label(wd_add_match,text='Add players')    
    lbl_add_player.grid(row=3,column=1)  
    
    #adds team name entry and label
    lbl_team1=tk.Label(wd_add_match,text='Team 1: ')
    lbl_team1.grid(row=2,column=0)
    ent_team1=tk.Entry(wd_add_match,width=50)
    ent_team1.grid(row=2,column=1)
    
    #adds the labels and buttons relating to add players
    lbl_add_player_t1=tk.Label(wd_add_match,text='Player name: ')
    ent_add_player_t1=tk.Entry(wd_add_match,width=50)
    btn_add_player=tk.Button(wd_add_match,command=add_player_t1,text='Add player')
    #place items
    lbl_add_player_t1.grid(row=4,column=0)
    ent_add_player_t1.grid(row=4,column=1)
    btn_add_player.grid(row=5,column=1)
    #listbox stuff
    lbl_player_lst_box=tk.Label(wd_add_match,text='Player list' )
    lstbx_team1=tk.Listbox(wd_add_match,height=10,width=30)
    scrl_t1=tk.Scrollbar(wd_add_match) #scrollbar 
    lstbx_team1.configure(yscrollcommand=scrl_t1.set)
    scrl_t1.configure(command=lstbx_team1.yview)
    #places listbox stuff
    lbl_player_lst_box.config(text=(ent_team1.get()+' Player list'))
    lbl_player_lst_box.grid(row=2,column=4)
    lstbx_team1.grid(row=3,column=3,rowspan=20,columnspan=3)
    scrl_t1.grid(row=3,column=6,sticky='ns',rowspan=21)
    
    #adds delete button
    btn_del_t1 = tk.Button(wd_add_match, text="Remove Player", command=delete_t1)
    btn_del_t1.grid(row=24,column=4)
    
    
    ##################################################################################
    #For defining players in team 2
    def add_player_t2():
        #when the add player button is pressed it adds the player to the list box
        if not ent_add_player_t2.get()=='':
            lstbx_team2.insert('end',(ent_add_player_t2.get()))
            ent_add_player_t2.delete(0,tk.END)
    def delete_t2():
        #deletes selected item from the listbox
        lstbx_team2.delete(tk.ANCHOR)
        
    #for definining the team name and placing it in the window   
    lbl_team2=tk.Label(wd_add_match,text='Team 2: ')
    ent_team2=tk.Entry(wd_add_match,width=50)
    #places team 2 info
    lbl_team2.grid(row=25,column=0)
    ent_team2.grid(row=25,column=1)
    
    lbl_add_players2=tk.Label(wd_add_match,text='Add players')   
    lbl_add_players2.grid(row=26,column=1)  
     
    lbl_add_player_t2=tk.Label(wd_add_match,text='Player name: ')
    ent_add_player_t2=tk.Entry(wd_add_match,width=50)
    btn_add_playert2=tk.Button(wd_add_match,command=add_player_t2,text='Add player')
    
    #places add player entry stuff
    lbl_add_player_t2.grid(row=27,column=0)
    ent_add_player_t2.grid(row=27,column=1)
    btn_add_playert2.grid(row=28,column=1)
    
    #creates list box for players in team 2
    lbl_player_lst_boxt2=tk.Label(wd_add_match,text='%s Player list' %ent_team1.get())
    lstbx_team2=tk.Listbox(wd_add_match,height=10,width=30)
    scrl_t2=tk.Scrollbar(wd_add_match) #scroll box
    scrl_t2.configure(command=lstbx_team2.yview)
    lstbx_team2.configure(yscrollcommand=scrl_t2.set)
    lbl_player_lst_boxt2.grid(row=25,column=4)
    lstbx_team2.grid(row=26,column=3,rowspan=20,columnspan=3)
    scrl_t2.grid(row=26,column=6,sticky='ns',rowspan=21)
    
    #add the remove player button
    btn_del_t2 = tk.Button(wd_add_match, text="Remove Player", command=delete_t2)
    btn_del_t2.grid(row=47,column=4)
    
    
    lbl_error=tk.Label(wd_add_match,text='  ',fg='red')
    lbl_error.grid(row=99,column=0,columnspan=3)
    
    #add the add match button at the bottom of the window
    btn_add_match=tk.Button(wd_add_match,text='add new match',command=add_match,width=20,height=1)
    btn_add_match.grid(row=100,column=1)

            
def import_match():
    #function to add a match and sync its contents with the rest of the data
    #gets the location of the file
    try:
        tournament_loc=filedialog.askdirectory(initialdir='/',title='Import Tournament')
    except:
        pass
    tournament=tournament_loc.split('/')[-1] #gets tournament name
    playerlist=list_files1('./games/player/','.xlsx') #gets current player list
    playernames=[item.split('.', 1)[0] for item in playerlist] #gets just player names

    matchlist=list_files1(tournament_loc, '.xlsx') #gets all files in the folder
    #iterates through each match
    for match in matchlist:
        #print(match)
        if match == 'Totals.xlsx':
            #if the current file is called totals skip it
            continue
        teams=match.split('_') #gets the team names
        #print(teams)
        teams.remove('vs')
        teams.remove('.xlsx')
        try:
            df=pd.read_excel(tournament_loc+'/'+match)
        except:
            #if it can't read the file in abort loading in all files 
            messagebox.showerror('Import Error',f'Cannot import {match} \n aborting import')
            return
        #print(df)
        
        team1_players=[]
        team2_players=[]
        for rownum in df.index:
            #iterates through every line
            data_list=(df.iloc[rownum].to_dict())
            #updates a players data
            player=pd.DataFrame()
            if data_list['Team']==teams[0]:
                data_list['Team against']=teams[1]
            else:
                data_list['Team against']=teams[0]

            if data_list['Name'] in playernames:
                #if the player exists
                player=(pd.read_excel('./games/player/'+data_list['Name']+'.xlsx').to_dict('records'))
                data_list['Tournament']=tournament
                player.append(data_list)
                df2=pd.DataFrame(player)
            else:
               df2=pd.DataFrame([data_list])
            del df2['Name']
            df2.to_excel('./games/player/'+data_list['Name']+'.xlsx',index=False)
            
            
            if data_list['Team']==teams[0]:
                team1_players.append(data_list)
            elif data_list['Team']==teams[1]:
                team2_players.append(data_list)
                
        df_team=[]        
        df_team.append(pd.DataFrame(team1_players))
        df_team.append(pd.DataFrame(team2_players))
       
        for team in range(len(df_team)):
            #print('team_row')
            #print(df_team[team].iloc[0]['Team'])
            try:
                team_dir='./games/team/'+df_team[team].iloc[0]['Team']+'/'
            except IndexError as error:
                messagebox.showerror('Error','Error: Team not found \n',
                                     error)
                continue
            #print('team dir- ',team_dir)
            #print(df_team[team])
            df_team[team].drop(['Team'],axis=1)
            
            #adds or updates team data
            #makes sure team folder exists
            if os.path.exists(team_dir)==False:
                os.mkdir(team_dir)
                #makes sure the tournament folder exists to store results
            if os.path.exists(team_dir+tournament+'/')==False:
                os.mkdir(team_dir+tournament+'/')
                #if the file already exists ask to increment file name
            if os.path.isfile(team_dir+tournament+'/'+match)==True:
                file_name=file_exists(team_dir+tournament+'/',match)
            else:
                file_name=match
            df_team[team].to_excel(team_dir+tournament+file_name,index=False)
            #create team summary for each tournament
            create_summary(team_dir+tournament+'/', ['Name','Position'])

    
        
        #adds to tournament folder
        tournament_dir='./games/tournament/'+tournament+'/'
        if os.path.exists(tournament_dir)==False:
            os.mkdir(tournament_dir)
        if os.path.isfile(tournament_dir+match)==True:
            file_name=file_exists(tournament_dir+match,match)
        else:
            file_name=match
        df.to_excel(tournament_dir+file_name,index=False)
        create_summary(tournament_dir, ['Name','Team','Position'])
        
    #create totals sheets-per season
    tournament_list= [f.name for f in os.scandir('./games/tournament/') if f.is_dir()] #gets list of tournaments
    years=[item.split('-', 1)[1] for item in tournament_list] #gets the year of each tournament
    years=list(set(years)) #removes duplicate years
    for season in years:
        #for each season get all of the totals from the tournaments in that year
        season_stats=pd.DataFrame()
        for tournament in tournament_list: 
            if tournament.split('-',1)[1]==season:
                season_stats=season_stats.append(pd.read_excel('./games/tournament/'+tournament+'/'+'Totals.xlsx').to_dict('records'))
                season_stats=season_stats.fillna(method='ffill')
        #group whole season stats by player and position
        try:   
            season_avg=season_stats.groupby(['Name','Position']).mean()
            
            try:
                cols_agg={'Score':'sum','Effectiveness':'sum','Pitch Time':'sum','drive goal':'sum','drive attempt':'sum','completed drive percent':'mean',
          'shot percent':'mean','shot goal':'sum','shot target':'sum','shot miss':'sum',
             'shot attempt':'sum','assist':'sum','short pass percent':'mean','short pass complete':'sum','short pass miss':'sum','short pass':'sum',
             'long pass percent':'mean','long pass complete':'sum','long pass miss':'sum','long pass':'sum',
             'catch percent':'mean','catch-':'sum','drop catch':'sum','targeted':'sum','broken tackle':'sum','block':'sum',
             'intercept':'sum','completed tackle':'sum','partial tackle':'sum','turnover forced':'sum',
             'control gained':'sum','control lost':'sum','control percent':'mean',
             'no bludgers forced':'sum','no bludgers own':'sum','forced pass':'sum','forced turnover':'sum',
             'team goal':'sum','shot block':'sum','catch':'sum','snitch catch':'sum','bubble created':'sum',
             'bubble broken':'sum','bubble lost':'sum','bubble percent':'mean',
             'time attacking':'sum','time defending':'sum','catch attempt':'sum','snitch catch':'sum',
             'blue':'sum','yellow':'sum','red':'sum'}
                season_stats=season_stats.groupby(['Name','Position']).agg(cols_agg)
            except:
                season_stats=season_stats.groupby(['Name','Position']).sum()

        except Exception as exception:
            messagebox.showerror('Error Grouping Stats','There has been an error grouping the season statistics \n'+
                                 exception)
        with pd.ExcelWriter('./games/season_results/'+season+'.xlsx') as writer:  
            season_avg.to_excel  (writer, sheet_name='Totals',index=True)
            season_stats.to_excel(writer, sheet_name='Averages',index=True)
        
    
    ## Try to remove tree; if failed show an error using try...except on screen
    try:
        shutil.rmtree(tournament_loc)
    except OSError as e:
        messagebox.showerror('Error',"Error: %s - %s." % (e.filename, e.strerror))
    
#file menu
file_menu=tk.Menu(main_menu,tearoff=0)
main_menu.add_cascade(label='File',menu=file_menu)
file_menu.add_command(label='Add Match',command=window_add_match)
file_menu.add_command(label='Import Match',command=import_match)
file_menu.add_command(label='Exit',command=root.quit)
#view menu
view_menu=tk.Menu(main_menu,tearoff=0)
main_menu.add_cascade(label='View',menu=view_menu)

root.mainloop() 

