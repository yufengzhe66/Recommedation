# -*- coding: utf-8 -*-
"""
Created on 2018/04/19

@author: Quincy Xue
"""



def writeTofile(u_id,b_id,rate):
    fr = open('C:/Users/Dell/.spyder-py3/project_recommendation/base/rateFile.data','a')
    string = str(u_id)+'\t'+str(b_id)+'\t'+str(rate)+'\n'
    fr.writelines(string)
    fr.close()


def loadFile():
    dataMat = dict()
    
    amount = 0
    res = 0
    fr = open(r'C:/Users/Dell/.spyder-py3/project_recommendation/base/rateFile.data')
    for line in fr.readlines():
        amount = amount+1
        lineArr = line.strip().split('\t')  
#        dataMat.append([int(lineArr[0]), int(lineArr[1]),float(lineArr[2])])
        res+=float(lineArr[2])
        dataMat.setdefault(int(lineArr[0]),[]).append([int(lineArr[1]),float(lineArr[2])])
    fr.close()
    
   
    return dataMat,res/amount


