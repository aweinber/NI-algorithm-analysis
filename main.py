import random
import sys

def read_in_file(file_name):
    test_object = open(file_name, 'r')
    data = test_object.readlines()
    out = []
    firstline = data[0].split(' ')
    num_var = firstline[2]
    num_clauses = firstline[3]

    for line in range(1, len(data)):
        str_array = data[line].split(' ')[:-1]  # copy into array
        int_arr = list(map(int, str_array))  # map from str to ints
        out.append(int_arr)

    test_object.close()

    return out, int(num_var), int(num_clauses)


def create_sample_vectors(vector, num_samples):
    """Create num_samples number of random samples, where each sample array
    is comprised of booleans such that the probability that sample[i] == True
    is equal to probability_vector[i]. Returns list of samples, each of which
    is a list."""
    samples = []

    for i in range(0, num_samples):
        new_sample = [False] * (len(vector))
        for j in range(0, len(vector)):
            if random.uniform(0, 1) < vector[j]:
                new_sample[j] = True
        samples.append(new_sample)

    return samples


def mutate_probability_vector(vector, mutate_prob, mutate_shift):
    """Given a probability vector, the probability of a mutation, and the
    strength of a mutation, apply mutations to create a new probability vector
    and the result."""

    new_vector = vector

    mutate_direction = 0  # default direction is downward
    for i in range(0, len(vector)):
        if random.uniform(0, 1) <= mutate_prob:
            if random.uniform(0, 1) <= .5:  # switch direction up
                mutate_direction = 1
            new_vector[i] = vector[i] * (1.0 - mutate_shift) + mutate_direction * mutate_shift
    return new_vector


def is_clause_satisfied(clause, sample):
    """Given a single clause and a single sample population,
    determine whether the sample satisfies the clause."""
    for i in range(0, len(clause)):

        if clause[i] < 0 and not sample[i]:  # neg num satisfied by False

            return True

        elif clause[i] > 0 and sample[i]:  # pos num satisfied by True

            return True

    return False


def count_satisfied_clauses(clause_set, sample):
    """Given a set of boolean clauses and a single sample, determine
    how many clauses the sample answer set satisfies."""

    counter = 0

    for clause in clause_set:

        if is_clause_satisfied(clause, sample):

            counter += 1

    return counter


def find_sample_counts(clause_set, samples):
    """Given a list of clauses and a list of samples, return a list
    sample_satisfy_count such that sample_satisfy_count[i] = x
    means that samples[i] satisfied x clauses"""

    sample_satisfy_count = [None] * len(samples)

    for i in range(0, len(samples)):

        sample_satisfy_count[i] = count_satisfied_clauses(clause_set, samples[i])

    return sample_satisfy_count


def find_outlier_samples(sample_satisfy_counts, samples, num_clauses):
    """Finds the best and the worst samples based on the minimum and maximum.
    Returns the best sample, the worst sample, and the index of the best sample"""
    best_amount = max(sample_satisfy_counts)
    best_index = sample_satisfy_counts.index(best_amount)
    best_sample = samples[best_index]

    worst_amount = max(sample_satisfy_counts)
    worst_index = sample_satisfy_counts.index(worst_amount)
    worst_sample = samples[worst_index]

    return best_sample, worst_sample, sample_satisfy_counts[best_index]


def update_vector_with_outlier(probability_vector, best_sample, rate):
    """Updates a probability vector using the outlying best sample using
    a magnitude rate. Reusable for update-to-best and update-from-worst"""
    for i in range(0, len(probability_vector)):

        vec = probability_vector[i]

        vec = vec * (1.0 - rate) + (best_sample[i] * rate)

        if vec > 1:
            vec = 1
        elif vec < 0:
            vec = 0

        probability_vector[i] = vec

    return probability_vector


def run_pbil(input_list):

    file_name = input_list[0]
    num_individuals = int(input_list[1])
    learning_rate = float(input_list[2])
    neg_learning_rate = float(input_list[3])
    mutation_prob = float(input_list[4])
    mutation_amount = float(input_list[5])
    num_iterations = int(input_list[6])

    clause_set, num_var, num_clauses = read_in_file(file_name)
    print("Beginning...")

    probability_vector = [.5] * num_var  # starting values

    best_clauses_sat = 0

    for i in range(0, num_iterations):
        samples = create_sample_vectors(probability_vector, num_individuals)
        sample_satisfy_counts = find_sample_counts(clause_set, samples)
        best, worst, best_clauses_sat = find_outlier_samples(sample_satisfy_counts, samples, len(clause_set))
        probability_vector = update_vector_with_outlier(probability_vector, best, learning_rate)
        if best != worst:
            probability_vector = update_vector_with_outlier(probability_vector, best, neg_learning_rate)
        mutate_probability_vector(probability_vector, mutation_prob, mutation_amount)

    print("Final probabilities:", probability_vector)
    print("Most clauses satisfied at end:", best_clauses_sat)


def main():

    input_list = sys.argv[1:] # ignore 'main.py' command
    print(input_list)
    if len(input_list) != 8:
        print("Error... must accept 8 command line arguments")
        return
    algorithm = input_list[7]

    if algorithm == 'p':
        run_pbil(input_list)






if __name__ == '__main__':
    main()