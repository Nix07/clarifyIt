import json
import time
import re
import string
import pandas as pd

from features import length_features
from features import quality_features
from features import style_features
from features import subjectivity_features
from features import readability_features


df = pd.DataFrame(columns=['Description'])


def copy_original_to_short():
    df['feature_tuned'] = df.Description


def preprocess_data(train_data_dic):
    copy_original_to_short()

    start = time.time()
    quality_features.compute_quality_features(df, train_data_dic)
    print(f'Quality feature {time.time() - start}')
    length_features.compute_length_features(df, train_data_dic)
    print(f'Length feature {time.time() - start}')
    style_features.compute_style_features(df)
    print(f'Style feature {time.time() - start}')
    subjectivity_features.compute_subjectivity_features(df, train_data_dic)
    print(f'Subjectivity feature {time.time() - start}')
    readability_features.compute_readability_features(df, train_data_dic)
    print(f'Readability feature {time.time() - start}')


def compute(taskData, train_data_dic):
    description = ''
    for key in ['title', 'description']:
        value = taskData[key].strip()
        if (key == 'title'):
            description += value + '. '
        else:
            description += value

    df.at[0, 'Description'] = description
    preprocess_data(train_data_dic)

    return df
    # response = {}
    # for column in df.columns:
    #     response[column] = str(df[column].tolist()[0])

    # return response
