import torch
from torch import nn
import numpy as np
import pandas as pd 
from  torch.utils.data import Dataset, DataLoader
import os 


# logger 
from logpkg import get_logger
logger = get_logger(fileName="train", timeFlag=True)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("cuda" if torch.cuda.is_available() else "cpu")  



BATCHSIZE = 32
EPOCH = 50
LR = 0.0005
MODLE_NAME = "linear"
pretrained = False 
pretrained_weight_path = r""
weightDir = "."

# check 
if os.path.isdir(weightDir):
    print("weightDir exists")
else:
    raise Exception(f" {os.path.abspath(weightDir)} , weightDir Not exists")

if os.path.isdir(pretrained_weight_path):
    print("pretrained weight exists")
else:
    raise Exception(f" {os.path.abspath(pretrained_weight_path)} , pretrained weight Not exists")

def saveWeight(model, name=MODLE_NAME, weightDir=weightDir):
    path = os.path.join(weightDir, f"{name}.pth")
    torch.save(model.state_dict(), path)


############################# dataset #############################
dataset= Dataset() # """ !!!!!!!!!!!!!!!!!!!!! put your dataset """
dataloader = DataLoader(dataset=dataset, batch_size=BATCHSIZE, shuffle=True)


############################# model #############################
model = nn.Module()  # """ !!!!!!!!!!!!!!!!!!!!! some NN module your will train  """ 
if pretrained:
    model.load_state_dict(torch.load(pretrained_weight_path))
    logger.info("Use pretrained model")

model = model.to(device)
###################### optimizer, and lossfinction ######################

optimizer = torch.optim.Adam(model.parameters(), lr=LR)
loss_func = nn.MSELoss()

logger.info("Start to train")
logger.info(f"total epoch is {EPOCH}, batch size {BATCHSIZE}, learning rate {LR}, model name {MODLE_NAME}")


###################### training ######################
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


    
    
