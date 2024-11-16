import random
from WumpusWorld import WumpusWorld
from Agent import Agent
from Knowledgebase import KnowledgeBase, Clause, ResolutionEngine

def main():
    # Initialize the knowledge base
    kb = KnowledgeBase()

    # Initialize the world with the knowledge base
    world = WumpusWorld(size=4, num_pits=2, knowledge_base=kb)

    # Create the agent
    agent = Agent(world)

    print("Game started!")

    # Simulation loop (can add more game rules here)
    while True:
        action = agent.take_action()
        print(f"Agent action: {action}")

        # Check if the agent grabbed the gold
        if action == "Grabbed the Gold!":
            print("Agent has grabbed the gold! Game over.")
            break

        # Add other exit conditions as necessary, like the agent falling into a pit or being eaten by the Wumpus
        # For simplicity, let's break the loop after 10 turns
        if len(world.visited) > 10:
            print("Maximum steps reached. Game over.")
            break

if __name__ == "__main__":
    main()
