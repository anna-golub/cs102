import csv
import string
from bayes import NaiveBayesClassifier

from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer


def clean(s):
    translator = str.maketrans("", "", string.punctuation)
    return s.translate(translator)


with open("SMSSpamCollection", encoding='utf8') as f:
    data = list(csv.reader(f, delimiter="\t"))

X, y = [], []
for target, msg in data:
    X.append(msg)
    y.append(target)
X = [clean(x).lower() for x in X]
X_train, y_train, X_test, y_test = X[:3900], y[:3900], X[3900:], y[3900:]

print('Testing my model...')
my_model = NaiveBayesClassifier(alpha=0.1)
my_model.fit(X_train, y_train)
print(my_model.score(X_test, y_test))

print('Testing sklearn...')
sk_model = Pipeline([
    ('vectorizer', TfidfVectorizer()),
    ('classifier', MultinomialNB(alpha=0.1)),
])
sk_model.fit(X_train, y_train)
print(sk_model.score(X_test, y_test))

