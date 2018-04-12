import sys
import math
import collections
import datetime as dt


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
    VectorDistance = collections.namedtuple("VectorDistance", ['distance', 'training_vector'])

    distances = []

    for t_vector in training_data:
        distances.append(VectorDistance(calc_euclidean_distance(t_vector, test_vector, feature_ranges), t_vector))

    # get the nearest k neighbours
    distances = sorted(distances, key=lambda tup: tup.distance)
    k_neighbours = distances[0:k]

    # vote
    class_votes = {}
    for x in range(k):
        # training_vector[4] is the class label
        vote = k_neighbours[x].training_vector[4]
        if vote in class_votes:
            class_votes[vote] += 1
        else:
            class_votes[vote] = 1
    sorted_votes = sorted(class_votes.items(), key=lambda tup: tup[1], reverse=True)

    print(sorted_votes[0][0])
    return sorted_votes[0][0]


def verify_prediction(training_data, test_data, k):
    feature_ranges = []
    # Workout the ranges for each feature
    for i in range(4):
        sorted_training_data = sorted(training_data, key=lambda tup: tup[i])
        max = sorted_training_data[-1][i]
        min = sorted_training_data[0][i]
        feature_ranges.append(max - min)

    # Test
    accuracy_count = 0
    for test_vector in test_data:
        prediction = predict(training_data, test_vector, feature_ranges, k)
        if prediction == test_vector[-1]:
            accuracy_count += 1
    # Test accuracy in percentage
    print("classification accuracy = " + str(accuracy_count / len(test_data)))


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
training_file_path = sys.argv[1] if len(sys.argv) > 1 else ".\iris-training.txt"
test_file_path = sys.argv[2] if len(sys.argv) > 2 else ".\iris-test.txt"
k = int(sys.argv[3]) if len(sys.argv) > 3 else 3

data = load_data_from_file(training_file_path)
test_data = load_data_from_file(test_file_path)

# view test data for debugging
#for outer_data in data:
#    for inner_data in outer_data:
#        print(inner_data)


# using mock test data
#mock_test_data = [[5.0, 3.0, 1.6, 0.2, "Iris-setosa"]]
start_time = dt.datetime.now()
verify_prediction(data, test_data, k)
end_time = dt.datetime.now()
print("Execution duration = " + str((end_time - start_time).microseconds) + "(microseconds)")
