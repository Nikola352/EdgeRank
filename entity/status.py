import time

class Status:
    def __init__(self, status_csv: list):
        self.status_id: str = status_csv[0]
        self.status_message: str = status_csv[1]
        self.status_type: str = status_csv[2]
        self.status_link: str = status_csv[3]
        self.date_published: time.struct_time = time.strptime(status_csv[4], "%Y-%m-%d %H:%M:%S")
        self.author: str = status_csv[5]
        self.num_reactions: str = int(status_csv[6])
        self.num_comments: str = int(status_csv[7])
        self.num_shares: str = int(status_csv[8])
        self.num_likes: str = int(status_csv[9])
        self.num_loves: str = int(status_csv[10])
        self.num_wows: str = int(status_csv[11])
        self.num_hahas: str = int(status_csv[12])
        self.num_sads: str = int(status_csv[13])
        self.num_angrys: str = int(status_csv[14])
        self.num_special: str = int(status_csv[15])
