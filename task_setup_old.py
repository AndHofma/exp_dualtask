"""
The single task procedure (execute_singleTask) involves the presentation of visual stimuli and the recording
of the participant's response (reading out loud).
The dual task procedure (execute_dualTask) involves the presentation of visual stimuli, along with math problems
and a moving-dots task, and records the participant's response (reading out loud) and
their response to the math problem and moving-dots task.
"""

# Import necessary libraries
from psychopy import core, event, visual  # import some libraries from PsychoPy
from psychopy.hardware import keyboard
import time
import datetime
import sounddevice as sd
from scipy.io.wavfile import write
import random
from configuration_old import append_result_to_csv
import os


# single task procedure
def execute_singleTask(window, results, subj_path_rec, stimuli, task_name, werKommt, fixation, item, pic, rec_seconds, fs, pics_path, participant_info, base_filename):
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
        pic: The pictogram stimulus.
        rec_seconds: The recording duration in seconds.
        fs: The sample rate for the recording.
        pics_path: The path to the pictograms.
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

        pictogram = stimuli.loc[x]['pic']
        pic.image = pics_path + pictogram + '_small_borderless.png'
        pic.name = str(pic.image)  # Naming the ImageStim to find it in the log-file

        # Start recording the participant's verbal response
        responseRecord = sd.rec(int(rec_seconds * fs), samplerate=fs, channels=1)

        # Present item and pic for 300 frames
        for frame in range(300):
            item.draw()  # Draw item
            pic.draw()  # Draw pic
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
            'rand_nr_calc': 'NA',
            'rand_operation': 'NA',
            'answer_calc': 'NA',
            'answer_input': 'NA',
            'answer_input_accuracy': 'NA',
            '2back_matching_trials_single': 'NA',
            '2back_matching_trials_dual': 'NA',
            '2back_trial_accuracy_single': 'NA',
            '2back_trial_accuracy_dual': 'NA',
            '2back_trial_rt_correct_single': 'NA',
            '2back_trial_rt_correct_dual': 'NA',
            '2back_shape_order': 'NA',
            'flanker_nr_trials_single': 'NA',
            'flanker_nr_trials_dual': 'NA',
            'flanker_trial_accuracy_single': 'NA',
            'flanker_trial_accuracy_dual': 'NA',
            'flanker_trial_rt_correct_single': 'NA',
            'flanker_trial_rt_correct_dual': 'NA',
            'flanker_trial_rt_incorrect_single': 'NA',
            'flanker_trial_rt_incorrect_dual': 'NA',
            'flanker_shape_nr_trials_single': 'NA',
            'flanker_shape_nr_trials_dual': 'NA',
            'flanker_shape_trial_accuracy_single': 'NA',
            'flanker_shape_trial_accuracy_dual': 'NA',
            'flanker_shape_trial_rt_correct_single': 'NA',
            'flanker_shape_trial_rt_correct_dual': 'NA',
            'flanker_shape_trial_rt_incorrect_single': 'NA',
            'flanker_shape_trial_rt_incorrect_dual': 'NA',
            'start_time': start_time_str,
            'end_time': end_time_str,
            'duration': duration_str,
        })
        # Append the result to the CSV file
        append_result_to_csv(results[-1], base_filename, participant_info)


# dual task procedure
def execute_dualTask_dotMotion_calc(window, results, base_filename, subj_path_rec, stimuli, task_name, werKommt, fixation, randNumber, item,
                                    pic, prompt, feedback, input_text, keyList, fs, rec_seconds, movementDirections, responseList,
                                    dots, operations, arrows, pics_path, participant_info):
    """
    Executes a dual task procedure in a psychophysical experiment.

    This function displays stimuli alongside math problems and arrow tasks.
    It records the participant's vocal response, as well as their responses to the math and arrow tasks.

    Args:
        window : A window object where the experiment is displayed.
        results : A list to store the results of the experiment.
        base_filename : The name of the file where results are to be stored.
        subj_path_rec : Path to save the audio recordings of the subject's responses.
        stimuli : A DataFrame containing the stimuli for the experiment.
        task_name : Name of the task, used to manage the experiment flow.
        werKommt : A psychopy.visual.TextStim object. This is a stimulus in the experiment.
        fixation : A psychopy.visual.ShapeStim object. This is a fixation point in the experiment.
        randNumber : A psychopy.visual.TextStim object. Displays a random number for the math task.
        item : A psychopy.visual.TextStim object. Represents one item from the stimuli.
        pic : A psychopy.visual.ImageStim object. Displays the picture stimulus.
        prompt : A psychopy.visual.TextStim object. Provides instructions to the participant.
        feedback : A psychopy.visual.TextStim object. Provides feedback to the participant on their performance.
        input_text : A psychopy.visual.TextBox object. Used to input the participant's response for the math task.
        keyList : A list of keys the participant can press to provide their answer to the math task.
        fs : Sampling frequency for audio recording.
        rec_seconds : Length of the audio recording in seconds.
        movementDirections : List of possible movement directions for the dot task.
        responseList : List of keys the participant can press to provide their answer to the arrow task.
        dots : A psychopy.visual.DotStim object. Used in the dot task.
        operations : List of math operations to be used in the math task.
        arrows : List of psychopy.visual.ShapeStim objects. Represents arrows pointing in different directions.
        pics_path : Path to the directory containing the picture stimuli.
        participant_info : A dictionary containing information about the participant.

    Returns:
        None. The function modifies the 'results' list and writes to a file in place.
    """

    # List of random numbers, same order for every participant
    if task_name == 'practice_dualTask':
        random.seed(42)  # Set a random seed for reproducibility - here to get same list of nrs for practice

    else:
        random.seed(666)  # Set a random seed for reproducibility - here to get same list of nrs for test

    randNr = [random.randint(120, 970) for _ in range(len(stimuli))]
    randNrForCalc = [random.randint(0, 20) for _ in range(len(stimuli))]

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

        operation = random.choice(operations)
        answer = operation(randNr[x], randNrForCalc[x])

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

        pictogram = stimuli.loc[x]['pic']
        pic.image = pics_path + pictogram + '_small_borderless.png'
        # naming the ImageStim to find it in the log-file
        pic.name = str(pic.image)

        # start recording the participant response - reading out loud the stimulus
        responseRecord = sd.rec(int(rec_seconds * fs), samplerate=fs, channels=1)

        # draw item and pic for 300 frames - and the moving dots btw 40-70 up to 190-220 frames
        for frame in range(300):
            item.draw()
            pic.draw()
            if rand1stFrame <= frame < randLastFrame:  # Present dots for subset of frames
                dots.dir = movement
                dots.draw()
            window.flip()
        sd.stop()  # stop the recording

        # safe stimulus recording as wav file
        write(os.path.join(subj_path_rec, 'dual_task_' + participant_info['subject'] + '_' + task_name + '_' + str(stimuli.loc[x]['ID']) + '.wav'), fs, responseRecord)
        # naming the recording wav file to find it in the log-file
        responseRecordName = 'dual_task_' + participant_info['subject'] + '_' + task_name + '_' + str(stimuli.loc[x]['ID']) + '.wav'

        # show first response screen
        prompt.setText('Drücken Sie den Richtungs-Pfeil auf der Tastatur,\n in die sich die Punkte bewegt haben.')
        prompt.pos = (0, 0.3)
        prompt.size = 0.15
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

        while True:
            prompt.setText('Rechnen Sie:')
            prompt.size = 0.2
            prompt.pos = (0, 0.4)
            prompt.setText('Geben Sie eine dreistellige Zahl ein und bestätigen Sie mit Enter.')
            prompt.size = 0.05
            prompt.pos = (0, -0.5)
            prompt.draw()

            if operation == operations[0]:
                operation_Name = 'addition'
                prompt.setText('Zahl +' + str(randNrForCalc[x]))
            elif operation == operations[1]:
                operation_Name = 'subtraction'
                prompt.setText('Zahl -' + str(randNrForCalc[x]))
            prompt.size = 0.2
            prompt.pos = (0, 0)
            prompt.draw()

            input_text.size = 0.2
            input_text.setAutoDraw(True)
            input_text.draw()
            window.flip()

            # wait for keyboard input
            calcInputKey = event.waitKeys(keyList=keyList)[0]
            # remove the num_ string to be able to use key.isdigit() below - otherwise key.isdigit()=False
            calcInputKey = calcInputKey.replace('num_', '')

            # if the key is a number/digit, add it to the input field
            if calcInputKey.isdigit() and len(input_text.text) < 3:
                input_text.text += calcInputKey
                input_text.setAutoDraw(True)  # update the stimulus with the new text

            # if the key is backspace, delete the last character of the input field
            elif calcInputKey == 'backspace':
                input_text.text = input_text.text[:-1]
                input_text.setAutoDraw(True)  # update the stimulus with the new text

            # if the key is return, compare the input to the correct answer
            elif calcInputKey == 'return':
                if len(input_text.text) == 3:
                    partic_Input = input_text.text
                    if input_text.text == str(answer):
                        calc_Accuracy = 'correct'
                        feedback.setText("Korrekt!")
                        feedback.setColor('green')
                    else:
                        calc_Accuracy = 'incorrect'
                        feedback.setText("Inkorrekt.")
                        feedback.setColor('red')
                    feedback.size = 0.3
                    feedback.draw()
                    # reset the input field and the feedback
                    input_text.text = ""
                    feedback.setAutoDraw(False)
                    window.flip()
                    core.wait(2)
                    break
                else:
                    error_text = "Bitte geben Sie eine dreistellige Zahl ein."
                    error = visual.TextStim(window, text=error_text, color='black', pos=(0, -0.5))
                    error.draw()
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
            'dot_response_accuracy': dot_Accuracy,
            'rand_nr_calc': str(randNrForCalc[x]),
            'rand_operation': operation_Name,
            'answer_calc': answer,
            'answer_input': partic_Input,
            'answer_input_accuracy': calc_Accuracy,
            '2back_matching_trials_single': 'NA',
            '2back_matching_trials_dual': 'NA',
            '2back_trial_accuracy_single': 'NA',
            '2back_trial_accuracy_dual': 'NA',
            '2back_trial_rt_correct_single': 'NA',
            '2back_trial_rt_correct_dual': 'NA',
            '2back_shape_order': 'NA',
            'flanker_nr_trials_single': 'NA',
            'flanker_nr_trials_dual': 'NA',
            'flanker_trial_accuracy_single': 'NA',
            'flanker_trial_accuracy_dual': 'NA',
            'flanker_trial_rt_correct_single': 'NA',
            'flanker_trial_rt_correct_dual': 'NA',
            'flanker_trial_rt_incorrect_single': 'NA',
            'flanker_trial_rt_incorrect_dual': 'NA',
            'flanker_shape_nr_trials_single': 'NA',
            'flanker_shape_nr_trials_dual': 'NA',
            'flanker_shape_trial_accuracy_single': 'NA',
            'flanker_shape_trial_accuracy_dual': 'NA',
            'flanker_shape_trial_rt_correct_single': 'NA',
            'flanker_shape_trial_rt_correct_dual': 'NA',
            'flanker_shape_trial_rt_incorrect_single': 'NA',
            'flanker_shape_trial_rt_incorrect_dual': 'NA',
            'start_time': start_time_str,
            'end_time': end_time_str,
            'duration': duration_str,
        })
        # Append the result to the CSV file
        append_result_to_csv(results[-1], base_filename, participant_info)


def execute_dualTask_2back(window, results, base_filename, subj_path_rec, stimuli, task_name, werKommt, fixation, item,
                           pic, feedback, fs, rec_seconds, pics_path, participant_info, shapes_list, shape):

    """
    This function executes a dual task 2-back experiment, which consists of presenting stimuli and recording the participant's
    responses.

    Parameters:
    window (psychopy.visual.window.Window): The window in which stimuli are presented.
    results (list): A list where participant's response data is stored.
    base_filename (str): Base filename to use when saving response data.
    subj_path_rec (str): Path to the directory where participant's response recordings are saved.
    stimuli (pandas.DataFrame): DataFrame that contains the stimuli to present.
    task_name (str): The name of the task, used for saving response data.
    werKommt (psychopy.visual.text.TextStim): TextStim for presenting stimulus names.
    fixation (psychopy.visual.shape.ShapeStim): ShapeStim for presenting fixation cross.
    item (psychopy.visual.text.TextStim): TextStim for presenting stimulus items.
    pic (psychopy.visual.image.ImageStim): ImageStim for presenting stimulus images.
    feedback (psychopy.visual.text.TextStim): TextStim for presenting feedback to the participant.
    fs (int): Sampling rate to use when recording participant's responses.
    rec_seconds (int): Duration of participant's response recording in seconds.
    pics_path (str): Path to the directory where stimulus images are stored.
    participant_info (dict): Information about the participant.
    shapes_list (list): List of shapes to use in the 2-back task.
    shape (psychopy.visual.image.ImageStim): ImageStim for presenting shapes in the 2-back task.

    Returns:
    None: The function doesn't return anything, it just modifies the `results` list in-place.
    """

    # Initialize the keyboard
    keyBoard = keyboard.Keyboard()
    keyBoard.clock.reset()

    # Initialize start time and start_time_str
    start_time = time.time()
    start_time_str = datetime.datetime.fromtimestamp(start_time).strftime('%H:%M:%S')

    # Iterate over stimuli
    for x in range(len(stimuli)):
        task = task_name
        nback_trial_counter = 0
        nback_stimulus_history = ["", ""]

        n_frames_per_shape = 100  # 6 different shapes within 1000 frames for 100 frames
        n_shapes = 1200 // n_frames_per_shape

        # Initialize a list for the shapes for the 2-back task.
        # This list will contain the sequence of shapes to be presented to the participant.
        shape_stimuli = []

        # Initialize a variable to keep track of the shape that was presented in the previous iteration of the loop.
        # This will be used to prevent the same shape from being presented consecutively.
        previous_shape = None

        # Loop over the range of shapes minus one to leave space for a repeated shape.
        # This loop generates the random sequence of shapes to be presented to the participant.
        for _ in range(n_shapes - 1):
            # Choose a random shape from the list of shapes
            current_shape = random.choice(shapes_list)

            # If the chosen shape is the same as the one that was presented in the previous iteration,
            # keep choosing a new random shape until it is different.
            while current_shape == previous_shape:
                current_shape = random.choice(shapes_list)

            # Add the chosen shape to the list of stimuli
            shape_stimuli.append(current_shape)

            # Set the previous shape to the current shape for the next iteration of the loop
            previous_shape = current_shape

        # Choose a random shape from the list of shapes excluding the last one to repeat in the stimuli.
        # This ensures at least one shape is repeated in the sequence, which gives the participant an opportunity for a correct response.
        shape_to_repeat = random.choice(shape_stimuli[:-1])

        # Determine the position to insert the repeated shape in the stimuli sequence.
        # The repeated shape is placed 2 positions after its first occurrence to meet the requirements of the 2-back task.
        repetition_index = shape_stimuli.index(shape_to_repeat) + 2
        shape_stimuli.insert(repetition_index, shape_to_repeat)

        # Generate a string representation of the sequence of shapes.
        # This is used for recording the sequence that was presented to the participant.
        shape_order = ", ".join([os.path.basename(shape) for shape in shape_stimuli])

        # Create a list of correct responses for the 2-back task.
        # For each shape, check if it's the same as the shape 2 positions before it in the sequence.
        # This list will be used to evaluate the participant's responses.
        correct_responses = [False, False] + [shape_stimuli[i] == shape_stimuli[i - 2] for i in range(2, len(shape_stimuli))]

        # draw item and pic for 300 frames
        start_offset = random.randint(300, 601)  # random number between 300 and 600
        end_offset = start_offset + 300

        # naming the TextStim to find it in the log-file
        werKommt.name = 'werKommt'
        werKommt.draw()
        window.flip()
        core.wait(1.0)
        window.flip()

        # naming the visualStim to find it in the log-file
        fixation.name = 'fixation'
        fixation.draw()
        window.flip()
        core.wait(1.0)
        window.flip()

        stimulus = stimuli.loc[x]['item']
        item.setText(stimulus)
        # naming the TextStim to find it in the log-file
        item.name = 'item_' + str(stimuli.loc[x]['ID'])

        pictogram = stimuli.loc[x]['pic']
        pic.image = pics_path + pictogram + '_small_borderless.png'
        # naming the ImageStim to find it in the log-file
        pic.name = str(pic.image)

        # start recording the participant response - reading out loud the stimulus
        responseRecord = None
        num_correct = 0

        # The loop runs 1200 times, which equates to 1200 frames assuming a frame rate of 60 Hz for 20 seconds
        for frame in range(1200):
            # Display item and picture for 300 frames
            if start_offset <= frame < end_offset:  # Check if current frame is within the display range
                item.draw()  # Draw item
                pic.draw()  # Draw picture

                if frame == start_offset:
                    # If current frame is the start frame, start recording the participant's response
                    responseRecord = sd.rec(int(rec_seconds * fs), samplerate=fs, channels=1)

                if frame == end_offset - 1:
                    # If current frame is the end frame, stop recording the participant's response
                    sd.stop()
                    # Save the recorded response as a .wav file
                    write(os.path.join(subj_path_rec,
                                       'dual_task_' + participant_info['subject'] + '_' + task_name + '_' + str(
                                           stimuli.loc[x]['ID']) + '.wav'), fs, responseRecord)

            if frame % n_frames_per_shape == 0 and frame != 0:  # Change shape every n_frames_per_shape frames, except for the first one
                # Record participant responses
                keys = keyBoard.getKeys(['space'], waitRelease=True)  # Check for 'space' key press

                # If a key was pressed, process the response
                if keys and results:
                    response, rt = keys[0], keys[0].rt
                    response_type = 'match' if stimulus_type == 'matching' else (
                        'false_alarm' if stimulus_type == 'non_matching' else 'miss')
                    reaction_time = rt
                    accuracy = 'correct' if stimulus_type == 'matching' and response_type == 'match' else 'incorrect'

                    # Update number of correct responses
                    if accuracy == 'correct' and stimulus_type == 'matching':
                        num_correct += 1

                    # Update response type, reaction time, and accuracy of the latest 2-back result
                    results[-1]['2back_response_type'] = response_type
                    results[-1]['2back_rt'] = reaction_time
                    results[-1]['2back_accuracy'] = accuracy

                    # Clear events immediately after processing a key press
                    keyBoard.clearEvents()
                else:
                    # If no response was made, process accordingly
                    response_type = 'miss' if stimulus_type == 'matching' else 'none'
                    reaction_time = 'NA'
                    accuracy = 'correct' if stimulus_type == 'non_matching' else 'incorrect'

                    # Update response type, reaction time, and accuracy of the latest 2-back result
                    results[-1]['2back_response_type'] = response_type
                    results[-1]['2back_rt'] = reaction_time
                    results[-1]['2back_accuracy'] = accuracy

                # Record end time and calculate duration of the task
                end_time = time.time()
                end_time_str = datetime.datetime.fromtimestamp(end_time).strftime('%H:%M:%S')
                duration = end_time - start_time
                hours, remainder = divmod(duration, 3600)
                minutes, seconds = divmod(remainder, 60)
                duration_str = '{:02d}:{:02d}:{:02d}'.format(int(hours), int(minutes), int(seconds))

                # Update end time and duration of the latest 2-back result
                results[-1]['end_time'] = end_time_str
                results[-1]['duration'] = duration_str

                # Write the latest 2-back result to the CSV file
                append_result_to_csv(results[-1], base_filename, participant_info, type='2back')

                # Clear any subsequent key presses during feedback
                keyBoard.clearEvents()

            # Update shape image and information about the 2-back stimulus for every n_frames_per_shape frames
            if frame % n_frames_per_shape == 0:
                keyBoard.clearEvents()  # Clear events immediately after processing a key press
                shape.image = shape_stimuli[frame // n_frames_per_shape]  # Change shape image
                # Set stimulus type: 'matching' if the response is correct, else 'non_matching'
                stimulus_type = 'matching' if correct_responses[frame // n_frames_per_shape] else 'non_matching'
                keyBoard.clock.reset()  # Reset the keyboard clock
                # Update 2-back stimulus history and counter
                nback_stimulus_history.append(shape_stimuli[frame // n_frames_per_shape])
                nback_trial_counter += 1

                # Append new result with current information about the 2-back trial
                results.append({
                    'task': task_name,
                    'phase': 'practice' if task_name.startswith('practice') else 'test',
                    'main_trial': str(x + 1),
                    '2back_trial': nback_trial_counter,
                    '2back_trial_type': stimulus_type,
                    '2back_accuracy': 'NA',
                    '2back_response_type': 'NA',
                    '2back_rt': 'NA',
                    '2back_current_shape': os.path.basename(shape_stimuli[frame // n_frames_per_shape]),
                    '2back_nback1_shape': os.path.basename(nback_stimulus_history[-2]),
                    '2back_nback2_shape': os.path.basename(nback_stimulus_history[-3]),
                    'presentation': 'dual' if start_offset <= frame < end_offset else 'single',
                    'start_time': start_time_str,
                    'end_time': 'NA',
                    'duration': 'NA',
                })

            shape.draw()  # Draw the shape
            window.flip()  # Update the window to display the drawn contents

        # Rest of the code after the frame loop is mostly similar to what was inside the loop,
        # but it's here to ensure we process and record the last response if any, and give final feedback.
        # Record responses
        keys = keyBoard.getKeys(['space'], waitRelease=True)

        if keys and results:
            response, rt = keys[0], keys[0].rt
            response_type = 'match' if stimulus_type == 'matching' else (
                'false_alarm' if stimulus_type == 'non_matching' else 'miss')
            reaction_time = rt
            accuracy = 'correct' if stimulus_type == 'matching' and response_type == 'match' else 'incorrect'

            if accuracy == 'correct' and stimulus_type == 'matching':
                num_correct += 1

            results[-1]['2back_response_type'] = response_type
            results[-1]['2back_rt'] = reaction_time
            results[-1]['2back_accuracy'] = accuracy
            keyBoard.clearEvents()  # Clear events immediately after processing a key press
        else:
            # No response was made
            response_type = 'miss' if stimulus_type == 'matching' else 'none'
            reaction_time = 'NA'
            accuracy = 'correct' if stimulus_type == 'non_matching' else 'incorrect'

            results[-1]['2back_response_type'] = response_type
            results[-1]['2back_rt'] = reaction_time
            results[-1]['2back_accuracy'] = accuracy

        # Record end time and duration
        end_time = time.time()
        end_time_str = datetime.datetime.fromtimestamp(end_time).strftime('%H:%M:%S')
        duration = end_time - start_time
        hours, remainder = divmod(duration, 3600)
        minutes, seconds = divmod(remainder, 60)
        duration_str = '{:02d}:{:02d}:{:02d}'.format(int(hours), int(minutes), int(seconds))

        results[-1]['end_time'] = end_time_str
        results[-1]['duration'] = duration_str

        append_result_to_csv(results[-1], base_filename, participant_info, type='2back')
        keyBoard.clearEvents()  # Clear keyboard events here too, so any subsequent key presses during feedback are ignored

        # Calculate num_matches
        num_matches = sum(correct_responses[2:])

        # naming the recording wav file to find it in the log-file
        responseRecordName = 'dual_task_' + participant_info['subject'] + '_' + task_name + '_' + str(
            stimuli.loc[x]['ID']) + '.wav'

        # Show first response screen: Display feedback to participants
        feedback.setText(
            'Sie haben ' + str(num_correct) + ' von ' + str(num_matches) + ' möglichen Matches richtig erkannt!')

        # Set feedback text color to black, position to the center of the screen, and size to 0.15
        feedback.setColor('black')
        feedback.pos = (0, 0)
        feedback.size = 0.15

        # Draw the feedback text and flip the window
        feedback.draw()
        window.flip()

        # Pause for 3 seconds to let participants see the feedback
        core.wait(3)

        # Record the end time of the task
        end_time = time.time()
        # Convert the end time into hours, minutes, and seconds
        end_time_str = datetime.datetime.fromtimestamp(end_time).strftime('%H:%M:%S')

        # Calculate the duration of the task
        duration = end_time - start_time
        hours, remainder = divmod(duration, 3600)
        minutes, seconds = divmod(remainder, 60)
        duration_str = '{:02d}:{:02d}:{:02d}'.format(int(hours), int(minutes), int(seconds))

        # Create a new list for the last 12 results
        last_twelve_results = results[-12:]

        # Filter the last 12 results for single and dual presentations respectively, only keeping those that are 'matching'
        results_single = [r for r in last_twelve_results if
                          'presentation' in r and '2back_trial_type' in r and r['presentation'] == 'single' and r[
                              '2back_trial_type'] == 'matching']
        results_dual = [r for r in last_twelve_results if
                        'presentation' in r and '2back_trial_type' in r and r['presentation'] == 'dual' and r[
                            '2back_trial_type'] == 'matching']

        # Calculate the total number of matching trials for single and dual presentations
        matching_trials_single = len(results_single)
        matching_trials_dual = len(results_dual)

        # Calculate accuracy of the trials for single and dual presentations by taking the ratio of correct responses to total matching trials
        trial_accuracy_single = sum(r['2back_accuracy'] == 'correct' for r in
                                    results_single) / matching_trials_single if matching_trials_single else None
        trial_accuracy_dual = sum(r['2back_accuracy'] == 'correct' for r in
                                  results_dual) / matching_trials_dual if matching_trials_dual else None

        # Calculate the reaction time (RT) for correct responses for single and dual presentations
        # This is done by summing the RTs for correct responses, and dividing by the number of correct responses
        # Exclude trials where the RT is 'NA'
        correct_and_not_na_single = sum(1 for r in results_single if '2back_accuracy' in r and '2back_rt' in r and r[
            '2back_accuracy'] == 'correct' and r['2back_rt'] != 'NA')
        trial_rt_correct_single = sum(float(r['2back_rt']) for r in results_single if
                                      '2back_accuracy' in r and '2back_rt' in r and r['2back_accuracy'] == 'correct' and
                                      r[
                                          '2back_rt'] != 'NA') / correct_and_not_na_single if correct_and_not_na_single > 0 else None
        correct_and_not_na_dual = sum(1 for r in results_dual if
                                      '2back_accuracy' in r and '2back_rt' in r and r['2back_accuracy'] == 'correct' and
                                      r['2back_rt'] != 'NA')
        trial_rt_correct_dual = sum(float(r['2back_rt']) for r in results_dual if
                                    '2back_accuracy' in r and '2back_rt' in r and r['2back_accuracy'] == 'correct' and
                                    r[
                                        '2back_rt'] != 'NA') / correct_and_not_na_dual if correct_and_not_na_dual > 0 else None

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
            'rand_nr_calc': 'NA',
            'rand_operation': 'NA',
            'answer_calc': 'NA',
            'answer_input': 'NA',
            'answer_input_accuracy': 'NA',
            '2back_matching_trials_single': matching_trials_single,
            '2back_matching_trials_dual': matching_trials_dual,
            '2back_trial_accuracy_single': trial_accuracy_single,
            '2back_trial_accuracy_dual': trial_accuracy_dual,
            '2back_trial_rt_correct_single': trial_rt_correct_single,
            '2back_trial_rt_correct_dual': trial_rt_correct_dual,
            '2back_shape_order': shape_order,
            'flanker_nr_trials_single': 'NA',
            'flanker_nr_trials_dual': 'NA',
            'flanker_trial_accuracy_single': 'NA',
            'flanker_trial_accuracy_dual': 'NA',
            'flanker_trial_rt_correct_single': 'NA',
            'flanker_trial_rt_correct_dual': 'NA',
            'flanker_trial_rt_incorrect_single': 'NA',
            'flanker_trial_rt_incorrect_dual': 'NA',
            'flanker_shape_nr_trials_single': 'NA',
            'flanker_shape_nr_trials_dual': 'NA',
            'flanker_shape_trial_accuracy_single': 'NA',
            'flanker_shape_trial_accuracy_dual': 'NA',
            'flanker_shape_trial_rt_correct_single': 'NA',
            'flanker_shape_trial_rt_correct_dual': 'NA',
            'flanker_shape_trial_rt_incorrect_single': 'NA',
            'flanker_shape_trial_rt_incorrect_dual': 'NA',
            'start_time': start_time_str,
            'end_time': end_time_str,
            'duration': duration_str,
        })
        # Append the result to the CSV file
        append_result_to_csv(results[-1], base_filename, participant_info)


def execute_dualTask_flanker(window, results, base_filename, subj_path_rec, stimuli, task_name, werKommt, fixation, item,
                             pic, prompt, feedback, fs, rec_seconds, pics_path, participant_info, flanker_stimuli,
                             flanker_correct, flanker_incorrect, flanker_neutral):
    """
    Executes a dual-task flanker experiment involving a name reading and a flanker task.

    Parameters:
    window : Object representing the window in which the experiment is displayed.
    results : List to store the results.
    base_filename : The base name of the result file.
    subj_path_rec : Path to the directory where subject recordings are stored.
    stimuli : DataFrame containing the stimuli for the name reading task.
    task_name : Name of the current task.
    werKommt : Object representing the fixation cross.
    fixation : Object representing the fixation cross.
    item : Text object for displaying the name reading task stimuli.
    pic : Image object for displaying the image of the name reading task stimuli.
    prompt : Text object for displaying the flanker task stimuli.
    feedback : Text object for displaying feedback after the flanker task.
    fs : Sample rate for the recordings.
    rec_seconds : Number of seconds to record.
    pics_path : Path to the directory where stimulus pictures are stored.
    participant_info : Information about the participant.
    flanker_stimuli : List of tuples, where each tuple contains the flanker stimulus, correct response, and condition.
    flanker_correct : Image object for the correct flanker feedback.
    flanker_incorrect : Image object for the incorrect flanker feedback.
    flanker_neutral : Image object for the neutral flanker feedback.
    """

    # Initialize the keyboard
    keyBoard = keyboard.Keyboard()
    keyBoard.clock.reset()

    start_time = time.time()
    start_time_str = datetime.datetime.fromtimestamp(start_time).strftime('%H:%M:%S')

    for x in range(len(stimuli)):
        # Initialize lists to store correct and incorrect responses, and a counter for the number of flanker trials.
        # Initialize a feedback counter and the starting and ending frame numbers for the name reading task
        task = task_name
        correct_responses = []
        incorrect_responses = []
        flanker_trial_counter = 0
        n_frames_per_stimulus = 100
        num_flanker_trials = 1200 // n_frames_per_stimulus
        # Add feedback frames counter
        feedback_counter = 0
        start_offset = random.randint(300, 601)  # random number between 300 and 600
        end_offset = start_offset + 350
        # Shuffle the flanker stimuli so they're presented in random order
        random.shuffle(flanker_stimuli)

        # Draw the initial question and fixation cross and then the stimulus for the name reading task
        werKommt.name = 'werKommt'
        werKommt.draw()
        window.flip()
        core.wait(1.0)

        fixation.name = 'fixation'
        fixation.draw()
        window.flip()
        core.wait(1.0)

        # Set the text of the item object to the current stimulus and the image of the pic object to the corresponding picture
        stimulus = stimuli.loc[x]['item']
        item.setText(stimulus)
        item.name = 'item_' + str(stimuli.loc[x]['ID'])
        pictogram = stimuli.loc[x]['pic']
        pic.image = pics_path + pictogram + '_small_borderless.png'
        pic.name = str(pic.image)

        responseRecord = None
        flanker_stimulus_shown = False

        for frame in range(1200):
            # The primary task is reading aloud
            if start_offset <= frame < end_offset:  # Present name items for subset of frames
                # Draw the item and picture on each frame within the offset range
                item.draw()
                pic.draw()

                if frame == start_offset:
                    # Start recording the participant's voice at the beginning of the range
                    responseRecord = sd.rec(int(rec_seconds * fs), samplerate=fs, channels=1)

                if frame == end_offset - 1:
                    # Stop recording the participant's voice at the end of the range
                    sd.stop()
                    # Save the recording as a wav file
                    write(os.path.join(subj_path_rec,
                                       'dual_task_' + participant_info['subject'] + '_' + task_name + '_' + str(
                                           stimuli.loc[x]['ID']) + '.wav'), fs, responseRecord)

            # The secondary task is the Flanker task
            if frame % n_frames_per_stimulus == 0 and frame // n_frames_per_stimulus < num_flanker_trials:
                # A new flanker trial starts at the beginning of each n_frames_per_stimulus interval
                flanker_stimulus, correct_response, condition = flanker_stimuli[frame // n_frames_per_stimulus]
                # Set the prompt text to the current flanker stimulus
                prompt.setText(flanker_stimulus)
                prompt.size = [0.5, 0.5]
                prompt.pos = [0, -0.4]
                prompt.draw()
                flanker_stimulus_shown = True  # Set a flag to indicate that the flanker stimulus has been shown
                keyBoard.clock.reset()  # Reset the keyboard clock here to prepare for response time recording
                keyPressRegistered = False  # Set a flag to false to track if a key has been pressed during the flanker trial
                flanker_trial_counter += 1  # Increase the counter of flanker trials

                # Append the initial state of the trial to the results list
                results.append({
                    'task': task_name,
                    'phase': 'practice' if task_name.startswith('practice') else 'test',
                    'main_trial': str(x + 1),
                    'flanker_trial': flanker_trial_counter,
                    'flanker_stimulus': flanker_stimulus,
                    'flanker_condition': condition,
                    'flanker_correct': correct_response,
                    'flanker_rt': 'NA',
                    'flanker_response': 'NA',
                    'flanker_response_accuracy': 'NA',
                    'presentation': 'dual' if start_offset <= frame < end_offset else 'single',
                    'start_time': start_time_str,
                    'end_time': 'NA',
                    'duration': 'NA',
                })

            # Continue showing the flanker stimulus until it's time for feedback
            elif 0 < frame % n_frames_per_stimulus < (n_frames_per_stimulus - 30) and flanker_stimulus_shown:
                prompt.draw()

            # Record responses and provide feedback
            elif (
                    n_frames_per_stimulus - 30) <= frame % n_frames_per_stimulus and flanker_stimulus_shown and not keyPressRegistered:
                keys = keyBoard.getKeys(keyList=['a', 'l'], waitRelease=True)
                # If there was a response
                if keys:
                    response, rt = keys[0].name, keys[0].rt  # Retrieve the key pressed and the reaction time
                    # Provide feedback based on the correctness of the response
                    if response == correct_response:  # If the response was correct
                        response_accuracy_flanker = 'correct'
                        correct_responses.append((response, rt))
                        keyPressRegistered = True
                    else:  # If the response was incorrect
                        response_accuracy_flanker = 'incorrect'
                        incorrect_responses.append((response, rt))
                    results[-1]['flanker_rt'] = rt
                    results[-1]['flanker_response'] = response
                else:  # If there was no response
                    response_accuracy_flanker = 'miss'  # Set response accuracy to 'miss'
                    results[-1]['flanker_rt'] = 'none'  # Set reaction time to 'none'
                    results[-1]['flanker_response'] = 'none'  # Set response to 'none'

                keyBoard.clearEvents()  # Clear keyboard events here, so any subsequent key presses during feedback are ignored
                feedback_counter = 30  # Start feedback, which lasts for 30 frames
                flanker_stimulus_shown = False  # Reset the flanker stimulus shown flag for the next trial

            # Show feedback
            if feedback_counter > 0:
                # Draw the appropriate feedback based on the response accuracy
                if response_accuracy_flanker == 'correct':
                    flanker_correct.draw()
                elif response_accuracy_flanker == 'incorrect':
                    flanker_incorrect.draw()
                else:
                    flanker_neutral.draw()
                feedback_counter -= 1  # Decrease the feedback counter

                # Record end time and duration
                end_time = time.time()
                end_time_str = datetime.datetime.fromtimestamp(end_time).strftime('%H:%M:%S')
                duration = end_time - start_time
                hours, remainder = divmod(duration, 3600)
                minutes, seconds = divmod(remainder, 60)
                duration_str = '{:02d}:{:02d}:{:02d}'.format(int(hours), int(minutes), int(seconds))

                # Update the most recent trial in the results with the final response type, reaction time, and accuracy
                results[-1]['flanker_response_accuracy'] = response_accuracy_flanker
                results[-1]['end_time'] = end_time_str
                results[-1]['duration'] = duration_str
                # Append the result to the csv file after the feedback has been completely shown.
                if feedback_counter == 0:
                    append_result_to_csv(results[-1], base_filename, participant_info, type='flanker')
                    keyBoard.clearEvents()  # Clear keyboard events here too, so any subsequent key presses during feedback are ignored

            window.flip()  # Flip the window to show the next frame

        # Count the number of correct and incorrect responses
        num_correct_responses = len(correct_responses)
        num_incorrect_responses = len(incorrect_responses)

        # Create a string for the name of the voice recording file
        responseRecordName = 'dual_task_' + participant_info['subject'] + '_' + task_name + '_' + str(
            stimuli.loc[x]['ID']) + '.wav'

        # Calculate average reaction times for correct and incorrect responses (returns None if there were no such responses)
        average_rt_correct = round(sum(rt for _, rt in correct_responses) / num_correct_responses,
                                   3) if correct_responses else None
        average_rt_incorrect = round(sum(rt for _, rt in incorrect_responses) / num_incorrect_responses,
                                     3) if incorrect_responses else None

        # Set the feedback text with the number of correct and incorrect responses, and their respective average reaction times
        feedback.setText(
            str(num_correct_responses) + ' Mal korrekt (Reaktionszeit: ' + str(average_rt_correct) + ' s.) \n' + str(
                num_incorrect_responses) + ' Mal inkorrekt (Reaktionszeit: ' + str(average_rt_incorrect) + ' s.)')

        # Set color, position, size of the feedback text, draw it, and flip the window to show it
        feedback.setColor('black')
        feedback.pos = (0, 0)
        feedback.size = 0.15
        feedback.draw()
        window.flip()

        # Wait 5 seconds for feedback display
        core.wait(5)

        # Calculate the total duration of the task and convert it into a time string
        end_time = time.time()
        end_time_str = datetime.datetime.fromtimestamp(end_time).strftime('%H:%M:%S')
        duration = end_time - start_time
        hours, remainder = divmod(duration, 3600)
        minutes, seconds = divmod(remainder, 60)
        duration_str = '{:02d}:{:02d}:{:02d}'.format(int(hours), int(minutes), int(seconds))

        # Select the last 12 results from the results list
        last_twelve_results_flanker = results[-12:]

        # Separate the results for the single-task and dual-task conditions
        flanker_results_single = [r for r in last_twelve_results_flanker if
                                  'presentation' in r and r['presentation'] == 'single']
        flanker_results_dual = [r for r in last_twelve_results_flanker if
                                'presentation' in r and r['presentation'] == 'dual']

        # Count the number of trials in the single-task and dual-task conditions
        trials_single = len(flanker_results_single)
        trials_dual = len(flanker_results_dual)

        # Calculate the accuracy of flanker trials in the single-task and dual-task conditions (returns None if no such trials)
        flanker_trial_accuracy_single = sum(r['flanker_response_accuracy'] == 'correct' for r in
                                            flanker_results_single) / trials_single if trials_single else None
        flanker_trial_accuracy_dual = sum(r['flanker_response_accuracy'] == 'correct' for r in
                                          flanker_results_dual) / trials_dual if trials_dual else None

        # Count the number of correct responses that are not N/A in the single-task and dual-task conditions
        flanker_correct_and_not_na_single = sum(1 for r in flanker_results_single if
                                                'flanker_response_accuracy' in r and 'flanker_rt' in r and r[
                                                    'flanker_response_accuracy'] == 'correct' and r[
                                                    'flanker_rt'] != 'NA')
        flanker_correct_and_not_na_dual = sum(1 for r in flanker_results_dual if
                                              'flanker_response_accuracy' in r and 'flanker_rt' in r and r[
                                                  'flanker_response_accuracy'] == 'correct' and r['flanker_rt'] != 'NA')

        # Calculate average reaction times for correct responses that are not N/A in the single-task and dual-task conditions (returns None if no such responses)
        flanker_trial_rt_correct_single = sum(float(r['flanker_rt']) for r in flanker_results_single if
                                              'flanker_response_accuracy' in r and 'flanker_rt' in r and r[
                                                  'flanker_response_accuracy'] == 'correct' and r[
                                                  'flanker_rt'] != 'NA') / flanker_correct_and_not_na_single if flanker_correct_and_not_na_single > 0 else None
        flanker_trial_rt_correct_dual = sum(float(r['flanker_rt']) for r in flanker_results_dual if
                                            'flanker_response_accuracy' in r and 'flanker_rt' in r and r[
                                                'flanker_response_accuracy'] == 'correct' and r[
                                                'flanker_rt'] != 'NA') / flanker_correct_and_not_na_dual if flanker_correct_and_not_na_dual > 0 else None

        # Count the number of incorrect responses that are not N/A in the single-task and dual-task conditions
        flanker_incorrect_and_not_na_single = sum(1 for r in flanker_results_single if
                                                  'flanker_response_accuracy' in r and 'flanker_rt' in r and r[
                                                      'flanker_response_accuracy'] == 'incorrect' and r[
                                                      'flanker_rt'] != 'NA')
        flanker_incorrect_and_not_na_dual = sum(1 for r in flanker_results_dual if
                                                'flanker_response_accuracy' in r and 'flanker_rt' in r and r[
                                                    'flanker_response_accuracy'] == 'incorrect' and r[
                                                    'flanker_rt'] != 'NA')

        # Calculate average reaction times for incorrect responses that are not N/A in the single-task and dual-task conditions (returns None if no such responses)
        flanker_trial_rt_incorrect_single = sum(float(r['flanker_rt']) for r in flanker_results_single if
                                                'flanker_response_accuracy' in r and 'flanker_rt' in r and r[
                                                    'flanker_response_accuracy'] == 'incorrect' and r[
                                                    'flanker_rt'] != 'NA') / flanker_incorrect_and_not_na_single if flanker_incorrect_and_not_na_single > 0 else None
        flanker_trial_rt_incorrect_dual = sum(float(r['flanker_rt']) for r in flanker_results_dual if
                                              'flanker_response_accuracy' in r and 'flanker_rt' in r and r[
                                                  'flanker_response_accuracy'] == 'incorrect' and r[
                                                  'flanker_rt'] != 'NA') / flanker_incorrect_and_not_na_dual if flanker_incorrect_and_not_na_dual > 0 else None

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
            'rand_nr_calc': 'NA',
            'rand_operation': 'NA',
            'answer_calc': 'NA',
            'answer_input': 'NA',
            'answer_input_accuracy': 'NA',
            '2back_matching_trials_single': 'NA',
            '2back_matching_trials_dual': 'NA',
            '2back_trial_accuracy_single': 'NA',
            '2back_trial_accuracy_dual': 'NA',
            '2back_trial_rt_correct_single': 'NA',
            '2back_trial_rt_correct_dual': 'NA',
            '2back_shape_order': 'NA',
            'flanker_nr_trials_single': trials_single,
            'flanker_nr_trials_dual': trials_dual,
            'flanker_trial_accuracy_single': flanker_trial_accuracy_single,
            'flanker_trial_accuracy_dual': flanker_trial_accuracy_dual,
            'flanker_trial_rt_correct_single': flanker_trial_rt_correct_single,
            'flanker_trial_rt_correct_dual': flanker_trial_rt_correct_dual,
            'flanker_trial_rt_incorrect_single': flanker_trial_rt_incorrect_single,
            'flanker_trial_rt_incorrect_dual': flanker_trial_rt_incorrect_dual,
            'flanker_shape_nr_trials_single': 'NA',
            'flanker_shape_nr_trials_dual': 'NA',
            'flanker_shape_trial_accuracy_single': 'NA',
            'flanker_shape_trial_accuracy_dual': 'NA',
            'flanker_shape_trial_rt_correct_single': 'NA',
            'flanker_shape_trial_rt_correct_dual': 'NA',
            'flanker_shape_trial_rt_incorrect_single': 'NA',
            'flanker_shape_trial_rt_incorrect_dual': 'NA',
            'start_time': start_time_str,
            'end_time': end_time_str,
            'duration': duration_str,
        })
        # Append the result to the CSV file
        append_result_to_csv(results[-1], base_filename, participant_info)


def execute_dualTask_flanker_shape(window, results, base_filename, subj_path_rec, stimuli, task_name, werKommt, fixation, item,
                             pic, prompt, feedback, fs, rec_seconds, pics_path, participant_info, flanker_shape_stimuli,
                             flanker_correct, flanker_incorrect, flanker_neutral):

    """
    Executes dual task flanker shape for the experiment.

    Parameters:
    - window: The window object from psychopy where everything is drawn
    - results: A list of dictionaries, where each dictionary is a row of the CSV file
    - base_filename: The base filename of the CSV file
    - subj_path_rec: The path for subject recordings
    - stimuli: The dataframe that contains all stimuli information
    - task_name: The name of the task (e.g., dual_task_flanker_shape)
    - werKommt: The 'who is coming' psychopy object
    - fixation: The fixation cross psychopy object
    - item: The item psychopy object
    - pic: The image psychopy object
    - prompt: The prompt psychopy object
    - feedback: The feedback psychopy object
    - fs: The frequency of the sound stimuli
    - rec_seconds: The number of seconds to record
    - pics_path: The path for all the pictures used in the stimuli
    - participant_info: A dictionary that contains all the information about the participant
    - flanker_shape_stimuli: The flanker shape stimuli
    - flanker_correct: The correct feedback image
    - flanker_incorrect: The incorrect feedback image
    - flanker_neutral: The neutral feedback image

    Returns:
    - None

    This function will update the results list with the participant's responses and reaction times for this task.
    """

    # Initialize the keyboard
    keyBoard = keyboard.Keyboard()
    keyBoard.clock.reset()

    # Get the start time of the task
    start_time = time.time()
    # Convert the start time to a readable format
    start_time_str = datetime.datetime.fromtimestamp(start_time).strftime('%H:%M:%S')

    # Loop through each stimulus
    for x in range(len(stimuli)):
        # Set the task name
        task = task_name
        # Initialize lists to hold correct and incorrect responses for flanker shape task
        correct_responses_flanker_shape = []
        incorrect_responses_flanker_shape = []
        # Initialize a counter for the number of trials in the flanker shape task
        flanker_shape_trial_counter = 0
        # Set the number of frames per flanker shape trial
        n_frames_per_flanker_shape = 100
        # Calculate the number of flanker shape trials (based on a total of 1200 frames)
        num_flanker_shape_trials = 1200 // n_frames_per_flanker_shape
        # Initialize a counter for the number of feedback frames
        feedback_counter = 0

        # Generate a random start and end frame for the main task stimulus presentation
        start_offset = random.randint(300, 601)  # random number between 300 and 600
        end_offset = start_offset + 350

        # Randomly shuffle the flanker shape stimuli
        random.shuffle(flanker_shape_stimuli)

        # Draw 'who is coming' text and display it for 1 second
        werKommt.name = 'werKommt'
        werKommt.draw()
        window.flip()
        core.wait(1.0)

        # Draw fixation cross and display it for 1 second
        fixation.name = 'fixation'
        fixation.draw()
        window.flip()
        core.wait(1.0)

        stimulus = stimuli.loc[x]['item']
        item.setText(stimulus)
        item.name = 'item_' + str(stimuli.loc[x]['ID'])

        pictogram = stimuli.loc[x]['pic']
        pic.image = pics_path + pictogram + '_small_borderless.png'
        pic.name = str(pic.image)

        responseRecord = None
        flanker_shape_stimulus_shown = False

        for frame in range(1200):  # Loop for 1200 frames
            # reading aloud primary task
            if start_offset <= frame < end_offset:  # This means that if the current frame is between start_offset and end_offset, it is the time to show the main task
                item.draw()  # Drawing the name of the image on the screen
                pic.draw()  # Drawing the image on the screen

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

            # flanker_shape task
            if frame % n_frames_per_flanker_shape == 0 and frame // n_frames_per_flanker_shape < num_flanker_shape_trials:
                # This condition checks whether it's time to start a new flanker shape task trial
                # Get the current stimulus, correct response and condition for the flanker shape task
                flanker_shape_stimulus, correct_response, condition = flanker_shape_stimuli[(frame // n_frames_per_flanker_shape) % len(flanker_shape_stimuli)]
                # Set the text of the prompt to the current stimulus
                prompt.setText(flanker_shape_stimulus)
                # Set the size and position of the prompt
                prompt.size = [0.5, 0.5]
                prompt.pos = [0, -0.4]
                prompt.draw()  # Draw the prompt
                flanker_shape_stimulus_shown = True  # This flag is used to know if we are in a flanker shape trial or not
                keyBoard.clock.reset()  # Reset the clock of the keyboard
                keyPressRegistered = False  # This flag is used to know if a key press was registered during the current flanker shape trial
                flanker_shape_trial_counter += 1  # Increase the flanker shape trial counter

                # Append the data of the current trial to the results
                results.append({
                    'task': task_name,
                    'phase': 'practice' if task_name.startswith('practice') else 'test',
                    'main_trial': str(x + 1),
                    'flanker_shape_trial': flanker_shape_trial_counter,
                    'flanker_shape_stimulus': flanker_shape_stimulus,
                    'flanker_shape_condition': condition,
                    'flanker_shape_correct': correct_response,
                    'flanker_shape_rt': 'NA',
                    'flanker_shape_response': 'NA',
                    'flanker_shape_response_accuracy': 'NA',
                    'presentation': 'dual' if start_offset <= frame < end_offset else 'single',
                    'start_time': start_time_str,
                    'end_time': 'NA',
                    'duration': 'NA',
                })

            elif 0 < frame % n_frames_per_flanker_shape < (n_frames_per_flanker_shape-30) and flanker_shape_stimulus_shown:
                # This condition means that we are in the middle of a flanker shape trial (before the feedback phase)
                prompt.draw()  # Keep drawing the prompt on the screen

            elif (n_frames_per_flanker_shape-30) <= frame % n_frames_per_flanker_shape and flanker_shape_stimulus_shown and not keyPressRegistered:
                # This condition means that it's the time to check for key presses (user's response)
                keys = keyBoard.getKeys(keyList=['a', 'l'], waitRelease=True)  # Check if the participant pressed 'a' or 'l'
                if keys:  # If there was a key press
                    response, rt = keys[0].name, keys[0].rt  # Get the key that was pressed and the reaction time
                    if response == correct_response:  # If the participant's response is correct
                        response_accuracy_flanker_shape = 'correct'
                        correct_responses_flanker_shape.append((response, rt))  # Append the response and the reaction time to the list of correct responses
                        keyPressRegistered = True  # Register that a key press has happened
                    else:  # If the participant's response is incorrect
                        response_accuracy_flanker_shape = 'incorrect'
                        incorrect_responses_flanker_shape.append((response, rt))  # Append the response and the reaction time to the list of incorrect responses
                    # Update the last trial data with the reaction time and the response
                    results[-1]['flanker_shape_rt'] = rt
                    results[-1]['flanker_shape_response'] = response
                else:  # If there was no key press
                    response_accuracy_flanker_shape = 'miss'  # The response is a miss
                    # Update the last trial data with 'none' as the reaction time and the response
                    results[-1]['flanker_shape_rt'] = 'none'
                    results[-1]['flanker_shape_response'] = 'none'

                keyBoard.clearEvents()  # Clear the events of the keyboard
                feedback_counter = 30  # Set the feedback counter to 30 frames
                flanker_shape_stimulus_shown = False  # The flanker shape trial has ended

            if feedback_counter > 0:  # If we are in the feedback phase
                if response_accuracy_flanker_shape == 'correct':  # If the response was correct
                    flanker_correct.draw()  # Draw the correct feedback
                elif response_accuracy_flanker_shape == 'incorrect':  # If the response was incorrect
                    flanker_incorrect.draw()  # Draw the incorrect feedback
                else:  # If the response was a miss
                    flanker_neutral.draw()  # Draw the neutral feedback
                feedback_counter -= 1  # Decrease the feedback counter

                # Record the end time and the duration
                end_time = time.time()  # Get the current time as the end time
                end_time_str = datetime.datetime.fromtimestamp(end_time).strftime('%H:%M:%S')  # Convert the end time to a string
                duration = end_time - start_time  # Calculate the duration of the trial
                # Convert the duration to hours, minutes and seconds
                hours, remainder = divmod(duration, 3600)
                minutes, seconds = divmod(remainder, 60)
                duration_str = '{:02d}:{:02d}:{:02d}'.format(int(hours), int(minutes), int(seconds))  # Convert the duration to a string

                # Update the last trial data with the response accuracy, the end time and the duration
                results[-1]['flanker_shape_response_accuracy'] = response_accuracy_flanker_shape
                results[-1]['end_time'] = end_time_str
                results[-1]['duration'] = duration_str
                # If the feedback counter has reached 0 (the feedback phase has ended)
                if feedback_counter == 0:
                    append_result_to_csv(results[-1], base_filename, participant_info, type='flanker_shape')  # Append the result of the last trial to the csv file
                    keyBoard.clearEvents()  # Clear the events of the keyboard

            window.flip()  # Update the window to show the drawn elements

        # Calculate the number of correct responses
        num_correct_responses_flanker_shape = len(correct_responses_flanker_shape)
        # Calculate the number of incorrect responses
        num_incorrect_responses_flanker_shape = len(incorrect_responses_flanker_shape)

        # Define a file name for the response record
        responseRecordName = 'dual_task_' + participant_info['subject'] + '_' + task_name + '_' + str(
            stimuli.loc[x]['ID']) + '.wav'

        # Calculate the average reaction time for correct responses if there are any
        average_rt_correct = round(sum(
            rt for _, rt in correct_responses_flanker_shape) / num_correct_responses_flanker_shape, 3) if correct_responses_flanker_shape else None
        # Calculate the average reaction time for incorrect responses if there are any
        average_rt_incorrect = round(sum(
            rt for _, rt in incorrect_responses_flanker_shape) / num_incorrect_responses_flanker_shape, 3) if incorrect_responses_flanker_shape else None

        # Display the number of correct and incorrect responses and their average reaction times
        feedback.setText(str(num_correct_responses_flanker_shape) + ' Mal korrekt (Reaktionszeit: ' + str(average_rt_correct) + ' s.) \n' + str(
            num_incorrect_responses_flanker_shape) + ' Mal inkorrekt (Reaktionszeit: ' + str(average_rt_incorrect) + ' s.)')

        feedback.setColor('black')  # Set the color of the feedback text to black
        feedback.pos = (0, 0)  # Set the position of the feedback text to the center of the window
        feedback.size = 0.15  # Set the size of the feedback text
        feedback.draw()  # Draw the feedback text on the window
        window.flip()  # Update the window to show the drawn elements
        core.wait(5)  # Wait for 5 seconds

        # Get the current time as the end time
        end_time = time.time()
        # Convert the end time to a string
        end_time_str = datetime.datetime.fromtimestamp(end_time).strftime('%H:%M:%S')
        # Calculate the duration of the task
        duration = end_time - start_time
        # Convert the duration to hours, minutes and seconds
        hours, remainder = divmod(duration, 3600)
        minutes, seconds = divmod(remainder, 60)
        # Convert the duration to a string
        duration_str = '{:02d}:{:02d}:{:02d}'.format(int(hours), int(minutes), int(seconds))

        # Get the last 12 rows from the results list
        last_twelve_results_flanker_shape = results[-12:]

        # Filter the last 12 rows for single presentation trials
        flanker_shape_results_single = [r for r in last_twelve_results_flanker_shape if
                          'presentation' in r and r['presentation'] == 'single']

        # Filter the last 12 rows for dual presentation trials
        flanker_shape_results_dual = [r for r in last_twelve_results_flanker_shape if
                        'presentation' in r and r['presentation'] == 'dual']

        # Calculate the number of single and dual presentation trials
        trials_single_shape = len(flanker_shape_results_single)
        trials_dual_shape = len(flanker_shape_results_dual)

        # Calculate the accuracy for single presentation trials if there are any
        flanker_shape_trial_accuracy_single = sum(r['flanker_shape_response_accuracy'] == 'correct' for r in
                                    flanker_shape_results_single) / trials_single_shape if trials_single_shape else None

        # Calculate the accuracy for dual presentation trials if there are any
        flanker_shape_trial_accuracy_dual = sum(r['flanker_shape_response_accuracy'] == 'correct' for r in
                                  flanker_shape_results_dual) / trials_dual_shape if trials_dual_shape else None

        # Calculate the number of correct responses for single presentation trials where the reaction time is not NA
        flanker_shape_correct_and_not_na_single = sum(
            1 for r in flanker_shape_results_single if
            'flanker_shape_response_accuracy' in r and 'flanker_shape_rt' in r and
            r['flanker_shape_response_accuracy'] == 'correct' and r['flanker_shape_rt'] != 'NA')

        # Calculate the average reaction time for correct responses for single presentation trials if there are any
        flanker_shape_trial_rt_correct_single = sum(
            float(r['flanker_shape_rt']) for r in flanker_shape_results_single if 'flanker_shape_response_accuracy' in r and
            'flanker_shape_rt' in r and r['flanker_shape_response_accuracy'] == 'correct' and
            r['flanker_shape_rt'] != 'NA') / flanker_shape_correct_and_not_na_single if flanker_shape_correct_and_not_na_single > 0 else None

        # Calculate the number of correct responses for dual presentation trials where the reaction time is not NA
        flanker_shape_correct_and_not_na_dual = sum(
            1 for r in flanker_shape_results_dual if
            'flanker_shape_response_accuracy' in r and 'flanker_shape_rt' in r and
            r['flanker_shape_response_accuracy'] == 'correct' and r['flanker_shape_rt'] != 'NA')

        # Calculate the average reaction time for correct responses for dual presentation trials if there are any
        flanker_shape_trial_rt_correct_dual = sum(
            float(r['flanker_shape_rt']) for r in flanker_shape_results_dual if
            'flanker_shape_response_accuracy' in r and 'flanker_shape_rt' in r and
            r['flanker_shape_response_accuracy'] == 'correct' and
            r['flanker_shape_rt'] != 'NA') / flanker_shape_correct_and_not_na_dual if flanker_shape_correct_and_not_na_dual > 0 else None

        # Calculate the number of incorrect responses for single presentation trials where the reaction time is not NA
        flanker_shape_incorrect_and_not_na_single = sum(
            1 for r in flanker_shape_results_single if
            'flanker_shape_response_accuracy' in r and 'flanker_shape_rt' in r and
            r['flanker_shape_response_accuracy'] == 'incorrect' and r['flanker_shape_rt'] != 'NA')

        # Calculate the average reaction time for incorrect responses for single presentation trials if there are any
        flanker_shape_trial_rt_incorrect_single = sum(
            float(r['flanker_shape_rt']) for r in flanker_shape_results_single if
            'flanker_shape_response_accuracy' in r and 'flanker_shape_rt' in r and
            r['flanker_shape_response_accuracy'] == 'incorrect' and
            r['flanker_shape_rt'] != 'NA') / flanker_shape_incorrect_and_not_na_single if flanker_shape_incorrect_and_not_na_single > 0 else None

        # Calculate the number of incorrect responses for dual presentation trials where the reaction time is not NA
        flanker_shape_incorrect_and_not_na_dual = sum(
            1 for r in flanker_shape_results_dual if
            'flanker_shape_response_accuracy' in r and 'flanker_shape_rt' in r and
            r['flanker_shape_response_accuracy'] == 'incorrect' and r['flanker_shape_rt'] != 'NA')

        # Calculate the average reaction time for incorrect responses for dual presentation trials if there are any
        flanker_shape_trial_rt_incorrect_dual = sum(
            float(r['flanker_shape_rt']) for r in flanker_shape_results_dual if
            'flanker_shape_response_accuracy' in r and 'flanker_shape_rt' in r and
            r['flanker_shape_response_accuracy'] == 'incorrect' and
            r['flanker_shape_rt'] != 'NA') / flanker_shape_incorrect_and_not_na_dual if flanker_shape_incorrect_and_not_na_dual > 0 else None

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
            'rand_nr_calc': 'NA',
            'rand_operation': 'NA',
            'answer_calc': 'NA',
            'answer_input': 'NA',
            'answer_input_accuracy': 'NA',
            '2back_matching_trials_single': 'NA',
            '2back_matching_trials_dual': 'NA',
            '2back_trial_accuracy_single': 'NA',
            '2back_trial_accuracy_dual': 'NA',
            '2back_trial_rt_correct_single': 'NA',
            '2back_trial_rt_correct_dual': 'NA',
            '2back_shape_order': 'NA',
            'flanker_nr_trials_single': 'NA',
            'flanker_nr_trials_dual': 'NA',
            'flanker_trial_accuracy_single': 'NA',
            'flanker_trial_accuracy_dual': 'NA',
            'flanker_trial_rt_correct_single': 'NA',
            'flanker_trial_rt_correct_dual': 'NA',
            'flanker_trial_rt_incorrect_single': 'NA',
            'flanker_trial_rt_incorrect_dual': 'NA',
            'flanker_shape_nr_trials_single': trials_single_shape,
            'flanker_shape_nr_trials_dual': trials_dual_shape,
            'flanker_shape_trial_accuracy_single': flanker_shape_trial_accuracy_single,
            'flanker_shape_trial_accuracy_dual': flanker_shape_trial_accuracy_dual,
            'flanker_shape_trial_rt_correct_single': flanker_shape_trial_rt_correct_single,
            'flanker_shape_trial_rt_correct_dual': flanker_shape_trial_rt_correct_dual,
            'flanker_shape_trial_rt_incorrect_single': flanker_shape_trial_rt_incorrect_single,
            'flanker_shape_trial_rt_incorrect_dual': flanker_shape_trial_rt_incorrect_dual,
            'start_time': start_time_str,
            'end_time': end_time_str,
            'duration': duration_str,
        })
        # Append the result to the CSV file
        append_result_to_csv(results[-1], base_filename, participant_info)


# Display instructions consecutively
def execute_task(window, task_name, participant_info, stimuli, werKommt, fixation, randNumber, item, pic, prompt,
                 feedback, input_text, keyList, fs, rec_seconds, movementDirections, responseList, dots, operations,
                 arrows, pics_path, shapes_list, shape, flanker_stimuli, flanker_correct, flanker_incorrect, flanker_neutral,flanker_shape_stimuli,
                 dual_task=False):

    """
    Orchestrates the execution of the tasks, whether they are dual or single. It prepares the paths for results and
    recordings of each participant, then calls the appropriate function to execute the task. It also displays an
    'end of practice' screen once the task is completed.

    Args:
        window (psychopy.visual.Window): The window object where the task will be displayed.
        task_name (str): The name of the task to be performed.
        participant_info (dict): A dictionary that contains information about the participant like subject id etc.
        stimuli (pandas.DataFrame): A DataFrame that contains the stimuli for the task.
        werKommt (psychopy.visual.TextStim): The TextStim object for "Wer kommt?" question.
        fixation (psychopy.visual.ShapeStim): The ShapeStim object for fixation cross.
        randNumber (psychopy.visual.TextStim): The TextStim object for displaying random number.
        item (psychopy.visual.TextStim): The TextStim object for displaying item.
        pic (psychopy.visual.ImageStim): The ImageStim object for displaying pictograms.
        prompt (psychopy.visual.TextStim): The TextStim object for displaying response prompt.
        feedback (psychopy.visual.TextStim): The TextStim object for displaying feedback.
        input_text (psychopy.visual.TextStim): The TextStim object for displaying input text.
        keyList (list): The list of keys allowed for the task.
        fs (int): The sample rate for recording.
        rec_seconds (float): The duration of recording in seconds.
        movementDirections (list): The list of possible directions for the dots to move.
        responseList (list): The list of corresponding responses for the dot movements.
        dots (psychopy.visual.DotStim): The DotStim object.
        operations (list): The list of mathematical operations for dual task.
        arrows (list): The list of arrow stimulus objects.
        pics_path (str): The path to the directory containing pictograms.
        shapes_list (list): The list of available shapes for the dual task.
        shape (psychopy.visual.ImageStim): The ImageStim object for displaying shapes in the dual task.
        flanker_stimuli (list): The list of flanker stimuli for the flanker task.
        flanker_correct (psychopy.visual.ShapeStim): The ShapeStim object for displaying correct feedback in the flanker task.
        flanker_incorrect (psychopy.visual.ShapeStim): The ShapeStim object for displaying incorrect feedback in the flanker task.
        flanker_neutral (psychopy.visual.ShapeStim): The ShapeStim object for displaying neutral feedback in the flanker task.
        flanker_shape_stimuli (list): The list of flanker shape stimuli for the flanker shape task.
        dual_task (bool, optional): The flag to denote whether the task to be executed is a dual task or not. Default is False.

    Returns:
        None
    """

    # Initialize an empty list to hold the results
    results = []
    # Import the end-of-practice instructions
    from instructions_old import instructPracticeSingleTaskEnd, instructPracticeDualTask_dotMotion_calc_End, \
        instructPracticeDualTask_2backEnd, instructPracticeDualTask_flankerEnd, instructPracticeDualTask_flankerShapeEnd

    # path setup results per participant
    # Define the path in results for each subject
    subj_path_results = os.path.join('results', participant_info['subject'])
    # Create the directory if it doesn't exist
    if not os.path.exists(subj_path_results):
        os.makedirs(subj_path_results)
    # generate the base_filename based on task_name and phase
    base_filename = os.path.join(subj_path_results,
                            f"{task_name}_{participant_info['subject']}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")

    # path setup recordings per participant
    # Define the path in recordings for each subject
    subj_path_rec = os.path.join('recordings', participant_info['subject'])
    # Create the directory if it doesn't exist
    if not os.path.exists(subj_path_rec):
        os.makedirs(subj_path_rec)

    # Execute the task and save the result
    if dual_task:
        if task_name == 'practice_dualTask_dotMotion_calc':
            execute_dualTask_dotMotion_calc(window, results, base_filename, subj_path_rec, stimuli, task_name, werKommt,
                                            fixation,
                                            randNumber, item, pic, prompt, feedback, input_text, keyList, fs,
                                            rec_seconds,
                                            movementDirections, responseList, dots, operations, arrows, pics_path,
                                            participant_info)
            display_text_and_wait(instructPracticeDualTask_dotMotion_calc_End, window)
        if task_name == 'test_dualTask_dotMotion_calc':
            execute_dualTask_dotMotion_calc(window, results, base_filename, subj_path_rec, stimuli, task_name, werKommt,
                                            fixation,
                                            randNumber, item, pic, prompt, feedback, input_text, keyList, fs,
                                            rec_seconds,
                                            movementDirections, responseList, dots, operations, arrows, pics_path,
                                            participant_info)

        if task_name == 'practice_dualTask_2back':
            execute_dualTask_2back(window, results, base_filename, subj_path_rec, stimuli, task_name, werKommt,
                                   fixation, item,
                                   pic, feedback, fs, rec_seconds, pics_path, participant_info, shapes_list, shape)
            display_text_and_wait(instructPracticeDualTask_2backEnd, window)
        if task_name == 'test_dualTask_2back':
            execute_dualTask_2back(window, results, base_filename, subj_path_rec, stimuli, task_name, werKommt,
                                   fixation, item,
                                   pic, feedback, fs, rec_seconds, pics_path, participant_info, shapes_list, shape)

        if task_name == 'practice_dualTask_flanker':
            execute_dualTask_flanker(window, results, base_filename, subj_path_rec, stimuli, task_name, werKommt,
                                     fixation, item,
                                     pic, prompt, feedback, fs, rec_seconds, pics_path, participant_info,
                                     flanker_stimuli,
                                     flanker_correct, flanker_incorrect, flanker_neutral)
            display_text_and_wait(instructPracticeDualTask_flankerEnd, window)
        if task_name == 'test_dualTask_flanker':
            execute_dualTask_flanker(window, results, base_filename, subj_path_rec, stimuli, task_name, werKommt,
                                     fixation, item,
                                     pic, prompt, feedback, fs, rec_seconds, pics_path, participant_info,
                                     flanker_stimuli,
                                     flanker_correct, flanker_incorrect, flanker_neutral)

        if task_name == 'practice_dualTask_flanker_shape':
            execute_dualTask_flanker_shape(window, results, base_filename, subj_path_rec, stimuli, task_name, werKommt,
                                           fixation,
                                           item, pic, prompt, feedback, fs, rec_seconds, pics_path, participant_info,
                                           flanker_shape_stimuli,
                                           flanker_correct, flanker_incorrect, flanker_neutral)
            display_text_and_wait(instructPracticeDualTask_flankerShapeEnd, window)
        if task_name == 'test_dualTask_flanker_shape':
            execute_dualTask_flanker_shape(window, results, base_filename, subj_path_rec, stimuli, task_name, werKommt,
                                           fixation,
                                           item, pic, prompt, feedback, fs, rec_seconds, pics_path, participant_info,
                                           flanker_shape_stimuli,
                                           flanker_correct, flanker_incorrect, flanker_neutral)

    else:
        execute_singleTask(window, results, subj_path_rec, stimuli, task_name, werKommt, fixation, item, pic, rec_seconds, fs,
                           pics_path, participant_info, base_filename)
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
    keys = event.waitKeys()

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