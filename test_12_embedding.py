import torch
batch_size = 1
input_size = 4
hidden_size = 8
num_layers = 2
seq_len = 5
num_class = 4
embedding_size = 10

idx2char = ['e' , 'h' , 'l' , 'o']
x_data = [[1 , 0 , 2 , 2 , 3]]
y_data = [3 , 1 , 2 , 3 , 2]

inputs = torch.LongTensor(x_data)
labels = torch.LongTensor(y_data)

class Model(torch.nn.Module):
    def __init__(self):
        super(Model, self).__init__()
        self.emb = torch.nn.Embedding(input_size , embedding_size)  #input_size代表独热向量的维度
        self.rnn = torch.nn.RNN(input_size=embedding_size , hidden_size=hidden_size ,
                                num_layers=num_layers , batch_first=True)       #batch_first参数为True,使用是batch_size放前面
        self.fc = torch.nn.Linear(hidden_size , num_class)

    def forward(self , x):
        hidden = torch.zeros(num_layers , x.size(0) , hidden_size)
        x = self.emb(x)
        x , _ = self.rnn(x , hidden)
        x = self.fc(x)
        return x.view(-1 , num_class)

net = Model()

criterion = torch.nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(net.parameters() , lr=0.5)

for epoch in range(20):
    optimizer.zero_grad()
    outputs = net(inputs)
    loss = criterion(outputs , labels)
    loss.backward()
    optimizer.step()

    _ , idx = outputs.max(dim = 1)
    idx = idx.data.numpy()
    print('Predicted:',''.join([idx2char[x] for x in idx]) , end='')
    print(', Epoch [%d / 20] loss = %.4f' % (epoch+1 , loss.item()))