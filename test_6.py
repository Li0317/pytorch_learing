
#import torch.nn.functional as F
#使用torch.nn.functional里面的sigmoid函数可以运行但是会提示错误，因为nn.functional.sigmoid将被弃用
#最好使用torch.sigmoid
import torch
import numpy as np
import matplotlib.pyplot as plt

x_data = torch.Tensor([[1.0] , [2.0] , [3.0]])
y_data = torch.Tensor([[0] , [0] , [1]])

class LogisticRegressionModel(torch.nn.Module):         #逻辑斯蒂回归模块
    def __init__(self):
        super(LogisticRegressionModel, self).__init__()
        self.linear = torch.nn.Linear(1,1)      #此处linear函数在test_5中有详细解释

    def forward(self , x):
        y_pred = torch.sigmoid(self.linear(x))      #F.sigmoid为σ(x) = 1/(1+ｅ^(-x))，其值在[0,1]，为饱和函数
        #y_pred = F.sigmoid(self.linear(x))
        return y_pred

model = LogisticRegressionModel()

criterion = torch.nn.BCELoss(reduction='mean')       #BCE损失计算，loss = -(ylog y_pred + (1-y)log(1-y_pred))
                                # 关于reduction参数见test_5里的注释

optimizer = torch.optim.SGD(model.parameters() , lr= 0.01)

for epoch in range(1000):
    y_pred = model(x_data)
    loss = criterion(y_pred , y_data)

    print("epoch:" , epoch , "loss:" , loss.item())
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

print("w = " , model.linear.weight.item())
print("b = " , model.linear.bias.item())

x = np.linspace(0 , 10 , 200)   #从0到10等距取200个
x_test = torch.Tensor(x).view((200,1))      #生成200行1列的矩阵
y_test = model(x_test)
y = y_test.data.numpy()     #tensor转换为numpy

plt.plot(x , y)
plt.plot([0 , 10] , [0.5 , 0.5] , c = 'r')      #做一条垂直于y轴的直线，颜色为red。[0,x][y,y]
                                                #垂直于x轴的直线,[x,x][0,y]
plt.xlabel("Hours")
plt.ylabel("Probability of pass")
plt.grid()      #画出表格
plt.show()