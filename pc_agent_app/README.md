# General Desktop Agent (Windows 10) — пошаговая установка с нуля

Ниже инструкция для случая, когда у вас **ещё нет проекта на компьютере**.

---

## 1) Что установить заранее

1. **Git for Windows**  
   https://git-scm.com/download/win
2. **Python 3.10+**  
   https://www.python.org/downloads/windows/

Проверьте в PowerShell:
```bash
git --version
python --version
```

---

## 2) Склонировать репозиторий (git clone)

Откройте PowerShell и перейдите в папку, где хотите хранить проект, например:
```bash
cd C:\Users\<ВАШ_ПОЛЬЗОВАТЕЛЬ>\Desktop
```

Склонируйте репозиторий:
```bash
git clone https://github.com/<your-user>/<your-repo>.git
cd <your-repo>
```

Если работа идёт в отдельной ветке (например `work`), переключитесь:
```bash
git checkout work
git pull
```

---

## 3) Перейти в приложение и создать виртуальное окружение

```bash
cd pc_agent_app
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

---

## 4) Куда вставлять API-ключ

1. Создайте `.env` из шаблона:
   ```bash
   copy .env.example .env
   ```
2. Откройте файл `.env` в любом редакторе и заполните:
   ```env
   OPENAI_API_KEY=sk-...ваш_ключ...
   OPENAI_MODEL=gpt-4.1-mini
   AGENT_SANDBOX_DIR=
   ```

### Что значит `AGENT_SANDBOX_DIR`
- Если оставить пустым — агент создаёт файлы по указанным путям (например рабочий стол).
- Если указать путь (рекомендуется для теста), файлы будут создаваться только внутри этой папки. Пример:
  ```env
  AGENT_SANDBOX_DIR=C:\Users\<ВАШ_ПОЛЬЗОВАТЕЛЬ>\Desktop\agent_sandbox
  ```

---

## 5) Запуск приложения

```bash
python app.py
```

Откроется окно агента, где можно ввести цель свободным текстом.

---

## 6) Быстрый тест, что всё работает

Примеры задач:
- `Создай текстовый файл на рабочем столе и запиши в него приветствие`
- `Открой Wordle в браузере`
- `Открой google.com`

Если вы указали `AGENT_SANDBOX_DIR`, проверяйте созданные файлы в этой папке.

---

## 7) Что делать, если не запускается

1. Убедитесь, что активировано окружение:
   ```bash
   .venv\Scripts\activate
   ```
2. Переустановите зависимости:
   ```bash
   pip install -r requirements.txt --upgrade
   ```
3. Проверьте, что `.env` лежит рядом с `app.py`.

---

## Что внутри проекта (коротко)
- `app.py` — GUI окно.
- `desktop_agent.py` — главный оркестратор.
- `llm.py` — планирование/самооценка через LLM + fallback.
- `tools.py` — инструменты действий (`create_text_file`, `open_url`).
- `policy.py` — правила безопасности.
- `memory.py` — SQLite-память запусков.
- `config.py` — чтение `.env`.
