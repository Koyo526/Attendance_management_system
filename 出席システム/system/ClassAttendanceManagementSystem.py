import pandas as pd
import datetime as dt
import pymysql.cursors
from ClassDataPlot import DataPlot

class AttendanceManagementsystem:
    def __init__(self,rule,schedule,timetable):
        self.rule=rule
        self.schedule=schedule
        self.timetable=timetable
    def LectureRule(self,day,time):
        df_rule=pd.read_csv(self.rule)
        df_rule=df_rule.dropna().reset_index(drop=True)
        weekday_list=["M","T","W","Th","F"]
        weekday_dictionary={"M":"Mon","T":"Tue","W":"Wed","Th":"Thu","F":"Fri"}
        df_week=df_rule["講義ID"]
        x=0
        for wd in df_week:
            for w_list in weekday_list:
                if(w_list in wd):
                    df_rule.at[x,"曜日"]=weekday_dictionary[w_list]
            x+=1
        df_rule=df_rule.dropna()
        start_time=df_rule["開始時間"].to_list()
        attendance_limit=df_rule["出席限度(分)"].to_list()
        late_limit=df_rule["遅刻限度(分)"].to_list()
        x=0
        for st in start_time:
            st_dt = dt.datetime.strptime(st,'%H:%M')
            if(00==int(st_dt.minute)):
                st_hour=int(st_dt.hour)-1
                st_minute=50
            else:
                st_hour=int(st_dt.hour)
                st_minute=int(st_dt.minute)-10
            at_minute=st_dt.minute+attendance_limit[x]
            at_hour=st_dt.hour
            while(at_minute>60):
                at_minute-=60
                at_hour+=1
            lt_minute=st_dt.minute+late_limit[x]
            lt_hour=st_dt.hour
            while(lt_minute>60):
                lt_minute-=60
                lt_hour+=1
            df_rule.at[x,"受付時間"]=str(st_hour)+":"+str(st_minute).zfill(2)
            df_rule.at[x,"出席時間"]=str(at_hour)+":"+str(at_minute).zfill(2)
            df_rule.at[x,"遅刻時間"]=str(lt_hour)+":"+str(lt_minute).zfill(2)
            x+=1
        self.rule=df_rule
        df_rule.to_csv("Class-Rule.csv")
        df_schedule=pd.read_csv(self.schedule)
        tstr=day+" "+time
        print(tstr)
        #tstr = '2012-12-29 13:49:37'
        dt_now=dt.datetime.strptime(tstr, '%Y-%m-%d %H:%M:%S')
        #dt_now = dt.datetime(2019,10,1,10,40) #今回は2019年10月1日10：40としている
        self.dt_now=dt_now
        dt_day=str(dt_now.year)+"/"+str(dt_now.month)+"/"+str(dt_now.day)
        dt_time=str(dt_now.hour)+":"+str(dt_now.minute)
        d_day=df_schedule.query('date == @dt_day')
        if(d_day.empty):
            print("今日は講義がありません")
            return 1
        else:
            l_week=d_day['lecture_week'].to_string(index=False)
            time=d_day["times"].to_string(index=False)
            today_lecture=df_rule.query('曜日==@l_week')
            reception_time=today_lecture["受付時間"].to_list()
            end_time=today_lecture["終了時間"].to_list()
            record_number=0
            for t in range(len(reception_time)-1):
                reception_select=reception_time[t]
                reception=dt.datetime.strptime(reception_time[t],'%H:%M')
                end=dt.datetime.strptime(end_time[t],'%H:%M')
                reception_t=dt.time(reception.hour,reception.minute)
                end_t=dt.time(end.hour,end.minute)
                now_time=dt.time(dt_now.hour,dt_now.minute)
                if(now_time >= reception_t and now_time <= end_t):
                    sreach_lecture=today_lecture.query('受付時間==@reception_select')
                    record_number=1
            if(record_number==0):
                print("現在の時間は講義がありません")
                return 1
            else:
                sreach_lecture=sreach_lecture.reset_index(drop=True)
                sreach_lecture["週"]=time
                self.sreach_lecture=sreach_lecture
                return 0
    def StudentJudgment(self,id):
        self.id=id
        df_student_timetable=pd.read_csv(self.timetable)
        student_ID=self.id
        df_lecture=self.sreach_lecture
        dt_now=self.dt_now
        dt_time=dt.time(dt_now.hour,dt_now.minute)
        dt_day_str=str(dt_now.year)+"/"+str(dt_now.month)+"/"+str(dt_now.day)
        index_x=df_lecture.index.to_list()
        if(len(index_x)>1):
            select_lecture=df_lecture["科目名"].to_list()
            y=1
            for sl in select_lecture:
                print(str(y)+":"+sl+"　",end='')
                y+=1
            print("")
            input_lecture=input('上の中から出席する講義の数字を選択して下さい')
            index_z=int(input_lecture)-1
            df_lecture=df_lecture.query('index == @index_z')
        lecture=df_lecture["講義ID"].to_string(index=False) 
        select_student=df_student_timetable.query('IDm==@student_ID')
        if("No-select"==select_student[lecture].to_string(index=False)):
            print("この生徒は履修者ではありません")
        else:
            print("この生徒は履修者です")
        st_time=df_lecture["受付時間"].to_string(index=False)
        at_time=df_lecture["出席時間"].to_string(index=False)
        ab_time=df_lecture["遅刻時間"].to_string(index=False)
        st_dt = dt.datetime.strptime(st_time,'%H:%M')
        at_dt = dt.datetime.strptime(at_time,'%H:%M')
        ab_dt = dt.datetime.strptime(ab_time,'%H:%M')
        st_dtime=dt.time(st_dt.hour,st_dt.minute)
        at_dtime=dt.time(at_dt.hour,at_dt.minute)
        ab_dtime=dt.time(ab_dt.hour,ab_dt.minute)
        if(dt_time<st_dtime):
            str_x="出席受付前です"
        elif(st_dtime<= dt_time and dt_time<=at_dtime):
            str_x="出席です"
            insert_add="UPDATE "+lecture+" SET 第"+str(int(float(df_lecture["週"])))+"週='出席' WHERE IDm='"+id+"';"
            conn=pymysql.connect(host='localhost',user='root',password='Koyo0526',db='test_db',charset='utf8',cursorclass=pymysql.cursors.DictCursor)
            # カーソルを取得する
            with conn.cursor() as cur:
                cur.execute("use test_db")
                cur.execute(insert_add)
                conn.commit()
            conn.close
        elif(at_dtime<dt_time and dt_time<=ab_dtime):
            str_x="遅刻です"
            insert_add="UPDATE "+lecture+" SET 第"+str(int(float(df_lecture["週"])))+"週='遅刻' WHERE IDm='"+id+"';"
            conn=pymysql.connect(host='localhost',
                             user='root',
                             password='Koyo0526',
                             db='test_db',
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)
                # カーソルを取得する
            with conn.cursor() as cur:
                cur.execute("use test_db")
                cur.execute(insert_add)
                conn.commit()
            conn.close
        else:
            str_x="欠席です"
            insert_add="UPDATE "+lecture+" SET 第"+str(int(float(df_lecture["週"])))+"週='欠席' WHERE IDm='"+id+"';"
            conn=pymysql.connect(host='localhost',
                             user='root',
                             password='Koyo0526',
                             db='test_db',
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)
                # カーソルを取得する
            with conn.cursor() as cur:
                cur.execute("use test_db")
                cur.execute(insert_add)
                conn.commit()
            conn.close
        DataPlot(lecture)
        return str_x