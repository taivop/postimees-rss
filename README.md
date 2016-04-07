# Fetch and manually classify Postimees articles

* fetch_articles.py pulls data from the RSS feed.
* elicit_ratings.py asks you to classify article titles (from command line). Motivation: [training a classifier](https://github.com/taivop/postimees-textclassifier).
* export_data.py saves the data into a nice csv file you can use e.g. for training an ML model.

Dependencies:
* [feedparser](https://pythonhosted.org/feedparser/)

