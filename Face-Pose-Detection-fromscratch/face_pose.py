# -*- coding: utf-8 -*-
"""Face_Pose.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1lqUXU6fYWMHly4-Q5yBBovJwBLsd8F-x

**In this The libraries we have used are os,numpy,random,google.colab**
"""

import os
import numpy as np
import random
from google.colab import drive

drive.mount('/content/drive')

"""**This Cell consists of a function named read_pgm**
**.The use of this function is dataset preparation**
"""

def read_pgm(pgmf):
    pgmf.readline()
    #pgmf.readline()
    #pgmf.readline()
    (width, height) = [int(i) for i in pgmf.readline().split()]
    depth = int(pgmf.readline())
    #print(pgmf.readline())
    raster=[]
    for i in range(960):    #Loop iterates to extract the pixels
        cherry=[int(j) for j in pgmf.readline().split()]
        raster.append(cherry)
    gopi=[]
    for i in range(len(raster)):
        for j in range(len(raster[i])):
            gopi.append(raster[i][j])
    return gopi

# Get the list of all files and directories
path = "/content/drive/MyDrive/ML Project/faces" # Original path
path_copy="/content/drive/MyDrive/ML Project/faces"  # Copy of the path

dir_list = os.listdir(path) # retrieves all the sub-folders

print("Files and directories in ", path, " :") # This will show the current path of directory

del dir_list[0] # This will deletes the Anchor file which is not useful

print("The total no: of subfolders/users in face folder are:",len(dir_list))
print(dir_list) # This is used to print all the sub-folders in the file "Faces"

final=[]
total=0
for i in range(len(dir_list)):  #Loop iterates over all the sub-folders/users

    path_copy=path_copy+'/'+dir_list[i] # This is path setting for i th subfolder
    pt=os.listdir(path_copy)    # Retrives all the pictures in the sub-folder

    for x in pt:    # Loop iterates over all the pictures
        if x.endswith('.bad') or x.endswith('2.pgm') or x.endswith('4.pgm') or x.endswith(').pgm'):#Filtering of all pictures and retriving only the pictures with extension .pgm
            total=total+1
        else:
            final.append(path_copy+'/'+x)
            total=total+1

    #print(path_copy)
    path_copy=path_copy[::-1]
    #print(path_copy)
    index=path_copy.find('/')
    path_copy=path_copy[index+1::]
    path_copy=path_copy[::-1]

print("The total no: of files in the folder faces is :",total)  # This will print the total no: of files in the folder faces
print("The no: of Userfiles with extension .pgm only are: ",len(final)) # This will print the total no: of useful files with extension .pgm in the folder faces
print("The list of User files with the extension .pgm only are :")  # This will print the list of useful files with extension .pgm
for i in range(len(final)):
  print(final[i])


X=[]    # Input matrix for all the pictures in pixels
y=[]    # Output matrix for all the pictures with directions

for i in range(len(final)):
    #print(final[i]) # This gives the path for i th user in the list format
    s=str(final[i]) # Converts the list item into string item
    #print(s)    # This gives the path for i th user in the string format

    f = open(s, 'rb')   # This will opens the i th user folder
    X.append(read_pgm(f))   # Takes the input as pixels from the i th user image

    if final[i].find('left')!=-1:
        output=[1,0,0,0]    # The picture is Left turned
    elif final[i].find('right')!=-1:
        output=[0,1,0,0]    # The picture is Right turned
    elif final[i].find('up')!=-1:
        output=[0,0,1,0]    # The picture is Up turned
    else:
        output=[0,0,0,1]    # The picture is Straight turned
    y.append(output)

layers=[len(X[0])]  #Taking the no: of nodes in input layer
print("The Total no: of nodes in input layer are :",len(X[0]))  #This will print the total no: of nodes in input layer

"""**Layer Class**"""

class layer:    # Layer class

    def __init__(self,no_inputs,no_neurons):
        self.weights = np.random.rand(no_inputs, no_neurons) # Generating random weights for a weight matrix in a layer
        self.biases = np.zeros((1, no_neurons)) # Generating zeroes for a bias matrix in a layer

    def act_func(self, x):  # Activation Function for each layer
        #self.type=random.randint(0,1)
        #if self.type==0:
          return 1 / (1 + np.exp(-x)) # Sigmoid Activation Function
        #else:
          #return np.tanh(x) # Tanh Activation Function

    def deact_func(self,x): # De-activation function for each layer

        #if self.type==0:
          return x * (1 - x) # Sigmoid De-activation Function
        #else:
          #return 1-np.tanh(x)**2 # Tanh De-activation Function

"""**Neural Network Class**"""

class neural_network:   # Neural-Network Class

    def __init__(self,l):
        self.l = l

    def predict(self,input):
        a = np.array([input])
        for i in range(len(self.l)):
            z = np.dot(a, self.l[i].weights) + self.l[i].biases
            a = self.l[i].act_func(z)
        '''sum=0
        for i in range(len(a[-1])):
          sum=sum+np.exp(a[-1][i])
        for i in range(len(a[-1])):
          a[-1][i]=a[-1][i]/sum'''
        return a[-1]

    def train(self,input,original,alpha):

        a=[np.array([input])]  # Taking the input matrix

        # Forward Propagation Starts
        for i in range(len(self.l)):    # Loops iterates over all the layers
            Z=np.array(np.dot(a[-1],self.l[i].weights)+self.l[i].biases)
            #print(Z)
            a.append(self.l[i].act_func(Z))


        error=np.array([original])-a[-1]    # Difference between the original and predicted values
        #error=(error**2)/2  # Mean Square Error


        # Backward Propagation Starts
        delta_w=[np.dot(np.transpose(a[-2]),error*self.l[-1].deact_func(a[-1]))] # delta_w Matrix
        for i in range(len(self.l)-2,-1,-1): # Loop iterates from last but one to first layer
            z=np.dot(error*self.l[-1].deact_func(a[-1]),np.transpose(self.l[-1].weights))
            for j in range(len(self.l)-2,i,-1): # Loop iterates from last but two to i th layer
                z=z*self.l[j].deact_func(a[j+1])
                z=np.dot(z,np.transpose(self.l[j].weights))
            z=z*self.l[i].deact_func(a[i+1])
            z=np.dot(np.transpose(a[i]),z)

            delta_w.append(z)


        delta_w.reverse()   # Matrix is reversed to calculate the change in weights of weight matrix of every layer

        delta_b=[]
        #c=np.array(delta_w)
        delta_wcopy=delta_w.copy()
        for i in range(len(delta_wcopy)):
          go=np.array([delta_wcopy[i].sum(axis=0)])
          delta_b.append(go)

        # Updating the weights
        for i in range(len(self.l)):    # Loop iterates for all the layers
            self.l[i].weights=self.l[i].weights + alpha * delta_w[i]    # Weights are adjusted for every layer
            self.l[i].biases=self.l[i].biases + alpha * delta_b[i]      # Bias Weights are adjusted for every layer

#Declare the No: of Hidden Layers
inp=int(input("No: of Hidden Layers:"))

print("Enter the no: of nodes in ",inp," Hidden layers")    #Taking the input of no: of nodes in hidden layers

for i in range(inp):
    print("Enter the no: of nodes in hidden layer ",i+1,": ",end='')  #Taking the no: of nodes in ith hidden layer
    layers.append(int(input()))


layers.append(len(y[0]))    #Taking the no: of nodes in output layer


l=[]    #Declaring the list for all layer objects


for i in range(1,len(layers)):  #Creating the object for individual layers except the input layer
    l.append(layer(layers[i-1],layers[i]))


nn=neural_network(l)    #Creating the Neural Network object
iterations=1  #No: of Iterations
alpha=0.1   # Value of alpha


X_train=X[0:500]    # Training Data-set with inputs
Y_train=y[0:500]    # Training Data-set with outputs

#print(X_train[0])
#print(Y_train[0])
X_train=np.array(X_train)
#print(X_train[0])
#print([np.array([X_train[0]])])
Y_train=np.array(Y_train)
#print(Y_train[0])

for i in range(iterations): # Loop executes for all iterations
    for j in range(len(X_train)): # Loop executes for all the inputs
        nn.train(X_train[j],Y_train[j],alpha)   #Neural network trains the model for each input
    print(i)

X_test=X[500:624]   # Testing Data-set with inputs
Y_test=y[500:624]   # Testing Data-set with outputs

X_test=np.array(X_test)
Y_test=np.array(Y_test)
#print(X_test[0])
for i in range(len(X_test)):    # Loop executes for all the test Data-set
    print(nn.predict(X_test[i]))  # Output the value obtained at the end