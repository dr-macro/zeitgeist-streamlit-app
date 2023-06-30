import boto3
import datetime
import pytz
import os
import pandas as pd

df2 = pd.read_csv('2021.csv')
df2.columns = ['Country', 'party', 'politician name', 'user_id',
       'Unnamed: 4', 'date time', 'tweet id']

access_point_arn = "arn:aws:s3:eu-central-1:474425760885:accesspoint/accesspointfortweets"

s3 = boto3.client("s3")
result = s3.list_objects_v2(Bucket=access_point_arn)


files_available = []
start_date = datetime.datetime(2023, 2, 4)
start_date = pytz.timezone("UTC").localize(start_date)
for content in result.get("Contents"):
    file_date = content.get("LastModified")
    if file_date >= start_date:
        print(content.get("Key"))
        files_available.append(content.get("Key"))

os.chdir('tweet topic overview images/data')
files_already_dowloaded = os.listdir()

files_to_download = [f for f in files_available if f not in files_already_dowloaded]

for file in files_to_download:
    s3.download_file(Bucket=access_point_arn, Key=file, Filename=file)


def get_country_file_names(files, country):
    select = []
    for x in files:
        select.append(country in x)
    return list(pd.Series(files)[select])


def get_merged_data(country_file_names):
    df_all = pd.DataFrame(columns=['created_at', 'id_tweet', 'user_id', 'text', 'count_rt', 'count_rep',
                                   'count_like', 'type', 'entities', 'in_reply_to_user_id',
                                   'referenced_tweets'])
    for file_name in country_file_names:
        df = prepare_data(file_name)

        df_all = df_all.append(df)

    df_all.index = range(len(df_all))
    df_all = df_all.loc[df_all['id_tweet'].drop_duplicates().index]
    return df_all


def prepare_data(file_name):
    df = pd.read_parquet(file_name)
    df.columns = ['created_at', 'id_tweet', 'user_id', 'text', 'count_rt', 'count_rep',
                  'count_like', 'type', 'entities', 'in_reply_to_user_id',
                  'referenced_tweets']

    party = []
    id_to_party = df2[df2['Country'] == 'United States'][['party', 'user_id']].drop_duplicates()
    for i in df.index:

        try:
            party.append(id_to_party[id_to_party['user_id'] == df.loc[i, 'user_id']]['party'].values[0])
        except:
            party.append('unknown')
    df['party'] = party

    return df


files = files_to_download

# Collate parquet files into dataframes for each country

countries_of_interest = ['United States', 'United Kingdom', 'European Parliament', 'France', 'Germany', 'Australia',
                         'Turkey']
data = {}
for country in countries_of_interest:
    print(f'Starting process for {country}')

    country_file_names = get_country_file_names(files, country)
    country_files = get_merged_data(country_file_names)

    data[country] = country_files
