DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS concentrations;
DROP TABLE IF EXISTS secondaries;
DROP TABLE IF EXISTS instructors;
DROP TABLE IF EXISTS courses;
DROP TABLE IF EXISTS meeting_patterns;
DROP TABLE IF EXISTS profiles;
DROP TABLE IF EXISTS user_courses;
DROP TABLE IF EXISTS course_gened_area;
DROP TABLE IF EXISTS course_divisional_dist;

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE concentrations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

CREATE TABLE secondaries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

-- Table for instructors
CREATE TABLE instructors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT
);

-- Table for courses
CREATE TABLE courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    subject TEXT,
    subjectDescription TEXT,
    catalogNumber TEXT,
    level TEXT,
    academicGroup TEXT,
    semester TEXT,
    academicYear INTEGER,
    classSection TEXT,
    component TEXT,
    description TEXT,
    instructor_id INTEGER,
    FOREIGN KEY (instructor_id) REFERENCES instructors(id)
);

-- Table for meeting patterns
CREATE TABLE meeting_patterns (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_id INTEGER NOT NULL,
    startTime TEXT,
    endTime TEXT,
    startDate TEXT,
    endDate TEXT,
    meetsOnMonday BOOLEAN NOT NULL DEFAULT 0,
    meetsOnTuesday BOOLEAN NOT NULL DEFAULT 0,
    meetsOnWednesday BOOLEAN NOT NULL DEFAULT 0,
    meetsOnThursday BOOLEAN NOT NULL DEFAULT 0,
    meetsOnFriday BOOLEAN NOT NULL DEFAULT 0,
    meetsOnSaturday BOOLEAN NOT NULL DEFAULT 0,
    meetsOnSunday BOOLEAN NOT NULL DEFAULT 0,
    FOREIGN KEY (course_id) REFERENCES courses(id)
);


CREATE TABLE profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT,
    concentration1_id INTEGER,
    concentration2_id INTEGER,
    secondary_id INTEGER,
    year INTEGER NOT NULL,
    current_semester TEXT NOT NULL,
    num_courses_want INTEGER NOT NULL,
    want_gened BOOLEAN NOT NULL DEFAULT 0,
    want_grad BOOLEAN NOT NULL DEFAULT 0,
    want_9am BOOLEAN NOT NULL DEFAULT 0,
    want_conc_req BOOLEAN NOT NULL DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (concentration1_id) REFERENCES concentrations(id),
    FOREIGN KEY (concentration2_id) REFERENCES concentrations(id),
    FOREIGN KEY (secondary_id) REFERENCES secondaries(id)
);

CREATE TABLE user_courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    semester TEXT NOT NULL,
    year INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (course_id) REFERENCES courses(id)
);

CREATE TABLE course_gened_area (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_id INTEGER NOT NULL,
    gened_area TEXT NOT NULL,
    FOREIGN KEY (course_id) REFERENCES courses(id)
);

CREATE TABLE course_divisional_dist (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_id INTEGER NOT NULL,
    divisional_dist TEXT NOT NULL,
    FOREIGN KEY (course_id) REFERENCES courses(id)
);