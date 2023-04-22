from sqlalchemy import (Boolean, Column, ForeignKey, DateTime,
                        Integer, SmallInteger, String, text)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata

# -------------------------- SCHEMA system ------------------------------------


class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'schema': 'system', 'comment': 'Таблица пользователей'}

    id_user = Column(Integer, primary_key=True, unique=True, server_default=text("nextval('system.create_id_users'::regclass)"), comment='ИД пользователя')
    first_name = Column(String(100), nullable=False, comment='Имя')
    last_name = Column(String(100), nullable=False, comment='Фамилия')
    email = Column(String(100), nullable=False, comment='Email')
    is_staff = Column(Boolean, nullable=False, server_default=text("false"), comment='Флаг "сотрудник"')
    username = Column(String(50), nullable=False, unique=True, comment='Имя пользователя')
    password = Column(String(), nullable=False, comment='Пароль')
    guid = Column(UUID, nullable=False, unique=True, comment='Уникальный идентификатор')


class System(Base):
    __tablename__ = 'system'
    __table_args__ = {'schema': 'system', 'comment': 'Таблица с описанием виртуальных систем'}

    id_system = Column(Integer, primary_key=True, server_default=text("nextval('system.create_id_system'::regclass)"))
    threads = Column(SmallInteger, nullable=False, comment='Количество ядер системы')
    available_threads = Column(SmallInteger, comment='Доступное количество ядер системы')
    active = Column(Boolean, nullable=False, server_default=text("false"), comment='Флаг "Состояние машины"')
    host = Column(String(15), unique=True, comment='Хост для подключения к машине')


# -------------------------- SCHEMA tasks -------------------------------------


class Status(Base):
    __tablename__ = 'status'
    __table_args__ = {'schema': 'tasks', 'comment': 'Классификатор статусов задачи'}

    id_status = Column(Integer, primary_key=True, server_default=text("nextval('tasks.create_id_status'::regclass)"), comment='ИД статуса')
    name = Column(String, nullable=False, unique=True, comment='Наименование статуса задачи')


class File(Base):
    __tablename__ = 'files'
    __table_args__ = {'schema': 'tasks', 'comment': 'Таблица для хранения информации о файлах'}

    id_file = Column(UUID, primary_key=True, comment='UUID Файла')
    file_path = Column(String, nullable=False, comment='Расположение файла')
    readable_file_name = Column(String, nullable=False, comment='Человеко-читаемое имя файла')


class Task(Base):
    __tablename__ = 'tasks'
    __table_args__ = {'schema': 'tasks', 'comment': 'Таблица с задачами для суперкомпьютера'}

    id_task = Column(Integer, primary_key=True, server_default=text("nextval('tasks.create_id_task'::regclass)"), comment='ИД задачи')
    params = Column(String, comment='Параметры исполнения')
    num_threads = Column(Integer, nullable=False, comment='Количество потоков исполнения')
    priority = Column(Integer, nullable=False, server_default=text("1"), comment='Приоритет исполнения задачи')
    running_on = Column(ForeignKey('system.system.id_system', ondelete='SET NULL', onupdate='SET NULL'), comment='ИД исполняющей системы')
    id_user = Column(ForeignKey('system.users.id_user', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, comment='ИД Пользователя')
    id_status = Column(ForeignKey('tasks.status.id_status', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=False, comment='Статус задачи')
    process_id = Column(Integer, comment='ИД процесса исполнения')
    created_at = Column(DateTime, nullable=False, comment='Время создания')
    output = Column(String, comment='Вывод программы')
    errors = Column(String, comment='Ошибки программы')
    exitcode = Column(Integer, comment='Код завершения программы')
    id_file = Column(ForeignKey('tasks.files.id_file', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=False, comment='UUID файла на сервере')

    file = relationship('File')
    user = relationship('User')
    system = relationship('System')
    status = relationship('Status')


class Order(Base):
    __tablename__ = 'order'
    __table_args__ = {'schema': 'tasks', 'comment': 'Таблица-очередь'}

    id_order = Column(Integer, primary_key=True, unique=True, server_default=text("nextval('tasks.create_id_order'::regclass)"), comment='ИД очереди')
    id_task = Column(ForeignKey('tasks.tasks.id_task', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, comment='ИД Задачи')
    order_number = Column(Integer, unique=True, comment='Номер в очереди')

    task = relationship('Task')
