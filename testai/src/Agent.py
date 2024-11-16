class Agent:
    def __init__(self, world):
        self.world = world
        self.position = (0, 0)

    def update_kb(self, percepts):
        """Update the KB based on the agent's percepts."""
        if "Stench" in percepts:
            self.world.kb.add_clause({f"Stench{self.position}"})
        if "Breeze" in percepts:
            self.world.kb.add_clause({f"Breeze{self.position}"})
        if "Glitter" in percepts:
            self.world.kb.add_clause({f"Gold{self.position}"})
            print("Gold found!")

    def decide_next_action(self):
        """Decide the next action based on the KB."""
        if self.world.kb.entails(f"Safe{self.position}"):
            print(f"Agent believes {self.position} is safe.")
            return "Move"
        else:
            print(f"Agent avoids {self.position}.")
            return "Avoid"
