--
-- PostgreSQL database dump
--

-- Dumped from database version 14.5 (Homebrew)
-- Dumped by pg_dump version 14.5 (Homebrew)

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

--
-- Name: task_manager; Type: DATABASE; Schema: -; Owner: postgres
--

CREATE DATABASE task_manager WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE = 'C';


ALTER DATABASE task_manager OWNER TO postgres;

\connect task_manager

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

--
-- Name: system; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA system;


ALTER SCHEMA system OWNER TO postgres;

--
-- Name: SCHEMA system; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON SCHEMA system IS 'Системная схема';


--
-- Name: tasks; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA tasks;


ALTER SCHEMA tasks OWNER TO postgres;

--
-- Name: create_id_system; Type: SEQUENCE; Schema: system; Owner: postgres
--

CREATE SEQUENCE system.create_id_system
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE system.create_id_system OWNER TO postgres;

--
-- Name: create_id_users; Type: SEQUENCE; Schema: system; Owner: postgres
--

CREATE SEQUENCE system.create_id_users
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE system.create_id_users OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: system; Type: TABLE; Schema: system; Owner: postgres
--

CREATE TABLE system.system (
    id_system integer DEFAULT nextval('system.create_id_system'::regclass) NOT NULL,
    available_threads smallint NOT NULL,
    active boolean DEFAULT false NOT NULL,
    host character varying(15),
    threads smallint NOT NULL
);


ALTER TABLE system.system OWNER TO postgres;

--
-- Name: TABLE system; Type: COMMENT; Schema: system; Owner: postgres
--

COMMENT ON TABLE system.system IS 'Таблица с описанием виртуальных систем';


--
-- Name: COLUMN system.available_threads; Type: COMMENT; Schema: system; Owner: postgres
--

COMMENT ON COLUMN system.system.available_threads IS 'Доступное количество ядер системы';


--
-- Name: COLUMN system.active; Type: COMMENT; Schema: system; Owner: postgres
--

COMMENT ON COLUMN system.system.active IS 'Флаг "Состояние машины"';


--
-- Name: COLUMN system.host; Type: COMMENT; Schema: system; Owner: postgres
--

COMMENT ON COLUMN system.system.host IS 'Хост для подключения к машине';


--
-- Name: COLUMN system.threads; Type: COMMENT; Schema: system; Owner: postgres
--

COMMENT ON COLUMN system.system.threads IS 'Количество ядер системы';


--
-- Name: users; Type: TABLE; Schema: system; Owner: postgres
--

CREATE TABLE system.users (
    id_user integer DEFAULT nextval('system.create_id_users'::regclass) NOT NULL,
    first_name character varying(100) NOT NULL,
    last_name character varying(100) NOT NULL,
    is_staff boolean DEFAULT false NOT NULL,
    username character varying(50) NOT NULL,
    password character varying NOT NULL,
    guid uuid NOT NULL,
    email character varying(100) NOT NULL
);


ALTER TABLE system.users OWNER TO postgres;

--
-- Name: TABLE users; Type: COMMENT; Schema: system; Owner: postgres
--

COMMENT ON TABLE system.users IS 'Таблица пользователей';


--
-- Name: COLUMN users.id_user; Type: COMMENT; Schema: system; Owner: postgres
--

COMMENT ON COLUMN system.users.id_user IS 'ИД пользователя';


--
-- Name: COLUMN users.first_name; Type: COMMENT; Schema: system; Owner: postgres
--

COMMENT ON COLUMN system.users.first_name IS 'Имя';


--
-- Name: COLUMN users.last_name; Type: COMMENT; Schema: system; Owner: postgres
--

COMMENT ON COLUMN system.users.last_name IS 'Фамилия';


--
-- Name: COLUMN users.is_staff; Type: COMMENT; Schema: system; Owner: postgres
--

COMMENT ON COLUMN system.users.is_staff IS 'Флаг "сотрудник"';


--
-- Name: COLUMN users.username; Type: COMMENT; Schema: system; Owner: postgres
--

COMMENT ON COLUMN system.users.username IS 'Имя пользователя';


--
-- Name: COLUMN users.password; Type: COMMENT; Schema: system; Owner: postgres
--

COMMENT ON COLUMN system.users.password IS 'Пароль';


--
-- Name: COLUMN users.guid; Type: COMMENT; Schema: system; Owner: postgres
--

COMMENT ON COLUMN system.users.guid IS 'Уникальный идентификатор';


--
-- Name: COLUMN users.email; Type: COMMENT; Schema: system; Owner: postgres
--

COMMENT ON COLUMN system.users.email IS 'Email';

--
-- Name: create_id_order; Type: SEQUENCE; Schema: tasks; Owner: postgres
--

CREATE SEQUENCE tasks.create_id_order
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE tasks.create_id_order OWNER TO postgres;

--
-- Name: create_id_status; Type: SEQUENCE; Schema: tasks; Owner: postgres
--

CREATE SEQUENCE tasks.create_id_status
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE tasks.create_id_status OWNER TO postgres;

--
-- Name: create_id_task; Type: SEQUENCE; Schema: tasks; Owner: postgres
--

CREATE SEQUENCE tasks.create_id_task
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE tasks.create_id_task OWNER TO postgres;

--
-- Name: files; Type: TABLE; Schema: tasks; Owner: postgres
--

CREATE TABLE tasks.files (
    id_file uuid NOT NULL,
    file_path character varying NOT NULL,
    readable_file_name character varying NOT NULL
);


ALTER TABLE tasks.files OWNER TO postgres;

--
-- Name: TABLE files; Type: COMMENT; Schema: tasks; Owner: postgres
--

COMMENT ON TABLE tasks.files IS 'Таблица для хранения информации о файлах';


--
-- Name: COLUMN files.id_file; Type: COMMENT; Schema: tasks; Owner: postgres
--

COMMENT ON COLUMN tasks.files.id_file IS 'UUID Файла';


--
-- Name: COLUMN files.file_path; Type: COMMENT; Schema: tasks; Owner: postgres
--

COMMENT ON COLUMN tasks.files.file_path IS 'Расположение файла';


--
-- Name: COLUMN files.readable_file_name; Type: COMMENT; Schema: tasks; Owner: postgres
--

COMMENT ON COLUMN tasks.files.readable_file_name IS 'Человеко-читаемое имя файла';


--
-- Name: order; Type: TABLE; Schema: tasks; Owner: postgres
--

CREATE TABLE tasks."order" (
    id_order integer DEFAULT nextval('tasks.create_id_order'::regclass) NOT NULL,
    id_task integer NOT NULL,
    order_number integer
);


ALTER TABLE tasks."order" OWNER TO postgres;

--
-- Name: TABLE "order"; Type: COMMENT; Schema: tasks; Owner: postgres
--

COMMENT ON TABLE tasks."order" IS 'Таблица-очередь';


--
-- Name: COLUMN "order".id_order; Type: COMMENT; Schema: tasks; Owner: postgres
--

COMMENT ON COLUMN tasks."order".id_order IS 'ИД очереди';


--
-- Name: COLUMN "order".id_task; Type: COMMENT; Schema: tasks; Owner: postgres
--

COMMENT ON COLUMN tasks."order".id_task IS 'ИД Задачи';


--
-- Name: COLUMN "order".order_number; Type: COMMENT; Schema: tasks; Owner: postgres
--

COMMENT ON COLUMN tasks."order".order_number IS 'Номер в очереди';


--
-- Name: status; Type: TABLE; Schema: tasks; Owner: postgres
--

CREATE TABLE tasks.status (
    id_status integer DEFAULT nextval('tasks.create_id_status'::regclass) NOT NULL,
    name character varying NOT NULL
);


ALTER TABLE tasks.status OWNER TO postgres;

--
-- Name: TABLE status; Type: COMMENT; Schema: tasks; Owner: postgres
--

COMMENT ON TABLE tasks.status IS 'Классификатор статусов задачи';


--
-- Name: COLUMN status.id_status; Type: COMMENT; Schema: tasks; Owner: postgres
--

COMMENT ON COLUMN tasks.status.id_status IS 'ИД статуса';


--
-- Name: COLUMN status.name; Type: COMMENT; Schema: tasks; Owner: postgres
--

COMMENT ON COLUMN tasks.status.name IS 'Наименование статуса задачи';


--
-- Name: tasks; Type: TABLE; Schema: tasks; Owner: postgres
--

CREATE TABLE tasks.tasks (
    id_task integer DEFAULT nextval('tasks.create_id_task'::regclass) NOT NULL,
    params character varying,
    num_threads integer NOT NULL,
    priority integer DEFAULT 1 NOT NULL,
    running_on integer,
    id_user integer NOT NULL,
    process_id integer,
    created_at timestamp without time zone NOT NULL,
    output character varying,
    errors character varying,
    exitcode integer,
    id_file uuid NOT NULL,
    id_status integer NOT NULL
);


ALTER TABLE tasks.tasks OWNER TO postgres;

--
-- Name: TABLE tasks; Type: COMMENT; Schema: tasks; Owner: postgres
--

COMMENT ON TABLE tasks.tasks IS 'Таблица с задачами для суперкомпьютера';


--
-- Name: COLUMN tasks.id_task; Type: COMMENT; Schema: tasks; Owner: postgres
--

COMMENT ON COLUMN tasks.tasks.id_task IS 'ИД задачи';


--
-- Name: COLUMN tasks.params; Type: COMMENT; Schema: tasks; Owner: postgres
--

COMMENT ON COLUMN tasks.tasks.params IS 'Параметры исполнения';


--
-- Name: COLUMN tasks.num_threads; Type: COMMENT; Schema: tasks; Owner: postgres
--

COMMENT ON COLUMN tasks.tasks.num_threads IS 'Количество потоков исполнения';


--
-- Name: COLUMN tasks.priority; Type: COMMENT; Schema: tasks; Owner: postgres
--

COMMENT ON COLUMN tasks.tasks.priority IS 'Приоритет исполнения задачи';


--
-- Name: COLUMN tasks.running_on; Type: COMMENT; Schema: tasks; Owner: postgres
--

COMMENT ON COLUMN tasks.tasks.running_on IS 'ИД исполняющей системы';


--
-- Name: COLUMN tasks.id_user; Type: COMMENT; Schema: tasks; Owner: postgres
--

COMMENT ON COLUMN tasks.tasks.id_user IS 'ИД Пользователя';


--
-- Name: COLUMN tasks.process_id; Type: COMMENT; Schema: tasks; Owner: postgres
--

COMMENT ON COLUMN tasks.tasks.process_id IS 'ИД процесса исполнения';


--
-- Name: COLUMN tasks.created_at; Type: COMMENT; Schema: tasks; Owner: postgres
--

COMMENT ON COLUMN tasks.tasks.created_at IS 'Время создания';


--
-- Name: COLUMN tasks.output; Type: COMMENT; Schema: tasks; Owner: postgres
--

COMMENT ON COLUMN tasks.tasks.output IS 'Вывод программы';


--
-- Name: COLUMN tasks.errors; Type: COMMENT; Schema: tasks; Owner: postgres
--

COMMENT ON COLUMN tasks.tasks.errors IS 'Ошибки программы';


--
-- Name: COLUMN tasks.exitcode; Type: COMMENT; Schema: tasks; Owner: postgres
--

COMMENT ON COLUMN tasks.tasks.exitcode IS 'Код завершения программы';


--
-- Name: COLUMN tasks.id_file; Type: COMMENT; Schema: tasks; Owner: postgres
--

COMMENT ON COLUMN tasks.tasks.id_file IS 'UUID файла на сервере';


--
-- Name: COLUMN tasks.id_status; Type: COMMENT; Schema: tasks; Owner: postgres
--

COMMENT ON COLUMN tasks.tasks.id_status IS 'Статус задачи';


--
-- Data for Name: system; Type: TABLE DATA; Schema: system; Owner: postgres
--

INSERT INTO system.system (id_system, available_threads, active, host, threads) VALUES (1, 8, false, '127.0.0.1', 8);


--
-- Data for Name: status; Type: TABLE DATA; Schema: tasks; Owner: postgres
--

INSERT INTO tasks.status (id_status, name) VALUES (3, 'Выполняется');
INSERT INTO tasks.status (id_status, name) VALUES (2, 'Поставлена в очередь');
INSERT INTO tasks.status (id_status, name) VALUES (1, 'Создана');
INSERT INTO tasks.status (id_status, name) VALUES (5, 'Завершена');
INSERT INTO tasks.status (id_status, name) VALUES (4, 'Остановлена');


--
-- Name: create_id_system; Type: SEQUENCE SET; Schema: system; Owner: postgres
--

SELECT pg_catalog.setval('system.create_id_system', 2, true);


--
-- Name: create_id_users; Type: SEQUENCE SET; Schema: system; Owner: postgres
--

SELECT pg_catalog.setval('system.create_id_users', 1, true);


--
-- Name: create_id_order; Type: SEQUENCE SET; Schema: tasks; Owner: postgres
--

SELECT pg_catalog.setval('tasks.create_id_order', 1, true);


--
-- Name: create_id_status; Type: SEQUENCE SET; Schema: tasks; Owner: postgres
--

SELECT pg_catalog.setval('tasks.create_id_status', 1, false);


--
-- Name: create_id_task; Type: SEQUENCE SET; Schema: tasks; Owner: postgres
--

SELECT pg_catalog.setval('tasks.create_id_task', 1, true);


--
-- Name: users pk_users; Type: CONSTRAINT; Schema: system; Owner: postgres
--

ALTER TABLE ONLY system.users
    ADD CONSTRAINT pk_users PRIMARY KEY (id_user);


--
-- Name: system system_pk; Type: CONSTRAINT; Schema: system; Owner: postgres
--

ALTER TABLE ONLY system.system
    ADD CONSTRAINT system_pk PRIMARY KEY (id_system);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: system; Owner: postgres
--

ALTER TABLE ONLY system.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: status ak_status; Type: CONSTRAINT; Schema: tasks; Owner: postgres
--

ALTER TABLE ONLY tasks.status
    ADD CONSTRAINT ak_status UNIQUE (name);


--
-- Name: files files_pkey; Type: CONSTRAINT; Schema: tasks; Owner: postgres
--

ALTER TABLE ONLY tasks.files
    ADD CONSTRAINT files_pkey PRIMARY KEY (id_file);


--
-- Name: order order_pk; Type: CONSTRAINT; Schema: tasks; Owner: postgres
--

ALTER TABLE ONLY tasks."order"
    ADD CONSTRAINT order_pk PRIMARY KEY (id_order);


--
-- Name: status pk_status; Type: CONSTRAINT; Schema: tasks; Owner: postgres
--

ALTER TABLE ONLY tasks.status
    ADD CONSTRAINT pk_status PRIMARY KEY (id_status);


--
-- Name: tasks tasks_pk; Type: CONSTRAINT; Schema: tasks; Owner: postgres
--

ALTER TABLE ONLY tasks.tasks
    ADD CONSTRAINT tasks_pk PRIMARY KEY (id_task);


--
-- Name: system_host_uindex; Type: INDEX; Schema: system; Owner: postgres
--

CREATE UNIQUE INDEX system_host_uindex ON system.system USING btree (host);


--
-- Name: users_guid_uindex; Type: INDEX; Schema: system; Owner: postgres
--

CREATE UNIQUE INDEX users_guid_uindex ON system.users USING btree (guid);


--
-- Name: users_id_user_uindex; Type: INDEX; Schema: system; Owner: postgres
--

CREATE UNIQUE INDEX users_id_user_uindex ON system.users USING btree (id_user);


--
-- Name: users_username_uindex; Type: INDEX; Schema: system; Owner: postgres
--

CREATE UNIQUE INDEX users_username_uindex ON system.users USING btree (username);


--
-- Name: order_id_order_uindex; Type: INDEX; Schema: tasks; Owner: postgres
--

CREATE UNIQUE INDEX order_id_order_uindex ON tasks."order" USING btree (id_order);


--
-- Name: order order_references_task; Type: FK CONSTRAINT; Schema: tasks; Owner: postgres
--

ALTER TABLE ONLY tasks."order"
    ADD CONSTRAINT order_references_task FOREIGN KEY (id_task) REFERENCES tasks.tasks(id_task) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: tasks task_references_file; Type: FK CONSTRAINT; Schema: tasks; Owner: postgres
--

ALTER TABLE ONLY tasks.tasks
    ADD CONSTRAINT task_references_file FOREIGN KEY (id_file) REFERENCES tasks.files(id_file) ON UPDATE RESTRICT ON DELETE RESTRICT;


--
-- Name: tasks task_references_status; Type: FK CONSTRAINT; Schema: tasks; Owner: postgres
--

ALTER TABLE ONLY tasks.tasks
    ADD CONSTRAINT task_references_status FOREIGN KEY (id_status) REFERENCES tasks.status(id_status) ON UPDATE RESTRICT ON DELETE RESTRICT;


--
-- Name: tasks task_references_system; Type: FK CONSTRAINT; Schema: tasks; Owner: postgres
--

ALTER TABLE ONLY tasks.tasks
    ADD CONSTRAINT task_references_system FOREIGN KEY (running_on) REFERENCES system.system(id_system) ON UPDATE SET NULL ON DELETE SET NULL;


--
-- Name: tasks task_references_user; Type: FK CONSTRAINT; Schema: tasks; Owner: postgres
--

ALTER TABLE ONLY tasks.tasks
    ADD CONSTRAINT task_references_user FOREIGN KEY (id_user) REFERENCES system.users(id_user) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

