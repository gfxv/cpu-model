
org 20

hello_string:
    word "Hello, World!"
pointer:
    int 0
counter:
    int 0

_start:
    ld &hello_string   ; load pointer
    st &pointer

    ld hello_string    ; Load length (acts like counter)
    st &counter        ; Store counter with address 5

    loop:
        ; inc ptr
        ld pointer   ; load current pointer
        inc          ; increment pointer
        st &pointer  ; save

        ; output symbol
        ld $pointer
        st #2

        ; dec counter
        ld counter   ; load counter
        dec          ; decrement
        st &counter  ; savve

        ; check length
        jz stop
        jmp loop

    stop:
    hlt
