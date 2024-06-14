
# little python script to check asm script

def main() -> None:
    counter = 0
    max_number = 1000
    number = 1

    while number < max_number:
        if number % 3 == 0:
            counter += 1
        elif number % 5 == 0:
            counter += 1
        number += 1

    print(counter)

if __name__ == "__main__":
    main()
