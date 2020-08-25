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

        """

        cursor = db_connection.cursor()

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

        INNER JOIN orders_details AS P3
        ON P1.order_no = P3.order_id
        AND P3.order_status_id=1
        AND P3.start_time > CASE
        WHEN %(from_date)s IS NULL THEN '1970-01-01 00:00:00' ELSE %(from_date)s END

        INNER JOIN order_product AS P2
        ON P3.order_detail_no = P2.order_id
        AND P2.order_product_no LIKE %(order_detail_id)s

        INNER JOIN product_options AS P8
        ON P2.product_option_id = P8.product_option_no

        INNER JOIN option_details AS P10
        ON P8.product_option_no = P10.product_option_id

        INNER JOIN sizes AS P4
        ON P10.size_id = P4.size_no

        INNER JOIN colors AS P5
        ON P10.color_id = P5.color_no

        INNER JOIN user_shipping_details AS P7
        ON P3.user_shipping_id = P7.user_shipping_detail_no
        AND P7.phone_number LIKE %(phone_number)s

        INNER JOIN product_details AS P6
        ON P8.product_id = P6.product_id
        AND P6.name LIKE %(product_name)s

        INNER JOIN order_status AS P9
        ON P3.order_status_id = P9.order_status_no

        INNER JOIN users AS P11
        ON P1.user_id = P11.user_no
        AND P11.name LIKE %(orderer)s

        WHERE order_no LIKE %(order_id)s

        ORDER BY
            (CASE WHEN %(sort)s = 1 THEN P3.start_time END) DESC,
            (CASE WHEN %(sort)s <> 1 THEN P3.start_time END) ASC

        LIMIT
            %(limit)s
        OFFSET
            %(offset)s

        """
        cursor.execute(select_list, filter_info)
        orders = cursor.fetchall()

        return orders

    def get_total_num(self, filters, db_connection):
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

        """
        cursor = db_connection.cursor()

        count_num = """
        SELECT
            COUNT(*) AS total_number

        FROM
            orders AS P1

        INNER JOIN orders_details AS P3
        ON P1.order_no = P3.order_id
        AND P3.order_status_id=1
        AND P3.start_time > CASE
        WHEN %(from_date)s IS NULL THEN '1970-01-01 00:00:00' ELSE %(from_date)s END

        INNER JOIN order_product AS P2
        ON P3.order_detail_no = P2.order_id
        AND P2.order_product_no LIKE %(order_detail_id)s

        INNER JOIN product_options AS P8
        ON P2.product_option_id = P8.product_option_no

        INNER JOIN option_details AS P10
        ON P8.product_option_no = P10.product_option_id

        INNER JOIN sizes AS P4
        ON P10.size_id = P4.size_no

        INNER JOIN colors AS P5
        ON P10.color_id = P5.color_no

        INNER JOIN user_shipping_details AS P7
        ON P3.user_shipping_id = P7.user_shipping_detail_no
        AND P7.phone_number LIKE %(phone_number)s

        INNER JOIN product_details AS P6
        ON P8.product_id = P6.product_id
        AND P6.name LIKE %(product_name)s

        INNER JOIN order_status AS P9
        ON P3.order_status_id = P9.order_status_no

        INNER JOIN users AS P11
        ON P1.user_id = P11.user_no
        AND P11.name LIKE %(orderer)s

        WHERE order_no LIKE %(order_id)s
        """

        cursor.execute(count_num, filters)
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

        cursor = db_connection.cursor()

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
        ON P1.order_detail_no = P11.order_id

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