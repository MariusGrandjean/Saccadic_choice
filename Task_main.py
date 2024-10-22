# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 11:01:16 2023

@author: Marius
"""

# %% Package imports 

from __future__ import division
from __future__ import print_function

import pylink
import csv
from math import atan2, degrees
import os
import time
import sys
import math
import numpy
import numpy.random as rnd
from PIL import Image
import random
import glob
from EyeLinkCoreGraphicsPsychoPy import EyeLinkCoreGraphicsPsychoPy
from psychopy import visual, event, core, gui, data, monitors
from string import ascii_letters, digits

# %% Set up EDF data file name and local data folder

# The EDF data filename should not exceed 8 alphanumeric characters
# use ONLY number 0-9, letters, & _ (underscore) in the filename
edf_fname = 'Hor_name' # Always indicate whether horizontal or vertical (for analysis sake)

# Prompt user to specify an EDF data filename
# before we open a fullscreen window
dlg_title = 'Enter EDF File Name'
dlg_prompt = 'Please enter a file name with 8 or fewer characters\n' + \
             '[letters, numbers, and underscore].'

# loop until we get a valid filename
while True:
    dlg = gui.Dlg(dlg_title)
    dlg.addText(dlg_prompt)
    dlg.addField('File Name:', edf_fname)
    # show dialog and wait for OK or Cancel
    ok_data = dlg.show()
    if dlg.OK:  # if ok_data is not None
        print('EDF data filename: {}'.format(ok_data[0]))
    else:
        print('user cancelled')
        core.quit()
        sys.exit()

    # get the string entered by the experimenter
    tmp_str = dlg.data[0]
    # strip trailing characters, ignore the ".edf" extension
    edf_fname = tmp_str.rstrip().split('.')[0]

    # check if the filename is valid (length <= 8 & no special char)
    allowed_char = ascii_letters + digits + '_'
    if not all([c in allowed_char for c in edf_fname]):
        print('ERROR: Invalid EDF filename')
    elif len(edf_fname) > 8:
        print('ERROR: EDF filename should not exceed 8 characters')
    else:
        break

# Set up a folder to store the EDF data files and the associated resources
# e.g., files defining the interest areas used in each trial
results_folder = 'results'
if not os.path.exists(results_folder):
    os.makedirs(results_folder)

# We download EDF data file from the EyeLink Host PC to the local hard
# drive at the end of each testing session, here we rename the EDF to
# include session start date/time
time_str = time.strftime("_%Y_%m_%d_%H_%M", time.localtime())
session_identifier = edf_fname + time_str

# create a folder for the current testing session in the "results" folder
session_folder = os.path.join(results_folder, session_identifier)
if not os.path.exists(session_folder):
    os.makedirs(session_folder)

# %% Image Paths

image_directory = "C:/Users/Marius/Dropbox/Travail/UCLouvain/PhD/Projet/Projet-Saccades/ChoixSaccadique/stimuli_Final"
face_images = glob.glob("C:/Users/Marius/Dropbox/Travail/UCLouvain/PhD/Projet/Projet-Saccades/ChoixSaccadique/stimuli_Final/*faces*.jpg")
vehicle_images = glob.glob("C:/Users/Marius/Dropbox/Travail/UCLouvain/PhD/Projet/Projet-Saccades/ChoixSaccadique/stimuli_Final/*vehicule*.jpg")

# %% Subject info

# This part should be modified according to your preferences and settings
exp_name = 'Saccadic_choice'
exp_info = {
        'dummy_mode':('FALSE', 'TRUE'),
        'participant': '',
        'gender': ('male', 'female'),
        'age':'',
        'left-handed':False,
        'Layout' : ('horizontal', 'vertical'),
        'desired_visual_angle' : '8', 
        'screenwidth(cm)': '209,6', 
        'screendistance(cm)': '90', 
        'screenresolutionhori(pixels)': '3840', 
        'screenresolutionvert(pixels)': '2160', 
        'refreshrate(hz)': '59'} 

dlg = gui.DlgFromDict(dictionary=exp_info, title=exp_name)
    
# If 'Cancel' is pressed, quit
if dlg.OK == False:
    core.quit()
        
# Get date and time
exp_info['date'] = data.getDateStr()
exp_info['exp_name'] = exp_name

# %% Creation of a dictonary with all the instruction

instruction_dictionary = {'instructions.text' : "Dans cette étude, vous allez voir deux images présentées simultanément d'une part et d'autre de l'écran.\n\n Appuyez sur ESPACE pour voir la suite des instructions.",
                          'instructions.text2' : "Votre tâche sera d'orienter votre regard LE PLUS VITE POSSIBLE vers l'image qui sera définie au préalable comme cible.\n\n Appuyez sur ESPACE pour voir la suite des instructions.",
                          'instructions.text3' : "Les cibles seront soit des VISAGES soit des VEHICULES.\n\n Appuyez sur ESPACE pour voir la suite des instructions.",
                          'instructions.text4' : "Nous allons d'abord commencer par un entrainement. \n\n Appuyez sur ESPACE pour commencer.",
                          'instructions.text5' : "Bravo!\nVous avez terminé l'entrainement.\nVous allez maintenant commencer l'étude.\n\nAppuyez sur ESPACE pour commencer l'étude",
                          'instructions.text6' : "Avant de continuer, veuillez vous assurez que la croix est bien en face de vous.",
                          'instructions.text7' : "Appuyez sur ESPACE pour voir la suite des instructions.",
                          'instructions_practice.faces' : "Dans ce bloc, votre tâche est de regarder les VISAGES.\n\n Veuillez fixer le ROND au centre entre les essais et garder votre tête IMMOBILE et bien positionée sur la mentionnière.\n\n Appuyez sur ESPACE pour commencer.",
                          'instructions_practice.vehicles' : "Dans ce bloc, votre tâche est de regarder les VEHICULES.\n\n Veuillez fixer le ROND au centre entre les essais et garder votre tête IMMOBILE et bien positionée sur la mentionnière.\n\n Appuyez sur ESPACE pour commencer.",
                          'instructions.faces' : "Dans ce bloc, votre tâche est de regarder les VISAGES.\n\n Veuillez fixer le ROND au centre entre les essais et garder votre tête IMMOBILE et bien positionée sur la mentionnière.\n\n Appuyez sur ESPACE pour lancer la calibration.",
                          'instructions.vehicles' : "Dans ce bloc, votre tâche est de regarder les VEHICULES.\n\n Veuillez fixer le ROND au centre entre les essais et garder votre tête IMMOBILE et bien positionée sur la mentionnière.\n\n Appuyez sur ESPACE pour lancer la calibration.",
                          'timertext.text' : "Prêt",
                          'blocktext1.text' : "Vous pouvez faire une courte pause avant le prochain bloc.\n\nVous pourrez appuyer sur ESPACE pour continuer après ",
                          'blocktext2.text' : "secondes lorsque vous serez prêt. \n\n Bloc:",
                          'calibration.text2' : "\n Maintenant, appuyez sur ENTER pour commencer l'entrainement.",
                          'calibration.text3' : "\n Maintenant, appuyez sur ENTER quatre fois pour calibrer l'eyetracker."}

# %% Connect to the EyeLink Host PC

if exp_info['dummy_mode'] == 'FALSE' :
   dummy_mode = False
else :
   dummy_mode = True

if dummy_mode:
    el_tracker = pylink.EyeLink(None)
else:
    try:
        el_tracker = pylink.EyeLink("100.1.1.1")
    except RuntimeError as error:
        print('ERROR:', error)
        core.quit()
        sys.exit()

# Open an EDF data file on the Host PC
edf_file = edf_fname + ".EDF"
try:
    el_tracker.openDataFile(edf_file)
except RuntimeError as err:
    print('ERROR:', err)
    # close the link if we have one open
    if el_tracker.isConnected():
        el_tracker.close()
    core.quit()
    sys.exit()

# Add a header text to the EDF file to identify the current experiment name
# This is OPTIONAL. If your text starts with "RECORDED BY " it will be
# available in DataViewer's Inspector window by clicking
# the EDF session node in the top panel and looking for the "Recorded By:"
# field in the bottom panel of the Inspector.
preamble_text = 'RECORDED BY %s' % os.path.basename(__file__)
el_tracker.sendCommand("add_file_preamble_text '%s'" % preamble_text)

# Configure the tracker

# Put the tracker in offline mode before we change tracking parameters
el_tracker.setOfflineMode()

# Get the software version:  1-EyeLink I, 2-EyeLink II, 3/4-EyeLink 1000,
# 5-EyeLink 1000 Plus, 6-Portable DUO
eyelink_ver = 0  # set version to 0, in case running in Dummy mode
if not dummy_mode:
    vstr = el_tracker.getTrackerVersionString()
    eyelink_ver = int(vstr.split()[-1].split('.')[0])
    # print out some version info in the shell
    print('Running experiment on %s, version %d' % (vstr, eyelink_ver))

# File and Link data control
# what eye events to save in the EDF file, include everything by default
file_event_flags = 'LEFT,RIGHT,FIXATION,SACCADE,BLINK,MESSAGE,BUTTON,INPUT'
# what eye events to make available over the link, include everything by default
link_event_flags = 'LEFT,RIGHT,FIXATION,SACCADE,BLINK,BUTTON,FIXUPDATE,INPUT'
# what sample data to save in the EDF data file and to make available
# over the link, include the 'HTARGET' flag to save head target sticker
# data for supported eye trackers
if eyelink_ver > 3:
    file_sample_flags = 'LEFT,RIGHT,GAZE,HREF,RAW,AREA,HTARGET,GAZERES,BUTTON,STATUS,INPUT'
    link_sample_flags = 'LEFT,RIGHT,GAZE,GAZERES,AREA,HTARGET,STATUS,INPUT'
else:
    file_sample_flags = 'LEFT,RIGHT,GAZE,HREF,RAW,AREA,GAZERES,BUTTON,STATUS,INPUT'
    link_sample_flags = 'LEFT,RIGHT,GAZE,GAZERES,AREA,STATUS,INPUT'
el_tracker.sendCommand("file_event_filter = %s" % file_event_flags)
el_tracker.sendCommand("file_sample_data = %s" % file_sample_flags)
el_tracker.sendCommand("link_event_filter = %s" % link_event_flags)
el_tracker.sendCommand("link_sample_data = %s" % link_sample_flags)

# Setting a smaller calibration area (use only if your screen is bigger than tracking area)
el_tracker.sendCommand("generate_default_targets = NO")
el_tracker.sendCommand("calibration_area_proportion = 0.38 0.49")
el_tracker.sendCommand("validation_area_proportion = 0.38 0.49")

# Optional tracking parameters
# Choose a calibration type, H3, HV3, HV5, HV13 (HV = horizontal/vertical),
el_tracker.sendCommand("calibration_type = HV5")

# Set a gamepad button to accept calibration/drift check target
# You need a supported gamepad/button box that is connected to the Host PC
el_tracker.sendCommand("button_function 5 'accept_target_fixation'")

# %% Monitor setup 

mon = monitors.Monitor('OLED...') #Pulls out photometer calibration settings by name.  
mon.setWidth(float(exp_info['screenwidth(cm)'])) # Cm width
mon.setDistance(float(exp_info['screendistance(cm)']))
horipix = float(exp_info['screenresolutionhori(pixels)'])
vertpix = float(exp_info['screenresolutionvert(pixels)'])
framerate = exp_info['refreshrate(hz)']
scrsize = (horipix,vertpix)
framelength = 1000/(float(framerate))
mon.setSizePix(scrsize)

# Calculate the number of degrees that correspond to a single pixel. This will
# generally be a very small value, something like 0.03.
w = float(exp_info['screenwidth(cm)'])
d = float(exp_info['screendistance(cm)'])
deg_per_px = degrees(atan2(.5 * w, d)) / (.5 * horipix)

# the candela / metersquare value
# cdm2 = (128-reduce)/255*100

# %% Open a window
win = visual.Window(monitor = mon, 
                    size = scrsize,
                    colorSpace = "rgb255",
                    color= [104.2, 104.2, 104.2], # luminance of the stimuli
                    units='pix',
                    fullscr=True,
                    allowStencil=True,
                    screen=1)
# Hide the cursor when the window is opened
win.mouseVisible=False

# get the native screen resolution used by PsychoPy
horipix, vertpix = scrsize

# Pass the display pixel coordinates (left, top, right, bottom) to the tracker
# see the EyeLink Installation Guide, "Customizing Screen Settings"
el_coords = "screen_pixel_coords = 0 0 %d %d" % (horipix - 1, vertpix - 1)
el_tracker.sendCommand(el_coords)

# Write a DISPLAY_COORDS message to the EDF file
# Data Viewer needs this piece of info for proper visualization, see Data
# Viewer User Manual, "Protocol for EyeLink Data to Viewer Integration"
dv_coords = "DISPLAY_COORDS = 0 0 %d %d" % (horipix - 1, vertpix - 1)
el_tracker.sendMessage(dv_coords)

# Configure a graphics environment (genv) for tracker calibration
genv = EyeLinkCoreGraphicsPsychoPy(el_tracker, win)
print(genv)  # print out the version number of the CoreGraphics library

# Set background and foreground colors for the calibration target
# in PsychoPy, (-1, -1, -1)=black, (1, 1, 1)=white, (0, 0, 0)=mid-gray
foreground_color = (-1, -1, -1)
background_color = win.color
genv.setCalibrationColors(foreground_color, background_color)

# Set up the calibration target

# The target could be a "circle" (default), a "picture", a "movie" clip, or a rotating "spiral". 
genv.setTargetType('circle')

# Configure the size of the calibration target (in pixels)
# this option applies only to "circle" and "spiral" targets
genv.setTargetSize(24)

# Beeps to play during calibration, validation and drift correction
# parameters: target, good, error
#     target -- sound to play when target moves
#     good -- sound to play on successful operation
#     error -- sound to play on failure or interruption
# Each parameter could be ''--default sound, 'off'--no sound, or a wav file
genv.setCalibrationSounds('', '', '')

# Request Pylink to use the PsychoPy window we opened above for calibration
pylink.openGraphicsEx(genv)

# %% Display instructions
instructions = visual.TextStim(win=win,
    pos = [0,0], 
    color = 'white',
    height = 1/deg_per_px,
    wrapWidth = horipix/2,
    alignHoriz = 'center')

instructions.text = instruction_dictionary['instructions.text']
instructions.draw()

win.flip() 
keys = event.waitKeys(keyList=['space','escape'])

# Adding other instructions
instructions = visual.TextStim(win=win,
    pos=[0,0], 
    color= 'white',
    height=1/deg_per_px,
    wrapWidth=horipix/2,
    alignHoriz='center')

instructions.text = instruction_dictionary['instructions.text2']
instructions.draw()

win.flip() 
keys = event.waitKeys(keyList=['space','escape'])

# Adding other instructions
instructions = visual.TextStim(win=win,
    pos=[0,0], 
    color= 'white',
    height=1/deg_per_px,
    wrapWidth=horipix/2,
    alignHoriz='center')

instructions.text = instruction_dictionary['instructions.text3']
instructions.draw()

# Adding examples
image_path1 = os.path.join(image_directory, "faces (41).jpg")  # Replace with your image path
bitmap_im = Image.open(image_path1)
image_stim = visual.ImageStim(win, image=bitmap_im, pos=[-20/deg_per_px, 0/deg_per_px], size= 7/deg_per_px)
image_stim.draw()

image_path2 = os.path.join(image_directory, "vehicule (191).jpg")  # Replace with your image path
bitmap_im = Image.open(image_path2)
image_stim = visual.ImageStim(win, image=bitmap_im, pos=[20/deg_per_px, 0/deg_per_px], size= 7/deg_per_px)
image_stim.draw()

win.flip() 
keys = event.waitKeys(keyList=['space','escape'])

# Adding fixation cross the verify that the participant is looking at the center of the screen
fixation_cross = visual.TextStim(win,
                                 text = "+",
                                 colorSpace = "rgb255",
                                 color=[225, 225, 225],
                                 height=2/deg_per_px,  
                                 pos=(0, 0))
fixation_cross.draw()

instructions = visual.TextStim(win=win,
    pos=[0/deg_per_px, 5/deg_per_px], 
    color= 'white',
    height=1/deg_per_px,
    wrapWidth=horipix/2)

instructions.text = instruction_dictionary['instructions.text6']
instructions.draw()

instructions_2 = visual.TextStim(win=win,
    pos=[0/deg_per_px, -5/deg_per_px], 
    color= 'white',
    height=1/deg_per_px,
    wrapWidth=horipix/2)

instructions_2.text = instruction_dictionary['instructions.text7']
instructions_2.draw()

win.flip() 
keys = event.waitKeys(keyList=['space','escape'])
# Addig other instructions
instructions = visual.TextStim(win=win,
    pos=[0,0], 
    color= 'white',
    height=1/deg_per_px,
    wrapWidth=horipix/2,
    alignHoriz='center')

instructions.text = instruction_dictionary['instructions.text4']
instructions.draw()

win.flip() 
keys = event.waitKeys(keyList=['space','escape'])

# %% Calculation of image_size

# Constants for the calculation
d = float(exp_info['screendistance(cm)'])  # eye-screen distance in cm
dd = 2 * d  # 2*d
pixelPitch = 0.315  # pixel size in mm (to change depending on your screen)
screenWidthPix = float(exp_info['screenresolutionhori(pixels)'])  # screen width in pixels
screenHeightPix = float(exp_info['screenresolutionvert(pixels)']) # screen height in pixels

# Calculate screen width and height in cm
screenWidthCm = pixelPitch * screenWidthPix / 10  # screen width in cm
screenHeightCm = pixelPitch * screenHeightPix / 10  # screen height in cm

# Desired angular size (width and height) in degrees
alphaW = float(exp_info['desired_visual_angle'])
alphaH = float(exp_info['desired_visual_angle'])

# Calculate image width and height in cm for the desired angular size
real_hori = dd * math.tan(math.radians(alphaW / 2))  # image width in cm = 2dtan(alpha/2)
real_vert = dd * math.tan(math.radians(alphaH / 2))  # image height in cm = 2dtan(alpha/2)

# Calculate image width and height in pixels for the desired size
real_hori_pix = round(real_hori * screenWidthPix / screenWidthCm)  # image width in pixels
real_vert_pix = round(real_vert * screenWidthPix / screenWidthCm)  # image height in pixels

# %% Preparing the experiment

fixation_circle = visual.Circle(win,
                             colorSpace = "rgb255",
                             fillColor=[225, 225, 225],
                             lineColor=[225, 225, 225],
                             radius=0.25/deg_per_px,  
                             pos=(0, 0))

# Number of blocks and trials for practice
prac_blocks = 2
prac_trials_per_block = 10

# Number of blocks and trials per block
num_blocks = 4
trials_per_block = 55

# Initialize trial_index before the first block
trial_index = 0

# Set the desired layout direction
layout_direction = exp_info['Layout']  

# %% Homemade functions

### Function to display target information and wait for key press
def display_target_info(win, target_text):
    # Create a visual stimulus for displaying target information
    target_info_text = visual.TextStim(win, text=target_text, color='white', height=1/deg_per_px,wrapWidth = horipix/2,pos=(0, 0))
    # Draw the target information on the window
    target_info_text.draw()
    # Display the window with the target information
    win.flip()
    # Wait for a key response (space or escape)
    event.waitKeys(keyList=['space'])

### Function to run a trial
def run_trial(win, target_image, distractor_image, layout_direction):
    
    # get a reference to the currently active EyeLink connection
    el_tracker = pylink.getEYELINK()

    # put the tracker in the offline mode first
    el_tracker.setOfflineMode()

    # clear the host screen before we draw the backdrop
    el_tracker.sendCommand('clear_screen 0')
    
    # send message to eye tracker to signal the start of the trial
    # also record trial variables to the EDF data file, for details, see Data
    # Viewer User Manual, "Protocol for EyeLink Data to Viewer Integration"
    el_tracker.sendMessage('BLOCKID %d TRIALID %d TARGET %s TARGET_POSITION %s DISTRACTOR %s DISTRACTOR_POSITION %s ' % (block,trial_index, target_image_name, target_position, distractor_image_name, distractor_position))
 
    # record_status_message : show some info on the Host PC
    status_msg = 'BLOCK_number %d TRIAL number %d TARGET %s TARGET_POSITION %s' % (block,trial_index, target_image_name, target_position)
    el_tracker.sendCommand("record_status_message '%s'" % status_msg)
    
    # drift correction
    # Perform drift correction every 10 trials
    if trial_index % 10 == 0:
        # Skip drift-check if running the script in Dummy Mode
        while not dummy_mode:
            # drift-check and re-do camera setup if ESCAPE is pressed
            try:
                error = pylink.getEYELINK().doDriftCorrect(int(horipix/2.0),
                                                           int(vertpix/2.0), 1, 1)
                # break following a success drift-check
                if error is not pylink.ESC_KEY:
                    break
            except:
                pass
            
    # put tracker in idle/offline mode before recording
    el_tracker.setOfflineMode()

    # Start recording
    # arguments: sample_to_file, events_to_file, sample_over_link,
    # event_over_link (1-yes, 0-no)
    try:
        el_tracker.startRecording(1, 1, 1, 1)
    except RuntimeError as error:
        print("ERROR:", error)
        abort_trial()
        return pylink.TRIAL_ERROR

    # Allocate some time for the tracker to cache some samples
    pylink.pumpDelay(100)
    
    # determine which eye(s) is/are available
    # 0- left, 1-right, 2-binocular
    eye_used = el_tracker.eyeAvailable()
    if eye_used == 1:
        el_tracker.sendMessage("EYE_USED 1 RIGHT")
    elif eye_used == 0 or eye_used == 2:
        el_tracker.sendMessage("EYE_USED 0 LEFT")
        eye_used = 0
    else:
        print("Error in getting the eye information!")
        return pylink.TRIAL_ERROR
    
    ## Beginning of the actual experiment 
    # 1. Generate a random fixation duration between 0.8 and 1.6 seconds
    fixation_duration = rnd.uniform(0.8, 1.6) 
    fixation_circle.draw() # Display the fixation cross
    win.flip()
    el_tracker.sendMessage('FIXATION_DISPLAY %d' )
    core.wait(fixation_duration) # Wait for the fixation duration to pass
    
    # 2. Clear the window and wait for a brief period (0.2 seconds)
    win.flip()
    el_tracker.sendMessage('GAP_DISPLAY %d')
    core.wait(0.2)
    
    # 3. Draw and display the target and distractor images for 0.4 seconds
    target_image.draw()
    distractor_image.draw()
    win.flip()
    el_tracker.sendMessage('TARGET_DISPLAY %d')
    core.wait(0.4)
    
    # 4. Clear the window and wait for 1.0 second (end of the trial)
    win.flip()
    el_tracker.sendMessage('TARGET_END %d')
    core.wait(1.0)
    el_tracker.sendMessage('ISI_END %d')
    
    # stop recording; add 100 msec to catch final events before stopping
    pylink.pumpDelay(100)
    el_tracker.stopRecording()
                
    # send interest area messages to record in the EDF data file
    # first we define left, top, right and bottom
    # Calculate ROI dimensions in pixels
    extra_degrees = 1  # Additional 1 degree margin
    extra_pixels = int(extra_degrees * deg_per_px)
    roi_width = real_hori_pix + 2 * extra_pixels  # Extra pixels on both sides
    roi_height = real_vert_pix + 2 * extra_pixels  # Extra pixels on both sides
    
    # Calculate ROI position
    left = int(float(exp_info['screenresolutionhori(pixels)'])/2.0) - roi_width / 2 + extra_pixels
    top = int(float(exp_info['screenresolutionvert(pixels)'])/2.0) - roi_height / 2 + extra_pixels
    right = int(float(exp_info['screenresolutionhori(pixels)'])/2.0) + roi_width / 2 + extra_pixels
    bottom = int(float(exp_info['screenresolutionvert(pixels)'])/2.0) + roi_height / 2 + extra_pixels
    
    # here we draw a rectangular IA, for illustration purposes
    # format: !V IAREA RECTANGLE <id> <left> <top> <right> <bottom> [label]
    # for all supported interest area commands, see the Data Viewer Manual,
    # "Protocol for EyeLink Data to Viewer Integration" 
    ia_pars = (1, left, top, right, bottom, 'screen_center')
    el_tracker.sendMessage('!V IAREA RECTANGLE %d %d %d %d %d %s' % ia_pars)

    # send a 'TRIAL_RESULT' message to mark the end of trial
    el_tracker.sendMessage('TRIAL_RESULT %d' % pylink.TRIAL_OK)
    
    if 'escape' in keys:
        win.close()
    
### Function that draws a break between blocks, shows which block they are at,
# and takes as arguments block no, the break time between each block, and a
# long break at every x block.
def block_break(block_no, totalblocks, timershort, timerlong):
    if block_no == totalblocks:
        return
    # Determine the timer duration based on block number
    timer = timerlong if block_no % half_blocks == 0 else timershort
    
    # Create a visual stimulus for the block's text
    blocktext = visual.TextStim(
        win=win,
        height=1/deg_per_px,
        wrapWidth=horipix/2,
        alignHoriz='center')
  
    blocktext.text = instruction_dictionary['blocktext1.text'] + str(timer) + instruction_dictionary['blocktext2.text'] + str(block_no) + "/" + str(totalblocks)
    
    # Create a visual stimulus for the timer text
    timertext = visual.TextStim(
        win=win,
        height=1/deg_per_px,
        pos=[0, -7/deg_per_px],
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

# %% Pylink functions

### Function to clear the screen
def clear_screen(win):
    """ clear up the PsychoPy window"""

    win.fillColor = genv.getBackgroundColor()
    win.flip()

### Function to show the instructions
def show_msg(win, text, wait_for_keypress=True):
    """ Show task instructions on screen"""

    msg = visual.TextStim(win, text,
                          color= 'white',
                          height=1/deg_per_px,
                          wrapWidth=horipix/2,
                          alignHoriz='center')
    clear_screen(win)
    msg.draw()
    win.flip()

    # wait indefinitely, terminates upon any key press
    if wait_for_keypress:
        event.waitKeys()
        clear_screen(win)

### Function that terminates the task gracefully and retrieve the EDF data file
def terminate_task():
    """ 
    file_to_retrieve: The EDF on the Host that we would like to download
    win: the current window used by the experimental script
    """

    el_tracker = pylink.getEYELINK()

    if el_tracker.isConnected():
        # Terminate the current trial first if the task terminated prematurely
        error = el_tracker.isRecording()
        if error == pylink.TRIAL_OK:
            abort_trial()

        # Put tracker in Offline mode
        el_tracker.setOfflineMode()

        # Clear the Host PC screen and wait for 500 ms
        el_tracker.sendCommand('clear_screen 0')
        pylink.msecDelay(500)

        # Close the edf data file on the Host
        el_tracker.closeDataFile()

        # Show a file transfer message on the screen
        msg = 'EDF data is transferring from EyeLink Host PC...'
        show_msg(win, msg, wait_for_keypress=False)

        # Download the EDF data file from the Host PC to a local data folder
        # parameters: source_file_on_the_host, destination_file_on_local_drive
        local_edf = os.path.join(session_folder, session_identifier + '.EDF')
        try:
            el_tracker.receiveDataFile(edf_file, local_edf)
        except RuntimeError as error:
            print('ERROR:', error)

        # Close the link to the tracker.
        el_tracker.close()

    # close the PsychoPy window
    win.close()

    # quit PsychoPy
    core.quit()
    sys.exit()

### Function to abort trials
def abort_trial():
    """Ends recording """

    el_tracker = pylink.getEYELINK()

    # Stop recording
    if el_tracker.isRecording():
        # add 100 ms to catch final trial events
        pylink.pumpDelay(100)
        el_tracker.stopRecording()

    # clear the screen
    clear_screen(win)
    # Send a message to clear the Data Viewer screen
    bgcolor_RGB = (116, 116, 116)
    el_tracker.sendMessage('!V CLEAR %d %d %d' % bgcolor_RGB)

    # send a message to mark trial end
    el_tracker.sendMessage('TRIAL_RESULT %d' % pylink.TRIAL_ERROR)

    return pylink.TRIAL_ERROR    

# %% Start calibration

# Set up the camera and calibrate the tracker

if dummy_mode:
    task_msg = instruction_dictionary['calibration.text2']
else:
    task_msg = instruction_dictionary['calibration.text3']
show_msg(win, task_msg)

# skip this step if running the script in Dummy Mode
if not dummy_mode:
    try:
        el_tracker.doTrackerSetup()
    except RuntimeError as err:
        print('ERROR:', err)
        el_tracker.exitCalibration()

# %% Create a unique filename for the experiment data

datapath = 'data'
if not os.path.isdir(datapath):
    os.makedirs(datapath)
data_fname = f"{exp_info['participant']}_{exp_info['Layout']}_{exp_info['date']}.csv"
data_fname = os.path.join(datapath, data_fname)

# Open the file for writing and create a CSV writer with the specified fieldnames
fieldnames = list(exp_info.keys()) + ['block', 'trial_index', 'target_image_name', 'target_position', 'distractor_image_name', 'distractor_position']
f = open(data_fname,'w',encoding='UTF8', newline='')
writer=csv.DictWriter(f, fieldnames=fieldnames)
writer.writeheader()


# %% Assignment of images for both the practice and the main experiment

# 240 images --> 20 for practice and 220 for main

# Randomly select 10 images per category for practice
practice_face = random.sample(face_images, 10)
practice_vehicle = random.sample(vehicle_images, 10)

# Create a dictionnary to store the pairs and their positions
practice_pairs={'target_face': [], 'target_vehicle': []}

# defining half to pseudo-randomize the positions:
# in target_face : (first half is 0 and other half is 1)
# in target_vehicle : (first half is 1 and other half is 0)
half = len(practice_face) // 2 # we are using face list as both lists are the same length

# Use a loop to create the pairs and assign them a position
for target in list(practice_pairs.keys()):
    for im_index in range(len(practice_face)):
        matching = 0 if im_index < half else 1
        practice_pairs[target].append({'im1name': practice_face[im_index], 'im2name': practice_vehicle[im_index], 'position': matching})

# Shuffling the order of the items in both dictionnaries
rnd.shuffle(practice_pairs['target_face'])
rnd.shuffle(practice_pairs['target_vehicle'])

# Assign the rest of the images for the main experiment
main_face = [img for img in face_images if img not in practice_face] # 110 face
main_vehicle = [img for img in vehicle_images if img not in practice_vehicle] # 110 vehicle

# Create a dictionnary to store the pairs and their positions
main_pairs={'target_face': [], 'target_vehicle': []}

# defining half to pseudo-randomize the positions:
# in target_face : (first half is 0 and other half is 1)
# in target_vehicle : (first half is 1 and other half is 0)
half = len(main_face) // 2

# Use a loop to create the pairs and assign them a position
for target in list(main_pairs.keys()):
    for im_index in range(len(main_face)): # we are using face list as both lists are the same length
        matching = 0 if im_index < half else 1
        main_pairs[target].append({'im1name': main_face[im_index], 'im2name': main_vehicle[im_index], 'position': matching})

# Shuffling the order of the items in both dictionnaries
rnd.shuffle(main_pairs['target_face'])
rnd.shuffle(main_pairs['target_vehicle']) 
# %% Practice loop

# Define the order of blocks (0 represents face-target, 1 represents vehicle-target)
half_pracblocks = prac_blocks // 2
group1 = [0] * half_pracblocks
group2 = [1] * half_pracblocks

# Randomly decide the order of groups
if random.choice([True, False]):
    condition_order = group1 + group2
else:
    condition_order = group2 + group1

# Initialize variables to store the previous condition_order
prev_condition_order = None

# Loop through blocks
for block in range(prac_blocks):
    if condition_order[block] == 0:
        block_target = 'face'
        target_text = instruction_dictionary['instructions_practice.faces']
    else:
        block_target = 'vehicle'
        target_text = instruction_dictionary['instructions_practice.vehicles']
    
    target_info_text = visual.TextStim(win, text=target_text, color='white', height=1/deg_per_px,wrapWidth = horipix/2,pos=(0, 0))
    # Draw the target information on the window
    target_info_text.draw()
    # Display the window with the target information
    win.flip()
    # Wait for a key response (space or escape)
    event.waitKeys(keyList=['space'])
    
    # Loop through trials within each block
    for trial in range(prac_trials_per_block):    
        if block_target == 'face':
            target_image_path = practice_pairs['target_face'][trial]['im1name'] # take a face image from a pair in the target_face dictionnary
            target_image_name = os.path.basename(practice_pairs['target_face'][trial]['im1name']) # store it's name for csv file
            target_pos = practice_pairs['target_face'][trial]['position'] # take the position assigned with the pair
            distractor_image_path = practice_pairs['target_face'][trial]['im2name'] # take a vehicle image from a pair in the target_face dictionnary
            distractor_image_name = os.path.basename(practice_pairs['target_face'][trial]['im2name']) # store it's name for csv file

        else:
            target_image_path = practice_pairs['target_vehicle'][trial]['im2name'] # take a vehicle image from a pair in the target_vehicle dictionnary
            target_image_name = os.path.basename(practice_pairs['target_vehicle'][trial]['im2name']) # store it's name for csv file
            target_pos = practice_pairs['target_vehicle'][trial]['position'] # take the position assigned with the pair
            distractor_image_path = practice_pairs['target_vehicle'][trial]['im1name'] # take a face image from a pair in the target_vehicle dictionnary
            distractor_image_name = os.path.basename(practice_pairs['target_vehicle'][trial]['im1name']) # store it's name for csv file
        
        # Draw the images
        target_image = visual.ImageStim(win, image=target_image_path, size=(real_hori_pix, real_vert_pix))
        distractor_image = visual.ImageStim(win, image=distractor_image_path, size=(real_hori_pix, real_vert_pix))
                
        # If it's not, assign new positions and store them in the dictionary
        if layout_direction == 'vertical':
            if target_pos == 0:
                target_position = (0, 15/deg_per_px)  # Position on the top
                target_position_name = 'top'
            else:
                target_position = (0, -15/deg_per_px)  # Position on the bottom
                target_position_name = 'bottom'
                
        elif layout_direction == 'horizontal':
            if target_pos == 0:
                target_position = (15/deg_per_px, 0)  # Position on the right
                target_position_name = 'right'
            else:
                target_position = (-15/deg_per_px, 0)  # Position on the left
                target_position_name = 'left'

        target_image.pos = target_position
        distractor_position = (-target_position[0], -target_position[1]) # opposite direction than the target
        distractor_image.pos = distractor_position
        
        # Now we do the same for the distractor
        if target_position_name == 'top':
            distractor_position_name = 'bottom'
        elif target_position_name == 'bottom':
            distractor_position_name = 'top'
        elif target_position_name == 'right':
            distractor_position_name = 'left'
        elif target_position_name == 'left':
            distractor_position_name = 'right'  
                       
        run_trial(win, target_image, distractor_image, layout_direction)
        trial_index += 1
        
        # Print trials info in console
        print(f"Trial Number: {trial_index}, Target Position: {target_position_name}, Target Name: {target_image_name}")
        
        trial_data = {
        'block': block,
        'trial_index': trial_index,
        'target_image_name': target_image_name,
        'target_position': target_position_name,
        'distractor_image_name': distractor_image_name,
        'distractor_position': distractor_position_name}
        
        # Close the window if escape or space keys are pressed
        keys = event.getKeys()
        if 'escape' in keys:
            abort_trial()
            win.close()
            f.close()

        # Write data to the .csv file
        combined_data = {**exp_info, **trial_data}
        writer.writerow(combined_data)

# Adding further instructions
instructions = visual.TextStim(win=win,
    pos=[0,0], 
    wrapWidth=None, height= 1/deg_per_px, alignHoriz='center', color = 'white')


instructions.text = instruction_dictionary['instructions.text5']
instructions.draw()

win.flip()
keys = event.waitKeys(keyList=['space','escape'])#core.wait(.1)

# %% Experimental loop

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

# Initialize indexes to track the number of the drawn image
# we are doing this because otherwise the loop will always 
# go back to the beginning of the dictonnary, repeating twice the same image 
# with the same order
face_trial = 0
vehicle_trial = 0

# Loop through blocks
for block in range(num_blocks):
    if condition_order[block] == 0:
        block_target = 'face'
        target_text = instruction_dictionary['instructions.faces']
    else:
        block_target = 'vehicle'
        target_text = instruction_dictionary['instructions.vehicles']
    
    target_info_text = visual.TextStim(win, text=target_text, color='white', height=1/deg_per_px,wrapWidth = horipix/2,pos=(0, 0))
    # Draw the target information on the window
    target_info_text.draw()
    # Display the window with the target information
    win.flip()
    # Wait for a key response (space or escape)
    event.waitKeys(keyList=['space'])
        
    # Perform calibration after each block except the last one
    if not dummy_mode and block < num_blocks:
        try:
            el_tracker.doTrackerSetup()
        except RuntimeError as err:
            print('ERROR:', err)
            el_tracker.exitCalibration()

    # Loop through trials within each block
    for trial in range(trials_per_block):
        if block_target == 'face':
            target_image_path = main_pairs['target_face'][face_trial]['im1name'] # take a face image from a pair in the target_face dictionnary
            target_image_name = os.path.basename(main_pairs['target_face'][face_trial]['im1name']) # store it's name for csv file
            target_pos = main_pairs['target_face'][face_trial]['position'] # take the position assigned with the pair
            distractor_image_path = main_pairs['target_face'][face_trial]['im2name'] # take a vehicle image from a pair in the target_face dictionnary
            distractor_image_name = os.path.basename(main_pairs['target_face'][face_trial]['im2name']) # store it's name for csv file
            face_trial += 1 # increase the index number by 1

        else:
            target_image_path = main_pairs['target_vehicle'][vehicle_trial]['im2name'] # take a vehicle image from a pair in the target_vehicle dictionnary
            target_image_name = os.path.basename(main_pairs['target_vehicle'][vehicle_trial]['im2name']) # store it's name for csv file
            target_pos = main_pairs['target_vehicle'][vehicle_trial]['position'] # take the position assign with the pair
            distractor_image_path = main_pairs['target_vehicle'][vehicle_trial]['im1name'] # take a face image from a pair in the target_vehicle dictionnary
            distractor_image_name = os.path.basename(main_pairs['target_vehicle'][vehicle_trial]['im1name']) # store it's name for csv file
            vehicle_trial += 1 # increase the index number by 1
            
        # Draw the images
        target_image = visual.ImageStim(win, image=target_image_path, size=(real_hori_pix, real_vert_pix))
        distractor_image = visual.ImageStim(win, image=distractor_image_path, size=(real_hori_pix, real_vert_pix))
               
        # If it's not, assign new positions and store them in the dictionary
        if layout_direction == 'vertical':
            if target_pos == 0:
                target_position = (0, 15/deg_per_px)  # Position on the top
                target_position_name = 'top'
            else:
                target_position = (0, -15/deg_per_px)  # Position on the bottom
                target_position_name = 'bottom'
                
        elif layout_direction == 'horizontal':
            if target_pos == 0:
                target_position = (15/deg_per_px, 0)  # Position on the right
                target_position_name = 'right'
            else:
                target_position = (-15/deg_per_px, 0)  # Position on the left
                target_position_name = 'left'

        target_image.pos = target_position
        distractor_position = (-target_position[0], -target_position[1]) # opposite direction than the target
        distractor_image.pos = distractor_position
        
        # Now we do the same for the distractor
        if target_position_name == 'top':
            distractor_position_name = 'bottom'
        elif target_position_name == 'bottom':
            distractor_position_name = 'top'
        elif target_position_name == 'right':
            distractor_position_name = 'left'
        elif target_position_name == 'left':
            distractor_position_name = 'right'  
                       
        run_trial(win, target_image, distractor_image, layout_direction)
        trial_index += 1
        
        # Print trials info in console
        print(f"Trial Number: {trial_index}, Target Position: {target_position_name}, Target Name: {target_image_name}")
        
        trial_data = {
        'block': block,
        'trial_index': trial_index,
        'target_image_name': target_image_name,
        'target_position': target_position_name,
        'distractor_image_name': distractor_image_name,
        'distractor_position': distractor_position_name}
    
        # Write data into the .csv file
        combined_data = {**exp_info, **trial_data}
        writer.writerow(combined_data)
        
    # Run block break function with a minimum of 10 seconds
    block_break(block + 1, num_blocks, 10, 30)  # Adjust the timer values as needed

f.close()    
# Disconnect, download the EDF file, then terminate the task
terminate_task()
