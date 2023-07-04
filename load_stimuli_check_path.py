"""
This script checks and if necessary creates all output directories and also loads and randomizes the stimuli.
"""

# Import necessary libraries
import os
import pandas
import logging


def check_config_paths(stim_path, output_path, pics_path, record_path, shapes_path):
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
    # Check if the shapes directory exists
    if not os.path.exists(shapes_path):
        # Raise exception if not
        raise Exception("No shapes folder detected. Please make sure that "
                        "'shapes_path' is correctly set in the configurations")
    # Check if the output directory exists, if not, create it
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    # Check if the path to recorded files exists, if not, create it
    if not os.path.exists(record_path):
        os.mkdir(record_path)


def load_and_randomize(stim_path, task):
    """
    Loads stimulus data from an Excel file, separates it into practice and coordinates data,
    randomizes the coordinates data, and returns the combined data.

    The function repeatedly shuffles the rows of the coordinates data until it achieves a
    randomization where neither the 'condition' nor the 'name1' field have the same values
    in three consecutive rows.

    Parameters:
    stim_path : str
        The path to the directory containing the 'conditions.xlsx' file. This file
        should contain stimulus data to be randomized.
    task : str
        A string indicating the type of task. The task type doesn't affect the randomization
        but it is used to log the operation in case of errors.

    Returns:
    stimulus_type : list
        A list of two pandas.DataFrame objects. The first one contains the practice data
        and the second one contains the randomized coordinates data.

    Raises:
    IOError:
        If there is an error opening the 'conditions.xlsx' file, an IOError is raised with a
        detailed error message.
    KeyError:
        If there is an error reading the 'conditions.xlsx' file because it does not contain
        the expected columns, a KeyError is raised with a detailed error message.

    Note:
    This function relies on pandas for reading Excel data and handling dataframes. It also
    utilizes the logging module for logging errors.
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
        if task == "single":
            rand_coordinates = coordinates.sample(frac=1).reset_index(drop=True)
        elif task == "dual_number_dots":
            rand_coordinates = coordinates.sample(frac=1).reset_index(drop=True)
        elif task == "dual_number_beep_press":
            rand_coordinates = coordinates.sample(frac=1).reset_index(drop=True)
        else:
            rand_coordinates = coordinates.sample(frac=1).reset_index(drop=True)

        # check for repeats
        for i in range(0, len(rand_coordinates)):
            if i >= len(rand_coordinates) - 3:
                # rand_coordinates.to_csv('rand_Coordinates_%s.csv' % i)
                randomized = True
            elif \
                    rand_coordinates['condition'][i] == rand_coordinates['condition'][i + 1] and \
                            rand_coordinates['condition'][i] == rand_coordinates['condition'][i + 2] and \
                            rand_coordinates['condition'][i] == rand_coordinates['condition'][i + 3] or \
                    rand_coordinates['name1'][i] == rand_coordinates['name1'][i + 1] and \
                            rand_coordinates['name1'][i] == rand_coordinates['name1'][i + 2]:
                # rand_coordinates.to_csv('rand_Coordinates_%s.csv' % i)
                break

    # Append practice data and randomized coordinates data to stimulus_type
    stimulus_type = [practice, rand_coordinates]

    return stimulus_type
