import os
import pickle
import pandas as pd
root = os.getcwd()


def get_training_data():
    df_train = pd.read_excel(os.path.join(
        root, 'data', 'New_Averaged_Complete_Train_Set.xlsx'))

    return df_train


def get_trained_models():
    models = {'state1_new': {}, 'state_3': {}, 'state_4': {}, 'state_5': {
    }, 'state_6': {}, 'state_7': {}, 'state_8': {}, 'state_9': {}}

    for state in ['state1_new', 'state_3', 'state_4', 'state_5', 'state_6', 'state_7', 'state_8', 'state_9']:
        with open(os.path.join(root, 'models', state, 'best.pkl'), 'rb') as fb:
            models[state]['best'] = pickle.load(fb)

    for state in ['state1_new', 'state_3', 'state_4', 'state_5', 'state_6', 'state_7', 'state_8', 'state_9']:
        with open(os.path.join(root, 'models', state, 'SecondBest.pkl'), 'rb') as fb:
            models[state]['secondBest'] = pickle.load(fb)

    for state in ['state1_new', 'state_3', 'state_4', 'state_5', 'state_6', 'state_7', 'state_8', 'state_9']:
        with open(os.path.join(root, 'models', state, 'ThirdBest.pkl'), 'rb') as fb:
            models[state]['thirdBest'] = pickle.load(fb)

    return models


def get_trained_selectors():
    selectors = {'state1_new': {}, 'state_3': {}, 'state_4': {}, 'state_5': {
    }, 'state_6': {}, 'state_7': {}, 'state_8': {}, 'state_9': {}}

    for state in ['state1_new', 'state_3', 'state_4', 'state_5', 'state_6', 'state_7', 'state_8', 'state_9']:
        with open(os.path.join(root, 'New Feature Selector', state, 'best.pkl'), 'rb') as fb:
            selectors[state]['best'] = pickle.load(fb)

    for state in ['state1_new', 'state_3', 'state_4', 'state_5', 'state_6', 'state_7', 'state_8', 'state_9']:
        with open(os.path.join(root, 'New Feature Selector', state, 'SecondBest.pkl'), 'rb') as fb:
            selectors[state]['secondBest'] = pickle.load(fb)

    for state in ['state1_new', 'state_3', 'state_4', 'state_5', 'state_6', 'state_7', 'state_8', 'state_9']:
        with open(os.path.join(root, 'New Feature Selector', state, 'ThirdBest.pkl'), 'rb') as fb:
            selectors[state]['thirdBest'] = pickle.load(fb)

    return selectors


def get_vectorizers():
    vectorizers = {}

    with open(os.path.join(root, 'Vectorizers', 'tf_idf_vectorizer.pkl'), 'rb') as fb:
        vectorizers['tf_idf_vectorizer'] = pickle.load(fb)
    with open(os.path.join(root, 'Vectorizers', 'pos_vectorizer.pkl'), 'rb') as fb:
        vectorizers['pos_vectorizer'] = pickle.load(fb)
    with open(os.path.join(root, 'Vectorizers', 'phrases_vectorizer.pkl'), 'rb') as fb:
        vectorizers['phrases_vectorizer'] = pickle.load(fb)
    with open(os.path.join(root, 'Vectorizers', 'gram_vectorizer.pkl'), 'rb') as fb:
        vectorizers['gram_vectorizer'] = pickle.load(fb)
    with open(os.path.join(root, 'Vectorizers', 'functional_vectorizer.pkl'), 'rb') as fb:
        vectorizers['functional_vectorizer'] = pickle.load(fb)
    with open(os.path.join(root, 'Vectorizers', 'feature_vectorizer.pkl'), 'rb') as fb:
        vectorizers['feature_vectorizer'] = pickle.load(fb)

    return vectorizers


def get_features_extreme_values():
    train_data_dic = {'phrases_ls_min': 1, 'phrases_ls_max': 119,
                      'mean_phrase_min': 0.5, 'mean_phrase_max': 91,
                      'open_POS_min': 4, 'open_POS_max': 81,
                      'close_POS_min': 0, 'close_POS_max': 49,
                      'POS_VB_min': 0, 'POS_VB_max': 29,
                      'POS_NN_min': 2, 'POS_NN_max': 33,
                      'POS_jj_min': 0, 'POS_jj_max': 18,
                      'POS_w_min': 0, 'POS_w_max': 4,
                      'POS_fw_min': 0, 'POS_fw_max': 2,
                      'POS_ls_min': 0, 'POS_ls_max': 2,
                      'polarity_min': -0.8, 'polarity_max': 1,
                      'subjectivity_min': 0, 'subjectivity_max': 1,
                      'text_len_min': 24, 'text_len_max': 731,
                      'unque_word_cnt_min': 3, 'unque_word_cnt_max': 92,
                      'mean_unque_word_cnt_min': 1.5, 'mean_unque_word_cnt_max': 78,
                      'word_count_min': 4, 'word_count_max': 129,
                      'mean_word_count_min': 2, 'mean_word_count_max': 117,
                      'mean_word_length_min': 3, 'mean_word_length_max': 11.5,
                      'punctuation_count_min': 0, 'punctuation_count_max': 83,
                      'mean_pnct_cnt_min': 0, 'mean_pnct_cnt_max': 36.5,
                      'sent_count_min': 1, 'sent_count_max': 9,
                      'mean_sent_len_min': 11.5, 'mean_sent_len_max': 713,
                      'letter_count_min': 17, 'letter_count_max': 575,
                      'mean_letter_count_min': 8.333333333333334, 'mean_letter_count_max': 575,
                      'digit_count_min': 0, 'digit_count_max': 24,
                      'mean_digit_count_min': 0, 'mean_digit_count_max': 14,
                      'whitespace_count_min': 3, 'whitespace_count_max': 128,
                      'mean_whitespace_count_min': 1.5, 'mean_whitespace_count_max': 116,
                      'FullUpper_count_min': 0, 'FullUpper_count_max': 14,
                      'mean_FullUpper_count_min': 0, 'mean_FullUpper_count_max': 5,
                      'FullLower_count_min': 0, 'FullLower_count_max': 93,
                      'mean_FullLower_count_min': 0, 'mean_FullLower_count_max': 93,
                      'title_count_min': 0, 'title_count_max': 21,
                      'mean_title_count_min': 0, 'mean_title_count_max': 10.5,
                      'char_count_min': 21, 'char_count_max': 603,
                      'mean_char_count_min': 10.333333333333334, 'mean_char_count_max': 597,
                      'Kincaid_min': -9.047261904761905, 'Kincaid_max': 47.776302521008404,
                      'ARI_min': -9.885, 'ARI_max': 60.907563025210074,
                      'Coleman-Liau_min': -11.002814941176469, 'Coleman-Liau_max': 29.85218838461539,
                      'FleschReadingEase_min': -61.599999999999994, 'FleschReadingEase_max': 169.27767857142857,
                      'GunningFogIndex_min': 0.8, 'GunningFogIndex_max': 54.65882352941177,
                      'LIX_min': 2, 'LIX_max': 146.7310924369748,
                      'SMOGIndex_min': 3, 'SMOGIndex_max': 28.099800796022265,
                      'RIX_min': 0, 'RIX_max': 33,
                      'DaleChallIndex_min': 0, 'DaleChallIndex_max': 19.8729,
                      'complex_words_min': 0, 'complex_words_max': 21,
                      'complex_words_dc_min': 0, 'complex_words_dc_max': 43,
                      'pos_score_min': 0, 'pos_score_max': 0.625,
                      'neg_score_min': 0, 'neg_score_max': 0.625,
                      'obj_score_min': 0.125, 'obj_score_max': 1,
                      'tags_ORG_min': 0, 'tags_ORG_max': 4,
                      'tags_ORDINAL_min': 0, 'tags_ORDINAL_max': 3,
                      'tags_LOC_min': 0, 'tags_LOC_max': 1,
                      'tags_LAW_min': 0, 'tags_LAW_max': 1,
                      'tags_TIME_min': 0, 'tags_TIME_max': 4,
                      'tags_EVENT_min': 0, 'tags_EVENT_max': 2,
                      'tags_PRODUCT_min': 0, 'tags_PRODUCT_max': 2,
                      'tags_CARDINAL_min': 0, 'tags_CARDINAL_max': 5,
                      'tags_MONEY_min': 0, 'tags_MONEY_max': 4,
                      'tags_GPE_min': 0, 'tags_GPE_max': 6,
                      'tags_QUANTITY_min': 0, 'tags_QUANTITY_max': 1,
                      'tags_PERCENT_min': 0, 'tags_PERCENT_max': 2,
                      'tags_NORP_min': 0, 'tags_NORP_max': 3,
                      'tags_WORK_OF_ART_min': 0, 'tags_WORK_OF_ART_max': 2,
                      'tags_LANGUAGE_min': 0, 'tags_LANGUAGE_max': 3,
                      'tags_DATE_min': 0, 'tags_DATE_max': 3,
                      'tags_PERSON_min': 0, 'tags_PERSON_max': 3,
                      'tags_FAC_min': 0, 'tags_FAC_max': 1,
                      'mean_open_POS_min': 1.666666667, 'mean_open_POS_max': 33.5,
                      'mean_close_POS_min': 0, 'mean_close_POS_max': 24.5,
                      'mean_POS_VB_min': 0, 'mean_POS_VB_max': 10,
                      'mean_POS_NN_min': 0.666666667, 'mean_POS_NN_max': 16,
                      'mean_POS_JJ_min': 0, 'mean_POS_JJ_max': 9,
                      'mean_POS_W_min': 0, 'mean_POS_W_max': 4,
                      'mean_POS_FW_min': 0, 'mean_POS_FW_max': 1,
                      'mean_POS_LS_min': 0, 'mean_POS_LS_max': 1,
                      'mean_complex_words_min': 0, 'mean_complex_words_max': 10.5,
                      'mean_complex_words_dc_min': 0, 'mean_complex_words_dc_max': 19,
                      'mean_tags_ORG_min': 0, 'mean_tags_ORG_max': 3,
                      'mean_tags_ORDINAL_min': 0, 'mean_tags_ORDINAL_max': 1,
                      'mean_tags_LOC_min': 0, 'mean_tags_LOC_max': 0.5,
                      'mean_tags_LAW_min': 0, 'mean_tags_LAW_max': 0.5,
                      'mean_tags_TIME_min': 0, 'mean_tags_TIME_max': 2,
                      'mean_tags_EVENT_min': 0, 'mean_tags_EVENT_max': 2,
                      'mean_tags_PRODUCT_min': 0, 'mean_tags_PRODUCT_max': 1,
                      'mean_tags_CARDINAL_min': 0, 'mean_tags_CARDINAL_max': 2,
                      'mean_tags_MONEY_min': 0, 'mean_tags_MONEY_max': 1.5,
                      'mean_tags_GPE_min': 0, 'mean_tags_GPE_max': 3,
                      'mean_tags_QUANTITY_min': 0, 'mean_tags_QUANTITY_max': 0.5,
                      'mean_tags_PERCENT_min': 0, 'mean_tags_PERCENT_max': 0.5,
                      'mean_tags_NORP_min': 0, 'mean_tags_NORP_max': 1,
                      'mean_tags_WORK_OF_ART_min': 0, 'mean_tags_WORK_OF_ART_max': 1,
                      'mean_tags_LANGUAGE_min': 0, 'mean_tags_LANGUAGE_max': 1.5,
                      'mean_tags_DATE_min': 0, 'mean_tags_DATE_max': 1.5,
                      'mean_tags_PERSON_min': 0, 'mean_tags_PERSON_max': 2,
                      'mean_tags_FAC_min': 0, 'mean_tags_FAC_max': 0.5
                      }

    return train_data_dic
