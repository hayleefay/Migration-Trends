import pandas as pd
import statsmodels.formula.api as sm

df = pd.read_csv('migration_data.csv', low_memory=False)

orig_flow = df['countryflow_2000']
orig_fertility = df['fertility_1990_x']
dest_fertility = df['fertility_1990_y']
orig_labor = df['laborparticipation_1990_x']
dest_labor = df['laborparticipation_1990_y']
orig_literacy = df['literacy_1990_x']
dest_literacy = df['literacy_1990_y']
orig_primaryenroll = df['primaryenroll_1990_x']
dest_primaryenroll = df['primaryenroll_1990_y']
orig_workingagepop = df['workingagepop_1990_x']
dest_workingagepop = df['workingagepop_1990_y']
orig_perworkergdp = df['perworkergdp_1990_x']
dest_perworkergdp = df['perworkergdp_1990_y']
orig_safetynet = df['safety_net_1990_x']
dest_safetynet = df['safety_net_2000_y']

countries = df['country_orig_id'].unique()
dummy_string = ''
for country in countries:
    dummy_string += ' + dummy_' + country

formula = 'orig_flow ~ dest_safetynet' + dummy_string

model = sm.ols(formula=formula, data=df).fit()

print(model.summary())

'''
'orig_flow ~ orig_fertility + dest_fertility + orig_labor + dest_labor + orig_literacy + dest_literacy \
+ orig_primaryenroll + dest_primaryenroll + orig_workingagepop + dest_workingagepop + orig_perworkergdp + dest_perworkergdp'
'''

# eh to primaryenroll I don't love it, not really sure what it is capturing
