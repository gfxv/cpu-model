org 5

_start:

    loop:
        ld 1     ; read next char
        st #1    ; write to output buffer
        jmp loop

