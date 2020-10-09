#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This file runs all of the data computational data analysis used to draw conclusions on the topic of the paper. Simply ensure the Voting.csv file is
correctly named and in the same folder as this script and run it. 
"""

import pandas as pd, math

# convert csv to pandas dataframe
voting_file = pd.read_csv("Voting.csv")

# number of people who voted in each state
voted_state = voting_file.groupby('state')['voted'].sum()

# number of people registered in each state
reg_state = voting_file.groupby('state')['registered'].sum()

# number of people who voted democrat in prez election per state
dem_state = voting_file.groupby('state')['democrat'].sum()

# number of people who voted democrat in senate election per state
dem_senate = voting_file.groupby('state')['demSenate'].sum()

# number of people who voted republican in prez election per state
rep_state = voting_file.groupby('state')['republican'].sum()

# number of people who voted republican in senate election per state
rep_senate = voting_file.groupby('state')['repSenate'].sum()

# create dataframe that will be helpful for looking at things at the state level: state_df
state_df = pd.DataFrame({'state': voting_file.state.unique(), 'voted':voted_state,'registered':reg_state, "dem": dem_state,
                         'rep': rep_state, 'demSenate': dem_senate, 'repSenate': rep_senate},
                        columns = ['state', 'voted', 'registered', 'dem', 'rep', 'demSenate', 'repSenate'])
state_df.reset_index(drop=True, inplace=True)

# add number of people who voted democrat or republican in prez election per state to state_df
state_df['dem_or_rep'] = state_df[['dem', 'rep']].sum(axis=1)

# add percent who voted for democrat presidential candidate per state to state_df
state_df['p_dem'] = state_df['dem']/state_df['dem_or_rep']

# add early voting status per state to state_df
state_early = []
for state in state_df['state']:
    far = str(voting_file[voting_file['state']==state]['earlyVoting'].unique())[2:-2]
    state_early.append(far)
state_df['earlyVoting'] = state_early


# dataframe same as state_df but just states whose 'earlyVoting' status is 'EarlyVoting' or 'NoEarlyVoting'
state_df_specific = state_df[(state_df['earlyVoting'] == 'EarlyVoting') | (state_df['earlyVoting'] == 'NoEarlyVoting')]


# table 1: only the info I need, discussed in paper
table_1 = state_df_specific[['state', 'dem', 'rep', 'dem_or_rep', 'p_dem', 'earlyVoting']]

# table 1, but just states with true early voting
table_1_true_early = table_1[(table_1['earlyVoting'] == 'EarlyVoting')]

# table 1, but just states without eary voting
table_1_no_early = table_1[(table_1['earlyVoting'] == 'NoEarlyVoting')]

# print table 1 to the console
print("Table 1 (as described in paper)")
with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    print(table_1)



# number of states with no form of early voting
n_no_early = (state_df['earlyVoting'] == 'NoEarlyVoting').sum() # 13

# number of states with true early voting
n_true_early = (state_df['earlyVoting'] == 'EarlyVoting').sum() # 20

# mean percent that voted democrat from states with no form of early voting
mean_p_dem_no_early = state_df.loc[state_df['earlyVoting'] == 'NoEarlyVoting', 'p_dem'].mean() # 0.4825950913492718
print("\n \n \nmean p_i from states with no early voting: ", mean_p_dem_no_early )

# standard deviation that voted democrat from states with no form of early voting
std_p_dem_no_early = state_df.loc[state_df['earlyVoting'] == 'NoEarlyVoting', 'p_dem'].std() # 0.09085158470133975

# mean percent that voted democrat from states with true early voting
mean_p_dem_true_early = state_df.loc[state_df['earlyVoting'] == 'EarlyVoting', 'p_dem'].mean() # 0.5025836958077804
print("mean p_i from states with early voting: ", mean_p_dem_true_early)

# standard deviation percent that voted democrat from states with true early voting
std_p_dem_true_early = state_df.loc[state_df['earlyVoting'] == 'EarlyVoting', 'p_dem'].std() # 0.16085460524277162

# t-test difference in mean p_dem between states with true early voting and no early voting
print("\n2-Sample T-Test on difference in mean p_i between states with and without early voting")
numerator = mean_p_dem_true_early - mean_p_dem_no_early # 0.019988604458508585
print("difference in mean p_i: ", numerator)
denominator_1 = mean_p_dem_true_early*(1-mean_p_dem_true_early)/n_true_early
denominator_2 = mean_p_dem_no_early*(1-mean_p_dem_no_early)/n_no_early
denominator = math.sqrt(denominator_1+denominator_2) # 0.1780649687160975 = SE
print("SE of the means: ", denominator)
t = numerator/denominator # t=0.11225455856158846
print("t-score: ", t)
c_i = [numerator - 1.96*denominator, numerator + 1.96*denominator] # confidence interval: [-0.3290187342250425, 0.3689959431420597]
print("confidence interval: ", c_i)


# look at states that voted democrat in presidenial election
print("\n \n \nDEMOCRATIC STATES\n")

# number of states with true early voting that went democrat in the prez election
t_e_d_apply = state_df.apply(lambda x : True if (x['earlyVoting'] == "EarlyVoting" and x['p_dem'] > 0.5) else False, axis = 1) 
n_true_early_dem = len(t_e_d_apply[t_e_d_apply == True].index) # 8

# number of states with no early voting that went democrat in the prez election
n_e_d_apply = state_df.apply(lambda x : True if (x['earlyVoting'] == "NoEarlyVoting" and x['p_dem'] > 0.5) else False, axis = 1) 
n_no_early_dem = len(n_e_d_apply[n_e_d_apply == True].index) # 6

# mean percent of voting democrat from states with true early voting that went democrat in the prez election
p_dem_true_early_dem_apply = state_df.apply(lambda x : x['p_dem'] if (x['earlyVoting'] == "EarlyVoting" and x['p_dem'] > 0.5) else False, axis = 1)
mean_p_dem_true_early_dem = p_dem_true_early_dem_apply.sum()/n_true_early_dem # 0.653621038068174
print("mean p_i from Democratic states with early voting: ", mean_p_dem_true_early_dem )

# standard deviation of percent voting democrat from states with true early voting that went democrat in the prez election
std_p_dem_true_early_dem = p_dem_true_early_dem_apply.std() # 0.24739215854690827

# mean percent of voting democrat from states with no early voting that went democrat in the prez election
p_dem_no_early_dem_apply = state_df.apply(lambda x : x['p_dem'] if (x['earlyVoting'] == "NoEarlyVoting" and x['p_dem'] > 0.5) else False, axis = 1)
mean_p_dem_no_early_dem = p_dem_no_early_dem_apply.sum()/n_no_early_dem # 0.5603158023636888
print("mean p_i from Democratic states with no early voting: ", mean_p_dem_no_early_dem )

# standard deviation of percent voting democrat from states with no early voting that went democrat in the prez election
std_p_dem_no_early_dem = p_dem_no_early_dem_apply.std() # 0.18439189852281082

# t-test difference in mean p_dem between states with true early voting and no early voting that went democrat in the presidential election
print("\n2-Sample T-Test on difference in mean p_i between Democratic states with and without early voting")
num_dem = mean_p_dem_true_early_dem - mean_p_dem_no_early_dem # 0.09330523570448512
print("difference in mean p_i: ", num_dem)
den_1_dem = mean_p_dem_true_early_dem*(1-mean_p_dem_true_early_dem)/n_true_early_dem
den_2_dem = mean_p_dem_no_early_dem*(1-mean_p_dem_no_early_dem)/n_no_early_dem 
den_dem = math.sqrt(den_1_dem+den_2_dem) # 0.2633636384932333 = SE
print("SE of the means: ", den_dem)
t_dem = num_dem/den_dem # t=0.35428290799104545
print("t-score: ", t_dem)
c_i_dem = [num_dem - 1.96*den_dem, num_dem + 1.96*den_dem] # [-0.42288749574225215, 0.6094979671512224]
print("confidence interval: ", c_i_dem)



# look at states that voted republican in presidential elction
print("\n \n \nREPUBLICAN STATES\n")

# number of states with true early voting that went republican in the prez election
t_e_r_apply = state_df.apply(lambda x : True if (x['earlyVoting'] == "EarlyVoting" and x['p_dem'] < 0.5) else False, axis = 1) 
n_true_early_rep = len(t_e_r_apply[t_e_r_apply == True].index) # 12

# number of states with no early voting that went republican in the prez election
n_e_r_apply = state_df.apply(lambda x : True if (x['earlyVoting'] == "NoEarlyVoting" and x['p_dem'] < 0.5) else False, axis = 1) 
n_no_early_rep = len(n_e_r_apply[n_e_r_apply == True].index) # 7

# mean percent of voting republican from states with true early voting that went republican in the prez election
p_dem_true_early_rep_apply = state_df.apply(lambda x : x['p_dem'] if (x['earlyVoting'] == "EarlyVoting" and x['p_dem'] < 0.5) else False, axis = 1)
mean_p_dem_true_early_rep = p_dem_true_early_rep_apply.sum()/n_true_early_rep # 0.4018921343008512
print("mean p_i from Republican states with early voting: ", mean_p_dem_true_early_rep )

# standard deviation of percent voting democrat from states with true early voting that went republican in the prez election
std_p_dem_true_early_rep = p_dem_true_early_rep_apply.std() # 0.1768467685640697

# mean percent of voting republican from states with no early voting that went republican in the prez election
p_dem_no_early_rep_apply = state_df.apply(lambda x : x['p_dem'] if (x['earlyVoting'] == "NoEarlyVoting" and x['p_dem'] < 0.5) else False, axis = 1)
mean_p_dem_no_early_rep = p_dem_no_early_rep_apply.sum()/n_no_early_rep # 0.4159773390512001
print("mean p_i from Republican states with no early voting: ", mean_p_dem_no_early_rep)

# standard deviation of percent voting democrat from states with no early voting that went republican in the prez election
std_p_dem_no_early_rep = p_dem_no_early_rep_apply.std() # 0.14743251901790505

# t-test difference in mean p_dem between states with true early voting and no early voting that went republican in the presidential election
print("\n2-Sample T-Test on difference in mean p_i between Republican states with and without early voting")
num_rep = mean_p_dem_true_early_rep - mean_p_dem_no_early_rep
print("difference in mean p_i: ", num_rep)
den_1_rep = mean_p_dem_true_early_rep*(1-mean_p_dem_true_early_rep)/n_true_early_rep
den_2_rep = mean_p_dem_no_early_rep*(1-mean_p_dem_no_early_rep)/n_no_early_rep
den_rep = math.sqrt(den_1_rep+den_2_rep) # 0.23395935331196144 = SE
print("SE of the means: ", den_rep)
t_rep = num_rep/den_rep # t=-0.06020364029459296
print("t-score: ", t_rep)
c_i_rep = [num_rep - 1.96*den_rep, num_rep + 1.96*den_rep] # [-0.4726455372417933, 0.4444751277410955]
print("confidence interval: ", c_i_rep)
