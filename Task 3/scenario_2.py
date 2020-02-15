import pandas as pd

data_initial = pd.read_json('task3_scn2.json')
data_1 = data_initial.drop(columns=['Percentage'], axis=1)
data_2 = data_initial.drop(columns=['Amount'], axis=1)
data_2.rename(columns={'Percentage': 'Amount'}, inplace=True)

data_final = data_2.append(data_1, sort=True)
data_final = data_final.reset_index(drop=True)

print('input_data:\n', data_initial)
print('output_data:\n', data_final)
