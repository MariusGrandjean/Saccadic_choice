# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 11:01:16 2023

@author: Marius
"""

# %% Package imports 

import os
import numpy.random as rnd
import random
import glob
from psychopy import visual, event, core, gui, data, monitors

# %% Image Paths
## For the entire folder
# face_images = glob.glob("C:/Users/Marius/Dropbox/Travail/UCLouvain/Ph.D/Projet/Projet - Saccades/ChoixSaccadique/STIMULI/*face*.jpg")
# vehicle_images = glob.glob("C:/Users/Marius/Dropbox/Travail/UCLouvain/Ph.D/Projet/Projet - Saccades/ChoixSaccadique/STIMULI/*vehicle*.jpg")
  
## Only for upright images
# Define image directory path
image_directory = "C:/Users/Marius/Dropbox/Travail/UCLouvain/Ph.D/Projet/Projet - Saccades/ChoixSaccadique/STIMULI"

# Get a list of face image filenames that don't contain "inverted" in their names
face_images = [filename for filename in glob.glob(os.path.join(image_directory, "*face*.jpg")) if "inverted" not in filename]

# Get a list of vehicle image filenames that don't contain "inverted" in their names
vehicle_images = [filename for filename in glob.glob(os.path.join(image_directory, "*vehicle*.jpg")) if "inverted" not in filename]


# %% Subject info

exp_name = 'Saccadic_choice'
exp_info = {
        'participant': '',
        'gender': ('male', 'female'),
        'age':'',
        'left-handed':False,
        'Layout' : ('horizontal', 'vertical'),
        'screenwidth(cm)': '49',
        'screenresolutionhori(pixels)': '1920',
        'screenresolutionvert(pixels)': '1080',
        'refreshrate(hz)': '120'}

dlg = gui.DlgFromDict(dictionary=exp_info, title=exp_name)
    
# If 'Cancel' is pressed, quit
if dlg.OK == False:
    core.quit()
        
# Get date and time
exp_info['date'] = data.getDateStr()
exp_info['exp_name'] = exp_name

# %% Creation of a dictonary with all the instruction

instruction_dictionary = {'instructions.text' : "Dans cette étude ... \n\nVotre tâche est d'indiquer",
                          'instructions.faces' : "Dans ce bloc, votre tâche est de regarder les VISAGES\n\n Appuyez sur la barre ESPACE pour commencer",
                          'instructions.vehicles' : "Dans ce bloc, votre tâche est de regarder les VEHICULES\n\n Appuyez sur la barre ESPACE pour commencer",
                          'timertext.text':"Prêt",
                          'blocktext1.text': "Veuillez faire une courte pause avant le prochain bloc. \nVous pouvez appuyer sur la barre 'ESPACE' pour continuer après ",
                          'blocktext2.text':" secondes lorsque vous serez prêt. \n Bloc:"}

# %% Monitor setup 

mon = monitors.Monitor('OLED...') #Pulls out photometer calibration settings by name.  
mon.setWidth(float(exp_info['screenwidth(cm)'])) # Cm width
mon.setDistance(57)
horipix = exp_info['screenresolutionhori(pixels)']
vertpix = exp_info['screenresolutionvert(pixels)']
framerate = exp_info['refreshrate(hz)']
scrsize = (float(horipix),float(vertpix))
framelength = 1000/(float(framerate))
mon.setSizePix(scrsize)

# how many rgb values do we lower the brightness
reduce=50

# the candela / metersquare value
cdm2 = (128-reduce)/255*100

# %% Open a window
win = visual.Window(monitor = mon, 
                    size = scrsize,
                    colorSpace = "rgb255",
                    color= [128-reduce, 128-reduce, 128-reduce],
                    units='deg',
                    fullscr=True,
                    allowStencil=True,
                    screen=1)
# Hide the cursor when the window is opened
win.mouseVisible=False

# %% Preparing the experiment

# Define fixation cross
fixation_cross = visual.TextStim(win, 
                                 text='+', 
                                 color='white', 
                                 height=2,
                                 font="Palatino Linotype", 
                                 bold=False)

# Number of blocks and trials per block
num_blocks = 5
trials_per_block = 10

# Set the desired layout direction
layout_direction = exp_info['Layout']  

# Function to display target information and wait for key press
def display_target_info(win, target_text):
    target_info_text = visual.TextStim(win, text=target_text, color='white', height=1.5, pos=(0, 0))
    target_info_text.draw()
    win.flip()
    event.waitKeys(keyList=['space', 'escape'])


# Function to run a trial
def run_trial(win, target_image, distractor_image, layout_direction):
    fixation_duration = rnd.uniform(0.8, 1.6)
    fixation_cross.draw()
    win.flip()
    core.wait(fixation_duration)

    win.flip()
    core.wait(0.2)

    target_image.draw()
    distractor_image.draw()
    win.flip()
    core.wait(0.4)

    win.flip()
    core.wait(1.0)

### Function that draws a break between blocks, shows which block they are at,
# and takes as arguments block no, the break time between each block, and a
# long break at every 6th block.    
def block_break(block_no, totalblocks, timershort, timerlong):
    timer = timershort
    blocktext = visual.TextStim(
        win=win,
        height=1,
        font="Palatino Linotype",
        alignHoriz='center')
    
    timertext = visual.TextStim(
        win=win,
        height=1,
        pos=[0, -6],
        font="Palatino Linotype",
        alignHoriz='center')
    
    if block_no % 3 == 0:
        timer = timerlong
    blocktext.text = (
        instruction_dictionary['blocktext1.text']
        + str(timer)
        + instruction_dictionary['blocktext2.text']
        + str(block_no)
        + """/"""
        + str(totalblocks)
    )
    for time in range(timer, 0, -1):
        blocktext.draw()
        timertext.text = ":" + str(time)
        timertext.draw()
        win.flip()
        core.wait(1)
    
    timertext.text = instruction_dictionary['timertext.text']
    blocktext.draw()
    timertext.draw()
    win.flip()

    keys = event.waitKeys(keyList=['space', 'escape'])
    if 'escape' in keys:
        win.close()
    win.flip()

# %% Starting the experiment 
# Loop through blocks
for block in range(num_blocks):
    if block % 2 == 0:
        target_images = face_images
        distractor_images = vehicle_images
        target_text = instruction_dictionary['instructions.faces']
    else:
        target_images = vehicle_images
        distractor_images = face_images
        target_text = instruction_dictionary['instructions.vehicles']
    
    display_target_info(win, target_text)
    
    rnd.shuffle(target_images)
    rnd.shuffle(distractor_images)

    # Loop through trials within each block
    for trial in range(trials_per_block):
        target_image_path = target_images[trial]
        distractor_image_path = distractor_images[trial]
        
        target_image = visual.ImageStim(win, image=target_image_path, size=(10, 10))
        distractor_image = visual.ImageStim(win, image=distractor_image_path, size=(10, 10))
        
        if layout_direction == 'vertical':
            target_image.pos = (0, 7)
            distractor_image.pos = (0, -7)
            
        if layout_direction == 'horizontal':
            # Randomly select left or right position
            target_x_position = random.choice([-10, 10])
            distractor_x_position = -target_x_position
            target_image.pos = (target_x_position, 0)
            distractor_image.pos = (distractor_x_position, 0)
        elif layout_direction == 'vertical':
            # Randomly select up or down position
            target_y_position = random.choice([7, -7])
            distractor_y_position = -target_y_position
            target_image.pos = (0, target_y_position)
            distractor_image.pos = (0, distractor_y_position)    
        
        run_trial(win, target_image, distractor_image, layout_direction)
        
        # Run block break function with a minimum of 10 seconds
    block_break(block + 1, num_blocks, 10, 30)  # Adjust the timer values as needed


# Close the window at the end
win.close()
