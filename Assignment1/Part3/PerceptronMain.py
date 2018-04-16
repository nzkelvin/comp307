import random
import textwrap
import sys


class Feature:
    def __init__(self, image_data):
        self.row = []
        self.col = []
        self.sgn = []
        self.image_data = image_data
        self.input = None

        for i in range(4):
            self.row.append(random.randint(0, 9))
            self.col.append(random.randint(0, 9))
            self.sgn.append(random.randint(0, 1))
            self.input = self.produce_input()

    def produce_input(self):
        # Special bias feature
        if self.image_data is None:
            return 1

        sum_num = 0
        for i in range(len(self.row)):
            if int(self.image_data.pixels[self.row[i]][self.col[i]]) == self.sgn[i]:
                sum_num += 1
        if sum_num >= 3:
            return 1
        else:
            return 0


class Image:
    def __init__(self):
        self.target = None
        self.width = None
        self.height = None
        self.pixels = []
        self.features = None


num_of_features = 50


def load_data(path):
    try:
        images = []
        with open(path, "r") as datafile:
            line = datafile.readline().rstrip()
            while line:
                if line == 'P1':
                    image = Image()
                    image.target = 1 if datafile.readline().rstrip() == '#X' else 0
                    image.width, image.height = datafile.readline().rstrip().split()
                    pixel_string = datafile.readline().rstrip() + datafile.readline().rstrip()
                    image.pixels = textwrap.wrap(pixel_string, 10)
                    images.append(image)
                line = datafile.readline().rstrip()
            datafile.close()
        return images
    except Exception:
        print("Could not read file")


def prep_features(image):
    # The dummy feature is bias
    bias = Feature(None)
    features = [bias]
    for x in range(num_of_features):
        feature = Feature(image)
        features.append(Feature(image))
        print("image feature " + str(x + 1) + ": " + str(feature.input))

    return features


# Activation Function
def sign(sum):
    if sum > 0:
        return 1
    else:
        return 0


def guess(features, weights):
    sum = 0
    for i in range(len(weights)):
        sum += weights[i] * features[i].input

    return sign(sum)


def train(images, weights, k, max_cycles):
    train_rate = 0.2
    hits = 0

    # Do not run the entire data set more than 100 times
    if k > max_training_cycles:
        return k

    for image in images:
        prediction = guess(image.features, weights)
        if image.target == prediction:
            hits += 1
        else:
            # Adjust weight
            for idx in range(len(weights)):
                weights[idx] += (image.target - prediction) * image.features[idx].input * train_rate

    if hits == len(images):
        # Mission completed. All hit
        return k
    else:
        print("Training cycle # = " + str(k) + ", Classification error count = " + str(len(images) - hits))
        # recursive
        k += 1
        train(images, weights, k, max_cycles)


def run(training_file, max_cycles):
    images = load_data(training_file)

    for image in images:
        image.features = prep_features(image)

    # initiate weights
    weights = []
    for i in range(num_of_features + 1):
        weights.append(random.random())

    k = 0
    train(images, weights, k, max_cycles)
    print("weights:")
    for w in weights:
        print(w)


# main function
training_file_path = sys.argv[1] if len(sys.argv) > 1 else ".\image.data"
max_training_cycles = int(sys.argv[2]) if len(sys.argv) > 2 else 100
run(training_file_path, max_training_cycles)
