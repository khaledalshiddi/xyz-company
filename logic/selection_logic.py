from db.connection import get_connection

def evaluate_applications():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Set all applications to not selected
        cursor.execute("UPDATE APPLICATION SET Is_selected = 0")

        # Update top applicant per job with >=5 passed rounds and avg grade > 70
        cursor.execute("""
            UPDATE APPLICATION A
            JOIN (
                SELECT App_id FROM (
                    SELECT 
                        A.App_id,
                        A.Jpid,
                        AVG(I.Grade) AS avg_grade,
                        COUNT(CASE WHEN I.Grade > 60 THEN 1 END) AS passed_rounds,
                        RANK() OVER (PARTITION BY A.Jpid ORDER BY AVG(I.Grade) DESC) AS job_rank
                    FROM APPLICATION A
                    JOIN INTERVIEW I ON A.App_id = I.App_id
                    GROUP BY A.App_id, A.Jpid
                    HAVING passed_rounds >= 5 AND avg_grade > 70
                ) AS Ranked
                WHERE job_rank = 1
            ) AS Qualified
            ON A.App_id = Qualified.App_id
            SET A.Is_selected = 1;
        """)

        conn.commit()
        cursor.close()
        conn.close()
        return {'message': 'Applications evaluated — one top candidate selected per job.'}

    except Exception as e:
        return {'error': str(e)}
