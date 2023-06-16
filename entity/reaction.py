import time

class Reaction:
    def __init__(self, reaction_csv: list):
        self.status_id: str = reaction_csv[0]
        self.type_of_reaction: str = reaction_csv[1]
        self.reactor: str = reaction_csv[2]
        self.date_reacted: time.struct_time = time.strptime(reaction_csv[3], "%Y-%m-%d %H:%M:%S")