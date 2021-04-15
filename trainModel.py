import torch
from torch import nn
import numpy as np
import pandas as pd 
from  torch.utils.data import Dataset, DataLoader
import os 


# logger 
from logpkg import get_logger
logger = get_logger(fileName="train")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("cuda" if torch.cuda.is_available() else "cpu")  



BATCHSIZE = 32
EPOCH = 50
LR = 0.0005
MODLE_NAME = "linear"

def saveWeight(model, name=MODLE_NAME, weightDir="."):
    path = os.path.join(weightDir, f"{name}.pth")
    torch.save(model.state_dict(), path)


# define dataset and loder 
dataset=Dataset()
dataloader = DataLoader(dataset=dataset, batch_size=BATCHSIZE, shuffle=True)


# model, optimizer, and lossfinction
model = nn.Module() # some NN module your will train 
optimizer = torch.optim.Adam(model.parameters(), lr=LR)
loss_func = nn.MSELoss()

logger.info("Start to train")
logger.info(f"total epoch is {EPOCH}, batch size {BATCHSIZE}, learning rate {LR}, model name {MODLE_NAME}")

for epoch in range(EPOCH):
    model.train()
    avg_loss = 0
    for data ,label in dataloader:
        
        optimizer.zero_grad()
        output = model(data.to(device))
        loss = loss_func(torch.squeeze(output), label.to(device))

        
        loss.backward()
        optimizer.step()
        avg_loss += loss
        
        # logger.debug(f"epoch {epoch}, loss={avg_loss:.10f}")
    avg_loss = avg_loss/len(dataset)

    if avg_loss < 0.0005 or epoch > 30:
        saveWeight(model, name=f"{MODLE_NAME}_{epoch}")
    logger.info(f"epoch {epoch}, loss={avg_loss:.10f}")

saveWeight(model)


    
    
