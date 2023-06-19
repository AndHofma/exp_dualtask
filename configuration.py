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
from psychopy import monitors, visual, gui, core
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
# directory to shapes images for dual-task version
shapes_path = 'shapes/'


# to use in acoustic lab - second monitor name fixed here
def create_window():
    """
    Create and initialize the experiment window.

    Returns:
    win: A PsychoPy visual.Window object for the experiment.
    """
    # Create a monitor object for the second screen
    second_monitor = monitors.Monitor(name='EA273WMi')
    # Set the appropriate settings for the second monitor
    second_monitor.setSizePix((1920, 1080))  # Set the desired resolution of the second screen

    # Create and return a window for the experiment on the second monitor
    return visual.Window(monitor=second_monitor,  # Use the second monitor
                         size=(1920, 1080),
                         screen=1,  # Specify the index of the second screen (0 for the first screen, 1 for the second, etc.)
                         allowGUI=True,
                         fullscr=True,
                         color=(255, 255, 255)
                         )


# to use for testing on laptop
#def create_window():
#   """
#   Create and initialize the experiment window.
#   Returns:
#   win : A PsychoPy visual.Window object for the experiment.
#   """
   # Create a monitor object
#   currentMonitor = monitors.Monitor(name='testMonitor')

   # Create and return a window for the experiment
#   return visual.Window(monitors.Monitor.getSizePix(currentMonitor),
#                        monitor="testMonitor",
#                        allowGUI=True,
#                        fullscr=True,
#                        color=(255, 255, 255)
#                        )


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
    visual_frames = 300
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

    # Get a list of all file paths in the shapes directory
    shapes_list = [os.path.join(shapes_path, f) for f in os.listdir(shapes_path)]

    # Initialize shape stimulus
    shape = visual.ImageStim(window,
                             pos=(0, -0.5),
                             name='shape')  # don't assign an image yet

    # flanker stimuli
    flanker_stimuli = [
        ("XXXXX", 'a', 'congruent'),  # Congruent condition
        ("XXCXX", 'a', 'congruent'),  # Congruent condition
        ("XXVXX", 'l', 'incongruent'),  # Incongruent condition
        ("XXBXX", 'l', 'incongruent'),  # Incongruent condition
        ("CCXCC", 'a', 'congruent'),  # Congruent condition
        ("CCCCC", 'a', 'congruent'),  # Congruent condition
        ("CCVCC", 'l', 'incongruent'),  # Incongruent condition
        ("CCBCC", 'l', 'incongruent'),  # Incongruent condition
        ("VVXVV", 'a', 'incongruent'),  # Incongruent condition
        ("VVCVV", 'a', 'incongruent'),  # Incongruent condition
        ("VVVVV", 'l', 'congruent'),  # Congruent condition
        ("VVBVV", 'l', 'congruent'),  # Congruent condition
        ("BBXBB", 'a', 'incongruent'),  # Incongruent condition
        ("BBCBB", 'a', 'incongruent'),  # Incongruent condition
        ("BBVBB", 'l', 'congruent'),  # Congruent condition
        ("BBBBB", 'l', 'congruent'),  # Congruent condition
    ]
    # flanker stimuli key mapping
    key_mapping = {
        "a": ["X", "C"],
        "l": ["V", "B"]
    }

    # flanker shape stimuli
    flanker_shape_stimuli = [
        (">>>>>", 'l', 'congruent'),  # Congruent condition
        ("<<<<<", 'a', 'congruent'),  # Congruent condition
        ("++>++", 'l', 'neutral'),  # Neutral condition
        ("++<++", 'a', 'neutral'),  # Neutral condition
        ("<<><<", 'l', 'incongruent'),  # Incongruent condition
        (">><>>", 'a', 'incongruent'),  # Incongruent condition
    ]

    # feedback flanker stimuli
    flanker_correct = visual.ImageStim(window, image='pics/fixgreen.png', pos=(0, -0.5))
    flanker_incorrect = visual.ImageStim(window, image='pics/fixred.png', pos=(0, -0.5))
    flanker_neutral = visual.ImageStim(window, image='pics/fix.png', pos=(0, -0.5))

    return werKommt, fixation, randNumber, item, pic, prompt, feedback, input_text, keyList, fs, rec_seconds, \
        movementDirections, responseList, dots, operations, arrows, shapes_list, shape, \
        flanker_stimuli, flanker_correct, flanker_incorrect, flanker_neutral, flanker_shape_stimuli


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
def append_result_to_csv(result, base_filename, participant_info, type='main'):
    """
    Append a participant's trial result to a CSV file.
    The CSV files correspond to the different dual-task versions (2back, flanker, flanker_shape) and the main CSV file with general parameters throughout all experiment parts.
    The main CSV file includes the single task parameter values as well as the dot-motion and calculation task parameters, which is the first dual-task option hereafter.
    If the file doesn't exist, it creates the file and adds headers.

    Args:
    result : dict. Contains the data for a single trial.
    filename : str. The filename of the CSV file.
    participant_info : dict. Contains the participant's information.
    type : str. Can be 'main' for the main trial results, 'flanker' for flanker task results, and '2back' for 2-back task results.

    Returns:
        None. The function directly writes to the CSV file.

    Raises:
        OSError: If there is an issue with accessing or writing to the CSV file.

    Notes:
        - The CSV file will be named "{base_filename}_{type}.csv".
        - The function appends the result data to the CSV file.
        - If the CSV file does not exist, it creates the file and adds the appropriate headers.

    """

    # Define the filename by appending the type of the task to the base filename
    filename = f"{base_filename}_{type}.csv"

    # Check if the file does not exist to write the header
    if not os.path.isfile(filename):
        with open(filename, 'w') as file:
            if type == 'main':
                file.write(
                'experiment,'
                'subject_ID,'
                'date,'
                'task,'
                'main_trial,'
                'phase,'
                'stimulus_id,'
                'stimulus,'
                'stimulus_rec,'
                'rand_nr,'
                'dot_direction,'
                'dot_1st_frame,'
                'dot_last_frame,'
                'dot_response_key,'
                'dot_response_accuracy,'
                'rand_nr_calc,'
                'rand_operation,'
                'answer_calc,'
                'answer_input,'
                'answer_input_accuracy,'
                '2back_matching_trials_single,'
                '2back_matching_trials_dual,'
                '2back_trial_accuracy_single,'
                '2back_trial_accuracy_dual,'
                '2back_trial_rt_correct_single,'
                '2back_trial_rt_correct_dual,'
                '2back_shape_order,'
                'flanker_nr_trials_single,'
                'flanker_nr_trials_dual,'
                'flanker_trial_accuracy_single,'
                'flanker_trial_accuracy_dual,'
                'flanker_trial_rt_correct_single,'
                'flanker_trial_rt_correct_dual,'
                'flanker_trial_rt_incorrect_single,'
                'flanker_trial_rt_incorrect_dual,'
                'flanker_shape_nr_trials_single,'
                'flanker_shape_nr_trials_dual,'
                'flanker_shape_trial_accuracy_single,'
                'flanker_shape_trial_accuracy_dual,'
                'flanker_shape_trial_rt_correct_single,'
                'flanker_shape_trial_rt_correct_dual,'
                'flanker_shape_trial_rt_incorrect_single,'
                'flanker_shape_trial_rt_incorrect_dual,'
                'start_time,'
                'end_time,'
                'duration \n'
                )
            elif type == '2back':
                file.write(
                    'experiment,'
                    'subject_id,'
                    'date,'
                    'task,'
                    'phase,'
                    'main_trial,'
                    '2back_trial,'
                    '2back_trial_type,'
                    '2back_accuracy,'
                    '2back_response_type,'
                    '2back_rt,'
                    '2back_current_shape,'
                    '2back_nback1_shape,'
                    '2back_nback2_shape,'
                    'presentation,'
                    'start_time,'
                    'end_time,'
                    'duration \n'
                )
            elif type == 'flanker':
                file.write(
                    'experiment,'
                    'subject_id,'
                    'date,'
                    'task,'
                    'phase,'
                    'main_trial,'
                    'flanker_trial,'
                    'flanker_stimulus,'
                    'flanker_condition,'
                    'flanker_correct,'
                    'flanker_rt,'
                    'flanker_response,'
                    'flanker_response_accuracy,'
                    'presentation,'
                    'start_time,'
                    'end_time,'
                    'duration \n'
                )
            elif type == 'flanker_shape':
                file.write(
                    'experiment,'
                    'subject_id,'
                    'date,'
                    'task,'
                    'phase,'
                    'main_trial,'
                    'flanker_shape_trial,'
                    'flanker_shape_stimulus,'
                    'flanker_shape_condition,'
                    'flanker_shape_correct,'
                    'flanker_shape_rt,'
                    'flanker_shape_response,'
                    'flanker_shape_response_accuracy,'
                    'presentation,'
                    'start_time,'
                    'end_time,'
                    'duration \n'
                )

    # Now append the result data
    with open(filename, 'a', newline='') as output_file:
        writer = csv.writer(output_file)
        if type == 'main':
            writer.writerow([
                participant_info['experiment'],
                participant_info['subject'],
                participant_info['cur_date'],
                result['task'],
                result['main_trial'],
                result['phase'],
                result['stimulus_id'],
                result['stimulus'],
                result['stimulus_rec'],
                result['rand_nr'],
                result['dot_direction'],
                result['dot_1st_frame'],
                result['dot_last_frame'],
                result['dot_response_key'],
                result['dot_response_accuracy'],
                result['rand_nr_calc'],
                result['rand_operation'],
                result['answer_calc'],
                result['answer_input'],
                result['answer_input_accuracy'],
                result['2back_matching_trials_single'],
                result['2back_matching_trials_dual'],
                result['2back_trial_accuracy_single'],
                result['2back_trial_accuracy_dual'],
                result['2back_trial_rt_correct_single'],
                result['2back_trial_rt_correct_dual'],
                result['2back_shape_order'],
                result['flanker_nr_trials_single'],
                result['flanker_nr_trials_dual'],
                result['flanker_trial_accuracy_single'],
                result['flanker_trial_accuracy_dual'],
                result['flanker_trial_rt_correct_single'],
                result['flanker_trial_rt_correct_dual'],
                result['flanker_trial_rt_incorrect_single'],
                result['flanker_trial_rt_incorrect_dual'],
                result['flanker_shape_nr_trials_single'],
                result['flanker_shape_nr_trials_dual'],
                result['flanker_shape_trial_accuracy_single'],
                result['flanker_shape_trial_accuracy_dual'],
                result['flanker_shape_trial_rt_correct_single'],
                result['flanker_shape_trial_rt_correct_dual'],
                result['flanker_shape_trial_rt_incorrect_single'],
                result['flanker_shape_trial_rt_incorrect_dual'],
                result['start_time'],
                result['end_time'],
                result['duration']
            ])
        elif type == '2back':
            writer.writerow([
                participant_info['experiment'],
                participant_info['subject'],
                participant_info['cur_date'],
                result['task'],
                result['phase'],
                result['main_trial'],
                result['2back_trial'],
                result['2back_trial_type'],
                result['2back_accuracy'],
                result['2back_response_type'],
                result['2back_rt'],
                result['2back_current_shape'],
                result['2back_nback1_shape'],
                result['2back_nback2_shape'],
                result['presentation'],
                result['start_time'],
                result['end_time'],
                result['duration']
            ])
        elif type == 'flanker':
            writer.writerow([
                participant_info['experiment'],
                participant_info['subject'],
                participant_info['cur_date'],
                result['task'],
                result['phase'],
                result['main_trial'],
                result['flanker_trial'],
                result['flanker_stimulus'],
                result['flanker_condition'],
                result['flanker_correct'],
                result['flanker_rt'],
                result['flanker_response'],
                result['flanker_response_accuracy'],
                result['presentation'],
                result['start_time'],
                result['end_time'],
                result['duration']
            ])
        elif type == 'flanker_shape':
            writer.writerow([
                participant_info['experiment'],
                participant_info['subject'],
                participant_info['cur_date'],
                result['task'],
                result['phase'],
                result['main_trial'],
                result['flanker_shape_trial'],
                result['flanker_shape_stimulus'],
                result['flanker_shape_condition'],
                result['flanker_shape_correct'],
                result['flanker_shape_rt'],
                result['flanker_shape_response'],
                result['flanker_shape_response_accuracy'],
                result['presentation'],
                result['start_time'],
                result['end_time'],
                result['duration']
            ])