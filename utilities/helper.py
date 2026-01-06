import pandas as pd
import numpy as np

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

def run_inference_demo(df_inf,labels,best_lr,best_svc,best_mnb,preprocess_fn,get_scores_fn,text_col="message", max_chars=350):
    texts = df_inf[text_col].fillna("").astype(str).tolist()
    y_true = df_inf[labels].values
    idxs =[59,45]
    sel_texts = [texts[i] for i in idxs]
    sel_texts_norm = [preprocess_fn(t) for t in sel_texts]

    lr_model,  lr_t  = best_lr["model"],  np.array(best_lr["thresholds_per_label"])
    svc_model, svc_t = best_svc["model"], np.array(best_svc["thresholds_per_label"])
    mnb_model, mnb_t = best_mnb["model"], np.array(best_mnb["thresholds_per_label"])

    lr_scores  = get_scores_fn(lr_model, sel_texts_norm)
    lr_pred    = (lr_scores >= lr_t.reshape(1, -1)).astype(int)

    svc_scores = get_scores_fn(svc_model, sel_texts_norm)
    svc_pred   = (svc_scores >= svc_t.reshape(1, -1)).astype(int)

    mnb_scores = get_scores_fn(mnb_model, sel_texts_norm)
    mnb_pred   = (mnb_scores >= mnb_t.reshape(1, -1)).astype(int)

    for k, i in enumerate(idxs):
        msg = texts[i]
        true_labels = [labels[j] for j in np.where(y_true[i] == 1)[0]]

        lr_labels  = [labels[j] for j in np.where(lr_pred[k] == 1)[0]]
        svc_labels = [labels[j] for j in np.where(svc_pred[k] == 1)[0]]
        mnb_labels = [labels[j] for j in np.where(mnb_pred[k] == 1)[0]]

        print("\nMESSAGE:", msg[:max_chars].replace("\n", " "))
        print("True labels          :", true_labels)
        print("MNB predicted labels  :", mnb_labels)
        print("LR predicted labels   :", lr_labels)
        print("SVC predicted labels  :", svc_labels)

