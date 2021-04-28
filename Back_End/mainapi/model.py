import joblib
import numpy as np
from sklearn import *
from sklearn.preprocessing import OneHotEncoder
import time
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.multioutput import MultiOutputRegressor
from sklearn.feature_extraction.text import TfidfVectorizer

df = pd.read_excel(
    'C:\\Users\\Chotu\\Desktop\\Sustainability_Study\\BrandDB.xlsx', )
df.head()
X_Cols = df['Statement']
df['Planet'] = df['Planet'].fillna(0)
df['Planet'] = df['Planet'].astype(int)
df['People'] = df['People'].fillna(0)
df['People'] = df['People'].astype(int)
df['Animals'] = df['Animals'].fillna(0)
df['Animals'] = df['Animals'].astype(int)
df['Planet'] = df['Planet'].astype(str)
df['People'] = df['Planet'].astype(str)
df['Animals'] = df['Animals'].astype(str)
df['Planet'] = df['Planet'].astype(str)
df['People'] = df['Planet'].astype(str)
df['Animals'] = df['Animals'].astype(str)


def split_data_train_model(labels, data):
    # 20% examples in test data
    train, test, train_labels, test_labels = train_test_split(data,
                                                              labels,
                                                              test_size=0.2,
                                                              random_state=RF_SEED)

    # training data fit
    regressor = RandomForestRegressor(n_estimators=1000, random_state=RF_SEED)
    regressor.fit(x_data, y_data)

    return test, test_labels, regressor


tfidf = TfidfVectorizer(sublinear_tf=True, min_df=1, norm='l2',
                        encoding='latin-1', ngram_range=(1, 2), stop_words='english')

features = tfidf.fit_transform(df.Statement.values.astype('U')).toarray()
print(type(features))
# vocabulary = "We believe in design simplicity and versatility as a way of reducing waste. We focus on what matters: design, sustainability, quality, comfort and functional integrity. We create outdoor footwear that you actually want to wear. Anytime, anywhere, on or off the beaten trail. We spend years developing each collection of footwear, meticulously searching for the most sustainable materials in the world. Materials that tread lightly on the planet and respect people - natural fair trade rubber, re-claimed ocean plastics, recycled PET, and vegan water based glue to name a few. All our footwear is virgin plastic free and our rubber sourced from sustainably managed forests. We travel the world to find the best producers of outdoor footwear, those with generational knowledge who also share our value of sustainability and ethics. Then we take it a step further: we move to the region, we get to know the culture + community, we break bread, we laugh and share stories, and most importantly work closely to push boundaries on sustainability and innovation. Why? Because we demand quality, not just in the products we make, but also for the lives of the people who make them. Headquartered in Toronto, Canada, we are a tight-knit, diverse team of people from around the world . Our diversity is what makes us stronger. Sofi Khwaja, our CEO, is a woman and a POC. This puts us in a unique position to truly represent our diverse community of outdoor enthusiasts. We are committed to ensure diversity in all our ranks as we grow"
# features2 = tfidf.transform([vocabulary])
X = features
# print(X)
y = df[['Planet', 'People', 'Animals']]
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=4)
max_depth = 30
regr_multirf = MultiOutputRegressor(RandomForestRegressor(n_estimators=1,
                                                          max_depth=max_depth,
                                                          random_state=0))
regr_multirf.fit(X_train, y_train)
# y_multirf = regr_multirf.predict(X_test)
# print(regr_multirf.predict(features2))
# Serialize the model and save
joblib.dump(regr_multirf, 'randomfs.pkl')
print("Random Forest Model Saved")
# Load the model
# Save features from training
rnd_columns = list(X_Cols)
joblib.dump(rnd_columns, 'rnd_columns.pkl')
print("Random Forest Model Colums Saved")
joblib.dump(tfidf, 'tfidf.pkl')
print("Tfidf saved")


