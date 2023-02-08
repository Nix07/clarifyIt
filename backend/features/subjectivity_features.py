import numpy as np
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from textblob import TextBlob
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer
from nltk.corpus import sentiwordnet as swn
lemmatizer = WordNetLemmatizer()


def cutoff_values(val):
    if (val > 1):
        return 1
    elif (val < 0):
        return 0
    else:
        return val


def remove_stopwords(desc):
    stop = stopwords.words('english')
    desc_nostop = " ".join([word for word in desc.split() if word not in stop])
    return desc_nostop


def stemm_str(desc):
    st = PorterStemmer()
    desc_stem = " ".join([st.stem(word) for word in desc.split()])
    return desc_stem


def get_blob(desc_list):
    # lowering the letters
    desc_ls = [desc.lower() for desc in desc_list]
    # special chars
    #desc_ls = [desc.replace('[^\w\s]','') for desc in desc_ls]
    # stopwords
    desc_ls = [remove_stopwords(desc) for desc in desc_ls]
    # stemming
    #desc_ls = [stemm_str(desc) for desc in desc_ls]
    blobs = [TextBlob(desc) for desc in desc_ls]
    return blobs


def run_sentPolarsubj(df):
    blobs = get_blob(df.Description.str.lower())
    df['polarity'] = [blob.sentiment.polarity for blob in blobs]
    df['subjectivity'] = [blob.sentiment.subjectivity for blob in blobs]


def penn_to_wn(tag):
    """
    Convert between the PennTreebank tags to simple Wordnet tags
    """
    if tag.startswith('J'):
        return wn.ADJ
    elif tag.startswith('N'):
        return wn.NOUN
    elif tag.startswith('R'):
        return wn.ADV
    elif tag.startswith('V'):
        return wn.VERB
    return None


def get_sentiment(word, tag):
    """ returns list of pos neg and objective score. But returns empty list if not present in senti wordnet. """

    wn_tag = penn_to_wn(tag)
    if wn_tag not in (wn.NOUN, wn.ADJ, wn.ADV):
        return []

    lemma = lemmatizer.lemmatize(word, pos=wn_tag)
    if not lemma:
        return []

    synsets = wn.synsets(word, pos=wn_tag)
    if not synsets:
        return []

    # Take the first sense, the most common
    synset = synsets[0]
    swn_synset = swn.senti_synset(synset.name())

    return [swn_synset.pos_score(), swn_synset.neg_score(), swn_synset.obj_score()]


def get_sentiment_pos_score(desc):
    desc_lst = desc.split()
    pos_val = nltk.pos_tag(desc_lst)
    senti_val = [get_sentiment(x, y) for (x, y) in pos_val]
    score_ls = []
    for item in senti_val:
        if (len(item) == 3):
            score_ls.append(item[0])
    return np.mean(score_ls)


def get_sentiment_neg_score(desc):
    desc_lst = desc.split()
    pos_val = nltk.pos_tag(desc_lst)
    senti_val = [get_sentiment(x, y) for (x, y) in pos_val]
    score_ls = []
    for item in senti_val:
        if (len(item) == 3):
            score_ls.append(item[1])
    return np.mean(score_ls)


def get_sentiment_obj_score(desc):
    desc_lst = desc.split()
    pos_val = nltk.pos_tag(desc_lst)
    senti_val = [get_sentiment(x, y) for (x, y) in pos_val]
    score_ls = []
    for item in senti_val:
        if (len(item) == 3):
            score_ls.append(item[2])
    return np.mean(score_ls)


def normalize_pos_values(val_ls, min_val, max_val):
    return [((x - min_val) / (max_val - min_val)) for x in val_ls]


def compute_subjectivity_features(df, train_data_dic):
    run_sentPolarsubj(df)
    min_val = train_data_dic['pos_score_min']
    max_val = train_data_dic['pos_score_max']
    df['pos_score'] = normalize_pos_values(df.Description.map(
        lambda x: get_sentiment_pos_score(x)), min_val, max_val)
    df['pos_score'] = df.pos_score.map(lambda x: cutoff_values(x))

    min_val = train_data_dic['neg_score_min']
    max_val = train_data_dic['neg_score_max']
    df['neg_score'] = normalize_pos_values(df.Description.map(
        lambda x: get_sentiment_neg_score(x)), min_val, max_val)
    df['neg_score'] = df.neg_score.map(lambda x: cutoff_values(x))

    min_val = train_data_dic['obj_score_min']
    max_val = train_data_dic['obj_score_max']
    df['obj_score'] = normalize_pos_values(df.Description.map(
        lambda x: get_sentiment_obj_score(x)), min_val, max_val)
    df['obj_score'] = df.obj_score.map(lambda x: cutoff_values(x))
