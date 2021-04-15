import torch
from torch import nn
import numpy as np
import pandas as pd 
from  torch.utils.data import Dataset, DataLoader
import os 


# logger 
from logpkg import get_logger
logger = get_logger(fileName="eval", timeFlag=True)

# if you want to eval in cpu , directly se device in cpu
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("your device is", "cuda" if torch.cuda.is_available() else "cpu")  



BATCHSIZE = 32
EPOCH = 50
LR = 0.0005
MODLE_NAME = "linear"
pretrained = False 
pretrained_weight_path = r""

def saveWeight(model, name=MODLE_NAME, weightDir="."):
    path = os.path.join(weightDir, f"{name}.pth")
    torch.save(model.state_dict(), path)


# define dataset and loder 
dataset=Dataset()
dataloader = DataLoader(dataset=dataset, batch_size=BATCHSIZE, shuffle=True)


# model
model = nn.Module() # some NN module your will train 
if pretrained:
    model.load_state_dict(torch.load(pretrained_weight_path))
    logger.info("Use pretrained model")

# optimizer, and lossfinction
optimizer = torch.optim.Adam(model.parameters(), lr=LR)
loss_func = nn.MSELoss()

logger.info("Start to train")
logger.info(f"total epoch is {EPOCH}, batch size {BATCHSIZE}, learning rate {LR}, model name {MODLE_NAME}")


model.eval()
avg_loss = 0

# -------------------------------
# another is put this loop into 
# with torch.no_grad():
#   .... some code 
# -------------------------------
for data ,label in dataloader:
    
    optimizer.zero_grad()
    output = model(data.to(device))
    loss = loss_func(torch.squeeze(output), label.to(device))

    avg_loss += loss.data.numpy()

avg_loss = avg_loss/len(dataset)


''' some graph 
plt.plot(gt_lt, color='r',alpha=0.5)
plt.plot(pre_lt, color="b")

plt.savefig(f"eval_{MODLE_NAME}.png")
logger.info(f"loss={avg_loss/len(dataset):.4f}")
'''