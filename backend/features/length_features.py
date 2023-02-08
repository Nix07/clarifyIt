import os
from os.path import dirname
import pandas as pd
import numpy as np
import string
import nltk
from nltk.tree import Tree
from nltk.tag import StanfordPOSTagger
from nltk.tokenize import word_tokenize, sent_tokenize

root = os.getcwd()
jar = os.path.join(root, 'stanford-postagger-full-2020-11-17',
                   'stanford-postagger.jar')
model = os.path.join(root, 'stanford-postagger-full-2020-11-17',
                     'models', 'english-left3words-distsim.tagger')
pos_tagger = StanfordPOSTagger(model, jar, encoding='utf8')


def cutoff_values(val):
    if (val > 1):
        return 1
    elif (val < 0):
        return 0
    else:
        return val


def get_phrases(desc_pos):
    grammar = r"""
      NP: {(<DT>?<JJ>*<CD>*<NN|NNP|NNPS|NNS>)+}          # Chunk sequences of DT, JJ, NN
      PP: {<IN><NP>}               # Chunk prepositions followed by NP
      VP: {<VB.*><NP|PP|CLAUSE>+$} # Chunk verbs and their arguments
      CLAUSE: {<NP><VP>}           # Chunk NP, VP
      """
    cp = nltk.RegexpParser(grammar)
    result = cp.parse(desc_pos)
    return result


def run_mean_uniqueWordCount(df, train_data_dic):
    min_val = train_data_dic['mean_unque_word_cnt_min']
    max_val = train_data_dic['mean_unque_word_cnt_max']
    unique_ls = df.Description.map(
        lambda x: len(set(str(x.lower()).split())))
    sentcount_ls = df.Description.map(lambda x: len(sent_tokenize(x)))
    tmp_ls = unique_ls / sentcount_ls
    df['mean_unique_word_count'] = [
        ((x - min_val) / (max_val - min_val)) for x in tmp_ls]
    df['mean_unique_word_count'] = df.mean_unique_word_count.map(
        lambda x: cutoff_values(x))


def run_mean_wordCount(df, train_data_dic):
    min_val = train_data_dic['mean_word_count_min']
    max_val = train_data_dic['mean_word_count_max']
    wordcount_ls = df.Description.str.split().map(lambda x: len(x))
    sentcount_ls = df.Description.map(lambda x: len(sent_tokenize(x)))
    tmp_ls = wordcount_ls / sentcount_ls
    df['mean_word_count'] = [
        ((x - min_val) / (max_val - min_val)) for x in tmp_ls]
    df['mean_word_count'] = df.mean_word_count.map(
        lambda x: cutoff_values(x))


def run_meanWordlen(df, train_data_dic):
    min_val = train_data_dic['mean_word_length_min']
    max_val = train_data_dic['mean_word_length_max']
    tmp_ls = df.Description.map(
        lambda x: np.mean([len(w) for w in str(x).split()]))
    df['mean_word_length'] = [
        ((x - min_val) / (max_val - min_val)) for x in tmp_ls]
    df['mean_word_length'] = df.mean_word_length.map(
        lambda x: cutoff_values(x))


def run_mean_punctuationCount(df, train_data_dic):
    min_val = train_data_dic['mean_pnct_cnt_min']
    max_val = train_data_dic['mean_pnct_cnt_max']
    sentcount_ls = df.Description.map(lambda x: len(sent_tokenize(x)))
    punccount_ls = df.Description.map(lambda x: len(
        [c for c in str(x) if c in string.punctuation]))
    tmp_ls = punccount_ls / sentcount_ls
    df['mean_punctuation_count'] = [
        ((x - min_val) / (max_val - min_val)) for x in tmp_ls]
    df['mean_punctuation_count'] = df.mean_punctuation_count.map(
        lambda x: cutoff_values(x))


def run_meanSentlen(df, train_data_dic):
    min_val = train_data_dic['mean_sent_len_min']
    max_val = train_data_dic['mean_sent_len_max']
    tmp_ls = df.Description.map(lambda x: np.mean(
        [len(sent) for sent in sent_tokenize(x)]))
    df['mean_sent_len'] = [
        ((x - min_val) / (max_val - min_val)) for x in tmp_ls]
    df['mean_sent_len'] = df.mean_sent_len.map(
        lambda x: cutoff_values(x))


def run_mean_phraseCount(df, train_data_dic):
    phrase_ls = df.phrases_ls.map(lambda x: len(x.split(' ')))
    sentcount_ls = df.Description.map(lambda x: len(sent_tokenize(x)))
    tmp_ls = phrase_ls / sentcount_ls
    min_val = train_data_dic['mean_phrase_min']
    max_val = train_data_dic['mean_phrase_max']
    df['mean_phrase_count'] = [
        ((x - min_val) / (max_val - min_val)) for x in tmp_ls]
    df['mean_phrase_count'] = df.mean_phrase_count.map(
        lambda x: cutoff_values(x))


def run_mean_letterCount(df, train_data_dic):
    min_val = train_data_dic['mean_letter_count_min']
    max_val = train_data_dic['mean_letter_count_max']
    lettcount_ls = df.Description.map(
        lambda x: sum(1 for c in str(x) if c.isalpha()))
    sentcount_ls = df.Description.map(lambda x: len(sent_tokenize(x)))
    tmp_ls = lettcount_ls / sentcount_ls
    df['mean_letter_count'] = [
        ((x - min_val) / (max_val - min_val)) for x in tmp_ls]
    df['mean_letter_count'] = df.mean_letter_count.map(
        lambda x: cutoff_values(x))


def run_mean_digitCount(df, train_data_dic):
    min_val = train_data_dic['mean_digit_count_min']
    max_val = train_data_dic['mean_digit_count_max']
    digitcount_ls = df.Description.map(
        lambda x: sum(1 for c in str(x) if c.isdigit()))
    sentcount_ls = df.Description.map(lambda x: len(sent_tokenize(x)))
    tmp_ls = digitcount_ls / sentcount_ls
    df['mean_digit_count'] = [
        ((x - min_val) / (max_val - min_val)) for x in tmp_ls]
    df['mean_digit_count'] = df.mean_digit_count.map(
        lambda x: cutoff_values(x))


def run_mean_whitespaceCount(df, train_data_dic):
    min_val = train_data_dic['mean_whitespace_count_min']
    max_val = train_data_dic['mean_whitespace_count_max']
    whitespace_ls = df.Description.map(
        lambda x: sum(1 for c in str(x) if c.isspace()))
    sentcount_ls = df.Description.map(lambda x: len(sent_tokenize(x)))
    tmp_ls = whitespace_ls / sentcount_ls
    df['mean_whitespace_count'] = [
        ((x - min_val) / (max_val - min_val)) for x in tmp_ls]
    df['mean_whitespace_count'] = df.mean_whitespace_count.map(
        lambda x: cutoff_values(x))


def run_mean_fullyUpperWordsCount(df, train_data_dic):
    min_val = train_data_dic['mean_FullUpper_count_min']
    max_val = train_data_dic['mean_FullUpper_count_max']
    fullupper_ls = df.Description.str.split().map(lambda x: sum(
        1 for c in x if (c.isupper() and c.isalpha() and len(c) > 1)))
    sentcount_ls = df.Description.map(lambda x: len(sent_tokenize(x)))
    tmp_ls = fullupper_ls / sentcount_ls
    df['mean_FullUpper_count'] = [
        ((x - min_val) / (max_val - min_val)) for x in tmp_ls]
    df['mean_FullUpper_count'] = df.mean_FullUpper_count.map(
        lambda x: cutoff_values(x))


def run_mean_fullyLowerWordsCount(df, train_data_dic):
    min_val = train_data_dic['mean_FullLower_count_min']
    max_val = train_data_dic['mean_FullLower_count_max']
    fullupper_ls = df.Description.str.split().map(lambda x: sum(
        1 for c in x if (c.islower() and c.isalpha() and len(c) > 1)))
    sentcount_ls = df.Description.map(lambda x: len(sent_tokenize(x)))
    tmp_ls = fullupper_ls / sentcount_ls
    df['mean_FullLower_count'] = [
        ((x - min_val) / (max_val - min_val)) for x in tmp_ls]
    df['mean_FullLower_count'] = df.mean_FullLower_count.map(
        lambda x: cutoff_values(x))


def run_mean_titleCount(df, train_data_dic):
    min_val = train_data_dic['mean_title_count_min']
    max_val = train_data_dic['mean_title_count_max']
    titlecount_ls = df.Description.str.split().map(lambda x: sum(
        1 for c in x if (c.istitle() and c.isalpha() and len(c) > 1)))
    sentcount_ls = df.Description.map(lambda x: len(sent_tokenize(x)))
    tmp_ls = titlecount_ls / sentcount_ls
    df['mean_title_count'] = [
        ((x - min_val) / (max_val - min_val)) for x in tmp_ls]
    df['mean_title_count'] = df.mean_title_count.map(
        lambda x: cutoff_values(x))


def run_mean_charCount(df, train_data_dic):
    min_val = train_data_dic['mean_char_count_min']
    max_val = train_data_dic['mean_char_count_max']
    charcount_ls = df.Description.map(
        lambda x: sum(len(word) for word in str(x).split(" ")))
    sentcount_ls = df.Description.map(lambda x: len(sent_tokenize(x)))
    tmp_ls = charcount_ls / sentcount_ls
    df['mean_char_count'] = [
        ((x - min_val) / (max_val - min_val)) for x in tmp_ls]
    df['mean_char_count'] = df.mean_char_count.map(
        lambda x: cutoff_values(x))


def phrase_pos_extraction(phrases_tree):
    phrase_pos_ls = []
    for child in phrases_tree:
        if not isinstance(child, Tree):
            phrase_pos_ls.append(child[1])
        else:
            children = str(child)
            phrase_pos_ls.append(children[1: 3])
    return ' '.join([item for item in phrase_pos_ls])


def phrase_extraction(desc_pos):
    phrases_tree = get_phrases(desc_pos)
    phrase_pos_ls = phrase_pos_extraction(phrases_tree)
    return phrase_pos_ls


def convert_FullDesc22POS(desc):
    sentences = sent_tokenize(desc)
    desc_POS = []
    for sent in sentences:
        pos_ls = pos_tagger.tag(word_tokenize(sent))
        for value in pos_ls:
            desc_POS.append(value)
    return desc_POS


def compute_length_features(df, train_data_dic):
    df['FullDesc_POS_ls'] = df.Description.map(
        lambda x: convert_FullDesc22POS(x))
    df['phrases_ls'] = df.FullDesc_POS_ls.map(lambda x: phrase_extraction(x))

    run_mean_uniqueWordCount(df, train_data_dic)
    run_mean_wordCount(df, train_data_dic)
    run_meanWordlen(df, train_data_dic)
    run_mean_punctuationCount(df, train_data_dic)
    run_meanSentlen(df, train_data_dic)
    run_mean_phraseCount(df, train_data_dic)
    run_mean_letterCount(df, train_data_dic)
    run_mean_digitCount(df, train_data_dic)
    run_mean_whitespaceCount(df, train_data_dic)
    run_mean_fullyUpperWordsCount(df, train_data_dic)
    run_mean_fullyLowerWordsCount(df, train_data_dic)
    run_mean_titleCount(df, train_data_dic)
    run_mean_charCount(df, train_data_dic)
