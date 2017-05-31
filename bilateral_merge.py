import pandas as pd

complete_df = pd.read_csv('migration_data.csv', low_memory=False)

language_df = pd.read_csv('feature_data/common_language.csv', low_memory=False)
language_df = language_df[['iso_o', 'iso_d', 'col']]
language_df = language_df.rename(index=str, columns={"iso_o": "country_orig_id", "iso_d": "country_dest_id"})

distance_df = pd.read_csv('feature_data/distances.csv', low_memory=False)
distance_df = distance_df[['iso_o', 'iso_d', 'distwces']]
distance_df = distance_df.rename(index=str, columns={"iso_o": "country_orig_id", "iso_d": "country_dest_id"})


complete_df = pd.merge(complete_df, language_df, how='inner', on=['country_orig_id','country_dest_id'])
complete_df = pd.merge(complete_df, distance_df, how='inner', on=['country_orig_id','country_dest_id'])

complete_df.to_csv("extra_migration_data.csv")
