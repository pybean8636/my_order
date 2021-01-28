from flask import Flask, jsonify, request, Response
from flask_cors import CORS
import pymysql
import jwt

app = Flask(__name__)
app.config.from_object(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})

db = pymysql.connect(host='localhost', port=3306, user='root', passwd='dhltlrdls', db='prjDB', charset='utf8')
cursor = db.cursor()

@app.route('/', methods=['GET'])
def test():
    return 'hello'

@app.route('/api/auth/login', methods=['POST'])
def login_auth():
    response_object = {'status':'success'}
    post_data = request.get_json()
    user_id=post_data['id']
    user_pw=post_data['pw']#client가 보낸 아이디, 패스워드

    sql="SELECT * FROM user WHERE user_id=%s"#유저 검색
    rows_count = cursor.execute(sql, user_id)

    if rows_count > 0:
        user_info = cursor.fetchone()
        #print('user info:', user_info)
        if user_pw==user_info[2]:#패스춰드 확인 -> 보안 관련 나중에 수정
            response_object['message'] = 'login success'
            store_id=user_info[5]
            payload = {
                'user_id':user_id,
                'store_id':store_id
            }
            token = jwt.encode(payload,'myordertoken', 'HS256')#토큰 생성
            #print(token)
            response_object['token']= token
        else:
            response_object['message'] = 'password error'
            #print('password error')
    else:
        response_object['message'] = 'ID does not exit'
        #print('does not exit')

    return jsonify(response_object)

@app.route('/api/user_info', methods=['GET'])
def get_userInfo():
    response_object = {'status':'success'}
    access_token = request.headers.get('Authorization')

    if access_token is not None:
        try:
            payload = jwt.decode(access_token, 'myordertoken', 'HS256')#토큰 디코딩
        except jwt.InvalidTokenError:
            response_object['status']="401 Error"
            return Response(status=401)
        
        user_id=payload['user_id']#디비 검색 결과 -> 해당 사용자의 아이디, 이름, 번호, 매장 아이디, 매장 위치 
        store_id=payload['store_id']
        sql="""
            SELECT user.user_id, user.user_name, user.user_contact, store.store_id, store.store_location 
            FROM user, store 
            WHERE store.store_id = user.store_id and user_id=%s;
            """
        cursor.execute(sql, user_id)
        user_info = cursor.fetchone()

        response_object['user_id']=user_info[0]
        response_object['user_name']=user_info[1]
        response_object['user_contact']=user_info[2]
        response_object['store_id']=user_info[3]
        response_object['store_location']=user_info[4]

    else:
        response_object['status']="401 Error"
        response_object['message'] = 'token error'
    
    #print('*'*20,response_object)

    return jsonify(response_object)

if __name__ == '__main__':
    app.run()