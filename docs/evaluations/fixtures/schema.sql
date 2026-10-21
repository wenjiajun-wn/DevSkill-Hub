CREATE TABLE repositories (
    id INTEGER PRIMARY KEY,
    full_name VARCHAR(200) NOT NULL UNIQUE
);

CREATE TABLE skill_entries (
    id INTEGER PRIMARY KEY,
    repository_id INTEGER NOT NULL,
    name VARCHAR(100) NOT NULL,
    FOREIGN KEY (repository_id) REFERENCES repositories(id)
);
