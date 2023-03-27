import os
import random
from datetime import datetime
import csv
from operator import itemgetter, attrgetter

# ランダムな時間と秒を発生させる関数
# 年，月，日，開始時間は固定，乱数の分布として正規分布を設定
def generate_random_datetimes(Y, M, D, H, m0, mu, sigma, N):
    MinMax = 59
    rand_datetimes = []
    for i in range(N):
        ValMin = int(random.normalvariate(mu, sigma))
        m = m0+ValMin
        Hp = H
        Mp = m
        # 分が59を超えたら時間を+1，分を-60
        if Mp > MinMax:
            Hp += 1
            Mp -= MinMax+1
        # 分が負の値となったら時間を-1，分を+60
        elif Mp < 0:
            Hp -= 1
            Mp += MinMax+1
        # 一旦datetime型のnowに今の時刻を入れる
        now = datetime.now()
        # 設定したランダム日時に入れ替える
        # 秒は一様乱数で1から59までの値を入れる
        rand_datetime = now.replace(year=Y, month=M, day=D, hour=Hp, minute=Mp,
                                    second=random.randint(1,59))
        rand_datetimes.append(rand_datetime)
    return rand_datetimes

SubjectID = 'M1'

# 講義の回ごとの年，月，日のリスト．時間割にしたがって設定
Ys = [2019, 2019, 2019, 2019, 2019, 2019, 2019, 2019, 2019, 2019, 2020, 2020, 2020, 2020, 2020] 
Ms = [10, 10, 10, 10, 11, 11, 11, 12, 12, 12, 1, 1, 1, 1, 1]
Ds = [7, 21, 25, 28, 11, 18, 25, 2, 9, 16, 6, 16, 20, 27, 29]
# 開始時刻
H = 8
m0 = 50
# 講義回ごとの正規分布の平均(mus)と標準偏差(sigmas)
mus = [3, 5, 5, 7, 9, 10, 10, 10, 10, 10, 12, 10, 11, 8, 7]
sigmas = [5, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10]

fileIDm = f'IDm-{SubjectID}.csv'

# 履修者のIDmのリストの入ったCSVファイルを開く
DataIDm = []
with open(fileIDm, 'r') as file:
    reader = csv.reader(file)
    header = next(reader)
    for row in reader:
        DataIDm.append(row)

# データを出力するディレクトリがなければ作成 
os.makedirs(SubjectID, exist_ok=True)

# CSVファイルのヘッダ
header = ['年月日'] + ['時刻'] + header

# リストYsの長さ(=講義回)でループ
for i in range(len(Ys)):
    Y = Ys[i]
    M = Ms[i]
    D = Ds[i]
    mu = mus[i]
    sigma = sigmas[i]
    N = len(DataIDm)
    RD = generate_random_datetimes(Y, M, D, H, m0, mu, sigma, N)

    # DataRDがランダムな時間を格納するリスト
    DataRD = []
    for j in range(len(RD)):
        YMD = '{:%Y-%m-%d}'.format(RD[j])
        HTS = '{:%X}'.format(RD[j])
        DataRD.append([YMD, HTS])

    # 時間の順にソートする
    DataRD.sort(key=itemgetter(1))

    # シャッフル
    numbers = [j for j in range(len(DataIDm))]
    random.shuffle(numbers)

    # リストにIDmを付加する
    for j in range(len(RD)):
        k = numbers[j]
        DataRD[j].append(DataIDm[k][0])
        # ここをコメントアウトすると学籍番号も付加される
        # DataRD[j].append(DataIDm[k][1])

    # ファイルに出力
    FileOut = f'{SubjectID}/{SubjectID}-{str(Y)}{str(M).zfill(2)}{str(D).zfill(2)}.csv'
    with open(FileOut, 'w') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(header)
        writer.writerows(DataRD)
