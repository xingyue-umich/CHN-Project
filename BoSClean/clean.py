from disability import *

def show_help():
    print("Welcome to the BoS Data Cleaner!\n")
    print("Available cleaning options:")
    print("  -disability   → Clean 'DISABILITY ENT' and 'DISABILITY EXT' tabs, calculate % with disability at entry and exit")
    print("  -income       → Clean 'INCOME ENT' and 'INCOME EXT' tabs, calculate % with income at entry and exit")
    print("  -exit         → Exit the program")
    print("\nPlease enter the option you want to clean:")

def main():
    show_help()
    option = input().strip().lower()

    if option == "-disability":
        clean_disability()
    elif option == "-income":
        clean_income()
    elif option == "-exit":
        print("Exiting program.")
    else:
        print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
