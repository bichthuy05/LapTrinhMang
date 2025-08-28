import sys
import unittest
from unittest.mock import MagicMock, patch
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from unittest.mock import MagicMock, patch
from shared.game_logic import determine_winner
from shared.constants import Move, Result

class TestGameLogic(unittest.TestCase):
    def test_standard_moves(self):
        test_cases = [
            # (player1, player2, expected)
            (Move.ROCK, Move.SCISSORS, Result.WIN),
            (Move.SCISSORS, Move.PAPER, Result.WIN),
            (Move.PAPER, Move.ROCK, Result.WIN),
            (Move.ROCK, Move.PAPER, Result.LOSE),
            (Move.PAPER, Move.SCISSORS, Result.LOSE),
            (Move.SCISSORS, Move.ROCK, Result.LOSE),
            (Move.ROCK, Move.ROCK, Result.DRAW)
        ]
        
        for p1, p2, expected in test_cases:
            with self.subTest(f"{p1.name} vs {p2.name}"):
                result = determine_winner(p1.value, p2.value)
                self.assertEqual(result, expected.value)
    
    def test_invalid_input(self):
        self.assertEqual(determine_winner("invalid", Move.ROCK.value), Result.INVALID.value)
        self.assertEqual(determine_winner(None, None), Result.INVALID.value)

    
    def test_concurrent_games(self):
        """Test xử lý đồng thời nhiều game"""
        from concurrent.futures import ThreadPoolExecutor
        
        test_cases = [
            ('rock', 'scissors', 'win'),
            ('paper', 'rock', 'win'),
            ('scissors', 'scissors', 'draw')
        ]
        
        with ThreadPoolExecutor(max_workers=3) as executor:
            results = list(executor.map(
                lambda p: determine_winner(p[0], p[1]), 
                test_cases
            ))
        
        self.assertEqual(results, [t[2] for t in test_cases])

if __name__ == '__main__':
    unittest.main(verbosity=2)