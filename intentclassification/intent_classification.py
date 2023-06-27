
import numpy as np
import pandas as pd
import pickle
import os

from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from imblearn.over_sampling import RandomOverSampler
from sklearn.svm import LinearSVC


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

        # Kiểm tra và xử lý dữ liệu thiếu, loại bỏ dòng trùng lặp
        self.data = self.data.drop_duplicates().dropna()

        # Xử lý mất cân bằng dữ liệu
        oversampler = RandomOverSampler()
        X_train_resampled, y_train_resampled = oversampler.fit_resample(
            X_train.values.reshape(-1, 1), y_train)

        self.count_vect = CountVectorizer()
        X_train_counts = self.count_vect.fit_transform(
            X_train_resampled.ravel())

        self.tfidf_transformer = TfidfTransformer()
        X_train_tfidf = self.tfidf_transformer.fit_transform(X_train_counts)

        self.svm = LinearSVC().fit(X_train_tfidf, y_train_resampled)

        # Lưu count_vect, tfidf_transformer và svm vào tệp
        with open('./intentclassification/model/count_vect.pkl', 'wb') as f:
            pickle.dump(self.count_vect, f)
        with open('./intentclassification/model/tfidf_transformer.pkl', 'wb') as f:
            pickle.dump(self.tfidf_transformer, f)
        with open('./intentclassification/model/svm.pkl', 'wb') as f:
            pickle.dump(self.svm, f)

    def predict(self, input_sentence):
        X_input_counts = self.count_vect.transform([input_sentence])
        X_input_tfidf = self.tfidf_transformer.transform(X_input_counts)
        confidence = self.svm.decision_function(X_input_tfidf)[0]
        # Ngưỡng để quyết định câu được chấp nhận hay không
        threshold = 0.2  
        if np.any(confidence >= threshold):
            predicted_label = self.svm.predict(X_input_tfidf)[0]
        else:
            predicted_label = "none"  

        return predicted_label
    
    def evaluate(self, test_set):
        correct = 0
        total = len(test_set)

        for input_sentence, true_label in test_set:
            predicted_label = self.predict(input_sentence)
            if predicted_label == true_label:
                correct += 1

        accuracy = correct / total
        return accuracy


intent_classifier = IntentClassifier()

# test_set = [("bạn có thể cho mình xem lích học mới nhất được không", "schedule"),
#             ("trường có bao nhiêu phong ban", "department"),
#             ("làm sao để đăng ký học bổng", "scholarship")]
# for input_sentence, true_label in test_set:
#     predicted_label = intent_classifier.predict(input_sentence)
#     if predicted_label == true_label:
#         print("Input sentence:", input_sentence)
#         print("True label:", true_label)
#         print("Predicted label:", predicted_label)
#         print("Accuracy: 1.0\n")
#     else:
#         print("Input sentence:", input_sentence)
#         print("True label:", true_label)
#         print("Predicted label:", predicted_label)
#         print("Accuracy: 0.0\n")