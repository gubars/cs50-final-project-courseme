CREATE TABLE users (
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

CREATE TABLE instructors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

CREATE TABLE courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    code TEXT NOT NULL UNIQUE,
    instructor_id INTEGER NOT NULL,
    year INTEGER NOT NULL,
    is_fall BOOLEAN NOT NULL DEFAULT 0,
    is_spring BOOLEAN NOT NULL DEFAULT 0,
    days_of_week TEXT,
    start_time TEXT,
    end_time TEXT,
    location TEXT,
    qguide TEXT,
    description TEXT,
    concentration_id INTEGER NOT NULL,
    FOREIGN KEY (instructor_id) REFERENCES instructors(id),
    FOREIGN KEY (concentration_id) REFERENCES concentrations(id)
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
    is_double BOOLEAN NOT NULL DEFAULT 0,
    is_joint BOOLEAN NOT NULL DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (concentration1_id) REFERENCES concentrations(id),
    FOREIGN KEY (concentration2_id) REFERENCES concentrations(id),
    FOREIGN KEY (secondary_id) REFERENCES secondaries(id)
)