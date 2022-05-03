from common import *

def main():
    # Create technologies table
    c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='techs' ''')
    if c.fetchone()[0] == 0:
        c.execute('''CREATE TABLE techs(
                id varchar NOT NULL PRIMARY KEY,
                regex varchar NOT NULL,
                type varchar NOT NULL DEFAULT 'language'
            )
        ''')
        c.execute('''CREATE UNIQUE INDEX techs_unique_name ON techs(id)''')
        c.execute('''CREATE UNIQUE INDEX techs_unique_regex ON techs(regex)''')
    else:
        print("Table techs exists")

    # Create positions table
    c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='positions' ''')
    if c.fetchone()[0] == 0:
        c.execute('''CREATE TABLE positions(
                id integer NOT NULL PRIMARY KEY,
                name varchar NOT NULL,
                salary real NULL,
                company varchar,
                location varchar,
                source varchar NOT NULL
            )
        ''')
    else:
        print("Table positions exists")

    # Create linker
    c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='positions_techs' ''')
    if c.fetchone()[0] == 0:
        c.execute('''CREATE TABLE positions_techs(
                tech_id varchar,
                position_id integer,
                PRIMARY KEY (tech_id, position_id),
                FOREIGN KEY (tech_id) REFERENCES techs(id) ON DELETE CASCADE,
                FOREIGN KEY (position_id) REFERENCES positions(id) ON DELETE CASCADE
            )
        ''')
    else:
        print("Table positions_techs exists")

    # Add Programming Languages
    c.execute('''INSERT OR IGNORE INTO techs (id, regex) VALUES
    ('Javascript', 'javascript'),
    ('Java', '[ ,]java[ \.,]'),
    ('C', '[ ,]c[ \.,]'),
    ('C++', 'c\+\+'),
    ('Kotlin', 'kotlin'),
    ('Swift', 'swift'),
    ('Ruby', 'ruby'),
    ('Python', 'python3?'),
    ('SQL', 'sql'),
    ('R', '[ ,]r[ \.,]'),
    ('Perl', 'perl'),
    ('C#', 'c#'),
    ('Lua', 'lua'),
    ('Rust', 'rust'),
    ('PHP', 'php'),
    ('HTML', 'html'),
    ('CSS', 'css'),
    ('XML', 'xml')
    ''')

    c.execute('''INSERT OR IGNORE INTO techs (id, regex, type) VALUES
    ('React', 'react', 'framework'),
    ('Vue', 'vue', 'framework'),
    ('Express', 'express', 'framework'),
    ('Spring', 'spring', 'framework'),
    ('Django', 'django', 'framework'),
    ('Flask', 'flask', 'framework'),
    ('Angular', 'angular', 'framework'),
    ('Ruby on Rails', '(ruby on rails)|(rails)', 'framework'),
    ('ASP.NET Core', '(asp\.net core)|(asp\.net)', 'framework'),
    ('.NET', '[ ,]\.net[ ,\.]', 'framework'),
    ('jQuery', ' jquery', 'framework'),
    ('Laravel', 'laravel', 'framework')
    ''')

    conn.commit()


if __name__ == "__main__":
    main()

