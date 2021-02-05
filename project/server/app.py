from flask import Flask, jsonify, request, Response
from flask_cors import CORS
import pymysql
import jwt
from datetime import datetime, timedelta
import bcrypt

app = Flask(__name__)
app.config.from_object(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})

# db = pymysql.connect(host='localhost', port=3306, user='root', passwd='dhltlrdls', db='prjDB', charset='utf8')
# cursor = db.cursor()

@app.route('/', methods=['GET'])
def test():
    return 'hello'

@app.route('/api/auth/login', methods=['POST'])
def login_auth():
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='dhltlrdls', db='prjDB', charset='utf8')
    cursor = db.cursor()


    response_object = {'status':'success'}
    post_data = request.get_json()
    
    user_id=post_data['id']
    user_pw=post_data['pw']#client가 보낸 아이디, 패스워드

    sql="SELECT * FROM user WHERE user_id=%s"#유저 검색
    rows_count = cursor.execute(sql, user_id)

    if rows_count > 0:
        user_info = cursor.fetchone()
        #print('user info:', user_info)
        if bcrypt.checkpw(user_pw.encode('utf-8'), user_info[2].encode('utf-8')):
        
            response_object['message'] = 'login success'
            store_id=user_info[5]
            user_key_id=user_info[0]

            payload = {#access payload
                'user_key_id':user_key_id,
                'user_id':user_id,
                'store_id':store_id,
                'exp':datetime.now()+timedelta(hours=2)
            }
            print('access token', payload)
            access_token = jwt.encode(payload,'myorderaccesstoken', 'HS256')#토큰 생성->2개로 추가 ####################
            #print(access_token)



            payload = {#refresh payload
                'user_key_id':user_key_id,
                'user_id':user_id,
                'store_id':store_id,
                'exp':datetime.now()+timedelta(weeks=2)
            }
            refresh_token = jwt.encode(payload,'myorderrefreshtoken', 'HS256')


            response_object['access_token']= access_token
            response_object['refresh_token']= refresh_token
            ###########################################################################################
        else:
            response_object['message'] = 'password error'
            #print('password error')
    else:
        response_object['message'] = 'ID does not exit'
        #print('does not exit')

    db.close()

    return jsonify(response_object)

@app.route('/api/user_info', methods=['GET'])#사용자 정보 반환해주는 서버 
def get_userInfo():


    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='dhltlrdls', db='prjDB', charset='utf8')
    cursor = db.cursor()


    response_object = {'status':'success'}
    access_token = request.headers.get('access_Authorization')
    refresh_token = request.headers.get('refresh_Authorization')
###########################################################################################
    if access_token is not None:
        try:##access 만료 전
            payload = jwt.decode(access_token, 'myorderaccesstoken', 'HS256')#토큰 디코딩
            response_object['message'] = 'access token 만료전'

        except jwt.ExpiredSignatureError:#access 만료 후 재발급

            try:#refresh 확인
                payload = jwt.decode(access_token, 'myorderrefreshtoken', 'HS256')
                #access 재발급
                print("NEW ACCESS TOKEN IS PUBLISHED\n")
                new_payload = {#access payload
                    'user_key_id':payload['user_key_id'],
                    'user_id':payload['user_id'],
                    'store_id':payload['store_id'],
                    'exp':datetime.now()+timedelta(seconds=60)
                }
                access_token = jwt.encode(new_payload,'myorderaccesstoken', 'HS256')

            except jwt.InvalidTokenError:
                response_object['status']="401 Error"
                response_object['message'] = 'refresh token error'
                return jsonify(response_object)

            # response_object['status']="401 Error"
            response_object['message'] = 'new access token'
            # return Response(status=401)
        
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
        response_object['access_token']=access_token


    else:
        response_object['status']="401 Error"
        response_object['message'] = 'access token error'
 ###########################################################################################   
    print('*'*20,response_object)

    db.close()
    return jsonify(response_object)


@app.route('/api/store_info', methods=['POST'])#매장 정보 반환해주는 서버 
def get_storeInfo():


    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='dhltlrdls', db='prjDB', charset='utf8')
    cursor = db.cursor()



    response_object = {'status':'success'}
    post_data = request.get_json()
    print(post_data)
    store_id=post_data.get('store_id')


    
    #디비 검색 결과 -> 해당 매장 위치, 매장 번호, 본사

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

    
    print('*'*20,response_object)
    db.close()
    return jsonify(response_object)


@app.route('/api/item_info', methods=['POST'])#아이템 정보 반환해주는 서버 
def get_itemInfo():


    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='dhltlrdls', db='prjDB', charset='utf8')
    cursor = db.cursor()

    post_data = request.get_json()
    print(post_data)
    store_id=post_data.get('store_id')

    # print('item_info')
    response_object = {'status':'success'}
    # access_token = request.headers.get('access_Authorization')
    # print(access_token)

    # if access_token is not None:
    #     try:
    #         payload = jwt.decode(access_token, 'myordertoken', 'HS256')#토큰 디코딩
    #     except jwt.InvalidTokenError:
    #         response_object['status']="401 Error"
    #         return Response(status=401)
        
    #    #디비 검색 결과 -> 아이템 아이디, 이름, 가격, 재고, 정보, 태그
    #     store_id=payload['store_id']
    # print(store_id)
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

    # else:
    #     response_object['status']="401 Error"
    #     response_object['message'] = 'token error'
    
    print('*'*20,response_object)
    db.close()

    return jsonify(response_object)

@app.route('/api/order_info', methods=['POST'])#사용자가 가장 최근 발주한 내역
def get_orderInfo():

    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='dhltlrdls', db='prjDB', charset='utf8')
    cursor = db.cursor()


    print('---------get order_info------------')
    response_object = {'status':'success'}
    post_data = request.get_json()
    print(post_data)
    user_key_id=post_data.get('user_key_id')
    # store_id=post_data['store_id']
    #디비 검색 결과 -> 아이템 아이디, 이름, 가격, 재고, 정보, 태그
############################################################################################################################################
    # sql="""
    #     SELECT `order`.`date` FROM `order` WHERE `order`.user_key_id=%s order by date desc;
    #     """
    # cursor.execute(sql, user_key_id)
    # latest = cursor.fetchone()
    # latest=latest[0]
    
    # sql="""
    #     SELECT  item.item_name, order_detail.detail_qty, item.item_unit, item.item_price, order_detail.detail_total_price, item.item_id, item.item_stock, item.item_info, item.item_tag
    #     FROM `order`, order_detail, item
    #     WHERE `order`.user_key_id=%s and `order`.order_id=order_detail.order_id and order_detail.item_id=item.item_id and `order`.`date`=%s
    #     """
    # cursor.execute(sql, (user_key_id, latest))
    # order_info = cursor.fetchall()
    # print(item_info)
############################################################################################################################################


    sql="""
        SELECT  item.item_name, order_detail.detail_qty, item.item_unit, item.item_price, order_detail.detail_total_price, item.item_id, item.item_stock, item.item_info, item.item_tag, `order`.`date`
        FROM `order`, order_detail, item
        WHERE `order`.user_key_id=%s and `order`.order_id=order_detail.order_id 
        and order_detail.item_id=item.item_id 
        and `order`.`date` = (SELECT `order`.`date` FROM `order` WHERE `order`.user_key_id=%s order by date desc limit 1);
        """

    cursor.execute(sql, (user_key_id,user_key_id))
    order_info = cursor.fetchall()

    response_object['order_info']=[]
    response_object['date']=order_info[0][-1]
    
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
        if info[8]==None:
                temp['tag']='기타'
        response_object['order_info'].append(temp)
    

    print('*'*20,response_object,'*'*20)
    db.close()

    return jsonify(response_object)



@app.route('/api/order', methods=['POST','PUT'])#발주 저장 
def put_orderInfo():

    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='dhltlrdls', db='prjDB', charset='utf8')
    cursor = db.cursor()


    print('put order')
    response_object = {'status':'success'}
    post_data = request.get_json()
    
    orderInfo=post_data['items']
    print(orderInfo)
    
    
    user_key_id=post_data.get('user_key_id')
    now = datetime.now()

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

        sql="""
            UPDATE `prjDB`.`item` SET `item_stock` = %s WHERE (`item_id` = %s);
            """
        cursor.execute(sql, (info['stock']-info['qty'], info['id']))

    

    db.commit()

    # sql="""
    #     SELECT * FROM prjDB.order_detail;
    #     """
    # cursor.execute(sql)
    # print(cursor.fetchall())
    db.close()

    return jsonify(response_object)

@app.route('/api/my_order_info', methods=['POST'])#마이메이지
def get_myOrderInfo():

    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='dhltlrdls', db='prjDB', charset='utf8')
    cursor = db.cursor()


    print('----my page------')
    response_object = {'status':'success'}
    post_data = request.get_json()
    store_id=post_data.get('store_id')
    # user_key_id=post_data.get('user_key_id')


    sql="""
        SELECT order_detail.* ,item.*, `order`.`date`
        FROM `order`, order_detail, item
        WHERE `order`.order_id=order_detail.order_id and order_detail.item_id= item.item_id and `order`.order_id in
        (SELECT  `order`.order_id
        FROM `order`, `user`, store
        WHERE store.store_id =%s and store.store_id = `user`.store_id and `order`.user_key_id=`user`.user_key_id) 
        order by `order`.order_id DESC;
        """
    cursor.execute(sql,store_id)
    orderInfo=cursor.fetchall()

    response_object['order_info']=[]
    order_id=orderInfo[0][3]
    temp={'order':[],'date':orderInfo[0][13], 'sum':0}
    # print(order_id)
    
    for info in orderInfo:
        # print('info',info)
        if order_id != info[3]:
            print('append')
            response_object['order_info'].append(temp)
            order_id=info[3]
            temp={'order':[],'date':info[13], 'sum':0}
            #temp append
            #order_id change
        
        temp2={
            'name':info[6],
            'qty':info[1],
            'unit':info[8],
            'price':info[7],
            'total_price':info[2],
            'id':info[4],
            'stock':info[9],
            'info':info[10],
            'tag':info[11],
            'check':True
        }
        temp['sum']+=info[2]
        if info[11]==None:
            temp2['tag']='기타'
        temp['order'].append(temp2)
            
    response_object['order_info'].append(temp)
    print(response_object)
    db.close()

    return jsonify(response_object)


if __name__ == '__main__':
    app.run()