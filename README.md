# Центральная библиотека города

## 1. Общая информация

* **Название проекта / страницы:** Центральная городская библиотека
* **Описание:**
  Страница представляет собой официальный веб-сайт Центральной городской библиотеки. Основные функции:

  * предоставление информации о библиотеке, её фонде и услугах;
  * навигация по разделам сайта;
  * отображение новостей и афиш мероприятий;
  * форма для отправки пользовательских данных;
  * информационные баннеры и контактные данные.
* **Используемые технологии:**

  * HTML5 для структуры страницы;
  * CSS3 для стилизации и адаптивного дизайна;
  * Django Template Language для динамических данных (`{% load static %}`, `{% url %}`, `{{ current_name }}`);
  * базовые элементы форм (`<form>`), ссылки (`<a>`), списки (`<ul>`/`<li>`).

---

## 2. Структура HTML

### 2.1 Контейнер страницы

* **Назначение:** Основной обёрточный блок для всех элементов страницы.
* **Теги:** `<div class="container">`
* **Родитель:** `<body>`
* **Дочерние элементы:** `<header>`, `.main-content`, `<footer>`
* **Пример HTML:**

```html
<div class="container">
  <header> ... </header>
  <div class="main-content"> ... </div>
  <footer> ... </footer>
</div>
```

### 2.2 Header (шапка сайта)

* **Назначение:** Отображение названия библиотеки и краткой информации.
* **Теги:** `<header>`, `<h1>`, `<p>`
* **Дочерние элементы:** `<h1>`, `<p>`
* **Пример HTML:**

```html
<header>
  <h1>Центральная городская библиотека</h1>
  <p>Культурный и информационный центр города с более чем 100-летней историей</p>
</header>
```

### 2.3 Main content (основная часть)

* **Назначение:** Основная информационная зона с тремя колонками.
* **Теги:** `<div class="main-content">`
* **Дочерние элементы:** `.left-sidebar`, `.center-content`, `.right-sidebar`
* **Пример HTML:**

```html
<div class="main-content">
  <aside class="left-sidebar"> ... </aside>
  <main class="center-content"> ... </main>
  <aside class="right-sidebar"> ... </aside>
</div>
```

#### 2.3.1 Left sidebar (левая колонка)

* **Назначение:** Навигация по разделам сайта.
* **Теги:** `<aside>`, `<h2>`, `<ul>`, `<li>`, `<a>`
* **Пример HTML:**

```html
<aside class="left-sidebar">
  <h2>Разделы сайта</h2>
  <ul class="nav-links">
    <li><a href="#about">О библиотеке</a></li>
    <li><a href="#poster">Афиша</a></li>
    ...
  </ul>
</aside>
```

#### 2.3.2 Center content (центральная колонка)

* **Назначение:** Основная информация о библиотеке, приветствие, особенности, форма.
* **Теги:** `<main>`, `<h2>`, `<div>`, `<h3>`, `<p>`, `<form>`, `<input>`, `<label>`
* **Пример HTML:**

```html
<main class="center-content">
  <h2>Добро пожаловать в нашу библиотеку</h2>
  <div class="welcome-text">
    <p>...</p>
    <p>...</p>
  </div>
  <div class="library-image">Читальный зал Центральной библиотеки</div>
  <div class="features">
    <div class="feature"> ... </div>
    <div class="feature"> ... </div>
    ...
  </div>
</main>
```

#### 2.3.3 Right sidebar (правая колонка)

* **Назначение:** Новости и баннеры.
* **Теги:** `<aside>`, `<section>`, `<div>`, `<h2>`, `<h3>`, `<a>`, `<p>`
* **Пример HTML:**

```html
<aside class="right-sidebar">
  <section class="news-section"> ... </section>
  <div class="banner"> ... </div>
  <div class="banner"> ... </div>
</aside>
```

### 2.4 Footer (подвал страницы)

* **Назначение:** Контакты, полезные ссылки, соцсети, авторские права.
* **Теги:** `<footer>`, `<div>`, `<h3>`, `<a>`, `<p>`
* **Пример HTML:**

```html
<footer>
  <div class="footer-content">
    <div class="footer-section"> ... </div>
    <div class="footer-section"> ... </div>
    <div class="footer-section"> ... </div>
  </div>
  <div class="copyright">&copy; 2023 Центральная городская библиотека</div>
</footer>
```

---

## 3. CSS документация

### 3.1 Общие селекторы

```css
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
}
```

* **Назначение:** Сброс отступов, установка универсальной модели box-sizing и шрифта.
* **Влияние:** Все элементы наследуют указанный шрифт и размеры без лишних отступов.

```css
body {
  background-color: #f5f5f5;
  color: #333;
  line-height: 1.6;
}
```

* **Назначение:** Основной фон и цвет текста для читаемости.
* **Совет:** Цвет текста контрастирует с фоном для улучшенной доступности.

### 3.2 Header

```css
header {
  background: linear-gradient(135deg, #2c3e50, #4a6491);
  color: white;
  padding: 20px;
  text-align: center;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
```

* **Назначение:** Визуально выделяет шапку сайта с градиентным фоном.
* **Взаимодействие:** Текст белого цвета хорошо виден на градиенте.

### 3.3 Sidebars

```css
.left-sidebar {
  flex: 0 0 220px;
  background-color: #fff;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
}
```

* **Назначение:** Отдельная колонка для навигации, визуально отделена от основного контента.
* **Взаимодействие:** Совместно с `.nav-links` создаёт интерактивное меню.

```css
.right-sidebar {
  flex: 0 0 300px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}
```

* **Назначение:** Правая колонка с вертикальным расположением новостей и баннеров.

### 3.4 Центр контента

```css
.center-content {
  flex: 1;
  background-color: #fff;
  border-radius: 8px;
  padding: 25px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
}
```

* **Назначение:** Основная область с информацией о библиотеке.

### 3.5 Функциональные блоки

```css
.features {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
}
.feature {
  background-color: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
  border-left: 4px solid #4a6491;
}
```

* **Назначение:** Сетка блоков с ключевой информацией (часы работы, контакты, новости).
* **Совет:** `auto-fill` позволяет адаптировать блоки под ширину экрана.

### 3.6 Баннеры и новости

```css
.banner, .news-section {
  background-color: #fff;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
}
.banner-placeholder {
  height: 150px;
  background-color: #e9ecef;
  display: flex;
  align-items: center;
  justify-content: center;
}
```

* **Назначение:** Отдельные информационные блоки с визуальной структурой.

### 3.7 Footer

```css
footer {
  background-color: #2c3e50;
  color: white;
  padding: 30px 20px;
  text-align: center;
}
```

* **Назначение:** Визуально отделяет нижнюю часть страницы и содержит важные ссылки и контакты.

---

## 4. Повторяющиеся компоненты

* **`.feature`** — одинаковый дизайн блоков с информацией.
* **`.banner` и `.banner-placeholder`** — стандартизированный вид баннеров.
* **`.news-item`** — единый стиль для новостей.
* **`.footer-section`** — повторяющийся блок информации в подвале.

**Пример с переменными:**

```html
<div class="feature">
  <h3>{{ заголовок }}</h3>
  <p>{{ текст }}</p>
</div>
```

---

## 5. Общие стили страницы

* **Цветовая схема:**

  * Фон страницы: `#f5f5f5`
  * Фон блоков: белый `#fff`
  * Основной текст: `#333`
  * Акценты (границы, ссылки): `#4a6491`
* **Шрифты:** `"Segoe UI", Tahoma, Geneva, Verdana, sans-serif`
* **Размеры и отступы:** Паддинги 20–25px, бордюры 8px
* **Сетка:** `flex` для основных колонок, `grid` для `.features`
* **Адаптивность:**

  * @media 1100px: колонки оборачиваются, правая колонка в ряд
  * @media 768px: колонки идут вертикально, footer тоже

---

# Визуальная карта страницы

```
<body>
 └── .container
      ├── <header>
      │     ├── <h1>Центральная городская библиотека</h1>
      │     └── <p>Культурный и информационный центр города...</p>
      │
      ├── .main-content
      │     ├── .left-sidebar
      │     │     ├── <h2>Разделы сайта</h2>
      │     │     └── .nav-links (ul)
      │     │           ├── <li><a href="#about">О библиотеке</a></li>
      │     │           ├── <li><a href="#poster">Афиша</a></li>
      │     │           └── ... (остальные ссылки)
      │     │
      │     ├── .center-content
      │     │     ├── <h2>Добро пожаловать в нашу библиотеку</h2>
      │     │     ├── .welcome-text
      │     │     │     ├── <p>Текст приветствия 1</p>
      │     │     │     └── <p>Текст приветствия 2</p>
      │     │     ├── .library-image
      │     │     └── .features
      │     │           ├── .feature (Часы работы)
      │     │           ├── .feature (Контакты)
      │     │           ├── .feature (Статистика)
      │     │           ├── .feature (Новости)
      │     │           └── .feature (Forms)
      │     │
      │     └── .right-sidebar
      │           ├── .news-section
      │           │     ├── <h2>Последние новости</h2>
      │           │     ├── .news-item
      │           │     │     ├── .news-date
      │           │     │     ├── .news-title
      │           │     │     └── <p>Описание новости</p>
      │           │     └── ... (остальные новости)
      │           │
      │           ├── .banner (Книжный клуб)
      │           │     ├── <h3>Присоединяйтесь к книжному клубу</h3>
      │           │     └── .banner-placeholder
      │           │
      │           └── .banner (Электронный каталог)
      │                 ├── <h3>Электронный каталог</h3>
      │                 └── .banner-placeholder
      │
      └── <footer>
            ├── .footer-content
            │     ├── .footer-section (Контакты)
            │     ├── .footer-section (Полезные ссылки)
            │     └── .footer-section (Социальные сети)
            │
            └── .copyright
```

---

### Легенда

1. **.container** — основной обёрточный блок, все элементы внутри.
2. **Header** — визуально выделенный блок шапки сайта.
3. **.main-content** — три колонки:

   * `.left-sidebar` — навигация;
   * `.center-content` — приветствие, информация, формы;
   * `.right-sidebar` — новости и баннеры.
4. **Footer** — нижняя часть страницы, разделённая на секции и отдельный блок авторских прав.


