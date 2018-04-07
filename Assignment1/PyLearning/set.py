outcomes = ["Stay Home", "Play Golf", "Play Golf", "Stay Home", "Play Golf", "Stay Home", "Play Golf"]

groups = set(outcomes)

# Lambda is basically anonymous funcs
# The below can be converted to max(set(outcomes), lambda x: outcomes.count(x))
# 1. It's a key/value pair
# the output of set(outcomes) feeds into key=outcome.count
decision = max(set(outcomes), key=outcomes.count)
decision2 = max(outcomes, key=outcomes.count)

num_of_playgolf = outcomes.count("Play Golf")

print()