from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
import pandas as pd
import numpy as np
import pickle

def reshape_data(df, window_size):
    reshaped_data = []
    for i in range(len(df) - window_size + 1):
        window = df.iloc[i:i+window_size].values.flatten()
        reshaped_data.append(window)
    return np.array(reshaped_data)

def predict(dataFile='Data.csv', modelFile='SentiTrader.pkl'):
    with open(modelFile, 'rb') as file:  
        model = pickle.load(file)

    df = pd.read_csv(dataFile)
    df = df[['Open', 'High', 'Low','Volume','Subjectivity','Polarity','compound','neg','pos','neu']]

    X = df.values.flatten().reshape(1, -1)
    y = model.predict(X)

    return y[0]

if __name__ == '__main__':
    print(predict())
