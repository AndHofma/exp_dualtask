"""
This script runs an experiment where participants complete single and dual tasks.
It starts by loading the necessary modules, setting up the stimuli, and displaying instructions.
Then, the experiment is executed in the following order:
single task practice, single task test, dual task practice, and dual task test.
The experiment finishes by displaying a 'thank you' message, closing the window, and saving the output.

The single task involves reading aloud the presented stimuli,
while the dual task requires participants to perform an additional task of identifying a number that was to be remembered,
 identifying the movement direction of a set of dots, counting high pitched beep sounds or reacting to high pitched
 beep sounds with a keypress.

Detailed inline comments have been added to help understand the flow and functionality of the script.
"""

# Import necessary PsychoPy libraries
from dualtask_stimuli_load_path_check import check_config_paths, load_and_randomize
from dualtask_configuration import get_participant_info, initialize_stimuli, create_window, stim_path, output_path, pics_path, record_path
from dualtask_task_setup import execute_task, display_and_wait, display_text_and_wait
from psychopy import core
from dualtask_instructions import *

# Checking validity of paths for stimuli and output
check_config_paths(stim_path, output_path, pics_path, record_path)
# Loading and randomizing the stimulus types
stimuli_single = load_and_randomize(stim_path, 'single')
stimuli_dual_number_dots = load_and_randomize(stim_path, 'dual_number_dots')
stimuli_dual_number_beep_press = load_and_randomize(stim_path, 'dual_number_beep_press')
stimuli_dual_beep_count_dots = load_and_randomize(stim_path, 'dual_beep_count_dots')

# this is just for debugging and piloting
"""stimuli_single[0] = stimuli_single[0][:2]

stimuli_single[1] = stimuli_single[1][:3]

stimuli_dual_number_dots[0] = stimuli_dual_number_dots[0][:3]
stimuli_dual_number_dots[1] = stimuli_dual_number_dots[1][:10]

stimuli_dual_number_beep_press[0] = stimuli_dual_number_beep_press[0][:3]
stimuli_dual_number_beep_press[1] = stimuli_dual_number_beep_press[1][:10]

stimuli_dual_beep_count_dots[0] = stimuli_dual_beep_count_dots[0][:3]
stimuli_dual_beep_count_dots[1] = stimuli_dual_beep_count_dots[1][:10]"""

# Get participant information
participant_info = get_participant_info()
# Creating the display window
window = create_window()
# Initializing all stimuli
werKommt, fixation, randNumber, item, prompt, feedback, fs, rec_seconds, movementDirections, responseList, dots, arrows, arrows_small, number_prompts = initialize_stimuli(window)

# Starting the experiment by displaying the instruction for the single task
display_text_and_wait(instructSingleTask1, window)
if display_text_and_wait(instructSingleTask2, window):
    display_text_and_wait(instructPracticeSingleTaskStart, window)

# Running the single task practice session
# practice items = stimuli_single[0]
execute_task(window=window,
             task_name='practice_single',
             participant_info=participant_info,
             stimuli=stimuli_single[0],
             werKommt=werKommt,
             fixation=fixation,
             randNumber=randNumber,
             item=item,
             prompt=prompt,
             feedback=feedback,
             fs=fs,
             rec_seconds=rec_seconds,
             movementDirections=movementDirections,
             responseList=responseList,
             dots=dots,
             arrows=arrows,
             arrows_small = arrows_small,
             number_prompts=number_prompts,
             )

# Running the single task test session
# test items = stimuli_single[1]
execute_task(window=window,
             task_name='test_single',
             participant_info=participant_info,
             stimuli=stimuli_single[1],
             werKommt=werKommt,
             fixation=fixation,
             randNumber=randNumber,
             item=item,
             prompt=prompt,
             feedback=feedback,
             fs=fs,
             rec_seconds=rec_seconds,
             movementDirections=movementDirections,
             responseList=responseList,
             dots=dots,
             arrows=arrows,
             arrows_small = arrows_small,
             number_prompts=number_prompts,
             )

"""# Displaying the instruction for the dual task
display_text_and_wait(instructDualTask_number_dots_1, window)
if display_text_and_wait(instructDualTask_number_dots_2, window):
    display_text_and_wait(instructPracticeDualTask_number_dots_Start, window)

# Running the dual task - number and dots - practice session
# practice items = stimuli_dual_number_dots[0]
execute_task(window=window,
             task_name='practice_number_dots',
             participant_info=participant_info,
             stimuli=stimuli_dual_number_dots[0],
             werKommt=werKommt,
             fixation=fixation,
             randNumber=randNumber,
             item=item,
             prompt=prompt,
             feedback=feedback,
             fs=fs,
             rec_seconds=rec_seconds,
             movementDirections=movementDirections,
             responseList=responseList,
             dots=dots,
             arrows=arrows,
             arrows_small=arrows_small,
             number_prompts=number_prompts,
             dual_task=True
             )

# Running the dual task - number and dots - test session
# randomized coordinates = stimuli_dual_number_dots[1]
execute_task(window=window,
             task_name='test_number_dots',
             participant_info=participant_info,
             stimuli=stimuli_dual_number_dots[1],
             werKommt=werKommt,
             fixation=fixation,
             randNumber=randNumber,
             item=item,
             prompt=prompt,
             feedback=feedback,
             fs=fs,
             rec_seconds=rec_seconds,
             movementDirections=movementDirections,
             responseList=responseList,
             dots=dots,
             arrows=arrows,
             arrows_small=arrows_small,
             number_prompts=number_prompts,
             dual_task=True  # or True if you want to execute a dual task
             )"""

# Displaying the instruction for the dot motion, calculation and beep deviation dual task
if display_text_and_wait(instructDualTask_number_beep_press_1, window):
    display_text_and_wait(instructDualTask_number_beep_press_2, window)

# Running the dual task - number and beep press - practice session
# practice items = stimuli_dual_number_beep_press[0]
execute_task(window=window,
             task_name='practice_number_beep_press',
             participant_info=participant_info,
             stimuli=stimuli_dual_number_beep_press[0],
             werKommt=werKommt,
             fixation=fixation,
             randNumber=randNumber,
             item=item,
             prompt=prompt,
             feedback=feedback,
             fs=fs,
             rec_seconds=rec_seconds,
             movementDirections=movementDirections,
             responseList=responseList,
             dots=dots,
             arrows=arrows,
             arrows_small = arrows_small,
             number_prompts=number_prompts,
             dual_task=True
             )

# Running the dual task - number and beep press - test session
# randomized coordinates = stimuli_dual_number_beep_press[1]
execute_task(window=window,
             task_name='test_number_beep_press',
             participant_info=participant_info,
             stimuli=stimuli_dual_number_beep_press[1],
             werKommt=werKommt,
             fixation=fixation,
             randNumber=randNumber,
             item=item,
             prompt=prompt,
             feedback=feedback,
             fs=fs,
             rec_seconds=rec_seconds,
             movementDirections=movementDirections,
             responseList=responseList,
             dots=dots,
             arrows=arrows,
             arrows_small = arrows_small,
             number_prompts=number_prompts,
             dual_task=True  # or True if you want to execute a dual task
             )

# Displaying the instruction for the dot motion, calculation and beep deviation dual task
if display_text_and_wait(instructDualTask_beep_count_dots_1, window):
    display_text_and_wait(instructDualTask_beep_count_dots_2, window)

# Running the dual task - beep count and dots - practice session
# practice items = stimuli_dual_beep_count_dots[0]
execute_task(window=window,
             task_name='practice_beep_count_dots',
             participant_info=participant_info,
             stimuli=stimuli_dual_beep_count_dots[0],
             werKommt=werKommt,
             fixation=fixation,
             randNumber=randNumber,
             item=item,
             prompt=prompt,
             feedback=feedback,
             fs=fs,
             rec_seconds=rec_seconds,
             movementDirections=movementDirections,
             responseList=responseList,
             dots=dots,
             arrows=arrows,
             arrows_small = arrows_small,
             number_prompts=number_prompts,
             dual_task=True
             )

# Running the dual task - beep count and dots - test session
# randomized coordinates = stimuli_dual_beep_count_dots[1]
execute_task(window=window,
             task_name='test_beep_count_dots',
             participant_info=participant_info,
             stimuli=stimuli_dual_beep_count_dots[1],
             werKommt=werKommt,
             fixation=fixation,
             randNumber=randNumber,
             item=item,
             prompt=prompt,
             feedback=feedback,
             fs=fs,
             rec_seconds=rec_seconds,
             movementDirections=movementDirections,
             responseList=responseList,
             dots=dots,
             arrows=arrows,
             arrows_small = arrows_small,
             number_prompts=number_prompts,
             dual_task=True  # or True if you want to execute a dual task
             )

# Show last prompt to end experiment with keypress
prompt.setText('Geschafft! \n Vielen Dank! \n Drücken Sie die Eingabetaste (Enter), um das Experiment zu beenden.')
prompt.height = 0.2
prompt.pos = [0, 0]
display_and_wait(prompt, window)
window.close()
core.quit()