from nltk.corpus import wordnet

word = input("Word: ")
synsets = wordnet.synsets(word)

for synset in synsets:
    print()
    print(f"{synset.name()}: {synset.definition()}")
    for hypernym in synset.hypernyms():
        print(f"  {hypernym.name()}")
