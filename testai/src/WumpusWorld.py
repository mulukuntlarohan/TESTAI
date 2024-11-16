import random
class WumpusWorld:
    def __init__(self, size, kb):
        self.size = size
        self.agent_pos = (0, 0)
        self.gold_pos = (random.randint(0, size - 1), random.randint(0, size - 1))
        self.wumpus_pos = (random.randint(0, size - 1), random.randint(0, size - 1))
        self.pits = {(random.randint(0, size - 1), random.randint(0, size - 1)) for _ in range(size // 2)}
        self.pits.discard(self.agent_pos)

        self.kb = kb
        self.initialize_kb()

    def initialize_kb(self):
        """Add initial facts about the environment."""
        self.kb.add_clause({f"¬Wumpus{self.agent_pos}"})  # No Wumpus at the starting position
        self.kb.add_clause({f"¬Pit{self.agent_pos}"})  # No Pit at the starting position
        self.kb.add_clause({f"Safe{self.agent_pos}"})  # Starting position is safe

    def get_percepts(self, pos):
        """Generate percepts based on the current position."""
        percepts = set()
        if pos in [(self.wumpus_pos[0] + dx, self.wumpus_pos[1] + dy) for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]]:
            percepts.add("Stench")
        if pos in [(pit[0] + dx, pit[1] + dy) for pit in self.pits for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]]:
            percepts.add("Breeze")
        if pos == self.gold_pos:
            percepts.add("Glitter")
        return percepts
