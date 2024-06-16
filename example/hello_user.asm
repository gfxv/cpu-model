
org 20

pointer:
    int 0
counter:
    int 0

prompt_message:
    word "What's your name? (Put length of your name at the beginning. Example: 8Username)"
greetings_string:
    word "Hello, "
new_line:
    int 10
end_string:
    word "!"

input_length:
    int 0
input_start_pointer:
    int 0
buffer_writer:
    int 0
buffer:
    int 64

_start:

    ;;;;;;;;;;;;;;;;;;;;;;;;;;
    ;; PRINT prompt_message ;;
    ;;;;;;;;;;;;;;;;;;;;;;;;;;

    ld &prompt_message ; load address of string
    st &pointer        ; save pointer

    ld prompt_message  ; load first value (string length)
    st &counter        ; save counter

    prompt_loop:
        ld pointer     ; load current pointer
        inc            ; increment pointer (move to next symbol)
        st &pointer    ; save

        ld $pointer    ; load current symbol
        st #1          ; print symbol ([1] - i/o address)

        ; decrement counter
        ld counter
        dec
        st &counter

        ; check counter
        jz read_input
        jmp prompt_loop

    ;;;;;;;;;;;;;;;;
    ;; READ INPUT ;; (and save to buffer)
    ;;;;;;;;;;;;;;;;

    read_input:

        ld new_line
        st #1

        ld 1                    ; read length
        st &input_length        ; save length (needed later to print buffer)
        st &counter             ; save length, acts as a counter

        ld &buffer              ; load buffer pointer (points at the beginning)
        st &input_start_pointer ; save start pointer (needed later to print buffer)
        st &buffer_writer       ; used to write to buffer

    input_loop:
        ld 1  ; read next symbol
        st buffer_writer

        ld buffer_writer
        inc
        st &buffer_writer

        ; decrement counter
        ld counter
        dec
        st &counter

        ; check counter
        jz print_greetings
        jmp input_loop

    ;;;;;;;;;;;;;;;;;;
    ;; PRINT ANSWER ;;
    ;;;;;;;;;;;;;;;;;;

    ; prints 'Hello, '
    print_greetings:

    ld &greetings_string
    st &pointer

    ld greetings_string
    st &counter

    greetings_loop:
        ld pointer
        inc
        st &pointer

        ld $pointer
        st #1

        ld counter
        dec
        st &counter

        jz print_name
        jmp greetings_loop

    ; prints '<name>'
    print_name:
    ld input_start_pointer
    st &pointer

    ld input_length
    st &counter

    hello_loop:
        ld $pointer
        st #1

        ld pointer
        inc
        st &pointer

        ld counter
        dec
        st &counter

        jz print_end
        jmp hello_loop

    ; prints '!'
    print_end:
        ld &end_string
        inc
        st &pointer

        ld $pointer
        st #1
    hlt
