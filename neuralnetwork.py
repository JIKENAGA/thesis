import torch
import numpy as np
import chessfunctions
import copy
import numpy as np
import torch.nn as nn
import torch.optim as optim
import tqdm
import torch.nn.functional as F
import os


class NeuralNetwork(nn.Module):
    def __init__(self):
        super().__init__()
        
        #what does this mean? does this change our tensor into a single array?
        self.flatten = nn.Flatten()
        self.linear_relu_stack = nn.Sequential(
            nn.Linear(8*8*6*2, 1536),
            nn.ReLU(),
            nn.Linear(1536, 1000),
            nn.ReLU(),
            nn.Linear(1000, 500),
            nn.ReLU(),
            nn.Linear(500, 250),
            nn.ReLU(),
            nn.Linear(250, 100),
            nn.ReLU(),
            nn.Linear(100, 50),
            nn.ReLU(),
            nn.Linear(50, 20),
            nn.ReLU(),
            nn.Linear(20, 5),
            nn.ReLU(),
            nn.Linear(5,1),
            nn.Sigmoid()
            #do I need softmax here?
        )

    def forward(self, x):
        x = self.flatten(x)
        probs = self.linear_relu_stack(x)
        return probs

class NeuralNetwork2(nn.Module):
    def __init__(self):
        super().__init__()
        
        #what does this mean? does this change our tensor into a single array?
        self.flatten = nn.Flatten()
        self.linear_relu_stack = nn.Sequential(
            nn.Linear(8*8*6*2, 384),
            nn.ReLU(),
            nn.Linear(384, 192),
            nn.ReLU(),
            nn.Linear(192, 48),
            nn.ReLU(),
            nn.Linear(48, 24),
            nn.ReLU(),
            nn.Linear(24, 6),
            nn.ReLU(),
            nn.Linear(6, 2),
            nn.ReLU(),
            nn.Linear(2, 1),
            nn.Sigmoid()
            #do I need softmax here?
        )

    def forward(self, x):
        x = self.flatten(x)
        probs = self.linear_relu_stack(x)
        return probs

class NeuralNetwork3(nn.Module):
    def __init__(self):
        super().__init__()
        
        self.flatten = nn.Flatten()
        self.linear_relu_stack = nn.Sequential(
            nn.Linear(8*8*6*2, 700),
            nn.ReLU(),
            nn.Linear(700, 600),
            nn.ReLU(),
            nn.Linear(600, 1),
            nn.Sigmoid()
            #do I need softmax here?
        )

    def forward(self, x):
        x = self.flatten(x)
        probs = self.linear_relu_stack(x)
        return probs
    
class NeuralNetwork4(nn.Module):
    def __init__(self):
        super().__init__()
        
        self.flatten = nn.Flatten()
        self.linear_relu_stack = nn.Sequential(
            nn.Linear(8*8*6*2, 700),
            nn.ReLU(),
            nn.Linear(700, 600),
            nn.ReLU(),
            nn.Linear(600, 500),
            nn.ReLU(),
            nn.Linear(500, 1),
            nn.Sigmoid()
            #do I need softmax here?
        )

    def forward(self, x):
        x = self.flatten(x)
        probs = self.linear_relu_stack(x)
        return probs

def model_train(model, X_train, y_train, X_val, y_val):
    # loss function and optimizer
    print("begin training")
    loss_fn = nn.BCELoss()  # defines loss function
    optimizer = optim.Adam(model.parameters(), lr=0.0001) #this is our optimizer 
 
    n_epochs = 500   # number of epochs to run 
    batch_size = 100  # size of each batch 
    batch_start = torch.arange(0, len(X_train), batch_size) #so this starts the training?
 
    # Hold the best model
    best_acc = - np.inf   # init to negative infinity 
    best_weights = None 
 
    for epoch in range(n_epochs):
        print("start epoch:", epoch)
        model.train() #initiates training mode
        
        with tqdm.tqdm(batch_start, unit="batch", mininterval=0, disable=True) as bar:
            
            bar.set_description(f"Epoch {epoch}") #This prints out stuff
            
            for start in bar:
                # take a batch
                X_batch = X_train[start:start+batch_size] #what we are training on x wise
                y_batch = y_train[start:start+batch_size] #what we are training on y wise
                y_batch = y_batch.unsqueeze(1)
                # forward pass
                y_pred = model(X_batch.float()) # this predicts what it should be using the model

                loss = loss_fn(y_pred.float(), y_batch.float()) #this counts our error
                # backward pass

                optimizer.zero_grad() #this changes the weights? or initiates optimizer?
                
                loss.backward() #sets us in backwards mode?
                
                # update weights
                optimizer.step() #I guess this changes our weights
                
                # print progress
                acc = (y_pred.round() == y_batch.float()).float().mean()
                bar.set_postfix(
                    loss=float(loss),
                    acc=float(acc)
                )
                # if start//batch_size % 20 == 0:
                #     print(acc)
        # evaluate accuracy at end of each epoch
        #I guess all this just prints our current accuracy and isnt useful?
        print("finished going through batches")
        
        model.eval() #back to eval mode
        
        sumofvals = 0
        
        for start in range(0, len(X_val), batch_size):
            X_val_slice = X_val[start: min(len(X_val), start+batch_size)] #list of 100 things tensor
            y_val_slice = y_val[start:min(len(y_val), start+batch_size)] 
            
            y_pred = model(X_val_slice.float()) # predict our y again
            sumofvals += (y_pred.round() == y_val_slice).float().sum() # I guess still acc
        
        
        acc = float(sumofvals) / len(X_val)
        print("epoch Num:", epoch, "accuracy:", acc)
        if acc > best_acc:
            best_acc = acc
            best_weights = copy.deepcopy(model.state_dict())
    # restore model and return best accuracy
        print(epoch)
    model.load_state_dict(best_weights)
    return best_acc

def model_validate(model, X_val, y_val):
    batch_size = 100  # size of each batch 
    model.eval() #back to eval mode
        
    sumofvals = 0

    for start in range(0, len(X_val), batch_size):
        X_val_slice = X_val[start: min(len(X_val), start+batch_size)] #list of 100 things tensor
        y_val_slice = y_val[start:min(len(y_val), start+batch_size)] 

        y_pred = model(X_val_slice.float()) # predict our y again
        sumofvals += (y_pred.round() == y_val_slice).float().sum() # I guess still acc


    acc = float(sumofvals) / len(X_val)
    print(acc)
    return acc