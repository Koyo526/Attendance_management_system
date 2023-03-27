import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pymysql.cursors
import matplotlib.image as mpimg


"""
font = {"family":"IPAexGothic"}
mpl.rc('font', **font)
"""
def DataPlot(name):
    lecture_name=name
    insert_add="select * from "+lecture_name+";"
    conn=pymysql.connect(host='localhost',user='root',password='Koyo0526',db='test_db',charset='utf8',cursorclass=pymysql.cursors.DictCursor)
    df=pd.read_sql(sql=insert_add, con=conn)
    Attendance=[]
    Late=[]
    Absence=[]
    for i in range(1,17):
        column="第"+str(i)+"週"
        count_attend=0
        count_late=0
        count_absent=0
        for j in range(0,100):
            if('出席'== df.at[j,column]):
                count_attend+=1
            elif('遅刻'== df.at[j,column]):
                count_late+=1
            elif('欠席'== df.at[j,column]):
                count_absent+=1
        Attendance.append(count_attend)
        Late.append(count_late)
        Absence.append(count_absent)
    fig = plt.figure(figsize=(10,7))
    left = np.arange(len(Attendance)) 
    labels = ['第1回', '第2回', '第3回','第4回', '第5回','第6回', '第7回', '第8回', '第9回', '第10回','第11回', '第12回', '第13回', '第14回', '第15回','第16回']
    width = 0.2
    plt.bar(left, Attendance, color='g', width=width, align='center',label='出席')
    plt.bar(left+width, Late, color='y', width=width, align='center',label='遅刻')
    plt.bar(left+width+width, Absence, color='r', width=width, align='center',label='欠席')
    plt.xticks(left + width/3, labels)
    plt.legend(loc='upper right')
    plt.title(lecture_name)
    plt.xlabel("講義回数")
    plt.ylabel("出欠回数")
    plt.grid()
    Graph_name="../../Web/Graph/"+lecture_name+"-Graph.png"
    fig.savefig(Graph_name)
    plt.close()
    
