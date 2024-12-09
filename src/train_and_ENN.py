import neat
import os
import pickle
import time
from snake import SnakeGame



def verify_config(config_path):
    """Debug config loading"""
    print(f"Reading config from: {config_path}")
    with open(config_path, 'r') as f:
        content = f.read()
        print("Config contents:", content)

    # Test config loading
    try:
        config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                             neat.DefaultSpeciesSet, neat.DefaultStagnation,
                             config_path)
        print("Config loaded successfully")
        return config
    except Exception as e:
        print(f"Config error: {str(e)}")
        return None

def create_dynamic_config(game):
    num_inputs = game.calculate_num_inputs()
    config = neat.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        'config/config.txt'
    )
    config.genome_config.num_inputs = num_inputs
    return config


def eval_genome(genome, config,game):

    max_bombs = 175
    max_segments = 680

    state=game.get_state()


    genome.fitness = 0
    net = neat.nn.FeedForwardNetwork.create(genome, config)


    game_over = False


    #play snake
    while not game_over:
        #get game state
        state = state[:1714]
        outputs = net.activate(state)

        #make an action
        action = outputs.index(max(outputs))
        reward,game_over, score = game.step(action)

        #update fitness based on score and survival
        genome.fitness += reward
        genome.fitness += score
        genome.fitness +=0.05

    print(genome.fitness)

    game.reset_game()

    return genome.fitness


def eval_genomes(genomes, config, game):
    #eval all genomes



    print("Evaluating genomes")

    for genome_id, genome in genomes:

        print(f"Evaluating genome {genome_id}")
        eval_genome(genome, config, game)
        game.reset_game()


def run_neat(config_path,generations):
    print("Initializing NEAT")
    #runs neat
    # Create test game to get input size

    game = SnakeGame()


    # Load config and modify num_inputs
    config = neat.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )

    # Modify config after loading
    config.genome_config.num_inputs = 1714


    # Initialize population with modified config
    pop = neat.Population(config)

    # Add reporters
    pop.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)

    # Run evolution
    winner = pop.run(lambda genomes, config: eval_genomes(genomes, config, game), generations)

    return winner

def save_best_genome(best_genome, filename="best_genome.pkl"):
    """Save the best genome to a file"""
    with open(filename, "wb") as f:
        pickle.dump(best_genome, f)
    print(f"Best genome saved to {filename}")


def load_best_genome(filename="best_genome.pkl", config=None):
    """Load the best genome from a file"""
    with open(filename, "rb") as f:
        best_genome = pickle.load(f)
    # Recreate the neural network from the loaded genome
    net = neat.nn.FeedForwardNetwork.create(best_genome, config)
    return net

if __name__ == '__main__':

    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(os.path.dirname(__file__), 'config-feedforward.txt')

    winner = run_neat(config_path, generations=10)

    # Save the best genome
    save_best_genome(winner, filename="best_genome.pkl")


    config = neat.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )
    net = load_best_genome("best_genome.pkl", config)


    game = SnakeGame()
    flattened_state = game.get_state()[:1714]  # Get the current state


    outputs = net.activate(flattened_state)
    action = outputs.index(max(outputs))
    reward, done, score = game.step(action)

    print(f"Action: {action}, Reward: {reward}, Score: {score}")

