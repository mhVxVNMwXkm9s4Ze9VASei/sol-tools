import os


def clearScreen():
    os.system("cls" if os.name == "nt" else "clear")


def test():
    print("Test function.")
    userInput = input(
        "Enter a token address or 'Q' to return to the main menu: ")

    if userInput.lower() == "q":
        return

    print("You entered: ", userInput)
    input("Press Enter to continue...")


def getMenuOption(function):
    while True:
        clearScreen()
        function()


def menu():
    menuOptions = ["Test"]
    numOptions = len(menuOptions)

    while True:
        clearScreen()
        print("Main menu")

        for i in range(numOptions):
            print(f"{i + 1}. {menuOptions[i]}")

        print(f"{numOptions + 1}. Exit")
        choice = int(input("Choose an option: "))

        if choice in range(1, numOptions + 2):
            if choice == numOptions + 1:
                print("Exiting...")
                break

            chosenOption = "".join(menuOptions[choice - 1].lower().split(" "))
            function = globals().get(chosenOption)

            if callable(function):
                function()
            else:
                print(f"{chosenOption} is not callable.")
        else:
            print("Invalid choice. Please try again.")
            input("Press Enter to continue...")


if __name__ == "__main__":
    menu()
