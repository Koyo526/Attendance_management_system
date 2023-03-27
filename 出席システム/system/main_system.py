import pandas as pd
from ClassAttendanceManagementSystem import AttendanceManagementsystem

Ys = [2019, 2019, 2019, 2019, 2019, 2019, 2019, 2019, 2019, 2019, 2020, 2020, 2020, 2020, 2020] 
Ms = [10, 10, 10, 10, 11, 11, 11, 12, 12, 12, 1, 1, 1, 1, 1]
Ds = [7, 21, 25, 28, 11, 18, 25, 2, 9, 16, 6, 16, 20, 27, 29]
for i in range(len(Ys)):
    Y = Ys[i]
    M = Ms[i]
    D = Ds[i]
    lecture_time="M1/M1-"+str(Y)+str(M).zfill(2)+str(D).zfill(2)+".csv"
    Student_list=pd.read_csv(lecture_time)
    today=Student_list["年月日"].to_list()
    now_time=Student_list["時刻"].to_list()
    data=Student_list["IDm"].to_list()
    for i in range(len(data)):
        Mydata=AttendanceManagementsystem("../data/Lecture-Rules.csv","../data/講義日程表.csv","../data/Student-Timetable.csv")
        df_lecture=Mydata.LectureRule(today[i],now_time[i])
        if(df_lecture==1):
            print("**********")
        else:
            studnet_ID=data[i]
            x=Mydata.StudentJudgment(studnet_ID)
            print(x)
