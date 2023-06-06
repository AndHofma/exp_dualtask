"""
The single task procedure (execute_singleTask) involves the presentation of visual stimuli and the recording
of the participant's response (reading out loud).
The dual task procedure (execute_dualTask) involves the presentation of visual stimuli, along with math problems
and a moving-dots task, and records the participant's response (reading out loud) and
their response to the math problem and moving-dots task.
"""

# Import necessary libraries
from psychopy import core, event, visual  # import some libraries from PsychoPy
import time
import datetime
import sounddevice as sd
from scipy.io.wavfile import write
import random
from configuration import append_result_to_csv
import os
from psychopy.hardware import keyboard


# single task procedure
def execute_singleTask(window, results, subj_path_rec, stimuli, task_name, werKommt, fixation, item, pic, rec_seconds, fs, pics_path, participant_info, filename):
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
        filename: The filename for the result CSV file.
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
            'trial': str(x+1),
            'phase': 'practice' if task_name == 'practice_singleTask' else 'test',
            'stimulus_ID': stimuli.loc[x]['ID'],
            'stimulus': stimuli.loc[x]['item'],
            'rand_Nr': 'NA',
            'stimulus_Rec': responseRecordName,
            'dot_Move_Dir': 'NA',
            'dot_1st_Frame': 'NA',
            'dot_Last_Frame': 'NA',
            'dot_Response_Key': 'NA',
            'dot_Response_Accuracy': 'NA',
            'rand_Nr_Calc': 'NA',
            'rand_Operation': 'NA',
            'answer_Calc': 'NA',
            'answer_Subject_Input': 'NA',
            'answer_Accuracy': 'NA',
            'nback_correct_responses': 'NA',
            'nback_false_responses': 'NA',
            'start_time': start_time_str,
            'end_time': end_time_str,
            'duration': duration_str,
        })
        # Append the result to the CSV file
        append_result_to_csv(results[-1], filename, participant_info)


# dual task procedure
def execute_dualTask_arrow_calc(window, results, filename, subj_path_rec, stimuli, task_name, werKommt, fixation, randNumber, item,
                                pic, prompt, feedback, input_text, keyList, fs, rec_seconds, movementDirections, responseList,
                                dots, operations, arrows, pics_path, participant_info):
    """
    Executes a dual task procedure in a psychophysical experiment.

    This function displays stimuli alongside math problems and arrow tasks.
    It records the participant's vocal response, as well as their responses to the math and arrow tasks.

    Args:
        window : A window object where the experiment is displayed.
        results : A list to store the results of the experiment.
        filename : The name of the file where results are to be stored.
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
            'trial': str(x+1),
            'phase': 'practice' if task_name == 'practice_dualTask' else 'test',
            'stimulus_ID': stimuli.loc[x]['ID'],
            'stimulus': stimuli.loc[x]['item'],
            'rand_Nr': str(randNr[x]),
            'stimulus_Rec': responseRecordName,
            'dot_Move_Dir': movement,
            'dot_1st_Frame': rand1stFrame,
            'dot_Last_Frame': randLastFrame,
            'dot_Response_Key': arrowKey,
            'dot_Response_Accuracy': dot_Accuracy,
            'rand_Nr_Calc': str(randNrForCalc[x]),
            'rand_Operation': operation_Name,
            'answer_Calc': answer,
            'answer_Subject_Input': partic_Input,
            'answer_Accuracy': calc_Accuracy,
            'nback_correct_responses': 'NA',
            'nback_false_responses': 'NA',
            'start_time': start_time_str,
            'end_time': end_time_str,
            'duration': duration_str,
        })
        # Append the result to the CSV file
        append_result_to_csv(results[-1], filename, participant_info)


def execute_dualTask_2_back(window, results, filename, subj_path_rec, stimuli, task_name, werKommt, fixation, item, pic,
                            prompt, feedback, fs, rec_seconds, pics_path, participant_info, shapes_list):
    """

    """

    # Initialize the keyboard
    kb = keyboard.Keyboard()

    # Initialize start time and start_time_str
    start_time = time.time()
    start_time_str = datetime.datetime.fromtimestamp(start_time).strftime('%H:%M:%S')

    # Iterate over stimuli
    for x in range(len(stimuli)):
        task = task_name

        n_frames_per_shape = 50  # want to show 6 different shapes within 300 frames
        n_shapes = 300 // n_frames_per_shape

        # Initialize a list for the shapes for the 2-back task
        shape_stimuli = [random.choice(shapes_list) for _ in range(n_shapes)]
        response_history = [False] * n_shapes  # initialize response history
        correct_responses = [shape_stimuli[i] == shape_stimuli[i-2] for i in range(n_shapes)]  # correct answers

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
            if frame % n_frames_per_shape == 0:  # Change the shape every n_frames_per_shape frames
                current_shape = shape_stimuli[frame // n_frames_per_shape]
                current_shape.draw()
                # Record responses
                kb.clock.reset()  # reset the clock
                keys = kb.getKeys(['space'], waitRelease=True)
                response_history[frame] = len(keys) > 0
            window.flip()
        sd.stop()  # stop the recording

        # calculate the number of correct and false responses
        num_correct = sum(a == b for a, b in zip(response_history[2:], correct_responses[2:]))
        num_false = sum(response_history[2:]) - num_correct
        num_matches = sum(response_history[2:])

        # safe stimulus recording as wav file
        write(os.path.join(subj_path_rec, 'dual_task_' + participant_info['subject'] + '_' + task_name + '_' + str(stimuli.loc[x]['ID']) + '.wav'), fs, responseRecord)
        # naming the recording wav file to find it in the log-file
        responseRecordName = 'dual_task_' + participant_info['subject'] + '_' + task_name + '_' + str(stimuli.loc[x]['ID']) + '.wav'

        # show first response screen
        feedback.setText('Sie haben' + num_correct + 'von' + num_matches + 'möglichen Matches richtig erkannt!')
        prompt.pos = (0, 0.3)
        prompt.size = 0.15
        prompt.draw()
        window.flip()

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
            'trial': str(x+1),
            'phase': 'practice' if task_name == 'practice_dualTask' else 'test',
            'stimulus_ID': stimuli.loc[x]['ID'],
            'stimulus': stimuli.loc[x]['item'],
            'rand_Nr': 'NA',
            'stimulus_Rec': responseRecordName,
            'dot_Move_Dir': 'NA',
            'dot_1st_Frame': 'NA',
            'dot_Last_Frame': 'NA',
            'dot_Response_Key': 'NA',
            'dot_Response_Accuracy': 'NA',
            'rand_Nr_Calc': 'NA',
            'rand_Operation': 'NA',
            'answer_Calc': 'NA',
            'answer_Subject_Input': 'NA',
            'answer_Accuracy': 'NA',
            'nback_correct_responses': num_correct,
            'nback_false_responses': num_false,
            'start_time': start_time_str,
            'end_time': end_time_str,
            'duration': duration_str,
        })
        # Append the result to the CSV file
        append_result_to_csv(results[-1], filename, participant_info)



# Display instructions consecutively
def execute_task(window, task_name, participant_info, stimuli, werKommt, fixation, randNumber, item, pic, prompt,
                 feedback, input_text, keyList, fs, rec_seconds, movementDirections, responseList, dots, operations,
                 arrows, pics_path, shapes_list, dual_task=False):
    """
    Orchestrates the execution of the tasks, whether they are dual or single. It prepares the paths for results and
    recordings of each participant, then calls the appropriate function to execute the task. It also displays an
    'end of practice' screen once the task is completed.

    Args:
        window (psychopy.visual.Window): Window object where the task will be displayed.
        task_name (str): Name of the task.
        participant_info (dict): Information about the participant such as the subject id.
        stimuli (pandas.DataFrame): Contains the stimuli for the task.
        werKommt (psychopy.visual.TextStim): Text stimulus object for "Wer kommt?" question.
        fixation (psychopy.visual.ShapeStim): Fixation cross stimulus.
        randNumber (psychopy.visual.TextStim): Text stimulus object for displaying random number.
        item (psychopy.visual.TextStim): Text stimulus object for displaying item.
        pic (psychopy.visual.ImageStim): Image stimulus for displaying pictograms.
        prompt (psychopy.visual.TextStim): Text stimulus object for displaying response prompt.
        feedback (psychopy.visual.TextStim): Text stimulus object for displaying feedback.
        input_text (psychopy.visual.TextStim): Text stimulus object for displaying input text.
        keyList (list): List of allowed keys for the task.
        fs (int): Sample rate for recording.
        rec_seconds (float): Recording duration in seconds.
        movementDirections (list): Possible directions for the dots to move.
        responseList (list): Corresponding responses for the dot movements.
        dots (psychopy.visual.DotStim): Dot stimulus object.
        operations (list): Mathematical operations for dual task.
        arrows (list): List of arrow stimulus objects.
        pics_path (str): Path to the directory containing pictograms.
        dual_task (bool, optional): Whether the task to be executed is a dual task. Default is False.

    Returns:
        None
    """
    # Initialize an empty list to hold the results
    results = []
    # Import the end-of-practice instructions
    from instructions import instructPracticeSingleTaskEnd, instructPracticeDualTaskEnd

    # path setup results per participant
    # Define the path in results for each subject
    subj_path_results = os.path.join('results', participant_info['subject'])
    # Create the directory if it doesn't exist
    if not os.path.exists(subj_path_results):
        os.makedirs(subj_path_results)
    # generate the filename based on task_name and phase
    filename = os.path.join(subj_path_results,
                            f"{task_name}_{participant_info['subject']}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")

    # path setup recordings per participant
    # Define the path in recordings for each subject
    subj_path_rec = os.path.join('recordings', participant_info['subject'])
    # Create the directory if it doesn't exist
    if not os.path.exists(subj_path_rec):
        os.makedirs(subj_path_rec)

    # Execute the task and save the result
    if dual_task:
        execute_dualTask_arrow_calc(window, results, filename, subj_path_rec, stimuli, task_name, werKommt, fixation,
                                    randNumber, item, pic, prompt, feedback, input_text, keyList, fs, rec_seconds,
                                    movementDirections, responseList, dots, operations, arrows, pics_path, participant_info)
        if task_name == 'practice_dualTask':
            display_text_and_wait(instructPracticeDualTaskEnd, window)
        execute_dualTask_2_back(window, results, filename, subj_path_rec, stimuli, task_name, werKommt, fixation, item,
                                pic, prompt, feedback, fs, rec_seconds, pics_path, participant_info, shapes_list)
        if task_name == 'practice_dualTask_2back':
            display_text_and_wait(instructPracticeDualTaskEnd, window)
    else:
        execute_singleTask(window, results, subj_path_rec, stimuli, task_name, werKommt, fixation, item, pic, rec_seconds, fs,
                           pics_path, participant_info, filename)
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
