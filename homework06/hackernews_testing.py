from db import News, session
import string
from bayes import NaiveBayesClassifier

from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer


def clean(s):
    translator = str.maketrans("", "", string.punctuation)
    return s.translate(translator)


s = session()
rows = s.query(News).filter(News.label != None).all()
X = [clean(row.title).lower() for row in rows]
y = [row.label for row in rows]

limit = int(len(rows) * 0.7)
X_train, y_train, X_test, y_test = X[:limit], y[:limit], X[limit:], y[limit:]

print('Testing my model...')
my_model = NaiveBayesClassifier(alpha=0.05)
my_model.fit(X_train, y_train)
print(my_model.score(X_test, y_test))

print('Testing sklearn...')
sk_model = Pipeline([
    ('vectorizer', TfidfVectorizer()),
    ('classifier', MultinomialNB(alpha=0.05)),
])
sk_model.fit(X_train, y_train)
print(sk_model.score(X_test, y_test))
