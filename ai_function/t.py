
import matplotlib.pyplot as plt

vector = [0.37796, 0.37796, 0.37796, 0.37796, 0.37796, 0.37796, 0.37796, 0, 0, 0,0,0]

# Tạo một list chứa các số từ 0 đến 9 để làm trục x
x = list(range(12))

# Vẽ biểu đồ đường
plt.plot(x, vector)

# Đặt tên cho trục x và trục y
plt.xlabel('Index')
plt.ylabel('Value')

# Hiển thị biểu đồ
plt.show()
