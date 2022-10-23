import math

'''
Defines a node in the decision tree. A node can either directly classify to one
class or be a feature which splits based on the category the data point belongs to.
'''
class Stump():
    def __init__(feature = None, class = None):
        self.class = class
        self.feature = feature
        if feature:
            self.children = {}

'''
data: numpy array of features.
categories: map with number of categories in each feature
labels: Labels for each data point
This isn't optimized.
'''
def decision_tree(data, categories, labels):

    def get_category(value):
        return value

    def in_category(value, category):
        return value == category

    def get_impurity(classes):
        impurity = 0
        for prob in classes:
            if prob == 0 or prob == 1: continue
            impurity -= prob * math.log(prob)
        return impurity

    def get_best_feature(examples, categories):
        best_feature = None
        best_impurity = float('inf')
        for feature in categories.keys():
            impurity = 0
            counts = [set() for _ in range(len(categories[feature]))]
            for example in examples:
                counts[get_category(data[example][feature])].add(example)
            for category in range(len(counts)):
                classes = [0] * len(labels)
                for example in counts[category]:
                    classes[labels[example]] += 1 / len(counts[category])
                impurity += (len(counts[category]) / len(examples)) * get_impurity(classes)
            if impurity < best_impurity:
                best_impurity = impurity
                best_feature = feature
        return best_feature

    def get_new_examples(examples, feature, category):
        res = set()
        for example in examples:
            if in_category(data[example][feature], category): res.add(example)
        return res

    def get_new_categories(categories, feature):
        res = dict(categories)
        del res[feature]
        return res

    def build(examples, categories, parent_class):
        if not examples: return Stump(class = parent_class)
        classes = collections.Counter()
        for example in examples:
            classes[label[example]] += 1
        if len(class) == 1:
            return Stump(class = example_class)
        majority_class = max([(v, k) for k, v in classes.items()])[1]
        if not categories:
            return max([(v, k) for k, v in classes.items()])[1]
        feature = get_best_feature(examples, categories)
        stump = Stump(feature)
        for category in categories[feature]:
            stump.children[category] = build(get_new_examples(examples, feature, category), get_new_categories(categories, feature), majority_class)
        return stump

    return build(set(range(len(data))), categories, max([(v, k) for k, v in collections.Counter(labels).items()])[1])
