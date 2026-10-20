# Карта проекта RSL

## Обзор

| Параметр | Значение |
|-----------|-----------|
| **Тип** | Django веб-приложение (сайт библиотеки) |
| **Стек** | Python 3.14, Django 5.2.8, SQLite3, HTML5, CSS3, vanilla JS |
| **Язык UI** | Русский |
| **Режим** | Разработка (DEBUG=True) |

---

## Структура каталогов

```
rsl/
├── manage.py                    # Точка входа Django CLI
├── db.sqlite3                   # База данных SQLite
├── requirements.txt             # Зависимости (Django 5.2.8, crispy-forms, pillow и др.)
├── rsl/                         # Конфигурация проекта Django
│   ├── settings.py              # Настройки (БД, приложения, middleware, шаблоны)
│   ├── urls.py                  # Корневая маршрутизация URL
│   ├── wsgi.py / asgi.py        # WSGI/ASGI точки входа
│
├── hello/                       # Основное приложение (статьи, комментарии)
│   ├── models.py                # Модели: Article, Comment
│   ├── views.py                 # index, news_one..four, news_page, CRUD комментариев (AJAX)
│   ├── forms.py                 # CommentForm (автор, email, текст)
│   ├── admin.py                 # Регистрация моделей в админке
│   ├── context_processors.py    # latest_news — последние 4 статьи во все шаблоны
│   ├── migrations/              # 11 файлов миграций
│   └── static/hello/            # CSS, JS (пусто), изображения
│
├── authorization/               # Аутентификация пользователей
│   ├── views.py                 # register, home, profile, ProtectedView
│   ├── forms.py                 # RegisterUserForm (расширяет UserCreationForm)
│   ├── urls.py                  # login/, logout/, register/, protected/, profile/
│   └── templates/               # registration/login, register, profile, protected
│
├── images/                      # Обработка изображений
│   ├── models.py                # Image (uuid, original, preview, thumb, webp)
│   ├── services.py              # ImageService — генерация версий через Pillow
│   ├── validators.py            # Валидация изображений (макс. 5MB)
│   └── views.py                 # Заглушка
│
├── analytics/                   # Заглушка (не в INSTALLED_APPS)
├── events/                      # Заглушка (не в INSTALLED_APPS)
│
├── media/                       # Загруженные файлы
│   ├── articles/                # Изображения статей
│   ├── news_images/             # Изображения новостей
│   └── uploads/                 # Сгенерированные версии (год/месяц/UUID/)
│
├── static/hello/                # Статика проекта (дублирует hello/static)
│   ├── css/styles.css
│   └── images/pic01..11.jpg
│
└── templates/                   # Шаблоны
    ├── base.html                # Базовый шаблон (header, сайдбары, footer)
    ├── index.html               # Главная страница
    ├── news-1..4.html           # Статические новости
    ├── news_base.html           # База динамической статьи + комментарии (AJAX)
    ├── news_page.html           # Динамическая статья (extends news_base)
    └── includes/latest_news.html
```

---

## Маршрутизация URL

| URL | View | Назначение |
|-----|------|------------|
| `/` | `hello.views.index` | Главная |
| `/admin/` | Django admin | Админ-панель |
| `/article/1..4/` | `news_one..four` | Статические новости |
| `/news/<pk>/` | `news_page` | Динамическая статья |
| `/news/<pk>/add-comment/` | `add_comment` | Добавить комментарий |
| `/news/<pk>/delete-comment/` | `delete_comment` | Удалить (soft-delete) |
| `/comment/edit/<pk>/` | `edit_comment` | AJAX-редактирование |
| `/auth/` | include authorization.urls | Модуль авторизации |
| `/auth/login/`, `/auth/logout/`, `/auth/register/`, `/auth/profile/`, `/auth/protected/` | Разные | Аутентификация |

---

## Ключевые паттерны

1. **Django MVT** — стандартная архитектура (Models → Views → Templates)
2. **Мульти-app структура** — 3 активных приложения (`hello`, `authorization`, `images`)
3. **Наследование шаблонов** — `news_page` → `news_base` → `base.html`
4. **Context processors** — глобальная инъекция последних статей
5. **Пайплайн обработки изображений** — Pillow генерирует preview/thumb/webp
6. **Soft-delete комментариев** — `approved = False` вместо удаления
7. **AJAX-редактирование** — fetch API + JSON response
8. **Гибрид контента** — статические HTML + динамические статьи из БД
9. **Адаптивный CSS** — Flexbox + Grid, breakpoints на 1100px и 768px
10. **Смешанная аутентификация** — FBV для register/profile, CBV для protected

---

## Замечания

- **Отсутствует** `hello/js/main.js` ( referenced в шаблоне, но нет на диске)
- **Пустые тесты** — все `tests.py` — заглушки
- **Не в INSTALLED_APPS** — `analytics`, `events`
- **Дублирование** статики (`hello/static/` и `rsl/static/`)
- **Потенциальный баг** — `CommentEditForm` используется в `news_page`, но не импортирован в `views.py`
- **SECRET_KEY** захардкожен, `DEBUG=True` — не готово к продакшену