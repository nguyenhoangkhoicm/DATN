import pandas as pd
import openpyxl
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score,f1_score


class IntentClassifier:
    def __init__(self):
        self.data = pd.read_csv('./intentclassification/data1.csv')
        self.train()

    def train(self):
        X_train, y_train = self.data['text'], self.data['intent']
        self.count_vect = CountVectorizer(ngram_range=(1,2), max_df=0.8, min_df=2)
        X_train_counts = self.count_vect.fit_transform(X_train)
        self.tfidf_transformer = TfidfTransformer()
        X_train_tfidf = self.tfidf_transformer.fit_transform(X_train_counts)
        self.svm = LinearSVC(C=0.1).fit(X_train_tfidf, y_train)
       
    def print_input_vector(self, text): 
        input_vector = self.count_vect.transform([text]) 
        input_tfidf = self.tfidf_transformer.transform(input_vector)
        return input_tfidf
    
    def evaluate(self, X_test, y_test):
         X_test_counts = self.count_vect.transform(X_test) 
         tfidf_transformer = TfidfTransformer() 
         X_test_tfidf = tfidf_transformer.fit_transform(X_test_counts) 
         y_pred = self.svm.predict(X_test_tfidf) 
         accuracy = accuracy_score(y_test, y_pred) 
         f1 = f1_score(y_test, y_pred, average='weighted') 
         print(f'Accuracy: {accuracy}') 
         print(f'F1-score: {f1}')

    def predict(self, text):
        return self.svm.predict(self.count_vect.transform([text]))[0]

intent_classifier = IntentClassifier()


# test_sentence = "Tôi muốn biết học phí của Trường được đóng như thế nào"
# test_intent = "tuition"


input_vector = intent_classifier.print_input_vector("Tôi muốn biết học phí của Trường được đóng như thế nào")

print("Vector của câu đầu vào:", input_vector.toarray())

X_test = ['Tôi muốn biết học phí của Trường được đóng như thế nào']
y_test = ['tuition'] 
prediction = intent_classifier.predict("Tôi muốn biết học phí của Trường được đóng như thế nào")

print("Dữ liệu kiểm tra",X_test)
print("Kết quả phân loại:", prediction)
intent_classifier.evaluate(X_test, y_test)
# X_test = ['Tôi muốn biết học phí của Trường được đóng như thế nào',          'Cơ cấu tổ chức phòng ban trong trường đại học là gì',          'Bạn xem giúp mình lịch học với',          'Tôi muốn xem bảng điểm của mình',          'Làm thế nào để tính GPA',          'Làm thế nào để liên lạc với các phòng ban'          ] 

# y_test = ['tuition','department','schedule','pointlookup','point','department'] 

# results = []
# for i in range(len(X_test)):
#     prediction = intent_classifier.predict(X_test[i])
#     accuracy = accuracy_score([y_test[i]], [prediction])
#     f1 = f1_score([y_test[i]], [prediction], average='weighted')
#     results.append({"Sentence": X_test[i], "Prediction": prediction, "Accuracy": accuracy, "F1-score": f1})

# df = pd.DataFrame(results)
# df.to_excel("predictions.xlsx", index=False)




