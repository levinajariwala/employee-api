CREATE TABLE IF NOT EXISTS employees (
    id      SERIAL PRIMARY KEY,
    name    VARCHAR(100) NOT NULL,
    dept    VARCHAR(50)  NOT NULL,
    salary  NUMERIC(10,2)
);

INSERT INTO employees (name, dept, salary) VALUES
('Priya Sharma', 'IT',      55000),
('James Wilson', 'HR',      42000),
('Emma Brown',   'Finance', 48000);