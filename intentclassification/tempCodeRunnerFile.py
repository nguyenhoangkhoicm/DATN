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
