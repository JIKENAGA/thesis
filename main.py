import chessfunctions
import neuralnetwork
import torch
from sklearn.model_selection import train_test_split
import numpy as np

X = np.zeros(shape = [1000000, 6,2,8,8])
y = np.zeros(shape=[1000000])
X[0:100000] = np.load("/home/jikenaga2/data/xdata1.npy")
X[100000:200000] = np.load("/home/jikenaga2/data/xdata2.npy")
X[200000:300000] = np.load("/home/jikenaga2/data/xdata3.npy")
X[300000:400000] = np.load("/home/jikenaga2/data/xdata4.npy")
X[400000:500000] = np.load("/home/jikenaga2/data/xdata5.npy")
X[500000:600000] = np.load("/home/jikenaga2/data/xdata6.npy")
X[600000:700000] = np.load("/home/jikenaga2/data/xdata7.npy")
X[700000:800000] = np.load("/home/jikenaga2/data/xdata8.npy")
X[800000:900000] = np.load("/home/jikenaga2/data/xdata9.npy")
X[900000:1000000] = np.load("/home/jikenaga2/data/xdata10.npy")

y[0:100000] = np.load("/home/jikenaga2/data/ydata1.npy")
y[100000:200000] = np.load("/home/jikenaga2/data/ydata2.npy")
y[200000:300000] = np.load("/home/jikenaga2/data/ydata3.npy")
y[300000:400000] = np.load("/home/jikenaga2/data/ydata4.npy")
y[400000:500000] = np.load("/home/jikenaga2/data/ydata5.npy")
y[500000:600000] = np.load("/home/jikenaga2/data/ydata6.npy")
y[600000:700000] = np.load("/home/jikenaga2/data/ydata7.npy")
y[700000:800000] = np.load("/home/jikenaga2/data/ydata8.npy")
y[800000:900000] = np.load("/home/jikenaga2/data/ydata9.npy")
y[900000:1000000] = np.load("/home/jikenaga2/data/ydata10.npy")
print("loaded in data")
x_train, x_test, y_train, y_test = train_test_split(X,y , 
                                   random_state=104,  
                                   test_size=0.1,  
                                   shuffle=True)

x_train_tensor = torch.tensor(x_train)
x_test_tensor = torch.tensor(x_test)
y_train_tensor = torch.tensor(y_train)
y_test_tensor = torch.tensor(y_test)
print("split data")
model = neuralnetwork.NeuralNetwork4()

neuralnetwork.model_train(model, x_train_tensor, y_train_tensor, x_test_tensor, y_test_tensor)

torch.save(model.state_dict(), "/home/jikenaga2/model6")