import sqlite3

connector = sqlite3.connect("db.db")
cursor = connector.cursor()

def run_query(query: str, params: tuple = (), commit=False):
    cursor.execute(query, params)
    if commit:
        cursor.connection.commit()
    return cursor.fetchall()

def insert_q(text:str, language:str, intent:str) -> bool:
    try:
        run_query(f"""
        INSERT INTO
        questions
        (question_text, language, intent)
        VALUES
        (?, ?, ?)
        """, (text, language, intent), commit=True)
        return True
    except: return False

def insert_a(question_id:int, text:str, user_id:int) -> bool:
    try:
        run_query(f"""
        INSERT INTO
        answers
        (question_id, answer_text, user_id)
        VALUES
        (?, ?, ?)
        """, (question_id, text, user_id), commit=True)
        return True
    except: return False

def insert_user(username:str, pswd_hash:str):
    try:
        run_query(f"""
        INSERT INTO
        users
        (username, password_hash)
        VALUES
        (?, ?)
        """, (username, pswd_hash), commit=True)
        return True
    except: return False

def insert_a_vote(answer_id:int, user_id:int, vote_type:str) -> bool:
    try:
        run_query(f"""
        INSERT INTO
        answer_votes
        (answer_id, user_id, vote_type)
        VALUES
        (?, ?, ?)
        """, (answer_id, user_id, vote_type), commit=True)
        return True
    except Exception as e: 
        return False

def insert_a_note(answer_id:int, text:str) -> bool:
    try:
        run_query(f"""
        INSERT INTO
        answer_notes
        (answer_id, note_text)
        VALUES
        (?, ?)
        """, (answer_id, text), commit=True)
        return True
    except Exception as e: 
        return False
    
def getall_usernames() -> list[str]:
    try:
        usernames = [user for (user,) in run_query(f"""
        SELECT
        username
        FROM
        users
        """)]
        return usernames
    except Exception as e: 
        print(e)
        return []
    
def get_hash(username:str) -> str:
    try:
        return run_query(f"""
        SELECT
        password_hash
        FROM
        users
        WHERE username = '{username}'
        """)[0][0]

    except Exception as e: 
        print(e)
        return ""

def get_uid(username:str) -> int:
    return run_query(f"""
        SELECT
        user_id
        FROM
        users
        WHERE username = '{username}'
        """)[0][0]

def random_entry(table:str=""):
    tables = [t for (t,) in list(run_query("SELECT name FROM sqlite_master WHERE type='table';"))]
    if table not in tables:
        raise ValueError("Invalid table name")

    return run_query(f"""    
        SELECT *
        FROM {table}
        WHERE question_id >= (
            SELECT FLOOR(RANDOM() * (MAX(question_id) - MIN(question_id) + 1)) + MIN(question_id)
            FROM {table}
        )
        ORDER BY question_id
        LIMIT 1;
    """)

#def get_q_a(question_id):

#print(insert_a("test", 0, 0))
#print(insert_user("ghhsbl", "1112"))
#print(insert_a("niuiu", 0, 1))
#print(insert_a_vote(2,1,"upvote"))
#print(insert_a_note(1,"togle"))
#print(getall_usernames())
#print(get_hash("user1"))
#print(get_uid("user2"))


def get_answers(question_id: int):
    query = """
    SELECT
        a.answer_id,
        a.answer_text,
        au.username AS author_username,
        COALESCE(v.weighted_upvotes, 0)   AS weighted_upvotes,
        COALESCE(v.weighted_downvotes, 0) AS weighted_downvotes,
        COALESCE(
            v.weighted_upvotes /
            CASE
                WHEN v.weighted_downvotes = 0 THEN 1
                ELSE v.weighted_downvotes
            END,
            0
        ) AS ratio
    FROM answers a

    -- author of the answer
    JOIN users au ON a.user_id = au.user_id

    -- votes aggregation
    LEFT JOIN (
        SELECT
            av.answer_id,

            SUM(
                CASE
                    WHEN av.vote_type = 'upvote'
                    THEN (1 + u.reputation_score * 10)
                    ELSE 0
                END
            ) AS weighted_upvotes,

            SUM(
                CASE
                    WHEN av.vote_type = 'downvote'
                    THEN (1 + u.reputation_score * 10)
                    ELSE 0
                END
            ) AS weighted_downvotes

        FROM answer_votes av
        JOIN users u ON av.user_id = u.user_id
        GROUP BY av.answer_id
    ) v ON a.answer_id = v.answer_id

    WHERE
        a.question_id = ?
        AND a.is_hidden = 0
        AND COALESCE(
            v.weighted_upvotes /
            CASE
                WHEN v.weighted_downvotes = 0 THEN 1
                ELSE v.weighted_downvotes
            END,
            0
        ) >= 0

    ORDER BY
        ratio DESC,
        weighted_upvotes DESC;
    """

    return run_query(query, (question_id,))

def get_q():
    return (run_query("SELECT question_id, question_text, intent FROM questions"))

def get_qid(text:str) -> int:
    return (run_query(f"SELECT question_id FROM questions WHERE question_text = '{text}'"))[0][0]

def get_aid(q_id:int, u_id:int) -> int:
    return (run_query(f"SELECT answer_id FROM answers WHERE question_id = '{q_id}' AND user_id = '{u_id}'"))[0][0]

