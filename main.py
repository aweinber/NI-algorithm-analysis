import random

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
    and the result"""

    new_vector = vector

    mutate_direction = 0

    for i in range(0, len(vector)):

        if random.uniform(0, 1) <= mutate_prob:

            if random.uniform(0, 1) <= .5:

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

    best_sample_count = -1  # guarantee we will get a maximum b/c min is sat 0
    worst_sample_count = num_clauses + 1  # guarantee we will get a minimum b/c max is num_clauses

    best = []
    worst = []
    best_index = 0
    worst_index = 0

    for i in range(0, len(sample_satisfy_counts)):

        if sample_satisfy_counts[i] > best_sample_count:

            best = samples[i]
            best_sample_count = sample_satisfy_counts[i]
            best_index = i
            # print("New best:", best)

        if sample_satisfy_counts[i] < worst_sample_count:

            worst = samples[i]
            worst_sample_count = sample_satisfy_counts[i]
            worst_index = i

    # print("Best got:", sample_satisfy_counts[best_index])
    # print("Worst got:", sample_satisfy_counts[worst_index])
    return best, worst, sample_satisfy_counts[best_index]


def update_toward_best(probability_vector, best_sample, learning_rate):

    for i in range(0, len(probability_vector)):

        vec = probability_vector[i]

        vec = vec * (1.0 - learning_rate) + (best_sample[i] * learning_rate)

        if vec > 1:
            vec = 1
        elif vec < 0:
            vec = 0

        probability_vector[i] = vec

    return probability_vector


def update_from_worst(probability_vector, best_sample, neg_learning_rate):

    for i in range(0, len(probability_vector)):

        vec = probability_vector[i]

        vec = vec * (1.0 - neg_learning_rate) + (best_sample[i] * neg_learning_rate)

        if vec > 1:
            vec = 1
        elif vec < 0:
            vec = 0

        probability_vector[i] = vec

    return probability_vector


def main():

    num_samples = 100
    num_iterations = 1000
    mut_probability = .02
    mut_shift = .05

    clause_set, num_var, num_clauses = read_in_file("problem-2.cnf")
    # print("Clauses:", clause_set)
    print("Beginning...")

    probability_vector = [.5] * num_var  # starting values

    counter = 0

    best_clauses_sat = 0

    while counter < num_iterations:
        samples = create_sample_vectors(probability_vector, num_samples)
        # print("Samples:", samples)

        sample_satisfy_counts = find_sample_counts(clause_set, samples)
        # print("Satisfy counts:", sample_satisfy_counts)

        best, worst, best_clauses_sat = find_outlier_samples(sample_satisfy_counts, samples, len(clause_set))

        # print("Best: ", best, "Worst:", worst)

        probability_vector = update_toward_best(probability_vector, best, .1)

        if best != worst:

            probability_vector = update_from_worst(probability_vector, best, .075)

        mutate_probability_vector(probability_vector, mut_probability, mut_shift)

        # print("New probabilities:", probability_vector)

        counter += 1

    print("Final probabilities:", probability_vector)
    print("Most clauses satisfied at end:", best_clauses_sat)



if __name__ == '__main__':
    main()