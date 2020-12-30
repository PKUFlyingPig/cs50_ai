from pagerank import transition_model
corpus = {"1.html": {"2.html", "3.html"}, "2.html": {"3.html"}, "3.html": {"2.html"}}
page = "1.html"
x = transition_model(corpus, page, 0.85)
print(x)