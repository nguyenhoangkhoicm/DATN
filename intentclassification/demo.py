
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.svm import LinearSVC
import pickle
import os


class IntentClassifier:

    def __init__(self):
        self.data = pd.read_csv('./intentclassification/data1.csv')
        if os.path.exists('./intentclassification/model/count_vect.pkl') and os.path.exists('./intentclassification/model/tfidf_transformer.pkl') and os.path.exists('./intentclassification/model/svm.pkl'):
            with open('./intentclassification/model/count_vect.pkl', 'rb') as f:
                self.count_vect = pickle.load(f)
            with open('./intentclassification/model/tfidf_transformer.pkl', 'rb') as f:
                self.tfidf_transformer = pickle.load(f)
            with open('./intentclassification/model/svm.pkl', 'rb') as f:
                self.svm = pickle.load(f)
        else:
            self.train()
        
    def train(self):
        X_train, y_train = self.data['text'], self.data['intent']
        self.count_vect = CountVectorizer()
        X_train_counts = self.count_vect.fit_transform(X_train)
        self.tfidf_transformer = TfidfTransformer()
        X_train_tfidf = self.tfidf_transformer.fit_transform(X_train_counts)
        self.svm = LinearSVC().fit(X_train_tfidf, y_train)

        # Lưu count_vect, tfidf_transformer và svm vào tệp
        with open('count_vect.pkl', 'wb') as f:
            pickle.dump(self.count_vect, f)
        with open('tfidf_transformer.pkl', 'wb') as f:
            pickle.dump(self.tfidf_transformer, f)
        with open('svm.pkl', 'wb') as f:
            pickle.dump(self.svm, f)

    def predict(self, input_sentence):
        X_input_counts = self.count_vect.transform([input_sentence])
        X_input_tfidf = self.tfidf_transformer.transform(X_input_counts)
        predicted_label = self.svm.predict(X_input_tfidf)[0]
        return predicted_label


intent_classifier = IntentClassifier()
predicted_label = intent_classifier.predict("mình muốn xem lịch học mới nhất")
print(predicted_label)

"""
Đối tượng count_vect là một đối tượng CountVectorizer đã được huấn luyện để chuyển đổi văn bản thành ma trận đếm. Bạn cần lưu đối tượng này vào tệp để sử dụng nó trong quá trình dự đoán để chuyển đổi câu đầu vào thành ma trận đếm.
Đối tượng tfidf_transformer là một đối tượng TfidfTransformer đã được huấn luyện để chuyển đổi ma trận đếm thành ma trận TF-IDF. Bạn cần lưu đối tượng này vào tệp để sử dụng nó trong quá trình dự đoán để chuyển đổi ma trận đếm của câu đầu vào thành ma trận TF-IDF.
Đối tượng svm là một mô hình SVM đã được huấn luyện để dự đoán nhãn cho ma trận TF-IDF. Bạn cần lưu đối tượng này vào tệp để sử dụng nó trong quá trình dự đoán để dự đoán nhãn cho ma trận TF-IDF của câu đầu vào.
"""
