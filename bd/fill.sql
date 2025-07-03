insert into city values (1, 'Kemerovo', null);

insert into item (name) values ('топливно-энергетический комплекс');
insert into item (name) values ('водное хозяйство');
insert into item (name) values ('лесное хозяйство');
insert into item (name) values ('транспорт');
insert into item (name) values ('дорожное хозяйство');
insert into item (name) values ('связь и информатика');

insert into item (name) values ('жилищное хозяйство');
insert into item (name) values ('коммунальное хозяйство');
insert into item (name) values ('благоустройство');

insert into item (name) values ('дошкольное образование');
insert into item (name) values ('общее образование');
insert into item (name) values ('среднее профессиональное образование');
insert into item (name) values ('высшее образование');

insert into item (name) values ('стационарная медицинская помощь');
insert into item (name) values ('скорая медицинская помощь');

-- Первый отчет (6 проблем)
INSERT INTO problem_report (created_at) VALUES (now() - interval '7 days');

INSERT INTO problem_item (name, report_id) VALUES
('Безработица', currval('problem_report_id_seq')),
('Дорожные пробки', currval('problem_report_id_seq')),
('Низкое качество образования', currval('problem_report_id_seq')),
('Коррупция в ЖКХ', currval('problem_report_id_seq')),
('Отсутствие детских садов', currval('problem_report_id_seq')),
('Загрязнение парков', currval('problem_report_id_seq'));

-- Второй отчет (10 проблем)
INSERT INTO problem_report (created_at) VALUES (now() - interval '3 days');

INSERT INTO problem_item (name, report_id) VALUES
('Высокие тарифы ЖКХ', currval('problem_report_id_seq')),
('Недостаток больниц', currval('problem_report_id_seq')),
('Уличное воровство', currval('problem_report_id_seq')),
('Наркомания среди молодежи', currval('problem_report_id_seq')),
('Разрушение дорожного покрытия', currval('problem_report_id_seq')),
('Отсутствие спортивных площадок', currval('problem_report_id_seq')),
('Шумовое загрязнение ночью', currval('problem_report_id_seq')),
('Нехватка парковочных мест', currval('problem_report_id_seq')),
('Проблемы с общественным транспортом', currval('problem_report_id_seq')),
('Засилье рекламных конструкций', currval('problem_report_id_seq'));

CREATE TEMP TABLE temp_data AS
SELECT
    p.id AS problem_id,
    p.name AS problem_name,
    b.id AS budget_id,
    b.name AS budget_name
FROM problem_item p
CROSS JOIN item b;

-- Вставляем связи с коэффициентами эффективности
INSERT INTO problem_budget_link (problem_item_id, budget_item_id, efficiency)
SELECT
    problem_id,
    budget_id,
    -- Логика назначения коэффициентов в зависимости от типа проблем
    CASE
        -- Транспортные проблемы
        WHEN problem_name LIKE '%пробки%' OR problem_name LIKE '%транспорт%' OR problem_name LIKE '%дорог%'
            AND budget_name IN ('Дорожное строительство', 'Общественный транспорт')
            THEN 0.7 + random() * 0.3

        WHEN problem_name LIKE '%пробки%' OR problem_name LIKE '%транспорт%' OR problem_name LIKE '%дорог%'
            THEN 0.2 + random() * 0.3

        -- Социальные проблемы
        WHEN problem_name LIKE '%безработиц%' OR problem_name LIKE '%социал%'
            AND budget_name IN ('Социальная поддержка', 'Образовательные программы')
            THEN 0.6 + random() * 0.3

        -- Медицинские проблемы
        WHEN problem_name LIKE '%больниц%' OR problem_name LIKE '%здраво%'
            AND budget_name = 'Здравоохранение'
            THEN 0.8 + random() * 0.2

        -- Экологические проблемы
        WHEN problem_name LIKE '%экологи%' OR problem_name LIKE '%загрязн%' OR problem_name LIKE '%парк%'
            AND budget_name IN ('Экологические программы', 'Благоустройство территорий')
            THEN 0.65 + random() * 0.3

        -- Образовательные проблемы
        WHEN problem_name LIKE '%образован%' OR problem_name LIKE '%детск% сад%'
            AND budget_name = 'Образовательные программы'
            THEN 0.75 + random() * 0.25

        -- Для всех остальных комбинаций
        ELSE 0.1 + random() * 0.4
    END AS efficiency
FROM temp_data;

-- Удаляем временную таблицу
DROP TABLE temp_data;

update problem_budget_link set efficiency = 0;