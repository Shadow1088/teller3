-- Users table
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    reputation_score REAL NOT NULL DEFAULT 0,
    status TEXT NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'suspended', 'banned')),
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX idx_users_username ON users(username);

-- Questions table
CREATE TABLE questions (
    question_id INTEGER PRIMARY KEY AUTOINCREMENT,
    question_text TEXT NOT NULL,
    language TEXT NOT NULL,
    intent TEXT NOT NULL CHECK (intent IN ('when', 'how', 'why', 'what', 'should', 'where', 'who')),
    tags TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

-- Only keep the compound index (covers both individual searches)
CREATE INDEX idx_questions_language_intent ON questions(language, intent);

-- Answers table
CREATE TABLE answers (
    answer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    question_id INTEGER NOT NULL,
    answer_text TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    confidence_score REAL NOT NULL DEFAULT 0,
    is_hidden INTEGER NOT NULL DEFAULT 0 CHECK (is_hidden IN (0, 1)),
    is_best INTEGER NOT NULL DEFAULT 0 CHECK (is_best IN (0, 1)),
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (question_id) REFERENCES questions(question_id) ON DELETE RESTRICT,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE RESTRICT
);

CREATE INDEX idx_answers_question_id ON answers(question_id);
CREATE INDEX idx_answers_user_id ON answers(user_id);
CREATE UNIQUE INDEX idx_one_answer_per_user_per_question ON answers(question_id, user_id);
CREATE UNIQUE INDEX idx_one_best_answer_per_question ON answers(question_id) WHERE is_best = 1;

-- Answer votes table
CREATE TABLE answer_votes (
    vote_id INTEGER PRIMARY KEY AUTOINCREMENT,
    answer_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    vote_type TEXT NOT NULL CHECK (vote_type IN ('upvote', 'downvote')),
    weight REAL NOT NULL DEFAULT 1.0,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (answer_id) REFERENCES answers(answer_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE RESTRICT,
    UNIQUE(answer_id, user_id)
);

CREATE INDEX idx_answer_votes_answer_id ON answer_votes(answer_id);
CREATE INDEX idx_answer_votes_user_id ON answer_votes(user_id);

-- Trigger to prevent users from voting on their own answers
CREATE TRIGGER prevent_self_vote
BEFORE INSERT ON answer_votes
FOR EACH ROW
WHEN EXISTS (
    SELECT 1 FROM answers 
    WHERE answer_id = NEW.answer_id 
    AND user_id = NEW.user_id
)
BEGIN
    SELECT RAISE(ABORT, 'Users cannot vote on their own answers');
END;

-- Answer notes table
CREATE TABLE answer_notes (
    note_id INTEGER PRIMARY KEY AUTOINCREMENT,
    answer_id INTEGER NOT NULL,
    note_text TEXT NOT NULL,
    created_by INTEGER,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (answer_id) REFERENCES answers(answer_id) ON DELETE CASCADE,
    FOREIGN KEY (created_by) REFERENCES users(user_id) ON DELETE SET NULL
);

CREATE INDEX idx_answer_notes_answer_id ON answer_notes(answer_id);

-- View for vote aggregation
CREATE VIEW answer_vote_summary AS
SELECT 
    answer_id,
    SUM(CASE WHEN vote_type = 'upvote' THEN 1 ELSE 0 END) as upvote_count,
    SUM(CASE WHEN vote_type = 'downvote' THEN 1 ELSE 0 END) as downvote_count,
    SUM(CASE WHEN vote_type = 'upvote' THEN weight ELSE 0 END) as upvote_weight,
    SUM(CASE WHEN vote_type = 'downvote' THEN weight ELSE 0 END) as downvote_weight,
    COUNT(*) as total_votes
FROM answer_votes
GROUP BY answer_id;