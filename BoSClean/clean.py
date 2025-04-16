# Import all the functions
from income import clean_income
from disability import clean_disability
from homelessness import clean_homelessness
from housing_timelines import process_length_and_movein
from permanent_housing import calculate_permanent_exit

# Print help messages
def show_help():
    print("Welcome to the BoS Data Cleaner!\n")
    print("Select a number to choose a cleaning option:")
    print("  1 → Disability         — Clean 'DISABILITY ENT' and 'DISABILITY EXT' tabs")
    print("  2 → Homelessness       — Clean 'EE UDES' tab (prior living, times homeless, months homeless)")
    print("  3 → Income             — Clean 'INCOME ENT' and 'INCOME EXT' tabs")
    print("  4 → Housing Timelines  — Clean 'ENTRY-EXIT' tab (length of stay and days to move-in)")
    print("  5 → Housing Exit Type  — Clean 'ENTRY-EXIT' tab, classify permanent vs. non-permanent housing exits")
    print("  6 → Exit               — Exit the program")


def main():
    show_help()
    option = input("\nEnter the number of your choice: ").strip()

    if option == "1":
        clean_disability()
        
    elif option == "2":
        clean_homelessness()
        
    elif option == "3":
        clean_income()
        
    elif option == "4":
        process_length_and_movein()
        
    elif option == "5":
        calculate_permanent_exit()
        
    elif option == "6":
        print("Exiting program.")
        
    else:
        print("Invalid option. Please run the program again and choose a valid number.")

if __name__ == "__main__":
    main()
