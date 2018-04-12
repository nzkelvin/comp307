class DecisionAttribute:
    def __init__(self, index, name, usage_count):
        # self is an instance attribute(python). instance VS class
        self.name = name
        self.index = index
        self.usage_count = usage_count

    def __str__(self):
        return str({"name": self.name, "index": self.index, "usage_count": self.usage_count})


def load_file(path):
    try:
        with open(path, "r") as datafile:
            for line in datafile.readlines():
                yield line
    except Exception:
        print("Could not read file")


# Status: Done
def load_data(path):
    lines = load_file(path)

    instances = []
    #yield doesn't return an array. You have to for ... in ... first to achieve it.
    for line in lines:
        instances.append(line.split())

    if len(instances) < 2:
        raise Exception("Couldn't find instances in data file " + path)

    idx = 1
    attributes = []
    for attr in instances[1]:
        attr_obj = DecisionAttribute(idx, attr, 0)
        attributes.append(attr_obj)
        idx += 1

    return {'attributes': attributes, 'instances': instances[2:], 'classes': [data for data in instances[0]]}


# Make a decision here
# Status: Done
def to_leaf(node):
    outcomes = [row[0] for row in node['instances']]
    if len(outcomes) < 1:
        raise Exception('leaf node does not have any instances')
    majority_class = max(set(outcomes), key=outcomes.count)
    prob = outcomes.count(majority_class) / len(outcomes)
    node['prob'] = prob
    return majority_class


# Split a dataset based on an attribute and an attribute value
def test_split(index, value, node):
    dataset = node["instances"]
    left, right = list(), list()
    for row in dataset:
        if row[index] == value:
            left.append(row)
        else:
            right.append(row)
    return left, right


# Evaluate a split
def gini_index(groups, classes):
    # All instances count
    # sum Gini index for each group
    gini = 0.0
    for group in groups:
        size = float(len(group))
        # avoid divide by zero
        if size == 0:
            continue
        score = 1.0
        # score the group based on the score for each class
        for class_val in classes:
            p = [row[0] for row in group].count(class_val) / size
            score = score * p

        # len(classes) / len(classes) is because I will use equal weigh on each group.
        gini += score * (len(classes) / len(classes))
        # Alternatively I can weight the group by its relative size like below
        # gini += score * (size / n_instances)

    #print("gini: " + str(gini) + ", groups: " + str(groups))
    return gini


def get_best_split(node):
    b_gini_index = 999
    b_groups = []
    b_attr = None
    for attr in node["attributes"]:
        # true on the right side. false on the left side
        groups = test_split(attr.index, 'false', node)
        current_gini_index = gini_index(groups, node["classes"])
        if current_gini_index < b_gini_index:
            b_gini_index = current_gini_index
            b_groups = groups
            b_attr = attr

    current_attr_list = node["attributes"][:]
    node["attributes"].remove(b_attr)
    # prepare for the next recursive iteration
    # attributes, instances, classes are for the next level
    # split_value and split_attr are for the current level
    left = {'attributes': node["attributes"][:], 'instances': b_groups[0], 'classes': node["classes"], 'split_value': 'false', 'split_attr': b_attr}
    right = {'attributes': node["attributes"][:], 'instances': b_groups[1], 'classes': node["classes"], 'split_value': 'true', 'split_attr': b_attr}

    node["attributes"] = current_attr_list
    node['groups'] = [left, right]
    node['best_index'] = b_gini_index
    node['best_attribute'] = b_attr
    return node


# each node contains: instance and attributes
def build_tree(node):
    # node["groups"] is the pre-stage of the left and right nodes
    left, right = node["groups"]
    del(node["groups"])

    # recursive conditions check
    if len(left) == 0 & len(right) == 0:
        raise Exception("Parent data set is empty! This should never happen.")
    if len(node['attributes']) < 1:
        node['class'] = to_leaf(node)
    #else if reaches deepth max (optional)
    #else if reaches instances amount minimum (optional)
    else:
        if len(left['instances']) > 0:
            # if impurity is 0
            if node['best_index'] == 0:
                node['class'] = to_leaf(node)
            else:
                node["left"] = get_best_split(left)
                #print("The best gini is " + str(node["left"]["best_index"]))
                build_tree(node["left"])
        if len(right['instances']) > 0:
            # if impurity is 0
            if node['best_index'] == 0:
                node['class'] = to_leaf(node)
            else:
                node["right"] = get_best_split(right)
                #print("The best gini is " + str(node["right"]["best_index"]))
                build_tree(node["right"])


def print_tree(node, indentation):
    if node is not None:
        if 'split_value' in node:
            print(indentation + node['split_attr'].name + " = " + node['split_value'] + ", instances count = " + str(len(node['instances'])))
        if 'class' in node:
            print(indentation + "  Class " + node['class'] + ', prob = ' + str(node['prob']))

        indentation += '  '
        if 'left' in node:
            # No instances means it is not node. It is just a shell which we can ignore.
            if ('instances' in node['left'] is not None) & (len(node['left']['instances']) > 0):
                print_tree(node['left'], indentation)
            else:
                return

        if 'right' in node:
            if ('instances' in node['right'] is not None) & (len(node['right']['instances']) > 0):
                print_tree(node['right'], indentation)
            else:
                return


def test():
    file_pathes = [".\hepatitis-test-run01.dat",
                   ".\hepatitis-test-run02.dat",
                   ".\hepatitis-test-run03.dat",
                   ".\hepatitis-test-run04.dat",
                   ".\hepatitis-test-run05.dat",
                   ".\hepatitis-test-run06.dat",
                   ".\hepatitis-test-run07.dat",
                   ".\hepatitis-test-run08.dat",
                   ".\hepatitis-test-run09.dat",
                   ".\hepatitis-test-run10.dat"]

    tree = train()
    for path in file_pathes:
        test_dataset = load_data(path)

        accuracy_count = 0
        for row in test_dataset['instances']:
            prediction = traverse_tree(tree, row)
            actual = row[0]
            # print(prediction + ' ' + actual)
            if prediction == actual:
                accuracy_count += 1

        print("Accuracy = " + str(accuracy_count / len(test_dataset['instances'])))


def traverse_tree(node, row):
    if 'class' in node:
        return node['class']

    value = row[node['best_attribute'].index]
    if (value == 'true') & ('right' in node):
        return traverse_tree(node['right'], row)
    elif 'left' in node:
        return traverse_tree(node['left'], row)


def train():
    #dataset = load_data(".\golf-test.dat")
    dataset = load_data(".\hepatitis-training-run01.dat")
    if dataset['instances']:
        root_node = get_best_split(dataset)
        # remove used attribute
        build_tree(root_node)
    else:
        raise Exception('There is no instance in the root node.')

    print_tree(root_node, '')
    return root_node


# train() is included in test() now
test()