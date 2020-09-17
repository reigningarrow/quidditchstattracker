# -*- coding: utf-8 -*-
"""
Created on Tue Sep  8 13:06:45 2020

@author: Sam
"""

#TODO make main window-analysis window, add option to go to new window as a menu bar or button
#TODO edit code so that the user can select by tournament then select by game
#TODO add time of bludger control
import tkinter as tk
import pandas as pd
import os 
import time      
from tkinter import messagebox 


root=tk.Tk()
#sets root window basic info
root.iconbitmap('hoops_icon.ico')      #sets the window icon
root.title('Quidditch Analysis Alpha')  #sets window title       
root.geometry('440x620')  
    
#add a menu bar
main_menu=tk.Menu(root)
root.config(menu=main_menu)

#ensures that the folders exist
if os.path.exists('.\\games\\')==False:
    os.mkdir('.\\games\\') #creates folder
if os.path.exists('.\\games\\game_def\\')==False:
    #if there is no folder called games to store it, make one
    os.mkdir('.\\games\\game_def\\') #creates folder
if os.path.exists('.\\games\\player\\')==False:
    os.mkdir('.\\games\\player\\')
if os.path.exists('.\\games\\team\\')==False:
    os.mkdir('.\\games\team\\')
if os.path.exists('.\\games\\tournament\\')==False:
    os.mkdir('.\\games\\tournament\\')




#TODO add new window to view stats
df_match=pd.DataFrame()



selected_match=tk.StringVar()
def select_match():
    #function to select a specific match
    global df_match
    global playerlist
    df_match=pd.read_csv('./games/'+match.get())
    #print(df_match['Name'].tolist())
    playerlist=(df_match['Name'].to_list())
    selected_match.set(match.get())
    #cheating way to do it, adds the new optionbox on top of the other optionbox
    #opt_select_player.grid_forget()
    opt_select_player=tk.OptionMenu(infoframe,player,*playerlist,command=player_pos)
    opt_select_player.config(width=20,bg='white',relief=tk.SUNKEN)

    opt_select_player.grid(row=3,column=0,sticky='w')

    root.update()

infoframe=tk.Frame(root)
match=tk.StringVar()

#makes so that only files with a specific extension are chosen
def list_files1(directory, extension):
    return (f for f in os.listdir(directory) if f.endswith(extension))
matchlist=list_files1('./games/game_def/', '.csv')

#TODO add way to select match to add stats to, either through optionbox or open file dialog
#creates widgets
lbl_select_match=tk.Label(infoframe,text='Choose match')
opt_select_match=tk.OptionMenu(infoframe,match,*matchlist)
btn_choose_match=tk.Button(infoframe,text='Select Match',width=12,command=select_match)

opt_select_match.config(width=50)
opt_select_match.grid(row=1,column=0,columnspan=3,sticky='w')
lbl_select_match.grid(row=0,column=0,columnspan=4)
btn_choose_match.grid(row=1,column=3,sticky='w')

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
    pitchtime.set(0)
    #removes frames
    chaserframe.grid_forget()
    beaterframe.grid_forget()
    seekerframe.grid_forget()
    #displays relevant frame
    
    try:
        #sets the selected player
        p_team=(df_match['Team'].to_list())
        p_team_index=playerlist.index(player.get())
        p_pos=df_match['Position'].to_list()
        selected_player.set(player.get())
        selected_team.set(p_team[p_team_index])
        selected_pos.set(p_pos[p_team_index])
        
        if pos.get()=='Keeper/Chaser' or pos.get()=='Chaser':
            chaserframe.grid(row=5,column=0,columnspan=3, pady=(5,0))
        elif pos.get()=='Beater':
            beaterframe.grid(row=5,column=0,columnspan=3, pady=(5,0))
        elif pos.get()=='Seeker':
            seekerframe.grid(row=5,column=0,columnspan=3, pady=(5,0))
            btn_goal_allowed['state']=tk.DISABLED
            
        #checks that user has entered a valid option before enabling buttons    
        if pos.get() in ['Keeper/Chaser','Chaser','Beater','Seeker']:
            for child in cardframe.winfo_children():
                child.configure(state='normal')
                btn_on_pitch['state']=tk.NORMAL        
        btn_off_pitch['state']=tk.DISABLED
    except:
        messagebox.showerror('Error Occured','An error has occured when trying to select a player')
def player_pos(event):
    #gets the currently selected players team and position from the optionbox
    try:
        p_team=(df_match['Team'].to_list())
        p_team_index=playerlist.index(player.get())
        team.set(p_team[p_team_index])
        
        p_pos=df_match['Position'].to_list()
        
        pos.set(p_pos[p_team_index])
    
        
        lbl_position.configure(text=pos.get()) #
        lbl_team.configure(text=team.get())
    except:
        messagebox.showerror('Error Occured','An error has occured when trying to select a player')

 
pos=tk.StringVar()     
player=tk.StringVar()
team  =tk.StringVar()

playerlist=['Keeper/Chaser','Chaser','Beater','Seeker']
lbl_select_player=tk.Label(infoframe,text='Select player to analyse')
opt_select_player=tk.OptionMenu(infoframe,player,*playerlist,command=player_pos)
btn_select_player=tk.Button(infoframe,text='Select Player',command=select_player)
lbl_position=tk.Label(infoframe,text=player.get(),width=12)
lbl_team    =tk.Label(infoframe,text=team.get(),width=12)

opt_select_player.config(width=20,bg='white',relief=tk.SUNKEN)
lbl_select_player.grid(row=2,column=0,pady=(10,2),sticky='w')
opt_select_player.grid(row=3,column=0,sticky='w')
btn_select_player.grid(row=3,column=1,sticky='w')
lbl_position.grid(row=3,column=2,sticky='w')
lbl_team.grid(row=3,column=3,sticky='w')

pitchtime=tk.IntVar()
def pitch_time(startstop):
    #gets the amount of time a player is on pitch.
    #if start start timer -time.time() is due to calculating the total time elapsed later
    if startstop=='start':
        pitchtime.set(pitchtime.get()-time.time())
        btn_off_pitch['state']=tk.NORMAL
        btn_on_pitch['state']=tk.DISABLED

    if startstop=='stop':

        pitchtime.set(pitchtime.get()+time.time())
        btn_off_pitch['state']=tk.DISABLED
        btn_on_pitch['state']=tk.NORMAL
        
infoframe.grid(row=2,column=0,columnspan=3)
#on pitch off pitch
btn_on_pitch =tk.Button(root,text='On pitch/Brooms up',width=28,command=lambda: pitch_time('start'))
btn_off_pitch=tk.Button(root,text='Off pitch/Brooms down',width=28,command=lambda: pitch_time('stop'))
#makes sure you can't press anything when no player is selected
btn_off_pitch['state']=tk.DISABLED
btn_on_pitch['state'] =tk.DISABLED


btn_on_pitch.grid(row=4,column=0,pady=(10,0))
btn_off_pitch.grid(row=4,column=1,pady=(10,0))

#TODO if possible add video
chaserframe=tk.Frame(root,borderwidth=1)

#creates a dictionary of values of info to be gathered
chaser_data={'drive goal':0,'drive attempt':0,'shot goal':0,'shot target':0,'shot miss':0,
             'shot attempt':0,'assist':0,'pass complete':0,'pass miss':0,'pass':0,
             'catch':0,'drop catch':0,'targeted':0,'broken tackle':0,'block':0,
             'intercept':0,'completed tackle':0,'partial tackle':0}
#dictionary of extra stuff that didnt need buttons
chaser_extra={'shot goal':'shot attempt','shot target':'shot attempt',
              'shot miss':'shot attempt','pass complete':'pass','pass miss':'pass',
              'catch':'targeted','drop catch':'targeted'} 


def add_value(name):
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
btn_ch_pass_cpt     =tk.Button(chaserframe,text='Pass completed',width=int(button_width/2+2),command=lambda:add_value('pass complete'))
btn_ch_pass_miss    =tk.Button(chaserframe,text='Pass missed',width=int(button_width/2+2),command=lambda:add_value('pass miss'))
btn_ch_catch        =tk.Button(chaserframe,text='Catch',width=int(button_width/2+2),command=lambda:add_value('catch'))
btn_ch_drp_catch    =tk.Button(chaserframe,text='Drop catch',width=int(button_width/2+2),command=lambda:add_value('drop catch'))
btn_ch_brk_tkl      =tk.Button(chaserframe,text='Broken tackle',width=button_width+6,command=lambda:add_value('broken tackle'))
lbl_ch_defence      =tk.Label(chaserframe,text='Defence')
btn_ch_pass_blk     =tk.Button(chaserframe,text='Pass/Shot block',width=int(button_width/2+2),command=lambda:add_value('block'))
btn_ch_intercept    =tk.Button(chaserframe,text='Interception',width=int(button_width/2+2),command=lambda:add_value('intercept'))
btn_ch_tackle_cpt   =tk.Button(chaserframe,text='Full tackle',width=int(button_width/2+2),command=lambda:add_value('completed tackle'))
btn_ch_tackle_ptl   =tk.Button(chaserframe,text='Partial tackle',width=int(button_width/2+2),command=lambda:add_value('partial tackle'))

#adds buttons to frame
  
lbl_ch_offence.grid(row=0,column=0,columnspan=12)
btn_ch_drive_goal.grid(row=1,column=0,columnspan=6)
btn_ch_drive_attempt.grid(row=1,column=6,columnspan=6)
btn_ch_shot_goal.grid(row=2,column=0,columnspan=4)
btn_ch_shot_miss.grid(row=2,column=4,columnspan=4)
btn_ch_shot_tgt.grid(row=2,column=8,columnspan=4)
btn_ch_assist.grid(row=3,column=0,columnspan=12)
btn_ch_pass_cpt.grid(row=4,column=0,columnspan=6)
btn_ch_pass_miss.grid(row=4,column=6,columnspan=6)
btn_ch_catch.grid(row=5,column=0,columnspan=6)
btn_ch_drp_catch.grid(row=5,column=6,columnspan=6)
btn_ch_brk_tkl.grid(row=6,column=0,columnspan=12)

lbl_ch_defence.grid(row=7,column=0,columnspan=12,pady=(5,0))
btn_ch_pass_blk.grid(row=8,column=0,columnspan=6)
btn_ch_intercept.grid(row=8,column=6,columnspan=6)
btn_ch_tackle_cpt.grid(row=9,column=0,columnspan=6)
btn_ch_tackle_ptl.grid(row=9,column=6,columnspan=6)

#chaserframe.grid(row=5,column=0,columnspan=3, pady=(20,0))

beaterframe=tk.Frame(root)
beater_data={'control gained':0,'control lost':0,'no bludgers forced':0,
             'no bludgers own':0,'forced pass':0,'forced turnover':0,'team goal':0,
             'shot block':0,'catch':0,
             'snitch catch':0,'bubble created':0,'bubble broken':0,'bubble lost':0}

def bt_add_value(name):
    beater_data[name]=beater_data[name]+1
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

btn_bt_ctrl_gain.grid(row=0,column=0,columnspan=6)
btn_bt_ctrl_lost.grid(row=0,column=6,columnspan=6)
btn_bt_nb_gn.grid(row=1,column=0,columnspan=6)
btn_bt_nb_lst.grid(row=1,column=6,columnspan=6)
btn_bt_fc_pass.grid(row=2,column=0,columnspan=6)
btn_bt_fc_turn.grid(row=2,column=6,columnspan=6)
btn_bt_shot_block.grid(row=3,column=0,columnspan=6)
btn_bt_catch.grid(row=3,column=6,columnspan=6)
btn_bt_snitch_catch.grid(row=5,column=0,columnspan=12)
btn_bt_bubble_created.grid(row=4,column=0,columnspan=4)
btn_bt_bubble_broken.grid(row=4,column=4,columnspan=4)
btn_bt_bubble_lost.grid(row=4,column=8,columnspan=4)
btn_bt_team_goal.grid(row=6,column=0,columnspan=12,pady=(10,0))

#beaterframe.grid(row=10,column=0,columnspan=3)

#seekerframes
seekerframe=tk.Frame(root)
seeker_data={'time attacking':0,'time defending':0,'catch attempt':0,'snitch catch':0}

def sk_add_value(name):
    seeker_data[name]=seeker_data[name]+1
    if seeker_data[name]=='snitch catch':
        seeker_data['catch_attempt']=seeker_data['catch_attempt']+1
def timers(timer):
    if timer=='attack':
        seeker_data['time attacking']=seeker_data['time attacking']-time.time()  
        btn_sk_atk_stp['state']=tk.NORMAL        
        btn_sk_atk['state']=tk.DISABLED
    elif timer=='attack stop':
        seeker_data['time attacking']=time.time()+seeker_data['time attacking']
        btn_sk_atk_stp['state']=tk.DISABLED        
        btn_sk_atk['state']    =tk.NORMAL
    if timer=='def':
        seeker_data['time defending']=seeker_data['time defending']-time.time()
        btn_sk_def_stp['state']=tk.NORMAL
        btn_sk_def['state']    =tk.DISABLED
    elif timer=='def stop':
        seeker_data['time defending']=seeker_data['time defending']+time.time()
        btn_sk_def_stp['state']=tk.DISABLED
        btn_sk_def['state']    =tk.NORMAL

    

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


btn_sk_atk_stp['state']=tk.DISABLED        
btn_sk_def_stp['state']=tk.DISABLED

#create frame for cards
cardframe=tk.Frame(root)
cards={'blue':0,'yellow':0,'red':0}
def card_fn(data):
    cards[data]=cards[data]+1
goals_allowed=tk.IntVar()
def goals():
    goals_allowed.set(goals_allowed.get()+1)
    
#add buttons for cardsframe
btn_blue_cd=tk.Button(cardframe,text='Blue card',width=int(button_width/3+1),command=lambda: card_fn('blue'))
btn_yellow_cd=tk.Button(cardframe,text='Yellow card',width=int(button_width/3+1),command=lambda: card_fn('yellow'))
btn_red_cd=tk.Button(cardframe,text='Red card',width=int(button_width/3+1),command=lambda: card_fn('red'))

btn_goal_allowed=tk.Button(cardframe,text='Goal allowed',width=button_width+6,command=goals)

#place buttons in frame
btn_goal_allowed.grid(row=0,column=0,columnspan=3)
btn_blue_cd.grid(row=1,column=0)
btn_yellow_cd.grid(row=1,column=1)
btn_red_cd.grid(row=1,column=2)

cardframe.grid(row=10,column=0,columnspan=4,pady=(20,0))
#disables card buttons at the start
for child in cardframe.winfo_children():
    child.configure(state='disable')


def save():
    #adds the data to the dataframe and resets variables
    #add try statement to save
    tot_pitchtime=time.strftime('%M:%S',pitchtime.get())
    initial_data={'Name':selected_player.get(),'Team':selected_team.get(),
                  'Position':selected_pos.get(),'Pitch Time':tot_pitchtime}
    if selected_pos.get()=='Keeper/Chaser' or selected_pos.get()=='Chaser':
        data={**initial_data,**chaser_data,**cards}
    elif selected_pos.get()=='Beater':
        data={**initial_data,**beater_data,**cards}
    elif selected_pos.get()=='Seeker':
        data={**initial_data,**seeker_data,**cards}
        
    
    game=selected_match.get().split('.')
    game=game[0]
    if os.path.isfile('./games/'+game+'.xlsx')==True:
        #changes the dataframe into a list of dictionaries
        main_data=pd.read_excel('./games/'+game+'.xlsx').to_dict('records')
        main_data.append(data)
    else:
        main_data=[]
        main_data.append(data)
    match_df=pd.DataFrame(main_data)
    match_df.to_excel('./games/'+game+'.xlsx',index=False)

   
    goals_allowed.set(0)
    chaser_data.fromkeys(chaser_data,0)
    beater_data.fromkeys(beater_data,0)
    seeker_data.fromkeys(seeker_data,0)
    cards.fromkeys(cards,0)
    pitchtime.set(0)
    
def reset():
    #resets all values to 0
    goals_allowed.set(0)
    chaser_data.fromkeys(chaser_data,0)
    beater_data.fromkeys(beater_data,0)
    seeker_data.fromkeys(seeker_data,0)
    cards.fromkeys(cards,0)
    pitchtime.set(0)
    
    
btn_save_results=tk.Button(root,text='Save player',width=30,command=save)
btn_save_results.grid(row=11,column=0,columnspan=4,pady=(20,20))

btn_reset=tk.Button(root,text='Reset',width=30,command=reset)
btn_reset.grid(row=12,column=0,columnspan=4)




def file_exists(file_name):
    #if file exists add a number to the end of the file rather than overwriting
    if os.path.isfile('./games/game_def/'+file_name):
        expand = 1
        while True:
            expand += 1
            new_file_name = file_name.split(".")[0] + str(expand) +'.'+file_name.split('.')[1]
            if os.path.isfile('./games/game_def'+new_file_name):
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
    wd_add_match.geometry('710x510')               #sets default window size
    wd_add_match.iconbitmap('hoops_icon.ico')      #sets the window icon
    lbl_error=tk.Label(wd_add_match,text=' ')

    def add_match():  
        
        
        # a lazy error label
        #if the entry boxes are filled in
        if not ent_match_name.get()=='' and not ent_team1.get()=='' and not ent_team2.get()=='' and not lstbx_team1.size()==0 and not lstbx_team2.size()==0:
            #create dataframe 
            df_match=pd.DataFrame(columns=['Name','Team','Position'])
        
            #when add match button is pressed creates a dataframe of all players in that match and their team
            df_match.style.set_table_attributes("style='display:inline'").set_caption(ent_match_name.get())
            
            for n in range(lstbx_team1.size()): #iterates across all items in the listbox
                item=lstbx_team1.get(n) #gets currently selected item
                item=item.split('-')    #splits item into player name and position
                #checks if the player in this position exists in the database already
                if item[0].strip() in df_match.Name.values:
                    #if player in a position exists in the database adds position to their name and add a new entry
                    df_match=df_match.append({'Name':(item[0]+'-'+item[1]),
                                              'Team':ent_team1.get(),'Position':item[1]},ignore_index=True)
                else:
                    #if player in a position doesnt exist in the database adds them
                    df_match=df_match.append({'Name':(item[0]),
                                              'Team':ent_team1.get(),'Position':item[1]},ignore_index=True)
                
            for n in range(lstbx_team2.size()): #iterates across all items in the listbox
                item=lstbx_team2.get(n)  #gets currently selected item
                item=item.split('-')     #splits item into player name and position
                if item[0].strip() in df_match.Name.values:
                    #if player in a position exists in the database adds position to their name and add a new entry
                    df_match=df_match.append({'Name':(item[0]+'-'+item[1]),
                                              'Team':ent_team2.get(),'Position':item[1]},ignore_index=True)
                else:
                    #if player in a position doesnt exist in the database adds them
                    df_match=df_match.append({'Name':(item[0]),
                                              'Team':ent_team2.get(),'Position':item[1]},ignore_index=True)
            match_name=ent_match_name.get()+'.csv'
            if os.path.isfile('.\\games\\game_def\\'+match_name)==True:
                file_check=messagebox.askyesno('Save File','File already exists \n would you like to overwrite?')
                if file_check==0:
                    match_name=file_exists(ent_match_name.get()+'.csv')

            #checks if there is a folder called games add then adds the game file
            if os.path.exists('.\\games\\game_def\\')==True:
                df_match.to_csv('.\\games\\game_def\\'+match_name,index=False)
            else:
                #if there is no folder called games to store it, make one
                os.mkdir('.\\games\\game_def\\') #creates folder
                match_name=file_exists(ent_match_name.get()+'.csv')
                df_match.to_csv('.\\games\\game_def\\'+match_name,index=False)
        
            
            #deletes all data on the screen    
            lstbx_team1.delete(0,tk.END)
            lstbx_team2.delete(0,tk.END)
            ent_team1.delete(0,tk.END)
            ent_team2.delete(0,tk.END)
            ent_add_player_t1.delete(0,tk.END)
            ent_add_player_t2.delete(0,tk.END)
            ent_match_name.delete(0,tk.END)
            df_match.drop(df_match.index, inplace=True)
            lbl_error.config(text='')
        else:
            #if fields not filled in show error message
            lbl_error.config(text='Error: A field is empty not saving match data',fg='red')
            lbl_error.grid(row=99,column=0,columnspan=3)
    
    def add_player_t1():
        #when the add player button is pressed it adds the player to the list box
        #if entry box isnt filled in dont do anything
        if not ent_add_player_t1.get()=='':
            lstbx_team1.insert('end',(ent_add_player_t1.get()+'-'+position.get()))
            ent_add_player_t1.delete(0,tk.END)
            
    
    def delete_t1():
        #deletes the selected item from the listbox
        lstbx_team1.delete(tk.ANCHOR) #tk.anchor is the current item selected
        
    #gets and places label and entry box for match name    
    lbl_match_name=tk.Label(wd_add_match,text='Match Name')
    lbl_match_name.grid(row=0,column=0)
    ent_match_name=tk.Entry(wd_add_match,width=50)
    ent_match_name.grid(row=0,column=1,pady=10)
    
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
    positions=['Keeper/Chaser','Chaser','Beater','Seeker']
    position=tk.StringVar()
    position.set(positions[0]) #makes sure the optionbox has a default item
    opt_add_player_pos_t1=tk.OptionMenu(wd_add_match,position,*positions)
    opt_add_player_pos_t1.config(width=13)
    #place items
    lbl_add_player_t1.grid(row=4,column=0)
    ent_add_player_t1.grid(row=4,column=1)
    opt_add_player_pos_t1.grid(row=4,column=2)
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
            lstbx_team2.insert('end',(ent_add_player_t2.get()+'-'+positiont2.get()))
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
    positiont2=tk.StringVar()
    positiont2.set(positions[0])
    opt_add_player_pos_t2=tk.OptionMenu(wd_add_match,positiont2,*positions)
    opt_add_player_pos_t2.config(width=13)
    
    #places add player entry stuff
    lbl_add_player_t2.grid(row=27,column=0)
    ent_add_player_t2.grid(row=27,column=1)
    opt_add_player_pos_t2.grid(row=27,column=2)
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


#file menu
file_menu=tk.Menu(main_menu,tearoff=0)
main_menu.add_cascade(label='File',menu=file_menu)
file_menu.add_command(label='Add Match',command=window_add_match)
file_menu.add_command(label='Exit',command=root.quit)
#view menu
view_menu=tk.Menu(main_menu,tearoff=0)
main_menu.add_cascade(label='View',menu=view_menu)

root.mainloop() 

