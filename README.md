# Quidditch stat tracker
A test program made in tkinter and python to enable users to measure stats from individual players.
This will eventually be made into an exe but currently this is not working correctly.  
### TODO
- upload to a central google sheet
- ~~add total stats per year that autoupdates~~
- separate tabs for each position
- ~~add totals for each tournament and each season~~
- ~~add way to sync files when a new file is added~~
### The main file is QuidAnalysisMain
## Running the script
Make sure you have all the relevant modules installed by running **install modules** script.  
To run this download the files to a new folder and then **run the script QuidAnalysisMain**

## Usage
### Main analysis window
At startup the program will show the main analysis window. From this window you select a tournament and then match to analyse from the dropdown boxes. You will then be able to select a player and their position from the dropdown boxes. Once you have selected these press the **select player** button.
The window will then display the buttons to record stats for that players position. As the player has to be on pitch for them to be able to perform an action most buttons will be greyed out initially. 
Once a player is on pitch when they perform a relevant action press a button and that action will be recorded.  
**If you make an error there is no current way to undo one action, to reset all of the stats and start again press the Reset button**  
For ease of use some actions which cannot happen concurrently are greyed out where necessary. This will change accordingly due to a players actions.  
If a player gets a red card or two yellows and are ejected from the game then all action buttons will be greyed out as they are no longer able to participate in the match.  
### Saving a players statistics  
To save a player press the Save player button. This will save to three excel files. 
- The match file for the tournament this was played in
- The match file for the team they player for
- The players excel file to record their lifetime stats
These will be saved in the relevant folders within the games folder
### Add match
To add a match go to the **file menu** and click on **add match**. This will bring up the add match window.  
You will then need to add in a tournament name and year and the teams playing. Then type in the player name and press the **add player** button where it will be added to their teams list box on the right hand side.  
If a players name is added incorrectly select them in the listbox and press the **remove player** button to remove them from the teams roster.  
Once the rosters have been completed press the **Add new match** button which will save the rosters and teams for that game in the tournament.  

# Please note that this is still in alpha so if there are any problems or requests for things to add feel free to contact me.
