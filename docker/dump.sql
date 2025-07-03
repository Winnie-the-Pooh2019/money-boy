--
-- PostgreSQL database dump
--

-- Dumped from database version 15.13
-- Dumped by pg_dump version 15.13

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: city; Type: TABLE; Schema: public; Owner: ivan
--

CREATE TABLE public.city (
    id integer NOT NULL,
    name character varying NOT NULL,
    parent_id integer
);


ALTER TABLE public.city OWNER TO ivan;

--
-- Name: foundation; Type: TABLE; Schema: public; Owner: ivan
--

CREATE TABLE public.foundation (
    id integer NOT NULL,
    sum double precision NOT NULL,
    city_id integer NOT NULL
);


ALTER TABLE public.foundation OWNER TO ivan;

--
-- Name: foundation_id_seq; Type: SEQUENCE; Schema: public; Owner: ivan
--

CREATE SEQUENCE public.foundation_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.foundation_id_seq OWNER TO ivan;

--
-- Name: foundation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ivan
--

ALTER SEQUENCE public.foundation_id_seq OWNED BY public.foundation.id;


--
-- Name: foundation_item; Type: TABLE; Schema: public; Owner: ivan
--

CREATE TABLE public.foundation_item (
    id integer NOT NULL,
    sum double precision,
    report_id integer NOT NULL,
    item_id integer NOT NULL
);


ALTER TABLE public.foundation_item OWNER TO ivan;

--
-- Name: foundation_item_id_seq; Type: SEQUENCE; Schema: public; Owner: ivan
--

CREATE SEQUENCE public.foundation_item_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.foundation_item_id_seq OWNER TO ivan;

--
-- Name: foundation_item_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ivan
--

ALTER SEQUENCE public.foundation_item_id_seq OWNED BY public.foundation_item.id;


--
-- Name: foundation_report; Type: TABLE; Schema: public; Owner: ivan
--

CREATE TABLE public.foundation_report (
    id integer NOT NULL,
    created_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.foundation_report OWNER TO ivan;

--
-- Name: foundation_report_id_seq; Type: SEQUENCE; Schema: public; Owner: ivan
--

CREATE SEQUENCE public.foundation_report_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.foundation_report_id_seq OWNER TO ivan;

--
-- Name: foundation_report_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ivan
--

ALTER SEQUENCE public.foundation_report_id_seq OWNED BY public.foundation_report.id;


--
-- Name: item; Type: TABLE; Schema: public; Owner: ivan
--

CREATE TABLE public.item (
    id integer NOT NULL,
    name character varying NOT NULL,
    min_sum double precision DEFAULT 0.0
);


ALTER TABLE public.item OWNER TO ivan;

--
-- Name: item_id_seq; Type: SEQUENCE; Schema: public; Owner: ivan
--

CREATE SEQUENCE public.item_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.item_id_seq OWNER TO ivan;

--
-- Name: item_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ivan
--

ALTER SEQUENCE public.item_id_seq OWNED BY public.item.id;


--
-- Name: problem_budget_link; Type: TABLE; Schema: public; Owner: ivan
--

CREATE TABLE public.problem_budget_link (
    problem_item_id integer NOT NULL,
    budget_item_id integer NOT NULL,
    efficiency numeric(5,4) NOT NULL,
    CONSTRAINT problem_budget_link_efficiency_check CHECK (((efficiency >= (0)::numeric) AND (efficiency <= (1)::numeric)))
);


ALTER TABLE public.problem_budget_link OWNER TO ivan;

--
-- Name: problem_item; Type: TABLE; Schema: public; Owner: ivan
--

CREATE TABLE public.problem_item (
    id integer NOT NULL,
    name character varying,
    report_id integer,
    frequency integer DEFAULT 100 NOT NULL
);


ALTER TABLE public.problem_item OWNER TO ivan;

--
-- Name: problem_item_id_seq; Type: SEQUENCE; Schema: public; Owner: ivan
--

CREATE SEQUENCE public.problem_item_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.problem_item_id_seq OWNER TO ivan;

--
-- Name: problem_item_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ivan
--

ALTER SEQUENCE public.problem_item_id_seq OWNED BY public.problem_item.id;


--
-- Name: problem_report; Type: TABLE; Schema: public; Owner: ivan
--

CREATE TABLE public.problem_report (
    id integer NOT NULL,
    created_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.problem_report OWNER TO ivan;

--
-- Name: problem_report_id_seq; Type: SEQUENCE; Schema: public; Owner: ivan
--

CREATE SEQUENCE public.problem_report_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.problem_report_id_seq OWNER TO ivan;

--
-- Name: problem_report_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ivan
--

ALTER SEQUENCE public.problem_report_id_seq OWNED BY public.problem_report.id;


--
-- Name: foundation id; Type: DEFAULT; Schema: public; Owner: ivan
--

ALTER TABLE ONLY public.foundation ALTER COLUMN id SET DEFAULT nextval('public.foundation_id_seq'::regclass);


--
-- Name: foundation_item id; Type: DEFAULT; Schema: public; Owner: ivan
--

ALTER TABLE ONLY public.foundation_item ALTER COLUMN id SET DEFAULT nextval('public.foundation_item_id_seq'::regclass);


--
-- Name: foundation_report id; Type: DEFAULT; Schema: public; Owner: ivan
--

ALTER TABLE ONLY public.foundation_report ALTER COLUMN id SET DEFAULT nextval('public.foundation_report_id_seq'::regclass);


--
-- Name: item id; Type: DEFAULT; Schema: public; Owner: ivan
--

ALTER TABLE ONLY public.item ALTER COLUMN id SET DEFAULT nextval('public.item_id_seq'::regclass);


--
-- Name: problem_item id; Type: DEFAULT; Schema: public; Owner: ivan
--

ALTER TABLE ONLY public.problem_item ALTER COLUMN id SET DEFAULT nextval('public.problem_item_id_seq'::regclass);


--
-- Name: problem_report id; Type: DEFAULT; Schema: public; Owner: ivan
--

ALTER TABLE ONLY public.problem_report ALTER COLUMN id SET DEFAULT nextval('public.problem_report_id_seq'::regclass);


--
-- Data for Name: city; Type: TABLE DATA; Schema: public; Owner: ivan
--

COPY public.city (id, name, parent_id) FROM stdin;
\.


--
-- Data for Name: foundation; Type: TABLE DATA; Schema: public; Owner: ivan
--

COPY public.foundation (id, sum, city_id) FROM stdin;
\.


--
-- Data for Name: foundation_item; Type: TABLE DATA; Schema: public; Owner: ivan
--

COPY public.foundation_item (id, sum, report_id, item_id) FROM stdin;
\.


--
-- Data for Name: foundation_report; Type: TABLE DATA; Schema: public; Owner: ivan
--

COPY public.foundation_report (id, created_at) FROM stdin;
\.


--
-- Data for Name: item; Type: TABLE DATA; Schema: public; Owner: ivan
--

COPY public.item (id, name, min_sum) FROM stdin;
1	топливно-энергетический комплекс	0
2	водное хозяйство	0
3	лесное хозяйство	0
4	транспорт	0
5	дорожное хозяйство	0
6	связь и информатика	0
7	жилищное хозяйство	0
8	коммунальное хозяйство	0
9	благоустройство	0
10	дошкольное образование	0
11	общее образование	0
12	среднее профессиональное образование	0
13	высшее образование	0
14	стационарная медицинская помощь	0
15	скорая медицинская помощь	0
\.


--
-- Data for Name: problem_budget_link; Type: TABLE DATA; Schema: public; Owner: ivan
--

COPY public.problem_budget_link (problem_item_id, budget_item_id, efficiency) FROM stdin;
4	7	1.0000
5	10	1.0000
6	9	1.0000
7	7	1.0000
8	14	1.0000
1	12	0.0000
1	13	1.0000
2	4	1.0000
2	5	0.0000
3	11	1.0000
3	12	0.0000
3	13	0.0000
1	1	0.0000
1	2	0.0000
1	3	0.0000
1	4	0.0000
1	5	0.0000
1	6	0.0000
1	7	0.0000
1	8	0.0000
1	9	0.0000
1	10	0.0000
1	11	0.0000
1	14	0.0000
1	15	0.0000
2	1	0.0000
2	2	0.0000
2	3	0.0000
2	6	0.0000
2	7	0.0000
2	8	0.0000
2	9	0.0000
2	10	0.0000
2	11	0.0000
2	12	0.0000
2	13	0.0000
2	14	0.0000
2	15	0.0000
3	1	0.0000
3	2	0.0000
3	3	0.0000
3	4	0.0000
3	5	0.0000
3	6	0.0000
3	7	0.0000
3	8	0.0000
3	9	0.0000
3	10	0.0000
3	14	0.0000
3	15	0.0000
4	1	0.0000
4	2	0.0000
4	3	0.0000
4	4	0.0000
4	5	0.0000
4	6	0.0000
4	8	0.0000
4	9	0.0000
4	10	0.0000
4	11	0.0000
4	12	0.0000
4	13	0.0000
4	14	0.0000
4	15	0.0000
5	1	0.0000
5	2	0.0000
5	3	0.0000
5	4	0.0000
5	5	0.0000
5	6	0.0000
5	7	0.0000
5	8	0.0000
5	9	0.0000
5	11	0.0000
5	12	0.0000
5	13	0.0000
5	14	0.0000
5	15	0.0000
6	1	0.0000
6	2	0.0000
6	3	0.0000
6	4	0.0000
6	5	0.0000
6	6	0.0000
6	7	0.0000
6	8	0.0000
6	10	0.0000
6	11	0.0000
6	12	0.0000
6	13	0.0000
6	14	0.0000
6	15	0.0000
7	1	0.0000
7	2	0.0000
7	3	0.0000
7	4	0.0000
7	5	0.0000
7	6	0.0000
7	8	0.0000
7	9	0.0000
7	10	0.0000
7	11	0.0000
7	12	0.0000
7	13	0.0000
7	14	0.0000
7	15	0.0000
8	1	0.0000
8	2	0.0000
8	3	0.0000
8	4	0.0000
8	5	0.0000
8	6	0.0000
8	7	0.0000
8	8	0.0000
8	9	0.0000
8	10	0.0000
8	11	0.0000
8	12	0.0000
8	13	0.0000
8	15	0.0000
9	1	0.0000
9	2	0.0000
9	3	0.0000
9	4	0.0000
9	5	0.0000
9	6	0.0000
9	7	0.0000
9	8	0.0000
9	9	0.0000
9	10	0.0000
9	13	0.0000
9	14	0.0000
9	15	0.0000
10	1	0.0000
10	2	0.0000
10	3	0.0000
10	4	0.0000
10	5	0.0000
10	6	0.0000
10	7	0.0000
10	8	0.0000
10	9	0.0000
10	10	0.0000
10	13	0.0000
10	14	0.0000
10	15	0.0000
11	1	0.0000
11	2	0.0000
11	3	0.0000
11	4	0.0000
11	6	0.0000
11	7	0.0000
11	8	0.0000
11	9	0.0000
11	10	0.0000
11	11	0.0000
11	12	0.0000
11	13	0.0000
11	14	0.0000
11	15	0.0000
12	1	0.0000
12	2	0.0000
12	3	0.0000
12	4	0.0000
12	5	0.0000
12	6	0.0000
12	7	0.0000
12	8	0.0000
12	10	0.0000
12	11	0.0000
12	12	0.0000
12	13	0.0000
12	14	0.0000
12	15	0.0000
13	1	0.0000
13	2	0.0000
13	3	0.0000
13	5	0.0000
13	6	0.0000
13	7	0.0000
13	8	0.0000
13	9	0.0000
13	10	0.0000
13	11	0.0000
13	12	0.0000
13	13	0.0000
13	14	0.0000
13	15	0.0000
14	1	0.0000
14	2	0.0000
14	3	0.0000
14	4	0.0000
14	6	0.0000
14	7	0.0000
14	8	0.0000
14	9	0.0000
14	10	0.0000
14	11	0.0000
14	12	0.0000
14	13	0.0000
14	14	0.0000
14	15	0.0000
15	1	0.0000
15	2	0.0000
15	3	0.0000
15	5	0.0000
15	6	0.0000
15	7	0.0000
15	8	0.0000
15	9	0.0000
15	10	0.0000
15	11	0.0000
15	12	0.0000
15	13	0.0000
15	14	0.0000
15	15	0.0000
16	1	0.0000
16	2	0.0000
16	3	0.0000
16	4	0.0000
16	5	0.0000
16	6	0.0000
16	7	0.0000
16	8	0.0000
16	10	0.0000
16	11	0.0000
16	12	0.0000
16	13	0.0000
16	14	0.0000
16	15	0.0000
11	5	1.0000
12	9	1.0000
13	4	1.0000
14	5	1.0000
15	4	1.0000
16	9	1.0000
9	11	1.0000
9	12	0.0000
10	11	1.0000
10	12	0.0000
\.


--
-- Data for Name: problem_item; Type: TABLE DATA; Schema: public; Owner: ivan
--

COPY public.problem_item (id, name, report_id, frequency) FROM stdin;
5	Отсутствие детских садов	1	100
16	Засилье рекламных конструкций	2	100
1	Безработица	1	80
2	Дорожные пробки	1	200
3	Низкое качество образования	1	150
4	Коррупция в ЖКХ	1	96
6	Загрязнение парков	1	330
7	Высокие тарифы ЖКХ	2	300
8	Недостаток больниц	2	491
9	Уличное воровство	2	73
10	Наркомания среди молодежи	2	90
11	Разрушение дорожного покрытия	2	427
12	Отсутствие спортивных площадок	2	212
13	Шумовое загрязнение ночью	2	346
14	Нехватка парковочных мест	2	452
15	Проблемы с общественным транспортом	2	500
\.


--
-- Data for Name: problem_report; Type: TABLE DATA; Schema: public; Owner: ivan
--

COPY public.problem_report (id, created_at) FROM stdin;
1	2025-06-25 22:52:34.965943+00
2	2025-06-29 22:52:47.334292+00
\.


--
-- Name: foundation_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ivan
--

SELECT pg_catalog.setval('public.foundation_id_seq', 1, false);


--
-- Name: foundation_item_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ivan
--

SELECT pg_catalog.setval('public.foundation_item_id_seq', 1, false);


--
-- Name: foundation_report_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ivan
--

SELECT pg_catalog.setval('public.foundation_report_id_seq', 1, false);


--
-- Name: item_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ivan
--

SELECT pg_catalog.setval('public.item_id_seq', 15, true);


--
-- Name: problem_item_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ivan
--

SELECT pg_catalog.setval('public.problem_item_id_seq', 16, true);


--
-- Name: problem_report_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ivan
--

SELECT pg_catalog.setval('public.problem_report_id_seq', 2, true);


--
-- Name: city city_pkey; Type: CONSTRAINT; Schema: public; Owner: ivan
--

ALTER TABLE ONLY public.city
    ADD CONSTRAINT city_pkey PRIMARY KEY (id);


--
-- Name: foundation_item foundation_item_pkey; Type: CONSTRAINT; Schema: public; Owner: ivan
--

ALTER TABLE ONLY public.foundation_item
    ADD CONSTRAINT foundation_item_pkey PRIMARY KEY (id);


--
-- Name: foundation foundation_pkey; Type: CONSTRAINT; Schema: public; Owner: ivan
--

ALTER TABLE ONLY public.foundation
    ADD CONSTRAINT foundation_pkey PRIMARY KEY (id);


--
-- Name: foundation_report foundation_report_pkey; Type: CONSTRAINT; Schema: public; Owner: ivan
--

ALTER TABLE ONLY public.foundation_report
    ADD CONSTRAINT foundation_report_pkey PRIMARY KEY (id);


--
-- Name: item item_pkey; Type: CONSTRAINT; Schema: public; Owner: ivan
--

ALTER TABLE ONLY public.item
    ADD CONSTRAINT item_pkey PRIMARY KEY (id);


--
-- Name: problem_budget_link pk_problem_budget; Type: CONSTRAINT; Schema: public; Owner: ivan
--

ALTER TABLE ONLY public.problem_budget_link
    ADD CONSTRAINT pk_problem_budget PRIMARY KEY (problem_item_id, budget_item_id);


--
-- Name: problem_item problem_item_pkey; Type: CONSTRAINT; Schema: public; Owner: ivan
--

ALTER TABLE ONLY public.problem_item
    ADD CONSTRAINT problem_item_pkey PRIMARY KEY (id);


--
-- Name: problem_report problem_report_pkey; Type: CONSTRAINT; Schema: public; Owner: ivan
--

ALTER TABLE ONLY public.problem_report
    ADD CONSTRAINT problem_report_pkey PRIMARY KEY (id);


--
-- Name: problem_budget_link fk_budget_item; Type: FK CONSTRAINT; Schema: public; Owner: ivan
--

ALTER TABLE ONLY public.problem_budget_link
    ADD CONSTRAINT fk_budget_item FOREIGN KEY (budget_item_id) REFERENCES public.item(id);


--
-- Name: foundation fk_foundation_city; Type: FK CONSTRAINT; Schema: public; Owner: ivan
--

ALTER TABLE ONLY public.foundation
    ADD CONSTRAINT fk_foundation_city FOREIGN KEY (city_id) REFERENCES public.city(id);


--
-- Name: foundation_item fk_foundationitem_foundation; Type: FK CONSTRAINT; Schema: public; Owner: ivan
--

ALTER TABLE ONLY public.foundation_item
    ADD CONSTRAINT fk_foundationitem_foundation FOREIGN KEY (report_id) REFERENCES public.foundation_report(id);


--
-- Name: problem_budget_link fk_problem_item; Type: FK CONSTRAINT; Schema: public; Owner: ivan
--

ALTER TABLE ONLY public.problem_budget_link
    ADD CONSTRAINT fk_problem_item FOREIGN KEY (problem_item_id) REFERENCES public.problem_item(id);


--
-- Name: problem_item fk_problem_report_item; Type: FK CONSTRAINT; Schema: public; Owner: ivan
--

ALTER TABLE ONLY public.problem_item
    ADD CONSTRAINT fk_problem_report_item FOREIGN KEY (report_id) REFERENCES public.problem_report(id);


--
-- PostgreSQL database dump complete
--

