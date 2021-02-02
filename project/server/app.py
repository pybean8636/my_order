from flask import Flask, jsonify, request, Response
from flask_cors import CORS
import pymysql
import jwt
import datetime


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
            user_key_id=user_info[0]
            payload = {
                'user_key_id':user_key_id,
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

@app.route('/api/user_info', methods=['GET'])#사용자 정보 반환해주는 서버 
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
            SELECT user.user_id, user.user_name, user.user_contact, store.store_id, store.store_location,user.user_key_id 
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
        response_object['user_key_id']=user_info[5]


    else:
        response_object['status']="401 Error"
        response_object['message'] = 'token error'
    
    #print('*'*20,response_object)

    return jsonify(response_object)


@app.route('/api/store_info', methods=['GET'])#매장 정보 반환해주는 서버 
def get_storeInfo():
    response_object = {'status':'success'}
    access_token = request.headers.get('Authorization')
    print(access_token)

    if access_token is not None:
        try:
            payload = jwt.decode(access_token, 'myordertoken', 'HS256')#토큰 디코딩
        except jwt.InvalidTokenError:
            response_object['status']="401 Error"
            return Response(status=401)
        
       #디비 검색 결과 -> 해당 매장 위치, 매장 번호, 본사
        store_id=payload['store_id']
        print(store_id)
        sql="""
            SELECT store.store_location, store.store_contact, headquarters.headquarters_name
            FROM store, headquarters 
            WHERE store.store_id=%s and headquarters.headquarters_id=store.headquarters_id;
            """
        cursor.execute(sql, store_id)
        user_info = cursor.fetchone()

        response_object['store_location']=user_info[0]
        response_object['store_contact']=user_info[1]
        response_object['headquarters_name']=user_info[2]
    else:
        response_object['status']="401 Error"
        response_object['message'] = 'token error'
    
    print('*'*20,response_object)

    return jsonify(response_object)


@app.route('/api/item_info', methods=['GET'])#아이템 정보 반환해주는 서버 
def get_itemInfo():
    print('item_info')
    response_object = {'status':'success'}
    access_token = request.headers.get('Authorization')
    print(access_token)

    if access_token is not None:
        try:
            payload = jwt.decode(access_token, 'myordertoken', 'HS256')#토큰 디코딩
        except jwt.InvalidTokenError:
            response_object['status']="401 Error"
            return Response(status=401)
        
       #디비 검색 결과 -> 아이템 아이디, 이름, 가격, 재고, 정보, 태그
        store_id=payload['store_id']
        print(store_id)
        sql="""
            SELECT item.item_id, item.item_name, item.item_price, item.item_stock, item.item_info, item.item_tag, item.item_unit
            FROM item, headquarters, store
            WHERE item.headquarters_id=headquarters.headquarters_id and headquarters.headquarters_id=store.headquarters_id and store.store_id=%s;
            """
        cursor.execute(sql, store_id)
        item_info = cursor.fetchall()
        print(item_info)

        response_object['item_info']=[]
        response_object['tags']=['기타']
        for info in item_info:
            temp_object={}

            
            temp_object['id']=info[0]
            temp_object['name']=info[1]
            temp_object['price']=info[2]
            temp_object['stock']=info[3]
            temp_object['info']=info[4]

            if info[5]==None:
                temp_object['tag']='기타'
            else:
                temp_object['tag']=info[5]

            temp_object['unit']=info[6]
            temp_object['check']=False #주문 여부 확인 위해 추가   
            temp_object['qty']=0
            if info[5] not in response_object['tags'] and info[5]!= None:
                response_object['tags'].append(info[5])
            response_object['item_info'].append(temp_object)

    else:
        response_object['status']="401 Error"
        response_object['message'] = 'token error'
    
    print('*'*20,response_object)

    return jsonify(response_object)

@app.route('/api/order_info', methods=['POST'])#아이템 정보 반환해주는 서버 
def get_orderInfo():
    print('---------get order_info------------')
    response_object = {'status':'success'}
    post_data = request.get_json()
    print(post_data)
    user_key_id=post_data.get('user_key_id')
    # store_id=post_data['store_id']
    #디비 검색 결과 -> 아이템 아이디, 이름, 가격, 재고, 정보, 태그

    sql="""
        SELECT `order`.`date` FROM `order` WHERE `order`.user_key_id=%s order by date desc;
        """
    cursor.execute(sql, user_key_id)
    latest = cursor.fetchone()
    latest=latest[0]
    
    sql="""
        SELECT  item.item_name, order_detail.detail_qty, item.item_unit, item.item_price, order_detail.detail_total_price, item.item_id, item.item_stock, item.item_info, item.item_tag
        FROM `order`, order_detail, item
        WHERE `order`.user_key_id=%s and `order`.order_id=order_detail.order_id and order_detail.item_id=item.item_id and `order`.`date`=%s
        """
    cursor.execute(sql, (user_key_id, latest))
    order_info = cursor.fetchall()
    # print(item_info)

    response_object['order_info']=[]
    response_object['date']=latest
    for info in order_info:

        temp={
            'name':info[0],
            'qty':info[1],
            'unit':info[2],
            'price':info[3],
            'total_price':info[4],
            'id':info[5],
            'stock':info[6],
            'info':info[7],
            'tag':info[8],
            'check':True
        }
        response_object['order_info'].append(temp)
    

    print('*'*20,response_object,'*'*20)

    return jsonify(response_object)



@app.route('/api/order', methods=['POST','PUT'])#발주 저장 
def put_orderInfo():
    print('put order')
    response_object = {'status':'success'}
    post_data = request.get_json()
    
    orderInfo=post_data['items']
    print(orderInfo)
    
    
    user_key_id=post_data.get('user_key_id')
    now = datetime.datetime.now()

    #order key 가져오기
    sql="""
        SELECT `order_id` FROM prjDB.order
        order by order_id desc;
        """
    cursor.execute(sql)
    id_num=cursor.fetchone()
    id_num=id_num[0]+1

    #디비 저장
    sql="""
        INSERT INTO `prjDB`.`order` (`order_id`,`date`, `user_key_id`) VALUES (%s, %s, %s);
        """


    cursor.execute(sql, (id_num, now.strftime('%Y-%m-%d %H:%M:%S'),user_key_id))

    for info in orderInfo:
        print("info2",info)
        sql="""
            INSERT INTO `prjDB`.`order_detail` (`detail_qty`, `detail_total_price`, `order_id`, `item_id`) VALUES (%s, %s, %s, %s);

            """

        cursor.execute(sql, (info['qty'], info['qty']*info['price'], id_num, info['id']))

    

    db.commit()

    sql="""
        SELECT * FROM prjDB.order_detail;
        """
    cursor.execute(sql)
    print(cursor.fetchall())

    return jsonify(response_object)

if __name__ == '__main__':
    app.run()