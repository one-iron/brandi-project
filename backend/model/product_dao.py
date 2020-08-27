from flask import jsonify

class ProductDao:

    def insert_product(self, db_connection):
        """
        product table insert function

        Args:
            db_connection : DATABASE Connection Instance

        Returns:
            200: SUCCESS, (상품등록 완료)

        Author:
            sincerity410@gmail.com (이곤호)

        History:
            2020-08-25 (sincerity410@gmail.com) : 초기생성
        """
        try:
            with db_connection.cursor() as cursor:
                insert_product_query = """
                    INSERT INTO products (
                        created_at,
                        is_deleted
                        ) VALUES (
                        DEFAULT,
                        DEFAULT
                        );
                """

                affected_row = cursor.execute(insert_product_query)

                if affected_row == -1:
                    raise Exception('QUERY_FAILED')

                return cursor.lastrowid

        except Exception as e:
            raise e

    def insert_product_detail(self, product_info, db_connection):
        """
        상품등록 Model Function

        Args:
            product_info  : ProductService.create_product로 받은 Parameter
            db_connection : DATABASE Connection Instance

        Returns:
            200: SUCCESS, (상품등록 완료)

        Author:
            sincerity410@gmail.com (이곤호)

        History:
            2020-08-25 (sincerity410@gmail.com) : 초기생성
        """

        try:
            with db_connection.cursor() as cursor:
                insert_product_detail_query = """
                    INSERT INTO product_details (
                        product_id,
                        is_activated,
                        is_displayed,
                        main_category_id,
                        sub_category_id,
                        name,
                        simple_description,
                        detail_information,
                        price,
                        discount_rate,
                        discount_start_date,
                        discount_end_date,
                        min_sales_quantity,
                        max_sales_quantity
                        ) VALUES (
                        %(product_id)s,
                        %(sellYn)s,
                        %(exhibitionYn)s,
                        %(mainCategoryId)s,
                        %(subCategoryId)s,
                        %(productName)s,
                        %(simpleDescription)s,
                        %(detailInformation)s,
                        %(price)s,
                        %(discountRate)s,
                        %(discountStartDate)s,
                        %(discountEndDate)s,
                        %(minSalesQuantity)s,
                        %(maxSalesQuantity)s
                        )
                """

                affected_row = cursor.execute(insert_product_detail_query, product_info)

                if affected_row == -1:
                    raise Exception('QUERY_FAILED')

                return cursor.lastrowid

        except Exception as e:
            raise e
        return jsonify({'message' : 'SUCCESS'}), 200

    def select_product_list(self, db_connection):
        cursor = db_connection.cursor()

        SQL = """
        SELECT
            P.product_no,
            I.image AS thumbnail_image,
            PD.name AS product_name,
            PD.price,
            PD.discount_rate

        FROM products as P

        LEFT JOIN product_images as PI
        ON P.product_no = PI.product_id

        LEFT JOIN images as I
        ON PI.image_id = I.image_no

        LEFT JOIN product_details as PD
        ON P.product_no = PD.product_id

        WHERE
            P.is_deleted = False AND
            PI.is_main = True AND
            I.is_deleted = False AND
            PD.is_activated = True AND
            PD.is_displayed = True
        """

        cursor.execute(SQL)
        products = cursor.fetchall()

        return products
