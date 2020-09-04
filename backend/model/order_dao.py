class OrderDao:

    def get_ordercompleted_list(self, filter_info, db_connection):

        """

        결제 완료 리스트 표출

        Args:
            db_connection : 연결된 db 객체

        Returns:
            결제 완료 리스트

        Author:
            tnwjd060124@gmail.com (손수정)

        History:
            2020-08-24 (tnwjd060124@gmail.com) : 초기 생성
            2020-09-01 (tnwjd060124@gmail.com) : 수정
                주문 시 유효한 데이터만 조회하도록 조건 추가
            2020-09-04 (tnwjd060124@gmail.com) : 수정
                제품명 검색조건 LIKE로 변경

        """

        with db_connection.cursor() as cursor:

            select_list = """
            SELECT
                P3.start_time AS order_time,
                P1.order_no,
                P2.order_product_no AS order_detail_no,
                P6.name AS product_name,
                P4.name AS size,
                P5.name AS color,
                P6.price,
                P2.quantity,
                P11.name AS user_name,
                P7.phone_number,
                P9.name AS order_status

            FROM
                orders AS P1
            """

            # 조회 기간 필터 존재하는 경우 추가
            if filter_info['from_date']:
                select_list += """
                INNER JOIN orders_details AS P3
                ON P1.order_no = P3.order_id
                AND P3.order_status_id=1
                AND P3.start_time > %(from_date)s
                """
            else:
                select_list += """
                INNER JOIN orders_details AS P3
                ON P1.order_no = P3.order_id
                AND P3.order_status_id=1
                """

            # 조회 기간 endDate 필터 존재하는 경우 추가
            if filter_info['to_date']:
                select_list += """
                AND P3.start_time < %(to_date)s
                """

            # 주문 상세정보 필터 존재하는 경우 추가
            if filter_info['order_detail_id']:
                select_list += """
                INNER JOIN order_product AS P2
                ON P3.order_detail_no = P2.order_detail_id
                AND P2.order_product_no = %(order_detail_id)s
                """
            else:
                select_list += """
                INNER JOIN order_product AS P2
                ON P3.order_detail_no = P2.order_detail_id
                """

            # JOIN 추가
            select_list += """
            INNER JOIN product_options AS P8
            ON P2.product_option_id = P8.product_option_no

            INNER JOIN option_details AS P10
            ON P8.product_option_no = P10.product_option_id
            AND P3.start_time >= P10.start_time
            AND P10.close_time >= P3.start_time

            INNER JOIN sizes AS P4
            ON P10.size_id = P4.size_no

            INNER JOIN colors AS P5
            ON P10.color_id = P5.color_no
            """

            # 제품명 필터 존재하는 경우 추가
            if filter_info['product_name']:
                select_list += """
                INNER JOIN product_details AS P6
                ON P8.product_id = P6.product_id
                AND P3.start_time >= P6.start_time
                AND P6.close_time >= P3.start_time
                AND P6.name LIKE %(product_name)s
                """
            else:
                select_list += """
                INNER JOIN product_details AS P6
                ON P8.product_id = P6.product_id
                AND P3.start_time >= P6.start_time
                AND P6.close_time >= P3.start_time
                """

            # JOIN 추가
            select_list += """
            INNER JOIN order_status AS P9
            ON P3.order_status_id = P9.order_status_no
            """

            # 핸드폰번호 필터 존재하는 경우 추가
            if filter_info['phone_number']:
                select_list += """
                INNER JOIN user_shipping_details AS P7
                ON P3.user_shipping_id = P7.user_shipping_detail_no
                AND P7.phone_number = %(phone_number)s
                """
            else:
                select_list += """
                INNER JOIN user_shipping_details AS P7
                ON P3.user_shipping_id = P7.user_shipping_detail_no
                """

            # 주문자명 필터 존재하는 경우 추가
            if filter_info['orderer']:
                select_list += """
                INNER JOIN users AS P11
                ON P1.user_id = P11.user_no
                AND P11.name = %(orderer)s
                """
            else:
                select_list +="""
                INNER JOIN users AS P11
                ON P1.user_id = P11.user_no
                """

            # 주문 id 필터 존재하는 경우 추가
            if filter_info['order_id']:
                select_list += """
                WHERE order_no = %(order_id)s
                """

            # 정렬 필터 존재하는 경우 주문일 오래된 순
            if filter_info['sort']:
                select_list += """
                ORDER BY P3.start_time ASC
                """
            else:
                select_list += """
                ORDER BY P3.start_time DESC
                """

            # limit, offset 설정 추가
            select_list += """
            LIMIT
                %(limit)s
            OFFSET
                %(offset)s
            """

            cursor.execute(select_list, filter_info)

            orders = cursor.fetchall()

            return orders

    def get_total_num(self, filter_info, db_connection):

        """

        총 결제 완료 건수 표출

        Args:
            filters : 필터 리스트
            db_connection : 연결된 db 객체

        Returns:
            총 결제 완료 건수

        Author:
            tnwjd060124@gmail.com (손수정)

        History:
            2020-08-25 (tnwjd060124@gmail.com) : 초기 생성
            2020-09-01 (tnwjd060124@gmail.com) : 수정
                주문시 유효한 데이터 조회하도록 조건 추가
            2020-09-04 (tnwjd060124@gmail.com) : 수정
                제품명 검색조건 LIKE로 변경

        """

        with db_connection.cursor() as cursor:

            count_num = """
            SELECT
                COUNT(*) AS total_number

            FROM
                orders AS P1
            """

            # 조회 기간 필터 존재하는 경우 추가
            if filter_info['from_date']:
                count_num += """
                INNER JOIN orders_details AS P3
                ON P1.order_no = P3.order_id
                AND P3.order_status_id=1
                AND P3.start_time > %(from_date)s
                """
            else:
                count_num += """
                INNER JOIN orders_details AS P3
                ON P1.order_no = P3.order_id
                AND P3.order_status_id=1
                """

            # 조회 기간 endDate 필터 존재하는 경우 추가
            if filter_info['to_date']:
                count_num += """
                AND P3.start_time < %(to_date)s
                """

            # 주문 상세정보 필터 존재하는 경우 추가
            if filter_info['order_detail_id']:
                count_num += """
                INNER JOIN order_product AS P2
                ON P3.order_detail_no = P2.order_detail_id
                AND P2.order_product_no = %(order_detail_id)s
                """
            else:
                count_num += """
                INNER JOIN order_product AS P2
                ON P3.order_detail_no = P2.order_detail_id
                """

            # JOIN 추가
            count_num += """
            INNER JOIN product_options AS P8
            ON P2.product_option_id = P8.product_option_no

            INNER JOIN option_details AS P10
            ON P8.product_option_no = P10.product_option_id
            AND P3.start_time >= P10.start_time
            AND P10.close_time >= P3.start_time

            INNER JOIN sizes AS P4
            ON P10.size_id = P4.size_no

            INNER JOIN colors AS P5
            ON P10.color_id = P5.color_no
            """

            # 제품명 필터 존재하는 경우 추가
            if filter_info['product_name']:
                count_num += """
                INNER JOIN product_details AS P6
                ON P8.product_id = P6.product_id
                AND P3.start_time >= P6.start_time
                AND P6.close_time >= P3.start_time
                AND P6.name LIKE %(product_name)s
                """
            else:
                count_num += """
                INNER JOIN product_details AS P6
                ON P8.product_id = P6.product_id
                AND P3.start_time >= P6.start_time
                AND P6.close_time >= P3.start_time
                """

            # JOIN 추가
            count_num += """
            INNER JOIN order_status AS P9
            ON P3.order_status_id = P9.order_status_no
            """

            # 핸드폰번호 필터 존재하는 경우 추가
            if filter_info['phone_number']:
                count_num += """
                INNER JOIN user_shipping_details AS P7
                ON P3.user_shipping_id = P7.user_shipping_detail_no
                AND P7.phone_number = %(phone_number)s
                """
            else:
                count_num += """
                INNER JOIN user_shipping_details AS P7
                ON P3.user_shipping_id = P7.user_shipping_detail_no
                """

            # 주문자명 필터 존재하는 경우 추가
            if filter_info['orderer']:
                count_num += """
                INNER JOIN users AS P11
                ON P1.user_id = P11.user_no
                AND P11.name = %(orderer)s
                """
            else:
                count_num +="""
                INNER JOIN users AS P11
                ON P1.user_id = P11.user_no
                """

            # 주문 id 필터 존재하는 경우 추가
            if filter_info['order_id']:
                count_num += """
                WHERE order_no = %(order_id)s
                """

            cursor.execute(count_num, filter_info)

            total_num = cursor.fetchone()

            return total_num

    def get_detail(self, order_detail, db_connection):

        """

        주문 상세정보 표출

        Args:
            order_detail:
                order_detail_id : 주문 상세 id
            db_connection: 연결된 db 객체

        Returns:
            주문 상세 정보

        Authors:
            tnwjd060124@gmail.com (손수정)

        History:
            2020-08-24 (tnwjd060124@gmail.com) : 초기 생성

        """

        with db_connection.cursor() as cursor:

            select_detail = """
            SELECT
                P2.order_no,
                P1.start_time AS order_time,
                P1.order_detail_no,
                P1.start_time AS paid_time,
                P3.name AS order_status,
                P10.name AS orderer,
                P4.phone_number,
                P6.product_no,
                P7.name AS product_name,
                P7.price,
                P8.name AS color,
                P9.name AS size,
                P11.quantity,
                P10.user_no,
                P4.receiver,
                P4.address,
                P4.delivery_request

            FROM
                orders_details P1

            INNER JOIN orders P2
            ON P1.order_id = P2.order_no

            INNER JOIN order_status P3
            ON P1.order_status_id = P3.order_status_no

            INNER JOIN user_shipping_details P4
            ON P1.user_shipping_id = P4.user_shipping_detail_no

            INNER JOIN order_product P11
            ON P1.order_detail_no = P11.order_detail_id

            INNER JOIN product_options P5
            ON P11.product_option_id = P5.product_option_no

            INNER JOIN option_details P12
            ON P5.product_option_no = P12.product_option_id

            INNER JOIN products P6
            ON P5.product_id = P6.product_no

            INNER JOIN product_details P7
            ON P5.product_id = P7.product_id

            INNER JOIN colors P8
            ON P12.color_id = P8.color_no

            INNER JOIN sizes P9
            ON P12.size_id = P9.size_no

            INNER JOIN users P10
            ON P2.user_id = P10.user_no

            WHERE order_detail_no = %(order_detail_id)s
            """

            cursor.execute(select_detail, order_detail)

            order_detail = cursor.fetchone()

            return order_detail

    def get_seller_product_info(self, product_info, db_connection):

        """

        서비스 페이지에서 상품의 옵션과 수량을 선택 후, 구매하기를 누르면 나오는
        주문하기 페이지중 '브랜디 배송 상품(구매할 상품 정보)'에 대한 정보입니다.

        Args:
            product_info  : 상품의 정보가 들어있는 객체입니다.(product_id, color_id, size_id)
            db_connection : 연결된 db 객체

        Returns:
            상품 id를 받아와 상품에 대한 이름, 이미지(S 사이즈)를 리턴해 줍니다.
            색상과 사이즈의 id값을 받아 해당 색상과 사이즈를 리턴해줍니다.

        Authors:
            minho.lee0716@gmail.com (이민호)
            tnwjd060124@gmail.com (손수정)

        History:
            2020-09-02 (minho.lee0716@gmail.com) : 초기 생성
            2020-09-02 (minho.lee0716@gmail.com) : 상품의 모든 정보를 받는 객체가 아닌 상품 id만 받는걸로 수정했습니다.
            2020-09-03 (minho.lee0716@gmail.com) : 상품의 모든 정보를 담는 객체를 받아 색상과 사이즈 또한 리턴.
            2020-09-04 (tnwjd060124@gmail.com) : 현재 유효한 데이터 리턴하는 조건 변경

        """

        try:

            with db_connection.cursor() as cursor:

                select_seller_product_info_query = """
                SELECT
                    P.product_no AS product_id,
                    C.name AS color_name,
                    S.name AS size_name,
                    PD.name,
                    PD.discount_rate,
                    PD.price,
                    I.image_small

                FROM products AS P

                LEFT JOIN product_details AS PD
                ON P.product_no = PD.product_id
                AND PD.is_activated = True
                AND PD.is_displayed = True
                AND PD.close_time = '9999-12-31 23:59:59'

                LEFT JOIN product_images AS PI
                ON P.product_no = PI.product_id
                AND PI.is_main = True
                AND PI.close_time = '9999-12-31 23:59:59'

                LEFT JOIN images AS I
                ON PI.image_id = I.image_no
                AND I.is_deleted = False

                LEFT JOIN product_options AS PO
                ON P.product_no = PO.product_id
                AND PO.is_deleted = False

                LEFT JOIN option_details AS OD
                ON PO.product_option_no = OD.product_option_id
                AND OD.close_time = '9999-12-31 23:59:59'

                LEFT JOIN colors AS C
                ON OD.color_id = C.color_no

                LEFT JOIN sizes AS S
                ON OD.size_id = S.size_no

                WHERE
                    P.is_deleted = False
                    AND P.product_no = %(product_id)s
                    AND C.color_no = %(color_id)s
                    AND S.size_no = %(size_id)s;
                """

                # 상품 번호만 받아와 해당 상품의 정보들을 seller_product에 담아줍니다.
                cursor.execute(select_seller_product_info_query, product_info)
                seller_product_info = cursor.fetchone()

                # 셀러의 상품이(구매하려는 상품) 존재하지 않을 경우 예외처리
                if not seller_product_info:
                    raise Exception('THIS_PRODUCT_DOES_NOT_EXISTS')

                return seller_product_info

        except  Exception as e:
            raise e

    def get_orderer_info(self, user_no, db_connection):

        """

        해당 유저의 id 정보(user_no)를 받아와 유저의 이름와 이메일, 그리고 배송지 정보들을  리턴해 줍니다.
        상품의 옵션을 선택 후, 구매하기를 눌렀을 때 나오는 '주문자 정보' + '배송지 정보'에 대한 정보입니다.

        Args:
            user_no       : 해당 유저의 id
            db_connection : 연결된 db 객체

        Returns:
            해당 유저의 이름과 이메일, 그리고 배송지 정보들을  리턴해 줍니다.

        Authors:
            minho.lee0716@gmail.com (이민호)

        History:
            2020-09-02 (minho.lee0716@gmail.com) : 초기 생성
            2020-09-02 (minho.lee0716@gmail.com) : 수정
                get_shipping_address_info라는 함수를 없애고 한 번에 유저의 정보와 배송지 정보를 리턴하기로 했습니다.

        """

        try:

            with db_connection.cursor() as cursor:

                # U라는 테이블이 '주문자 정보'에 관한 정보입니다.
                # USD라는 테이블은 '배송지 정보'에 관한 정보입니다.
                select_orderer_info_query = """
                SELECT
                    U.name AS orderer_name,
                    U.email AS orderer_email,
                    USD.receiver,
                    USD.phone_number,
                    USD.address,
                    USD.additional_address,
                    USD.zip_code

                FROM
                users AS U

                LEFT JOIN user_shipping_details AS USD
                ON U.user_no = USD.user_id

                WHERE
                    U.is_deleted = False
                    AND U.user_no = %s;
                """

                # 헤더의 토큰에서 유저의 id를 받아와 인자로 넣어주면,
                # 해당 유저의 이름, 이메일, 그리고 배송지 정보들(존재하지 않으면 NULL)을 리턴해 줍니다.
                cursor.execute(select_orderer_info_query, user_no)
                orderer_info = cursor.fetchone()

                # 유저의 정보가 존재하지 않는다면
                if not orderer_info:
                    raise Exception('UNAUTHORIZED')

                return orderer_info

        except Exception as e:
            raise e
