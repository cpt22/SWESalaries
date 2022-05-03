import sqlite3
import re

conn = sqlite3.connect('data.db')
c = conn.cursor()


def load_techs():
    c.row_factory = sqlite3.Row
    c.execute(''' SELECT * FROM techs ''')
    techs = {}
    for record in c.fetchall():
        techs[record['id']] = record['regex']
    return techs


def save_data(data, source=''):
    if data['position']:
        position_query = "INSERT INTO positions (name, salary, company, location, source) VALUES (?, ?, ?, ?, ?) RETURNING id"
        c.execute(position_query, (data['position'], data['salary'], data['company'], data['location'], source))
        new_id = c.fetchone()[0]
        linkers = []
        tech_query = "INSERT OR IGNORE INTO positions_techs (position_id, tech_id) VALUES (?, ?)"
        for tech in data['technologies']:
            linkers.append((new_id, tech))
        c.executemany(tech_query, linkers)
        conn.commit()
    else:
        print("Failed to save entry")


# Helper function to extract programming languages from the job description text
def extract_technologies(job_description):
    temp = set()
    for tech, reg in technologies.items():
        if re.search(reg, job_description, flags=re.IGNORECASE) is not None:
            temp.add(tech)
    return list(temp)


technologies = load_techs()

