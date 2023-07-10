import os


def get_int_list_from_env(env_var_name, default=None):
    v = os.getenv(env_var_name)
    if not v:
        return default
    
    return [int(token.strip()) for token in v.split(',')]


POPULATION_SIZE = int(os.getenv('POPULATION_SIZE', 200))
OFFSPRING_NUMBER = int(os.getenv('OFFSPRING_NUMBER', 200))
HIDDEN_LAYERS = get_int_list_from_env('HIDDEN_LAYERS', [20, 12]) 
MUTATION_PROBABILITY = float(os.getenv('MUTATION_PROBABILITY', 0.25)) 
