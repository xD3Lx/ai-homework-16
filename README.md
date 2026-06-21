# AI Homework 16: Notes MCP Server
Домашнє завдання до Заняття 16: MCP (Model Context Protocol): AI Tools Architecture

## Requirements

- Python 3.10+
- `mcp` Python package
- Claude Desktop

## Installation & Setup

1. Make sure you are in the project folder:
   ```bash
   cd /Users/delrius/ai/ai-homework-16
   ```

2. Activate your virtual environment (if not already actived):
   ```bash
   source .venv/bin/activate
   ```

3. Install requirements (assuming a `requirements.txt` exists) or install `mcp`:
   ```bash
   pip install -r requirements.txt
   ```

## Connecting to Claude Desktop

Для того, щоб інтегрувати цей MCP server в Claude for Desktop, треба додати зміни з `claude_desktop_config.json` 
в конфігураційний файл Claude Desktop (для macOS `~/Library/Application Support/Claude/claude_desktop_config.json`).

```json
{
  "mcpServers": {
    "mcp-server-notes": {
      "command": "/Users/delrius/ai/ai-homework-16/.venv/bin/python",
      "args": [
        "/Users/delrius/ai/ai-homework-16/server.py"
      ]
    }
  }
}
```

Після зміни в файлі необхідно перезапустити Claude Desktop, щоб він підхопив нові налаштування.

## Tools

Сервер експортує 2 tools i 1 resource:

### create_note (tool)

Параметри: content - обов'язковий, tag - необов'язковий. 
Створює нову нотатку з текстом text та тегом tag (якщо він вказаний).

Приклад запиту: 

```with the help of mcp-server-notes  create a note: "Hello, MCP server" with tag "hello"```

### search_notes (tool)

Параметри: query - обов'язковий. 
Пошук нотаток, які містять текст query.

Приклад запиту:

```with the help of mcp-server-notes search for "Second"```

### "notes://summary" (resource)

Цей ресурс повертає короткий огляд всіх нотаток у вигляді тексту. 
Він містить:
- загальну кількість нотаток
- кількість нотаток з тегами
- всі нотатки


