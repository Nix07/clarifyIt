def general_tag_of_desc(desc):
    pos_ls = []
    for word in desc.split():
        if len(word)>2:
            ls = word.split('/')
            pos_ls.append(ls[1])
    return ' '.join([item for item in pos_ls])

def compute_style_features(df):
    df['DescPOS_Only'] = df.FullDesc_POS.map(lambda x: general_tag_of_desc(x))
