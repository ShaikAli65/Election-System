
-- Insert sample data into the candidates table
-- Assuming each election has 4 candidates
DO $$
DECLARE
    election_rec RECORD;
BEGIN
    FOR election_rec IN
        SELECT election_id FROM public.elections
    LOOP
        INSERT INTO public.candidates (candidate_id, word_from_candidate, manifesto_file_path, total_votes, nomination_date, email_id, candidate_name, election_id)
        VALUES
            (uuid_generate_v4(), 'Word from Candidate 1', 'C:\\Users\\7862s\\Desktop\\Election-System\\database\\portfolios\\67338e84-a39e-4398-82cd-5623e2a9b8a1\\bd787bfb-5041-4443-b73b-9bc456a42f6b.pdf', 0, now(), 'candidate1@example.com', 'Candidate 1', election_rec.election_id),
            (uuid_generate_v4(), 'Word from Candidate 2', 'C:\\Users\\7862s\\Desktop\\Election-System\\database\\portfolios\\67338e84-a39e-4398-82cd-5623e2a9b8a1\\bd787bfb-5041-4443-b73b-9bc456a42f6b.pdf', 0, now(), 'candidate2@example.com', 'Candidate 2', election_rec.election_id),
            (uuid_generate_v4(), 'Word from Candidate 3', 'C:\\Users\\7862s\\Desktop\\Election-System\\database\\portfolios\\67338e84-a39e-4398-82cd-5623e2a9b8a1\\bd787bfb-5041-4443-b73b-9bc456a42f6b.pdf', 0, now(), 'candidate3@example.com', 'Candidate 3', election_rec.election_id),
            (uuid_generate_v4(), 'Word from Candidate 4', 'C:\\Users\\7862s\\Desktop\\Election-System\\database\\portfolios\\67338e84-a39e-4398-82cd-5623e2a9b8a1\\bd787bfb-5041-4443-b73b-9bc456a42f6b.pdf', 0, now(), 'candidate4@example.com', 'Candidate 4', election_rec.election_id);
    END LOOP;
END $$;