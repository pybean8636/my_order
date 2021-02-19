from flask import Flask, jsonify, request, Response
from flask_cors import CORS
import pymysql
import jwt
from datetime import datetime, timedelta
import bcrypt

app = Flask(__name__)
app.config.from_object(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})


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
            access_token = jwt.encode(payload,'myorderaccesstoken', 'HS256')#토큰 생성-
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
            
        else:
            response_object['message'] = 'password error'
            #print('password error')
    else:
        response_object['message'] = 'ID does not exit'
        #print('does not exit')


        # db.close()

    return jsonify(response_object)

@app.route('/api/user_info', methods=['GET'])#사용자 정보 반환해주는 서버 
def get_userInfo():


    # db = pymysql.connect(host='localhost', port=3306, user='root', passwd='dhltlrdls', db='prjDB', charset='utf8')
    # cursor = db.cursor()


    response_object = {'status':'success'}
    access_token = request.headers.get('access_Authorization')
    refresh_token = request.headers.get('refresh_Authorization')

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
        
        user_id=payload['user_id']#디비 검색 결과 -> 해당 사용자의 아이디, 이름, 번호, 매장 아이디, 매장 위치 , user key
        store_id=payload['store_id']
      
        ####################################################################################################################
        sql="""
            SELECT u.user_id, u.user_name, u.user_contact, s.store_id, s.store_location, u.user_key_id 
            FROM `user` u, store s
            WHERE s.store_id = u.store_id and u.user_id=%s;
            """
        ####################################################################################################################
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
   
    print('*'*20,response_object)

    # db.close()
    return jsonify(response_object)


@app.route('/api/store_info', methods=['POST'])#매장 정보 반환해주는 서버 
def get_storeInfo():
    print("--------get_storeInfo--------")


    # store_db = pymysql.connect(host='localhost', port=3306, user='root', passwd='dhltlrdls', db='prjDB', charset='utf8')
    # store_cursor = store_db.cursor()



    response_object = {'status':'success'}
    post_data = request.get_json()
    store_id=post_data.get('store_id')

    print("store_id", store_id)
    
    #디비 검색 결과 -> 해당 매장 위치, 매장 번호, 본사
    ####################################################################################################################
    sql="""
        SELECT s.store_location, s.store_contact, h.headquarters_name
        FROM store s, headquarters h 
        WHERE s.store_id=%s and h.headquarters_id=s.headquarters_id;
        """
    ####################################################################################################################
    cursor.execute(sql, store_id)
    user_info = cursor.fetchone()

    response_object['store_location']=user_info[0]
    response_object['store_contact']=user_info[1]
    response_object['headquarters_name']=user_info[2]

    # store_db.close()
    print('store'*20,response_object)
    return jsonify(response_object)


@app.route('/api/item_info', methods=['POST'])#아이템 정보 반환해주는 서버 
def get_itemInfo():


    # db = pymysql.connect(host='localhost', port=3306, user='root', passwd='dhltlrdls', db='prjDB', charset='utf8')
    # cursor = db.cursor()

    post_data = request.get_json()
    print(post_data)
    store_id=post_data.get('store_id')

    # print('item_info')
    response_object = {'status':'success'}

    ####################################################################################################################
    sql="""
        SELECT i.*
        FROM item i, store s
        WHERE i.headquarters_id=s.headquarters_id and s.store_id=%s;
        """
    ####################################################################################################################
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
        temp_object['unit']=info[3]
        temp_object['stock']=info[4]
        temp_object['info']=info[5]

        if info[6]==None:
            temp_object['tag']='기타'
        else:
            temp_object['tag']=info[6]

        
        temp_object['check']=False #주문 여부 확인 위해 추가   
        temp_object['qty']=0
        if info[6] not in response_object['tags'] and info[6]!= None:
            response_object['tags'].append(info[6])
        response_object['item_info'].append(temp_object)

    
    print('*'*20,response_object)
    # db1.close()

    return jsonify(response_object)

@app.route('/api/order_info', methods=['POST'])#사용자가 가장 최근 발주한 내역
def get_orderInfo():

    # latest_order_db = pymysql.connect(host='localhost', port=3306, user='root', passwd='dhltlrdls', db='prjDB', charset='utf8')
    # order_cursor = latest_order_db.cursor()


    print('---------get order_info------------')
    response_object = {'status':'success'}
    post_data = request.get_json()
    print(post_data)
    user_key_id=post_data.get('user_key_id')

    
    ##############################################        #################################################################
    sql="""
        SELECT  i.*, od.detail_qty, od.detail_total_price, o.`date`
        FROM `order` o, order_detail od, item i
        WHERE o.user_key_id=%s and o.order_id=od.order_id 
        and od.item_id=i.item_id 
        and o.`date` = (SELECT o.`date` FROM `order` o WHERE o.user_key_id=%s order by date desc limit 1);
        """
    ####################################################################################################################
    cursor.execute(sql, (user_key_id,user_key_id))
    order_info = cursor.fetchall()


    response_object['order_info']=[]
    response_object['date']=order_info[0][-1]
    
    for info in order_info:
        
        temp={
            'name':info[1],
            'qty':info[8],
            'unit':info[3],
            'price':info[2],
            'total_price':info[9],
            'id':info[0],
            'stock':info[4],
            'info':info[5],
            'tag':info[6],
            'check':True
        }
        if temp['tag']==None:
                temp['tag']='기타'
        response_object['order_info'].append(temp)
 
    # finally:
    # latest_order_db.close()
    

    print('*'*20,response_object,'*'*20)
    # db.close()

    return jsonify(response_object)



@app.route('/api/order', methods=['POST','PUT'])#발주 저장 
def put_orderInfo():

    # db = pymysql.connect(host='localhost', port=3306, user='root', passwd='dhltlrdls', db='prjDB', charset='utf8')
    # cursor = db.cursor()


    print('put order')
    response_object = {'status':'success'}
    post_data = request.get_json()
    
    orderInfo=post_data['items']
    print(orderInfo)
    
    
    user_key_id=post_data.get('user_key_id')
    now = datetime.now()
    ####################################################################################################################
    #order key 가져오기
    # sql="""
    #     SELECT `order_id` FROM prjDB.order
    #     order by order_id desc;
    #     """
    # cursor.execute(sql)
    # id_num=cursor.fetchone()
    # id_num=id_num[0]+1

    #디비 저장

    sql="""
        INSERT INTO `prjDB`.`order` (`date`, `user_key_id`) VALUES (%s, %s);
        """


    cursor.execute(sql, (now.strftime('%Y-%m-%d %H:%M:%S'),user_key_id))
    id_num=cursor.lastrowid#cursor.fetchone()

    insert_list=[]
    update_list=[]

    # for info in orderInfo:
    #     print("info2",info)
    #     sql="""
    #         INSERT INTO `prjDB`.`order_detail` (`detail_qty`, `detail_total_price`, `order_id`, `item_id`) VALUES (%s, %s, %s, %s);
    #         """
    #     cursor.execute(sql, (info['qty'], info['qty']*info['price'], id_num, info['id']))

    #     sql="""
    #         UPDATE `prjDB`.`item` SET `item_stock` = %s WHERE (`item_id` = %s);
    #         """
    #     cursor.execute(sql, (info['stock']-info['qty'], info['id']))

    ##############################################################       ################################################### excutemany
    for info in orderInfo:
        insert_list.append([info['qty'], info['qty']*info['price'], id_num, info['id']])
        update_list.append([info['stock']-info['qty'], info['id']])

    
    sql="""
        INSERT INTO `prjDB`.`order_detail` (`detail_qty`, `detail_total_price`, `order_id`, `item_id`) VALUES (%s, %s, %s, %s);
        """
    cursor.executemany(sql, insert_list)


    db.commit()

    sql="""
        UPDATE `prjDB`.`item` SET `item_stock` = %s WHERE (`item_id` = %s);
    """
    cursor.executemany(sql, update_list)

    db.commit()



   


    # db.close()

    return jsonify(response_object)

@app.route('/api/my_order_info', methods=['POST'])#마이메이지
def get_myOrderInfo():


    print('----my page------')
    response_object = {'status':'success'}
    post_data = request.get_json()
    store_id=post_data.get('store_id')



    ############################################################       ########################################################
    sql="""
        SELECT od.* ,i.*, o.`date`
        FROM `order` o, order_detail od, item i
        WHERE  o.order_id=od.order_id and od.item_id= i.item_id and o.order_id in
        (SELECT  o.order_id
        FROM `order` o, `user` u
        WHERE u.store_id=%s and o.user_key_id=u.user_key_id)  
        order by o.order_id DESC;
        """
    ####################################################################################################################
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
    # db.close()

    return jsonify(response_object)


@app.route('/api/dash_board_summary', methods=['POST'])#메인 홈 요약 대시보드
def dash_board_summary():

    print('----dash_board_summary------')
    response_object = {'status':'success'}
    post_data = request.get_json()
    store_id=post_data.get('store_id')



    ##################################################### 1   ########################################################
    sql="""
        SELECT date_format(o.`date`,'%%Y-%%m-%%d') `day`, count(o.order_id) `count`, sum(od.detail_total_price) sum
        FROM `order` o, order_detail od, `user` u
        WHERE o.`date` BETWEEN DATE_ADD(NOW(), INTERVAL -1 MONTH) AND NOW() 
            and o.user_key_id = u.user_key_id
            and o.order_id = od.order_id
            and u.store_id=%s
        group by `day`
        order by `day`;
        """
    ####################################################################################################################
    cursor.execute(sql,store_id)
    orderInfo=cursor.fetchall()


    response_object['frq']=[]#빈도
    response_object['payment']=[]#지출
    response_object['dates']=[]#지출


    for info in orderInfo:
        response_object['dates'].append(info[0])
        response_object['frq'].append(info[1])
        response_object['payment'].append(info[2])


    ######################################################### 2  #########################################################
    sql="""
        SELECT i.item_tag, count(*)
        FROM `order` o, order_detail od, `user` u, item i
        WHERE o.`date` BETWEEN DATE_ADD(NOW(), INTERVAL -1 MONTH) AND NOW() 
            and o.user_key_id = u.user_key_id
            and o.order_id = od.order_id
            and od.item_id=i.item_id
            and u.store_id=%s
        group by i.item_tag;
        """
    ####################################################################################################################
    cursor.execute(sql,store_id)
    tag_info=cursor.fetchall()

    response_object['tags']=[]#tag
    response_object['tag_count']=[]#태그 개수   

    for info in tag_info:
            
        if info[0] is None:
            response_object['tags'].append('기타')
        else:
            response_object['tags'].append(info[0])
        response_object['tag_count'].append(info[1])




    print(response_object)

    return jsonify(response_object)


@app.route('/api/dash_board_stacked', methods=['POST'])#대시보드
def dash_board_stacked():

    print('----dash_board------')
    response_object = {'status':'success'}
    post_data = request.get_json()
    store_id=post_data.get('store_id')

    sql="""
        select user_id from `user` where store_id=%s;
        """
    cursor.execute(sql,store_id)
    user_ids=[user[0] for user in cursor.fetchall()]
    # print(user_ids)
    response_object['users']=user_ids#발주한 사람 id

    users=""
    for user in user_ids:
        users+=", SUM(IF(user_id = '" + str(user) + "', c, 0)) AS " + str(user) +" "
        response_object[user]=[]

    ############################################## 발주 빈도 (사용자 빈도) ###############################################
    sql="""
        select `day` %s
        FROM (
            SELECT date_format(o.`date`,'%%Y-%%m-%%d') `day`, u.user_id, count(1) c
            FROM `order` o,`user` u
            WHERE o.`date` BETWEEN DATE_ADD(NOW(), INTERVAL -1 MONTH) AND NOW() 
                and u.store_id=%s and o.user_key_id = u.user_key_id
            group by `day`, u.user_id
            order by `day`
        ) us
        group by `day`
        ;
        """
    #################################################################################################################
    sql = sql%(users,store_id)
    cursor.execute(sql)
    orderInfo=cursor.fetchall()
    print('확인',orderInfo)

    response_object['dates']=[]#날짜
    



    for info in orderInfo:
        response_object['dates'].append(info[0])
        for i in range(len(user_ids)):
            print(user_ids[i],info[1+i])
            response_object[user_ids[i]].append(info[i+1])


    print(response_object)
    return jsonify(response_object)


@app.route('/api/dash_board_item', methods=['POST'])#대시보드
def dash_board_item():

    print('-------dash_board_item------')
    response_object = {'status':'success'}
    post_data = request.get_json()
    store_id=post_data.get('store_id')



    ##################################################################################################################
    sql="""
        SELECT i.item_id,i.item_name, count(*) c
        FROM `order` o, order_detail od, `user` u, item i
        WHERE o.`date` BETWEEN DATE_ADD(NOW(), INTERVAL -1 MONTH) AND NOW() 
            and o.user_key_id = u.user_key_id
            and o.order_id = od.order_id
            and od.item_id=i.item_id
            and u.store_id=%s
        group by i.item_id
        order by c DESC limit 10;
        """
    ####################################################################################################################
    cursor.execute(sql,store_id)
    item_info=cursor.fetchall()

    response_object['item_names']=[]
    response_object['item_qty']=[]

    for info in item_info:
        response_object['item_names'].append(info[1])
        response_object['item_qty'].append(info[2])


    print(response_object)
    return jsonify(response_object)


if __name__ == '__main__':
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='dhltlrdls', db='prjDB', charset='utf8')
    try:
        with db.cursor() as curs:
            cursor = db.cursor()
            app.run()
    finally:
        print('db close!!')
        db.close()
    