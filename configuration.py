"""
Experiment Preparation and Execution
This section of code prepares and executes the experiment.
It starts by defining the preferred audio library and setting up paths for stimuli, results, pictograms, and recordings.
Next, the create_window function creates a new window for the experiment using the PsychoPy visual.Window object.
The initialize_stimuli function sets up all the visual and auditory stimuli as well as parameter values needed for the experiment.
The get_participant_info function retrieves information about the participant.
And the append_result_to_csv function is used to save the participant's trial results to a CSV file.
"""

# Import necessary libraries
from psychopy import prefs, monitors, visual, gui, core
import csv
import os
import datetime


# Setup paths
# stimulus directory
stim_path = 'stimuli/'
# output directory for experiment results
output_path = 'results/'
# directory for the pictograms used
pics_path = 'pics/'
# directory for all recordings
record_path = 'recordings/'


def create_window():
    """
    Create and initialize the experiment window.

    Returns:
    win : A PsychoPy visual.Window object for the experiment.
    """
    # Create a monitor object
    currentMonitor = monitors.Monitor(name='testMonitor')

    # Create and return a window for the experiment
    return visual.Window(monitors.Monitor.getSizePix(currentMonitor),
                         monitor="testMonitor",
                         allowGUI=True,
                         fullscr=True,
                         color=(255, 255, 255)
                         )


def initialize_stimuli(window):
    """
    Initialize all the stimuli that will be used throughout the experiment.

    Args:
    window : psychopy.visual.Window. The window object in which the stimuli will be displayed.

    Returns:
    A tuple containing all the stimuli and other related objects.
    """

    # set up different TextStim needed throughout experiment
    # trigger question
    werKommt = visual.TextStim(window,
                               text="Wer kommt?",
                               height=0.3,
                               pos=(0, 0),
                               color="black",
                               name='question')
    # fixation cross
    fixation = visual.ShapeStim(window,
                                vertices=((0, -0.13), (0, 0.13), (0, 0), (-0.09, 0), (0.09, 0)),
                                lineWidth=15,
                                closeShape=False,
                                lineColor="black",
                                name='fixation')
    # random number to be remembered
    randNumber = visual.TextStim(window,
                                 pos=(0, 0),
                                 color="black",
                                 name='randNumber')
    # item (aka stimulus or name coordinate) from list
    item = visual.TextStim(window,
                           pos=(0, 0.5),
                           height=0.25,
                           wrapWidth=2,
                           color="black",
                           name='item')
    # pictogram
    pic = visual.ImageStim(window,
                           pos=(0, 0.1),
                           name='pictogram')
    # response prompt
    prompt = visual.TextStim(window,
                             color='black',
                             wrapWidth=2)
    # feedback
    feedback = visual.TextStim(window,
                               pos=(0, 0),
                               wrapWidth=2,
                               height=0.2)
    # create an empty text stimulus to serve as the input field
    input_text = visual.TextStim(window,
                                 text="",
                                 color='black',
                                 pos=(0, -0.3),
                                 wrapWidth=2)

    # allowed keys are all numbers from the numpad and the num keys from the keyboard
    # return to complete entry / backspace to remove an error
    keyList = ['num_0', 'num_1', 'num_2', 'num_3', 'num_4', 'num_5', 'num_6', 'num_7', 'num_8', 'num_9',
               '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
               'return', 'backspace']

    # default parameters for the recordings
    fs = 44100  # Sample rate
    # Calculate the recording duration in seconds
    visual_frames = 350
    # automatically estimate monitor's refresh rate from window object
    estimated_frame_rate = window.getActualFrameRate()
    # If for some reason the function fails to get the actual frame rate, it will return None.
    # In this case, you could default to a reasonable estimate, e.g., 60 Hz.
    if estimated_frame_rate is None:
        estimated_frame_rate = 60

    rec_seconds = visual_frames / estimated_frame_rate

    # dot parameters
    n_dots = 500  # number of dots in the stimulus
    dot_size = 6  # size of each dot in pixels
    dot_speed = 3  # speed of the dots in pixels per frame
    dot_coherence = 0.5  # coherence - proportion of dots that move in the same direction
    movementDirections = [0, 90, 180, 270]  # possible directions to move
    responseList = ['right', 'up', 'left', 'down']  # corresponding responses

    # dot stimulus
    dots = visual.DotStim(
        win=window,  # window where the stimulus will be drawn
        units='pix',  # units of size and position (pixels in this case)
        fieldPos=(0, -280),  # position of the center of the stimulus field
        fieldShape="circle",  # shape of the stimulus field (circle in this case)
        dotSize=dot_size,  # size of each dot in pixels
        dotLife=-1,  # duration of each dot in frames (-1 for unlimited)
        coherence=dot_coherence,  # proportion of dots that move in the same direction
        nDots=n_dots,  # number of dots in the stimulus
        fieldSize=400,  # size of the stimulus field in pixels
        speed=dot_speed,  # speed of the dots in pixels per frame
        color=(0, 0, 0),  # color of the dots (black in this case)
        colorSpace='rgb'  # color space used to specify the color (RGB in this case)
    )

    # arrow parameters
    arrowPositions = [[0.12, -0.45], [0, -0.25], [-0.12, -0.45], [0, -0.65]]  # position in the x-y-coordinate system
    arrowOrientations = [0, -90, -180, -270]  # rotation in degrees
    arrowSize = 0.5  # size in pixels?
    arrows = []  # empty list to append to

    # generate all arrows in correct orientation
    for i in range(4):
        arrow = visual.TextStim(window,
                                text='\u21e8',
                                pos=arrowPositions[i],
                                height=arrowSize,
                                ori=arrowOrientations[i],
                                color='black')
        arrows.append(arrow)

    # possible mathematical operations for calculation part of the dual task
    # operations[0]=addition, operations[1]=subtraction
    operations = [lambda x, y: x + y, lambda x, y: x - y]  # Define operations for dual task

    return werKommt, fixation, randNumber, item, pic, prompt, feedback, input_text, keyList, fs, rec_seconds, movementDirections, responseList, dots, operations, arrows


def get_participant_info():
    """
    Open a dialogue box to get participant information, including current date and time, subject_ID and experiment name.

    Returns:
    A dictionary containing the participant's information.
    """

    # Define experiment name and configuration
    experiment_name = "Dual-Task"  # Production-Dual-Task
    experiment_config = {
        'experiment': 'dual_task_experiment',
        'subject': 'subject_ID',
        'cur_date': datetime.datetime.now().strftime("%Y-%m-%d_%Hh%M")  # Use strftime to format the date string
    }
    # Create a dialogue box for the subject to enter their information
    info_dialog = gui.DlgFromDict(experiment_config,
                                  title=f'{experiment_name} Experiment',
                                  fixed=['experiment', 'cur_date']
                                  )

    if info_dialog.OK:
        return experiment_config
    else:
        core.quit()


# Function to append a single result to the CSV file
def append_result_to_csv(result, filename, participant_info):
    """
    Append a participant's trial result to a CSV file. If the file doesn't exist, it creates the file and adds headers.

    Args:
    result : dict. Contains the data for a single trial.
    filename : str. The filename of the CSV file.
    participant_info : dict. Contains the participant's information.

    Returns:
    None. The function directly writes to the CSV file.
    """

    # Check if the file does not exist to write the header
    if not os.path.isfile(filename):
        with open(filename, 'w') as file:
            file.write(
                'experiment,subject_ID,date,task,trial,phase,stimulus_ID,stimulus,rand_Nr,stimulus_Rec,dot_Move_Dir,dot_1st_Frame,dot_Last_Frame,dot_Response_Key,dot_Response_Accuracy,rand_Nr_Calc,rand_Operation,answer_Calc,answer_Subject_Input,answer_Accuracy,start_time,end_time,duration \n'
            )

    # Now append the result data
    with open(filename, 'a', newline='') as output_file:
        writer = csv.writer(output_file)
        writer.writerow([
            participant_info['experiment'],
            participant_info['subject'],
            participant_info['cur_date'],
            result['task'],
            result['trial'],
            result['phase'],
            result['stimulus_ID'],
            result['stimulus'],
            result['rand_Nr'],
            result['stimulus_Rec'],
            result['dot_Move_Dir'],
            result['dot_1st_Frame'],
            result['dot_Last_Frame'],
            result['dot_Response_Key'],
            result['dot_Response_Accuracy'],
            result['rand_Nr_Calc'],
            result['rand_Operation'],
            result['answer_Calc'],
            result['answer_Subject_Input'],
            result['answer_Accuracy'],
            result['start_time'],
            result['end_time'],
            result['duration']
        ])
