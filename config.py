# --*-- coding: utf-8 -*-


"""
This file contains the function used to handle loading a configuration file and command line arguments.
    load_configurations - Function to load configurations from a configurations file and command line arguments.
    print_arguments - Function to print the loaded arguments.
"""


# Built-in/Generic Imports
import sys
from configparser import ConfigParser
from argparse import ArgumentParser, Namespace

# Own Modules Import
from utils import log, str_to_bool


__author__    = ["Jacob Carse"]
__copyright__ = "Copyright 2023, Calibration Where it Matters"
__credits__   = ["Jacob Carse"]
__license__   = "MIT"
__version__   = "1.0.0"
__maintainer  = ["Jacob Carse"]
__email__     = ["j.carse@dundee.ac.uk"]
__status__    = "Development"


def load_configurations(description: str) -> Namespace:
    """
    Loads arguments from a configuration file and command line.
    Arguments from the command line override arguments from the configuration file.
    :param description: The description of the application that is shown when using the "--help" command.
    :return: ArgumentParser Namespace object containing the loaded configurations.
    """

    # Creates an ArgumentParser to read the command line arguments.
    argument_parser = ArgumentParser(description=description)

    # Creates a ConfigParser to read configurations file arguments.
    config_parser = ConfigParser()

    # Loads either a specified configurations file or file from the default location.
    if len(sys.argv) > 1:
        if sys.argv[1] == "--config_file":
            config_parser.read(sys.argv[2])
        else:
            config_parser.read("config.ini")
    else:
        config_parser.read("config.ini")

    # Standard Arguments
    argument_parser.add_argument("--config_file", type=str,
                                 default="config.ini",
                                 help="String - File path to the config file.")
    argument_parser.add_argument("--experiment", type=str,
                                 default=config_parser["standard"]["experiment"],
                                 help="String - The name of the current experiment.")
    argument_parser.add_argument("--task", type=str,
                                 default=config_parser["standard"]["task"],
                                 help="String - The task to be run, either \"train\" or \"test\".")
    argument_parser.add_argument("--seed", type=int,
                                 default=int(config_parser["standard"]["seed"]),
                                 help="Integer - Seed used to generate random numbers.")

    # Logging Arguments
    argument_parser.add_argument("--verbose", type=str_to_bool,
                                 default=config_parser["logging"]["verbose"].lower() == "true",
                                 help="Boolean - Should outputs should be printed on the terminal.")
    argument_parser.add_argument("--log_dir", type=str,
                                 default=config_parser["logging"]["log_dir"],
                                 help="String - Directory path for where log files are stored.")

    # Dataset Arguments
    argument_parser.add_argument("--dataset", type=str,
                                 default=config_parser["dataset"]["dataset"].lower(),
                                 help="String - Dataset to be used.")

    # Performance Arguments
    argument_parser.add_argument("--use_gpu", type=str_to_bool,
                                 default=config_parser["performance"]["use_gpu"].lower() == "true",
                                 help="Boolean - Should training and testing use GPU acceleration.")

    # Debug Arguments
    argument_parser.add_argument("--warning", type=str_to_bool,
                                 default=config_parser["debug"]["warning"].lower() == "true",
                                 help="Boolean - Should warnings be shown during the running of the application.")

    # Returns the argument parser.
    return argument_parser.parse_args()


def print_arguments(arguments: Namespace) -> None:
    """
    Prints all arguments in a ArgumentParser Namespace.
    :param arguments: ArgumentsParser Namespace object containing arguments.
    """

    # Cycles through all the arguments within the ArgumentParser Namespace.
    for argument in vars(arguments):
        log(arguments, f"{argument: <24}: {getattr(arguments, argument)}")

    # Adds a blank line after printing arguments.
    log(arguments, "\n")
