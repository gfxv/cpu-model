# Архитектура компьютера - 2024

- Рудкевич Илья Александрович, P3206
- `asm | acc | neum | hw | instr | struct | stream | mem | pstr | prob1`
- Упрощённый вариант

## Язык программирования

__Форма Бэкуса-Наура__

```ebnf
<program> ::= lines

<lines> ::= line | line new_line program

<line> ::= statement | label | comment

<label> ::= <any string except: ";">":" | start_label

<start_label> ::= "_start:" new_line

<comment> ::= ";" string

<statement> ::= opcode | opcode arg | opcode comment | opcode arg comment

<opcode> ::= org
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


## Организация памяти

## Система команд

## Транслятор

## Модель процессора

## Тестирование


```
| ФИО                         | алг   | LoC | code инстр. | инстр. | такт  | вариант                                                              |
| Рудкевич Илья Александрович | hello | 25  | 19          | 135    | 770   | asm | acc | neum | hw | instr | struct | stream | mem | pstr | prob1 |
| Рудкевич Илья Александрович | cat   | 16  | 12          | 66     | 359   | asm | acc | neum | hw | instr | struct | stream | mem | pstr | prob1 |
| Рудкевич Илья Александрович | prob1 | 31  | 23          | 12860  | 65767 | asm | acc | neum | hw | instr | struct | stream | mem | pstr | prob1 |
```
