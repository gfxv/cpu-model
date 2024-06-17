# Архитектура компьютера - 2024

- Рудкевич Илья Александрович, P3206
- `asm | acc | neum | hw | instr | struct | stream | mem | pstr | prob1`
- Упрощённый вариант

## Язык программирования

### Форма Бэкуса-Наура

```ebnf
<program> ::= lines

<lines> ::= line | line new_line program

<line> ::= statement | label | comment

<label> ::= <any string except: ";">":" | start_label

<start_label> ::= "_start:" new_line

<comment> ::= ";" string

<statement> ::= mnemonic | mnemonic arg | mnemonic comment | mnemonic arg comment

<mnemonic> ::= org
           | word
           | int
           | ld
           | st
           | add
           | sub
           | inc
           | dec
           | cmp
           | jmp
           | jz
           | nop
           | hlt

<arg> ::= integer
        | "#"integer
        | "$"integer
        | label
        | "&"label
        | "$"label
        | string

<string> ::= "char" | "<char><string>"
<integer> ::= digit | <digit><integer>
<digit> ::= 0 | 1 | 2 | ... | 8 | 9
```

- Код выполняется последовательно.
- Видимость меток и данных -- глобальная
- Для записи литералов используются `word` и `int`.

### Операции
- `org` - разместить код начиная с определенного адреса
- `word` - разместить строку в памяти (один символ - одна ячейка)
- `int` - разместить число в памяти
- `ld` - загрузить значение по адресу в аккумулятор
- `st` - записать значение из аккумулятора по адресу
- `add` - суммировать значение аргумента и аккумулятора (_acc + arg_)
- `sub` - вычесть значение аргумента из аккумулятора (_acc - arg_)
- `mod` - вычислить остаток от деления аккумулятора на значение аргумента (_acc % arg_)
- `inc` - увеличить значение аккумулятора на единицу
- `dec` - уменьшить значение аккумулятора на единицу
- `cmp` - сравнить значение аккумулятора с значением аргумента
- `jmp` - выполнить безусловный переход по адресу
- `jz` - выполнить переходе, если Z == 1
- `nop` - ипользуется для резервирования памяти
- `hlt` - остановить выполнение


## Организация памяти
- Фон-Неймановская архитектура – общая память для инструкций и данных
- Память содержит 1024 ячеек
- Размер машинного слова не определён
- Реализуется списком словарей
- Выполнение программы начинается с метки `_start`
- В нулевой ячейке находится `jmp` на метку `_start`
- Для команд ввода/вывода используется ячейка с адремом `0x1`
- Программист имеет доступ к регистру `ACC` (аккумулятор)

```
Регистры
+------------------------+
| ACC - аккумулятор      |
+------------------------+
| PC - счётчик команд    |
+------------------------+
| DR - регистр данных    |
+------------------------+
| CR - регистр команд    |
+------------------------+
| AR - регистр адреса    |
+------------------------+
| NZ - регистр состояния |
+------------------------+

Память данных и команд
+---------------------+
| 0      : jmp _start |
| 1      : I/O        |
|       ...           |
| n+0    : literal 1  |  <-- Хранит длину литерала, если он является строкой
| n+1    : literal 1  |  <-- Далее -- символы по порядку (один символ -- одна ячейка)
| n+2    : literal 1  |
|       ...           |
| k      : literal 2  |
|       ...           |
| _start : prog start |
|       ...           |
+---------------------+
```

### Адресация
- `69` - указывает на значение ячейки по адресу `69`
- `#69` - прямая загрузка операнда
- `label` - указывает на значение ячейки по адресу метки `label`
- `&label` - указывает на адрес метки `label`
- `$69` - указывает на значение ячейки, которая находится по адресу, находящемуся по адресу `69`

## Система команд
### Набор инструкций
| Мнемоника | Кол-во тактов | Описание |
|-|-|-|
|add `<arg>`| 2-6 | `acc + arg -> acc, nz` |
|sub  `<arg>`| 2-6 | `acc - arg -> acc, nz` |
|inc| 1 | `acc + 1 -> acc, nz` |
|dec| 1 | `acc - 1 -> acc, nz` |
|ld `<arg>`| 2-6 | `mem[arg] -> acc, nz` |
|st `<arg>`| 4-8 | `acc -> mem[arg]` |
|cmp `<arg>`| 2-6 | `acc - arg -> nz` |
|mod `<arg>`| 2-6| `acc % arg -> acc, nz` |
|jmp `<addr>`| 2-6| Выполнить безусловный переход по адресу `<addr>` |
|jz `<addr>`| 2-6 |Выполнить переход по адресу `<addr>`, если Z == 1 |
|hlt| 1 | Останвить выполнение |
|nop|-|Отсутсвие операции (Используется для размещения литералов в памяти)|
|word `<str>`| - | Записать в память строку `<str>` (один символ - одна ячейка)|
|int `<int>`| - | Записать в память число `<int>` |
|org `<addr>`| - | Разместить след. блок кода начиная с адреса `<addr>` |

Где:
- `acc` - аккумулятор
- `nz` - флаги состояния (Negative, Zero)
- `mem[arg]` - значение ячейки памяти по адресу `arg`

> Мнемоники `int` и `word` не являются инструкциями, а используются для записи данных в память.

### Кодирование инструкций
- Инструкции хранятся в формате JSON
- Один элемент списка -- одна инструкция.

Пример:
```json
{
  "index": 13,
  "opcode": "st",
  "arg": 6,
  "arg_type": "raw"
}
```
Где:
- `index` - адрес инструкции в памяти
- `opcode` - код операции
- `arg` - операнд
- `arg_type` - тип аргумента

## Транслятор
`Интерфейс командной строки: translator.py <input_file> <target_file>`


Реализовано в модуле: [translator]{src/translator.py}

Этапы трансляции:
- Выделение меток из кода, проверка их корректности (не совпадают с названиями команд, отсуствуют дубликаты)
- Парсинг кода построчно (определение инструкции, её адреса, тип адресации.)
- Замена `word` и `int` на соответсвующие `nop` операции
- Генерация машинного кода
- Подстановка меток в соответсвующие машинные инструкции

Метки в машинном коде, __не сохраняются__ . Метки, использованные в качестве операнда, преобразуются к адресам команд

## Модель процессора

## Тестирование


```
| ФИО                         | алг   | LoC | code инстр. | инстр. | такт  | вариант                                                              |
| Рудкевич Илья Александрович | hello | 25  | 19          | 135    | 770   | asm | acc | neum | hw | instr | struct | stream | mem | pstr | prob1 |
| Рудкевич Илья Александрович | cat   | 16  | 12          | 66     | 359   | asm | acc | neum | hw | instr | struct | stream | mem | pstr | prob1 |
| Рудкевич Илья Александрович | prob1 | 31  | 23          | 12860  | 65767 | asm | acc | neum | hw | instr | struct | stream | mem | pstr | prob1 |
```
