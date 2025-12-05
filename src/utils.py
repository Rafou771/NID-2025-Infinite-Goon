from json import load, dump

CONFIG_PATH = "./config.json"
ENCONDING = "utf8"

def get_config(args : list[str] | str = None) -> dict:
    with open(CONFIG_PATH, 'r', encoding=ENCONDING) as f:
        data = load(f)
    return ([data[e] for e in args] if type(args) == list else data[args]) if args != None else data

def write_config(args : dict) -> None:
    data = get_config()
    for key, value in args.items():
        data[key] = value

    with open(CONFIG_PATH, 'w', encoding=ENCONDING) as f:
        dump(data, f, indent=4)