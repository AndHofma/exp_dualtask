"""
The single task procedure (execute_singleTask) involves the presentation of visual stimuli and the recording
of the participant's response (reading out loud).
The dual task procedure (execute_dualTask) involves the presentation of visual stimuli, along with math problems
and a moving-dots task, and records the participant's response (reading out loud) and
their response to the math problem and moving-dots task.
"""

# Import necessary libraries
from psychopy import prefs
# Set the audio library preference
prefs.hardware['audioLib'] = ['ptb', 'sounddevice', 'pygame', 'pyo']
# Now, import sound
from psychopy import sound, core, event, visual
import time
import datetime
import sounddevice as sd
from scipy.io.wavfile import write
import random
from dualtask_configuration import append_result_to_csv
import os
import numpy as np


# single task procedure
def execute_singleTask(window, results, subj_path_rec, stimuli, task_name, werKommt, fixation, item, rec_seconds,
                       fs, participant_info, base_filename):
    """
    Execute the single task procedure.

    This function takes a set of stimuli and a task name and runs the single task experiment.
    It presents the stimuli visually and records the participants' verbal responses.

    Args:
        window: The display window.
        results: A list to store the results.
        subj_path_rec: The path for the subject's recording.
        stimuli: The stimuli to be presented.
        task_name: The name of the task.
        werKommt: The "werKommt" stimulus.
        fixation: The fixation point stimulus.
        item: The item stimulus.
        rec_seconds: The recording duration in seconds.
        fs: The sample rate for the recording.
        participant_info: The participant's information.
        base_filename: The filename for the result CSV file.
    """
    # Initialize start time and format it into string
    start_time = time.time()
    start_time_str = datetime.datetime.fromtimestamp(start_time).strftime('%H:%M:%S')

    # Iterate through each stimulus in the provided stimuli
    for x in range(len(stimuli)):
        task = task_name  # store the task name

        # Present the "werKommt" stimulus, draw it, flip window, wait for 1 sec, and flip window again
        werKommt.name = 'werKommt'  # Naming the TextStim to find it in the log-file
        werKommt.draw()  # Draw stimulus to window
        window.flip()  # Flip window to make drawn stimulus visible
        core.wait(1.0)  # Wait for 1 sec
        window.flip()  # Flip window to clear stimulus

        # Repeat the same process for fixation stimulus
        fixation.name = 'fixation'
        fixation.draw()
        window.flip()
        core.wait(1.0)
        window.flip()

        # Set item TextStim and pic ImageStim based on the current stimulus in the iteration
        stimulus = stimuli.loc[x]['item']
        item.setText(stimulus)
        item.name = 'item_' + str(stimuli.loc[x]['ID'])  # Naming the TextStim to find it in the log-file

        # Start recording the participant's verbal response
        responseRecord = sd.rec(int(rec_seconds * fs), samplerate=fs, channels=1)

        # Present item and pic for 350 frames
        for frame in range(350):
            item.draw()  # Draw item
            window.flip()  # Flip window to make drawn items visible

        # Stop the recording after the presentation is over
        sd.stop()

        # Save the recording as a WAV file
        write(os.path.join(subj_path_rec, 'dualtask_' + participant_info['subject'] + '_' + task_name + '_' +
                           "{:02d}".format(x + 1) + '_' + str(stimuli.loc[x]['ID']) + '.wav'), fs, responseRecord)
        # naming the recording wav file to find it in the log-file
        responseRecordName = 'dualtask_' + participant_info['subject'] + '_' + task_name + '_' + \
                             "{:02d}".format(x + 1) + '_' + str(stimuli.loc[x]['ID']) + '.wav'

        # Calculate and format end time and duration
        end_time = time.time()
        end_time_str = datetime.datetime.fromtimestamp(end_time).strftime('%H:%M:%S')
        duration = end_time - start_time
        hours, remainder = divmod(duration, 3600)
        minutes, seconds = divmod(remainder, 60)
        duration_str = '{:02d}:{:02d}:{:02d}'.format(int(hours), int(minutes), int(seconds))

        # Prepare the result dictionary
        results.append({
            'task': task,
            'main_trial': "{:02d}".format(x + 1),
            'phase': 'practice' if task_name.startswith('practice') else 'test',
            'stimulus_id': stimuli.loc[x]['ID'],
            'stimulus': stimuli.loc[x]['item'],
            'stimulus_rec': responseRecordName,
            'dot_direction': 'NA',
            'dot_1st_frame': 'NA',
            'dot_last_frame': 'NA',
            'dot_response_key': 'NA',
            'dot_response_accuracy': 'NA',
            'beep_sequence':'NA',
            'beep_count_trials': 'NA',
            'beep_count_deviant_trials': 'NA',
            'beep_count_normal_trials': 'NA',
            'beep_count_number_selection': 'NA',
            'beep_count_index_correct_count': 'NA',
            'beep_count_response': 'NA',
            'beep_count_response_accuracy': 'NA',
            'start_time': start_time_str,
            'end_time': end_time_str,
            'duration': duration_str,
        })
        # Append the result to the CSV file
        append_result_to_csv(results[-1], base_filename, participant_info)


# dual task procedure
def execute_dualTask_beep_count_dots(window, results, base_filename, subj_path_rec, stimuli, task_name, werKommt,
                                     fixation, item, prompt, feedback, fs, rec_seconds, movementDirections,
                                     responseList, dots, arrows, arrows_small, number_prompts, participant_info):
    """
    Executes a dual-task experiment where the participant is asked to count beeps and track moving dots.
    The participant's responses are recorded for analysis.

    Parameters:
    window : object
        The window object where all the visual stimuli are drawn.
    results : list
        A list to hold the results of the experiment.
    base_filename : str
        The base filename for all output files.
    subj_path_rec : str
        The path to save the recordings of the participant's responses.
    stimuli : DataFrame
        A DataFrame containing the stimuli for the experiment.
    task_name : str
        The name of the task to be executed.
    werKommt : object
        Text stimulus object for drawing.
    fixation : object
        Shape stimulus object for drawing.
    item : object
        Text stimulus object for drawing the main task.
    prompt : object
        Text stimulus object for drawing instructions.
    feedback : object
        Text stimulus object for drawing feedback.
    fs : int
        The sampling frequency for recording.
    rec_seconds : int
        The duration of recording in seconds.
    movementDirections : list
        List of possible movement directions for the dots.
    responseList : list
        List of possible responses from the participant.
    dots : object
        Dot stimulus object for drawing.
    arrows : list
        List of arrow stimulus objects for drawing.
    arrows_small : list
        List of small arrow stimulus objects for drawing.
    number_prompts : list
        List of number prompt stimulus objects for drawing.
    participant_info : dict
        Dictionary containing information about the participant.

    Returns:
    None
    """

    # List of random numbers, same order for every participant
    if task_name == 'practice_beep_count_dots':
        random.seed(424)  # Set a random seed for reproducibility - here to get same list of nrs for practice
    elif task_name == 'test_beep_count_dots':
        random.seed(6667)  # Set a random seed for reproducibility - here to get same list of nrs for test

    # Initialize start time and start_time_str
    start_time = time.time()
    start_time_str = datetime.datetime.fromtimestamp(start_time).strftime('%H:%M:%S')

    # Beep configuration
    beep_duration = 0.2  # Duration of each beep in seconds

    # Iterate over stimuli
    for x in range(len(stimuli)):
        task = task_name

        # Generate a random start and end frame for the main task stimulus presentation
        start_offset = random.randint(300, 601)  # random number between 300 and 600
        end_offset = start_offset + 350

        # Randomly select a movement direction and a start/end frame for the moving dots
        movement = random.choice(movementDirections)
        rand1stFrame = random.randint((start_offset+15), (start_offset+50))
        randLastFrame = rand1stFrame + 250

        # naming the TextStim to find it in the log-file
        werKommt.name = 'werKommt'
        werKommt.draw()
        window.flip()
        core.wait(1.0)
        window.flip()

        # naming the ShapeStim to find it in the log-file
        fixation.name = 'fixation'
        fixation.draw()
        window.flip()
        core.wait(1.0)
        window.flip()

        stimulus = stimuli.loc[x]['item']
        item.setText(stimulus)
        # naming the TextStim to find it in the log-file
        item.name = 'item_' + str(stimuli.loc[x]['ID'])

        # start recording the participant response - reading out loud the stimulus
        responseRecord = sd.rec(int(rec_seconds * fs), samplerate=fs, channels=1)
        beep_type = 'NA'
        beep_counter = 0
        beep_sequence = []  # List to store the beep sounds played within the current main trial
        beep_count_results = []
        is_row_added = False  # Flag variable to track if a row has been added for the condition

        for frame in range(1200):  # Loop for 1200 frames
            # Check if it's time to play a beep sound
            if frame % 35 == 0 and frame >= 49:

                # If the first 3 beeps have not yet been generated, they should be normal
                if beep_counter < 3:
                    beep_sound = sound.Sound('C', octave=5, secs=beep_duration)
                    beep_type = 'normal'
                else:
                    # Ensure that there are at least 3 deviants in the sequence
                    deviants_so_far = beep_sequence.count('deviant')
                    remaining_beeps = 22 - beep_counter  # assuming you have 23 beeps in total

                    if deviants_so_far < 3 and remaining_beeps <= (3 - deviants_so_far):
                        beep_sound = sound.Sound('A', octave=5, secs=beep_duration)
                        beep_type = 'deviant'
                    else:
                        # Calculate the probability of generating a deviant beep
                        if deviants_so_far >= 3:
                            deviant_prob = min(0.5, deviants_so_far / (beep_counter - 3))
                        else:
                            deviant_prob = 0.5

                        if np.random.rand() < deviant_prob:
                            beep_sound = sound.Sound('A', octave=5, secs=beep_duration)
                            beep_type = 'deviant'
                        else:
                            beep_sound = sound.Sound('C', octave=5, secs=beep_duration)
                            beep_type = 'normal'

                # Play the beep sound if it is not in the item presentation or dot presentation phase
                if not start_offset - 10 <= frame < end_offset + 10:
                    beep_sound.play()

                    # Increment the beep counter
                    beep_counter += 1

                    # Append the beep sound to the current trial's beep sequence
                    beep_sequence.append(beep_type)

                    # Record end time and duration
                    end_time = time.time()
                    end_time_str = datetime.datetime.fromtimestamp(end_time).strftime('%H:%M:%S')
                    duration = end_time - start_time
                    hours, remainder = divmod(duration, 3600)
                    minutes, seconds = divmod(remainder, 60)
                    duration_str = '{:02d}:{:02d}:{:02d}'.format(int(hours), int(minutes), int(seconds))

                    # Append the data of the current trial to the results
                    beep_count_results.append({
                        'task': task_name,
                        'phase':'practice' if task_name.startswith('practice') else 'test',
                        'main_trial': "{:02d}".format(x + 1),
                        'beep_count_trial': beep_counter,
                        'beep_count_stimulus': beep_type,
                        'presentation': 'dual' if start_offset <= frame < end_offset else 'single',
                        'start_time': start_time_str,
                        'end_time': end_time_str,
                        'duration': duration_str,
                    })

                # Add a row for frames when item is shown
                if start_offset - 10 <= frame < end_offset + 10:

                    # Record end time and duration
                    end_time = time.time()
                    end_time_str = datetime.datetime.fromtimestamp(end_time).strftime('%H:%M:%S')
                    duration = end_time - start_time
                    hours, remainder = divmod(duration, 3600)
                    minutes, seconds = divmod(remainder, 60)
                    duration_str = '{:02d}:{:02d}:{:02d}'.format(int(hours), int(minutes), int(seconds))

                    # Append the data of the current trial to the results if a row hasn't been added already
                    if not is_row_added:
                        beep_count_results.append({
                        'task': task_name,
                        'phase':'practice' if task_name.startswith('practice') else 'test',
                        'main_trial': "{:02d}".format(x + 1),
                        'beep_count_trial': 'pause for ' + str(end_offset-start_offset) + 'frames',
                        'beep_count_stimulus': 'none',
                        'presentation': 'name_coordinate and dots',
                        'start_time': start_time_str,
                        'end_time': end_time_str,
                        'duration': duration_str,
                    })
                    is_row_added = True

            # reading aloud primary task
            if start_offset <= frame < end_offset:  # This means that if the current frame is between start_offset and end_offset, it is the time to show the main task
                item.draw()  # Drawing the name of the image on the screen

                if frame == start_offset:  # If we are at the start of the primary task
                    # Start recording the participant's spoken response
                    responseRecord = sd.rec(int(rec_seconds * fs), samplerate=fs, channels=1)

                if frame == end_offset - 1:  # If we are at the end of the primary task
                    # Stop recording the participant's spoken response
                    sd.stop()
                    # Save the spoken response as a .wav file
                    write(os.path.join(subj_path_rec,
                                       'dualtask_' + participant_info['subject'] + '_' + task_name + '_' +
                                       "{:02d}".format(x + 1) + '_' + str(stimuli.loc[x]['ID']) + '.wav'),
                          fs, responseRecord)

            if rand1stFrame <= frame < randLastFrame:  # Present dots for subset of frames
                dots.dir = movement
                dots.draw()

            window.flip()

        for result in beep_count_results:
            append_result_to_csv(result, base_filename, participant_info, type='beep_count')

        # Reset the flag for the next trial
        is_row_added = False

        core.wait(2)

        # show first response screen
        prompt.setText('Drücken Sie den Richtungs-Pfeil auf der Tastatur,\n in die sich die Punkte bewegt haben.')
        prompt.pos = (0, -0.6)
        prompt.size = 0.12
        prompt.draw()

        # these are the arrows pointing at 0,90,180,270 degrees - resembling movement direction of dots
        for arrow in arrows:
            arrow.draw()
        window.flip()

        # wait for a response - allowed are the key buttons on the keypad
        arrowKey = event.waitKeys(keyList=responseList)
        # compare input arrow key with movement direction to check accuracy
        if responseList.index(arrowKey[0]) == movementDirections.index(movement):
            dot_Accuracy = 'correct'
            feedback.setText('Korrekt!')
            feedback.setColor('black')
            feedback.draw()
        else:
            dot_Accuracy = 'incorrect'
            feedback.setText('Inkorrekt!')
            feedback.setColor('black')
            feedback.draw()
        window.flip()

        core.wait(2)

        number_selection, correct_index = select_and_replace_number(beep_sequence.count('deviant'))

        # now number_prompts have been created and are of the same length as number_selection
        for i, arrow in zip(range(len(number_selection)), arrows_small):
            number_prompts[i].text = str(number_selection[i])
            number_prompts[i].draw()
            arrow.draw()

        # show second response screen
        prompt.setText('Wieviele hohe Töne haben Sie gehört?\n Drücken Sie den entsprechenden Pfeil auf der Tastatur.')
        prompt.pos = (0, -0.75)
        prompt.size = 0.12
        prompt.draw()

        window.flip()

        # wait for a response - allowed are the key buttons on the keypad
        arrowKey_number = event.waitKeys(keyList=responseList)
        # compare input arrow key with movement direction to check accuracy
        if responseList.index(arrowKey_number[0]) == correct_index:
            numbers_accuracy = 'correct'
            feedback.setText('Korrekt!')
            feedback.setColor('black')
            feedback.draw()
        else:
            numbers_accuracy = 'incorrect'
            feedback.setText('Inkorrekt!')
            feedback.setColor('black')
            feedback.draw()
        window.flip()

        core.wait(2)

        # Define a file name for the response record
        responseRecordName = 'dualtask_' + participant_info['subject'] + '_' + task_name + '_' + \
                             "{:02d}".format(x + 1) + '_' + str(stimuli.loc[x]['ID']) + '.wav'

        # Record end time and duration
        end_time = time.time()
        end_time_str = datetime.datetime.fromtimestamp(end_time).strftime('%H:%M:%S')
        duration = end_time - start_time
        hours, remainder = divmod(duration, 3600)
        minutes, seconds = divmod(remainder, 60)
        duration_str = '{:02d}:{:02d}:{:02d}'.format(int(hours), int(minutes), int(seconds))

        # Filter single presentation trials
        count_results_trials_single = [r for r in beep_count_results if
                             'presentation' in r and r['presentation'] == 'single']

        beep_count_trials = len(count_results_trials_single)

        # Filter deviants in single presentation trials
        count_results_trials_single_deviant = [r for r in beep_count_results if
                               'presentation' and 'beep_count_stimulus' in r and
                                        r['presentation'] == 'single' and
                                        r['beep_count_stimulus'] == 'deviant']

        # Calculate the number of single deviant presentation trials
        beep_count_trials_deviant = len(count_results_trials_single_deviant)

        # Calculate the number of single normal presentation trials
        beep_count_trials_normal = beep_count_trials - beep_count_trials_deviant

        beep_count_results.clear()  # Clear beep_results after writing to CSV

        # Prepare the result dictionary
        results.append({
            'task': task,
            'main_trial': "{:02d}".format(x + 1),
            'phase': 'practice' if task_name.startswith('practice') else 'test',
            'stimulus_id': stimuli.loc[x]['ID'],
            'stimulus': stimuli.loc[x]['item'],
            'stimulus_rec': responseRecordName,
            'dot_direction': movement,
            'dot_1st_frame': rand1stFrame,
            'dot_last_frame': randLastFrame,
            'dot_response_key': arrowKey,
            'dot_response_accuracy': dot_Accuracy,
            'beep_sequence':str(beep_sequence),
            'beep_count_trials': beep_count_trials,
            'beep_count_deviant_trials': beep_count_trials_deviant,
            'beep_count_normal_trials': beep_count_trials_normal,
            'beep_count_number_selection': str(number_selection),
            'beep_count_index_correct_count': correct_index,
            'beep_count_response': str(arrowKey_number[0]),
            'beep_count_response_accuracy': numbers_accuracy,
            'start_time': start_time_str,
            'end_time': end_time_str,
            'duration': duration_str,
        })
        # Append the result to the CSV file
        append_result_to_csv(results[-1], base_filename, participant_info)


# Display instructions consecutively
def execute_task(window, task_name, participant_info, stimuli, werKommt, fixation, item, prompt,
                 feedback, fs, rec_seconds, movementDirections, responseList, dots, arrows, arrows_small,
                 number_prompts, dual_task=False):
    """
    Executes a task for a participant based on the task_name and type (single or dual).
    It sets up paths for recording and results, checks the task name to call the appropriate
    task execution function, and displays end-of-practice instructions.

    Parameters:
    window : object
        The window object where all the visual stimuli are drawn.
    task_name : str
        The name of the task to be executed.
    participant_info : dict
        Dictionary containing information about the participant.
    stimuli : DataFrame
        A DataFrame containing the stimuli for the experiment.
    werKommt : object
        Text stimulus object for drawing.
    fixation : object
        Shape stimulus object for drawing.
    item : object
        Text stimulus object for drawing the main task.
    prompt : object
        Text stimulus object for drawing instructions.
    feedback : object
        Text stimulus object for drawing feedback.
    fs : int
        The sampling frequency for recording.
    rec_seconds : int
        The duration of recording in seconds.
    movementDirections : list
        List of possible movement directions for the dots.
    responseList : list
        List of possible responses from the participant.
    dots : object
        Dot stimulus object for drawing.
    arrows : list
        List of arrow stimulus objects for drawing.
    arrows_small : list
        List of small arrow stimulus objects for drawing.
    number_prompts : list
        List of number prompt stimulus objects for drawing.
    dual_task : bool, optional
        Whether the task to be executed is a dual task or a single task (default is False).

    Returns:
    None

    Notes:
    Depending on the task_name and whether the task is a dual task, different tasks are executed.
    These are: 'practice_number_dots', 'test_number_dots', 'practice_number_beep_press',
    'test_number_beep_press', 'practice_beep_count_dots', 'test_beep_count_dots', and
    'practice_single'. For each task, an end-of-practice instruction is displayed. Directories for storing the
    results and recordings are created if they do not already exist. The results of the task are saved to a
    results file, and a base filename is generated for the task.
    """

    # Initialize an empty list to hold the results
    results = []
    # Import the end-of-practice instructions
    from dualtask_instructions import instructPracticeSingleTaskEnd,  instructPracticeDualTask_beep_count_dots_End

    # path setup results per participant
    # Define the path in results for each subject
    subj_path_results = os.path.join('results', participant_info['subject'])
    # Create the directory if it doesn't exist
    if not os.path.exists(subj_path_results):
        os.makedirs(subj_path_results)
    # generate the base_filename based on task_name and phase
    base_filename = os.path.join(subj_path_results,
                            f"{task_name}_{participant_info['subject']}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}")

    # path setup recordings per participant
    # Define the path in recordings for each subject
    subj_path_rec = os.path.join('recordings', participant_info['subject'])
    # Create the directory if it doesn't exist
    if not os.path.exists(subj_path_rec):
        os.makedirs(subj_path_rec)

    # Execute the task and save the result
    if dual_task:
        if task_name == 'practice_beep_count_dots':
            execute_dualTask_beep_count_dots(window, results, base_filename, subj_path_rec, stimuli, task_name, werKommt,
                                             fixation, item, prompt, feedback, fs, rec_seconds, movementDirections,
                                             responseList, dots, arrows, arrows_small, number_prompts, participant_info)
            display_text_and_wait(instructPracticeDualTask_beep_count_dots_End, window)
        if task_name == 'test_beep_count_dots':
            execute_dualTask_beep_count_dots(window, results, base_filename, subj_path_rec, stimuli, task_name, werKommt,
                                             fixation, item, prompt, feedback, fs, rec_seconds, movementDirections,
                                             responseList, dots, arrows, arrows_small, number_prompts, participant_info)
    else:
        execute_singleTask(window, results, subj_path_rec, stimuli, task_name, werKommt, fixation, item, rec_seconds,
                           fs, participant_info, base_filename)
        if task_name == 'practice_single':
            display_text_and_wait(instructPracticeSingleTaskEnd, window)


def display_and_wait(element, window):
    """
    Displays a given screen element, flips the window, and then waits for any key press.

    Args:
        element: A psychopy visual element (TextStim, ImageStim, etc.) to be displayed on the screen.
        window: A psychopy.visual.Window object where the element will be displayed.

    Returns:
        keys: List of the keys that were pressed while waiting.
    """
    # Draw the provided element and flip window
    element.draw()
    window.flip()
    # Wait for any key to be pressed to display the next screen
    keys = event.waitKeys(keyList=['return'])

    return keys


def display_text_and_wait(text_string, window):
    """
    This function creates a TextStim object from a provided string, then draws it and waits for any key press.

    Args:
        text_string: The string to be displayed.
        window: The window to draw on.

    Returns:
        keys: A list of the keys that were pressed.
    """
    text_stim = visual.TextStim(window, text=text_string, color='black', wrapWidth=2)

    return display_and_wait(text_stim, window)


def select_and_replace_number(given_number):
    """
    Based on the given number, this function generates three random numbers that are within the
    same tens or ones range. It then combines these numbers with the given number,
    and randomly shuffles them to produce a list of four numbers.

    Parameters:
    given_number : int
        The base number based on which three other numbers are generated.

    Returns:
    numbers : list of int
        List of four numbers where one of the numbers is the given_number.
    replace_index : int
        The index at which the given_number is placed in the list.
    """

    # Check the range of the given_number
    if given_number < 10:
        range_start = given_number - 2
        range_end = given_number + 2
    else:
        num_str = str(given_number)
        range_start = int(num_str[:-1] + '0')
        range_end = int(num_str[:-1] + '9')

    # Create a list of all numbers in the range except the given_number
    range_without_given = [i for i in range(range_start, range_end + 1) if i != given_number]

    # Randomly select 3 numbers from this list
    numbers = random.sample(range_without_given, 3)

    # Add the given_number to the list and shuffle
    numbers.append(given_number)
    random.shuffle(numbers)

    # Get the index of the given_number
    replace_index = numbers.index(given_number)

    return numbers, replace_index
