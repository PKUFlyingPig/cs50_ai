import nltk
import os
import sys


def main():

    # Read data from files
    if len(sys.argv) != 2:
        sys.exit("Usage: python sentiment.py corpus")
    positives, negatives = load_data(sys.argv[1])

    # Create a set of all words
    words = set()
    for document in positives:
        words.update(document)
    for document in negatives:
        words.update(document)

    # Extract features from text
    training = []
    training.extend(generate_features(positives, words, "Positive"))
    training.extend(generate_features(negatives, words, "Negative"))

    # Classify a new sample
    classifier = nltk.NaiveBayesClassifier.train(training)
    s = input("s: ")
    result = (classify(classifier, s, words))
    for key in result.samples():
        print(f"{key}: {result.prob(key):.4f}")


def extract_words(document):
    return set(
        word.lower() for word in nltk.word_tokenize(document)
        if any(c.isalpha() for c in word)
    )


def load_data(directory):
    result = []
    for filename in ["positives.txt", "negatives.txt"]:
        with open(os.path.join(directory, filename)) as f:
            result.append([
                extract_words(line)
                for line in f.read().splitlines()
            ])
    return result


def generate_features(documents, words, label):
    features = []
    for document in documents:
        features.append(({
            word: (word in document)
            for word in words
        }, label))
    return features


def classify(classifier, document, words):
    document_words = extract_words(document)
    features = {
        word: (word in document_words)
        for word in words
    }
    print(features)
    return classifier.prob_classify(features)


if __name__ == "__main__":
    main()
