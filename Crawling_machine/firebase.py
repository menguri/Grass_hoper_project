#pip install firebase_admin
#real_time Database/ test version 이기 때문에 플러터 개발 어느정도 끝나면 손봐줘야 함.
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import json
import numpy as np

#Firebase database 인증 및 앱 초기화
cred = credentials.Certificate('ant-indicator-firebase-adminsdk-orxkq-59daefb774.json')
firebase_admin.initialize_app(cred,{
    'databaseURL' : 'https://ant-indicator-default-rtdb.firebaseio.com/'
})


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)

def Count_storage(dic, corporation, time):
    dir = db.reference(f'Counting Data/{corporation}/{time}')  #기본 위치 지정
    dir.update(dic)

# def Get_storage(corporation, time):


