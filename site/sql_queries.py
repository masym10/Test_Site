import sqlite3

conn = sqlite3.connect("Quiz.sqlite")

cursor = conn.cursor()

cursor.execute('DROP TABLE IF EXISTS quiz')
cursor.execute('DROP TABLE IF EXISTS question')
cursor.execute('DROP TABLE IF EXISTS quiz_content')
conn.commit()

cursor.execute('''
CREATE TABLE IF NOT EXISTS quiz (id INTEGER PRIMARY KEY, name VARCHAR)
''')

conn.commit()
cursor.execute('''
CREATE TABLE IF NOT EXISTS question (id INTEGER PRIMARY KEY, question VARCHAR, answer VARCHAR, wrong_answer1 VARCHAR, wrong_answer2 VARCHAR, wrong_answer3 VARCHAR)
''')

conn.commit()
cursor.execute('''
CREATE TABLE IF NOT EXISTS quiz_content (
               id INTEGER PRIMARY KEY, 
               quiz_id INTEGER, 
               question_id INTEGER,
               FOREIGN KEY (quiz_id) REFERENCES quiz (id),
               FOREIGN KEY (question_id) REFERENCES question (id)
               )
''')

conn.commit()

questions = [
    ("Який переклад слова blue правельний?", 'синій', 'блуе', 'щось на англійській', 'незадоволення'),
    ("Який переклад слова magazine правельний?", 'журнал', 'магазин', 'ринок', 'мапа'),
    ("За якийсь час Земля робить один оберт навколо своєї осі?", "12 місяців", "12 годин", "24 години", "30 днів"),
    ("Яків в космосу бувають діри?", "чорні", "білі", "блакитні", "червоні")
]

cursor.executemany('''INSERT INTO question (question, answer, wrong_answer1,
 wrong_answer2, wrong_answer3) 
 VALUES (?, ?, ?, ?, ?)''', questions)

conn.commit()

cursor.execute('''
CREATE TABLE IF NOT EXISTS quiz(
               id INTEGER PRIMARY KEY,
               id quiz INTEGER,
               name quiz VARCHAR
)
               ''')

quziz = [
    ('English words translate',),
    ('Mystery_Galaxy',)
]

cursor.executemany('''INSERT INTO quiz (name) VALUES (?) ''', quziz)
conn.commit()

cursor.execute('''INSERT INTO quiz_content (quiz_id, question_id) VALUES (?, ?) ''', [1, 1])
conn.commit()

def get_question(quiz_id, question_id):
    conn = sqlite3.connect('Quiz.sqlite')
    cursor = conn.cursor()

    cursor.execute('''SELECT quiz_content.id, question.question, question.answer, question.wrong_answer1, 
                   question.wrong_answer2, question.wrong_answer3
                   FROM question, quiz_content 
                   WHERE quiz_content.question_id == question_id
                   AND question.id == ?
                   AND quiz_content.quiz_id = ?''', [question_id, quiz_id])
    
    data = cursor.fetchall()
    
    return data

def get_quises():
    query = 'SELECT * FROM quiz ORDER BY id'
    conn = sqlite3.connect('Quiz.sqlite')
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()

    return result

def open():
    global conn, cursor
    conn = sqlite3.connect('Quiz.sqlite')
    cursor = conn.cursor()
 
def close():
    cursor.close()
    conn.close()

def check_answer(question_id, answer):
    query = sqlite3.connect('Quiz.sqlite')
    cursor = conn.cursor()

    cursor.execute('''
                   Select question.answer FROM quiz_content, question WHERE quiz_content.id = ?
                   AND quiz_content.question_id = question.id
                   ''')
    
    open()
    cursor.execute(query, str(question_id))
    result = cursor.fetchone()
    close()
    
    if result is not None:
        return False
    else:
        if result[0] == answer:
            return True
        else:
            return False