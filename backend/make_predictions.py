import time
from concurrent.futures import ProcessPoolExecutor
import multiprocessing
from multiprocessing import Pool

import pandas as pd
import numpy as np
from scipy import sparse
from scipy.sparse import hstack
from sklearn.preprocessing import normalize
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer

df = pd.DataFrame(columns=['State1', 'State3', 'State4',
                  'State5', 'State6', 'State7', 'State8', 'State9'])


X_train_vector = None


def get_tafrigh_set_lower_ros(top_n, df_train_ros):
    # .  clear short
    topwords_tot_clear = []
    corpus = df_train_ros[df_train_ros['state1_binary'] == 0].feature_tuned
    topwords = get_top_text_ngrams_nostop_lower(corpus, (1, 1), top_n)
    for item in topwords:
        topwords_tot_clear.append(item)

    for i in range(3, 10, 1):
        state_str = 'state'+str(i)+'_binary'
        corpus = df_train_ros[df_train_ros[state_str] == 0].feature_tuned
        topwords = get_top_text_ngrams_nostop_lower(corpus, (1, 1), top_n)
        for item in topwords:
            topwords_tot_clear.append(item)
    # # print(set(topwords_tot_clear))

    # unclear short
    topwords_tot_unclear = []
    corpus = df_train_ros[df_train_ros['state1_binary'] == 1].feature_tuned
    topwords = get_top_text_ngrams_nostop_lower(corpus, (1, 1), top_n)
    for item in topwords:
        topwords_tot_unclear.append(item)

    for i in range(3, 10, 1):
        state_str = 'state'+str(i)+'_binary'
        corpus = df_train_ros[df_train_ros[state_str] == 1].feature_tuned
        topwords = get_top_text_ngrams_nostop_lower(corpus, (1, 1), top_n)
        for item in topwords:
            topwords_tot_unclear.append(item)
    # # print(set(topwords_tot_unclear))

    # tafrigh
    topwords_core_short = []
    for item in set(topwords_tot_clear):
        if item not in set(topwords_tot_unclear):
            topwords_core_short.append(item)
    for item in set(topwords_tot_unclear):
        if item not in set(topwords_tot_clear):
            topwords_core_short.append(item)
    return topwords_core_short


def get_top_text_ngrams_withstop_lower(corpus, ngrams, nr):
    """
    creates a bag of ngrams and counts ngram frequency.

    returns a sorted list of tuples: (ngram, count)
    """

    vec = CountVectorizer(ngram_range=ngrams, lowercase=True).fit(corpus)
    bag_of_words = vec.transform(corpus)
    sum_words = bag_of_words.sum(axis=0)
    words_freq = [(word, sum_words[0, idx])
                  for word, idx in vec.vocabulary_.items()]
    words_freq = sorted(words_freq, key=lambda x: x[1], reverse=True)
    top_words_list = [item[0] for item in words_freq[:nr]]
    return top_words_list


def get_top_char_ngrams_withstop_lower(corpus, ngrams, nr):
    """
    creates a bag of ngrams and counts ngram frequency.

    returns a sorted list of tuples: (ngram, count)
    """

    vec = CountVectorizer(
        analyzer='char', ngram_range=ngrams, lowercase=True).fit(corpus)
    bag_of_words = vec.transform(corpus)
    sum_words = bag_of_words.sum(axis=0)
    words_freq = [(word, sum_words[0, idx])
                  for word, idx in vec.vocabulary_.items()]
    words_freq = sorted(words_freq, key=lambda x: x[1], reverse=True)
    top_words_list = [item[0] for item in words_freq[:nr]]
    return top_words_list


def get_tafrigh_set_lower_ros(top_n, df_train_ros):
    # .  clear short
    topwords_tot_clear = []
    corpus = df_train_ros[df_train_ros['state1_binary'] == 0].feature_tuned
    topwords = get_top_text_ngrams_nostop_lower(corpus, (1, 1), top_n)
    for item in topwords:
        topwords_tot_clear.append(item)

    for i in range(3, 10, 1):
        state_str = 'state'+str(i)+'_binary'
        corpus = df_train_ros[df_train_ros[state_str] == 0].feature_tuned
        topwords = get_top_text_ngrams_nostop_lower(corpus, (1, 1), top_n)
        for item in topwords:
            topwords_tot_clear.append(item)
    # # print(set(topwords_tot_clear))

    # unclear short
    topwords_tot_unclear = []
    corpus = df_train_ros[df_train_ros['state1_binary'] == 1].feature_tuned
    topwords = get_top_text_ngrams_nostop_lower(corpus, (1, 1), top_n)
    for item in topwords:
        topwords_tot_unclear.append(item)

    for i in range(3, 10, 1):
        state_str = 'state'+str(i)+'_binary'
        corpus = df_train_ros[df_train_ros[state_str] == 1].feature_tuned
        topwords = get_top_text_ngrams_nostop_lower(corpus, (1, 1), top_n)
        for item in topwords:
            topwords_tot_unclear.append(item)
    # # print(set(topwords_tot_unclear))

    # tafrigh
    topwords_core_short = []
    for item in set(topwords_tot_clear):
        if item not in set(topwords_tot_unclear):
            topwords_core_short.append(item)
    for item in set(topwords_tot_unclear):
        if item not in set(topwords_tot_clear):
            topwords_core_short.append(item)
    return topwords_core_short


def get_top_text_ngrams_nostop_lower(corpus, ngrams, nr):
    """
    creates a bag of ngrams and counts ngram frequency.

    returns a sorted list of tuples: (ngram, count)
    """

    vec = CountVectorizer(stop_words='english',
                          ngram_range=ngrams, lowercase=True).fit(corpus)
    #vec = CountVectorizer(ngram_range=ngrams).fit(corpus)
    bag_of_words = vec.transform(corpus)
    sum_words = bag_of_words.sum(axis=0)
    words_freq = [(word, sum_words[0, idx])
                  for word, idx in vec.vocabulary_.items()]
    words_freq = sorted(words_freq, key=lambda x: x[1], reverse=True)
    top_words_list = [item[0] for item in words_freq[:nr]]
    return top_words_list


def get_top_text_ngrams_withstop(corpus, ngrams, nr):
    """
    creates a bag of ngrams and counts ngram frequency.

    returns a sorted list of tuples: (ngram, count)
    """

    vec = CountVectorizer(ngram_range=ngrams, lowercase=False).fit(corpus)
    bag_of_words = vec.transform(corpus)
    sum_words = bag_of_words.sum(axis=0)
    words_freq = [(word, sum_words[0, idx])
                  for word, idx in vec.vocabulary_.items()]
    words_freq = sorted(words_freq, key=lambda x: x[1], reverse=True)
    top_words_list = [item[0] for item in words_freq[:nr]]
    return top_words_list


def get_top_char_ngrams_withstop(corpus, ngrams, nr):
    """
    creates a bag of ngrams and counts ngram frequency.

    returns a sorted list of tuples: (ngram, count)
    """

    vec = CountVectorizer(
        analyzer='char', ngram_range=ngrams, lowercase=False).fit(corpus)
    bag_of_words = vec.transform(corpus)
    sum_words = bag_of_words.sum(axis=0)
    words_freq = [(word, sum_words[0, idx])
                  for word, idx in vec.vocabulary_.items()]
    words_freq = sorted(words_freq, key=lambda x: x[1], reverse=True)
    top_words_list = [item[0] for item in words_freq[:nr]]
    return top_words_list


def get_tafrigh_set_ros(top_n, df_train):
    # .  clear short
    topwords_tot_clear = []
    corpus = df_train[df_train['state1_binary'] == 0].feature_tuned
    topwords = get_top_text_ngrams_nostop(corpus, (1, 1), top_n)
    for item in topwords:
        topwords_tot_clear.append(item)

    for i in range(3, 10, 1):
        state_str = 'state'+str(i)+'_binary'
        corpus = df_train[df_train[state_str] == 0].feature_tuned
        topwords = get_top_text_ngrams_nostop(corpus, (1, 1), top_n)
        for item in topwords:
            topwords_tot_clear.append(item)
    # # print(set(topwords_tot_clear))

    # unclear short
    topwords_tot_unclear = []
    corpus = df_train[df_train['state1_binary'] == 1].feature_tuned
    topwords = get_top_text_ngrams_nostop(corpus, (1, 1), top_n)
    for item in topwords:
        topwords_tot_unclear.append(item)

    for i in range(3, 10, 1):
        state_str = 'state'+str(i)+'_binary'
        corpus = df_train[df_train[state_str] == 1].feature_tuned
        topwords = get_top_text_ngrams_nostop(corpus, (1, 1), top_n)
        for item in topwords:
            topwords_tot_unclear.append(item)
    # # print(set(topwords_tot_unclear))

    # tafrigh
    topwords_core_short = []
    for item in set(topwords_tot_clear):
        if item not in set(topwords_tot_unclear):
            topwords_core_short.append(item)
    for item in set(topwords_tot_unclear):
        if item not in set(topwords_tot_clear):
            topwords_core_short.append(item)
    return topwords_core_short


def get_top_text_ngrams_nostop(corpus, ngrams, nr):
    """
    creates a bag of ngrams and counts ngram frequency.

    returns a sorted list of tuples: (ngram, count)
    """

    vec = CountVectorizer(stop_words='english',
                          ngram_range=ngrams, lowercase=False).fit(corpus)
    #vec = CountVectorizer(ngram_range=ngrams).fit(corpus)
    bag_of_words = vec.transform(corpus)
    sum_words = bag_of_words.sum(axis=0)
    words_freq = [(word, sum_words[0, idx])
                  for word, idx in vec.vocabulary_.items()]
    words_freq = sorted(words_freq, key=lambda x: x[1], reverse=True)
    top_words_list = [item[0] for item in words_freq[:nr]]
    return top_words_list


def predict_using_new_kBest_features(df_pred, trained_model, selector, vectorizers):

    global X_train_vector
    if (X_train_vector == None):
        # pos_tagging
        vectorizer = vectorizers['pos_vectorizer']
        X_train_pos = vectorizer.fit_transform(df_pred.DescPOS_Only)

        # phrases
        vectorizer = vectorizers['phrases_vectorizer']
        X_train_phrase = vectorizer.fit_transform(df_pred.phrases_ls)

        # char 3-gram
        vectorizer = vectorizers['gram_vectorizer']
        X_train_char = vectorizer.fit_transform(df_pred.Description)

        # Tfidf
        vectorizer = vectorizers['tf_idf_vectorizer']
        X_train_tfidf = vectorizer.fit_transform(df_pred.Description)

        # feature quality
        vectorizer = vectorizers['feature_vectorizer']

        X_train_transformed = vectorizer.fit_transform(df_pred.feature_tuned)
        X_train_norm = normalize(X_train_transformed, norm='l1', axis=1)

        # merging the vectors
        X_train_vector = hstack(
            (X_train_tfidf, X_train_pos, X_train_phrase, X_train_char, X_train_norm))

        X_train = np.array(df_pred[[
            'website', 'link', 'giventime', 'reward',
            # subjectivity
            'subjectivity', 'polarity', 'pos_score', 'neg_score', 'obj_score',
            # readability
            'Kincaid', 'ARI', 'Coleman_Liau', 'FleschReadingEase', 'GunningFogIndex',
            'LIX', 'SMOGIndex', 'RIX', 'DaleChallIndex',
            'mean_unique_word_count', 'mean_word_count', 'mean_word_length',
            'mean_punctuation_count', 'mean_sent_len', 'mean_letter_count', 'mean_digit_count',
            'mean_whitespace_count', 'mean_FullUpper_count', 'mean_FullLower_count',
            'mean_title_count', 'mean_char_count', 'mean_phrase_count',
            'mean_open_POS', 'mean_close_POS', 'mean_POS_VB', 'mean_POS_NN',
            'mean_POS_JJ', 'mean_POS_W', 'mean_POS_FW', 'mean_POS_LS', 'mean_tags_PERSON', 'mean_tags_QUANTITY', 'mean_tags_WORK_OF_ART', 'mean_tags_TIME',
            'mean_tags_PERCENT', 'mean_tags_LANGUAGE', 'mean_tags_PRODUCT', 'mean_tags_MONEY',
            'mean_tags_ORDINAL', 'mean_tags_CARDINAL', 'mean_tags_ORG', 'mean_tags_DATE',
            'mean_tags_LOC', 'mean_tags_LAW', 'mean_tags_EVENT', 'mean_tags_GPE', 'mean_tags_NORP',
            'mean_tags_FAC', 'mean_complex_words', 'mean_complex_words_dc',
        ]].values)

        Matrix_train = sparse.coo_matrix(X_train)
        X_train_vector = hstack((X_train_vector, Matrix_train))

    predictions = {}
    for key, _ in selector.items():
        X_new = selector[key].transform(X_train_vector)
        predictions[key] = trained_model[key].predict(X_new)

    return predictions


def predict(all_features, models, selectors, vectorizers):
    states = ['state1_new', 'state_3', 'state_4', 'state_5',
              'state_6', 'state_7', 'state_8', 'state_9']
    res = {'state1_new': {}, 'state_3': {}, 'state_4': {}, 'state_5': {},
           'state_6': {}, 'state_7': {}, 'state_8': {}, 'state_9': {}}

    global X_train_vector
    X_train_vector = None

    for state in states:
        res[state] = predict_using_new_kBest_features(
            all_features, models[state], selectors[state], vectorizers)

    return res
