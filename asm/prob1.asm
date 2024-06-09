
org 25

prepare_data:
    ; first delimiter
    ld #3
    st 1

    ; second delimiter 
    ld #5
    st 2

    ; max number to check
    ld #1000
    st 3

    ; number to check
    ld #1
    st 4

    ; final sum
    ld #0
    st 5

    jmp loop


_start:

    jmp prepare_data

    loop:

        ld 4 ; load current number
        cmp 3 ; current number - max number -> Z, N
        jeq stop ; if Z == 0

        ld 4 ; load current number
        mod 1 ; acc % 3 -> acc
        jz inc_sum

        ld 4 ; load current number
        mod 2 ; acc % 5 -> acc
        jz inc_sum

    continue:
        ld 4 ; load current number
        inc
        st 4 ; save new number to check
        jmp loop ; jump back to loop

    stop:
        hlt ; stop

    inc_sum:
        ld 5 ; load final sum 
        inc
        st 5 ; save (update) final sum
        jmp continue