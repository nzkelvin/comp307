import math

def read_data_file(path):
    try:
        with open(path, "r") as data_file:
            # readlines() is optional here
            for line in data_file.readlines():
                yield line
    except Exception:
        print("Could not read file")


def load_data_from_file(path):
    data_list = []
    data_lines = read_data_file(path)
    for data_line in data_lines:
        if data_line and data_line.strip():
            # Convert data to float type
            data_part = [float(x) for x in data_line.split()[0:4]]
            # The last column is label
            data_part.append(data_line.split()[4])
            data_list.append(data_part)
    return data_list


def train():
    # do nothing
    pass


def predict(training_data, test_vector, feature_ranges, k):
    distances = []

    for training_vector in training_data:
        distances.append((calc_euclidean_distance(training_vector, test_vector, feature_ranges), training_vector, test_vector))

    # get the nearest k neighbours
    sorted(distances, key=lambda tup: tup[0])
    predicted_label = distances[0][2][4]
    print(predicted_label)
    return predicted_label


def verify_prdiction(training_data, test_data, k):
    feature_ranges = []
    # Workout the ranges for each feature
    for i in range(4):
        sorted_training_data = sorted(training_data, key=lambda tup: tup[i])
        max = sorted_training_data[-1][i]
        min = sorted_training_data[0][i]
        feature_ranges.append(max - min)

    for test_vector in test_data:
        predict(training_data, test_vector, feature_ranges, k)


# Pythagorean formula
def calc_euclidean_distance(training_vector, test_vector, feature_ranges):
    # Pythogorean formula
    # divided by range to normalize
    distance = 0
    for x in range(len(feature_ranges)):
        distance += pow((training_vector[x] - test_vector[x]), 2) / feature_ranges[x]
    # debug
    #print(math.sqrt(distance))
    return math.sqrt(distance)


# main function
data = load_data_from_file(".\iris-training.txt")
test_data = load_data_from_file(".\iris-test.txt")

# view test data for debugging
#for outer_data in data:
#    for inner_data in outer_data:
#        print(inner_data)


# using mock test data
#mock_test_data = [[5.0, 3.0, 1.6, 0.2, "Iris-setosa"]]
verify_prdiction(data, test_data, 3)


