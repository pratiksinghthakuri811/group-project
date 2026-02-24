FILE_NAME = "players.txt"


def add_player():
    jersey = input("Enter Jersey Number: ")
    name = input("Enter Name: ")
    age = input("Enter Age: ")
    position = input("Enter Position: ")
    fitness = input("Enter Fitness (Fit/Injured): ")
    goals = input("Enter Goals: ")
    injury = input("Any Injury (Yes/No): ")
    suspension = input("Suspended (Yes/No): ")

    with open(FILE_NAME, "a") as file:
        file.write(jersey + "," + name + "," + age + "," +
                   position + "," + fitness + "," +
                   goals + "," + injury + "," +
                   suspension + "\n")

    print("✅ Player added successfully!\n")


def view_players():
    try:
        with open(FILE_NAME, "r") as file:
            data = file.readlines()

            if not data:
                print("No players found.\n")
                return

            for line in data:
                player = line.strip().split(",")

                print("\nJersey:", player[0])
                print("Name:", player[1])
                print("Age:", player[2])
                print("Position:", player[3])
                print("Fitness:", player[4])
                print("Goals:", player[5])
                print("Injury:", player[6])
                print("Suspension:", player[7])

    except FileNotFoundError:
        print("No data file found.\n")


def delete_player():
    jersey_delete = input("Enter Jersey Number to delete: ")

    try:
        with open(FILE_NAME, "r") as file:
            lines = file.readlines()

        with open(FILE_NAME, "w") as file:
            found = False
            for line in lines:
                player = line.strip().split(",")
                if player[0] != jersey_delete:
                    file.write(line)
                else:
                    found = True

        if found:
            print("✅ Player deleted successfully!\n")
        else:
            print("❌ Player not found.\n")

    except FileNotFoundError:
        print("No data file found.\n")


def search_player():
    search_value = input("Enter Jersey Number or Name to search: ").lower()

    try:
        with open(FILE_NAME, "r") as file:
            lines = file.readlines()

            found = False

            for line in lines:
                player = line.strip().split(",")

                jersey = player[0]
                name = player[1].lower()

                if search_value == jersey or search_value == name:
                    print("\n✅ Player Found:")
                    print("Jersey:", player[0])
                    print("Name:", player[1])
                    print("Age:", player[2])
                    print("Position:", player[3])
                    print("Fitness:", player[4])
                    print("Goals:", player[5])
                    print("Injury:", player[6])
                    print("Suspension:", player[7])
                    found = True

            if not found:
                print("❌ Player not found.\n")

    except FileNotFoundError:
        print("No data file found.\n")


# top scorer
def top_scorer():
    try:
        with open(FILE_NAME, "r") as file:
            lines = file.readlines()

            if not lines:
                print("No players found.\n")
                return

            top_player = None
            max_goals = -1

            for line in lines:
                player = line.strip().split(",")
                goals = int(player[5])

                if goals > max_goals:
                    max_goals = goals
                    top_player = player

            print("\n🏆 Top Scorer:")
            print("Jersey:", top_player[0])
            print("Name:", top_player[1])
            print("Goals:", top_player[5])
            print()

    except FileNotFoundError:
        print("No data file found.\n")


def total_team_goals():
    try:
        with open(FILE_NAME, "r") as file:
            lines = file.readlines()

            total = 0
            for line in lines:
                player = line.strip().split(",")
                total += int(player[5])

            print("⚽ Total Team Goals:", total, "\n")

    except FileNotFoundError:
        print("No data file found.\n")


def menu():
    while True:
        print("⚽ Football Player Management")
        print("1. Add Player")
        print("2. View Players")
        print("3. Delete Player")
        print("4. Search Player")
        print("5. Show Top Scorer")
        print("6. Total Team Goals")
        print("7. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            add_player()
        elif choice == "2":
            view_players()
        elif choice == "3":
            delete_player()
        elif choice == "4":
            search_player()
        elif choice == "5":
            top_scorer()
        elif choice == "6":
            total_team_goals()
        elif choice == "7":
            print("Exiting...")
            break
        else:
            print("Invalid choice!\n")


menu()
