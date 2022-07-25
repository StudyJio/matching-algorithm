
import math
import numpy
from geopy import distance
import pandas
import pygad
import random

path_to_user_data = "ToyUserData1.csv"

def reorder_chromosome(chromosome):
    dictionary = {}

    for i in range(len(chromosome)):

        if (chromosome[i] not in dictionary): # O(1) average time
            dictionary[chromosome[i]] = len(dictionary)

        chromosome[i] = dictionary[chromosome[i]]

def generate_chromosome(length):
    
    # Generate the array [0, 1, 2, ..., length - 1].
    chromosome = []
    chromosome.extend(range(length))

    # Shuffle the array.
    numpy.random.shuffle(chromosome)

    # Divide (integer division) each number by five.
    chromosome = [math.floor(n / 5) for n in chromosome]
    reorder_chromosome(chromosome)

    return chromosome

def chromosome_is_valid(chromosome):

    number_of_groups = math.floor(len(chromosome) / 5)

    # Use a dictionary to maintain a count of how many times each integer has been seen.
    occurrences = {}
    for i in range(number_of_groups):
        occurrences[i] = 0

    # When iterating through the chromosome, remember what is the highest number seen.
    highest_number_seen = -1

    # Iterate through the chromosome.
    for i in range(len(chromosome)):

        current_number = chromosome[i]

        # (The chromosome cannot contain the number 8 if there are only 5 groups.)
        if (current_number > (number_of_groups - 1)):
            return False

        # (The chromosome cannot contain negative numbers.)
        if (current_number < 0):
            return False
        
        occurrences[current_number] += 1

        if (current_number - highest_number_seen > 1):
            return False

        highest_number_seen = max(current_number, highest_number_seen)     

    # Check the dictionary for any values which !== 5.
    for i in range(number_of_groups):
        if (occurrences[i] != 5):
            return False

    return True

def repair_chromosome(chromosome):

    number_of_groups = math.floor(len(chromosome) / 5)

    # Use a dictionary to maintain a count of how many times each integer has been seen.
    occurrences = {}
    for i in range(number_of_groups):
        occurrences[i] = 0

    # Iterate through the chromosome.
    for i in range(len(chromosome)):

        # (If a number in the chromosome is out of bounds, replace it with 0.)
        if (chromosome[i] > number_of_groups - 1 or chromosome[i] < 0):
            chromosome[i] = 0
        
        occurrences[chromosome[i]] += 1

    # Get an array of numbers there are too few of.
    # For example, if the chromosome has three 7s, the array will be [..., 7, 7, ...].

    array_of_missing_numbers = []

    for group_number in range(number_of_groups):
        if (occurrences[group_number] < 5):
            for ignore in range(5 - occurrences[group_number]):
                array_of_missing_numbers.append(group_number)

    numpy.random.shuffle(array_of_missing_numbers)

    # Select a place in the chromosome to start reparing.
    repair_chromosome_index = numpy.random.randint(len(chromosome));

    for ignore in range(len(chromosome)):
        current_number = chromosome[repair_chromosome_index]

        if (occurrences[current_number] > 5):
            chromosome[repair_chromosome_index] = array_of_missing_numbers.pop()
            
            occurrences[current_number] -= 1
            # (There is no need to do occurrences[number_that_replaces_current_number] += 1.)

        # Look at the next number in the chromosome.
        # If we have reached the end of the chromosome, jump to the beginning of the chromosome.
        repair_chromosome_index = (repair_chromosome_index + 1) % len(chromosome)

# Read the data.
df_location = pandas.read_csv("Location Information.csv", index_col = "station_name")

# Return the distance between the MRT stations in kilometers.
def distance_between_locations(station_1: str, station_2: str):

    station_1 = station_1.upper()
    station_2 = station_2.upper()

    station_1_coordinates = (df_location.loc[station_1].latitude, df_location.loc[station_1].longitude)
    station_2_coordinates = (df_location.loc[station_2].latitude, df_location.loc[station_2].longitude)
    
    return math.ceil(distance.distance(station_1_coordinates, station_2_coordinates).km)

def learning_style_compatibility(array_1, array_2):

    # Divide the input vectors by their magnitudes to obtain unit vectors.
    array_1_normalised = array_1 / numpy.linalg.norm(array_1)
    array_2_normalised = array_2 / numpy.linalg.norm(array_2)

    return numpy.dot(array_1_normalised, array_2_normalised)

def module_compatibility(set_1: set, set_2: set):
    return len(set_1.intersection(set_2))

# Read the data.
df_users = pandas.read_csv(path_to_user_data, index_col = "user_id")

class User:
    def __init__(self, user_id, dim_1, dim_2, dim_3, dim_4, location, module_1, module_2, module_3, module_4, module_5, module_6):
        self.user_id = user_id
        self.learning_style = [dim_1, dim_2, dim_3, dim_4]
        self.location = location
        self.modules = {module_1, module_2, module_3, module_4, module_5, module_6}

    def toString(self):
        return "user_id: " + str(self.user_id) + " learning_style: " + str(self.learning_style) + " location: " + str(self.location) + " modules: " + str(self.modules)


# An optimisation would be to initialise the users before the genetic algorithm begins.

def get_user_from_id(user_id):

    row = df_users.loc[user_id]

    return User(user_id, row.studying_style_dim_1, row.studying_style_dim_2, row.studying_style_dim_3, row.studying_style_dim_4, row.user_location, row.module_1, row.module_2, row.module_3, row.module_4, row.module_5, row.module_6)
   

def calculate_pair_compatibility(user_1, user_2):
    # user_1 and user_2 are of type User.

    a = 50 * module_compatibility(user_1.modules, user_2.modules)
    b = 100 * learning_style_compatibility(user_1.learning_style, user_2.learning_style)
    c = - 5 * distance_between_locations(user_1.location, user_2.location)
    
    return a + b + c

def calculate_group_compatibility(user_array):
    # user_array is an array of type User.

    compatibility_score = 0

    number_of_users = len(user_array)

    for i in range(0, number_of_users):
        for j in range(i, number_of_users):
            if (i != j):
                compatibility_score += calculate_pair_compatibility(user_array[i], user_array[j])
    
    return compatibility_score / math.comb(number_of_users, 2)

def calculate_chromosome_fitness(chromosome, solution_index):

    # solution_index is not used. PyGAD requires such a parameter.
    
    # if (not chromosome_is_valid(chromosome)):
    #     print("Chromosome is invalid.")
    #     repair_chromosome(chromosome)

    # Parse the chromosome and represent the grouping using a dictionary.
    # The dictionary's keys are the team IDs. Each value is an array of user objects.
    number_of_users = len(chromosome)
    number_of_groups = math.floor(number_of_users / 5)

    dictionary = {}

    # Initialise the dictionary.
    for i in range(number_of_groups):
        dictionary[i] = []

    # Add users to their corresponding groups.
    for i in range(number_of_users):
        dictionary[chromosome[i]].append(get_user_from_id(i))
        
    total_group_compatibility = 0;
    for i in range(number_of_groups):
        total_group_compatibility += calculate_group_compatibility(dictionary[i])

    return total_group_compatibility / number_of_groups

def callback_gen(ga_instance):
    print("Generation: " + str(ga_instance.generations_completed)
    + " | Highest Fitness: " + str(round(ga_instance.best_solution()[1])))

    # For every chromosome,
    for i in range(sol_per_pop):
        # Ensure that the chromosome is valid.
        if (not chromosome_is_valid(ga_instance.population[i])):
            print("callback_gen(): Invalid chromosome was found!")

def custom_mutation_function(offspring, ga_instance):

    # To each chromosome, swap the values at two randomly chosen locations.
    for chromosome_index in range(offspring.shape[0]):

        # Select two indices.
        index_1 = numpy.random.randint(0, offspring.shape[1])
        index_2 = numpy.random.randint(0, offspring.shape[1])

        # It is possible that index_1 == index_2.
        # It is possible that the values at the two indices are the same.
        # These are okay.

        # Swap the values at the two indices.
        temp = offspring[chromosome_index, index_1]
        offspring[chromosome_index, index_1] = offspring[chromosome_index, index_2]
        offspring[chromosome_index, index_2] = temp

        # Reorder the chromosome.
        reorder_chromosome(offspring[chromosome_index])

    return offspring

class Team:
    def __init__(self, userIDs, compatibility_score):
        self.userIDs = userIDs # An array of user IDs (integers).
        self.compatibility_score = compatibility_score

    def toString(self):
        return "userIDs: " + str(self.userIDs) + " compatibility_score: " + str(self.compatibility_score)


def custom_crossover_function(parents, offspring_size, ga_instance):
    
    # The parameter parents is a 2D array of size (number of parents mating, number of users).
    # The paremeter offspring_size is a 2-tuple of the form (number of offspring, number of users).
    # I am unsure how the number of offspring is determined.
    
    array_of_offspring = []

    # Create offspring_size[0] number of arrays of size offspring_size[1].
    for i in range(offspring_size[0]):

        array_of_teams = []

        # Randomly choose two different parents.
        parent_1_index = numpy.random.randint(0, parents.shape[0])
        parent_2_index = numpy.random.randint(0, parents.shape[0])
        while (parent_1_index == parent_2_index):
            parent_2_index = numpy.random.randint(0, parents.shape[0])
        
        # Create a chromosome with values initialised to -1.
        offspring = numpy.full(offspring_size[1], -1)
        
        # For each parent chromosome, create n/5 teams.
        for parent_index in [parent_1_index, parent_2_index]:

            for team_id in range(math.floor(offspring_size[1] / 5)):
                # Determine the IDs of the users which the parent chromosome assigned to the team with team_id.
                # The parent chromosome is parents[parent_index].

                # Determine the indices of parents[parent_index] at which the value is team_id.
                # (The user IDs of the team members of team team_id)
                user_indices = numpy.where(parents[parent_index] == team_id)[0]

                # For each user ID, create an object.
                user_objects = []
                for user_index in user_indices:
                    user_objects.append(get_user_from_id(user_index))

                # Create a team object.
                team = Team(user_indices, calculate_group_compatibility(user_objects))

                array_of_teams.append(team)
        
        # Sort the array of teams by their compatibility score.
        array_of_teams.sort(key=lambda x: x.compatibility_score, reverse=True)

        # Records the number of teams assigned together so far.
        number_of_teams_assigned = 0

        # Assign the user IDs of the top team to the offspring.
        for team in array_of_teams:
            # If any member in the team has already been assigned a team in the offspring chromosome (i.e. the value is not -1),
            # then skip this team.

            # For each user ID in the team, if offspring[user_id] is not -1, then skip this team.
            everyone_not_yet_assigned = True

            for user_id in team.userIDs:
                if (offspring[user_id] != -1):
                    everyone_not_yet_assigned = False
            
            if (not everyone_not_yet_assigned):
                continue
            
            # Otherwise, put this team's members together in the offspring chromosome!
            for user_id in team.userIDs:
                offspring[user_id] = number_of_teams_assigned

            number_of_teams_assigned += 1

        # At the end, there will probably be some leftover users who are (still) assigned to team -1.
        # Randomly allocate these users into groups.

        # First, get an array of the user IDs of users who are not assigned to a team.
        unassigned_user_ids = numpy.where(offspring == -1)[0]
        
        # Shuffle the array of user IDs.
        numpy.random.shuffle(unassigned_user_ids)

        members_in_group = 0
        for user_id in unassigned_user_ids:
            # Assign the current user to the group with id number_of_teams_assigned.
            offspring[user_id] = number_of_teams_assigned
            members_in_group += 1

            # If the current group is full, then start a new group.
            if (members_in_group == 5):
                number_of_teams_assigned += 1
                members_in_group = 0
        
        # Reorder and repair the chromosome.
        reorder_chromosome(offspring)

        array_of_offspring.append(offspring)

    # Return a numpy array of size (28, 20).
    return numpy.array(array_of_offspring)

initial_population = []
sol_per_pop = 64

number_of_users = len(df_users)

for i in range(sol_per_pop):
    initial_population.append(generate_chromosome(number_of_users))

def debug_on_start(ga_instance):
    print("debug_on_start() =============== ")
    # Print the initial population.
    print("Initial population:")
    for i in range(sol_per_pop):
        print(str(ga_instance.population[i]) + " " + str(chromosome_is_valid(ga_instance.population[i])))

def debug_on_fitness(ga_instance, population_fitness):
    print("on_fitness()")

def debug_on_parents(ga_instance, selected_parents):
    print("debug_on_parents() ===================== ")
    # Print each selected parent.
    for parent in selected_parents:
        print(str(parent) + " " + str(chromosome_is_valid(parent)))

def debug_on_crossover(ga_instance, offspring_crossover):
    print("debug_on_crossover() ===================== ")
    # Print each offspring.
    for offspring in offspring_crossover:
        print(offspring + " " + str(chromosome_is_valid(offspring)))

def debug_on_mutation(ga_instance, offspring_mutation):
    print("debug_on_mutation() ===================== ")
    # Print each offspring.
    for offspring in offspring_mutation:
        print(str(offspring) + " " + str(chromosome_is_valid(offspring)))

def debug_on_generation(ga_instance):
    print("on_generation()")




ga_instance = pygad.GA(num_generations=50,
                       num_parents_mating=8,
                       fitness_func=calculate_chromosome_fitness,
                       sol_per_pop=sol_per_pop,
                       initial_population=initial_population,
                       num_genes=number_of_users,
                       parent_selection_type="sss",
                       keep_parents=4,
                       crossover_type=custom_crossover_function,
                       mutation_type=custom_mutation_function,
                       mutation_percent_genes=10,
                       gene_type=int,
                       callback_generation=callback_gen,
                       # parallel_processing=4,
                        #    on_start=debug_on_start,
                        #    on_parents=debug_on_parents,
                        #    on_crossover=debug_on_crossover,
                        #    on_mutation=debug_on_mutation,
                        #    on_fitness=debug_on_fitness,
                        #    on_generation=debug_on_generation
                       )


ga_instance.run()

ga_instance.plot_fitness()

solution = ga_instance.best_solution()[0]

for i in range(len(solution)):
    if (solution[i] == 2):
        print(get_user_from_id(i).toString())