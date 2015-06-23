CREATE TABLE status (
    id INTEGER NOT NULL,
    directory VARCHAR(50) NOT NULL,
    name VARCHAR(20) NOT NULL,

    PRIMARY KEY(id)
)

CREATE TABLE category (
    id INTEGER NOT NULL,
    name VARCHAR(20) NOT NULL,

    PRIMARY KEY(id)
)

CREATE TABLE language (
    id INTEGER NOT NULL,
    name VARCHAR(20) NOT NULL,
    extension VARCHAR(8) NOT NULL,

    PRIMARY KEY(id)
)

CREATE TABLE problem (
    id INTEGER NOT NULL,
    name VARCHAR(20) NOT NULL,
    category_id INTEGER,

    PRIMARY KEY(id),
    FOREIGN KEY(category_id) REFERENCES category(id)
)

CREATE TABLE problem_attempt (
    problem_id INTEGER NOT NULL,
    language_id INTEGER NOT NULL,
    status_id INTEGER NOT NULL,
    attempt_no INTEGER NOT NULL,

    PRIMARY KEY(problem_id, language_id, status_id, attempt_no),
    FOREIGN KEY(problem_id) REFERENCES problem(id),
    FOREIGN KEY(language_id) REFERENCES language(id),
    FOREIGN KEY(status_id) REFERENCES status(id)
)

CREATE TABLE settings (
    default_language_id INTEGER NOT NULL,
    current_problem_id INTEGER NOT NULL,

    FOREIGN KEY(default_language_id) REFERENCES language(id),
    FOREIGN KEY(current_problem_id) REFERENCES problem(id)
)
