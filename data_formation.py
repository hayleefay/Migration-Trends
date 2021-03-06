import pandas as pd

bilateral_df = pd.read_csv('feature_data/bilateral_flow.csv', low_memory=False)

bilateral_df = pd.melt(bilateral_df, value_vars=['countryflow_1990','countryflow_1995','countryflow_2000','countryflow_2005'], id_vars=['region_orig','region_orig_id','region_dest','region_dest_id','country_orig','country_orig_id','country_dest','country_dest_id'])

bilateral_df['year'] = bilateral_df.variable.str[-4:]

feature_list = ['fertility','laborparticipation','literacy','primaryenroll','workingagepop','perworkergdp', 'safety_net', 'employratio','social_cont']

def feature_average(x, feature):
    feature_orig = feature + '_orig'
    feature_dest = feature + '_dest'
    if x['year'] == '1990':
        value_orig = feature + '_1990_x'
        value_dest = feature + '_1990_y'
    elif x['year'] == '1995':
        value_orig = feature + '_1995_x'
        value_dest = feature + '_1995_y'
    elif x['year'] == '2000':
        value_orig = feature + '_2000_x'
        value_dest = feature + '_2000_y'
    elif x['year'] == '2005':
        value_orig = feature + '_2005_x'
        value_dest = feature + '_2005_y'

    x[feature_orig] = x[value_orig]
    x[feature_dest] = x[value_dest]

    return x


for feature in feature_list:
    file_name = 'feature_data/' + feature + '.csv'
    feature_df = pd.read_csv(file_name, low_memory=False)

    df = pd.DataFrame()
    mean_df = pd.DataFrame()

    df['1990'] = feature_df['1990 [YR1990]']
    df['1991'] = feature_df['1991 [YR1991]']
    df['1992'] = feature_df['1992 [YR1992]']
    df['1993'] = feature_df['1993 [YR1993]']
    df['1994'] = feature_df['1994 [YR1994]']
    df['1995'] = feature_df['1995 [YR1995]']
    df['1996'] = feature_df['1996 [YR1996]']
    df['1997'] = feature_df['1997 [YR1997]']
    df['1998'] = feature_df['1998 [YR1998]']
    df['1999'] = feature_df['1999 [YR1999]']
    df['2000'] = feature_df['2000 [YR2000]']
    df['2001'] = feature_df['2001 [YR2001]']
    df['2002'] = feature_df['2002 [YR2002]']
    df['2003'] = feature_df['2003 [YR2003]']
    df['2004'] = feature_df['2004 [YR2004]']
    df['2005'] = feature_df['2005 [YR2005]']
    df['2006'] = feature_df['2006 [YR2006]']
    df['2007'] = feature_df['2007 [YR2007]']
    df['2008'] = feature_df['2008 [YR2008]']
    df['2009'] = feature_df['2009 [YR2009]']
    df['2010'] = feature_df['2010 [YR2010]']

    df = df.convert_objects(convert_numeric=True)
    feature_1990 = feature + '_1990'
    feature_1995 = feature + '_1995'
    feature_2000 = feature + '_2000'
    feature_2005 = feature + '_2005'

    mean_df[feature_1990] = df[['1990','1991','1992','1993','1994','1995']].mean(axis=1)
    mean_df[feature_1995] = df[['1995','1996','1997','1998','1999','2000']].mean(axis=1)
    mean_df[feature_2000] = df[['2000','2001','2002','2003','2004','2005']].mean(axis=1)
    mean_df[feature_2005] = df[['2005','2006','2007','2008','2009','2010']].mean(axis=1)
    mean_df['Country'] = feature_df['Country Name']

    joined_df = pd.merge(bilateral_df, mean_df, how='inner', left_on='country_orig', right_on='Country')
    double_joined_df = pd.merge(joined_df, mean_df, how='inner', left_on='country_dest', right_on='Country')
    bilateral_df = double_joined_df.apply(feature_average, args=(feature,), axis=1)

complete_df = bilateral_df[['region_orig','region_orig_id','region_dest','region_dest_id',\
'country_orig','country_orig_id','country_dest','country_dest_id','year','value',\
'fertility_orig','fertility_dest','laborparticipation_orig','laborparticipation_dest',\
'literacy_orig','literacy_dest','primaryenroll_orig','primaryenroll_dest','workingagepop_orig','workingagepop_dest',\
'perworkergdp_orig','perworkergdp_dest','safety_net_orig','safety_net_dest','employratio_orig','employratio_dest',\
'social_cont_orig', 'social_cont_dest']]

country_orig_list = pd.Series(complete_df['country_orig_id'])
country_dummy = pd.get_dummies(country_orig_list, prefix='dummy')

year_list = pd.Series(complete_df['year'])
year_df = pd.get_dummies(year_list, prefix='dummy')

complete_df = pd.concat([complete_df, country_dummy, year_df], axis=1)

language_df = pd.read_csv('feature_data/common_language.csv', low_memory=False)
language_df = language_df[['iso_o', 'iso_d', 'col']]
language_df.rename(index=str, columns={"iso_o": "country_orig_id", "iso_d": "country_dest_id"})

distance_df = pd.read_csv('feature_data/distances.csv', low_memory=False)
distance_df = distance_df[['iso_o', 'iso_d', 'distwces']]
distance_df.rename(index=str, columns={"iso_o": "country_orig_id", "iso_d": "country_dest_id"})


complete_df = pd.merge(complete_df, language_df, how='inner', on=['country_orig','country_dest'])
complete_df = pd.merge(complete_df, distance_df, how='inner', on=['country_orig','country_dest'])

complete_df.to_csv("migration_data.csv")
