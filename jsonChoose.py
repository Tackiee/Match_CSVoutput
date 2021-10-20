import json
import pandas as pd
import numpy as np
import glob
import csv
import os

def getFileName(path): # ファイル名の取得
    filelist = glob.glob(path + "/*.json") # .jsonという名前で終わるファイルを出力
    return filelist

def getSpecificData(filelist1, filelist2):
    # 中央フォーム
    with open('output_center.csv', 'w') as f:
        writer_C = csv.writer(f, lineterminator='\n') 
        # 自分の必要なデータの列の名前を用意。上のデータと同じだけの列数を揃える
        # writerowメソッド：csvファイルへの一行の書き込み
        writer_C.writerow(["RElbow_x","RElbow_y","RWrist_x","RWrist_y","RShoulder_x","RShoulder_y"])
    for i in range(len(filelist1)):
        with open(filelist1[i]) as f:
            data = json.load(f)
            data = np.array(data['people'][0]['pose_keypoints_2d']).reshape(-1,3)
        # df：データフレーム（2次元のラベル付きデータ構造）
        df = pd.DataFrame(data, columns=['X','Y','P'], index=["Nose", "Neck", "RShoulder", "RElbow", "RWrist", "LShoulder", "LElbow", "LWrist", "MidHip", "RHip", \
            "RKnee", "RAnkle", "LHip", "LKnee", "LAnkle", "REye", "LEye", "REar", "LEar", "LBigToe", "LSmallToe", "LHeel", "RBigToe", "RSmallToe", "RHeel"])
        
        # 始点のx座標とy座標を取得する
        if(i == 0):
            # x座標
            Base_RElbow_X_center = float(df.at["RElbow", "X"])
            Base_RWrist_X_center = float(df.at["RWrist", "X"])
            Base_RShoulder_X_center = float(df.at["RShoulder", "X"])
            # y座標
            Base_RElbow_Y_center = float(df.at["RElbow", "Y"])
            Base_RWrist_Y_center = float(df.at["RWrist", "Y"])
            Base_RShoulder_Y_center = float(df.at["RShoulder", "Y"])
            

        # 自分の必要なデータを取り出す
        writeCSV([float(df.at["RElbow", "X"]), float(df.at["RElbow", "Y"]), float(df.at["RWrist", "X"]), float(df.at["RWrist", "Y"]), float(df.at["RShoulder", "X"]), float(df.at["RShoulder", "Y"])], "output_center")

    # 左側フォーム
    with open('output_left.csv', 'w') as f:
        writer_L = csv.writer(f, lineterminator='\n') 
        # 自分の必要なデータの列の名前を用意。上のデータと同じだけの列数を揃える。
        # writerowメソッド：csvファイルへの一行の書き込み
        writer_L.writerow(["RElbow_x","RElbow_y","RWrist_x","RWrist_y","RShoulder_x","RShoulder_y"])
    for i in range(len(filelist2)):
        with open(filelist2[i]) as f:
            data = json.load(f)
            data = np.array(data['people'][0]['pose_keypoints_2d']).reshape(-1,3)
        # df：データフレーム（2次元のラベル付きデータ構造）
        df = pd.DataFrame(data, columns=['X','Y','P'], index=["Nose", "Neck", "RShoulder", "RElbow", "RWrist", "LShoulder", "LElbow", "LWrist", "MidHip", "RHip", \
            "RKnee", "RAnkle", "LHip", "LKnee", "LAnkle", "REye", "LEye", "REar", "LEar", "LBigToe", "LSmallToe", "LHeel", "RBigToe", "RSmallToe", "RHeel"])

        # 始点のx座標とy座標を取得する
        if(i == 0):
            #x座標
            Base_RElbow_X_left = float(df.at["RElbow", "X"])
            Base_RWrist_X_left = float(df.at["RWrist", "X"])
            Base_RShoulder_X_left = float(df.at["RShoulder", "X"])
            #y座標
            Base_RElbow_Y_left = float(df.at["RElbow", "Y"])
            Base_RWrist_Y_left = float(df.at["RWrist", "Y"])
            Base_RShoulder_Y_left = float(df.at["RShoulder", "Y"])
        
        # 中央フォームと左側フォームでの差分を取得する
        # 今回は左側の値が大きかったので，left-centerで差分を求め，始点を中央の座標に揃える
        diff_Base_RElbow_X = Base_RElbow_X_left - Base_RElbow_X_center
        diff_Base_RWrist_X = Base_RWrist_X_left - Base_RWrist_X_center
        diff_Base_RShoulder_X = Base_RShoulder_X_left - Base_RShoulder_X_center
        diff_Base_RElbow_Y = Base_RElbow_Y_left - Base_RElbow_Y_center
        diff_Base_RWrist_Y = Base_RWrist_Y_left - Base_RWrist_Y_center
        diff_Base_RShoulder_Y = Base_RShoulder_Y_left - Base_RShoulder_Y_center

        
        # 自分の必要なデータを取り出す
        # 左の値をcsvに描きこむ際に，差分を引いておく
        writeCSV([float((df.at["RElbow", "X"]) - diff_Base_RElbow_X), float((df.at["RElbow", "Y"]) - diff_Base_RElbow_Y),
                  float((df.at["RWrist", "X"]) - diff_Base_RWrist_X), float((df.at["RWrist", "Y"]) - diff_Base_RWrist_Y), 
                  float((df.at["RShoulder", "X"]) - diff_Base_RShoulder_X), float((df.at["RShoulder", "Y"]) - diff_Base_RShoulder_Y)], "output_left")

def writeCSV(data, filelist):
    with open(filelist + '.csv', 'a') as f:
        writer = csv.writer(f, lineterminator='\n') 
        writer.writerow(data)

def main():
    filelist1 = getFileName('json_center')
    filelist2 = getFileName('json_left')
    getSpecificData(filelist1, filelist2)

if __name__ == '__main__':
    main()