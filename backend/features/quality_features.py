import os
import re
import collections
import pandas as pd
from nltk.tag import StanfordPOSTagger
from nltk.tokenize import word_tokenize, sent_tokenize
import spacy
ner = spacy.load('en_core_web_sm')

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


def mask_giventime(tokens):
    # date and time
    tokens = re.sub(r'\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d',
                    'givendatetime', tokens, re.DOTALL).strip()
    # time of audios r'(\[)?\d\d:\d\d mmss(\])?'
    tokens = re.sub(r'(\[)?\d\d:\d\d mmss(\])?',
                    'giventime', tokens, re.DOTALL).strip()
    # given time
    tokens = re.sub(r'(\()?audio\slength(\:)?(\s)?((\d+\s(hour(\w*.)?|min(\w*.)?|sec(\w*.)?)+)?)+(\()?',
                    'giventime', tokens, re.DOTALL).strip()
    tokens = re.sub(r'(\()?(approx(\w*.)?(\s)?|about(\s)?|around(\s)?)?(\d+(\.)?\d+|\w*)?(\s*-\s*\d*)?(\s*~\s*\d*)?(\s)?(to\s\d*)?(\s)?(to\s\w*)?\s(hour(\w*.)?|min(\w*.)?|sec(\w*.)?)(\s)?(approx(\w*.)?)?(\))?(\s)?(to\s\w+)?', 'giventime ', tokens, re.DOTALL).strip()
    return tokens


def mask_link(tokens):
    #tokens= re.sub(r'\'(the(\s)?|a(\s)?)?given(\s)?(the(\s)?|a(\s)?)?(\s)?link\'', 'link',tokens, re.DOTALL).strip()
    tokens = re.sub(r'[uU][Rr][Ll]|[Ll][Ii][nN][Kk]',
                    'LINKK', tokens, re.DOTALL).strip()
    tokens = re.sub(r'(www.)?\w+\.(com|info)+',
                    'LINKK', tokens, re.DOTALL).strip()
    tokens = re.sub(
        r'(\()?http(s)?(://){1,1}(\w*-*_*\d*.*/*)?.(org|com|html|biz|in|ca|net|gl|hu){1,1}((/*\w*\d*-*_*)*)?(/\))?', 'LINKK', tokens, re.DOTALL).strip()
    return tokens


def mask_website(tokens):
    # web page unifing
    #tokens= re.sub(r'([wW]eb\s)?([sS]ite(s)?(\s)+|[pP]age(s)?(\s)+|[lL]ink(\s)+|[aA]pplication(\s)+|[aA]pp(\.)?(\s)+|[Uu][Rr][lL](\s)+)', 'website ',tokens, re.DOTALL).strip()
    tokens = re.sub(r'([wW]eb\s)?([sS]ite(s)?(\s)+|[wW][Ee][bB][sS][Ii][Tt][eE](s)?|[pP]age(s)?(\s)+)',
                    'WEBSSITE ', tokens, re.DOTALL).strip()
    tokens = re.sub(r'\s[sS]ite(s)?\s', ' WEBSSITE ',
                    tokens, re.DOTALL).strip()
    tokens = re.sub(r'[wW]ebWEBSSITE', 'WEBSSITE ', tokens, re.DOTALL).strip()
    #tokens= re.sub(r'website\s[aA]ddress(es)?', 'website',tokens, re.DOTALL).strip()
    tokens = re.sub(r'[wW]eb\s', 'WEBSSITE ', tokens, re.DOTALL).strip()
    tokens = re.sub(r'[pP]age(\,|\.)?\s', 'WEBSSITE ',
                    tokens, re.DOTALL).strip()
    return tokens


def mask_reward(tokens):
    # given reward bonus
    tokens = re.sub(r'(\()?(\s)?earn\sup\sto\s\$\d+(\.\d+)?\s\+\s(\d+\%|\$\d+(\.\d+)?)\sbonus\s=\s\$(\d+\.\d+)?\smax(\))?',
                    'REWARDD', tokens, re.DOTALL).strip()
    tokens = re.sub(r'(\()?avg\srwrd\+bns(\:)?\s\$\d*.\d*(\))?',
                    'REWARDD', tokens, re.DOTALL).strip()
    tokens = re.sub(r'\$\d*(\.*\d+)?(\s)?(\+)?(/)?(BONUS|hour|hr)?(!*)?',
                    'REWARDD', tokens, re.DOTALL).strip()
    # given premium
    tokens = re.sub(r'(\()?\d+\%\spremium(\))?',
                    'REWARDD', tokens, re.DOTALL).strip()
    return tokens


def mask_socialmedia(tokens):
    # social media types
    tokens = re.sub(r'\s[fF][bB]\s', 'SOCIALMEDIAA', tokens, re.DOTALL).strip()
    tokens = re.sub(r'[Tt]witter|[Ll]inkedIn|[Ff]ace[bB]ook|[Gg]ithub|[Ii]nstagram|[Ss]ocial\s[Mm]edia|[Ss]ocial\s[nN]etwork(ing)?',
                    'SOCIALMEDIAA', tokens, re.DOTALL).strip()
    tokens = re.sub(r'socialmedia\s+([Aa]ccount(s)?|[Pp]rofile(s)?|[pP]ost(s)?|[Ww]ebsite(s)?|[Ii]mage(s)?|[Cc]omment(s)?|[wW]all(s)?|[bB]log(s)?|[sS]tatus(es)?|[aA]pp(s)?|[lL]ike(s)?|[vV]ote(s)?)+',
                    'SOCIALMEDIAA', tokens, re.DOTALL).strip()
    return tokens


def mask_image(tokens):
    tokens = re.sub(r'([pP]hoto(s)?|[pP]icture(s)?|[iI]mage(s)?)',
                    'IMAGEE', tokens, re.DOTALL).strip()
    return tokens


def convert_FullDesc2POS(desc):
    sentences = sent_tokenize(desc)
    desc_POS = []
    for sent in sentences:
        pos_ls = [str(item[0]+'/'+item[1])
                  for item in pos_tagger.tag(word_tokenize(sent))]
        for value in pos_ls:
            desc_POS.append(value)
    return ' '.join(desc_POS)


def general_tag_counting_openpos(desc):
    pos_ls = []
    for word in word_tokenize(desc):
        # print(word)
        if len(word) > 3:
            try:
                ls = word.split('/')
                pos_ls.append(ls[1])
            except:
                pass
    open_pos = sum(1 for tag in pos_ls if tag in ['MD', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ',
                                                  'NN', 'NNS', 'NNP', 'NNPS', 'RB', 'RBR', 'RBS', 'JJ', 'JJR', 'JJS', 'UH', 'WDT', 'WP', 'WP$', 'WRB'])
    return open_pos


def general_tag_counting_closepos(desc):
    pos_ls = []
    for word in word_tokenize(desc):
        # print(word)
        if len(word) > 3:
            try:
                ls = word.split('/')
                pos_ls.append(ls[1])
            except:
                pass
    close_pos = sum(1 for tag in pos_ls if tag in [
                    'IN', 'PRP', 'PRP$', 'RP', 'CC', 'DT', 'CD', 'TO'])
    return close_pos


def general_tag_counting_posvb(desc):
    pos_ls = []
    for word in word_tokenize(desc):
        # print(word)
        if len(word) > 3:
            try:
                ls = word.split('/')
                pos_ls.append(ls[1])
            except:
                pass
    pos_vb = sum(1 for tag in pos_ls if tag in [
                 'MD', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ'])
    return pos_vb


def general_tag_counting_posnn(desc):
    pos_ls = []
    for word in word_tokenize(desc):
        # print(word)
        if len(word) > 3:
            try:
                ls = word.split('/')
                pos_ls.append(ls[1])
            except:
                pass
    pos_nn = sum(1 for tag in pos_ls if tag in ['NN', 'NNS', 'NNP', 'NNPS'])
    return pos_nn


def general_tag_counting_posjj(desc):
    pos_ls = []
    for word in word_tokenize(desc):
        # print(word)
        if len(word) > 3:
            try:
                ls = word.split('/')
                pos_ls.append(ls[1])
            except:
                pass
    pos_jj = sum(1 for tag in pos_ls if tag in ['JJ', 'JJR', 'JJS', 'RB'])
    return pos_jj


def general_tag_counting_posw(desc):
    pos_ls = []
    for word in word_tokenize(desc):
        # print(word)
        if len(word) > 3:
            try:
                ls = word.split('/')
                pos_ls.append(ls[1])
            except:
                pass
    pos_w = sum(1 for tag in pos_ls if tag in ['WDT', 'WP', 'WP$', 'WRB'])
    return pos_w


def general_tag_counting_posfw(desc):
    pos_ls = []
    for word in word_tokenize(desc):
        # print(word)
        if len(word) > 3:
            try:
                ls = word.split('/')
                pos_ls.append(ls[1])
            except:
                pass
    pos_fw = sum(1 for tag in pos_ls if tag in ['FW'])
    return pos_fw


def general_tag_counting_posls(desc):
    pos_ls = []
    for word in word_tokenize(desc):
        # print(word)
        if len(word) > 3:
            try:
                ls = word.split('/')
                pos_ls.append(ls[1])
            except:
                pass
    pos_ls = sum(1 for tag in pos_ls if tag in ['LS'])
    return pos_ls


def normalize_pos_values(val_ls, min_val, max_val):
    return [((x - min_val) / (max_val - min_val)) for x in val_ls]


def compute_mean_POS_features(df, train_data_dic):
    sentcount_ls = df.Description.map(lambda x: len(sent_tokenize(x)))

    open_pos = df.FullDesc_POS.map(lambda x: general_tag_counting_openpos(x))
    tmp_ls = open_pos / sentcount_ls
    min_val = train_data_dic['mean_open_POS_min']
    max_val = train_data_dic['mean_open_POS_max']
    df['mean_open_POS'] = normalize_pos_values(tmp_ls, min_val, max_val)
    df['mean_open_POS'] = df.mean_open_POS.map(lambda x: cutoff_values(x))

    close_pos = df.FullDesc_POS.map(lambda x: general_tag_counting_closepos(x))
    tmp_ls = close_pos / sentcount_ls
    min_val = train_data_dic['mean_close_POS_min']
    max_val = train_data_dic['mean_close_POS_max']
    df['mean_close_POS'] = normalize_pos_values(tmp_ls, min_val, max_val)
    df['mean_close_POS'] = df.mean_close_POS.map(lambda x: cutoff_values(x))

    pos_vb = df.FullDesc_POS.map(lambda x: general_tag_counting_posvb(x))
    tmp_ls = pos_vb / sentcount_ls
    min_val = train_data_dic['mean_POS_VB_min']
    max_val = train_data_dic['mean_POS_VB_max']
    df['mean_POS_VB'] = normalize_pos_values(tmp_ls, min_val, max_val)
    df['mean_POS_VB'] = df.mean_POS_VB.map(lambda x: cutoff_values(x))

    pos_nn = df.FullDesc_POS.map(lambda x: general_tag_counting_posnn(x))
    tmp_ls = pos_nn / sentcount_ls
    min_val = train_data_dic['mean_POS_NN_min']
    max_val = train_data_dic['mean_POS_NN_max']
    df['mean_POS_NN'] = normalize_pos_values(tmp_ls, min_val, max_val)
    df['mean_POS_NN'] = df.mean_POS_NN.map(lambda x: cutoff_values(x))

    pos_jj = df.FullDesc_POS.map(lambda x: general_tag_counting_posjj(x))
    tmp_ls = pos_jj / sentcount_ls
    min_val = train_data_dic['mean_POS_JJ_min']
    max_val = train_data_dic['mean_POS_JJ_max']
    df['mean_POS_JJ'] = normalize_pos_values(tmp_ls, min_val, max_val)
    df['mean_POS_JJ'] = df.mean_POS_JJ.map(lambda x: cutoff_values(x))

    pos_w = df.FullDesc_POS.map(lambda x: general_tag_counting_posw(x))
    tmp_ls = pos_w / sentcount_ls
    min_val = train_data_dic['mean_POS_W_min']
    max_val = train_data_dic['mean_POS_W_max']
    df['mean_POS_W'] = normalize_pos_values(tmp_ls, min_val, max_val)
    df['mean_POS_W'] = df.mean_POS_W.map(lambda x: cutoff_values(x))

    pos_fw = df.FullDesc_POS.map(lambda x: general_tag_counting_posfw(x))
    tmp_ls = pos_fw / sentcount_ls
    min_val = train_data_dic['mean_POS_FW_min']
    max_val = train_data_dic['mean_POS_FW_max']
    df['mean_POS_FW'] = normalize_pos_values(tmp_ls, min_val, max_val)
    df['mean_POS_FW'] = df.mean_POS_FW.map(lambda x: cutoff_values(x))

    pos_ls = df.FullDesc_POS.map(lambda x: general_tag_counting_posls(x))
    tmp_ls = pos_ls / sentcount_ls
    min_val = train_data_dic['mean_POS_LS_min']
    max_val = train_data_dic['mean_POS_LS_max']
    df['mean_POS_LS'] = normalize_pos_values(tmp_ls, min_val, max_val)
    df['mean_POS_LS'] = df.mean_POS_LS.map(lambda x: cutoff_values(x))


def run_tag_spacy_dftest(df):
    # tag text and exctract tags into a list
    df["tags"] = df["Description"].apply(lambda x: [(tag.text, tag.label_)
                                                    for tag in ner(x).ents])
    # utils function to count the element of a list

    def utils_lst_count_dftask(lst):
        dic_counter = collections.Counter()
        for x in lst:
            dic_counter[x] += 1
        dic_counter = collections.OrderedDict(
            sorted(dic_counter.items(),
                   key=lambda x: x[1], reverse=True))
        lst_count = [{key: value} for key, value in dic_counter.items()]
        return lst_count

    # count tags
    df["tags"] = df["tags"].apply(lambda x: utils_lst_count_dftask(x))

    # utils function create new column for each tag category
    def utils_ner_features_dftask(lst_dics_tuples, tag):
        if len(lst_dics_tuples) > 0:
            tag_type = []
            for dic_tuples in lst_dics_tuples:
                for tuple in dic_tuples:
                    type, n = tuple[1], dic_tuples[tuple]
                    tag_type = tag_type + [type]*n
                    dic_counter = collections.Counter()
                    for x in tag_type:
                        dic_counter[x] += 1
            return dic_counter[tag]
        else:
            return 0

    # extract features
    tags_set = []
    for lst in df["tags"].tolist():
        for dic in lst:
            for k in dic.keys():
                tags_set.append(k[1])
    tags_set = list(set(tags_set))
    for feature in tags_set:
        df["tags_"+feature] = df["tags"].apply(lambda x:
                                               utils_ner_features_dftask(x, feature))


def normalize_tag_features(df, train_data_dic):
    tags_task_ls = df.columns
    sentcount_ls = df.Description.map(lambda x: len(sent_tokenize(x)))

    if ('tags_ORG' in tags_task_ls):
        tmp_ls = df['tags_ORG'] / sentcount_ls
        min_val = train_data_dic['mean_tags_ORG_min']
        max_val = train_data_dic['mean_tags_ORG_max']
        df['mean_tags_ORG'] = [
            ((x - min_val) / (max_val - min_val)) for x in tmp_ls]
        df['mean_tags_ORG'] = df.mean_tags_ORG.map(lambda x: cutoff_values(x))

        tmp_ls = df['tags_ORG']
        min_val = train_data_dic['tags_ORG_min']
        max_val = train_data_dic['tags_ORG_max']
        df['tags_ORG'] = [((x - min_val) / (max_val - min_val))
                          for x in tmp_ls]
        df['tags_ORG'] = df.tags_ORG.map(lambda x: cutoff_values(x))
    else:
        df['mean_tags_ORG'] = [0] * len(df)
        df['tags_ORG'] = [0] * len(df)

    if ('tags_ORDINAL' in tags_task_ls):
        tmp_ls = df['tags_ORDINAL'] / sentcount_ls
        min_val = train_data_dic['mean_tags_ORDINAL_min']
        max_val = train_data_dic['mean_tags_ORDINAL_max']
        df['mean_tags_ORDINAL'] = [
            ((x - min_val) / (max_val - min_val)) for x in tmp_ls]
        df['mean_tags_ORDINAL'] = df.mean_tags_ORDINAL.map(
            lambda x: cutoff_values(x))

        tmp_ls = df['tags_ORDINAL']
        min_val = train_data_dic['tags_ORDINAL_min']
        max_val = train_data_dic['tags_ORDINAL_max']
        df['tags_ORDINAL'] = [((x - min_val) / (max_val - min_val))
                              for x in tmp_ls]
        df['tags_ORDINAL'] = df.tags_ORDINAL.map(lambda x: cutoff_values(x))
    else:
        df['mean_tags_ORDINAL'] = [0] * len(df)
        df['tags_ORDINAL'] = [0] * len(df)

    if ('tags_LOC' in tags_task_ls):
        tmp_ls = df['tags_LOC'] / sentcount_ls
        min_val = train_data_dic['mean_tags_LOC_min']
        max_val = train_data_dic['mean_tags_LOC_max']
        df['mean_tags_LOC'] = [
            ((x - min_val) / (max_val - min_val)) for x in tmp_ls]
        df['mean_tags_LOC'] = df.mean_tags_LOC.map(lambda x: cutoff_values(x))

        tmp_ls = df['tags_LOC']
        min_val = train_data_dic['tags_LOC_min']
        max_val = train_data_dic['tags_LOC_max']
        df['tags_LOC'] = [((x - min_val) / (max_val - min_val))
                          for x in tmp_ls]
        df['tags_LOC'] = df.tags_LOC.map(lambda x: cutoff_values(x))
    else:
        df['mean_tags_LOC'] = [0] * len(df)
        df['tags_LOC'] = [0] * len(df)

    if ('tags_LAW' in tags_task_ls):
        tmp_ls = df['tags_LAW'] / sentcount_ls
        min_val = train_data_dic['mean_tags_LAW_min']
        max_val = train_data_dic['mean_tags_LAW_max']
        df['mean_tags_LAW'] = [
            ((x - min_val) / (max_val - min_val)) for x in tmp_ls]
        df['mean_tags_LAW'] = df.mean_tags_LAW.map(lambda x: cutoff_values(x))

        tmp_ls = df['tags_LAW']
        min_val = train_data_dic['tags_LAW_min']
        max_val = train_data_dic['tags_LAW_max']
        df['tags_LAW'] = [((x - min_val) / (max_val - min_val))
                          for x in tmp_ls]
        df['tags_LAW'] = df.tags_LAW.map(lambda x: cutoff_values(x))
    else:
        df['mean_tags_LAW'] = [0] * len(df)
        df['tags_LAW'] = [0] * len(df)

    if ('tags_TIME' in tags_task_ls):
        tmp_ls = df['tags_TIME'] / sentcount_ls
        min_val = train_data_dic['mean_tags_TIME_min']
        max_val = train_data_dic['mean_tags_TIME_max']
        df['mean_tags_TIME'] = [
            ((x - min_val) / (max_val - min_val)) for x in tmp_ls]
        df['mean_tags_TIME'] = df.mean_tags_TIME.map(
            lambda x: cutoff_values(x))

        tmp_ls = df['tags_TIME']
        min_val = train_data_dic['tags_TIME_min']
        max_val = train_data_dic['tags_TIME_max']
        df['tags_TIME'] = [((x - min_val) / (max_val - min_val))
                           for x in tmp_ls]
        df['tags_TIME'] = df.tags_TIME.map(lambda x: cutoff_values(x))
    else:
        df['mean_tags_TIME'] = [0] * len(df)
        df['tags_TIME'] = [0] * len(df)

    if ('tags_EVENT' in tags_task_ls):
        tmp_ls = df['tags_EVENT'] / sentcount_ls
        min_val = train_data_dic['mean_tags_EVENT_min']
        max_val = train_data_dic['mean_tags_EVENT_max']
        df['mean_tags_EVENT'] = [
            ((x - min_val) / (max_val - min_val)) for x in tmp_ls]
        df['mean_tags_EVENT'] = df.mean_tags_EVENT.map(
            lambda x: cutoff_values(x))

        tmp_ls = df['tags_EVENT']
        min_val = train_data_dic['tags_EVENT_min']
        max_val = train_data_dic['tags_EVENT_max']
        df['tags_EVENT'] = [((x - min_val) / (max_val - min_val))
                            for x in tmp_ls]
        df['tags_EVENT'] = df.tags_EVENT.map(lambda x: cutoff_values(x))
    else:
        df['mean_tags_EVENT'] = [0] * len(df)
        df['tags_EVENT'] = [0] * len(df)

    if ('tags_PRODUCT' in tags_task_ls):
        tmp_ls = df['tags_PRODUCT'] / sentcount_ls
        min_val = train_data_dic['mean_tags_PRODUCT_min']
        max_val = train_data_dic['mean_tags_PRODUCT_max']
        df['mean_tags_PRODUCT'] = [
            ((x - min_val) / (max_val - min_val)) for x in tmp_ls]
        df['mean_tags_PRODUCT'] = df.mean_tags_PRODUCT.map(
            lambda x: cutoff_values(x))

        tmp_ls = df['tags_PRODUCT']
        min_val = train_data_dic['tags_PRODUCT_min']
        max_val = train_data_dic['tags_PRODUCT_max']
        df['tags_PRODUCT'] = [((x - min_val) / (max_val - min_val))
                              for x in tmp_ls]
        df['tags_PRODUCT'] = df.tags_PRODUCT.map(lambda x: cutoff_values(x))
    else:
        df['mean_tags_PRODUCT'] = [0] * len(df)
        df['tags_PRODUCT'] = [0] * len(df)

    if ('tags_CARDINAL' in tags_task_ls):
        tmp_ls = df['tags_CARDINAL'] / sentcount_ls
        min_val = train_data_dic['mean_tags_CARDINAL_min']
        max_val = train_data_dic['mean_tags_CARDINAL_max']
        df['mean_tags_CARDINAL'] = [
            ((x - min_val) / (max_val - min_val)) for x in tmp_ls]
        df['mean_tags_CARDINAL'] = df.mean_tags_CARDINAL.map(
            lambda x: cutoff_values(x))

        tmp_ls = df['tags_CARDINAL']
        min_val = train_data_dic['tags_CARDINAL_min']
        max_val = train_data_dic['tags_CARDINAL_max']
        df['tags_CARDINAL'] = [
            ((x - min_val) / (max_val - min_val)) for x in tmp_ls]
        df['tags_CARDINAL'] = df.tags_CARDINAL.map(lambda x: cutoff_values(x))
    else:
        df['mean_tags_CARDINAL'] = [0] * len(df)
        df['tags_CARDINAL'] = [0] * len(df)

    if ('tags_MONEY' in tags_task_ls):
        tmp_ls = df['tags_MONEY'] / sentcount_ls
        min_val = train_data_dic['mean_tags_MONEY_min']
        max_val = train_data_dic['mean_tags_MONEY_max']
        df['mean_tags_MONEY'] = [
            ((x - min_val) / (max_val - min_val)) for x in tmp_ls]
        df['mean_tags_MONEY'] = df.mean_tags_MONEY.map(
            lambda x: cutoff_values(x))

        tmp_ls = df['tags_MONEY']
        min_val = train_data_dic['tags_MONEY_min']
        max_val = train_data_dic['tags_MONEY_max']
        df['tags_MONEY'] = [((x - min_val) / (max_val - min_val))
                            for x in tmp_ls]
        df['tags_MONEY'] = df.tags_MONEY.map(lambda x: cutoff_values(x))
    else:
        df['mean_tags_MONEY'] = [0] * len(df)
        df['tags_MONEY'] = [0] * len(df)

    if ('tags_GPE' in tags_task_ls):
        tmp_ls = df['tags_GPE'] / sentcount_ls
        min_val = train_data_dic['mean_tags_GPE_min']
        max_val = train_data_dic['mean_tags_GPE_max']
        df['mean_tags_GPE'] = [
            ((x - min_val) / (max_val - min_val)) for x in tmp_ls]
        df['mean_tags_GPE'] = df.mean_tags_GPE.map(lambda x: cutoff_values(x))

        tmp_ls = df['tags_GPE']
        min_val = train_data_dic['tags_GPE_min']
        max_val = train_data_dic['tags_GPE_max']
        df['tags_GPE'] = [((x - min_val) / (max_val - min_val))
                          for x in tmp_ls]
        df['tags_GPE'] = df.tags_GPE.map(lambda x: cutoff_values(x))
    else:
        df['mean_tags_GPE'] = [0] * len(df)
        df['tags_GPE'] = [0] * len(df)

    if ('tags_QUANTITY' in tags_task_ls):
        tmp_ls = df['tags_QUANTITY'] / sentcount_ls
        min_val = train_data_dic['mean_tags_QUANTITY_min']
        max_val = train_data_dic['mean_tags_QUANTITY_max']
        df['mean_tags_QUANTITY'] = [
            ((x - min_val) / (max_val - min_val)) for x in tmp_ls]
        df['mean_tags_QUANTITY'] = df.mean_tags_QUANTITY.map(
            lambda x: cutoff_values(x))

        tmp_ls = df['tags_QUANTITY']
        min_val = train_data_dic['tags_QUANTITY_min']
        max_val = train_data_dic['tags_QUANTITY_max']
        df['tags_QUANTITY'] = [
            ((x - min_val) / (max_val - min_val)) for x in tmp_ls]
        df['tags_QUANTITY'] = df.tags_QUANTITY.map(lambda x: cutoff_values(x))
    else:
        df['mean_tags_QUANTITY'] = [0] * len(df)
        df['tags_QUANTITY'] = [0] * len(df)

    if ('tags_PERCENT' in tags_task_ls):
        tmp_ls = df['tags_PERCENT'] / sentcount_ls
        min_val = train_data_dic['mean_tags_PERCENT_min']
        max_val = train_data_dic['mean_tags_PERCENT_max']
        df['mean_tags_PERCENT'] = [
            ((x - min_val) / (max_val - min_val)) for x in tmp_ls]
        df['mean_tags_PERCENT'] = df.mean_tags_PERCENT.map(
            lambda x: cutoff_values(x))

        tmp_ls = df['tags_PERCENT']
        min_val = train_data_dic['tags_PERCENT_min']
        max_val = train_data_dic['tags_PERCENT_max']
        df['tags_PERCENT'] = [((x - min_val) / (max_val - min_val))
                              for x in tmp_ls]
        df['tags_PERCENT'] = df.tags_PERCENT.map(lambda x: cutoff_values(x))
    else:
        df['mean_tags_PERCENT'] = [0] * len(df)
        df['tags_PERCENT'] = [0] * len(df)

    if ('tags_NORP' in tags_task_ls):
        tmp_ls = df['tags_NORP'] / sentcount_ls
        min_val = train_data_dic['mean_tags_NORP_min']
        max_val = train_data_dic['mean_tags_NORP_max']
        df['mean_tags_NORP'] = [
            ((x - min_val) / (max_val - min_val)) for x in tmp_ls]
        df['mean_tags_NORP'] = df.mean_tags_NORP.map(
            lambda x: cutoff_values(x))

        tmp_ls = df['tags_NORP']
        min_val = train_data_dic['tags_NORP_min']
        max_val = train_data_dic['tags_NORP_max']
        df['tags_NORP'] = [((x - min_val) / (max_val - min_val))
                           for x in tmp_ls]
        df['tags_NORP'] = df.tags_NORP.map(lambda x: cutoff_values(x))
    else:
        df['mean_tags_NORP'] = [0] * len(df)
        df['tags_NORP'] = [0] * len(df)

    if ('tags_WORK_OF_ART' in tags_task_ls):
        tmp_ls = df['tags_WORK_OF_ART'] / sentcount_ls
        min_val = train_data_dic['mean_tags_WORK_OF_ART_min']
        max_val = train_data_dic['mean_tags_WORK_OF_ART_max']
        df['mean_tags_WORK_OF_ART'] = [
            ((x - min_val) / (max_val - min_val)) for x in tmp_ls]
        df['mean_tags_WORK_OF_ART'] = df.mean_tags_WORK_OF_ART.map(
            lambda x: cutoff_values(x))

        tmp_ls = df['tags_WORK_OF_ART']
        min_val = train_data_dic['tags_WORK_OF_ART_min']
        max_val = train_data_dic['tags_WORK_OF_ART_max']
        df['tags_WORK_OF_ART'] = [
            ((x - min_val) / (max_val - min_val)) for x in tmp_ls]
        df['tags_WORK_OF_ART'] = df.tags_WORK_OF_ART.map(
            lambda x: cutoff_values(x))
    else:
        df['mean_tags_WORK_OF_ART'] = [0] * len(df)
        df['tags_WORK_OF_ART'] = [0] * len(df)

    if ('tags_LANGUAGE' in tags_task_ls):
        tmp_ls = df['tags_LANGUAGE'] / sentcount_ls
        min_val = train_data_dic['mean_tags_LANGUAGE_min']
        max_val = train_data_dic['mean_tags_LANGUAGE_max']
        df['mean_tags_LANGUAGE'] = [
            ((x - min_val) / (max_val - min_val)) for x in tmp_ls]
        df['mean_tags_LANGUAGE'] = df.mean_tags_LANGUAGE.map(
            lambda x: cutoff_values(x))

        tmp_ls = df['tags_LANGUAGE']
        min_val = train_data_dic['tags_LANGUAGE_min']
        max_val = train_data_dic['tags_LANGUAGE_max']
        df['tags_LANGUAGE'] = [
            ((x - min_val) / (max_val - min_val)) for x in tmp_ls]
        df['tags_LANGUAGE'] = df.tags_LANGUAGE.map(lambda x: cutoff_values(x))
    else:
        df['mean_tags_LANGUAGE'] = [0] * len(df)
        df['tags_LANGUAGE'] = [0] * len(df)

    if ('tags_DATE' in tags_task_ls):
        tmp_ls = df['tags_DATE'] / sentcount_ls
        min_val = train_data_dic['mean_tags_DATE_min']
        max_val = train_data_dic['mean_tags_DATE_max']
        df['mean_tags_DATE'] = [
            ((x - min_val) / (max_val - min_val)) for x in tmp_ls]
        df['mean_tags_DATE'] = df.mean_tags_DATE.map(
            lambda x: cutoff_values(x))

        tmp_ls = df['tags_DATE']
        min_val = train_data_dic['tags_DATE_min']
        max_val = train_data_dic['tags_DATE_max']
        df['tags_DATE'] = [((x - min_val) / (max_val - min_val))
                           for x in tmp_ls]
        df['tags_DATE'] = df.tags_DATE.map(lambda x: cutoff_values(x))
    else:
        df['mean_tags_DATE'] = [0] * len(df)
        df['tags_DATE'] = [0] * len(df)

    if ('tags_PERSON' in tags_task_ls):
        tmp_ls = df['tags_PERSON'] / sentcount_ls
        min_val = train_data_dic['mean_tags_PERSON_min']
        max_val = train_data_dic['mean_tags_PERSON_max']
        df['mean_tags_PERSON'] = [
            ((x - min_val) / (max_val - min_val)) for x in tmp_ls]
        df['mean_tags_PERSON'] = df.mean_tags_PERSON.map(
            lambda x: cutoff_values(x))

        tmp_ls = df['tags_PERSON']
        min_val = train_data_dic['tags_PERSON_min']
        max_val = train_data_dic['tags_PERSON_max']
        df['tags_PERSON'] = [((x - min_val) / (max_val - min_val))
                             for x in tmp_ls]
        df['tags_PERSON'] = df.tags_PERSON.map(lambda x: cutoff_values(x))
    else:
        df['mean_tags_PERSON'] = [0] * len(df)
        df['tags_PERSON'] = [0] * len(df)

    if ('tags_FAC' in tags_task_ls):
        tmp_ls = df['tags_FAC'] / sentcount_ls
        min_val = train_data_dic['mean_tags_FAC_min']
        max_val = train_data_dic['mean_tags_FAC_max']
        df['mean_tags_FAC'] = [
            ((x - min_val) / (max_val - min_val)) for x in tmp_ls]
        df['mean_tags_FAC'] = df.mean_tags_FAC.map(lambda x: cutoff_values(x))

        tmp_ls = df['tags_FAC']
        min_val = train_data_dic['tags_FAC_min']
        max_val = train_data_dic['tags_FAC_max']
        df['tags_FAC'] = [((x - min_val) / (max_val - min_val))
                          for x in tmp_ls]
        df['tags_FAC'] = df.tags_FAC.map(lambda x: cutoff_values(x))
    else:
        df['mean_tags_FAC'] = [0] * len(df)
        df['tags_FAC'] = [0] * len(df)


def compute_quality_features(df, train_data_dic):
    df['feature_tuned'] = df.feature_tuned.map(lambda x: mask_giventime(x))
    df['giventime'] = df.feature_tuned.map(lambda x: int(
        'giventime' in x) or int('givendatetime' in x))
    df['feature_tuned'] = df.feature_tuned.map(lambda x: mask_link(x))
    df['link'] = df.feature_tuned.map(lambda x: int(
        ('LINKK' in x) or ('link' in x) or ('Link' in x)))
    df['feature_tuned'] = df.feature_tuned.map(lambda x: mask_website(x))
    df['website'] = df.feature_tuned.map(lambda x: int('WEBSSITE' in x))
    df['feature_tuned'] = df.feature_tuned.map(lambda x: mask_reward(x))
    df['reward'] = df.feature_tuned.map(lambda x: int('REWARDD' in x))
    df['feature_tuned'] = df.feature_tuned.map(lambda x: mask_socialmedia(x))
    df['socialmedia'] = df.feature_tuned.map(
        lambda x: int('SOCIALMEDIAA' in x))
    df['feature_tuned'] = df.feature_tuned.map(lambda x: mask_image(x))
    df['image'] = df.feature_tuned.map(lambda x: int('IMAGEE' in x))

    df['FullDesc_POS'] = df.Description.map(lambda x: convert_FullDesc2POS(x))

    compute_mean_POS_features(df, train_data_dic)

    run_tag_spacy_dftest(df)
    normalize_tag_features(df, train_data_dic)
