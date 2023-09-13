# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 11:01:16 2023

@author: Marius
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 11:01:16 2023

@author: Marius
"""

# %% Package imports 

import os
import numpy as np
import numpy.random as rnd
from PIL import Image
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
        'screenresolution_hori(pixels)': '1920',
        'screenresolution_vert(pixels)': '1080',
        'refreshrate(hz)': '120'}

dlg = gui.DlgFromDict(dictionary=exp_info, title=exp_name)
    
# If 'Cancel' is pressed, quit
if dlg.OK == False:
    core.quit()
        
# Get date and time
exp_info['date'] = data.getDateStr()
exp_info['exp_name'] = exp_name

# %% Creation of a dictonary with all the instruction

instruction_dictionary = {'instructions.text' : "Dans cette étude, vous allez voir deux images présentées simultanément d'un part et d'autre de l'écran.\n\n Appuyez sur ESPACE pour voir la suite des instructions.",
                          'instructions.text2': "Votre tâche sera de regarder LE PLUS VITE POSSIBLE vers l'image qui sera définie au préalable comme cible.\n\n Appuyez sur ESPACE pour voir la suite des instructions.",
                          'instructions.text3' : "Les cibles seront soit des VISAGES soit des VEHICULES.\n\n Appuyez sur ESPACE pour commencer.",
                          'instructions.faces' : "Durant les prochains blocs, votre tâche sera de regarder les VISAGES.\n\n Appuyez sur la barre ESPACE pour commencer.",
                          'instructions.vehicles' : "Durant les prochains blocs, votre tâche sera de regarder les VEHICULES.\n\n Appuyez sur la barre ESPACE pour commencer.",
                          'timertext.text':"Prêt",
                          'blocktext1.text': "Veuillez faire une courte pause avant le prochain bloc. \nVous pouvez appuyer sur la barre 'ESPACE' pour continuer après ",
                          'blocktext2.text':" secondes lorsque vous serez prêt. \n Bloc:"}

# %% Monitor setup 

mon = monitors.Monitor('OLED...') #Pulls out photometer calibration settings by name.  
mon.setWidth(float(exp_info['screenwidth(cm)'])) # Cm width
mon.setDistance(57)
horipix = exp_info['screenresolution_hori(pixels)']
vertpix = exp_info['screenresolution_vert(pixels)']
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

# %% Opening a file for writing the data
# if not os.path.isdir(dataPath):
#     os.makedirs(dataPath)
# fieldnames=list(blocks[0][0].keys())
# data_fname = exp_info['participant'] + '_' + exp_info['age'] + '_' + exp_info['gender'][0] + '_' + exp_info['date'] + '.csv'
# data_fname = os.path.join(dataPath, data_fname)
# f = open(data_fname,'w',encoding='UTF8', newline='')
# writer=csv.DictWriter(f, fieldnames=fieldnames)
# writer.writeheader()

# %% Display instructions

instructions = visual.TextStim(win=win,
    pos=[0,0], 
    wrapWidth=None, height=1.25, font="Palatino Linotype", alignHoriz='center', color = 'white')

instructions.text = instruction_dictionary['instructions.text']
instructions.draw()

win.flip() 
keys = event.waitKeys(keyList=['space','escape'])

# Adding other instructions
instructions = visual.TextStim(win=win,
    pos=[0,0], 
    wrapWidth=None, height=1.25, font="Palatino Linotype", alignHoriz='center', color = 'white')

instructions.text = instruction_dictionary['instructions.text2']
instructions.draw()

win.flip() 
keys = event.waitKeys(keyList=['space','escape'])

# Adding other instructions
instructions = visual.TextStim(win=win,
    pos=[0,0], 
    wrapWidth=None, height=1.25, font="Palatino Linotype", alignHoriz='center', color = 'white')

instructions.text = instruction_dictionary['instructions.text3']
instructions.draw()

# Adding examples
image_path1 = os.path.join(image_directory, "face_beautiful-1996283_cut_300_Norm_RGB.jpg")  # Replace with your image path
bitmap_im = Image.open(image_path1)
image_stim = visual.ImageStim(win, image=bitmap_im, pos=[-13, 0], size=6)
image_stim.draw()

image_path2 = os.path.join(image_directory, "vehicle_volkswagen-569315_1920_cut_300_Norm_RGB.jpg")  # Replace with your image path
bitmap_im = Image.open(image_path2)
image_stim = visual.ImageStim(win, image=bitmap_im, pos=[13, 0], size=6)
image_stim.draw()

win.flip() 
keys = event.waitKeys(keyList=['space','escape'])

# %% Preparing the experiment

# Define fixation cross
fixation_cross = visual.TextStim(win, 
                                 text='+', 
                                 color='white', 
                                 height=2,
                                 font="Palatino Linotype", 
                                 bold=False)

# Number of blocks and trials per block
num_blocks = 10
trials_per_block = 10

# Set the desired layout direction
layout_direction = exp_info['Layout']  

### Function to display target information and wait for key press
def display_target_info(win, target_text):
    # Create a visual stimulus for displaying target information
    target_info_text = visual.TextStim(win, text=target_text, color='white', height=1.5, pos=(0, 0))
    # Draw the target information on the window
    target_info_text.draw()
    # Display the window with the target information
    win.flip()
    # Wait for a key response (space or escape)
    event.waitKeys(keyList=['space', 'escape'])

### Function to run a trial
def run_trial(win, target_image, distractor_image, layout_direction):
    
    # Quit the experiment is escape is pressed
    keys = event.getKeys()
    if 'escape' in keys:
        win.close() 
    
    # Generate a random fixation duration between 0.8 and 1.6 seconds
    fixation_duration = rnd.uniform(0.8, 1.6) 
    fixation_cross.draw() # Display the fixation cross
    win.flip()
    core.wait(fixation_duration) # Wait for the fixation duration to pass
    # Clear the window and wait for a brief period (0.2 seconds)
    win.flip()
    core.wait(0.2)
    # Draw and display the target and distractor images
    target_image.draw()
    distractor_image.draw()
    win.flip()
    # Wait for 0.4 seconds to display the images
    core.wait(0.4)
    # Clear the window and wait for 1.0 second (end of the trial)
    win.flip()
    core.wait(1.0)

### Function that draws a break between blocks, shows which block they are at,
# and takes as arguments block no, the break time between each block, and a
# long break at every x block.
def block_break(block_no, totalblocks, timershort, timerlong):
    
    # Determine the timer duration based on block number
    timer = timerlong if block_no % 5 == 0 else timershort
    
    # Create a visual stimulus for the block's text
    blocktext = visual.TextStim(
        win=win,
        height=1,
        font="Palatino Linotype",
        alignHoriz='center')
    
    blocktext.text = instruction_dictionary['blocktext1.text'] 
    + str(timer) 
    + instruction_dictionary['blocktext2.text'] 
    + str(block_no) 
    + "/" 
    + str(totalblocks)
    
    # Create a visual stimulus for the timer text
    timertext = visual.TextStim(
        win=win,
        height=1,
        pos=[0, -6],
        font="Palatino Linotype",
        alignHoriz='center',
        text=instruction_dictionary['timertext.text'])
    
    # Countdown and display the timer
    for time in range(timer, 0, -1):
        blocktext.draw()
        timertext.text = ":" + str(time)
        timertext.draw()
        win.flip()
        core.wait(1)
    
    # Display "ready" when the timer is over    
    timertext.text = instruction_dictionary['timertext.text']
    blocktext.draw()
    timertext.draw()
    win.flip()
    
    # Close the window if escape or space keys are pressed
    keys = event.waitKeys(keyList=['space', 'escape'])
    if 'escape' in keys:
        win.close()
    win.flip()

# %% Starting the experiment 

# Define the order of blocks (0 represents face-target, 1 represents vehicle-target)
half_blocks = num_blocks // 2
group1 = [0] * half_blocks
group2 = [1] * half_blocks

# Randomly decide the order of groups
if random.choice([True, False]):
    condition_order = group1 + group2
else:
    condition_order = group2 + group1

# Initialize variables to store the previous condition_order
prev_condition_order = None

# Loop through blocks
for block in range(num_blocks):
    if condition_order[block] == 0:
        target_images = face_images
        distractor_images = vehicle_images
        target_text = instruction_dictionary['instructions.faces']
    else:
        target_images = vehicle_images
        distractor_images = face_images
        target_text = instruction_dictionary['instructions.vehicles']
    
    # Display target_text only when condition_order changes
    if condition_order[block] != prev_condition_order:
        display_target_info(win, target_text)
        prev_condition_order = condition_order[block]
    
    rnd.shuffle(target_images)
    rnd.shuffle(distractor_images)

    # Loop through trials within each block
    for trial in range(trials_per_block):
        target_image_path = target_images[trial]
        distractor_image_path = distractor_images[trial]
        
        target_image = visual.ImageStim(win, image=target_image_path, size=(10, 10))
        distractor_image = visual.ImageStim(win, image=distractor_image_path, size=(10, 10))
             
        # Specify the direction of the layout
        if layout_direction == 'vertical':
            # Randomly select up or down position
            target_y_position = random.choice([7, -7])
            distractor_y_position = -target_y_position
            target_image.pos = (0, target_y_position)
            distractor_image.pos = (0, distractor_y_position) 
            
        elif layout_direction == 'horizontal':
            # Randomly select left or right position
            target_x_position = random.choice([-10, 10])
            distractor_x_position = -target_x_position
            target_image.pos = (target_x_position, 0)
            distractor_image.pos = (distractor_x_position, 0)
                            
        run_trial(win, target_image, distractor_image, layout_direction)
        
        # Run block break function with a minimum of 10 seconds
    block_break(block + 1, num_blocks, 10, 30)  # Adjust the timer values as needed

    # # Close the window if escape or space keys are pressed
    if 'escape' in keys:
        win.close()
        
# Close the window at the end
win.close()