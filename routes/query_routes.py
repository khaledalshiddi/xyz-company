from flask import Blueprint, jsonify
from db.connection import get_connection

query_blueprint = Blueprint('query', __name__)
@query_blueprint.route('/q1', methods=['GET'])
def query_1():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT DISTINCT E.Eid, P2.Fname, P2.Lname
            FROM PERSON P
            JOIN APPLICATION A ON P.Person_id = A.Applicant_id
            JOIN INTERVIEW I ON A.App_id = I.App_id
            JOIN EMPLOYEE E ON I.Interviewer_id = E.Eid
            JOIN PERSON P2 ON E.Eid = P2.Person_id
            WHERE P.Fname = 'Hellen' AND P.Lname = 'Cole' AND A.Jpid = 11111;
        """)

        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@query_blueprint.route('/q2', methods=['GET'])
def query_2():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT J.Jpid
            FROM JOB_POSITION J
            JOIN DEPARTMENT D ON J.Dept_ID = D.Dept_id
            WHERE D.Dname = 'Marketing' 
              AND J.Posted_date BETWEEN '2011-01-01' AND '2011-01-31';
        """)

        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@query_blueprint.route('/q3', methods=['GET'])
def query_3():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT E.Eid, P.Fname, P.Lname
            FROM EMPLOYEE E
            JOIN PERSON P ON E.Eid = P.Person_id
            WHERE E.Eid NOT IN (
                SELECT DISTINCT Super_id
                FROM EMPLOYEE
                WHERE Super_id IS NOT NULL
            );
        """)

        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@query_blueprint.route('/q4', methods=['GET'])
def query_4():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT MS.Site_id, MS.Slocation
            FROM MARKETING_SITE MS
            WHERE MS.Site_id NOT IN (
                SELECT Site_id
                FROM SALE
                WHERE Sale_time BETWEEN '2011-03-01' AND '2011-03-31'
            );
        """)

        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@query_blueprint.route('/q5', methods=['GET'])
def query_5():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT J.Jpid, J.Jdescription
            FROM JOB_POSITION J
            WHERE NOT EXISTS (
                SELECT 1
                FROM APPLICATION A
                WHERE A.Jpid = J.Jpid
                  AND A.Is_selected = 1
                  AND A.App_date <= DATE_ADD(J.Posted_date, INTERVAL 1 MONTH)
            );
        """)

        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@query_blueprint.route('/q6', methods=['GET'])
def query_6():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT DISTINCT E.Eid AS Employee_id, P.Fname AS First_name, P.Lname AS Last_name
            FROM EMPLOYEE E
            JOIN PERSON P ON E.Eid = P.Person_id
            WHERE NOT EXISTS (
                SELECT PT.Ptype
                FROM PRODUCT PT
                WHERE PT.List_price > 200
                  AND PT.Ptype NOT IN (
                      SELECT PR.Ptype
                      FROM SALE S
                      JOIN SALE_DETAIL SD ON S.Sale_id = SD.Sale_id
                      JOIN PRODUCT PR ON SD.Product_id = PR.Product_id
                      WHERE S.Sman_id = E.Eid
                  )
            );
        """)

        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@query_blueprint.route('/q7', methods=['GET'])
def query_7():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT D.Dept_id, D.Dname
            FROM DEPARTMENT D
            WHERE D.Dept_id NOT IN (
                SELECT J.Dept_ID
                FROM JOB_POSITION J
                WHERE J.Posted_date BETWEEN '2011-01-01' AND '2011-02-01'
            );
        """)

        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@query_blueprint.route('/q8', methods=['GET'])
def query_8():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT E.Eid, P.Fname, P.Lname, J.Dept_ID
            FROM APPLICATION A
            JOIN JOB_POSITION J ON A.Jpid = J.Jpid
            JOIN EMPLOYEE E ON A.Applicant_id = E.Eid
            JOIN PERSON P ON E.Eid = P.Person_id
            WHERE A.Jpid = 12345;
        """)

        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@query_blueprint.route('/q9', methods=['GET'])
def query_9():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT PR.Ptype
            FROM PRODUCT PR
            JOIN SALE_DETAIL SD ON PR.Product_id = SD.Product_id
            GROUP BY PR.Ptype
            ORDER BY SUM(SD.Quantity) DESC
            LIMIT 1;
        """)

        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@query_blueprint.route('/q10', methods=['GET'])
def query_10():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT R.Ptype, SUM(R.revenue - COALESCE(C.cost, 0)) AS net_profit
            FROM (
                SELECT 
                    P.Product_id,
                    P.Ptype,
                    SUM(SD.Quantity * SD.Unit_price) AS revenue
                FROM PRODUCT P
                JOIN SALE_DETAIL SD ON P.Product_id = SD.Product_id
                GROUP BY P.Product_id, P.Ptype
            ) AS R
            LEFT JOIN (
                SELECT 
                    PP.Product_id,
                    SUM(PP.Quantity * AVG_VP.avg_price) AS cost
                FROM PRODUCT_PART PP
                JOIN (
                    SELECT Part_id, AVG(Price) AS avg_price
                    FROM VENDOR_PART
                    GROUP BY Part_id
                ) AS AVG_VP ON PP.Part_id = AVG_VP.Part_id
                GROUP BY PP.Product_id
            ) AS C ON R.Product_id = C.Product_id
            GROUP BY R.Ptype
            ORDER BY net_profit DESC
            LIMIT 1;
        """)

        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@query_blueprint.route('/q11', methods=['GET'])
def query_11():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT E.Eid, P.Fname, P.Lname
            FROM EMPLOYEE E
            JOIN PERSON P ON E.Eid = P.Person_id
            WHERE NOT EXISTS (
                SELECT D.Dept_id
                FROM DEPARTMENT D
                WHERE D.Dept_id NOT IN (
                    SELECT WA.Dept_id
                    FROM WORK_ASSIGNMENT WA
                    WHERE WA.Emp_id = E.Eid
                )
            );
        """)

        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@query_blueprint.route('/q12', methods=['GET'])
def query_12():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT P.Fname, P.Lname, P.Email
            FROM APPLICATION A
            JOIN PERSON P ON A.Applicant_id = P.Person_id
            WHERE A.Is_selected = 1;
        """)

        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@query_blueprint.route('/q13', methods=['GET'])
def query_13():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT 
                P.Fname, P.Lname, P.Email,
                GROUP_CONCAT(PN.Phone_num SEPARATOR ', ') AS PhoneNumbers
            FROM PERSON P
            JOIN APPLICATION A ON P.Person_id = A.Applicant_id
            JOIN PHONE_NUMBER PN ON P.Person_id = PN.Person_id
            WHERE P.Person_id IN (
                SELECT Applicant_id
                FROM APPLICATION
                GROUP BY Applicant_id
                HAVING COUNT(*) = SUM(Is_selected)
            )
            GROUP BY P.Person_id, P.Fname, P.Lname, P.Email;
        """)

        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@query_blueprint.route('/q14', methods=['GET'])
def query_14():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            WITH monthly_avg AS (
                SELECT 
                    S.Eid,
                    YEAR(S.Pay_date) AS yr,
                    MONTH(S.Pay_date) AS mon,
                    SUM(S.Amount) AS monthly_total
                FROM SALARY S
                GROUP BY S.Eid, YEAR(S.Pay_date), MONTH(S.Pay_date)
            ),
            avg_per_employee AS (
                SELECT Eid, AVG(monthly_total) AS avg_monthly_salary
                FROM monthly_avg
                GROUP BY Eid
            )
            SELECT E.Eid, P.Fname, P.Lname, A.avg_monthly_salary
            FROM avg_per_employee A
            JOIN EMPLOYEE E ON A.Eid = E.Eid
            JOIN PERSON P ON E.Eid = P.Person_id
            ORDER BY A.avg_monthly_salary DESC
            LIMIT 1;
        """)

        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@query_blueprint.route('/q15', methods=['GET'])
def query_15():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT V.Vendor_id, V.Vname
            FROM VENDOR V
            JOIN VENDOR_PART VP ON V.Vendor_id = VP.Vendor_id
            JOIN PART P ON VP.Part_id = P.Part_id
            WHERE P.Pname = 'Cup' AND P.Weight < 4
              AND VP.Price = (
                  SELECT MIN(VP2.Price)
                  FROM VENDOR_PART VP2
                  JOIN PART P2 ON VP2.Part_id = P2.Part_id
                  WHERE P2.Pname = 'Cup' AND P2.Weight < 4
              );
        """)

        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
@query_blueprint.route('/view1', methods=['GET'])
def view_1():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM AvgMonthlySalary;")
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@query_blueprint.route('/view2', methods=['GET'])
def view_2():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM PassedInterviewRounds;")
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@query_blueprint.route('/view3', methods=['GET'])
def view_3():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM View3_ProductsSold;")
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@query_blueprint.route('/view4', methods=['GET'])
def view_4():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM PartCostPerProduct;")
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500