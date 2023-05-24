
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.svm import LinearSVC
import pickle
import os
from transformers import BertTokenizer, BertModel
import torch
import numpy as np

class IntentClassifier:
    def __init__(self):
        self.data = pd.read_csv('./intentclassification/data1.csv')
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        self.model = BertModel.from_pretrained('bert-base-uncased')
        if os.path.exists('./intentclassification/model/svm.pkl'):
            with open('./intentclassification/model/svm.pkl', 'rb') as f:
                self.svm = pickle.load(f)
        else:
            self.train()

    def extract_features(self, text):
        input_ids = self.tokenizer.encode(text, return_tensors='pt')
        with torch.no_grad():
            last_hidden_states = self.model(input_ids)[0]
        return last_hidden_states[:,0,:].numpy().reshape(1, -1)

    def train(self):
        X_train, y_train = self.data['text'], self.data['intent']
        X_train_features = np.concatenate([self.extract_features(text) for text in X_train])
        self.svm = LinearSVC().fit(X_train_features, y_train)

        # Lưu svm vào tệp
        with open('./intentclassification/model/svm.pkl', 'wb') as f:
            pickle.dump(self.svm, f)


    def predict(self, input_sentence):
        X_input_features = self.extract_features(input_sentence)
        predicted_label = self.svm.predict(X_input_features)[0]
        return predicted_label

intent_classifier = IntentClassifier()
predicted_label = intent_classifier.predict("mình không cần xem điểm số mình cần xem lịch học")
print(predicted_label)

