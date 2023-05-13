import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.svm import LinearSVC
import matplotlib.pyplot as plt

class IntentClassifier:
    def __init__(self):

        self.data = pd.read_csv('./intentclassification/data1.csv')
       
        self.train()
        
    def train(self):

        X_train, y_train = self.data['text'], self.data['intent']
        self.count_vect = CountVectorizer()
        X_train_counts = self.count_vect.fit_transform(X_train)
        tfidf_transformer = TfidfTransformer()
        X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
        self.svm = LinearSVC().fit(X_train_tfidf, y_train)

    def predict(self, text):
        text_vector = self.count_vect.transform([text])
        predicted_intent = self.svm.predict(text_vector)[0]
        plt.plot(text_vector.toarray()[0])
        plt.title(f"Input: {text} | Predicted intent: {predicted_intent}")
        # plt.xlabel("Số chiều")
        # plt.ylabel("Độ chính xác")
        plt.show()
        return predicted_intent

intent_classifier = IntentClassifier()
prediction = intent_classifier.predict("Tôi muốn biết học phí của Trường được đóng như thế nào")
print("Kết quả phân loại:", prediction)


