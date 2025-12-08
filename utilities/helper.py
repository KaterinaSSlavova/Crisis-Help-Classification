def calculate_label_message_percentage(df):
    label_cols = get_label_columns(df)
    label_counts = df[label_cols].sum().sort_values(ascending=False)
    total_msgs = len(df)
    label_pct = (label_counts / total_msgs * 100).round(2)
    return label_pct

def get_label_columns(df):
    non_label_cols = ["id", "message", "original", "genre"]
    label_cols = [c for c in df.columns if c not in non_label_cols]
    return label_cols