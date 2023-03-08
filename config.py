from environs import Env

env = Env()
env.read_env()

VIRUS_TOTAL = env.str("VIRUS_TOTAL")
GOOGLE = env.str("GOOGLE")

API_KEY = env.str("API_KEY")
API_KEY_NAME = env.str("API_KEY_NAME")

DB_HOST = env.str("DB_HOST")
DB_NAME = env.str("DB_NAME")
DB_PASS = env.str("DB_PASS")
DB_PORT = env.str("DB_PORT")
DB_USER = env.str("DB_USER")
