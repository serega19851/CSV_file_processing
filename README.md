# CSV File Processing

**Универсальный CLI-обработчик CSV-файлов с фильтрацией, агрегацией и сортировкой.**

---

## Быстрый старт

### 1. Клонируйте репозиторий и перейдите в папку проекта

```bash
git clone <repo-url>
cd CSV_file_processing
```

### 2. Создайте и активируйте виртуальное окружение

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Установите зависимости

```bash
pip install -r requirements.txt
```

### 4. Запустите тесты (опционально)

```bash
pytest -v
```

---

## Использование

> **Примечание:** тестовый файл `phones.csv` уже лежит в корневой папке проекта — можно сразу запускать примеры ниже.

```bash
python main.py <файл.csv> [--where "условие"] [--aggregate "столбец=функция"] [--order-by "столбец=asc|desc"]
```

**Примеры:**

- Показать все данные:

  ```bash
  python main.py phones.csv
  ```

- Фильтрация:

  ```bash
  python main.py phones.csv --where "price>500"
  python main.py phones.csv --where "name=Apple"
  ```

- Агрегация:

  ```bash
  python main.py phones.csv --aggregate "price=avg"
  python main.py phones.csv --aggregate "rating=max"
  ```

- Сортировка:
  ```bash
  python main.py phones.csv --order-by "price=asc"
  python main.py phones.csv --order-by "brand=desc"
  ```

---

## Пример вывода

```
+------------------+---------+---------+----------+
| name             | brand   |   price |   rating |
+==================+=========+=========+==========+
| redmi note 12    | xiaomi  |     199 |      4.6 |
| poco x5 pro      | xiaomi  |     299 |      4.4 |
| iphone 15 pro    | apple   |     999 |      4.9 |
| galaxy s23 ultra | samsung |    1199 |      4.8 |
+------------------+---------+---------+----------+
```
