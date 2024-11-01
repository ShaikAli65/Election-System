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

-- Foreign key constraint to reference the authentication table



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
CREATE TYPE account_status AS ENUM ('active', 'suspended', 'inactive')

ALTER TABLE candidates
ALTER COLUMN user_id TYPE UUID USING user_id::UUID;

ALTER TABLE voters
ALTER COLUMN user_id TYPE UUID USING user_id::UUID;

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

CREATE TABLE ballots (
    ballot_id UUID PRIMARY KEY,                   -- Unique identifier for each ballot
    voter_id UUID NOT NULL,                       -- Foreign key to the voter table
    election_id UUID NOT NULL,                    -- Foreign key to the election table
    candidate_id UUID NOT NULL,                   -- Foreign key to the candidate table (who the voter selected)
    voting_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- When the vote was cast
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
