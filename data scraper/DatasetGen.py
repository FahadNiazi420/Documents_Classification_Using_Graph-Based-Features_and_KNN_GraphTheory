import pandas as pd
from sklearn.model_selection import train_test_split
import os

# Load csv files into dataframes
data1 = pd.read_csv('../Processed Data/cleaned_inToGloss.csv')
data2 = pd.read_csv('../Processed Data/cleaned_MyFitnessPal.csv')
data3 = pd.read_csv('../Processed Data/cleaned_SciAM.csv')

# Combine dataframes
combined_data = pd.concat([data1, data2, data3])

# Split data into training set and test set
train_data, test_data = train_test_split(combined_data, test_size=0.2, random_state=42)
if not os.path.exists('../Dataset'):
    os.makedirs('../Dataset')
# Save training set and test set to Dataset folder
train_data.to_csv('../Dataset/Train.csv', index=False)
test_data.to_csv('../Dataset/Test.csv', index=False)