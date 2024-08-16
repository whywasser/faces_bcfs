#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division  # enable division with "/"
from psychopy import visual, core, data, event, logging, sound, gui

from psychopy.constants import *  # things like STARTED, FINISHED
import random as rand
from PIL import Image
import numpy  # as np  # whole numpy lib is available, prepend 'np.'
from numpy import sin, cos, tan, log, log10, pi, average, sqrt, std, deg2rad, rad2deg, linspace, asarray
from numpy.random import random, randint, normal, shuffle
import os  # handy system and path functions
from os import listdir
import copy

# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)

# Store info about the experiment session
expName = 'Continuous Flash Suppression Experiment' 
expInfo = {
    # 'ParticipantID': '',
    # 'Age': '',
    # 'Gender': '',
    # 'Ocular Dominance': ''
}
#dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
dlg = gui.Dlg(title = expName)
dlg.addField('Participant ID:')
dlg.addField('Age:')
dlg.addField('Gender:')
dlg.addField('Ocular Dominance:', choices = ['l', 'r'])
dlg.addField('Normal or corrected-to-normal vision:', choices = ['yes', 'no'])
dlg.addField('Condition:', choices = ['cfs','nocfs'])
dlg.show()
if not dlg.OK:
    core.quit()  # user pressed cancel
expInfo['ID'] = dlg.data[0]
expInfo['Age'] = dlg.data[1]
expInfo['Gender'] = dlg.data[2]
expInfo['Ocular Dominance'] = dlg.data[3]
expInfo['nor_vis'] = dlg.data[4]
expInfo['condition'] = dlg.data[5]
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName

def set_exp_info():
    global stim_color
    global flash_color
    if expInfo['condition'] == 'cfs' and expInfo['Ocular Dominance'] == 'l':
        stim_color = [1, 0, 0] 
        flash_color = [0, 1, 1] 
        expInfo['stim_color'] = 'red' 
        expInfo['flash_color'] = 'cyan' 
    elif expInfo['condition'] == 'cfs' and expInfo['Ocular Dominance'] == 'r':
        stim_color = [0, 1, 1]
        flash_color = [1, 0, 0]
        expInfo['stim_color'] = 'cyan'
        expInfo['flash_color'] = 'red'
    else:
        stim_color = [1, 1, 1]
        flash_color = [1, 1, 1]
        expInfo['stim_color'] = 'color'
        expInfo['flash_color'] = 'color'

    
set_exp_info()


# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filepath = _thisDir + os.sep + 'data'
file = 'logfile_' + expInfo['ID'] + '_' + expInfo['condition']
filename = os.path.join (filepath, file)
#define custom listdir functions, so hidden files are excluded
def listdir_nohidden(path):
    list = []
    for f in os.listdir(path):
        if not f.startswith('.'):
            list.append(f)
    return list

listpath = _thisDir + os.sep + 'lists'
stimulus_lists = listdir_nohidden(listpath)
# stimulus list to load
listchoice = rand.choice(stimulus_lists)
listparticipant = os.path.join(listpath, listchoice)
# folder with stimuli
dirstim = _thisDir + os.sep + 'stimuli'

# folder with mondrians
dirmondrians = _thisDir + os.sep + 'Mondrians'

# folder with checkerboards for blanks
dirmask = _thisDir + os.sep + 'masks'

# define max num of trials you want 
trialmax = 64

# trials at which a pause should occur
when_Pause = numpy.arange(32, 33, 1)
num_pause = 1

# define how long the pause should be at least
duration_pause = 0

# duration of FIX CROSS BEFORE each trial
time_before = 30  # 30 frames at 60Hz are 500 ms

# duration of BLANK AFTER each trial
time_blank = 18  # 18 frames at 60Hz are 300 ms

# max opacity of stimuli
max_opacity = 0.6

# max opacity of flash
max_opacity_flash = 1

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
                                 extraInfo=expInfo, runtimeInfo=None,
                                 originPath=None,
                                 savePickle=True, saveWideText=True,
                                 dataFileName=filename)
# save a log file for detail verbose info
# this outputs to the screen, not a file
logging.console.setLevel(logging.WARNING)

endExpNow = False  # flag for 'escape' or other condition => quit the exp


# Set up the Window
win = visual.Window(size=(640, 400),
                    fullscr=True, screen=0, allowGUI=False, allowStencil=False,
                    monitor='testMonitor', color=[0, 0, 0], colorSpace='rgb',
                    blendMode='avg', useFBO=True, units='pix')
# store frame rate of monitor if we can measure it successfully
expInfo['frameRate'] = win.getActualFrameRate()
if expInfo['frameRate'] != None:
    frameDur = 1.0/round(expInfo['frameRate'])
else:
    frameDur = 1.0/60.0  # couldn't get a reliable measure so guess

# set_colors()
# Colors used during the experiment.
# Color variables end with _c.
def set_colors():
    global sc_c  # screen color
    global f_c  # frame color
    global f2_c  # frame 2 color
    global sq_c  # square color
    global t_c  # text color
    global c_c  # circle color

    sc_c = [.002, .002, .002]
    f_c = [-1, -1, -1]  # black
    f2_c = [1, 1, 1]    # white
    sq_c = [.002, .002, .002]
    t_c = [1, 1, 1]     # white
    c_c = 'red'

# initiate colors
set_colors()


# define response buttons/hand
left_hand = '''up'''
right_hand = '''down'''
correct_up = 'z'
correct_down = 'g'


# set_sizes()
def set_sizes():
    global f_s  # frame size (square) (frame surrounding the stimulus)
    global f2_s  # frame 2 size (square) (frame surrounding the stimulus)
    global sq_s  # square size (square where the stimulus is shown)
    global l_s  # line size (the width of the line surrounding the stimulus)
    global fix_s  # size of fixation crosses on top of stimuli
    # size of the face (useful when showing smaller face above/below fixation
    # cross)
    global pic_s
    f_s = 840
    f2_s = 820
    sq_s = 800
    l_s = 20
    fix_s = 60
#    pic_s = sq_s/2
    pic_s = sq_s

# data init
set_sizes()

def set_positions():
    # position of the text and image stimuli (up or down according experiment settings).
    global s_p
    # position of the flash stimulus (up or down according experiment settings).
    global f_p
    global txt_above_f_p  # position of the reminder for the button for above.
    global txt_below_f_p  # position of the reminder for the button for below.
    global txt_above_s_p  # position of the reminder for the button for above.
    global txt_below_s_p  # position of the reminder for the button for below.
    # start position of vertical lines sticking out of frame
    global line_left_start
    global line_left_end
    global line_right_start
    global line_right_end
    offset = 0  # To displace the center from the real center.
    # Positive offset approach to the screen center
    # while negative offset move away the screen center.
    center = offset
    s_p = [0, 0]
    f_p = [0, 0]
#  txt_above_f_p = [0, 250]
#  txt_below_f_p = [0, -250]
#  txt_above_s_p = [0, 250]
#  txt_below_s_p = [0, -250]
    txt_above_s_p = [-520, 0]
    txt_below_s_p = [520, 0]

    line_left_start = (- f_s/2 - 50, 0)
    line_left_end = (- f_s/2, 0)
    line_right_start = (+ f_s/2, 0)
    line_right_end = (+ f_s/2 + 50, 0)


# define timings
def jittery(x):
    # The duration (in frames) before the stimulus presentation
    global before_t
    global fade_i_t  # The duration (in frames) of the fade in of stimulus
    global inside_t
    global fade_o_t  # The duration (in frames) of the fade out of stimulus
    global after_t  # The duration (in frames) after stimulus presentation
    global stim_t   # The duration (in frames) of the stimulus (in + inside + out)
    global total_t     # The duration (in frames) of a stimulus presentation (before + stimulus + after)
    global fade_i_end_t  # The frame end of the fade in
    global fade_o_beg_t  # The frame end of the inside
    global fade_o_end_t  # The frame end of the fade out
    global f_t  # The duration (in frames) of a flash image presentation
    
    global before_f
    global fade_i_f  # The duration (in frames) of the fade in of flash
    global inside_f
    global fade_o_f  # The duration (in frames) of the fade out of flash
    global after_f  # The duration (in frames) after flash presentation
    global stim_f   # The duration (in frames) of the flash (in + inside + out)
    global total_f     # The duration (in frames) of a flash presentation (before + stimulus + after)
    global fade_i_end_f  # The frame end of the fade in
    global fade_o_beg_f  # The frame end of the inside
    global fade_o_end_f  # The frame end of the fade out

    fps = 60  # frames per second
    
    # for stim
    before_t = 0 * fps
    fade_i_t = 3 * fps
    inside_t = 7 * fps
    fade_o_t = 0 * fps
    after_t = 0 * fps
    stim_t = fade_i_t + inside_t + fade_o_t
    total_t = before_t + stim_t + after_t
    fade_i_end_t = before_t + fade_i_t
    fade_o_beg_t = fade_i_end_t + inside_t
    fade_o_end_t = before_t + stim_t
    
    # for flash
    before_f = 0 * fps
    fade_i_f = 0 * fps
    inside_f = 4 * fps
    fade_o_f = 6 * fps
    after_f = 0 * fps
    stim_f = fade_i_f + inside_f + fade_o_f
    total_f = before_f + stim_f + after_f
    fade_i_end_f = before_f + fade_i_f
    fade_o_beg_f = fade_i_end_f + inside_f
    fade_o_end_f = before_f + stim_f
    
    f_t = 6


# data_init
# set_exp_info()
set_positions()

# first create a list of the file names

nums = list(map(str, range(1, 101)))
names = list(map(str, numpy.repeat(['Mondrian'], 100)))
Mondrian_names = []
for x in range(0, 100):
    #    print names[x] +  nums[x]
    Mondrian_names.append(names[x] + nums[x] + '.jpg')

names1 = list(map(str, numpy.repeat(['frame'], 100)))
Mondrian_s_names = []
for x in range(0, 100):
    #    print names[x] +  nums[x]
    Mondrian_s_names.append(names1[x] + nums[x] + '.png')
# then load them all
flash = []
for x in range(0, 100):
    flash.append(visual.ImageStim(win,
                                  name='',
                                  image=os.path.join(dirmondrians, Mondrian_names[x]),
                                  mask=None,
                                  size=sq_s, pos=s_p,
                                  color=flash_color,   # blue
                                  colorSpace='rgb', opacity=1,
                                  flipHoriz=False, flipVert=False,
                                  texRes=128, interpolate=True))

flash1 = []
for x in range(0, 100):
    flash1.append(visual.ImageStim(win,
                                  name='flash1',
                                  image=os.path.join(dirmondrians, Mondrian_s_names[x]),
                                  mask=None,
                                  size=sq_s, pos=s_p,
                                  color=flash_color,   # blue
                                  colorSpace='rgb', opacity=1,
                                  flipHoriz=False, flipVert=False,
                                  texRes=128, interpolate=True))
#    print "which mondrian - " + flash[x].image   # to check


# print "length flash " + str(len(flash))   # to check

#############     #############       #############      #############
#############     #############       #############      #############

# function to establish position of face (based on trial list)

def set_pos_ver(x):
    if  x == 'up':
        pos_ver = sq_s/4
    elif x == 'down':
        pos_ver =  -sq_s/4
    return pos_ver
    
       
# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
# to track time remaining of each (non-slip) routine
routineTimer = core.CountdownTimer()


# Initialize components for Routine "Instructions"
Instructions1Clock = core.Clock()
Instructions3Clock = core.Clock()

text_for_instruction1 = '''Welcome! By continuing, you confirm that you have received 
information about the study and give your informed consent to participate.
If you wish to exit, press ESC at any time. To continue, press SPACE.
'''

text_for_instruction3 = '''
Please keep your gaze on the fixation cross for the duration of the experiment.

Images will slowly appear between the flashing patterns.

If you see a stimulus on the upper half of the screen, press %s 

If it appears on the lower half press %s 

Press SPACE to start the experiment''' % (correct_up, correct_down)


text_instructions1_s = visual.TextStim(win=win, ori=0, name='text_instructions1_s',
                                       font=u'Arial',
                                       pos=[s_p[0], 0], height=25, wrapWidth=float(win.size[0]/3),
                                       color=u'white', colorSpace='rgb', opacity=1,
                                       depth=1.0,
                                       text=text_for_instruction1)

text_instructions3_s = visual.TextStim(win=win, ori=0, name='text_instructions3_s',
                                       text=text_for_instruction3,    font=u'Arial',
                                       pos=[s_p[0], 0], height=25, wrapWidth=float(win.size[0]/3),
                                       color=u'white', colorSpace='rgb', opacity=1,
                                       depth=1.0)


# Initialize components for Routine "pause"
PauseClock = core.Clock()
text_pause_s = visual.TextStim(win=win, ori=0, name='text_pause_s',
                               text=u'',  font=u'Arial',  # the text is defined at each pause
                               pos=[s_p[0], 0], height=30, wrapWidth=float(win.size[0]/3),
                               color=u'white', colorSpace='rgb', opacity=1,
                               depth=0.0)


# Initialize components for Routine "pretrial"
pretrialClock = core.Clock()
square_f_i = visual.Rect(win=win, name='square_f_i', units='pix',
                         width=sq_s, height=sq_s,
                         ori=0, pos=f_p,
                         lineWidth=0, lineColor=sc_c, 
                         fillColor=sc_c, colorSpace='rgb',
                         opacity=1, interpolate=True)


# Initialize components for Routine "trial"
trialClock = core.Clock()
frame_s_i = visual.Rect(win=win, name='frame_s_i', units='pix',
                        width=f_s, height=f_s,
                        ori=0, pos=s_p,
                        lineWidth=0, lineColor=f_c, 
                        fillColor=f_c, colorSpace='rgb',
                        opacity=1, interpolate=True)
frame2_s_i = visual.Rect(win=win, name='frame2_s_i', units='pix',
                         width=f2_s, height=f2_s,
                         ori=0, pos=s_p,
                         lineWidth=0, lineColor=f2_c, 
                         fillColor=f2_c, colorSpace='rgb',
                         opacity=1, interpolate=True)

line_left_s_i = visual.Line(win=win, name='line_left_s_i', units='pix',
                            start=line_left_start, end=line_left_end,
                            ori=0, pos=s_p,
                            lineWidth=10, lineColor=f_c, 
                            fillColor=None, colorSpace='rgb',
                            opacity=1, depth=-2.0, interpolate=True)
line_right_s_i = visual.Line(win=win, name='line_right_s_i', units='pix',
                             start=line_right_start, end=line_right_end,
                             ori=0, pos=s_p, lineWidth=10, lineColor=f_c, 
                             fillColor=None, colorSpace='rgb',
                             opacity=1, depth=-2.0, interpolate=True)
line_above_s_i = visual.Line(win=win, name='line_above_s_i', units='pix',
                             start=line_left_start, end=line_left_end,
                             ori=90, pos=s_p,
                             lineWidth=10, lineColor=f_c, 
                             fillColor=None, colorSpace='rgb',
                             opacity=1, depth=-2.0, interpolate=True)
line_below_s_i = visual.Line(win=win, name='line_below_horz_s_i', units='pix',
                             start=line_right_start, end=line_right_end,
                             ori=90, pos=s_p, lineWidth=10, lineColor=f_c, 
                             fillColor=None, colorSpace='rgb',
                             opacity=1, depth=-2.0, interpolate=True)

square_s_i = visual.Rect(win=win, name='square_s_i', units='pix',
                         width=sq_s, height=sq_s,
                         ori=0, pos=s_p,
                         lineWidth=0, lineColor=sc_c, 
                         fillColor=sq_c,  # change color of square
                         colorSpace='rgb',
                         opacity=1, interpolate=True)
image = visual.ImageStim(win=win, name='image',
                         image='sin', mask=None,
                         ori=0,
                         #size = [2,2],
                         color=stim_color,   # change color of image
                         colorSpace='rgb', opacity=1,
                         flipHoriz=False, flipVert=False,
                         texRes=128, interpolate=True)
image.size *= [2,2]

fix_cross_stim_side = visual.TextStim(win=win, ori=0, name='text',
                                      text='+',    font='Arial',
                                      pos=s_p, height=fix_s, wrapWidth=None,
                                      color='black', colorSpace='rgb', opacity=1,
                                      depth=-4.0)


# Initialize components for Routine "posttrial"
posttrialClock = core.Clock()
square_f_i = visual.Rect(win=win, name='square_f_i', units='pix',
                         width=sq_s, height=sq_s,
                         ori=0, pos=f_p,
                         lineWidth=0, lineColor=sc_c, 
                         fillColor=sc_c, colorSpace='rgb',
                         opacity=1, interpolate=True)
scramble_s = visual.ImageStim(win=win, name='image',
                              image='sin', mask=None,
                              ori=0, pos=f_p, size=sq_s,
                              color=[1, 1, 1], colorSpace='rgb', opacity=1,
                              flipHoriz=False, flipVert=False,
                              texRes=128, interpolate=True, depth=-2.0)


# Initialize components for Routine "thanks"
thanksClock = core.Clock()
thanksText_s = visual.TextStim(win=win, ori=0, name='thanksText_s',
                               text='This is the end of this part.\n\nThanks for participating!', font='arial',
                               pos=s_p, height=30, wrapWidth=float(win.size[0]/3),
                               color='white', colorSpace='rgb', opacity=1,
                               depth=-4.0)

#------Prepare to start Routine "Instructions1"-------
t = 0
Instructions1Clock.reset()  # clock
frameN = -1
# update component parameters for each repeat
# create an object of type KeyResponse
key_resp_inst1 = event.BuilderKeyResponse()
key_resp_inst1.status = NOT_STARTED
# keep track of which components have finished
Instructions1Components = []
Instructions1Components.append(text_instructions1_s)
Instructions1Components.append(key_resp_inst1)
for thisComponent in Instructions1Components:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED


#-------Start Routine "Instructions1"-------
continueRoutine = True
while continueRoutine:
    # get current time
    t = Instructions1Clock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame

    # *text_instructions1_s* updates
    if t >= 0.0 and text_instructions1_s.status == NOT_STARTED:
        # keep track of start time/frame for later
        # underestimates by a little under one frame
        text_instructions1_s.tStart = t
        text_instructions1_s.frameNStart = frameN  # exact frame index
        text_instructions1_s.setAutoDraw(True)

    # *key_resp_inst1* updates
    if t >= 0.0 and key_resp_inst1.status == NOT_STARTED:
        # keep track of start time/frame for later
        key_resp_inst1.tStart = t  # underestimates by a little under one frame
        key_resp_inst1.frameNStart = frameN  # exact frame index
        key_resp_inst1.status = STARTED
        # keyboard checking is just starting
        key_resp_inst1.clock.reset()  # now t=0
        event.clearEvents(eventType='keyboard')
    if key_resp_inst1.status == STARTED:
        theseKeys = event.getKeys(keyList=['space'])

        # check for quit:
        if "escape" in theseKeys:
            endExpNow = True
        if len(theseKeys) > 0:  # at least one key was pressed
            key_resp_inst1.keys = theseKeys[-1]  # just the last key pressed
            key_resp_inst1.rt = key_resp_inst1.clock.getTime()
            # second  response ends the routine
            continueRoutine = False

    # check if all components have finished
    # a component has requested a forced-end of Routine
    if not continueRoutine:
        # if we abort early the non-slip timer needs reset
        routineTimer.reset()
        break
    # will revert to True if at least one component still running
    continueRoutine = False
    for thisComponent in Instructions1Components:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished

    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()

    # refresh the screen
    if continueRoutine:
        win.flip()
    else:  # this Routine was not non-slip safe so reset non-slip timer
        routineTimer.reset()

#-------Ending Routine "Instructions1"-------
for thisComponent in Instructions1Components:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# check responses
# if key_resp_inst1.keys in ['', [], None]:  # No response was made
#   key_resp_inst1.keys=None
# store data for thisExp (ExperimentHandler)
# thisExp.addData('key_resp_inst1.keys',key_resp_inst1.keys)
# if key_resp_inst1.keys != None:  # we had a response
#    thisExp.addData('key_resp_inst1.rt', key_resp_inst1.rt)
# thisExp.nextEntry()


#------Prepare to start Routine "Instructions3"-------
t = 0
Instructions3Clock.reset()  # clock
frameN = -1
# update component parameters for each repeat
key_resp_2 = event.BuilderKeyResponse()  # create an object of type KeyResponse
key_resp_2.status = NOT_STARTED
# keep track of which components have finished
Instructions3Components = []
Instructions3Components.append(text_instructions3_s)
Instructions3Components.append(key_resp_2)
for thisComponent in Instructions3Components:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED


#-------Start Routine "Instructions2"-------
continueRoutine = True
while continueRoutine:
    # get current time
    t = Instructions3Clock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame

    # *text_instructions2_s* updates
    if t >= 0.0 and text_instructions3_s.status == NOT_STARTED:
        # underestimates by a little under one frame
        text_instructions3_s.tStart = t
        text_instructions3_s.frameNStart = frameN  # exact frame index
        text_instructions3_s.setAutoDraw(True)

    # *key_resp_2* updates
    if t >= 0.0 and key_resp_2.status == NOT_STARTED:
        key_resp_2.tStart = t  # underestimates by a little under one frame
        key_resp_2.frameNStart = frameN  # exact frame index
        key_resp_2.status = STARTED
        # keyboard checking is just starting
        key_resp_2.clock.reset()  # now t=0
        event.clearEvents(eventType='keyboard')
    if key_resp_2.status == STARTED:
        theseKeys = event.getKeys(keyList=['space'])

        # check for quit:
        if "escape" in theseKeys:
            endExpNow = True
        if len(theseKeys) > 0:  # at least one key was pressed
            key_resp_2.keys = theseKeys[-1]  # just the last key pressed
            key_resp_2.rt = key_resp_2.clock.getTime()
            # second  response ends the routine
            continueRoutine = False

    # check if all components have finished
    # a component has requested a forced-end of Routine
    if not continueRoutine:
        # if we abort early the non-slip timer needs reset
        routineTimer.reset()
        break
    # will revert to True if at least one component still running
    continueRoutine = False
    for thisComponent in Instructions3Components:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished

    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()

    # refresh the screen
    # don't flip if this routine is over or we'll get a blank screen
    if continueRoutine:
        win.flip()
    else:  # this Routine was not non-slip safe so reset non-slip timer
        routineTimer.reset()

#-------Ending Routine "instructions2"-------
for thisComponent in Instructions3Components:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)


# ########   #########    #########      START OF TRIALS      ########

# set up handler to look after randomisation of conditions etc
trials = data.TrialHandler(nReps=1, method='random',
                           extraInfo=expInfo, originPath=None,
                           trialList=data.importConditions(listparticipant),
                           seed=None, name='trials')
thisExp.addLoop(trials)  # add the loop to the experiment
# so we can initialise stimuli with some values
thisTrial = trials.trialList[0]

# abbreviate parameter names if possible (e.g. rgb=thisTrial.rgb)
if thisTrial != None:
    for paramName in thisTrial.keys():
        #exec(paramName + '= thisTrial.' + paramName)
        exec('{} = thisTrial[paramName]'.format(paramName))

for thisTrial in trials:    #range(trialmax):   
    currentLoop = trials
    # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
    if thisTrial != None:
        for paramName in thisTrial.keys():
            #exec(paramName + '= thisTrial.' + paramName)
            exec('{} = thisTrial[paramName]'.format(paramName))

    # define durations (because of jitter in fix cross)
    jittery(0)

    # quit after max number of trials
    if trials.thisTrialN == trialmax:
        endExpNow = True
        

#     ###########   ##############     PAUSE    ###########   ############

    if trials.thisTrialN in when_Pause:   # ONLY SHOW PAUSE ON THESE TRIALS
        
        
        text_pause_s.setText('Halfway through! Take a breath and press SPACE when you are ready to continue')
        

        #------Prepare to start Routine "pause"-------
        t = 0
        PauseClock.reset()  # clock
        frameN = -1

        # update component parameters for each repeat
        key_resp_pause = event.BuilderKeyResponse()
        key_resp_pause.status = NOT_STARTED

        # keep track of which components have finished
        pauseComponents = []
        pauseComponents.append(text_pause_s)
        pauseComponents.append(key_resp_pause)
        for thisComponent in pauseComponents:
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED

        #-------Start Routine "pause"-------
        continueRoutine = True
        while continueRoutine:
            # get current time
            t = PauseClock.getTime()
            # number of completed frames (so 0 is the first frame)
            frameN = frameN + 1
            # update/draw components on each frame

#            if trials.thisTrialN  not in when_Pause:   # ONLY SHOW PAUSE ON THESE TRIALS
#                continueRoutine = False

            # *text_pause_s* updates
            if frameN >= 0 and text_pause_s.status == NOT_STARTED:
                # underestimates by a little under one frame
                text_pause_s.tStart = t
                text_pause_s.frameNStart = frameN  # exact frame index
                text_pause_s.setAutoDraw(True)

            # *key_resp_pause* updates
            if frameN >= 0 and key_resp_pause.status == NOT_STARTED:
                # underestimates by a little under one frame
                key_resp_pause.tStart = t
                key_resp_pause.frameNStart = frameN  # exact frame index
                key_resp_pause.status = STARTED
                key_resp_pause.clock.reset()
                event.clearEvents(eventType='keyboard')
            if key_resp_pause.status == STARTED:
                # wait for space press
                theseKeys = event.getKeys(keyList=['space'])

                # check for quit (the Esc key)
                if "escape" in theseKeys:
                    endExpNow = True
                
                # check if there was a resp
                if len(theseKeys) > 0:
                    key_resp_pause.keys = theseKeys[-1]
                    key_resp_pause.rt = key_resp_pause.clock.getTime()
                    # but move on only after X sec
                    if frameN < duration_pause*60:
                        core.wait((duration_pause*60 - frameN)/60)
                        continueRoutine = False
                    else: 
                        continueRoutine = False

            # check for quit (the Esc key)
            if endExpNow or event.getKeys(keyList=["escape"]):
                core.quit()

            # check if all components have finished
            # a component has requested a forced-end of Routine
            if not continueRoutine:
                # if we abort early the non-slip timer needs reset
                routineTimer.reset()
                break
            # will revert to True if at least one component still running
            continueRoutine = False
            for thisComponent in pauseComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished

            # refresh the screen
            # don't flip if this routine is over or we'll get a blank screen
            if continueRoutine:
                win.flip()
            else:  # this Routine was not non-slip safe so reset non-slip timer
                routineTimer.reset()

        #-------Ending Routine "pause"-------
        for thisComponent in pauseComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
    #    # check responses
    #    if key_resp_pause.keys in ['', [], None]:
    #        key_resp_pause.keys = None
    #    # store data for trial (TrialHandler)
    #    trials.addData('key_resp_pause.keys', key_resp_pause.keys)
    #    if key_resp_pause.keys != None:
    #        trials.addData('key_resp_pause.rt', key_resp_pause.rt)
    #
    #    thisExp.nextEntry()


#     ###########   ##############     FIXATION CROSS at beginning of each

    #------Prepare to start Routine "pretrial"-------
    t = 0
    pretrialClock.reset()  # clock
    frameN = -1

    start_cross = 0

#    key_resp_pre = event.BuilderKeyResponse()  # create an object of type KeyResponse
#    key_resp_pre.status = NOT_STARTED

    pretrialComponents = []
    pretrialComponents.append(line_left_s_i)
    pretrialComponents.append(line_right_s_i)
    pretrialComponents.append(line_above_s_i)
    pretrialComponents.append(line_below_s_i)
    pretrialComponents.append(fix_cross_stim_side)

    for thisComponent in pretrialComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED

    #-------Start Routine "pretrial"-------
    continueRoutine = True
    while continueRoutine:
        # get current time
        t = pretrialClock.getTime()
        # number of completed frames (so 0 is the first frame)
        frameN = frameN + 1
        # update/draw components on each frame

        # *line_left_s_i* updates
        if frameN >= 0 and line_left_s_i.status == NOT_STARTED:
            # underestimates by a little under one frame
            line_left_s_i.tStart = t
            line_left_s_i.frameNStart = frameN  # exact frame index
            line_left_s_i.setAutoDraw(True)

        # *line_right_s_i* updates
        if frameN >= 0 and line_right_s_i.status == NOT_STARTED:
            # underestimates by a little under one frame
            line_right_s_i.tStart = t
            line_right_s_i.frameNStart = frameN  # exact frame index
            line_right_s_i.setAutoDraw(True)

        # *line_above_s_i* updates
        if frameN >= 0 and line_above_s_i.status == NOT_STARTED:
            # underestimates by a little under one frame
            line_above_s_i.tStart = t
            line_above_s_i.frameNStart = frameN  # exact frame index
            line_above_s_i.setAutoDraw(True)

        # *line_below_s_i* updates
        if frameN >= 0 and line_below_s_i.status == NOT_STARTED:
            # underestimates by a little under one frame
            line_below_s_i.tStart = t
            line_below_s_i.frameNStart = frameN  # exact frame index
            line_below_s_i.setAutoDraw(True)

        # *frame_s_i* updates
        if frameN >= 0 and frame_s_i.status == NOT_STARTED:
            # keep track of start time/frame for later
            frame_s_i.tStart = t  # underestimates by a little under one frame
            frame_s_i.frameNStart = frameN  # exact frame index
            frame_s_i.draw()
            frame2_s_i.draw()
            square_s_i.tStart = t  # underestimates by a little under one frame
            square_s_i.draw()
        if frame_s_i.status == STARTED and frameN >= time_before:
            frame_s_i.setAutoDraw(False)
            frame2_s_i.setAutoDraw(False)

        # *fix_cross_stim_side* updates
        if frameN >= 0 and fix_cross_stim_side.status == NOT_STARTED:
            # underestimates by a little under one frame
            fix_cross_stim_side.tStart = t
            fix_cross_stim_side.frameNStart = frameN  # exact frame index
            fix_cross_stim_side.setAutoDraw(True)

        # check if all components have finished
        # a component has requested a forced-end of Routine
        if not continueRoutine:
            break
        # will revert to True if at least one component still running
        continueRoutine = False
        for thisComponent in pretrialComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished

        # check if time is over
        if frameN >= time_before:        # fixlength is an attribute of the list
            continueRoutine = False

        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()

        # refresh the screen
        # don't flip if this routine is over or we'll get a blank screen
        if continueRoutine:
            win.flip()

    #-------Ending Routine "pretrial"-------
    for thisComponent in pretrialComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)

#     ###########   ##############     FACES DISPLAYED    ###########   ##

    #------Prepare to start Routine "trial"-------
    t = 0
    trialClock.reset()  # clock
    frameN = -1
    imagepath = os.path.join(dirstim, filename)
    image.setImage(imagepath)#set image of trial
    image.setPos([0, s_p[0] + set_pos_ver(position)])

    f_change = 0  # counter for change of mondrians (every 6 tfs)

    start_trial = trialClock.getTime()

    # create an object of type KeyResponse
    key_resp_image = event.BuilderKeyResponse()
    key_resp_image.status = NOT_STARTED

    trialComponents = []
    trialComponents.append(line_left_s_i)
    trialComponents.append(line_right_s_i)
    trialComponents.append(line_above_s_i)
    trialComponents.append(line_below_s_i)
    trialComponents.append(image)
    trialComponents.append(fix_cross_stim_side)
    trialComponents.append(key_resp_image)

    for thisComponent in trialComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED

    #-------Start Routine "trial"-------
    continueRoutine = True
    while continueRoutine:
        # get current time
        t = trialClock.getTime()
        # number of completed frames (so 0 is the first frame)
        frameN = frameN + 1
        # update/draw components on each frame

        # *line_left_s_i* updates
        if frameN >= 0 and line_left_s_i.status == NOT_STARTED:
            # underestimates by a little under one frame
            line_left_s_i.tStart = t
            line_left_s_i.frameNStart = frameN  # exact frame index
            line_left_s_i.setAutoDraw(True)
        if line_left_s_i.status == STARTED and frameN >= (line_left_s_i.frameNStart + total_t):
            line_left_s_i.setAutoDraw(False)

        # *line_right_s_i* updates
        if frameN >= 0 and line_right_s_i.status == NOT_STARTED:
            # underestimates by a little under one frame
            line_right_s_i.tStart = t
            line_right_s_i.frameNStart = frameN  # exact frame index
            line_right_s_i.setAutoDraw(True)
        if line_right_s_i.status == STARTED and frameN >= (line_right_s_i.frameNStart + total_t):
            line_right_s_i.setAutoDraw(False)

        # *line_above_s_i* updates
        if frameN >= 0 and line_above_s_i.status == NOT_STARTED:
            # underestimates by a little under one frame
            line_above_s_i.tStart = t
            line_above_s_i.frameNStart = frameN  # exact frame index
            line_above_s_i.setAutoDraw(True)
        if line_above_s_i.status == STARTED and frameN >= (line_above_s_i.frameNStart + total_t):
            line_above_s_i.setAutoDraw(False)

        # *line_below_s_i* updates
        if frameN >= 0 and line_below_s_i.status == NOT_STARTED:
            # underestimates by a little under one frame
            line_below_s_i.tStart = t
            line_below_s_i.frameNStart = frameN  # exact frame index
            line_below_s_i.setAutoDraw(True)
        if line_below_s_i.status == STARTED and frameN >= (line_below_s_i.frameNStart + total_t):
            line_below_s_i.setAutoDraw(False)

        # *image* updates
        if frameN >= 0 and image.status == NOT_STARTED:
            image.tStart = t  # underestimates by a little under one frame
            image.frameNStart = frameN  # exact frame index
            image.setAutoDraw(True)
        if image.status == STARTED and frameN >= (image.frameNStart + before_t + stim_t):
            image.setAutoDraw(False)
        if image.status == STARTED:  # only update if being drawn
            image.setOpacity(((frameN - before_t) / fade_i_t)*float(max_opacity) if (frameN < fade_i_end_t) else (
                float(max_opacity) if(frameN < fade_o_beg_t) else (fade_o_end_t - frameN) / fade_o_t), log=False)

        # *fix_cross_stim_side* updates
        if frameN >= 0 and fix_cross_stim_side.status == NOT_STARTED:
            # keep track of start time/frame for later
            # underestimates by a little under one frame
            fix_cross_stim_side.tStart = t
            fix_cross_stim_side.frameNStart = frameN  # exact frame index
            fix_cross_stim_side.setAutoDraw(True)
        if fix_cross_stim_side.status == STARTED and frameN >= (fix_cross_stim_side.frameNStart + total_t):
            fix_cross_stim_side.setAutoDraw(False)

        # *update all frames
        if frameN >= 0 and frame_s_i.status == NOT_STARTED:
            # keep track of start time/frame for later
            frame_s_i.tStart = t  # underestimates by a little under one frame
            frame_s_i.frameNStart = frameN  # exact frame index
            frame_s_i.draw()
            frame2_s_i.draw()
            square_s_i.tStart = t  # underestimates by a little under one frame
            square_s_i.draw()
        if frame_s_i.status == STARTED and frameN >= (frame_i.frameNStart + total_t):
            frame_s_i.setAutoDraw(False)
            frame2_s_i.setAutoDraw(False)

        # flash Mondrians
        if frameN >= f_change:
            myRand = randint(1, 100)
#            print myRand    # tto check
            # advance by 6 frames, so that the next draw occurs 6 frames later
            f_change += f_t
#           print globalClock.getTime()  # get precise timing of each flash refresh

#            # uncomment to check timing of flashes (how much do they differ from the intended 100 ms?)
            intended = 0.1
            print  ("%.5f" % (intended - (trialClock.getTime() - start_trial))  )
            start_trial = trialClock.getTime()
        num = trials.thisIndex
        if (num%2) == 0:
            flash[myRand].setOpacity(((frameN - before_f) / fade_i_f)*float(max_opacity_flash) if (frameN < fade_i_end_f) else 
            (float(max_opacity_flash) if(frameN < fade_o_beg_f) else (fade_o_end_f - frameN) / fade_o_f), log=False)
            flash[myRand].draw()  # draw one of the randomly selected flashes
        else: 
            flash1[myRand].setOpacity(((frameN - before_f) / fade_i_f)*float(max_opacity_flash) if (frameN < fade_i_end_f) else 
            (float(max_opacity_flash) if(frameN < fade_o_beg_f) else (fade_o_end_f - frameN) / fade_o_f), log=False)
            flash1[myRand].draw()
        # *key_resp_image* updates
        if frameN >= 0 and key_resp_image.status == NOT_STARTED:
            # keep track of start time/frame for later
            # underestimates by a little under one frame
            key_resp_image.tStart = t
            key_resp_image.frameNStart = frameN  # exact frame index
            key_resp_image.status = STARTED
            # keyboard checking is just starting
            key_resp_image.clock.reset()  # now t=0
            event.clearEvents(eventType='keyboard')
        if key_resp_image.status == STARTED and frameN >= (key_resp_image.frameNStart + total_t):
            key_resp_image.status = STOPPED
        if key_resp_image.status == STARTED:
            theseKeys = event.getKeys(keyList=['g', 'z'])

            # check for quit:
            if "escape" in theseKeys:
                endExpNow = True
            if len(theseKeys) > 0:  # at least one key was pressed
                # just the last key pressed
                key_resp_image.keys = theseKeys[-1]
                key_resp_image.rt = key_resp_image.clock.getTime()
#                    key_resp_image.globtime = init_experimentClock.getTime()

                # a response ends the routine
                if frameN >= before_t:
                    continueRoutine = False

                # was this 'correct'?
                if position == 'up' and (key_resp_image.keys == correct_up):
                    key_resp_image.corr = 1
                elif position == 'down' and (key_resp_image.keys == correct_down):
                    key_resp_image.corr = 1
                else:
                    key_resp_image.corr = 0
        
        # check if all components have finished
        if not continueRoutine:
            break
        # will revert to True if at least one component still running
        continueRoutine = False
        for thisComponent in trialComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished

        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()

        # refresh the screen
        # don't flip if this routine is over or we'll get a blank screen
        if continueRoutine:
            win.flip()

    #-------Ending Routine "trial"-------
    for thisComponent in trialComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)

    #    # check responses
    if key_resp_image.keys in ['', [], None]:  # No response was made
        key_resp_image.keys = None
    # store data for images (TrialHandler)
    #trials.addData('image_i.startTime', image_i.startTime)
    trials.addData('key_resp_image.keys', key_resp_image.keys)
    if key_resp_image.keys != None:  # we had a response
        trials.addData('key_resp_image.rt', key_resp_image.rt)
        trials.addData('RT_from_SO.rt', key_resp_image.rt - (before_t/60))

    trials.addData('correct_response', key_resp_image.corr)
    trials.addData('before_t', before_t)
    trials.addData('stim_t', stim_t)
    trials.addData('total_t', total_t)
    thisExp.nextEntry()

#     ###########   ##############     MASK at end of each trial    ######

    #------Prepare to start Routine "posttrial"-------
    t = 0
    posttrialClock.reset()  # clock
    frameN = -1

    # set mask of trial (in column 'masks' of list)
    maskpath = os.path.join(dirmask, mask)
    scramble_s.setImage(maskpath)  # set scramble of trial (in column 'scrambled_face' of list)


#    key_resp_pre = event.BuilderKeyResponse()  # create an object of type KeyResponse
#    key_resp_pre.status = NOT_STARTED

    posttrialComponents = []
    posttrialComponents.append(line_left_s_i)
    posttrialComponents.append(line_right_s_i)
    posttrialComponents.append(line_above_s_i)
    posttrialComponents.append(line_below_s_i)
#    posttrialComponents.append(fix_cross_stim_side)
    posttrialComponents.append(scramble_s)

    for thisComponent in posttrialComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED

    #-------Start Routine "posttrial"-------
    continueRoutine = True
    while continueRoutine:
        # get current time
        t = posttrialClock.getTime()
        # number of completed frames (so 0 is the first frame)
        frameN = frameN + 1
        # update/draw components on each frame

        # *line_left_s_i* updates
        if frameN >= 0 and line_left_s_i.status == NOT_STARTED:
            # underestimates by a little under one frame
            line_left_s_i.tStart = t
            line_left_s_i.frameNStart = frameN  # exact frame index
            line_left_s_i.setAutoDraw(True)

        # *line_right_s_i* updates
        if frameN >= 0 and line_right_s_i.status == NOT_STARTED:
            # underestimates by a little under one frame
            line_right_s_i.tStart = t
            line_right_s_i.frameNStart = frameN  # exact frame index
            line_right_s_i.setAutoDraw(True)

        # *line_above_s_i* updates
        if frameN >= 0 and line_above_s_i.status == NOT_STARTED:
            # underestimates by a little under one frame
            line_above_s_i.tStart = t
            line_above_s_i.frameNStart = frameN  # exact frame index
            line_above_s_i.setAutoDraw(True)

        # *line_below_s_i* updates
        if frameN >= 0 and line_below_s_i.status == NOT_STARTED:
            # underestimates by a little under one frame
            line_below_s_i.tStart = t
            line_below_s_i.frameNStart = frameN  # exact frame index
            line_below_s_i.setAutoDraw(True)

        # *frame_s_i* updates
        if frameN >= 0 and frame_s_i.status == NOT_STARTED:
            # keep track of start time/frame for later
            frame_s_i.tStart = t  # underestimates by a little under one frame
            frame_s_i.frameNStart = frameN  # exact frame index
            frame_s_i.draw()
            frame2_s_i.draw()
            square_s_i.tStart = t  # underestimates by a little under one frame
            square_s_i.draw()
        if frame_s_i.status == STARTED and frameN >= time_blank:
            frame_s_i.setAutoDraw(False)
            frame2_s_i.setAutoDraw(False)

        # *scramble_s* updates
        if frameN >= 0 and scramble_s.status == NOT_STARTED:
            # keep track of start time/frame for later
            scramble_s.tStart = t  # underestimates by a little under one frame
            scramble_s.frameNStart = frameN  # exact frame index
            scramble_s.setAutoDraw(True)

#        # *fix_cross_stim_side* updates
#        if frameN >= 0 and fix_cross_stim_side.status == NOT_STARTED:
#            fix_cross_stim_side.tStart = t  # underestimates by a little under one frame
#            fix_cross_stim_side.frameNStart = frameN  # exact frame index
#            fix_cross_stim_side.setAutoDraw(True)

        # check if all components have finished
        if not continueRoutine:
            break
        # will revert to True if at least one component still running
        continueRoutine = False
        for thisComponent in posttrialComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished

        # check if time is over
        if frameN >= time_blank:
            continueRoutine = False

        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()

        # refresh the screen
        # don't flip if this routine is over or we'll get a blank screen
        if continueRoutine:
            win.flip()

    #-------Ending Routine "posttrial"-------
    for thisComponent in posttrialComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)

#------Prepare to start Routine "thanks"-------
t = 0
thanksClock.reset()  # clock
frameN = -1

key_resp_thanks = event.BuilderKeyResponse()
key_resp_thanks.status = NOT_STARTED

# update component parameters for each repeat
# keep track of which components have finished
thanksComponents = []
thanksComponents.append(thanksText_s)
thanksComponents.append(key_resp_thanks)

for thisComponent in thanksComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

#-------Start Routine "thanks"-------
continueRoutine = True
while continueRoutine:
    # get current time
    t = thanksClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame

    # *thanksText_s* updates
    if frameN >= 0.0 and thanksText_s.status == NOT_STARTED:
        # keep track of start time/frame for later
        thanksText_s.tStart = t  # underestimates by a little under one frame
        thanksText_s.frameNStart = frameN  # exact frame index
        thanksText_s.setAutoDraw(True)

    # *key_resp_thanks* updates
    if frameN >= 0 and key_resp_thanks.status == NOT_STARTED:
        # keep track of start time/frame for later
        # underestimates by a little under one frame
        key_resp_thanks.tStart = t
        key_resp_thanks.frameNStart = frameN  # exact frame index
        key_resp_thanks.status = STARTED
        key_resp_thanks.clock.reset()
        event.clearEvents(eventType='keyboard')
    if key_resp_thanks.status == STARTED:
        theseKeys = event.getKeys(keyList=['space'])  # wait for space press

        # check for quit (the Esc key)
        if "escape" in theseKeys:
            endExpNow = True
        if len(theseKeys) > 0:
            key_resp_thanks.keys = theseKeys[-1]
            key_resp_thanks.rt = key_resp_thanks.clock.getTime()
            continueRoutine = False

    # check if all components have finished
    # a component has requested a forced-end of Routine
    if not continueRoutine:
        break
    # will revert to True if at least one component still running
    continueRoutine = False
    for thisComponent in thanksComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished

    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()

    # refresh the screen
    # don't flip if this routine is over or we'll get a blank screen
    if continueRoutine:
        win.flip()

#-------Ending Routine "thanks"-------
for thisComponent in thanksComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)

win.close()
core.quit()
