import csv
import sys
from datetime import datetime

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    
    with open('shopping.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        evidence_list = []
        label_list = []
        month_set = set()
        for row in reader:
            month_set.add(row['Month'])
            evidence_row = []

            evidence_row.append(int(row['Administrative']))
            evidence_row.append(float(row['Administrative_Duration']))
            evidence_row.append(int(row['Informational']))
            evidence_row.append(float(row['Informational_Duration']))
            evidence_row.append(int(row['ProductRelated']))
            evidence_row.append(float(row['ProductRelated_Duration']))
            evidence_row.append(float(row['BounceRates']))
            evidence_row.append(float(row['ExitRates']))
            evidence_row.append(float(row['PageValues']))
            evidence_row.append(float(row['SpecialDay']))
            evidence_row.append(month_string_to_int_dict(row['Month']))
            evidence_row.append(int(row['OperatingSystems']))
            evidence_row.append(int(row['Browser']))
            evidence_row.append(int(row['Region']))
            evidence_row.append(int(row['TrafficType']))

            visitor_type = 1
            if row['VisitorType'] != 'Returning_Visitor':
                visitor_type = 0

            evidence_row.append(visitor_type)
            evidence_row.append(boolean_string_to_int(row['Weekend']))

            evidence_list.append(evidence_row)

            label_list.append(boolean_string_to_int(row['Revenue']))
        
        data = []
        index = 0
        for row in reader:
            data.append({
                    "evidence": evidence_list[index],
                    "label":  label_list[index]
                }
            )

            index += 1
    
    print(f"month_set {month_set}")

    return (evidence_list,label_list)

def month_string_to_int_dict(month_name):
    month_mapping = {
        "january": 0, "february": 1, "march": 2, "april": 3,
        "june": 5, "july": 6, "august": 7,
        "september": 8, "october": 9, "november": 10, "december": 11,
        "jan": 0, "feb": 1, "mar": 2, "apr": 3,
        "may": 4, "jun": 5, "jul": 6, "aug": 7,
        "sep": 8, "oct": 9, "nov": 10, "dec": 11
    }
    return month_mapping.get(month_name.lower())

def boolean_string_to_int(bool_str):
    """
    Returns 0 or 1 based on string value passed False or True respectively
    """
    if bool_str.lower() == "true":
        return 1
    elif bool_str.lower() == "false":
        return 0
    else:
        raise ValueError("Invalid boolean string: Must be 'True' or 'False'")

def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(evidence,labels)
    return model

def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """

    sensitivity = 0
    specificity = 0

    total_size = len(labels)
    correct = 0
    incorrect = 0
    true_positive = 0
    true_negative = 0
    false_positive = 0
    false_negative = 0
    for actual,predicted in zip(labels,predictions):
        #if correct < 10:
        #    print(F"actual {actual} predicted {predicted}")

        if actual == predicted:
            correct += 1
        
        if actual != predicted:
            incorrect += 1

        if actual == 1 and predicted == 1:
            true_positive += 1

        if actual == 1 and predicted == 0:
            false_negative += 1

        if actual == 0 and predicted == 0:
            true_negative += 1

        if actual == 0 and predicted == 1:
             false_positive += 1

    
    print(f"true_positive {true_positive} false_negative {false_negative} true_negative {true_negative} false_positive {false_positive}")

    sensitivity = 0
    if (true_positive + false_negative) > 0:
        sensitivity = true_positive / (true_positive + false_negative)

    specificity = 0
    if (true_negative + false_positive) > 0:
        specificity = true_negative / (true_negative + false_positive)

    return (sensitivity,specificity)


if __name__ == "__main__":
    main()
