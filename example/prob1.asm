
org 25


max_number:
    int 1000
number:
    int 1
counter:
    int 0


_start:

    loop:

        ld number       ; load current number
        cmp max_number  ; current number - max number -> Z, N
        jz stop         ; if Z == 0: stop

        ; ld number ; load current number
        mod #3      ; acc % 3 -> acc, Z
        jz inc_sum

        ld number   ; load current number
        mod #5      ; acc % 5 -> acc
        jz inc_sum

    continue:
        ld number    ; load current number
        inc
        st &number   ; save new number to check
        jmp loop     ; jump back to loop

    inc_sum:
        ld counter    ; load counter
        inc
        st &counter   ; save (update) counter
        jmp continue

    stop:
        ld counter
        st #1
        hlt ; stop
