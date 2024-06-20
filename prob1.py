# little python script to check asm script


def main() -> None:
    final_sum = 0
    max_number = 1000
    number = 1
    

    while number < max_number:
        if number % 3 == 0:
            final_sum += number
            number += 1
            continue
        elif number % 5 == 0:
            final_sum += number
        
        number += 1
    print(final_sum)


if __name__ == "__main__":
    main()
