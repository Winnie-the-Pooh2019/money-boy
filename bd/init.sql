CREATE TABLE City
(
  id        int     NOT NULL,
  name      varchar NOT NULL,
  parent_id int    ,
  PRIMARY KEY (id)
);

CREATE TABLE Foundation
(
  id         int              NOT NULL,
  sum        double precision NOT NULL,
  city_id    int              NOT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE FoundationItem
(
  id            int              NOT NULL,
  sum           double precision,
  foundation_id int              NOT NULL,
  gov_item_id   int              NOT NULL,
  PRIMARY KEY (id)
);

create table item (
    id int primary key ,
    name varchar not null
);

