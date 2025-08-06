import unittest
from server.game_logic import determine_winner
from shared.constants import Move, Result

class TestGameLogic(unittest.TestCase):
    def test_determine_winner(self):
        # Test các trường hợp thắng
        self.assertEqual(determine_winner(Move.ROCK.value, Move.SCISSORS.value), Result.WIN)
        self.assertEqual(determine_winner(Move.PAPER.value, Move.ROCK.value), Result.WIN)
        self.assertEqual(determine_winner(Move.SCISSORS.value, Move.PAPER.value), Result.WIN)
        
        # Test các trường hợp thua
        self.assertEqual(determine_winner(Move.ROCK.value, Move.PAPER.value), Result.LOSE)
        self.assertEqual(determine_winner(Move.PAPER.value, Move.SCISSORS.value), Result.LOSE)
        self.assertEqual(determine_winner(Move.SCISSORS.value, Move.ROCK.value), Result.LOSE)
        
        # Test các trường hợp hòa
        self.assertEqual(determine_winner(Move.ROCK.value, Move.ROCK.value), Result.DRAW)
        self.assertEqual(determine_winner(Move.PAPER.value, Move.PAPER.value), Result.DRAW)
        self.assertEqual(determine_winner(Move.SCISSORS.value, Move.SCISSORS.value), Result.DRAW)
        
        # Test trường hợp không hợp lệ
        self.assertEqual(determine_winner(999, Move.ROCK.value), Result.INVALID)
        self.assertEqual(determine_winner(Move.PAPER.value, 999), Result.INVALID)

if __name__ == '__main__':
    unittest.main()