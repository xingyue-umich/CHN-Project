# Import all the functions
from disability import clean_disability
from homelessness import clean_homelessness
from income import clean_income

# Print help messages
def show_help():
    print("Welcome to the BoS Data Cleaner!\n")
    print("Available cleaning options:")
    print("  -disability   → Clean 'DISABILITY ENT' and 'DISABILITY EXT' tabs, calculate % with disability at entry and exit")
    print("  -homelessness → Clean 'EE UDES' tab, analyze prior living situation, times homeless, and months homeless in the past 3 years")
    print("  -income       → Clean 'INCOME ENT' and 'INCOME EXT' tabs, calculate % receiving income within a date range")
    print("  -exit         → Exit the program")
    print("\nPlease enter the option you want to clean:")

def main():
    
    show_help()
    option = input().strip().lower()

    if option == "disability":
        clean_disability()
        return
    
    if option == "homelessness":
        clean_homelessness()
        return
    
    elif option == "income":
        clean_income()
        return
    
    elif option == "exit":
        print("Exiting program.")
    
    else:
        print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
