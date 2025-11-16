# app/load_data.py
import os
import psycopg2

def load_data_to_sql(data):  # Nhận trực tiếp List[Dict]
    #Connect
    conn = psycopg2.connect(
        host="postgres",
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    )
    cur = conn.cursor()

    insert_sql = """
        INSERT INTO topcv(
            title,
            job_url,
            company,
            company_url,
            salary_million,
            experience,
            deadline,
            tags,
            detail_address,
            working_times,
            job_description,
            requirements,
            benefits,
            city,
            district
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (job_url) DO NOTHING
    """

    rows = []
    for item in data:
        # Xử lý deadline
        deadline_value = item.get("Deadline") or item.get("deadline")
        if deadline_value is None or deadline_value == "":
            deadline_value = None

        rows.append((
            item.get("Title") or item.get("title"),
            item.get("Job URL") or item.get("job_url"),
            item.get("Company") or item.get("company"),
            item.get("Company URL") or item.get("company_url"),
            item.get("Salary_Avg"),  # Lấy trực tiếp từ transform
            item.get("Experience") or item.get("experience"),
            deadline_value,
            item.get("Tags") or item.get("tags"),
            item.get("Detail Address") or item.get("detail_address"),
            item.get("Working Times") or item.get("working_times"),
            item.get("Job_Description") or item.get("job_description"),
            item.get("Requirements") or item.get("requirements"),
            item.get("Benefits") or item.get("benefits"),
            item.get("City") or item.get("city"),
            item.get("District") or item.get("district"),
        ))

    cur.executemany(insert_sql, rows)
    conn.commit()
    cur.close()
    conn.close()