"""
This script runs an experiment where participants complete single and dual tasks.
It starts by loading the necessary modules, setting up the stimuli, and displaying instructions.
Then, the experiment is executed in the following order:
single task practice, single task test, dual task practice, and dual task test.
The experiment finishes by displaying a 'thank you' message, closing the window, and saving the output.

The single task involves reading aloud the presented stimuli,
while the dual task requires participants to perform an additional task of identifying the movement direction
of a set of dots and performing mathematical operations (addition or subtraction) on random numbers.

Detailed inline comments have been added to help understand the flow and functionality of the script.
"""

# Import necessary PsychoPy libraries
from load_stimuli_check_path import check_config_paths, load_and_randomize
from configuration import get_participant_info, initialize_stimuli, create_window, stim_path, output_path, pics_path, record_path
from task_setup import execute_task, display_and_wait, display_text_and_wait
from psychopy import core
from instructions import *

# Checking validity of paths for stimuli and output
check_config_paths(stim_path, output_path, pics_path, record_path)
# Loading and randomizing the stimulus types
stimulus_Type = load_and_randomize(stim_path)
# Get participant information
participant_info = get_participant_info()
# Creating the display window
window = create_window()
# Initializing all stimuli
werKommt, fixation, randNumber, item, pic, prompt, feedback, input_text, keyList, fs, rec_seconds, movementDirections, responseList, dots, operations, arrows = initialize_stimuli(window)

# Starting the experiment by displaying the instruction for the single task
display_text_and_wait(instructSingleTask1, window)
if display_text_and_wait(instructSingleTask2, window):
    display_text_and_wait(instructPracticeSingleTaskStart, window)

# Running the single task practice session
# execute_task(stimulus_Type[0], 'practice_singleTask')  # practice items = stimulus_Type[0]
execute_task(window=window,
             task_name='practice_singleTask',
             participant_info=participant_info,
             stimuli=stimulus_Type[0],
             werKommt=werKommt,
             fixation=fixation,
             randNumber=randNumber,
             item=item,
             pic=pic,
             prompt=prompt,
             feedback=feedback,
             input_text=input_text,
             keyList=keyList,
             fs=fs,
             rec_seconds=rec_seconds,
             movementDirections=movementDirections,
             responseList=responseList,
             dots=dots,
             operations=operations,
             arrows=arrows,
             pics_path=pics_path
             )

# Running the single task test session
# execute_task(stimulus_Type[1], 'test_singleTask')  # test items = stimulus_Type[1]
execute_task(window=window,
             task_name='test_singleTask',
             participant_info=participant_info,
             stimuli=stimulus_Type[1],
             werKommt=werKommt,
             fixation=fixation,
             randNumber=randNumber,
             item=item,
             pic=pic,
             prompt=prompt,
             feedback=feedback,
             input_text=input_text,
             keyList=keyList,
             fs=fs,
             rec_seconds=rec_seconds,
             movementDirections=movementDirections,
             responseList=responseList,
             dots=dots,
             operations=operations,
             arrows=arrows,
             pics_path=pics_path
             )

# Displaying the instruction for the dual task
display_text_and_wait(instructDualTask1, window)
if display_text_and_wait(instructDualTask2, window):
    display_text_and_wait(instructPracticeDualTaskStart, window)

# Running the dual task practice session
# execute_task(stimulus_Type[0], 'practice_dualTask', dual_task=True)  # practice items = stimulus_Type[0]
execute_task(window=window,
             task_name='practice_dualTask',
             participant_info=participant_info,
             stimuli=stimulus_Type[0],
             werKommt=werKommt,
             fixation=fixation,
             randNumber=randNumber,
             item=item,
             pic=pic,
             prompt=prompt,
             feedback=feedback,
             input_text=input_text,
             keyList=keyList,
             fs=fs,
             rec_seconds=rec_seconds,
             movementDirections=movementDirections,
             responseList=responseList,
             dots=dots,
             operations=operations,
             arrows=arrows,
             pics_path=pics_path,
             dual_task=True
             )

# Running the dual task test session
# execute_task(stimulus_Type[1], 'test_dualTask', dual_task=True)  # randomized coordinates = stimulus_Type[1]
execute_task(window=window,
             task_name='test_dualTask',
             participant_info=participant_info,
             stimuli=stimulus_Type[1],
             werKommt=werKommt,
             fixation=fixation,
             randNumber=randNumber,
             item=item,
             pic=pic,
             prompt=prompt,
             feedback=feedback,
             input_text=input_text,
             keyList=keyList,
             fs=fs,
             rec_seconds=rec_seconds,
             movementDirections=movementDirections,
             responseList=responseList,
             dots=dots,
             operations=operations,
             arrows=arrows,
             pics_path=pics_path,
             dual_task=True  # or True if you want to execute a dual task
             )

# Show last prompt to end experiment with keypress
prompt.setText('Geschafft! \n Vielen Dank! \n Drücken Sie eine Taste, um das Experiment zu beenden.')
display_and_wait(prompt, window)
window.close()
core.quit()
