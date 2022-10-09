import pandas as pd
df = pd.read_csv("./Web-Scraping/club_data.csv")
print(df)
print(df.iloc[999]['topics'])