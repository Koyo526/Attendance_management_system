import mysql.connector
import pandas as pd
import sqlalchemy as sqa
 
# コネクションの作成
conn = mysql.connector.connect(
    host='localhost',
    port='3306',
    user='root',
    password='Koyo0526',
    database='test_db'
)

# カーソルを取得する
cur = conn.cursor()
df=pd.read_csv("../data/Student-Timetable.csv")

cur.execute("use test_db")
url = 'mysql+pymysql://root:Koyo0526@localhost/test_db'
engine = sqa.create_engine(url, echo=True)
df.to_sql("student_timetable", url, index=None)
week_lessons=['M1','M2','M3','M4','T2','T3_1','T3_2','T4','T5','W12','W3_1','W3_2','W4','W5_1','W5_2','Th2','Th34','Th5_1','Th5_2','F1','F2','F3','F4_1','F4_2']
for w in week_lessons:
    lesson="../database/"+w+".csv"
    lesson_student=pd.read_csv(lesson)
    name=w
    lesson_student.to_sql(name, url, index=None)
data=pd.read_csv("../data/学生リスト.csv")
data =data.drop("ふりがな", axis=1)
data["パスワード"]=data["学籍番号"]
data.to_sql("student_users", url, index=None)

data1=pd.read_csv("../data/Lecture-Rules.csv")
drop_list=["開始時間","終了時間","出席限度(分)","遅刻限度(分)","試験","履修者数","曜日","受付時間","出席時間","遅刻時間"]
for dl in drop_list:
    data1=data1.drop(dl,axis=1)
data1["パスワード"]=data1["ID"]
data1.to_sql("teacher_users",url,index=None)
cur.close
conn.close