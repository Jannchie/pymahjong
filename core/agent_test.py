import unittest
from .agent import Agent
from .game import Game


class TestAgent(unittest.TestCase):
    def test_agent(self):
        agents = [Agent() for _ in range(3)]
        game = Game()
        game.print_info()
        for agent, i in enumerate(agents):
            game.link_with(agent, i)


if __name__ == "__main__":
    unittest.main()
