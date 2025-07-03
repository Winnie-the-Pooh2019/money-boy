create table if not exists city
(
    id        int primary key,
    name      varchar not null,
    parent_id int
);

create table if not exists problem_report
(
    id serial primary key ,
    created_at timestamp with time zone default now()
);

create table if not exists problem_item
(
    id serial primary key ,
    name varchar ,
    report_id int,

    constraint fk_problem_report_item foreign key (report_id) references problem_report(id)
);

create table if not exists foundation
(
    id      serial primary key,
    sum     double precision not null,
    city_id int              not null,

    constraint fk_foundation_city foreign key (city_id) references city (id)
);

create table if not exists foundation_report
(
    id         serial primary key,
    created_at timestamp with time zone default now()
);

create table if not exists foundation_item
(
    id        serial primary key,
    sum       double precision,
    report_id int not null,
    item_id   int not null,

    constraint fk_foundationitem_foundation foreign key (report_id) references foundation_report (id)
);

create table if not exists item
(
    id      serial primary key,
    name    varchar not null,
    min_sum double precision default 0.0
);

CREATE TABLE IF NOT EXISTS problem_budget_link (
    problem_item_id INT NOT NULL,
    budget_item_id INT NOT NULL,
    efficiency NUMERIC(5, 4) NOT NULL CHECK (efficiency BETWEEN 0 AND 1),

    CONSTRAINT fk_problem_item FOREIGN KEY (problem_item_id) REFERENCES problem_item(id),
    CONSTRAINT fk_budget_item FOREIGN KEY (budget_item_id) REFERENCES item(id),
    CONSTRAINT pk_problem_budget PRIMARY KEY (problem_item_id, budget_item_id)
);