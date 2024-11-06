create type election_status as enum ('upcoming', 'ongoing', 'completed');

alter type election_status owner to postgres;

create type result_status as enum ('winner', 'loser', 'tie');

alter type result_status owner to postgres;

create table authentication
(
    user_id   uuid         not null
        primary key,
    user_name varchar(255) not null,
    email_id  varchar(255) not null
        unique
);

alter table authentication
    owner to postgres;

create table voters
(
    user_id     uuid not null
        constraint fk_user_id
            references authentication,
    has_voted   boolean default false,
    election_id uuid not null,
    constraint voters_pk
        primary key (election_id, user_id)
);

alter table voters
    owner to postgres;

create table elections
(
    election_id      uuid         not null
        primary key,
    title            varchar(255) not null,
    start_date       timestamp    not null,
    end_date         timestamp    not null,
    total_voters     integer         default 0,
    total_candidates integer         default 0,
    election_status  election_status default 'upcoming'::election_status,
    description      varchar(1024),
    validation_regex varchar(255)
);

alter table elections
    owner to postgres;

create table candidates
(
    candidate_id        uuid not null
        primary key,
    word_from_candidate text,
    manifesto_file_path varchar(1024),
    total_votes         integer   default 0,
    nomination_date     timestamp default now(),
    email_id            varchar(255),
    candidate_name      varchar(255),
    election_id         uuid not null
        constraint candidates_elections_election_id_fk
            references elections
);

alter table candidates
    owner to postgres;

create table ballots
(
    voter_id     uuid not null,
    election_id  uuid not null
        constraint fk_election_id_ballot
            references elections,
    candidate_id uuid not null
        constraint fk_candidate_id_ballot
            references candidates,
    voting_time  timestamp default CURRENT_TIMESTAMP,
    constraint ballots_pk
        unique (voter_id, election_id)
);

alter table ballots
    owner to postgres;

create table audit_log
(
    log_id    uuid         not null
        primary key,
    user_id   uuid         not null
        constraint fk_user_id_audit
            references authentication,
    action    varchar(255) not null,
    timestamp timestamp default CURRENT_TIMESTAMP,
    details   text
);

alter table audit_log
    owner to postgres;

create table election_results
(
    result_id    uuid not null
        primary key,
    election_id  uuid not null
        constraint fk_election_id_result
            references elections,
    candidate_id uuid not null
        constraint fk_candidate_id_result
            references candidates,
    total_votes  integer default 0
);

alter table election_results
    owner to postgres;

create function uuid_nil() returns uuid
    immutable
    strict
    parallel safe
    language c
as
$$
begin
-- missing source code
end;
$$;

alter function uuid_nil() owner to postgres;

create function uuid_ns_dns() returns uuid
    immutable
    strict
    parallel safe
    language c
as
$$
begin
-- missing source code
end;
$$;

alter function uuid_ns_dns() owner to postgres;

create function uuid_ns_url() returns uuid
    immutable
    strict
    parallel safe
    language c
as
$$
begin
-- missing source code
end;
$$;

alter function uuid_ns_url() owner to postgres;

create function uuid_ns_oid() returns uuid
    immutable
    strict
    parallel safe
    language c
as
$$
begin
-- missing source code
end;
$$;

alter function uuid_ns_oid() owner to postgres;

create function uuid_ns_x500() returns uuid
    immutable
    strict
    parallel safe
    language c
as
$$
begin
-- missing source code
end;
$$;

alter function uuid_ns_x500() owner to postgres;

create function uuid_generate_v1() returns uuid
    strict
    parallel safe
    language c
as
$$
begin
-- missing source code
end;
$$;

alter function uuid_generate_v1() owner to postgres;

create function uuid_generate_v1mc() returns uuid
    strict
    parallel safe
    language c
as
$$
begin
-- missing source code
end;
$$;

alter function uuid_generate_v1mc() owner to postgres;

create function uuid_generate_v3(namespace uuid, name text) returns uuid
    immutable
    strict
    parallel safe
    language c
as
$$
begin
-- missing source code
end;
$$;

alter function uuid_generate_v3(uuid, text) owner to postgres;

create function uuid_generate_v4() returns uuid
    strict
    parallel safe
    language c
as
$$
begin
-- missing source code
end;
$$;

alter function uuid_generate_v4() owner to postgres;

create function uuid_generate_v5(namespace uuid, name text) returns uuid
    immutable
    strict
    parallel safe
    language c
as
$$
begin
-- missing source code
end;
$$;

alter function uuid_generate_v5(uuid, text) owner to postgres;

