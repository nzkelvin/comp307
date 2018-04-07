def gini_index(groups, classes):
    # All instances count
    n_instances = float(sum([len(group) for group in groups]))
    # sum weighted Gini index for each group
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

    return gini


def test_gini_index():
    groups = [[["PlayGolf", "true"], ["PlayGolf", "true"], ["StayHome", "true"]], [["PlayGolf", "true"]]]
    classes = ["PlayGolf", "StayHome"]
    gini_impurity = gini_index(groups, classes)
    print(gini_impurity)


#test_gini_index()