#!/usr/bin/env python3

import csv

class StatePopulation:

    POPULATION_FILE_PATH = "/home/mdaigle/covid/data/state_population.csv"
    state_populations = {}

    def __init__(self):
        first_row = True
        with open(StatePopulation.POPULATION_FILE_PATH) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                if first_row:
                    first_row = False
                else:
                    state = row[1]
                    population = row[2]
                    self.state_populations[state] = population

    # Get the state population for a given state name
    def get_state_population(self, state_name):
        if state_name in self.state_populations:
            return int(self.state_populations[state_name])
        else:
            return 0

    # Get the dictionary of state populations
    def get_state_populations():
        return self.state_populations