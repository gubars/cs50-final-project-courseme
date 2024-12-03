DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS profile;
DROP TABLE IF EXISTS concentration;
DROP TABLE IF EXISTS secondary;
DROP TABLE IF EXISTS course;

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE profile (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    concentration1_id INTEGER NOT NULL,
    concentration2_id INTEGER,
    secondary_id INTEGER,
    double BOOLEAN NOT NULL,
    joint BOOLEAN NOT NULL,
    course1_id INTEGER NOT NULL,
    course2_id INTEGER NOT NULL,
    course3_id INTEGER NOT NULL,
    course4_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user (id),
    FOREIGN KEY (concentration1_id) REFERENCES concentration (id),
    FOREIGN KEY (concentration2_id) REFERENCES concentration (id),
    FOREIGN KEY (secondary_id) REFERENCES secondary (id),
    FOREIGN KEY (course1_id) REFERENCES course (id),
    FOREIGN KEY (course2_id) REFERENCES course (id),
    FOREIGN KEY (course3_id) REFERENCES course (id),
    FOREIGN KEY (course4_id) REFERENCES course (id)
)

CREATE TABLE concentration (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
)

CREATE TABLE secondary (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
)

CREATE TABLE instructors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
)

CREATE TABLE course (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    code TEXT NOT NULL,
    instructor TEXT NOT NULL,
    year INTEGER NOT NULL,
    fall BOOLEAN NOT NULL,
    spring BOOLEAN NOT NULL,
)