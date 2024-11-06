INSERT INTO public.elections (election_id, title, start_date, end_date, total_voters, total_candidates, election_status, description, validation_regex)
VALUES
-- 20 elections with unique UUIDs, titles, dates, and default values for voters and candidates
(uuid_generate_v4(), 'Election 1', '2024-01-01 08:00:00', '2024-01-01 20:00:00', 100, 4, 'upcoming', 'Description for Election 1', '^[A-Z]{3}-\\d{4}$'),
(uuid_generate_v4(), 'Election 2', '2024-02-01 08:00:00', '2024-02-01 20:00:00', 150, 4, 'upcoming', 'Description for Election 2', '^[A-Z]{3}-\\d{4}$'),
(uuid_generate_v4(), 'Election 3', '2024-03-01 08:00:00', '2024-03-01 20:00:00', 200, 4, 'upcoming', 'Description for Election 3', '^[A-Z]{3}-\\d{4}$'),
(uuid_generate_v4(), 'Election 4', '2024-03-01 08:00:00', '2024-03-01 20:00:00', 200, 4, 'upcoming', 'Description for Election 3', '^[A-Z]{3}-\\d{4}$'),
(uuid_generate_v4(), 'Election 5', '2024-03-01 08:00:00', '2024-03-01 20:00:00', 200, 4, 'upcoming', 'Description for Election 3', '^[A-Z]{3}-\\d{4}$'),
(uuid_generate_v4(), 'Election 6', '2024-03-01 08:00:00', '2024-03-01 20:00:00', 200, 4, 'upcoming', 'Description for Election 3', '^[A-Z]{3}-\\d{4}$'),
(uuid_generate_v4(), 'Election 7', '2024-03-01 08:00:00', '2024-03-01 20:00:00', 200, 4, 'upcoming', 'Description for Election 3', '^[A-Z]{3}-\\d{4}$'),
(uuid_generate_v4(), 'Election 8', '2024-03-01 08:00:00', '2024-03-01 20:00:00', 200, 4, 'upcoming', 'Description for Election 3', '^[A-Z]{3}-\\d{4}$'),
(uuid_generate_v4(), 'Election 9', '2024-03-01 08:00:00', '2024-03-01 20:00:00', 200, 4, 'upcoming', 'Description for Election 3', '^[A-Z]{3}-\\d{4}$'),
(uuid_generate_v4(), 'Election 10', '2024-03-01 08:00:00', '2024-03-01 20:00:00', 200, 4, 'upcoming', 'Description for Election 3', '^[A-Z]{3}-\\d{4}$'),
(uuid_generate_v4(), 'Election 11', '2024-03-01 08:00:00', '2024-03-01 20:00:00', 200, 4, 'upcoming', 'Description for Election 3', '^[A-Z]{3}-\\d{4}$'),
(uuid_generate_v4(), 'Election 12', '2024-03-01 08:00:00', '2024-03-01 20:00:00', 200, 4, 'upcoming', 'Description for Election 3', '^[A-Z]{3}-\\d{4}$'),
(uuid_generate_v4(), 'Election 13', '2024-03-01 08:00:00', '2024-03-01 20:00:00', 200, 4, 'upcoming', 'Description for Election 3', '^[A-Z]{3}-\\d{4}$'),
(uuid_generate_v4(), 'Election 14', '2024-03-01 08:00:00', '2024-03-01 20:00:00', 200, 4, 'upcoming', 'Description for Election 3', '^[A-Z]{3}-\\d{4}$'),
(uuid_generate_v4(), 'Election 15', '2024-03-01 08:00:00', '2024-03-01 20:00:00', 200, 4, 'upcoming', 'Description for Election 3', '^[A-Z]{3}-\\d{4}$'),
(uuid_generate_v4(), 'Election 16', '2024-03-01 08:00:00', '2024-03-01 20:00:00', 200, 4, 'upcoming', 'Description for Election 3', '^[A-Z]{3}-\\d{4}$'),
(uuid_generate_v4(), 'Election 17', '2024-03-01 08:00:00', '2024-03-01 20:00:00', 200, 4, 'upcoming', 'Description for Election 3', '^[A-Z]{3}-\\d{4}$'),
(uuid_generate_v4(), 'Election 18', '2024-03-01 08:00:00', '2024-03-01 20:00:00', 200, 4, 'upcoming', 'Description for Election 3', '^[A-Z]{3}-\\d{4}$'),
(uuid_generate_v4(), 'Election 19', '2024-03-01 08:00:00', '2024-03-01 20:00:00', 200, 4, 'upcoming', 'Description for Election 3', '^[A-Z]{3}-\\d{4}$'),
(uuid_generate_v4(), 'Election 20', '2024-12-01 08:00:00', '2024-12-01 20:00:00', 400, 4, 'upcoming', 'Description for Election 20', '^[A-Z]{3}-\\d{4}$');
