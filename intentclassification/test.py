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


import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Ba vector
vector1 = [0.5, 0.6, 0.7]
vector2 = [0.8, 0.3, 0.9]
vector3 = [0.2, 0.9, 0.4]

# Tạo biểu đồ 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Điểm và đường nối cho vector 1
ax.scatter(vector1[0], vector1[1], vector1[2], color='red', label='Vector 1')
ax.plot([0, vector1[0]], [0, vector1[1]], [0, vector1[2]], 'r--', label='Đường nối 1')

# Điểm và đường nối cho vector 2
ax.scatter(vector2[0], vector2[1], vector2[2], color='green', label='Vector 2')
ax.plot([0, vector2[0]], [0, vector2[1]], [0, vector2[2]], 'g--', label='Đường nối 2')

# Điểm và đường nối cho vector 3
ax.scatter(vector3[0], vector3[1], vector3[2], color='blue', label='Vector 3')
ax.plot([0, vector3[0]], [0, vector3[1]], [0, vector3[2]], 'b--', label='Đường nối 3')

# Cài đặt các nhãn trục
ax.set_xlabel('Trục X')
ax.set_ylabel('Trục Y')
ax.set_zlabel('Trục Z')

# Hiển thị biểu đồ
plt.legend()
plt.show()
