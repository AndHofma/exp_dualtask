"""
This script checks and if necessary creates all output directories and also loads and randomizes the stimuli.
"""

# Import necessary libraries
import os
import pandas
import logging


def check_config_paths(stim_path, output_path, pics_path, record_path):
    """
        Function checks the existence of specific directories and raises
        exceptions with appropriate error messages if any of the directories are not found.
    """
    # Check if the input directory for stimuli exists
    if not os.path.exists(stim_path):
        # Raise exception if not
        raise Exception("No stimulus folder detected. Please make sure that "
                        "'stim_path' is correctly set in the configurations")
    # Check if the pics directory exists
    if not os.path.exists(pics_path):
        # Raise exception if not
        raise Exception("No pics folder detected. Please make sure that "
                        "'pics_path' is correctly set in the configurations")
    # Check if the output directory exists, if not, create it
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    # Check if the path to recorded files exists, if not, create it
    if not os.path.exists(record_path):
        os.mkdir(record_path)


def load_and_randomize(stim_path):
    """
    Load stimuli data from an Excel file, randomize the coordinates without consecutive repetitions,
    and return a list containing practice and randomized coordinates data.

    Returns:
        stimulus_Type (list): A list containing two dataframes - practice data and randomized coordinates data.
    """
    try:
        # save all data from all cols and rows in dataframe
        stimuli = pandas.read_excel(stim_path + 'conditions.xlsx')
    except IOError:
        msg_error = "Fehler beim Öffnen der Datei '{}': Datei falsch benannt oder nicht im gleichen Verzeichnis?".format(
            stim_path)
        logging.log(level=logging.ERROR, msg=msg_error)
        quit()
    except KeyError as e:
        error = str(e)
        msg_error = "Fehler beim lesen der Datei '{}': Es konnte keine Spalte mit dem Titel '{}' gefunden werden.".format(
            stim_path, error)
        logging.log(level=logging.ERROR, msg=msg_error)
        quit()

    # Separate practice data and coordinates data
    practice = stimuli[:6]
    coordinates = stimuli[6:]

    randomized = False

    while not randomized:
        # Randomize the order of coordinates
        rand_Coordinates = coordinates.sample(frac=1).reset_index(drop=True)

        # check for repeats
        for i in range(0, len(rand_Coordinates)):
            if i >= len(rand_Coordinates) - 3:
                # rand_Coordinates.to_csv('rand_Coordinates_%s.csv' % i)
                randomized = True
            elif \
                    rand_Coordinates['condition'][i] == rand_Coordinates['condition'][i + 1] and \
                            rand_Coordinates['condition'][i] == rand_Coordinates['condition'][i + 2] and \
                            rand_Coordinates['condition'][i] == rand_Coordinates['condition'][i + 3] or \
                    rand_Coordinates['name1'][i] == rand_Coordinates['name1'][i + 1] and \
                            rand_Coordinates['name1'][i] == rand_Coordinates['name1'][i + 2]:
                # rand_Coordinates.to_csv('rand_Coordinates_%s.csv' % i)
                break

    # Append practice data and randomized coordinates data to stimulus_Type
    stimulus_Type = [practice, rand_Coordinates]

    return stimulus_Type
