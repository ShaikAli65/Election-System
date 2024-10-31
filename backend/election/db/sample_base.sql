CREATE TABLE voters (
    voter_id UUID PRIMARY KEY,                     -- Unique identifier for voter
    user_id VARCHAR(32) NOT NULL UNIQUE,           -- Foreign key to authentication table
    voter_registration_number VARCHAR(100) UNIQUE, -- Unique voter registration number
    first_name VARCHAR(100) NOT NULL,              -- Voter's first name
    last_name VARCHAR(100) NOT NULL,               -- Voter's last name
    date_of_birth DATE NOT NULL,                   -- Date of birth
    address TEXT NOT NULL,                         -- Voter's residential address
    phone_number VARCHAR(20) UNIQUE,               -- Optional: Phone number for contact
    has_voted BOOLEAN DEFAULT FALSE,               -- Whether the voter has voted
    voting_time TIMESTAMP,                         -- Timestamp of when the vote was cast
    election_id UUID,                              -- Foreign key to election table (if multi-election system)
    is_eligible BOOLEAN DEFAULT TRUE,              -- Flag for voter eligibility
    registration_date TIMESTAMP DEFAULT NOW(),     -- Date of voter registration
    voting_district VARCHAR(100),                  -- Voter's district for regional elections
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,-- Record creation time
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Last record update time
);


CREATE TABLE candidates (
    candidate_id UUID PRIMARY KEY,                -- Unique identifier for the candidate
    user_id VARCHAR(32) NOT NULL UNIQUE,          -- Foreign key to authentication table
    election_id UUID NOT NULL,                    -- Foreign key to election table
    party_name VARCHAR(100),                      -- Political party the candidate is associated with (if applicable)
    manifesto TEXT,                               -- Optional text-based manifesto content
    manifesto_file_path VARCHAR(255),             -- Path or URL to the manifesto file (stored on the server or cloud)
    total_votes INT DEFAULT 0,                    -- Count of votes received
    constituency VARCHAR(100),                    -- Candidate's constituency or district
    nomination_date TIMESTAMP DEFAULT NOW(),      -- Date the candidate was nominated
    is_approved BOOLEAN DEFAULT FALSE,            -- Whether the candidate is approved to run
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,-- Record creation time
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Last record update time
);


CREATE TYPE user_role AS ENUM ('voter', 'candidate', 'admin');
CREATE TYPE account_status AS ENUM ('active', 'suspended', 'inactive');

-- Foreign key constraint to reference the authentication table
CREATE TABLE authentication (
    user_id UUID PRIMARY KEY,                        -- Unique identifier for the user
    user_name VARCHAR(255) NOT NULL UNIQUE,          -- Unique username for login
    password_hash VARCHAR(255) NOT NULL,             -- Hashed password for security
    salt VARCHAR(32) NOT NULL,                       -- Salt used in the password hashing
    user_role user_role NOT NULL, -- Role of the user
    account_status account_status NOT NULL, -- Account status
    email_id VARCHAR(255) NOT NULL UNIQUE,           -- Email ID, must be unique
    last_login TIMESTAMP,                            -- Timestamp of the user's last login
    account_creation_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Account creation time
    session_token VARCHAR(255),                      -- Token used for session management
    session_expiration_time TIMESTAMP                -- When the session will expire
);


ALTER TABLE voters
ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES authentication(user_id);

ALTER TABLE candidates
ALTER COLUMN user_id TYPE UUID USING user_id::UUID;

ALTER TABLE voters
ALTER COLUMN user_id TYPE UUID USING user_id::UUID;


-- Foreign key constraint to reference the authentication table
ALTER TABLE candidates
ADD CONSTRAINT fk_user_id_candidates FOREIGN KEY (user_id) REFERENCES authentication(user_id);

CREATE TABLE admin (
    admin_id UUID PRIMARY KEY,                    -- Unique identifier for each admin
    user_id VARCHAR(32) NOT NULL UNIQUE,          -- Foreign key to authentication table
    role VARCHAR(100) NOT NULL,                   -- Role or level of admin (e.g., 'super_admin', 'election_manager')
    permissions TEXT,                             -- JSON or text defining admin permissions (optional)
    assigned_elections UUID[],                    -- List of elections this admin is responsible for (optional)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,-- Record creation time
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Last record update time
);

CREATE TABLE ballots (
    ballot_id UUID PRIMARY KEY,                   -- Unique identifier for each ballot
    voter_id UUID NOT NULL,                       -- Foreign key to the voter table
    election_id UUID NOT NULL,                    -- Foreign key to the election table
    candidate_id UUID NOT NULL,                   -- Foreign key to the candidate table (who the voter selected)
    voting_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- When the vote was cast
);

ALTER TABLE admin
ALTER COLUMN user_id TYPE UUID USING user_id::UUID;

ALTER TABLE admin
ADD CONSTRAINT fk_user_id_admin FOREIGN KEY (user_id) REFERENCES authentication(user_id);

CREATE TYPE election_status AS ENUM ('upcoming', 'ongoing', 'completed');

CREATE TABLE elections (
    election_id UUID PRIMARY KEY,                  -- Unique identifier for the election
    election_name VARCHAR(255) NOT NULL,           -- Name of the election (e.g., 'Presidential Election 2024')
    election_type VARCHAR(100),                    -- Type of election (e.g., 'national', 'regional', 'local')
    election_start_date TIMESTAMP NOT NULL,        -- Date and time when the election starts
    election_end_date TIMESTAMP NOT NULL,          -- Date and time when the election ends
    is_active BOOLEAN DEFAULT TRUE,                -- Whether the election is currently active
    total_voters INT DEFAULT 0,                    -- Total number of voters eligible to vote in this election
    total_candidates INT DEFAULT 0,                -- Total number of candidates running in this election
    election_status election_status DEFAULT 'upcoming', -- Status of the election
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,-- Record creation time
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Last record update time 
);

INSERT INTO authentication (
    user_id, 
    user_name, 
    password_hash, 
    salt, 
    user_role, 
    account_status, 
    email_id
) VALUES 
(
    'b3d77a8c-81cd-4f01-9cfd-1ee71c43b527', -- Matching UUID
    'candidate1', 
    'hashedpassword', 
    'randomsalt', 
    'candidate', 
    'active', 
    'candidate1@example.com'
),
(
    '7a2b9112-7f45-43b0-bb76-6a499d71cb01', -- Matching UUID
    'candidate2', 
    'hashedpassword', 
    'randomsalt', 
    'candidate', 
    'active', 
    'candidate2@example.com'
),
(
    'ef9d2b6e-3fdc-4d11-b938-3f43537d8c97', -- Matching UUID
    'candidate3', 
    'hashedpassword', 
    'randomsalt', 
    'candidate', 
    'active', 
    'candidate3@example.com'
);


INSERT INTO candidates (
    candidate_id, 
    user_id, 
    election_id, 
    party_name, 
    manifesto, 
    manifesto_file_path, 
    total_votes, 
    constituency, 
    nomination_date, 
    is_approved, 
    created_at, 
    updated_at
) VALUES 
(
    'e4d909c2-8f45-4f9c-bfba-1bb8e2bca7a1', 
    'b3d77a8c-81cd-4f01-9cfd-1ee71c43b527', -- Replace with a valid UUID
    '1a3c5e8a-7d8b-4e4a-8f96-c6c9a9f5a9d3', 
    'Green Party', 
    'Promoting clean energy and sustainable living.', 
    '/manifestos/green_party_candidate.pdf', 
    0, 
    'Central District', 
    '2024-10-05 09:00:00', 
    TRUE, 
    '2024-10-05 09:00:00', 
    '2024-10-05 09:00:00'
),
(
    'b57fdf20-1a89-4e5a-b29f-6e5f3cb1c2d4', 
    '7a2b9112-7f45-43b0-bb76-6a499d71cb01', -- Replace with a valid UUID
    '2f7e3d4c-bc72-4b29-8e6d-29d79a3ab88d', 
    'Independent', 
    'Focusing on community-driven projects and transparency.', 
    '/manifestos/independent_candidate.pdf', 
    0, 
    'North Ward', 
    '2024-10-06 11:30:00', 
    FALSE, 
    '2024-10-06 11:30:00', 
    '2024-10-06 11:30:00'
),
(
    'c234ef89-dc73-4b20-90a4-1234abcd5678', 
    'ef9d2b6e-3fdc-4d11-b938-3f43537d8c97', -- Replace with a valid UUID
    'd4e6f8a5-c3ab-4117-8f0b-e7a9b6f2a1d2', 
    'Progressive Alliance', 
    'Advocating for education reform and economic growth.', 
    '/manifestos/progressive_alliance_candidate.pdf', 
    0, 
    'South East Constituency', 
    '2024-10-07 15:45:00', 
    TRUE, 
    '2024-10-07 15:45:00', 
    '2024-10-07 15:45:00'
);

-- Foreign key constraints to reference voter, election, and candidate tables
ALTER TABLE ballots
ADD CONSTRAINT fk_voter_id_ballot FOREIGN KEY (voter_id) REFERENCES voters(voter_id),
ADD CONSTRAINT fk_election_id_ballot FOREIGN KEY (election_id) REFERENCES elections(election_id),
ADD CONSTRAINT fk_candidate_id_ballot FOREIGN KEY (candidate_id) REFERENCES candidates(candidate_id);

CREATE TABLE audit_log (
    log_id UUID PRIMARY KEY,                      -- Unique identifier for the log entry
    user_id UUID NOT NULL,                        -- Foreign key to the user who performed the action
    action VARCHAR(255) NOT NULL,                 -- Description of the action (e.g., 'voted', 'login', 'updated profile')
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,-- When the action occurred
    details TEXT                                  -- Additional details about the action (optional)
);

-- Foreign key constraint to reference the authentication table
ALTER TABLE audit_log
ADD CONSTRAINT fk_user_id_audit FOREIGN KEY (user_id) REFERENCES authentication(user_id);

CREATE TYPE result_status AS ENUM('winner', 'loser', 'tie');

CREATE TABLE election_results (
    result_id UUID PRIMARY KEY,                   -- Unique identifier for the result entry
    election_id UUID NOT NULL,                    -- Foreign key to the election table
    candidate_id UUID NOT NULL,                   -- Foreign key to the candidate table
    total_votes INT DEFAULT 0,                    -- Total votes received by the candidate
    result_status result_status                   -- Status indicating if the candidate won, lost, or tied
);


-- Foreign key constraints to reference election and candidate tables
ALTER TABLE election_results
ADD CONSTRAINT fk_election_id_result FOREIGN KEY (election_id) REFERENCES elections(election_id),
ADD CONSTRAINT fk_candidate_id_result FOREIGN KEY (candidate_id) REFERENCES candidates(candidate_id);


CREATE TABLE voter_eligibility_log (
    log_id UUID PRIMARY KEY,                      -- Unique identifier for the log entry
    voter_id UUID NOT NULL,                       -- Foreign key to the voter table
    changed_by UUID,                              -- Admin who changed eligibility (foreign key to admin table)
    is_eligible BOOLEAN,                          -- New eligibility status
    change_reason TEXT,                           -- Reason for eligibility change
    change_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- When the change occurred
);

-- Foreign key constraint to reference voters and admin tables
ALTER TABLE voter_eligibility_log
ADD CONSTRAINT fk_voter_id_eligibility FOREIGN KEY (voter_id) REFERENCES voters(voter_id),
ADD CONSTRAINT fk_changed_by_admin FOREIGN KEY (changed_by) REFERENCES admin(admin_id);

CREATE TABLE notifications (
    notification_id UUID PRIMARY KEY,             -- Unique identifier for the notification
    user_id UUID NOT NULL,                        -- Foreign key to the user receiving the notification
    message TEXT NOT NULL,                        -- Content of the notification
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- When the notification was sent
    read_status BOOLEAN DEFAULT FALSE             -- Whether the user has read the notification
);

-- Foreign key constraint to reference the authentication table
ALTER TABLE notifications	
ADD CONSTRAINT fk_user_id_notification FOREIGN KEY (user_id) REFERENCES authentication(user_id);


select * from authentication;
select * from candidates;
