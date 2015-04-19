# coding=gbk
'''
Created on 2015年4月18日

@author: Blunce
'''

import random
import math
import matplotlib.pyplot as plt

PRECISION = 6
FATHER, SON = 100, 100  # (FATHER + SON)
ITERATE_NUM = 100
RATE = 0.2  # 突变在子代中发生的概率

def f(x1, x2):
    return (x2 - 5.1 / (4 * math.pi ** 2) * x1 ** 2 + 5 * x1 / math.pi - 6) ** 2 + 10.0 * (1 - 1 / math.pi) * math.cos(x1) + 10.0

def numToStr(x, y):
    # 返回字符串
    x, y = x * 10 ** PRECISION, y * 10 ** PRECISION
    if x >= 0:
        xstr = '0' + bin(int(x))
    else:
        xstr = '1' + bin(abs(int(x)))
        
    if y >= 0:
        ystr = '0' + bin(int(y))
    else:
        ystr = '1' + bin(abs(int(y)))
        
    if 26 - len(xstr) != 0:
        xstr = xstr[:3] + '0' * (26 - len(xstr)) + xstr[3:]
    if 26 - len(ystr) != 0:
        ystr = ystr[:3] + '0' * (26 - len(ystr)) + ystr[3:]
        
    return xstr + ',' + ystr


def strToNum(aim):
    aim = aim.split(',')
    if aim[0][0] == '0':
        aim[0] = aim[0][1:]
    else:
        aim[0] = '-' + aim[0][1:]
    if aim[1][0] == '0':
        aim[1] = aim[1][1:]
    else:
        aim[1] = '-' + aim[1][1:]
    return [int(aim[0], 2) / float(10 ** PRECISION), int(aim[1], 2) / float(10 ** PRECISION)]
   
   
def encode(dataSet):
    aimList = []
    for item in dataSet:
        aimList.append(numToStr(item[0], item[1]))
    return aimList


def decode(dataSet):
    aimList = []
    for item in dataSet:
        aimList.append([strToNum(item)[0], strToNum(item)[1], f(strToNum(item)[0], strToNum(item)[1])])
    return aimList


def InitialGen():
    sons = []
    for i in range(FATHER):
        sons.append([random.uniform(-5, 5), random.uniform(-5, 5)])
    return sons


def recombination(dataSet):
    sonDataSet = []
    for i in range(SON / 2):
        random.shuffle(dataSet)
        fa1 = list(dataSet[0])
        fa2 = list(dataSet[1])
        
        if random.randint(0, 1) == 1:
            # 符号重组
            fa1[0], fa2[0] = fa2[0], fa1[0]
        
        # 数值部分重组    
        head = random.randint(3, 24)
        rear = random.randint(head + 1, 25)
        fa1[head:rear], fa2[head:rear] = fa2[head:rear], fa1[head:rear]
        
        if random.randint(0, 1) == 1:
            # 符号重组
            fa1[27], fa2[27] = fa2[27], fa1[27]
            
        # 数值部分重组            
        head = random.randint(30, 51)
        rear = random.randint(head, 52)
        fa1[head:rear], fa2[head:rear] = fa2[head:rear], fa1[head:rear]
        
        fa1 = ''.join(fa1)
        fa2 = ''.join(fa2)
        sonDataSet.extend([fa1, fa2])
    return sonDataSet


def mutation(dataSet):
    random.shuffle(dataSet)
    for i in range(int(SON * RATE)):
        temp = range(0, 53)
        del temp[29]  # 1, 2, 26, 28, 29
        del temp[28]
        del temp[26]
        del temp[2]
        del temp[1]
        random.shuffle(temp)
        aim = dataSet[i]
        aim = list(aim)
        aim[temp[0]] = str((int(aim[temp[0]]) + 1) % 2)
        dataSet[i] = ''.join(aim)
    return dataSet


def produceNextGen(dataSet):
    sonDataSet = recombination(dataSet)
    sonDataSet = mutation(sonDataSet)
    dataSet.extend(sonDataSet)
    return dataSet

def deleteAbnormal(dataSet):
    aim = []
    for i in range(len(dataSet)):
        if dataSet[i][0] > 5 or dataSet[i][0] < -5 or dataSet[i][1] > 5 or dataSet[i][1] < -5:
            aim.append(i)
    aim = aim[::-1]
    print aim
    for item in aim:
        del dataSet[item]
    return dataSet

def NaturalSelection(dataSet):
    dataSet = decode(dataSet)
    dataSet = deleteAbnormal(dataSet)
    dataSet = sorted(dataSet, key=lambda x:x[2], reverse=False)
    dataSet = dataSet[:FATHER][:]
    return encode(dataSet)
    

def Label(dataSet):
    # 用平均值和标准差表示变化
    import numpy as np 
    dataSet = decode(dataSet)
    dataSet = np.array(dataSet)
    dataSet = dataSet[:][2]
    return  np.mean(dataSet)   ,np.std(dataSet)

    
if __name__ == '__main__':
    dataSet = encode(InitialGen())
    y = []
    for i in range(ITERATE_NUM):
        print i
        dataSet = produceNextGen(dataSet)
        dataSet = NaturalSelection(dataSet)
        y.append(Label(dataSet))
        
    
    x = range(1, ITERATE_NUM + 1)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(x, y)
    print 'save result'
    fig.savefig('result.jpg')
    print 'end'
