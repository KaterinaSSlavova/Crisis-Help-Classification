import pandas as pd

def get_label_columns(df):
    non_label_cols = ["id", "message", "original", "genre"]
    label_cols = [c for c in df.columns if c not in non_label_cols]
    return label_cols

def load_split_data(show = False):
    X_train = pd.read_csv("../data/split_data/X_train.csv").iloc[:, 0]
    X_test = pd.read_csv("../data/split_data/X_test.csv").iloc[:, 0]
    X_val = pd.read_csv("../data/split_data/X_val.csv").iloc[:, 0]
    y_train = pd.read_csv("../data/split_data/y_train.csv")
    y_test = pd.read_csv("../data/split_data/y_test.csv")
    y_val = pd.read_csv("../data/split_data/y_val.csv")
    if show == True:
        print("X_train:", X_train.shape)
        print("X_val:", X_val.shape)
        print("X_test:", X_test.shape)
        print("y_train:", y_train.shape)
        print("y_val:", y_val.shape)
        print("y_test:", y_test.shape)
    return X_train, X_val, X_test, y_train, y_val, y_test


