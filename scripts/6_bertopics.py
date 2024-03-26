import pandas as pd 
import numpy as np
from bertopic import BERTopic
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sentence_transformers import SentenceTransformer
import spacy.cli #german tagger
from dotenv import load_dotenv
import os

load_dotenv()

# stopwords
#nltk.download("punkt")
#nltk.download("stopwords")
stopwords=set(stopwords.words("german"))
custom_stopwords = ["ärztin", "arzt", "frau", "herr", "dr", "dr.", "praxis", "sein", "haben", "halten", "nehmen", "finden", "patient", "mal"]
stopwords.update(custom_stopwords)

# download + load german tagging model:
#spacy.cli.download("de_core_news_sm")
nlp = spacy.load("de_core_news_sm")

def remove_stopwords(data):  # data = array of strings
    output_list = []
    for review in data:
        review_tagged = nlp(review)
        item_list = []
        for token in review_tagged:
            if token.lemma_.lower() not in stopwords and token.is_stop == False:  #oder Abfrage token.is_stop
                item_list.append(token.lemma_.lower())
        output_list.append(" ".join(item_list))
    return output_list
    

df = pd.read_csv(os.getenv("REVIEWS_CSV"))

# show review overview/preview:
print(df.shape, "\n")
print(df.head(), "\n")
print(df["rating"].value_counts(), "\n")

#print(df.head(), "\n")
print(df.shape, "\n")

# negative ratings:
negRat_df = df[df.rating < 4]

# positive ratings:
posRat_df = df[df.rating > 3]

#print(negRat_df.head(), "\n")
print(negRat_df.shape, "\n")

# convert dfs to lists:
negRat_texts = negRat_df.review.to_list()
posRat_texts = posRat_df.review.to_list()

# remove stopwords:
negRat_texts = remove_stopwords(negRat_texts)
posRat_texts = remove_stopwords(posRat_texts)

#set up models + tune:
modelNegative = BERTopic(embedding_model="paraphrase-multilingual-MiniLM-L12-v2", language="german", nr_topics="auto")
neg_topics, neg_probabilities = modelNegative.fit_transform(negRat_texts)

modelPositive = BERTopic(embedding_model="paraphrase-multilingual-MiniLM-L12-v2", language="german", nr_topics="auto")
pos_topics, pos_probabilites = modelPositive.fit_transform(posRat_texts)

# show:
print("negative ratings:")
neg_modelpreview = modelNegative.get_topic_freq().head(20)
neg_topics = modelNegative.get_topics().items()
for topic_id, keywords in neg_topics:
    print(f"Topic {topic_id}: {keywords}\n")

print("\n\npositive ratings:")
pos_modelpreview = modelPositive.get_topic_freq().head(20)
pos_topics = modelPositive.get_topics().items()
for topic_id, keywords in pos_topics:
    print(f"Topic {topic_id}: {keywords}\n")




