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
            lines = file.readlines()

            if not lines:
                print("No players found.\n")
                return

            for line in lines:
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


# ✅ UPDATE PLAYER
def update_player():
    jersey_update = input("Enter Jersey Number to update: ")

    try:
        with open(FILE_NAME, "r") as file:
            lines = file.readlines()

        with open(FILE_NAME, "w") as file:
            found = False

            for line in lines:
                player = line.strip().split(",")

                if player[0] == jersey_update:
                    found = True
                    print("Enter new details:")

                    player[1] = input("New Name: ")
                    player[2] = input("New Age: ")
                    player[3] = input("New Position: ")
                    player[4] = input("New Fitness: ")
                    player[5] = input("New Goals: ")
                    player[6] = input("New Injury: ")
                    player[7] = input("New Suspension: ")

                    file.write(",".join(player) + "\n")
                else:
                    file.write(line)

        if found:
            print("✅ Player updated successfully!\n")
        else:
            print("❌ Player not found.\n")

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


# ✅ NEW: Search Player
def search_player():
    search_value = input("Enter Jersey Number or Name to search: ").lower()

    try:
        with open(FILE_NAME, "r") as file:
            lines = file.readlines()

            print("\n🚑 Injured Players:")
            for line in lines:
                player = line.strip().split(",")
                if player[6].lower() == "yes":
                    print("Jersey:", player[0], "| Name:", player[1])

    except FileNotFoundError:
        print("No data file found.\n")


# ✅ NEW: Top Scorer
def top_scorer():
    try:
        with open(FILE_NAME, "r") as file:
            lines = file.readlines()

            print("\n⛔ Suspended Players:")
            for line in lines:
                player = line.strip().split(",")
                if player[7].lower() == "yes":
                    print("Jersey:", player[0], "| Name:", player[1])

    except FileNotFoundError:
        print("No data file found.\n")


# ✅ SORT BY GOALS
def sort_by_goals():
    try:
        with open(FILE_NAME, "r") as file:
            lines = file.readlines()

            players = []
            for line in lines:
                player = line.strip().split(",")
                players.append(player)

            players.sort(key=lambda x: int(x[5]), reverse=True)

            print("\n📊 Players Sorted by Goals:")
            for player in players:
                print("Name:", player[1], "| Goals:", player[5])

    except FileNotFoundError:
        print("No data file found.\n")


# ✅ COUNT TOTAL PLAYERS
def total_players():
    try:
        with open(FILE_NAME, "r") as file:
            lines = file.readlines()
            print("👥 Total Players:", len(lines), "\n")

    except FileNotFoundError:
        print("No data file found.\n")


def menu():
    while True:
        print("\n⚽ Football Player Management")
        print("1. Add Player")
        print("2. View Players")
        print("3. Update Player")
        print("4. Delete Player")
        print("5. Show Injured Players")
        print("6. Show Suspended Players")
        print("7. Sort Players by Goals")
        print("8. Total Players")
        print("9. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            add_player()
        elif choice == "2":
            view_players()
        elif choice == "3":
            update_player()
        elif choice == "4":
            delete_player()
        elif choice == "5":
            show_injured()
        elif choice == "6":
            show_suspended()
        elif choice == "7":
            sort_by_goals()
        elif choice == "8":
            total_players()
        elif choice == "9":
            print("Exiting...")
            break
        else:
            print("Invalid choice!\n")


menu()
