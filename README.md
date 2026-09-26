# Эмулятор командной оболочки

Практическая работа по дисциплине «Конфигурационное управление», вариант 27.

Программа имитирует командную строку UNIX: показывает приглашение, читает
команду, выполняет её и печатает результат. Написана на Python.

Сделаны этапы 1–4: интерактивный режим, разбор кавычек, параметры
запуска, стартовый скрипт, виртуальная файловая система в памяти
и команды `ls`, `cd`, `uptime`, `uname`, `tail`, `exit`.

## Что умеет

**Приглашение** выглядит как `deep:/docs$ ` — сначала имя виртуальной
файловой системы, потом текущая папка внутри неё.

**Кавычки в аргументах.** Если аргумент содержит пробел, его можно взять
в кавычки: `cd "my dir"`. Подходят и двойные, и одинарные.

**Команды:**

| Команда | Что делает |
|---|---|
| `ls [путь]` | Содержимое папки. Без аргумента — текущей. Для файла — его имя |
| `cd [путь]` | Переход в папку. Без аргумента — в корень. Понимает `.`, `..`, абсолютные и относительные пути |
| `uptime` | Текущее время и сколько работает эмулятор |
| `uname [-a]` | Имя системы; с `-a` — ещё имя VFS, версия и архитектура |
| `tail [-n N] файл` | Последние строки файла, по умолчанию 10 |
| `exit [код]` | Выход. Можно указать код: `exit 3` |

**Ошибки** — программа сообщает и продолжает работать:

- неизвестная команда → `foo: command not found`
- не закрыта кавычка → `syntax error: unterminated quote`
- нет такого пути → `ls: nope: no such file or directory`
- `cd` на файл → `cd: readme.md: not a directory`
- `tail` на папку → `tail: /docs: is a directory`
- `tail -n abc` → `tail: abc: invalid number of lines`
- `exit abc` → `exit: abc: numeric argument required`

`Ctrl+D` тоже завершает программу.

## Параметры запуска

```
./run.sh --vfs ПУТЬ --script ФАЙЛ
```

- `--vfs ПУТЬ` — папка, из которой загружается виртуальная файловая
  система. Её имя показывается в приглашении: `--vfs vfs/deep` даёт `deep$`.
- `--script ФАЙЛ` — стартовый скрипт (см. ниже).

Оба параметра необязательны. Пути проверяются библиотекой pydantic: если
папки VFS или файла скрипта нет, печатается сообщение и программа
завершается с кодом 1. При запуске печатается отладочная строка с тем,
что получено: `[debug] vfs=... script=...`.

## Виртуальная файловая система

С параметром `--vfs` эмулятор читает указанную папку и строит её копию
в памяти: все вложенные папки, файлы и их содержимое. Дальше все команды
работают только с этой копией — папка на диске никогда не изменяется.

При загрузке печатается список всех путей, чтобы было видно, что
загрузилось:

```
$ ./run.sh --vfs vfs/deep
[debug] vfs=vfs/deep script=None
[debug] vfs tree:
  /docs
  /docs/guides
  /docs/guides/guide.txt
  /docs/guides/linux
  /docs/guides/linux/commands.txt
  /docs/intro.txt
  /readme.md
  /src
  /src/main.py
  /src/shell
  /src/shell/shell.py
deep$
```

Для проверки в репозитории лежат три готовых VFS:

- `vfs/minimal` — один файл
- `vfs/files` — несколько файлов в корне
- `vfs/deep` — вложенность в четыре уровня

## Стартовый скрипт

Текстовый файл с командами эмулятора, по одной на строку. Строки,
начинающиеся с `#`, и пустые строки пропускаются. Каждая команда
печатается вместе с приглашением, как будто её ввёл пользователь, затем
её результат. Ошибка не останавливает скрипт. Если в скрипте есть
`exit`, эмулятор завершается с его кодом; если нет — после скрипта
начинается обычный интерактивный режим.

Пример — `start_scripts/stage4.txt`:

```
# просмотр содержимого и переходы
ls
cd docs/guides
tail -n 3 linux/commands.txt

# ошибки
cd nope
tail /docs
exit 0
```

Проверочные скрипты для ОС лежат в `scripts/` — каждый запускает эмулятор
с одним набором параметров:

```sh
sh scripts/test_no_args.sh         # без параметров
sh scripts/test_vfs.sh             # только --vfs
sh scripts/test_script.sh          # только --script
sh scripts/test_all.sh             # оба параметра
sh scripts/test_missing_script.sh  # несуществующий скрипт
sh scripts/test_vfs_minimal.sh     # минимальная VFS
sh scripts/test_vfs_files.sh       # несколько файлов
sh scripts/test_vfs_deep.sh        # вложенность в четыре уровня
sh scripts/test_vfs_missing.sh     # несуществующая папка VFS
sh scripts/test_vfs_not_dir.sh     # вместо папки указан файл
sh scripts/test_commands_minimal.sh  # команды этапа 4 на минимальной VFS
sh scripts/test_commands_files.sh    # то же на нескольких файлах
sh scripts/test_commands_deep.sh     # то же на вложенной VFS
```

## Как запустить

Нужен Python 3.12 и [uv].

```sh
uv sync        # поставить зависимости
./run.sh       # запустить эмулятор
uv run pytest  # запустить тесты
uv run ruff check src tests  # проверить код линтером
```

## Пример работы

```
$ ./run.sh --vfs vfs/deep
[debug] vfs=vfs/deep script=None
[debug] vfs tree:
  /docs
  /docs/guides
  ...
deep:/$ ls
docs
readme.md
src
deep:/$ cd docs/guides
deep:/docs/guides$ ls
guide.txt
linux
deep:/docs/guides$ tail -n 3 linux/commands.txt
10
11
12
deep:/docs/guides$ cd ..
deep:/docs$ uname -a
ShellEmulator deep 0.1.0 arm64
deep:/docs$ uptime
15:42:07 up 00:01:12
deep:/docs$ cd nope
cd: nope: no such file or directory
deep:/docs$ exit 0
```

Со стартовым скриптом команды выполняются сами, видно и ввод, и вывод:

```
$ ./run.sh --vfs vfs/deep --script start_scripts/stage4.txt
[debug] vfs=vfs/deep script=start_scripts/stage4.txt
...
deep:/$ tail -n 3 /docs/guides/linux/commands.txt
10
11
12
deep:/$ tail /docs
tail: /docs: is a directory
deep:/$ exit 0
$ echo $?
0
```

## Структура

```
src/shell_emulator/
    main.py       запуск
    config.py     проверка параметров (pydantic)
    shell.py      цикл ввода команд
    parser.py     разбор строки на слова
    vfs.py        виртуальная файловая система в памяти
    commands/     команды, каждая в своём файле
    core/         константы
tests/            тесты
vfs/              тестовые файловые системы
start_scripts/    стартовые скрипты для эмулятора
scripts/          скрипты ОС для проверки параметров запуска
run.sh            скрипт запуска
```

## Этапы

Каждый этап заканчивается отдельным коммитом. Чтобы посмотреть проект
в состоянии на конец этапа:

```sh
git checkout 55d74a4   # этап 1
git checkout 626c1d2   # этап 2
git checkout 0922590   # этап 3
git checkout main      # вернуться к последней версии
```

- Этап 1 (REPL) — `55d74a4`
- Этап 2 (конфигурация) — `626c1d2`
- Этап 3 (VFS) — `0922590`
