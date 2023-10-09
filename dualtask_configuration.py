"""
Experiment Preparation and Execution
This section of code prepares and executes the experiment.
It starts by defining the preferred audio library and setting up paths for stimuli, results, and recordings.
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
import sys


def resource_path(relative_path):
    """Determine and return the absolute path to the resource."""

    # Check if the application is frozen (compiled)
    if getattr(sys, 'frozen', False):
        # If we're running as a bundled exe, set the base path as one level above the executable
        base_path = os.path.join(os.path.dirname(sys.executable), "..")
    else:
        # If we're running in a normal Python environment
        base_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_path, relative_path)


# Setup paths
# stimulus directory
stim_path = resource_path('stimuli/')
# output directory for experiment results
output_path = resource_path('results/')
# directory for the pictograms used
pics_path = resource_path('pics/')
# directory for all recordings
record_path = resource_path('recordings/')


# to use in acoustic lab - second monitor name fixed here
def create_window():
    """
    Create and initialize the experiment window.

    Returns:
    win: A PsychoPy visual.Window object for the experiment.
    """
    # Create a monitor object for the second screen
    second_monitor = monitors.Monitor(name='EA244WMi')
    # Set the appropriate settings for the second monitor
    second_monitor.setSizePix((1920, 1080))  # Set the desired resolution of the second screen

    # Create and return a window for the experiment on the second monitor
    return visual.Window(monitor=second_monitor,  # Use the second monitor
                         size=(1920, 1080),
                         screen=2,  # Specify the index of the second screen (0 for the first screen, 1 for the second, etc.)
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

#   # Create a monitor object
#   currentMonitor = monitors.Monitor(name='testMonitor')

#   # Create and return a window for the experiment
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
        window (psychopy.visual.Window): The window object in which the stimuli will be displayed.

    Returns:
        tuple: A tuple containing all the stimuli and other related objects, which includes:

            werKommt (psychopy.visual.TextStim): Text stimulus for triggering question.
            fixation (psychopy.visual.ShapeStim): Visual stimulus for fixation cross.
            randNumber (psychopy.visual.TextStim): Text stimulus for displaying random number to be remembered.
            item (psychopy.visual.TextStim): Text stimulus for displaying item (stimulus or name coordinate) from list.
            prompt (psychopy.visual.TextStim): Text stimulus for displaying response prompt.
            feedback (psychopy.visual.TextStim): Text stimulus for displaying feedback.
            fs (int): Sample rate for recordings.
            rec_seconds (float): Recording duration in seconds, calculated based on visual frames and estimated frame rate.
            movementDirections (list): Possible directions for the dots to move.
            responseList (list): Corresponding responses to the movement directions.
            dots (psychopy.visual.DotStim): Dot stimulus object.
            arrows (list): List of visual.ImageStim objects representing arrows in different orientations.
            arrows_small (list): List of smaller visual.ImageStim objects representing arrows in different orientations.
            number_prompts (list): List of visual.TextStim objects for number prompts in different positions.
    """

    # set up different TextStim needed throughout experiment
    # trigger question
    werKommt = visual.TextStim(window,
                               text="Wer kommt?",
                               height=0.25,
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
                           pos=(0, 0),
                           height=0.25,
                           wrapWidth=2,
                           color="black",
                           name='item')

    # response prompt
    prompt = visual.TextStim(window,
                             color='black',
                             wrapWidth=2)
    # feedback
    feedback = visual.TextStim(window,
                               pos=(0, 0),
                               wrapWidth=2,
                               height=0.2)


    # default parameters for the recordings
    fs = 48000  # Sample rate
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
        fieldPos=(0, 0),  # position of the center of the stimulus field
        fieldShape="circle",  # shape of the stimulus field (circle in this case)
        dotSize=dot_size,  # size of each dot in pixels
        dotLife=-1,  # duration of each dot in frames (-1 for unlimited)
        coherence=dot_coherence,  # proportion of dots that move in the same direction
        nDots=n_dots,  # number of dots in the stimulus
        fieldSize=800,  # size of the stimulus field in pixels
        speed=dot_speed,  # speed of the dots in pixels per frame
        color=(0, 0, 0),  # color of the dots (black in this case)
        colorSpace='rgb'  # color space used to specify the color (RGB in this case)
    )

    # arrow parameters
    arrowPositions = [[0.18,0], [0,0.28], [-0.18,0], [0,-0.28]]  # position in the x-y-coordinate system
    arrowPositions_small = [[0.13, 0], [0, 0.23], [-0.13, 0], [0, -0.23]]  # position in the x-y-coordinate system
    arrowOrientations = [0, -90, -180, -270]  # rotation in degrees
    arrowSize = 0.2  # size in pixels?
    arrowSize_small = 0.12  # size in pixels?
    arrows = []  # empty list to append to
    arrows_small =  []

    # generate all arrows in correct orientation
    for i in range(4):
        arrow = visual.ImageStim(window,
                                image=os.path.join(pics_path, 'next.png'),
                                pos=arrowPositions[i],
                                size=arrowSize,
                                ori=arrowOrientations[i])
        arrows.append(arrow)

        arrow_small = visual.ImageStim(window,
                                 image=os.path.join(pics_path, 'next.png'),
                                 pos=arrowPositions_small[i],
                                 size=arrowSize_small,
                                 ori=arrowOrientations[i])
        arrows_small.append(arrow_small)

    # number parameters
    number_prompts_positions = [[0.29,0], [0,0.41], [-0.29,0], [0,-0.4]]  # position in the x-y-coordinate system
    number_prompts_size = 0.2  # size in pixels?

    number_prompts = []
    for i in range(4):
        number_prompt = visual.TextStim(
            win=window,
            text="0",  # placeholder text
            pos=number_prompts_positions[i],
            height=number_prompts_size,
            color='black'
        )
        number_prompts.append(number_prompt)


    return werKommt, fixation, randNumber, item, prompt, feedback, fs, rec_seconds, movementDirections, responseList, dots, arrows, arrows_small, number_prompts


def get_participant_info():
    """
    Open a dialogue box to get participant information, including the current date and time, subjectID, and experiment name.

    The function creates a dialogue box with pre-defined experiment parameters such as experiment name and the current date.
    The user is then required to input their unique subject ID.

    Returns:
        dict: A dictionary containing the participant's information, which includes:
            - 'experiment' (str): The name of the experiment, in this case, 'dual_task_experiment'.
            - 'subject' (str): The subject's unique identifier entered by the participant.
            - 'cur_date' (str): The current date and time when the function is executed, in 'YYYY-MM-DD_HHhMM' format.

    If the user cancels the dialog box, the function will terminate the experiment by calling core.quit().

    """

    # Define experiment name and configuration
    experiment_name = "Dual-Task"  # Production-Dual-Task
    experiment_config = {
        'experiment': 'dual_task_experiment',
        'subject': 'subjectID',
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
    Append a participant's trial result to a CSV file. This can correspond to different task results and the main CSV file with general parameters
    throughout all experiment parts. The main CSV file includes the single task parameter values as well as the dot-motion and calculation task parameters.

    The function takes in a dictionary of results and participant information, and a filename, then appends the results to the respective CSV file
    (either the main, beep_press, or beep_count file). If the file doesn't exist, it will create the file and add headers.

    Args:
        result (dict): A dictionary containing the data for a single trial.
        base_filename (str): The base name of the CSV file to which results are appended.
        participant_info (dict): A dictionary containing the participant's information, including experiment name, subjectID, and date.
        type (str, optional): Determines the type of task for which results are being recorded. It can be 'main' for the main trial results,
        'beep_press' for beep press task results, and 'beep_count' for beep count task results. Defaults to 'main'.

    Returns:
        None. The function directly writes the results to the CSV file.

    Raises:
        OSError: If there is an issue with accessing or writing to the CSV file.

    Notes:
        - The CSV file will be named "{base_filename}_{type}.csv".
        - The function appends the result data to the CSV file.
        - If the CSV file does not exist, it creates the file and adds the appropriate headers based on the type.
    """

    # Define the filename by appending the type of the task to the base filename
    filename = f"{base_filename}_{type}.csv"

    # Check if the file does not exist to write the header
    if not os.path.isfile(filename):
        with open(filename, 'w') as file:
            if type == 'main':
                file.write(
                'experiment,'
                'subjectID,'
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
                'number_selection,'
                'index_rand_nr,'
                'index_number_response,'
                'number_response_accuracy,'
                'beep_sequence,'
                'beep_press_trials,'
                'beep_press_deviant_trials,'
                'beep_press_normal_trials,'
                'beep_press_rt_correct,'
                'beep_press_rt_incorrect,'
                'beep_press_accuracy,'
                'beep_count_trials,'
                'beep_count_deviant_trials,'
                'beep_count_normal_trials,'
                'beep_count_number_selection,'
                'beep_count_index_correct_count,'            
                'beep_count_response,'
                'beep_count_response_accuracy,'
                'start_time,'
                'end_time,'
                'duration \n'
                )
            elif type == 'beep_press':
                file.write(
                    'experiment,'
                    'subjectID,'
                    'date,'
                    'task,'
                    'phase,'
                    'main_trial,'
                    'beep_press_trial,'
                    'beep_press_stimulus,'
                    'beep_press_rt,'
                    'beep_press_response_type,'
                    'beep_press_accuracy,'
                    'presentation,'
                    'start_time,'
                    'end_time,'
                    'duration \n'
                )
            elif type == 'beep_count':
                file.write(
                    'experiment,'
                    'subjectID,'
                    'date,'
                    'task,'
                    'phase,'
                    'main_trial,'
                    'beep_count_trial,'
                    'beep_count_stimulus,'
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
                result['number_selection'],
                result['index_rand_nr'],
                result['index_number_response'],
                result['number_response_accuracy'],
                result['beep_sequence'],
                result['beep_press_trials'],
                result['beep_press_deviant_trials'],
                result['beep_press_normal_trials'],
                result['beep_press_rt_correct'],
                result['beep_press_rt_incorrect'],
                result['beep_press_accuracy'],
                result['beep_count_trials'],
                result['beep_count_deviant_trials'],
                result['beep_count_normal_trials'],
                result['beep_count_number_selection'],
                result['beep_count_index_correct_count'],
                result['beep_count_response'],
                result['beep_count_response_accuracy'],
                result['start_time'],
                result['end_time'],
                result['duration']
            ])
        elif type == 'beep_press':
            writer.writerow([
                participant_info['experiment'],
                participant_info['subject'],
                participant_info['cur_date'],
                result['task'],
                result['phase'],
                result['main_trial'],
                result['beep_press_trial'],
                result['beep_press_stimulus'],
                result['beep_press_rt'],
                result['beep_press_response_type'],
                result['beep_press_accuracy'],
                result['presentation'],
                result['start_time'],
                result['end_time'],
                result['duration']
            ])
        elif type == 'beep_count':
            writer.writerow([
                participant_info['experiment'],
                participant_info['subject'],
                participant_info['cur_date'],
                result['task'],
                result['phase'],
                result['main_trial'],
                result['beep_count_trial'],
                result['beep_count_stimulus'],
                result['presentation'],
                result['start_time'],
                result['end_time'],
                result['duration']
            ])
