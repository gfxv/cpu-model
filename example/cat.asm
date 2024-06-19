org 5
; counter:
;     int 0

_start:

    ; ld 1         ; load string length
    ; st &counter  ; store to counter

    loop:
        ld 1     ; read next char
        st #1    ; write to output buffer

        ; decrement counter
        ; ld counter
        ; dec
        ; st &counter

        ; check length
        ; jz stop
        jmp loop

    ; stop:
    ;     hlt
