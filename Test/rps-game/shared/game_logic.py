from shared.constants import Move, Result

def determine_winner(choice1, choice2):
    if choice1 not in [m.value for m in Move] or choice2 not in [m.value for m in Move]:
        return Result.INVALID.value
    
    if choice1 == choice2:
        return Result.DRAW.value
    
    win_conditions = {
        Move.ROCK.value: Move.SCISSORS.value,
        Move.PAPER.value: Move.ROCK.value,
        Move.SCISSORS.value: Move.PAPER.value
    }
    
    return Result.WIN.value if win_conditions[choice1] == choice2 else Result.LOSE.value