import DecisionTree

def test_gini_index():
    groups = [[["PlayGolf", "true"], ["PlayGolf", "true"], ["StayHome", "true"]], [["PlayGolf", "true"]]]
    classes = ["PlayGolf", "StayHome"]
    gini_impurity = DecisionTree.gini_index(groups, classes)
    print(gini_impurity)


#test_gini_index()