from game import Game
from agent import Agent


# def main():  # to play the game manually
#     game = Game()
#     while game.is_running:
#         game.update()
#     game.quit()


def main():
    record = 0
    agent = Agent()
    game = Game()
    while game.is_running:
        state = game.get_state()

        action = agent.get_action(state)

        reward, new_state, done, score = game.step(action)

        agent.train_short_memory(state, action, reward, new_state, done)

        agent.remember(state, action, reward, new_state, done)

        if done:
            game.reset()
            agent.train_long_memory()

            if score > record:
                record = score
                agent.model.save()


if __name__ == '__main__':
    main()
