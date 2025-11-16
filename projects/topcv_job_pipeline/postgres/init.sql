CREATE TABLE IF NOT EXISTS topcv (
    id               SERIAL PRIMARY KEY,          -- khoá chính tự tăng
    title            TEXT       NOT NULL,        -- Title
    job_url         TEXT        NOT NULL UNIQUE,  -- Job URL
    company          TEXT,                        -- Company
    company_url      TEXT,                        -- Company URL
    salary_million   NUMERIC(10,2),               -- Salary (Triệu VND) - lương trung bình, đơn vị: triệu
    experience       TEXT,                        -- Experience
    deadline         TEXT,                        -- Deadline
    tags             TEXT,                        -- Tags
    detail_address   TEXT,                        -- Detail Address
    working_times    TEXT,                        -- Working Times
    job_description  TEXT,                        -- Job_Description
    requirements     TEXT,                        -- Requirements
    benefits         TEXT,                        -- Benefits
    city             TEXT,                        -- City
    district         TEXT                         -- District
);