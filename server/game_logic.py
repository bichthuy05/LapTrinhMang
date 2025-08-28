def determine_winner(choice1, choice2):
    if choice1 not in ['rock', 'paper', 'scissors'] or choice2 not in ['rock', 'paper', 'scissors']:
        return -1  # Invalid

    if choice1 == choice2:
        return 0  # Draw
    elif (choice1 == 'rock' and choice2 == 'scissors') or \
         (choice1 == 'scissors' and choice2 == 'paper') or \
         (choice1 == 'paper' and choice2 == 'rock'):
        return 1  # Player 1 wins
    else:
        return 2  # Player 2 wins
