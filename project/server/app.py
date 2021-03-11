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

@app.route('/api/login', methods=['POST'])
def login_auth():

    response_object = {'status':'success'}
    post_data = request.get_json()
    
    user_id=post_data['id']
    user_pw=post_data['pw']#client가 보낸 아이디, 패스워드

    sql="SELECT user_key_id, store_id, user_pw FROM user WHERE user_id=%s"#유저 검색
    rows_count = cursor.execute(sql, user_id)

    if rows_count > 0:
        user_info = cursor.fetchone()
        #print('user info:', user_info)
        if bcrypt.checkpw(user_pw.encode('utf-8'), user_info[2].encode('utf-8')):
        
            response_object['message'] = 'login success'
            store_id=user_info[1]
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

            response_object['message'] = 'new access token'
        
        user_key_id=payload['user_key_id']
        store_id=payload['store_id']
      
        ####################사용자의 아이디, 이름, 번호, 매장 아이디, 매장 위치 , user key#########################
        sql="""
            SELECT u.user_id, u.user_name, u.user_contact, s.store_id, s.store_location, s.store_name
            FROM `user` u, store s
            WHERE u.user_key_id=%s and s.store_id = u.store_id;
            """
        ################################################################################################
        cursor.execute(sql, user_key_id)
        user_info = cursor.fetchone()

        response_object['user_id']=user_info[0]
        response_object['user_name']=user_info[1]
        response_object['user_contact']=user_info[2]
        response_object['store_id']=user_info[3]
        response_object['store_location']=user_info[4]
        response_object['store_name']=user_info[5]
        response_object['user_key_id']=user_key_id
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

    response_object = {'status':'success'}
    post_data = request.get_json()
    store_id=post_data.get('store_id')

    #####################해당 매장 위치, 매장 번호, 본사###########################
    sql="""
        SELECT s.store_location, s.store_contact, s.store_name,
            (select headquarters_name
            from headquarters
            where headquarters_id=s.headquarters_id) headquarters_name
        FROM store s
        WHERE s.store_id=%s ;
        """
    ########################################################################
    cursor.execute(sql, store_id)
    user_info = cursor.fetchone()

    response_object['store_location']=user_info[0] #주소
    response_object['store_contact']=user_info[1] #연락처
    response_object['store_name']=user_info[2]  #가게명
    response_object['headquarters_name']=user_info[3] #본사명

    # store_db.close()
    print('store'*20,response_object)
    return jsonify(response_object)


@app.route('/api/item_info', methods=['POST'])#아이템 정보 반환
def get_itemInfo():

    post_data = request.get_json()
    print(post_data)
    store_id=post_data.get('store_id')
    response_object = {'status':'success'}

    ###############아이템 아이디, 이름, 가격, 단위, 재고, 정보, 태그###############
    sql="""
        SELECT i.*
        FROM store s, item i
        WHERE s.store_id=%s and s.headquarters_id=i.headquarters_id;
        """
    #####################################################################
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

    return jsonify(response_object)

@app.route('/api/order_info', methods=['POST'])#사용자가 가장 최근 발주한 내역
def get_orderInfo():

    print('---------get order_info------------')
    response_object = {'status':'success'}
    post_data = request.get_json()
    print(post_data)
    user_key_id=post_data.get('user_key_id')

    
    ################아이템 아이디, 이름, 가격, 단위, 재고, 정보, 태그, 주문상세 수량, 발주 금액, 날짜##############
    sql="""
        SELECT i.*, od.detail_qty, od.detail_total_price, (select `date` from `order`where order_id=od.order_id)
        FROM order_detail od, item i
        where od.order_id=(select order_id from `order` where user_key_id=%s order by `date` DESC limit 1)
        and od.item_id=i.item_id
        """
    cursor.execute(sql, user_key_id)
    order_info = cursor.fetchall()
    print(order_info)

    response_object['order_info']=[]
    response_object['date']=order_info[0][-1].strftime('%Y-%m-%d %H:%M:%S')
    
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

    return jsonify(response_object)



@app.route('/api/order', methods=['POST','PUT'])#발주 저장 
def put_orderInfo():


    print('put order')
    response_object = {'status':'success'}
    post_data = request.get_json()
    
    orderInfo=post_data['items']
    print(orderInfo)
    
    user_key_id=post_data.get('user_key_id')
    store_id=post_data.get('store_id')
    total_price=post_data.get('total_price')
    
    summary=orderInfo[0]['name']
    if len(orderInfo)>1:
        summary+=' 외 '+str(len(orderInfo)-1)
    now = datetime.now()

    ###order insert
    sql="""
        INSERT INTO `prjDB2`.`order` (`date`, `user_key_id`, `total_price`, `summary`, `store_id`) VALUES (%s, %s, %s, %s, %s);
        """


    cursor.execute(sql, (now.strftime('%Y-%m-%d %H:%M:%S'),user_key_id,total_price,summary,store_id))
    id_num=cursor.lastrowid#방금 insert 한 order_id

    insert_list=[]
    update_list=[]

    # excutemany 처리를 위한 for 문
    for info in orderInfo:
        insert_list.append([info['qty'], info['qty']*info['price'], id_num, info['id']])
        update_list.append([info['stock']-info['qty'], info['id']])

    ### order detail insert
    sql="""
        INSERT INTO `prjDB2`.`order_detail` (`detail_qty`, `detail_total_price`, `order_id`, `item_id`) VALUES (%s, %s, %s, %s);
        """
    cursor.executemany(sql, insert_list)


    db.commit()



    ### item stock update
    sql="""
        UPDATE `prjDB2`.`item` SET `item_stock` = %s WHERE (`item_id` = %s);
    """
    cursor.executemany(sql, update_list)

    db.commit()

    return jsonify(response_object)

@app.route('/api/my_page', methods=['POST'])#마이페이지 들어갔을때
def get_MyPage():

    print('-----my page 1-----')
    response_object = {'status':'success'}
    post_data= request.get_json()

    store_id=post_data.get('store_id')

    sql="""
        SELECT o.order_id, o.`date`, (select user_id from `user` where user_key_id=o.user_key_id) id, o.total_price, o.summary
        FROM `order` o
        where o.store_id=%s
        order by o.`date` desc
        ;
        """
    cursor.execute(sql,store_id)
    orderInfo=cursor.fetchall()

    print(orderInfo)
    response_object['order_info']=[]
    for info in orderInfo:
        temp={
            'order_id':info[0],
            'date':info[1].strftime('%Y-%m-%d %H:%M:%S'),
            'user_id':info[2],
            'total_price':info[3],
            'summary':info[4]
        }
        response_object['order_info'].append(temp)

    print(response_object['order_info'])
    return jsonify(response_object)

@app.route('/api/order_detail', methods=['POST'])#order_id 받아와서 상세 내용 반환  
def get_detail():

    print('---get_detail---')
    response_object = {'status':'success'}
    post_data= request.get_json()
    order_id=post_data.get('order_id')

    sql="""
        select o.`date`, 
            (select user_id from `user` where user_key_id=o.user_key_id) id,
            od.detail_qty, od.detail_total_price,
            i.item_name, i.item_price, i.item_stock, i.item_info, i.item_tag, i.item_unit, i.item_id
        from `order` o, order_detail od, item i
        where o.order_id=%s
            and o.order_id=od.order_id
            and od.item_id=i.item_id
        ;
        """

    cursor.execute(sql,order_id)
    detailInfo=cursor.fetchall()

    response_object['detail_info']=[]

    for info in detailInfo:
        temp={
            'date':info[0].strftime('%Y-%m-%d %H:%M:%S'),
            'user_id':info[1],
            'qty':info[2],
            'total_price':info[3],
            'name':info[4],
            'price':info[5],
            'stock':info[6],
            'info':info[7],
            'tag':info[8],
            'unit':info[9],
            'id':info[10],
            'check':True
        }
        if temp['tag']==None:
            temp['tag']='기타'
        
        response_object['detail_info'].append(temp)

    

    return jsonify(response_object)


@app.route('/api/dash_board_summary', methods=['POST'])#메인 홈 요약 대시보드
def dash_board_summary():

    print('----dash_board_summary------')
    response_object = {'status':'success'}
    post_data = request.get_json()
    store_id=post_data.get('store_id')



    #############################################날짜, 발주 수, 해당 날짜 발주 총 금액##########################################
    sql="""
        SELECT date_format(o.`date`,'%%Y-%%m-%%d') `day`, count(o.order_id) `count`, sum(o.total_price) sum
        FROM `order` o
        WHERE o.store_id=%s and o.`date` BETWEEN DATE_ADD(NOW(), INTERVAL -1 MONTH) AND NOW()
        group by `day`
        order by `day`;
        """
    ####################################################################################################################
    # SELECT date_format(o.`date`,'%%Y-%%m-%%d') `day`, count(*) `count`, sum(od.detail_total_price) sum
    #     FROM `order` o, order_detail od
    #     WHERE o.user_key_id in(select user_key_id from `user` where store_id=%s)
	#         and o.`date` BETWEEN DATE_ADD(NOW(), INTERVAL -1 MONTH) AND NOW()
    #         and o.order_id = od.order_id
    #     group by `day`
    #     order by `day`;

    cursor.execute(sql,store_id)
    orderInfo=cursor.fetchall()


    response_object['frq']=[]#빈도
    response_object['payment']=[]#지출
    response_object['dates']=[]#날짜


    for info in orderInfo:
        response_object['dates'].append(info[0])
        response_object['frq'].append(info[1])
        response_object['payment'].append(info[2])


    #################################태그, 태그 수######################################..................
    sql="""
        SELECT i.item_tag, count(*)
        FROM `order` o, order_detail od, `user` u, item i
        WHERE o.store_id=%s
            and o.`date` BETWEEN DATE_ADD(NOW(), INTERVAL -1 MONTH) AND NOW() 
            and o.order_id = od.order_id
            and od.item_id=i.item_id
        group by i.item_tag;
        """
    #################################################################################
    #  SELECT i.item_tag, count(*)
    #     FROM `order` o, order_detail od, `user` u, item i
    #     WHERE o.user_key_id in(select user_key_id from `user` where store_id=%s)
    #         and o.`date` BETWEEN DATE_ADD(NOW(), INTERVAL -1 MONTH) AND NOW() 
    #         and o.order_id = od.order_id
    #         and od.item_id=i.item_id
    #     group by i.item_tag;
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

    print('----dash_board_stacked------')
    response_object = {'status':'success'}
    post_data = request.get_json()
    store_id=post_data.get('store_id')

    ##############해당 매점을 관리하는 사용자 id##############......................
    sql="""
        select user_key_id, user_id from `user` where store_id=%s;
        """
    ###################################################
    cursor.execute(sql,store_id)
    
    users=""
    user_key_ids=[]
    # ids=[]
    response_object['users']=[]
    user_info=cursor.fetchall()
    for user_key, user_id in user_info:
        users+=", SUM(IF(user_key_id = " + str(user_key) + ", c, 0)) AS " + str(user_id) +" "
        # ids.append(user_id)
        response_object['users'].append(user_id)
        response_object[user_id]=[]
        user_key_ids.append(str(user_key))
    user_key_ids=",".join(user_key_ids)


    ################################ 날짜, 사용자별 발주 수 #################################
 
    sql="""
        select `day` %s
        FROM (
            SELECT date_format(o.`date`,'%%Y-%%m-%%d') `day`, o.user_key_id, count(*) c
            FROM `order` o
            WHERE o.user_key_id in(%s)
                and o.`date` BETWEEN DATE_ADD(NOW(), INTERVAL -1 MONTH) AND NOW() 
            group by `day`, o.user_key_id
        ) us
        group by `day`
        order by `day`
        ;
    """
    sql = sql%(users,user_key_ids)
    print(sql)
    cursor.execute(sql)
    orderInfo=cursor.fetchall()

    response_object['dates']=[]#날짜

    for info in orderInfo:
        response_object['dates'].append(info[0])
        for i in range(len(user_info)):
            # print(user_ids[i],info[1+i])
            response_object[response_object['users'][i]].append(info[i+1])


    print(response_object)
    return jsonify(response_object)


@app.route('/api/dash_board_item', methods=['POST'])#대시보드 물품 순위
def dash_board_item():

    print('-------dash_board_item------')
    response_object = {'status':'success'}
    post_data = request.get_json()
    store_id=post_data.get('store_id')



    ############################아이템 아이디, 이름, 발주된 수#################################......
    sql="""
        SELECT od.item_id,(select item_name from item where item_id=od.item_id) item_name, sum(od.detail_qty) c
        FROM `order` o, order_detail od
        WHERE o.store_id = %s
            and o.`date` BETWEEN DATE_ADD(NOW(), INTERVAL -1 MONTH) AND NOW()
            and o.order_id = od.order_id
        group by od.item_id
        order by c DESC limit 7;
        """
    #####################################################################################
    # SELECT i.item_id,i.item_name, count(*) c
    #     FROM `order` o, order_detail od, `user` u, item i
    #     WHERE o.`date` BETWEEN DATE_ADD(NOW(), INTERVAL -1 MONTH) AND NOW() 
    #         and o.user_key_id = u.user_key_id
    #         and o.order_id = od.order_id
    #         and od.item_id=i.item_id
    #         and u.store_id=%s
    #     group by i.item_id
    #     order by c DESC limit 7;
    cursor.execute(sql,store_id)
    item_info=cursor.fetchall()

    response_object['item_names']=[]
    response_object['item_qty']=[]

    for info in item_info:
        response_object['item_names'].append(info[1])
        response_object['item_qty'].append(info[2])


    print(response_object)
    return jsonify(response_object)

@app.route('/api/dash_board_payment', methods=['POST'])#대시보드-payment
def dash_board_payment():

    print('-------dash_board_payment------')
    response_object = {'status':'success'}
    post_data = request.get_json()
    store_id=post_data.get('store_id')

    #######################################날짜, 발주 금액 총합###########################################
    sql="""
        SELECT date_format(o.`date`,'%%Y-%%m-%%d') `day`,  sum(o.total_price) sum
        FROM `order` o
        WHERE o.store_id=%s
            and o.`date` BETWEEN DATE_ADD(NOW(), INTERVAL -1 YEAR) AND NOW()
        group by `day`
        order by `day`;
        """
    ###############################################################################################
    
        # SELECT date_format(o.`date`,'%%Y-%%m-%%d') `day`, sum(od.detail_total_price) sum
        # FROM `order` o, order_detail od
        # WHERE o.user_key_id in(select user_key_id from `user` where store_id=%s)
	    #     and o.`date` BETWEEN DATE_ADD(NOW(), INTERVAL -1 YEAR) AND NOW()
        #     and o.order_id = od.order_id
        # group by `day`
        # order by `day`;

    response_object['payment_year']=[]
    response_object['dates_year']=[]

    cursor.execute(sql, store_id)
    item_info=cursor.fetchall()

    for info in item_info:
        response_object['dates_year'].append(info[0])
        response_object['payment_year'].append(info[1])

    print(response_object)
    return jsonify(response_object)


if __name__ == '__main__':
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='dhltlrdls', db='prjDB2', charset='utf8')
    try:
        with db.cursor() as curs:
            cursor = db.cursor()
            app.run()
    finally:
        print('db close!!')
        db.close()
    