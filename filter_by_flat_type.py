import pandas as pd

df = pd.read_csv("cleanRegressionData.csv", index_col=0)
df = df[df["4 ROOM"]==1]
df = df[df["s_months"]>=200]
df = df[df["s_months"]<=260]

print (df.info())

df.to_csv("4_room_clean_new.csv")
