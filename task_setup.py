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
from psychopy.hardware import keyboard
import time
import datetime
import sounddevice as sd
from scipy.io.wavfile import write
import random
from configuration import append_result_to_csv
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

        # Present item and pic for 300 frames
        for frame in range(300):
            item.draw()  # Draw item
            window.flip()  # Flip window to make drawn items visible

        # Stop the recording after the presentation is over
        sd.stop()

        # Save the recording as a WAV file
        write(os.path.join(subj_path_rec, 'single_task_' + participant_info['subject'] + '_' + task_name + '_' + str(stimuli.loc[x]['ID']) + '.wav'), fs, responseRecord)
        # naming the recording wav file to find it in the log-file
        responseRecordName = 'single_task_' + participant_info['subject'] + '_' + task_name + '_' + str(stimuli.loc[x]['ID']) + '.wav'

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
            'main_trial': str(x+1),
            'phase': 'practice' if task_name.startswith('practice') else 'test',
            'stimulus_id': stimuli.loc[x]['ID'],
            'stimulus': stimuli.loc[x]['item'],
            'stimulus_rec': responseRecordName,
            'rand_nr': 'NA',
            'dot_direction': 'NA',
            'dot_1st_frame': 'NA',
            'dot_last_frame': 'NA',
            'dot_response_key': 'NA',
            'dot_response_accuracy': 'NA',
            'number_selection': 'NA',
            'index_rand_nr':'NA',
            'index_number_response':'NA',
            'number_response_accuracy':'NA',
            'beep_sequence':'NA',
            'beep_press_trials':'NA',
            'beep_press_deviant_trials': 'NA',
            'beep_press_normal_trials': 'NA',
            'beep_press_rt_correct':'NA',
            'beep_press_rt_incorrect':'NA',
            'beep_press_accuracy':'NA',
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
def execute_dualTask_number_dots(window, results, base_filename, subj_path_rec, stimuli, task_name, werKommt,
                                 fixation, randNumber, item, prompt, feedback, fs, rec_seconds, movementDirections,
                                 responseList, dots, arrows, arrows_small, number_prompts, participant_info):
    """
    Execute the dual-task experiment, collect the data, and save it in a CSV file.

    The experiment involves tasks related to number recognition and dot movement. During the experiment,
    participants view a stimulus, then report on the direction in which the majority of dots moved and the number they memorized.

    Args:
        window (Window): The window to display the experiment.
        results (list of dict): The list to store experiment results.
        base_filename (str): The base name of the CSV file to save results.
        subj_path_rec (str): The path to the directory to save the recorded responses.
        stimuli (pd.DataFrame): The dataframe containing stimuli data.
        task_name (str): The name of the task ('practice_dualTask_number_dots' or 'test_dualTask_number_dots').
        werKommt (VisualStim): Visual stimulus object for displaying a cue.
        fixation (ShapeStim): The fixation point.
        randNumber (TextStim): The random number to display.
        item (TextStim): The TextStim object to display the stimulus.
        prompt (TextStim): The TextStim object to display the instruction.
        feedback (TextStim): The TextStim object to display the feedback.
        fs (int): The sample rate for recording the participant's response.
        rec_seconds (int): The duration in seconds to record the participant's response.
        movementDirections (list of int): The list of possible movement directions for the dots.
        responseList (list of str): The list of keys that can be pressed for response.
        dots (DotStim): The DotStim object to display the moving dots.
        arrows (list of ShapeStim): The list of ShapeStim objects to display arrows.
        arrows_small (list of ShapeStim): The list of small ShapeStim objects to display arrows.
        number_prompts (list of TextStim): The list of TextStim objects to display the number prompts.
        participant_info (dict): The dictionary to store participant information.

    Returns:
        None

    Notes:
        - The function directly writes the results to the CSV file after each trial.
    """

    # Setting up random seed for reproducibility based on the task type
    if task_name == 'practice_dualTask_number_dots':
        random.seed(42)  # Seed for practice trials
    elif task_name == 'test_dualTask_number_dots':
        random.seed(666)  # Seed for test trials
    # Generating list of random numbers for each trial
    randNr = [random.randint(100, 999) for _ in range(len(stimuli))]
    # Initialize start time and start_time_str
    start_time = time.time()
    start_time_str = datetime.datetime.fromtimestamp(start_time).strftime('%H:%M:%S')
    # Iterate over stimuli
    for x in range(len(stimuli)):
        task = task_name
        # Randomly select a movement direction and a start/end frame for the moving dots
        movement = random.choice(movementDirections)
        rand1stFrame = random.randint(40, 70)
        randLastFrame = random.randint(190, 220)
        # Select and replace a number in the selection
        number_selection, correct_index = select_and_replace_number(task_name, randNr[x])
        # Setting up number_prompts with numbers from number_selection
        for i in range(len(number_selection)):
            number_prompts[i].text = str(number_selection[i])  # set each prompt with corresponding number
        # Displaying the random number and setting its name and size for logging
        randNumber.setText(randNr[x])
        randNumber.name = 'randNumber_' + task_name + '_' + str(randNr)
        randNumber.size = 0.5
        randNumber.draw()
        window.flip()
        core.wait(2.0)
        window.flip()
        # Displaying 'werKommt' text stimulus
        werKommt.name = 'werKommt'
        werKommt.draw()
        window.flip()
        core.wait(1.0)
        window.flip()
        # Displaying fixation cross
        fixation.name = 'fixation'
        fixation.draw()
        window.flip()
        core.wait(1.0)
        window.flip()
        # Displaying stimulus
        stimulus = stimuli.loc[x]['item']
        item.setText(stimulus)
        item.name = 'item_' + str(stimuli.loc[x]['ID'])
        # Start recording the participant's response
        responseRecord = sd.rec(int(rec_seconds * fs), samplerate=fs, channels=1)
        # Draw stimulus and dots for specific frames
        for frame in range(350):
            item.draw()
            if rand1stFrame <= frame < randLastFrame:  # Present dots for subset of frames
                dots.dir = movement
                dots.draw()
            window.flip()
        sd.stop()  # stop the recording
        # Saving the response recording as a wav file
        responseRecordName = 'dual_task_' + participant_info['subject'] + '_' + task_name + '_' + str(stimuli.loc[x]['ID']) + '.wav'
        write(os.path.join(subj_path_rec, 'dual_task_' + participant_info['subject'] + '_' + task_name + '_' + str(stimuli.loc[x]['ID']) + '.wav'), fs, responseRecord)
        # Displaying first response screen and collecting the response
        prompt.setText('In welche Richtung haben sich die meisten Punkte bewegt?\n Drücken Sie den entsprechenden Pfeil auf der Tastatur.')
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
            dot_accuracy = 'correct'
            feedback.setText('Korrekt!')
            feedback.setColor('green')
            feedback.draw()
        else:
            dot_accuracy = 'incorrect'
            feedback.setText('Inkorrekt!')
            feedback.setColor('red')
            feedback.draw()
        window.flip()
        core.wait(2)
        # Displaying second response screen and collecting the response
        prompt.setText('Welche Nummer haben Sie sich gemerkt?\n Drücken Sie den entsprechenden Pfeil auf der Tastatur.')
        prompt.pos = (0, -0.75)
        prompt.size = 0.12
        prompt.draw()
        # now each number_prompt has a number from number_selection
        for number_prompt, arrow_small in zip(number_prompts, arrows_small):
            number_prompt.draw()  # draw each number_prompt
            arrow_small.draw()
        window.flip()
        # wait for a response - allowed are the key buttons on the keypad
        arrowKey_number = event.waitKeys(keyList=responseList)
        # compare input arrow key with movement direction to check accuracy
        if responseList.index(arrowKey_number[0]) == correct_index:
            numbers_accuracy = 'correct'
            feedback.setText('Korrekt!')
            feedback.setColor('green')
            feedback.draw()
        else:
            numbers_accuracy = 'incorrect'
            feedback.setText('Inkorrekt!')
            feedback.setColor('red')
            feedback.draw()
        window.flip()
        core.wait(2)
        # Record end time and duration
        end_time = time.time()
        end_time_str = datetime.datetime.fromtimestamp(end_time).strftime('%H:%M:%S')
        duration = end_time - start_time
        hours, remainder = divmod(duration, 3600)
        minutes, seconds = divmod(remainder, 60)
        duration_str = '{:02d}:{:02d}:{:02d}'.format(int(hours), int(minutes), int(seconds))
        # Prepare the result dictionary
        results.append({
            'task': task,
            'main_trial': str(x+1),
            'phase': 'practice' if task_name.startswith('practice') else 'test',
            'stimulus_id': stimuli.loc[x]['ID'],
            'stimulus': stimuli.loc[x]['item'],
            'stimulus_rec': responseRecordName,
            'rand_nr': str(randNr[x]),
            'dot_direction': movement,
            'dot_1st_frame': rand1stFrame,
            'dot_last_frame': randLastFrame,
            'dot_response_key': arrowKey,
            'dot_response_accuracy': dot_accuracy,
            'number_selection':str(number_selection),
            'index_rand_nr':correct_index,
            'index_number_response':str(arrowKey_number[0]),
            'number_response_accuracy':numbers_accuracy,
            'beep_sequence':'NA',
            'beep_press_trials':'NA',
            'beep_press_deviant_trials': 'NA',
            'beep_press_normal_trials': 'NA',
            'beep_press_rt_correct':'NA',
            'beep_press_rt_incorrect':'NA',
            'beep_press_accuracy':'NA',
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


def execute_dualTask_number_beep_press(window, results, base_filename, subj_path_rec, stimuli, task_name, werKommt,
                                       fixation, randNumber, item, prompt, feedback, fs, rec_seconds, responseList,
                                       arrows_small, number_prompts, participant_info):
    """
    Executes a dual task where the participant listens for a specific beep sound while reading aloud a stimulus.

    The participant is also required to press a button when they hear the beep sound. The task requires the participant
    to split their attention between reading aloud and listening for a beep. The task records the spoken response
    of the participant and their reaction to the beep sounds. Results are recorded and written to a CSV file.

    Parameters
    ----------
    window: obj
        The window object where the stimuli are presented.
    results: list
        The list that stores the results of the task.
    base_filename: str
        The base filename to be used for writing the results to a CSV file.
    subj_path_rec: str
        The path where the recordings of the participant's responses are saved.
    stimuli: DataFrame
        The dataframe containing the stimuli for the task.
    task_name: str
        The name of the task, which can be either 'practice_dualTask_number_beep_press' or 'test_dualTask_number_beep_press'.
    werKommt: obj
        The TextStim object used to display the "Wer kommt?" message.
    fixation: obj
        The ShapeStim object used for the fixation cross.
    randNumber: obj
        The TextStim object used to display random numbers.
    item: obj
        The TextStim object used to display the stimuli items.
    prompt: obj
        The TextStim object used to display prompts to the participant.
    feedback: obj
        The TextStim object used to display feedback to the participant.
    fs: int
        The sampling rate for the audio recording.
    rec_seconds: int
        The number of seconds to record the participant's response.
    responseList: list
        The list of possible responses from the participant.
    arrows_small: list
        The list of ArrowStim objects used to display the possible responses.
    number_prompts: list
        The list of TextStim objects used to display the number prompts.
    participant_info: dict
        A dictionary containing information about the participant, like the subject number.

    Returns
    -------
    None
    """
    # Initialize the keyboard
    keyBoard = keyboard.Keyboard()
    keyBoard.clock.reset()

    # List of random numbers, same order for every participant
    if task_name == 'practice_dualTask_number_beep_press':
        random.seed(242)  # Set a random seed for reproducibility - here to get same list of nrs for practice
    elif task_name == 'test_dualTask_number_beep_press':
        random.seed(7666)  # Set a random seed for reproducibility - here to get same list of nrs for test

    randNr = [random.randint(100, 999) for _ in range(len(stimuli))]

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

        number_selection, correct_index = select_and_replace_number(task_name,randNr[x])

        # naming the TextStim to find it in the log-file
        randNumber.setText(randNr[x])
        randNumber.name = 'randNumber_' + task_name + '_' + str(randNr)
        randNumber.size = 0.5
        randNumber.draw()
        window.flip()
        core.wait(2.0)
        window.flip()

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
        beep_press_results = []
        is_row_added = False  # Flag variable to track if a row has been added for the condition

        for frame in range(1200):  # Loop for 1200 frames
            # Check if it's time to play a beep sound
            if frame % 50 == 0 and frame >= 49:

                keyBoard.clearEvents()  # Clear events immediately after processing a key press
                keyBoard.clock.reset()  # Reset the keyboard clock

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
                if not start_offset-10 <= frame < end_offset+10:
                    beep_sound.play()

                    # Record end time and calculate duration of the trial
                    end_time = time.time()
                    end_time_str = datetime.datetime.fromtimestamp(end_time).strftime('%H:%M:%S')
                    duration = end_time - start_time
                    hours, remainder = divmod(duration, 3600)
                    minutes, seconds = divmod(remainder, 60)
                    duration_str = '{:02d}:{:02d}:{:02d}'.format(int(hours), int(minutes), int(seconds))

                    # Increment the beep counter
                    beep_counter += 1

                    # Append the beep sound to the current trial's beep sequence
                    beep_sequence.append(beep_type)

                    # Append the data of the current trial to the results
                    beep_press_results.append({
                        'task': task_name,
                        'phase': 'practice' if task_name.startswith('practice') else 'test',
                        'main_trial': x + 1,
                        'beep_press_trial': beep_counter,
                        'beep_press_stimulus': beep_type,
                        'beep_press_rt': 'NA',
                        'beep_press_response_type': 'NA',
                        'beep_press_accuracy': 'NA',
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
                        # Append the data of the current trial to the results
                        beep_press_results.append({
                            'task': task_name,
                            'phase': 'practice' if task_name.startswith('practice') else 'test',
                            'main_trial': x + 1,
                            'beep_press_trial': 'pause for ' + str(end_offset-start_offset) + 'frames',
                            'beep_press_stimulus': 'none',
                            'beep_press_rt': 'NA',
                            'beep_press_response_type': 'NA',
                            'beep_press_accuracy': 'NA',
                            'presentation': 'name_coordinate',
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
                                       'dual_task_' + participant_info['subject'] + '_' + task_name + '_' + str(
                                           stimuli.loc[x]['ID']) + '.wav'), fs, responseRecord)

            if frame > 50 and frame < 1200:
                keys = keyBoard.getKeys(keyList=['space'], waitRelease=True)  # Check if the participant pressed 'space'
                # Find the corresponding beep stimulus in the results
                last_trial_idx = len(beep_press_results) - 1
                # If a key was pressed, process the response
                if keys:  # If there was a key press
                    # Process the response based on the beep stimulus
                    if beep_type == 'deviant':
                        accuracy = 'correct'
                        response_type = 'hit'
                        reaction_time = keys[0].rt

                        beep_press_results[last_trial_idx]['beep_press_rt'] = reaction_time
                        beep_press_results[last_trial_idx]['beep_press_accuracy'] = accuracy
                        beep_press_results[last_trial_idx]['beep_press_response_type'] = response_type

                        # Record end time and calculate duration of the trial
                        end_time = time.time()
                        end_time_str = datetime.datetime.fromtimestamp(end_time).strftime('%H:%M:%S')
                        duration = end_time - start_time
                        hours, remainder = divmod(duration, 3600)
                        minutes, seconds = divmod(remainder, 60)
                        duration_str = '{:02d}:{:02d}:{:02d}'.format(int(hours), int(minutes), int(seconds))

                        # Update end time and duration of the latest beep response result
                        beep_press_results[last_trial_idx]['end_time'] = end_time_str
                        beep_press_results[last_trial_idx]['duration'] = duration_str

                        # Clear events immediately after processing a key press
                        keyBoard.clearEvents()

                    else:
                        accuracy = 'incorrect'
                        response_type = 'false_alarm'
                        reaction_time = keys[0].rt

                        beep_press_results[last_trial_idx]['beep_press_rt'] = reaction_time
                        beep_press_results[last_trial_idx]['beep_press_accuracy'] = accuracy
                        beep_press_results[last_trial_idx]['beep_press_response_type'] = response_type

                    # Record end time and calculate duration of the trial
                    end_time = time.time()
                    end_time_str = datetime.datetime.fromtimestamp(end_time).strftime('%H:%M:%S')
                    duration = end_time - start_time
                    hours, remainder = divmod(duration, 3600)
                    minutes, seconds = divmod(remainder, 60)
                    duration_str = '{:02d}:{:02d}:{:02d}'.format(int(hours), int(minutes), int(seconds))

                    # Update end time and duration of the latest beep response result
                    beep_press_results[last_trial_idx]['end_time'] = end_time_str
                    beep_press_results[last_trial_idx]['duration'] = duration_str

                    # Clear any subsequent key presses during feedback
                    keyBoard.clearEvents()

            window.flip()

        # Code for evaluating non-responses after stimulus presentation...
        for result in beep_press_results:
            # Record end time and calculate duration of the task
            end_time = time.time()
            end_time_str = datetime.datetime.fromtimestamp(end_time).strftime('%H:%M:%S')
            duration = end_time - start_time
            hours, remainder = divmod(duration, 3600)
            minutes, seconds = divmod(remainder, 60)
            duration_str = '{:02d}:{:02d}:{:02d}'.format(int(hours), int(minutes), int(seconds))
            if 'beep_press_stimulus' in result:
                beep_stimulus = result['beep_press_stimulus']
                # Initialize accuracy with a default value
                accuracy = 'NA'
                # Process non-response based on the beep stimulus
                if beep_stimulus == 'deviant':
                    if result['beep_press_response_type'] == 'NA':
                        accuracy = 'incorrect'
                        response_type = 'miss'
                        # Update the last trial data with non-response information
                        result['beep_press_accuracy'] = accuracy
                        result['beep_press_response_type'] = response_type
                        result['end_time'] = end_time_str
                        result['duration'] = duration_str
                elif beep_stimulus == 'normal':
                    if result['beep_press_response_type'] == 'NA':
                        accuracy = 'correct'
                        response_type = 'none'
                        # Update the last trial data with non-response information
                        result['beep_press_accuracy'] = accuracy
                        result['beep_press_response_type'] = response_type
                        result['end_time'] = end_time_str
                        result['duration'] = duration_str

        # Reset the flag for the next trial
        is_row_added = False

        # After all trials and computations, write the results to the CSV file
        for result in beep_press_results:
            append_result_to_csv(result, base_filename, participant_info, type='beep_press')

        keyBoard.clearEvents()  # Clear keyboard events here too, so any subsequent key presses during feedback are ignored

        core.wait(1)

        # Filter deviants in single presentation trials
        deviants_correct = sum(
            1 for r in beep_press_results if
            'presentation' and 'beep_press_stimulus' and 'beep_press_accuracy' in r and
            r['presentation'] == 'single' and
            r['beep_press_stimulus'] == 'deviant' and
            r['beep_press_accuracy'] == 'correct'
        )

        deviants = sum(
            1 for r in beep_press_results if
            'presentation' and 'beep_press_stimulus' in r and
            r['presentation'] == 'single' and
            r['beep_press_stimulus'] == 'deviant')

        # show second response screen
        prompt.setText('Korrekt erkannt: ' + str(deviants_correct) + ' von ' + str(deviants))
        prompt.pos = (0, 0)
        prompt.size = 0.12
        prompt.draw()
        window.flip()
        core.wait(2)

        # now number_prompts have been created and are of the same length as number_selection
        for i, arrow in zip(range(len(number_selection)), arrows_small):
            number_prompts[i].text = str(number_selection[i])
            number_prompts[i].draw()
            arrow.draw()

        # show second response screen
        prompt.setText('Welche Nummer haben Sie sich gemerkt?\n Drücken Sie den entsprechenden Pfeil auf der Tastatur.')
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
            feedback.setColor('green')
            feedback.draw()
        else:
            numbers_accuracy = 'incorrect'
            feedback.setText('Inkorrekt!')
            feedback.setColor('red')
            feedback.draw()
        window.flip()

        core.wait(2)

        # Define a file name for the response record
        responseRecordName = 'dual_task_' + participant_info['subject'] + '_' + task_name + '_' + str(
            stimuli.loc[x]['ID']) + '.wav'

        # Record end time and duration
        end_time = time.time()
        end_time_str = datetime.datetime.fromtimestamp(end_time).strftime('%H:%M:%S')
        duration = end_time - start_time
        hours, remainder = divmod(duration, 3600)
        minutes, seconds = divmod(remainder, 60)
        duration_str = '{:02d}:{:02d}:{:02d}'.format(int(hours), int(minutes), int(seconds))

        # Filter single presentation trials
        beep_press_results_all = [r for r in beep_press_results if
                               'presentation' in r and r['presentation'] == 'single']

        # Calculate the number of single presentation trials
        beep_press_trials = len(beep_press_results_all)

        # Filter deviants in single presentation trials
        beep_press_results_deviants = [r for r in beep_press_results if
                               'presentation' and 'beep_press_stimulus' in r and
                                        r['presentation'] == 'single' and
                                        r['beep_press_stimulus'] == 'deviant']

        # Calculate the number of single deviant presentation trials
        beep_press_trials_deviant = len(beep_press_results_deviants)

        # Calculate the number of single deviant presentation trials
        beep_press_trials_normal = beep_press_trials - len(beep_press_results_deviants)

        beep_press_results.clear()  # Clear beep_press_results after writing to CSV

        # Calculate the accuracy for single presentation trials if there are any
        beep_press_trial_accuracy = sum(r['beep_press_accuracy'] == 'correct' for r in
                                         beep_press_results_all) / beep_press_trials if beep_press_trials else None

        # Calculate the number of correct responses for single presentation trials where the reaction time is not NA
        beep_press_correct_and_not_na = sum(
            1 for r in beep_press_results_all if
            'beep_press_accuracy' in r and 'beep_press_rt' in r and
            r['beep_press_accuracy'] == 'correct' and r['beep_press_rt'] != 'NA')

        # Calculate the average reaction time for correct responses for single presentation trials if there are any
        beep_press_trial_rt_correct = sum(
            float(r['beep_press_rt']) for r in beep_press_results_all if 'beep_press_accuracy' in r and
            'beep_press_rt' in r and r['beep_press_accuracy'] == 'correct' and
            r['beep_press_rt'] != 'NA') / beep_press_correct_and_not_na if beep_press_correct_and_not_na > 0 else None

        # Calculate the number of incorrect responses for single presentation trials where the reaction time is not NA
        beep_press_incorrect_and_not_na = sum(
            1 for r in beep_press_results_all if
            'beep_press_accuracy' in r and 'beep_press_rt' in r and
            r['beep_press_accuracy'] == 'incorrect' and r['beep_press_rt'] != 'NA')

        # Calculate the average reaction time for incorrect responses for single presentation trials if there are any
        beep_press_trial_rt_incorrect = sum(
            float(r['beep_press_rt']) for r in beep_press_results_all if
            'beep_press_accuracy' in r and 'beep_press_rt' in r and
            r['beep_press_accuracy'] == 'incorrect' and
            r['beep_press_rt'] != 'NA') / beep_press_incorrect_and_not_na if beep_press_incorrect_and_not_na > 0 else None

        # Prepare the result dictionary
        results.append({
            'task': task,
            'main_trial': str(x + 1),
            'phase': 'practice' if task_name.startswith('practice') else 'test',
            'stimulus_id': stimuli.loc[x]['ID'],
            'stimulus': stimuli.loc[x]['item'],
            'stimulus_rec': responseRecordName,
            'rand_nr': str(randNr[x]),
            'dot_direction': 'NA',
            'dot_1st_frame': 'NA',
            'dot_last_frame': 'NA',
            'dot_response_key': 'NA',
            'dot_response_accuracy': 'NA',
            'number_selection': str(number_selection),
            'index_rand_nr':correct_index,
            'index_number_response':str(arrowKey_number[0]),
            'number_response_accuracy':numbers_accuracy,
            'beep_sequence':str(beep_sequence),
            'beep_press_trials':beep_press_trials,
            'beep_press_deviant_trials': beep_press_trials_deviant,
            'beep_press_normal_trials': beep_press_trials_normal,
            'beep_press_rt_correct':beep_press_trial_rt_correct,
            'beep_press_rt_incorrect':beep_press_trial_rt_incorrect,
            'beep_press_accuracy':beep_press_trial_accuracy,
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
    if task_name == 'practice_dualTask_beep_count_dots':
        random.seed(424)  # Set a random seed for reproducibility - here to get same list of nrs for practice
    elif task_name == 'test_dualTask_beep_count_dots':
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
            if frame % 50 == 0 and frame >= 49:

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
                        'main_trial': x+1,
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
                        'main_trial': x+1,
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
                                       'dual_task_' + participant_info['subject'] + '_' + task_name + '_' + str(
                                           stimuli.loc[x]['ID']) + '.wav'), fs, responseRecord)

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
            feedback.setColor('green')
            feedback.draw()
        else:
            dot_Accuracy = 'incorrect'
            feedback.setText('Inkorrekt!')
            feedback.setColor('red')
            feedback.draw()
        window.flip()

        core.wait(2)

        number_selection, correct_index = select_and_replace_number(task_name, beep_sequence.count('deviant'))

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
            feedback.setColor('green')
            feedback.draw()
        else:
            numbers_accuracy = 'incorrect'
            feedback.setText('Inkorrekt!')
            feedback.setColor('red')
            feedback.draw()
        window.flip()

        core.wait(2)

        # Define a file name for the response record
        responseRecordName = 'dual_task_' + participant_info['subject'] + '_' + task_name + '_' + str(
            stimuli.loc[x]['ID']) + '.wav'

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
            'main_trial': str(x + 1),
            'phase': 'practice' if task_name.startswith('practice') else 'test',
            'stimulus_id': stimuli.loc[x]['ID'],
            'stimulus': stimuli.loc[x]['item'],
            'stimulus_rec': responseRecordName,
            'rand_nr': 'NA',
            'dot_direction': movement,
            'dot_1st_frame': rand1stFrame,
            'dot_last_frame': randLastFrame,
            'dot_response_key': arrowKey,
            'dot_response_accuracy': dot_Accuracy,
            'number_selection': 'NA',
            'index_rand_nr':'NA',
            'index_number_response':'NA',
            'number_response_accuracy':'NA',
            'beep_sequence':str(beep_sequence),
            'beep_press_trials':'NA',
            'beep_press_deviant_trials': 'NA',
            'beep_press_normal_trials': 'NA',
            'beep_press_rt_correct':'NA',
            'beep_press_rt_incorrect':'NA',
            'beep_press_accuracy':'NA',
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
def execute_task(window, task_name, participant_info, stimuli, werKommt, fixation, randNumber, item, prompt,
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
    randNumber : object
        Random number generator object.
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
    These are: 'practice_dualTask_number_dots', 'test_dualTask_number_dots', 'practice_dualTask_number_beep_press',
    'test_dualTask_number_beep_press', 'practice_dualTask_beep_count_dots', 'test_dualTask_beep_count_dots', and
    'practice_singleTask'. For each task, an end-of-practice instruction is displayed. Directories for storing the
    results and recordings are created if they do not already exist. The results of the task are saved to a
    results file, and a base filename is generated for the task.
    """

    # Initialize an empty list to hold the results
    results = []
    # Import the end-of-practice instructions
    from instructions import instructPracticeSingleTaskEnd,  instructPracticeDualTask_number_dots_End, instructPracticeDualTask_number_beep_press_End, instructPracticeDualTask_beep_count_dots_End

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
        if task_name == 'practice_dualTask_number_dots':
            execute_dualTask_number_dots(window, results, base_filename, subj_path_rec, stimuli, task_name, werKommt,
                                         fixation, randNumber, item, prompt, feedback, fs, rec_seconds, movementDirections,
                                         responseList, dots, arrows, arrows_small, number_prompts, participant_info)
            display_text_and_wait(instructPracticeDualTask_number_dots_End, window)
        if task_name == 'test_dualTask_number_dots':
            execute_dualTask_number_dots(window, results, base_filename, subj_path_rec, stimuli, task_name, werKommt,
                                         fixation, randNumber, item, prompt, feedback, fs, rec_seconds, movementDirections,
                                         responseList, dots, arrows, arrows_small, number_prompts, participant_info)

        if task_name == 'practice_dualTask_number_beep_press':
            execute_dualTask_number_beep_press(window, results, base_filename, subj_path_rec, stimuli, task_name,
                                               werKommt, fixation, randNumber, item, prompt, feedback, fs, rec_seconds,
                                               responseList, arrows_small, number_prompts, participant_info)
            display_text_and_wait(instructPracticeDualTask_number_beep_press_End, window)
        if task_name == 'test_dualTask_number_beep_press':
            execute_dualTask_number_beep_press(window, results, base_filename, subj_path_rec, stimuli, task_name,
                                               werKommt, fixation, randNumber, item, prompt, feedback, fs, rec_seconds,
                                               responseList, arrows_small, number_prompts, participant_info)

        if task_name == 'practice_dualTask_beep_count_dots':
            execute_dualTask_beep_count_dots(window, results, base_filename, subj_path_rec, stimuli, task_name, werKommt,
                                             fixation, item, prompt, feedback, fs, rec_seconds, movementDirections,
                                             responseList, dots, arrows, arrows_small, number_prompts, participant_info)
            display_text_and_wait(instructPracticeDualTask_beep_count_dots_End, window)
        if task_name == 'test_dualTask_beep_count_dots':
            execute_dualTask_beep_count_dots(window, results, base_filename, subj_path_rec, stimuli, task_name, werKommt,
                                             fixation, item, prompt, feedback, fs, rec_seconds, movementDirections,
                                             responseList, dots, arrows, arrows_small, number_prompts, participant_info)
    else:
        execute_singleTask(window, results, subj_path_rec, stimuli, task_name, werKommt, fixation, item, rec_seconds,
                           fs, participant_info, base_filename)
        if task_name == 'practice_singleTask':
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


def select_and_replace_number(task_name, replacement_number):
    """
    Selects a set of unique numbers within a given range, and replaces one of these numbers
    with a specified replacement number. The range of numbers and the position of the replacement
    number are determined randomly.

    Parameters:
    task_name : str
        The name of the task, which determines the range of numbers to be selected. If the task
        is 'practice_dualTask_beep_count_dots' or 'test_dualTask_beep_count_dots', the range is from
        3 to 23, otherwise the range is from 100 to 999.
    replacement_number : int
        The number that will replace one of the randomly selected numbers in the final list.

    Returns:
    numbers : list of int
        List of four numbers where one of the numbers is the replacement_number.
    replace_index : int
        The index at which the replacement_number is placed in the list.

    Notes:
    This function is used to create a list of four numbers that includes a certain number
    (the replacement number). The other three numbers are selected randomly from a range
    that depends on the task_name. The replacement number's position in the list is also chosen randomly.
    """

    if task_name == 'practice_dualTask_beep_count_dots' or task_name == 'test_dualTask_beep_count_dots':
        range_start = 3
        range_end = 23
    else:
        range_start = 100
        range_end = 999

    # Create a list of all numbers in the range except the replacement number
    range_without_replacement = [i for i in range(range_start, range_end) if i != replacement_number]

    # Randomly select 3 numbers from this list
    numbers = random.sample(range_without_replacement, 3)

    # Randomly choose an index to insert the replacement number
    replace_index = random.randint(0, 3)

    # Insert the replacement number at this index
    numbers.insert(replace_index, replacement_number)

    return numbers, replace_index
