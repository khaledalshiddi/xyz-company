from flask import Blueprint, request, jsonify
from db.connection import get_connection

crud_blueprint = Blueprint('crud', __name__)

@crud_blueprint.route('/persons', methods=['GET'])
def get_all_persons():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM PERSON")
        persons = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(persons)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@crud_blueprint.route('/persons', methods=['POST'])
def create_person():
    data = request.json
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO PERSON (Fname, Lname, Age, Gender, Email, Addr_line_one, Addr_line_two, City, State, Zip)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            data['Fname'],
            data['Lname'],
            data['Age'],
            data['Gender'],
            data['Email'],
            data['Addr_line_one'],
            data['Addr_line_two'],
            data['City'],
            data['State'],
            data['Zip']
        )
        cursor.execute(query, values)
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Person created successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
@crud_blueprint.route('/persons/<int:person_id>', methods=['PUT'])
def update_person(person_id):
    data = request.json
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = """
            UPDATE PERSON SET
                Fname = %s,
                Lname = %s,
                Age = %s,
                Gender = %s,
                Email = %s,
                Addr_line_one = %s,
                Addr_line_two = %s,
                City = %s,
                State = %s,
                Zip = %s
            WHERE Person_id = %s
        """
        values = (
            data['Fname'],
            data['Lname'],
            data['Age'],
            data['Gender'],
            data['Email'],
            data['Addr_line_one'],
            data['Addr_line_two'],
            data['City'],
            data['State'],
            data['Zip'],
            person_id
        )
        cursor.execute(query, values)
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Person updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# deleting a person
@crud_blueprint.route('/persons/<int:person_id>', methods=['DELETE'])
def delete_person(person_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM PERSON WHERE Person_id = %s", (person_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Person deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@crud_blueprint.route('/employees', methods=['GET'])
def get_all_employees():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT E.Eid, P.Fname, P.Lname, E.Title, E.Emp_rank, E.Super_id
            FROM EMPLOYEE E
            JOIN PERSON P ON E.Eid = P.Person_id
        """)
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@crud_blueprint.route('/employees', methods=['POST'])
def create_employee():
    data = request.json
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO EMPLOYEE (Eid, Title, Emp_rank, Super_id)
            VALUES (%s, %s, %s, %s)
        """
        values = (
            data['Eid'],          # Must already exist in PERSON
            data['Title'],
            data['Emp_rank'],
            data['Super_id']
        )
        cursor.execute(query, values)
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Employee added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@crud_blueprint.route('/employees/<int:eid>', methods=['PUT'])
def update_employee(eid):
    data = request.json
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = """
            UPDATE EMPLOYEE SET
                Title = %s,
                Emp_rank = %s,
                Super_id = %s
            WHERE Eid = %s
        """
        values = (
            data['Title'],
            data['Emp_rank'],
            data['Super_id'],
            eid
        )
        cursor.execute(query, values)
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Employee updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@crud_blueprint.route('/employees/<int:eid>', methods=['DELETE'])
def delete_employee(eid):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM EMPLOYEE WHERE Eid = %s", (eid,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Employee deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@crud_blueprint.route('/applications/evaluate', methods=['POST'])
def run_evaluation():
    result = evaluate_applications()
    return result

@crud_blueprint.route('/customers', methods=['GET'])
def get_all_customers():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM CUSTOMER")
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@crud_blueprint.route('/customers', methods=['POST'])
def create_customer():
    data = request.json
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO CUSTOMER (Cid, Pref_eid) VALUES (%s, %s)",
            (data['Cid'], data.get('Pref_eid'))
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Customer created successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@crud_blueprint.route('/customers/<int:cid>', methods=['PUT'])
def update_customer(cid):
    data = request.json
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE CUSTOMER SET Pref_eid = %s WHERE Cid = %s",
            (data.get('Pref_eid'), cid)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Customer updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@crud_blueprint.route('/customers/<int:cid>', methods=['DELETE'])
def delete_customer(cid):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM CUSTOMER WHERE Cid = %s", (cid,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Customer deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@crud_blueprint.route('/potential_employees', methods=['GET'])
def get_all_potential_employees():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM POTENTIAL_EMPLOYEE")
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@crud_blueprint.route('/potential_employees', methods=['POST'])
def create_potential_employee():
    data = request.json
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO POTENTIAL_EMPLOYEE (Peid) VALUES (%s)",
            (data['Peid'],)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Potential employee added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@crud_blueprint.route('/potential_employees/<int:peid>', methods=['DELETE'])
def delete_potential_employee(peid):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM POTENTIAL_EMPLOYEE WHERE Peid = %s", (peid,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Potential employee deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@crud_blueprint.route('/departments', methods=['GET'])
def get_departments():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM DEPARTMENT")
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@crud_blueprint.route('/departments', methods=['POST'])
def create_department():
    data = request.json
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO DEPARTMENT (Dname) VALUES (%s)", (data['Dname'],))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Department added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@crud_blueprint.route('/departments/<int:dept_id>', methods=['PUT'])
def update_department(dept_id):
    data = request.json
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE DEPARTMENT SET Dname = %s WHERE Dept_id = %s", (data['Dname'], dept_id))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Department updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@crud_blueprint.route('/departments/<int:dept_id>', methods=['DELETE'])
def delete_department(dept_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM DEPARTMENT WHERE Dept_id = %s", (dept_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Department deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@crud_blueprint.route('/jobs', methods=['GET'])
def get_jobs():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM JOB_POSITION")
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@crud_blueprint.route('/jobs', methods=['POST'])
def create_job():
    data = request.json
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO JOB_POSITION (Jdescription, Posted_date, Dept_ID) VALUES (%s, %s, %s)",
            (data['Jdescription'], data['Posted_date'], data['Dept_ID'])
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Job created successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@crud_blueprint.route('/jobs/<int:jpid>', methods=['PUT'])
def update_job(jpid):
    data = request.json
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE JOB_POSITION SET Jdescription = %s, Posted_date = %s, Dept_ID = %s WHERE Jpid = %s",
            (data['Jdescription'], data['Posted_date'], data['Dept_ID'], jpid)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Job updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@crud_blueprint.route('/jobs/<int:jpid>', methods=['DELETE'])
def delete_job(jpid):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM JOB_POSITION WHERE Jpid = %s", (jpid,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Job deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ─── VENDOR CRUD ────────────────────────────────────────────────────────────────

@crud_blueprint.route('/vendors', methods=['GET'])
def get_vendors():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM VENDOR")
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@crud_blueprint.route('/vendors', methods=['POST'])
def create_vendor():
    data = request.json
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO VENDOR (Vname) VALUES (%s)", (data['Vname'],))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Vendor added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@crud_blueprint.route('/vendors/<int:vendor_id>', methods=['PUT'])
def update_vendor(vendor_id):
    data = request.json
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE VENDOR SET Vname = %s WHERE Vendor_id = %s", (data['Vname'], vendor_id))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Vendor updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@crud_blueprint.route('/vendors/<int:vendor_id>', methods=['DELETE'])
def delete_vendor(vendor_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM VENDOR WHERE Vendor_id = %s", (vendor_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Vendor deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ─── PART CRUD ──────────────────────────────────────────────────────────────────

@crud_blueprint.route('/parts', methods=['GET'])
def get_parts():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM PART")
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@crud_blueprint.route('/parts', methods=['POST'])
def create_part():
    data = request.json
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO PART (Pname, Ptype, Weight, Price) VALUES (%s, %s, %s, %s)",
            (data['Pname'], data['Ptype'], data['Weight'], data['Price'])
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Part added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@crud_blueprint.route('/parts/<int:part_id>', methods=['PUT'])
def update_part(part_id):
    data = request.json
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE PART SET Pname = %s, Ptype = %s, Weight = %s, Price = %s WHERE Part_id = %s",
            (data['Pname'], data['Ptype'], data['Weight'], data['Price'], part_id)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Part updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@crud_blueprint.route('/parts/<int:part_id>', methods=['DELETE'])
def delete_part(part_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM PART WHERE Part_id = %s", (part_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Part deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@crud_blueprint.route('/salaries', methods=['GET'])
def get_salaries():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM SALARY")
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@crud_blueprint.route('/salaries', methods=['POST'])
def create_salary():
    data = request.json
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO SALARY (Eid, Trans_num, Pay_date, Amount)
            VALUES (%s, %s, %s, %s)
        """, (data['Eid'], data['Trans_num'], data['Pay_date'], data['Amount']))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Salary added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@crud_blueprint.route('/salaries/<int:eid>/<int:trans_num>', methods=['PUT'])
def update_salary(eid, trans_num):
    data = request.json
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE SALARY
            SET Pay_date = %s, Amount = %s
            WHERE Eid = %s AND Trans_num = %s
        """, (data['Pay_date'], data['Amount'], eid, trans_num))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Salary updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@crud_blueprint.route('/salaries/<int:eid>/<int:trans_num>', methods=['DELETE'])
def delete_salary(eid, trans_num):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM SALARY WHERE Eid = %s AND Trans_num = %s", (eid, trans_num))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Salary deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@crud_blueprint.route('/phone_numbers', methods=['GET'])
def get_phone_numbers():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM PHONE_NUMBER")
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@crud_blueprint.route('/phone_numbers', methods=['POST'])
def add_phone_number():
    data = request.json
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO PHONE_NUMBER (Person_id, Phone_num)
            VALUES (%s, %s)
        """, (data['Person_id'], data['Phone_num']))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Phone number added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@crud_blueprint.route('/phone_numbers/<int:person_id>/<string:phone_num>', methods=['DELETE'])
def delete_phone_number(person_id, phone_num):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM PHONE_NUMBER WHERE Person_id = %s AND Phone_num = %s", (person_id, phone_num))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Phone number deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@crud_blueprint.route('/work_assignments', methods=['GET'])
def get_work_assignments():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM WORK_ASSIGNMENT")
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@crud_blueprint.route('/work_assignments', methods=['POST'])
def create_work_assignment():
    data = request.json
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO WORK_ASSIGNMENT (Emp_id, Dept_id, Start_date, End_date)
            VALUES (%s, %s, %s, %s)
        """, (data['Emp_id'], data['Dept_id'], data['Start_date'], data.get('End_date')))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Work assignment added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@crud_blueprint.route('/work_assignments/<int:emp_id>/<int:dept_id>/<string:start_date>', methods=['PUT'])
def update_work_assignment(emp_id, dept_id, start_date):
    data = request.json
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE WORK_ASSIGNMENT
            SET End_date = %s
            WHERE Emp_id = %s AND Dept_id = %s AND Start_date = %s
        """, (data.get('End_date'), emp_id, dept_id, start_date))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Work assignment updated'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@crud_blueprint.route('/work_assignments/<int:emp_id>/<int:dept_id>/<string:start_date>', methods=['DELETE'])
def delete_work_assignment(emp_id, dept_id, start_date):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM WORK_ASSIGNMENT WHERE Emp_id = %s AND Dept_id = %s AND Start_date = %s",
                       (emp_id, dept_id, start_date))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Work assignment deleted'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
@crud_blueprint.route('/works_at', methods=['GET'])
def get_works_at():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM WORKS_AT")
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@crud_blueprint.route('/works_at', methods=['POST'])
def create_works_at():
    data = request.json
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO WORKS_AT (Eid, Site_id, Start_date, End_date)
            VALUES (%s, %s, %s, %s)
        """, (data['Eid'], data['Site_id'], data['Start_date'], data.get('End_date')))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Works_at record added'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@crud_blueprint.route('/works_at/<int:eid>/<int:site_id>/<string:start_date>', methods=['PUT'])
def update_works_at(eid, site_id, start_date):
    data = request.json
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE WORKS_AT SET End_date = %s
            WHERE Eid = %s AND Site_id = %s AND Start_date = %s
        """, (data.get('End_date'), eid, site_id, start_date))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Works_at record updated'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@crud_blueprint.route('/works_at/<int:eid>/<int:site_id>/<string:start_date>', methods=['DELETE'])
def delete_works_at(eid, site_id, start_date):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM WORKS_AT WHERE Eid = %s AND Site_id = %s AND Start_date = %s",
                       (eid, site_id, start_date))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Works_at record deleted'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@crud_blueprint.route('/products', methods=['GET'])
def get_products():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM PRODUCT")
        products = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(products)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@crud_blueprint.route('/products', methods=['POST'])
def create_product():
    data = request.json
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO PRODUCT (Ptype, Weight, Size, List_price, Style)
            VALUES (%s, %s, %s, %s, %s)
        """, (data['Ptype'], data['Weight'], data['Size'], data['List_price'], data['Style']))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Product added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@crud_blueprint.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.json
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE PRODUCT SET
                Ptype = %s,
                Weight = %s,
                Size = %s,
                List_price = %s,
                Style = %s
            WHERE Product_id = %s
        """, (data['Ptype'], data['Weight'], data['Size'], data['List_price'], data['Style'], product_id))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Product updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@crud_blueprint.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM PRODUCT WHERE Product_id = %s", (product_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Product deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@crud_blueprint.route('/marketing_sites', methods=['GET'])
def get_sites():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM MARKETING_SITE")
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@crud_blueprint.route('/marketing_sites', methods=['POST'])
def create_site():
    data = request.json
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO MARKETING_SITE (Sname, Slocation)
            VALUES (%s, %s)
        """, (data['Sname'], data['Slocation']))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Site added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@crud_blueprint.route('/marketing_sites/<int:site_id>', methods=['PUT'])
def update_site(site_id):
    data = request.json
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE MARKETING_SITE SET Sname = %s, Slocation = %s
            WHERE Site_id = %s
        """, (data['Sname'], data['Slocation'], site_id))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Site updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@crud_blueprint.route('/marketing_sites/<int:site_id>', methods=['DELETE'])
def delete_site(site_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM MARKETING_SITE WHERE Site_id = %s", (site_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Site deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@crud_blueprint.route('/sales', methods=['GET'])
def get_sales():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM SALE")
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@crud_blueprint.route('/sales', methods=['POST'])
def create_sale():
    data = request.json
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO SALE (Sman_id, Cust_id, Site_id, Sale_time)
            VALUES (%s, %s, %s, %s)
        """, (data['Sman_id'], data['Cust_id'], data['Site_id'], data['Sale_time']))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Sale created'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@crud_blueprint.route('/sales/<int:sale_id>', methods=['PUT'])
def update_sale(sale_id):
    data = request.json
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE SALE
            SET Sman_id = %s, Cust_id = %s, Site_id = %s, Sale_time = %s
            WHERE Sale_id = %s
        """, (data['Sman_id'], data['Cust_id'], data['Site_id'], data['Sale_time'], sale_id))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Sale updated'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@crud_blueprint.route('/sales/<int:sale_id>', methods=['DELETE'])
def delete_sale(sale_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM SALE WHERE Sale_id = %s", (sale_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Sale deleted'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
@crud_blueprint.route('/sale_details', methods=['GET'])
def get_sale_details():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM SALE_DETAIL")
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@crud_blueprint.route('/sale_details', methods=['POST'])
def create_sale_detail():
    data = request.json
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO SALE_DETAIL (Sale_id, Product_id, Quantity, Unit_price)
            VALUES (%s, %s, %s, %s)
        """, (data['Sale_id'], data['Product_id'], data['Quantity'], data['Unit_price']))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Sale detail added'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@crud_blueprint.route('/sale_details/<int:sale_id>/<int:product_id>', methods=['PUT'])
def update_sale_detail(sale_id, product_id):
    data = request.json
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE SALE_DETAIL
            SET Quantity = %s, Unit_price = %s
            WHERE Sale_id = %s AND Product_id = %s
        """, (data['Quantity'], data['Unit_price'], sale_id, product_id))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Sale detail updated'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@crud_blueprint.route('/sale_details/<int:sale_id>/<int:product_id>', methods=['DELETE'])
def delete_sale_detail(sale_id, product_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM SALE_DETAIL WHERE Sale_id = %s AND Product_id = %s", (sale_id, product_id))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Sale detail deleted'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
@crud_blueprint.route('/product_parts', methods=['GET'])
def get_product_parts():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM PRODUCT_PART")
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@crud_blueprint.route('/product_parts', methods=['POST'])
def create_product_part():
    data = request.json
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO PRODUCT_PART (Product_id, Part_id, Quantity)
            VALUES (%s, %s, %s)
        """, (data['Product_id'], data['Part_id'], data['Quantity']))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Product part added'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@crud_blueprint.route('/product_parts/<int:product_id>/<int:part_id>', methods=['PUT'])
def update_product_part(product_id, part_id):
    data = request.json
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE PRODUCT_PART SET Quantity = %s
            WHERE Product_id = %s AND Part_id = %s
        """, (data['Quantity'], product_id, part_id))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Product part updated'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@crud_blueprint.route('/product_parts/<int:product_id>/<int:part_id>', methods=['DELETE'])
def delete_product_part(product_id, part_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM PRODUCT_PART WHERE Product_id = %s AND Part_id = %s", (product_id, part_id))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Product part deleted'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
@crud_blueprint.route('/vendor_parts', methods=['GET'])
def get_vendor_parts():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM VENDOR_PART")
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@crud_blueprint.route('/vendor_parts', methods=['POST'])
def create_vendor_part():
    data = request.json
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO VENDOR_PART (Part_id, Vendor_id, Price)
            VALUES (%s, %s, %s)
        """, (data['Part_id'], data['Vendor_id'], data['Price']))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Vendor part added'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@crud_blueprint.route('/vendor_parts/<int:part_id>/<int:vendor_id>', methods=['PUT'])
def update_vendor_part(part_id, vendor_id):
    data = request.json
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE VENDOR_PART SET Price = %s
            WHERE Part_id = %s AND Vendor_id = %s
        """, (data['Price'], part_id, vendor_id))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Vendor part updated'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@crud_blueprint.route('/vendor_parts/<int:part_id>/<int:vendor_id>', methods=['DELETE'])
def delete_vendor_part(part_id, vendor_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM VENDOR_PART WHERE Part_id = %s AND Vendor_id = %s", (part_id, vendor_id))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Vendor part deleted'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# --- APPLICATION ROUTES ---
@crud_blueprint.route('/applications', methods=['GET'])
def get_applications():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM APPLICATION")
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@crud_blueprint.route('/applications', methods=['POST'])
def create_application():
    data = request.json
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO APPLICATION (Applicant_id, Jpid, App_date, Is_selected)
            VALUES (%s, %s, %s, %s)
        """, (data['Applicant_id'], data['Jpid'], data['App_date'], data['Is_selected']))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Application added'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@crud_blueprint.route('/applications/<int:app_id>', methods=['PUT'])
def update_application(app_id):
    data = request.json
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE APPLICATION
            SET Applicant_id = %s, Jpid = %s, App_date = %s, Is_selected = %s
            WHERE App_id = %s
        """, (data['Applicant_id'], data['Jpid'], data['App_date'], data['Is_selected'], app_id))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Application updated'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@crud_blueprint.route('/applications/<int:app_id>', methods=['DELETE'])
def delete_application(app_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM APPLICATION WHERE App_id = %s", (app_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Application deleted'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# --- INTERVIEW ROUTES ---
@crud_blueprint.route('/interviews', methods=['GET'])
def get_interviews():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM INTERVIEW")
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@crud_blueprint.route('/interviews', methods=['POST'])
def create_interview():
    data = request.json
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO INTERVIEW (App_id, Interviewer_id, Interview_date, Grade, Round_num)
            VALUES (%s, %s, %s, %s, %s)
        """, (data['App_id'], data['Interviewer_id'], data['Interview_date'], data['Grade'], data['Round_num']))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Interview added'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@crud_blueprint.route('/interviews/<int:int_id>', methods=['PUT'])
def update_interview(int_id):
    data = request.json
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE INTERVIEW
            SET App_id = %s, Interviewer_id = %s, Interview_date = %s, Grade = %s, Round_num = %s
            WHERE Interview_id = %s
        """, (data['App_id'], data['Interviewer_id'], data['Interview_date'], data['Grade'], data['Round_num'], int_id))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Interview updated'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@crud_blueprint.route('/interviews/<int:int_id>', methods=['DELETE'])
def delete_interview(int_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM INTERVIEW WHERE Interview_id = %s", (int_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Interview deleted'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
