

org 5
counter:
    int 0

_start:

    ld 1
    st &counter

    loop:
        ld 1
        st #1

        ld counter
        dec
        st &counter

        jz stop
        jmp loop

    stop:
        hlt
