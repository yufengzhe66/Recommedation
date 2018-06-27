# -*- coding: utf-8 -*-
"""
Created on 2018/04/19

@author: Quincy Xue
"""
"""
评分平均值:ave
偏移向量:bu[NumUser],bi[NumBook]
特征量参数:k
隐因子矩阵:qi[NumBook][k],pu[NumUser][k]
表示对项目有过操作行为的客户的特征向量:y[NumBook][k]
"""
import numpy as np
import math
import sys
from sqlalchemy import func
sys.path.append(r'C:\Users\Dell\.spyder-py3\project_recommendation\base')

import fileOperation
import sqlModel

def init():
    dim = 30
    sqlsession = sqlModel.DBSession()
    NumUser = sqlsession.query(func.count(sqlModel.User.u_id)).scalar()
    NumBook = sqlsession.query(func.count(sqlModel.Book.b_id)).scalar()
    sqlsession.close()
    amount = max(NumUser,NumBook)
    
    bu=np.zeros((amount),np.double)+0.01
    bi=np.zeros((amount),np.double)+0.01
    pu=np.zeros((amount,dim),np.double)+0.01
    qi=np.zeros((amount,dim),np.double)+0.01
    y=np.zeros((amount,dim),np.double)+0.01
    z=np.zeros((amount,dim),np.double)
    
    train_ui = dict()
    
    train_ui,ave = fileOperation.loadFile()
    
    return ave,bu,bi,pu,qi,y,train_ui,z,amount





def SVDPlusPlus():
    ave,bu,bi,pu,qi,y,train_ui,z,amount=init()
    alpha = 0.007
    lamda = 0.007
    train_ui = dict()

    train_ui,ave = fileOperation.loadFile()
    for step in range(1,101):
        for u,item in train_ui.items():    
            nu = len(item)
            ru = 1/(math.sqrt(nu))
            for i,rui in item:
                z[u]+=y[i]*ru
    
            for i,rui in item:
                e_ui=rui-ave-bu[u]-bi[i]-np.dot(qi[i],(pu[u]+z[u]).T)
                bu[u]+=alpha*(e_ui-lamda*bu[u])
                bi[i]+=alpha*(e_ui-lamda*bi[i])
            #for k in range(0,dim):
                pu[u]+=alpha*(qi[i]*e_ui-lamda*pu[u])
                qi[i]+=alpha*((pu[u]+z[u])*e_ui-lamda*qi[i])
                y[i]+=alpha*(qi[i]*ru*e_ui-lamda*y[i])
        print(step,np.dot((qi[i]+z[u]).T,pu[u]))
        alpha*=0.9                        
    return ave,bu,bi,pu,qi,z,train_ui,amount







ave,bu,bi,pu,qi,z,train_ui,amount=SVDPlusPlus()  




def isexist(u,i):
    ok = 0
    if u in train_ui.keys():
        for item_id,rui in train_ui[u]:
            ok=0
            if item_id == i:
                ok=1
        if ok == 1:
            return True
        else:
            return False
    return True




def recommend():
    sqlsession = sqlModel.DBSession
    rateArr = []
    for u in range(1,amount):
        for i in range(1,amount):
            if not isexist(u,i):
                rateArr.append([i,(ave+bu[u]+bi[i]+np.dot(qi[i],(pu[u]+z[u]).T))])
                
        rateArr=sorted(rateArr,key=lambda x:x[1],reverse=True)
        rateArr.append([])
        rateArr.append([])
        rateArr.append([])
        rateArr.append([])
        rateArr.append([])
#        print (u)
 #       for k in range(0,5):            
#            print (rateArr[k])
        sqlsession.query(sqlModel.Recommendation).filter(u==sqlModel.Recommendation.u_id).update({sqlModel.Recommendation.recommendation1:rateArr[0] , sqlModel.Recommendation.recommendation2:rateArr[1] , sqlModel.Recommendation.recommendation3:rateArr[2] , sqlModel.Recommendation.recommendation4:rateArr[3] , sqlModel.Recommendation.recommendation5:rateArr[4]})
        sqlsession.commit()
        sqlsession.close()
        rateArr.clear()
   