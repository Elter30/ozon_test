# Test task for Ozon

## Скрипт для получения самого высокого героя

Python скрипт для поиска самого высокого героя по заданным параметрам

 - Пол
 - Наличие работы

### Установка и запуск

#### 1. Установка зависимостей

```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### 2. Запуск скрипта

```
cd src
python script.py <gender> <is_work>
```
 - gender - Значение: Male/Female
 - is_work - Значение: 0/1

Результат: кортеж вида (id, name)

#### 3. Запуск тестов

Из корневой директории проекта

```
python -m pytest
```