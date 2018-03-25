def assign_value_to_dictionary_after_initialization():
    votes = {}

    votes["Iris-sentosa"] = 3
    votes["Iris-versicolor"] = 2

    for v in votes:
        print(v)


def named_dictionary_collection():
    test_data = [dict(feature1=5.0, label="iris-blue")]
    print(test_data[0]["feature1"])


named_dictionary_collection()