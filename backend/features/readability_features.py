import pandas as pd
from nltk.tokenize import word_tokenize, sent_tokenize
import readability


def cutoff_values(val):
    if (val > 1):
        return 1
    elif (val < 0):
        return 0
    else:
        return val


def compute_Kincaid_score(df, read_val, train_data_dic):
    min_val = train_data_dic['Kincaid_min']
    max_val = train_data_dic['Kincaid_max']
    tmp_ls_val = [item['readability grades']['Kincaid'] for item in read_val]
    if ((max_val - min_val) != 0):
        df['Kincaid'] = [((x - min_val) / (max_val - min_val))
                         for x in tmp_ls_val]
        df['Kincaid'] = df.Kincaid.map(lambda x: cutoff_values(x))
    else:
        df['Kincaid'] = [0] * len(df)


def compute_ARI_score(df, read_val, train_data_dic):
    min_val = train_data_dic['ARI_min']
    max_val = train_data_dic['ARI_max']
    tmp_ls_val = [item['readability grades']['ARI'] for item in read_val]
    if ((max_val - min_val) != 0):
        df['ARI'] = [((x - min_val) / (max_val - min_val))
                     for x in tmp_ls_val]
        df['ARI'] = df.ARI.map(lambda x: cutoff_values(x))
    else:
        df['ARI'] = [0] * len(df)


def compute_ColemanLiau_score(df, read_val, train_data_dic):
    min_val = train_data_dic['Coleman-Liau_min']
    max_val = train_data_dic['Coleman-Liau_max']
    tmp_ls_val = [item['readability grades']['Coleman-Liau']
                  for item in read_val]
    if ((max_val - min_val) != 0):
        df['Coleman_Liau'] = [
            ((x - min_val) / (max_val - min_val)) for x in tmp_ls_val]
        df['Coleman_Liau'] = df.Coleman_Liau.map(
            lambda x: cutoff_values(x))
    else:
        df['Coleman_Liau'] = [0] * len(df)


def compute_FleschReadingEase_score(df, read_val, train_data_dic):
    min_val = train_data_dic['FleschReadingEase_min']
    max_val = train_data_dic['FleschReadingEase_max']
    tmp_ls_val = [item['readability grades']['FleschReadingEase']
                  for item in read_val]
    if ((max_val - min_val) != 0):
        df['FleschReadingEase'] = [
            ((x - min_val) / (max_val - min_val)) for x in tmp_ls_val]
        df['FleschReadingEase'] = df.FleschReadingEase.map(
            lambda x: cutoff_values(x))
    else:
        df['FleschReadingEase'] = [0] * len(df)


def compute_GunningFogIndex_score(df, read_val, train_data_dic):
    min_val = train_data_dic['GunningFogIndex_min']
    max_val = train_data_dic['GunningFogIndex_max']
    tmp_ls_val = [item['readability grades']['GunningFogIndex']
                  for item in read_val]
    if ((max_val - min_val) != 0):
        df['GunningFogIndex'] = [
            ((x - min_val) / (max_val - min_val)) for x in tmp_ls_val]
        df['GunningFogIndex'] = df.GunningFogIndex.map(
            lambda x: cutoff_values(x))
    else:
        df['GunningFogIndex'] = [0] * len(df)


def compute_LIX_score(df, read_val, train_data_dic):
    min_val = train_data_dic['LIX_min']
    max_val = train_data_dic['LIX_max']
    tmp_ls_val = [item['readability grades']['LIX'] for item in read_val]
    if ((max_val - min_val) != 0):
        df['LIX'] = [((x - min_val) / (max_val - min_val))
                     for x in tmp_ls_val]
        df['LIX'] = df.LIX.map(lambda x: cutoff_values(x))
    else:
        df['LIX'] = [0] * len(df)


def compute_SMOGIndex_score(df, read_val, train_data_dic):
    min_val = train_data_dic['SMOGIndex_min']
    max_val = train_data_dic['SMOGIndex_max']
    tmp_ls_val = [item['readability grades']['SMOGIndex'] for item in read_val]
    if ((max_val - min_val) != 0):
        df['SMOGIndex'] = [
            ((x - min_val) / (max_val - min_val)) for x in tmp_ls_val]
        df['SMOGIndex'] = df.SMOGIndex.map(
            lambda x: cutoff_values(x))
    else:
        df['SMOGIndex'] = [0] * len(df)


def compute_RIX_score(df, read_val, train_data_dic):
    min_val = train_data_dic['RIX_min']
    max_val = train_data_dic['RIX_max']
    tmp_ls_val = [item['readability grades']['RIX'] for item in read_val]
    if ((max_val - min_val) != 0):
        df['RIX'] = [((x - min_val) / (max_val - min_val))
                     for x in tmp_ls_val]
        df['RIX'] = df.RIX.map(lambda x: cutoff_values(x))
    else:
        df['RIX'] = [0] * len(df)


def compute_DaleChallIndex_score(df, read_val, train_data_dic):
    min_val = train_data_dic['DaleChallIndex_min']
    max_val = train_data_dic['DaleChallIndex_max']
    tmp_ls_val = [item['readability grades']['DaleChallIndex']
                  for item in read_val]
    if ((max_val - min_val) != 0):
        df['DaleChallIndex'] = [
            ((x - min_val) / (max_val - min_val)) for x in tmp_ls_val]
        df['DaleChallIndex'] = df.DaleChallIndex.map(
            lambda x: cutoff_values(x))
    else:
        df['DaleChallIndex'] = [0] * len(df)


def compute_mean_complex_words(df, read_val, train_data_dic):
    min_val = train_data_dic['mean_complex_words_min']
    max_val = train_data_dic['mean_complex_words_max']
    complex_words = [item['sentence info']['complex_words']
                     for item in read_val]
    if ((max_val - min_val) != 0):
        sentcount_ls = df.Description.map(
            lambda x: len(sent_tokenize(x)))
        tmp_ls_val = complex_words / sentcount_ls
        df['mean_complex_words'] = [
            ((x - min_val) / (max_val - min_val)) for x in tmp_ls_val]
        df['mean_complex_words'] = df.mean_complex_words.map(
            lambda x: cutoff_values(x))
    else:
        df['mean_complex_words'] = [0] * len(df)


def compute_mean_complex_dc_words(df, read_val, train_data_dic):
    min_val = train_data_dic['mean_complex_words_dc_min']
    max_val = train_data_dic['mean_complex_words_dc_max']
    complex_words_dc = [item['sentence info']
                        ['complex_words_dc'] for item in read_val]
    if ((max_val - min_val) != 0):
        sentcount_ls = df.Description.map(
            lambda x: len(sent_tokenize(x)))
        tmp_ls_val = complex_words_dc / sentcount_ls
        df['mean_complex_words_dc'] = [
            ((x - min_val) / (max_val - min_val)) for x in tmp_ls_val]
        df['mean_complex_words_dc'] = df.mean_complex_words_dc.map(
            lambda x: cutoff_values(x))
    else:
        df['mean_complex_words_dc'] = [0] * len(df)


def compute_readability_features(df, train_data_dic):
    desc_list_val = df.Description.map(lambda x: '\n '.join(sent_tokenize(x)))
    read_val = [readability.getmeasures(
        text, lang='en') for text in desc_list_val]

    compute_Kincaid_score(df, read_val, train_data_dic)
    compute_ARI_score(df, read_val, train_data_dic)
    compute_ColemanLiau_score(df, read_val, train_data_dic)
    compute_FleschReadingEase_score(df, read_val, train_data_dic)
    compute_GunningFogIndex_score(df, read_val, train_data_dic)
    compute_LIX_score(df, read_val, train_data_dic)
    compute_SMOGIndex_score(df, read_val, train_data_dic)
    compute_RIX_score(df, read_val, train_data_dic)
    compute_DaleChallIndex_score(df, read_val, train_data_dic)
    compute_mean_complex_words(df, read_val, train_data_dic)
    compute_mean_complex_dc_words(df, read_val, train_data_dic)
