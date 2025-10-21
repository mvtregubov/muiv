-- SQL-дамп демонстрационной базы данных Django-проекта по C++
BEGIN TRANSACTION;
CREATE TABLE app_answer (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question_id INTEGER NOT NULL REFERENCES app_question(id) ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED,
        text VARCHAR(255) NOT NULL,
        is_correct BOOLEAN NOT NULL
    );
INSERT INTO "app_answer" VALUES(1,1,'*',1);
INSERT INTO "app_answer" VALUES(2,1,'&',0);
INSERT INTO "app_answer" VALUES(3,1,'->',0);
INSERT INTO "app_answer" VALUES(4,1,'[]',0);
INSERT INTO "app_answer" VALUES(5,2,'<memory>',1);
INSERT INTO "app_answer" VALUES(6,2,'<vector>',0);
INSERT INTO "app_answer" VALUES(7,2,'<optional>',0);
INSERT INTO "app_answer" VALUES(8,2,'<thread>',0);
INSERT INTO "app_answer" VALUES(9,3,'concept',1);
INSERT INTO "app_answer" VALUES(10,3,'module',0);
INSERT INTO "app_answer" VALUES(11,3,'requires',0);
INSERT INTO "app_answer" VALUES(12,3,'constexpr',0);
INSERT INTO "app_answer" VALUES(13,4,'std::jthread',1);
INSERT INTO "app_answer" VALUES(14,4,'std::future',0);
INSERT INTO "app_answer" VALUES(15,4,'std::packaged_task',0);
INSERT INTO "app_answer" VALUES(16,4,'std::async',0);
CREATE TABLE app_course (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title VARCHAR(200) NOT NULL,
        description TEXT NOT NULL,
        author_id INTEGER NOT NULL REFERENCES app_user(id) ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED,
        published DATE NOT NULL
    );
INSERT INTO "app_course" VALUES(1,'Основы языка C++','Базовый курс, охватывающий синтаксис, типы данных и управление памятью.',1,'2023-09-01');
INSERT INTO "app_course" VALUES(2,'Современный C++','Продвинутый курс по стандартам C++17/20, шаблонам и метапрограммированию.',1,'2023-11-10');
CREATE TABLE app_lesson (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        course_id INTEGER NOT NULL REFERENCES app_course(id) ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED,
        title VARCHAR(200) NOT NULL,
        content TEXT NOT NULL,
        "order" INTEGER NOT NULL
    );
INSERT INTO "app_lesson" VALUES(1,1,'Введение','История языка C++ и области применения.',1);
INSERT INTO "app_lesson" VALUES(2,1,'Переменные и типы','Обзор встроенных типов, области видимости и инициализации.',2);
INSERT INTO "app_lesson" VALUES(3,1,'Управление памятью','Стек, куча и умные указатели.',3);
INSERT INTO "app_lesson" VALUES(4,2,'Стандартная библиотека','Контейнеры, алгоритмы и итераторы.',1);
INSERT INTO "app_lesson" VALUES(5,2,'Параллельность','Средства многопоточности в стандарте C++.',2);
CREATE TABLE app_question (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        quiz_id INTEGER NOT NULL REFERENCES app_quiz(id) ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED,
        text TEXT NOT NULL
    );
INSERT INTO "app_question" VALUES(1,1,'Какой оператор используется для разыменования указателя?');
INSERT INTO "app_question" VALUES(2,1,'Какой заголовок необходимо подключить для работы с std::unique_ptr?');
INSERT INTO "app_question" VALUES(3,2,'Какой ключевое слово включает поддержку концептов в C++20?');
INSERT INTO "app_question" VALUES(4,2,'Какой класс потока используется для конкурентного выполнения задач?');
CREATE TABLE app_quiz (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        course_id INTEGER NOT NULL REFERENCES app_course(id) ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED,
        title VARCHAR(200) NOT NULL,
        duration_minutes INTEGER NOT NULL
    );
INSERT INTO "app_quiz" VALUES(1,1,'Тест по основам',15);
INSERT INTO "app_quiz" VALUES(2,2,'Тест по современному C++',20);
CREATE TABLE app_result (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL REFERENCES app_user(id) ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED,
        quiz_id INTEGER NOT NULL REFERENCES app_quiz(id) ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED,
        score INTEGER NOT NULL,
        created_at DATETIME NOT NULL
    );
INSERT INTO "app_result" VALUES(1,1,1,2,'2024-01-15 12:00:00');
INSERT INTO "app_result" VALUES(2,1,2,1,'2024-01-15 12:00:00');
CREATE TABLE app_user (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        password VARCHAR(128) NOT NULL,
        last_login DATETIME NULL,
        is_superuser BOOLEAN NOT NULL,
        username VARCHAR(150) NOT NULL UNIQUE,
        first_name VARCHAR(150) NOT NULL,
        last_name VARCHAR(150) NOT NULL,
        email VARCHAR(254) NOT NULL,
        is_staff BOOLEAN NOT NULL,
        is_active BOOLEAN NOT NULL,
        date_joined DATETIME NOT NULL,
        bio TEXT NOT NULL,
        organization VARCHAR(255) NOT NULL
    );
INSERT INTO "app_user" VALUES(1,'pbkdf2_sha256$600000$muivdemo$gBogx5l6KvxGcJR12LM0kP8H519k+VtiIUiK4GTOxQo=',NULL,1,'admin','Администратор','Портала','admin@example.com',1,1,'2024-01-15 12:00:00','Руководитель программы C++.','МУИВ');
CREATE TABLE app_user_groups (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL REFERENCES app_user(id) DEFERRABLE INITIALLY DEFERRED,
        group_id INTEGER NOT NULL REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED,
        UNIQUE(user_id, group_id)
    );
CREATE TABLE app_user_user_permissions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL REFERENCES app_user(id) DEFERRABLE INITIALLY DEFERRED,
        permission_id INTEGER NOT NULL REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED,
        UNIQUE(user_id, permission_id)
    );
CREATE TABLE auth_group (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(150) NOT NULL UNIQUE
    );
CREATE TABLE auth_group_permissions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        group_id INTEGER NOT NULL REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED,
        permission_id INTEGER NOT NULL REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED,
        UNIQUE(group_id, permission_id)
    );
CREATE TABLE auth_permission (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(255) NOT NULL,
        content_type_id INTEGER NOT NULL REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED,
        codename VARCHAR(100) NOT NULL,
        UNIQUE(content_type_id, codename)
    );
INSERT INTO "auth_permission" VALUES(1,'Can add log entry',1,'add_logentry');
INSERT INTO "auth_permission" VALUES(2,'Can change log entry',1,'change_logentry');
INSERT INTO "auth_permission" VALUES(3,'Can delete log entry',1,'delete_logentry');
INSERT INTO "auth_permission" VALUES(4,'Can view log entry',1,'view_logentry');
INSERT INTO "auth_permission" VALUES(5,'Can add permission',2,'add_permission');
INSERT INTO "auth_permission" VALUES(6,'Can change permission',2,'change_permission');
INSERT INTO "auth_permission" VALUES(7,'Can delete permission',2,'delete_permission');
INSERT INTO "auth_permission" VALUES(8,'Can view permission',2,'view_permission');
INSERT INTO "auth_permission" VALUES(9,'Can add group',3,'add_group');
INSERT INTO "auth_permission" VALUES(10,'Can change group',3,'change_group');
INSERT INTO "auth_permission" VALUES(11,'Can delete group',3,'delete_group');
INSERT INTO "auth_permission" VALUES(12,'Can view group',3,'view_group');
INSERT INTO "auth_permission" VALUES(13,'Can add content type',4,'add_contenttype');
INSERT INTO "auth_permission" VALUES(14,'Can change content type',4,'change_contenttype');
INSERT INTO "auth_permission" VALUES(15,'Can delete content type',4,'delete_contenttype');
INSERT INTO "auth_permission" VALUES(16,'Can view content type',4,'view_contenttype');
INSERT INTO "auth_permission" VALUES(17,'Can add session',5,'add_session');
INSERT INTO "auth_permission" VALUES(18,'Can change session',5,'change_session');
INSERT INTO "auth_permission" VALUES(19,'Can delete session',5,'delete_session');
INSERT INTO "auth_permission" VALUES(20,'Can view session',5,'view_session');
INSERT INTO "auth_permission" VALUES(21,'Can add user',6,'add_user');
INSERT INTO "auth_permission" VALUES(22,'Can change user',6,'change_user');
INSERT INTO "auth_permission" VALUES(23,'Can delete user',6,'delete_user');
INSERT INTO "auth_permission" VALUES(24,'Can view user',6,'view_user');
INSERT INTO "auth_permission" VALUES(25,'Can add course',7,'add_course');
INSERT INTO "auth_permission" VALUES(26,'Can change course',7,'change_course');
INSERT INTO "auth_permission" VALUES(27,'Can delete course',7,'delete_course');
INSERT INTO "auth_permission" VALUES(28,'Can view course',7,'view_course');
INSERT INTO "auth_permission" VALUES(29,'Can add lesson',8,'add_lesson');
INSERT INTO "auth_permission" VALUES(30,'Can change lesson',8,'change_lesson');
INSERT INTO "auth_permission" VALUES(31,'Can delete lesson',8,'delete_lesson');
INSERT INTO "auth_permission" VALUES(32,'Can view lesson',8,'view_lesson');
INSERT INTO "auth_permission" VALUES(33,'Can add quiz',9,'add_quiz');
INSERT INTO "auth_permission" VALUES(34,'Can change quiz',9,'change_quiz');
INSERT INTO "auth_permission" VALUES(35,'Can delete quiz',9,'delete_quiz');
INSERT INTO "auth_permission" VALUES(36,'Can view quiz',9,'view_quiz');
INSERT INTO "auth_permission" VALUES(37,'Can add question',10,'add_question');
INSERT INTO "auth_permission" VALUES(38,'Can change question',10,'change_question');
INSERT INTO "auth_permission" VALUES(39,'Can delete question',10,'delete_question');
INSERT INTO "auth_permission" VALUES(40,'Can view question',10,'view_question');
INSERT INTO "auth_permission" VALUES(41,'Can add answer',11,'add_answer');
INSERT INTO "auth_permission" VALUES(42,'Can change answer',11,'change_answer');
INSERT INTO "auth_permission" VALUES(43,'Can delete answer',11,'delete_answer');
INSERT INTO "auth_permission" VALUES(44,'Can view answer',11,'view_answer');
INSERT INTO "auth_permission" VALUES(45,'Can add result',12,'add_result');
INSERT INTO "auth_permission" VALUES(46,'Can change result',12,'change_result');
INSERT INTO "auth_permission" VALUES(47,'Can delete result',12,'delete_result');
INSERT INTO "auth_permission" VALUES(48,'Can view result',12,'view_result');
CREATE TABLE django_admin_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        action_time DATETIME NOT NULL,
        object_id TEXT NULL,
        object_repr VARCHAR(200) NOT NULL,
        action_flag INTEGER NOT NULL,
        change_message TEXT NOT NULL,
        content_type_id INTEGER REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED,
        user_id INTEGER NOT NULL REFERENCES app_user(id) DEFERRABLE INITIALLY DEFERRED
    );
CREATE TABLE django_content_type (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        app_label VARCHAR(100) NOT NULL,
        model VARCHAR(100) NOT NULL,
        UNIQUE(app_label, model)
    );
INSERT INTO "django_content_type" VALUES(1,'admin','logentry');
INSERT INTO "django_content_type" VALUES(2,'auth','permission');
INSERT INTO "django_content_type" VALUES(3,'auth','group');
INSERT INTO "django_content_type" VALUES(4,'contenttypes','contenttype');
INSERT INTO "django_content_type" VALUES(5,'sessions','session');
INSERT INTO "django_content_type" VALUES(6,'app','user');
INSERT INTO "django_content_type" VALUES(7,'app','course');
INSERT INTO "django_content_type" VALUES(8,'app','lesson');
INSERT INTO "django_content_type" VALUES(9,'app','quiz');
INSERT INTO "django_content_type" VALUES(10,'app','question');
INSERT INTO "django_content_type" VALUES(11,'app','answer');
INSERT INTO "django_content_type" VALUES(12,'app','result');
CREATE TABLE django_migrations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        app VARCHAR(255) NOT NULL,
        name VARCHAR(255) NOT NULL,
        applied DATETIME NOT NULL
    );
INSERT INTO "django_migrations" VALUES(1,'contenttypes','0001_initial','2024-01-15 12:00:00');
INSERT INTO "django_migrations" VALUES(2,'auth','0001_initial','2024-01-15 12:00:00');
INSERT INTO "django_migrations" VALUES(3,'admin','0001_initial','2024-01-15 12:00:00');
INSERT INTO "django_migrations" VALUES(4,'app','0001_initial','2024-01-15 12:00:00');
INSERT INTO "django_migrations" VALUES(5,'sessions','0001_initial','2024-01-15 12:00:00');
INSERT INTO "django_migrations" VALUES(6,'contenttypes','0002_remove_content_type_name','2024-01-15 12:00:00');
INSERT INTO "django_migrations" VALUES(7,'auth','0002_alter_permission_name_max_length','2024-01-15 12:00:00');
INSERT INTO "django_migrations" VALUES(8,'auth','0003_alter_user_email_max_length','2024-01-15 12:00:00');
INSERT INTO "django_migrations" VALUES(9,'auth','0004_alter_user_username_opts','2024-01-15 12:00:00');
INSERT INTO "django_migrations" VALUES(10,'auth','0005_alter_user_last_login_null','2024-01-15 12:00:00');
INSERT INTO "django_migrations" VALUES(11,'auth','0006_require_contenttypes_0002','2024-01-15 12:00:00');
INSERT INTO "django_migrations" VALUES(12,'auth','0007_alter_validators_add_error_messages','2024-01-15 12:00:00');
INSERT INTO "django_migrations" VALUES(13,'auth','0008_alter_user_username_max_length','2024-01-15 12:00:00');
INSERT INTO "django_migrations" VALUES(14,'auth','0009_alter_user_last_name_max_length','2024-01-15 12:00:00');
INSERT INTO "django_migrations" VALUES(15,'auth','0010_alter_group_name_max_length','2024-01-15 12:00:00');
INSERT INTO "django_migrations" VALUES(16,'auth','0011_update_proxy_permissions','2024-01-15 12:00:00');
INSERT INTO "django_migrations" VALUES(17,'auth','0012_alter_user_first_name_max_length','2024-01-15 12:00:00');
CREATE TABLE django_session (
        session_key VARCHAR(40) NOT NULL PRIMARY KEY,
        session_data TEXT NOT NULL,
        expire_date DATETIME NOT NULL
    );
CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON django_admin_log(content_type_id);
CREATE INDEX django_admin_log_user_id_c564eba6 ON django_admin_log(user_id);
CREATE INDEX django_session_expire_date_a5c62663 ON django_session(expire_date);
CREATE INDEX app_course_author_id_idx ON app_course(author_id);
CREATE INDEX app_lesson_course_id_idx ON app_lesson(course_id);
CREATE INDEX app_quiz_course_id_idx ON app_quiz(course_id);
CREATE INDEX app_question_quiz_id_idx ON app_question(quiz_id);
CREATE INDEX app_answer_question_id_idx ON app_answer(question_id);
CREATE INDEX app_result_user_id_idx ON app_result(user_id);
CREATE INDEX app_result_quiz_id_idx ON app_result(quiz_id);
DELETE FROM "sqlite_sequence";
INSERT INTO "sqlite_sequence" VALUES('django_content_type',12);
INSERT INTO "sqlite_sequence" VALUES('auth_permission',48);
INSERT INTO "sqlite_sequence" VALUES('app_user',1);
INSERT INTO "sqlite_sequence" VALUES('app_course',2);
INSERT INTO "sqlite_sequence" VALUES('app_lesson',5);
INSERT INTO "sqlite_sequence" VALUES('app_quiz',2);
INSERT INTO "sqlite_sequence" VALUES('app_question',4);
INSERT INTO "sqlite_sequence" VALUES('app_answer',16);
INSERT INTO "sqlite_sequence" VALUES('app_result',2);
INSERT INTO "sqlite_sequence" VALUES('django_migrations',17);
COMMIT;
