CREATE TABLE voters (
    user_id UUID PRIMARY KEY,                      -- Foreign key to authentication table
    has_voted BOOLEAN DEFAULT FALSE,               -- Whether the voter has voted
    election_id UUID                             -- Foreign key to election table (if multi-election system)
);


CREATE TABLE candidates (
    candidate_id UUID PRIMARY KEY,                -- Foreign key to authentication table
    election_id UUID NOT NULL,                    -- Foreign key to election table
    candidate_description TEXT,                   -- Optional text-based manifesto content
    manifesto_file_path VARCHAR(255),             -- Path or URL to the manifesto file (stored on the server or cloud)
    total_votes INT DEFAULT 0,                    -- Count of votes received
    nomination_date TIMESTAMP DEFAULT NOW(),       -- Date the candidate was nominated
    candidate_name VARCHAR(255),
    email_id VARCHAR(255)
);



-- Foreign key constraint to reference the authentication table
CREATE TABLE authentication (
    user_id UUID PRIMARY KEY,                        -- Unique identifier for the user
    user_name VARCHAR(255) NOT NULL UNIQUE,          -- Username for login
    email_id VARCHAR(255) NOT NULL UNIQUE            -- Email ID, must be unique
    
);


ALTER TABLE voters
ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES authentication(user_id);



CREATE TABLE ballots (
    ballot_id UUID PRIMARY KEY,                   -- Unique identifier for each ballot
    voter_id UUID NOT NULL,                       -- Foreign key to the voter table
    election_id UUID NOT NULL,                    -- Foreign key to the election table
    candidate_id UUID NOT NULL,                   -- Foreign key to the candidate table (who the voter selected)
    voting_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- When the vote was cast
);


CREATE TYPE election_status AS ENUM ('upcoming', 'ongoing', 'completed');

CREATE TABLE elections (
    election_id UUID PRIMARY KEY,                       -- Unique identifier for the election
    election_name VARCHAR(255) NOT NULL,                -- Name of the election (e.g., 'Presidential Election 2024')
    election_start_date TIMESTAMP NOT NULL,             -- Date and time when the election starts
    election_end_date TIMESTAMP NOT NULL,               -- Date and time when the election ends
    total_voters INT DEFAULT 0,                         -- Total number of voters eligible to vote in this election
    total_candidates INT DEFAULT 0,                     -- Total number of candidates running in this election
    election_status election_status DEFAULT 'upcoming'  -- Status of the election
);


-- Foreign key constraints to reference voter, election, and candidate tables
ALTER TABLE ballots
ADD CONSTRAINT fk_voter_id_ballot FOREIGN KEY (voter_id) REFERENCES voters(user_id),
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
    candidate_id UUID NOT NULL,                        -- Foreign key to the candidate table
    total_votes INT DEFAULT 0,                    -- Total votes received by the candidate
    result_status result_status                   -- Status indicating if the candidate won, lost, or tied
);


-- Foreign key constraints to reference election and candidate tables
ALTER TABLE election_results
ADD CONSTRAINT fk_election_id_result FOREIGN KEY (election_id) REFERENCES elections(election_id),
ADD CONSTRAINT fk_candidate_id_result FOREIGN KEY (candidate_id) REFERENCES candidates(candidate_id);

