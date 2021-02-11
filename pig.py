import random
import sys  # for argv

double_points = {"Sider": 1, "Razorback": 20, "Trotter": 20,
                 "Snouter": 40, "Leaning Jowler": 60}
single_points = {"Sider": 0, "Razorback": 5, "Trotter": 5,
                 "Snouter": 10, "Leaning Jowler": 15}
pigs_weights = {"Sider": 60, "Razorback": 20, "Trotter": 10,
                "Snouter": 7, "Leaning Jowler": 3}
pigs_events = {"no touch": 92, "Oinker": 7, "Piggyback": 1}


class PigGame:

    def __init__(self, player1, player2, max_point):
        """
        Initialize pig game and start the game
        :param player1: string player name
        :param player2: string player name
        :param max_point: int points to win
        """
        self.player1_name = player1
        self.player2_name = player2
        self.player1_point = self.player2_point = 0
        self.max_point = max_point
        self.game_round = 0
        self.stop_rolling = False
        self.stop_game = False
        self.start_game()

    def game_over(self, winner: str) -> None:
        """
        print game over, score and announce winner
        ask player would they like to play again
        :param winner: the winner player's name
        :return: None
        """

        print(20 * ".")
        print("GAME OVER")
        print(f"{self.player1_name}: {self.player1_point}, "
              f"{self.player2_name}: {self.player2_point}")
        print(f"{winner} wins!")
        print("\nThank you for playing")

        again = input("Would you like to play again? ")
        if again.lower() in ["yes", "ye", "y"]:
            print(30 * ".")
            main()
        else:
            print("See you later!")
            sys.exit(0)

    def print_score(self) -> None:
        """
        print score
        :return: None
        """
        print(20 * ".")
        print(f"{self.player1_name}: {self.player1_point}, "
              f"{self.player2_name}: {self.player2_point}")
        print(20 * ".")

    def roll(self) -> None:
        """
        roll and randomly pick a landing position and process the points
        :return: None
        """

        def process_roll(roll1: str, roll2: str) -> int:
            """
            given position of pig1 and pig2, process touching event
            and print combo and points
            :return: integer of points need to add or deducted
            """
            points_delta = 0
            special_event = random.choices(list(pigs_events.keys()),
                                           list(pigs_events.values()))[0]

            if special_event == "Oinker":
                combo = "an Oinker!"
                self.stop_rolling = True
                if self.game_round % 2 == 0:
                    points_delta = -1 * self.player1_point
                else:
                    points_delta = -1 * self.player2_point
            elif special_event == "Piggyback":
                combo = "a Piggyback! Unlucky!"
                self.stop_game = True
            elif roll1 == roll2:  # both pigs match
                combo = "a Double " + roll1
                points_delta = double_points[roll1]
            else:  # both pigs are different
                combo = f"a Mixed Combo: {roll1} and {roll2}"
                points_delta = single_points[roll1] + single_points[roll2]

            print(5 * " " + "You rolled " + combo)
            if self.stop_rolling:  # oinker
                print(5 * " " + "You lose all of your points")
            elif self.stop_game:  # piggyback
                print(5 * " " + "Your opponent won!")
            else:
                print(5 * " " + f"You earned {points_delta} points\n")

            return points_delta

        pig1 = random.choices(list(pigs_weights.keys()),
                              list(pigs_weights.values()))[0]
        pig2 = random.choices(list(pigs_weights.keys()),
                              list(pigs_weights.values()))[0]
        points = process_roll(pig1, pig2)
        if self.game_round % 2 == 0:
            self.player1_point += points
        else:
            self.player2_point += points

    def start_game(self) -> None:
        """
        start the pig game
        :return: None
        """

        while not self.stop_game:
            self.print_score()
            self.stop_rolling = False
            self.turn()
            self.game_round += 1

    def turn(self) -> None:
        """
        Start a turn for the player. Player would either roll or pass.
        If oinker, lose point and stop rolling. If piggyback, lose game.
        If pass, bank the points. If roll, call self.roll().
        :return: None
        """
        player = self.player1_name \
            if self.game_round % 2 == 0 else self.player2_name

        print(f"Your turn, {player}\n")

        while not self.stop_rolling:
            player_input = input(5 * " " + "ROLL or PASS? ")
            if player_input.lower() in ["r", "ro", "rol", "roll"]:  # roll
                self.roll()
                if self.player1_point > self.max_point or \
                        self.player2_point > self.max_point:
                    self.stop_rolling = True
                    self.stop_game = True
                    winner = self.player1_name \
                        if self.player1_point > self.player2_point \
                        else self.player2_name
                    self.game_over(winner)
                elif self.stop_game:  # piggyback
                    self.stop_rolling = True
                    self.stop_game = True
                    winner = self.player2_name \
                        if player == self.player1_name else self.player1_name
                    self.game_over(winner)
            elif player_input.lower() in ["p", "pa", "pas", "pass"]:  # pass
                self.stop_rolling = True
            else:
                print(5 * " " + "Invalid input. Roll or Pass.")


def main() -> None:
    """
    process command line argument and initialize pig game
    handle invalid command line argument
    :return: None
    """

    command_line_argument = sys.argv

    try:
        player1 = command_line_argument[1]
        player2 = command_line_argument[2]
        max_point = int(command_line_argument[3])
        if len(command_line_argument) > 4:
            raise IndexError()
        elif max_point <= 0:
            raise ValueError
    except IndexError:
        print("Invalid Command Line Argument.")
        print("Usage:[player 1 name] [player 2 name] [target score]")
        print("Example: Spot Rover 300")
        sys.exit(1)
    except ValueError:
        print("Third arguments needs to be an positive integer")
        sys.exit(1)

    print(f"Competitors: {player1} vs. {player2}\n")
    PigGame(player1, player2, max_point)


if __name__ == '__main__':
    main()
