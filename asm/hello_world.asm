
org 20
hello_string:
    word "Hello World"

_start:
    ld &hello_string

    ; Preparation
    st #4   ; Pointer to string
    ld $4    ; Load length (acts like counter)
    st #5   ; Store counter with address 5

    ; [4] - ptr to string
    ; [5] - total length 

    loop:
    ; inc ptr
    ld 4   ; load current pointer
    inc    ; increment pointer
    st #4  ; save

    ; out char
    ld $4
    st #1  ; [1] - i/o address

    ; dec counter
    ld 5   ; load counter
    dec    ; decrement
    st #5  ; savve

    ; check length
    jz stop
    jmp loop

    stop:
    hlt





