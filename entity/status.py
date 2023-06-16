import time

class Status:
    def __init__(self, status_csv: list):
        self.status_id: str = status_csv[0]
        self.status_message: str = status_csv[1]
        self.status_type: str = status_csv[2]
        self.status_link: str = status_csv[3]
        self.date_published: time.struct_time = time.strptime(status_csv[4], "%Y-%m-%d %H:%M:%S")
        self.author: str = status_csv[5]
        self.num_reactions: int = int(status_csv[6])
        self.num_comments: int = int(status_csv[7])
        self.num_shares: int = int(status_csv[8])
        self.num_likes: int = int(status_csv[9])
        self.num_loves: int = int(status_csv[10])
        self.num_wows: int = int(status_csv[11])
        self.num_hahas: int = int(status_csv[12])
        self.num_sads: int = int(status_csv[13])
        self.num_angrys: int = int(status_csv[14])
        self.num_special: int = int(status_csv[15])

    def to_csv(self) -> list:
        return [
            self.status_id,
            self.status_message,
            self.status_type,
            self.status_link,
            time.strftime("%Y-%m-%d %H:%M:%S", self.date_published),
            self.author,
            self.num_reactions,
            self.num_comments,
            self.num_shares,
            self.num_likes,
            self.num_loves,
            self.num_wows,
            self.num_hahas,
            self.num_sads,
            self.num_angrys,
            self.num_special
        ]

    def __str__(self) -> str:
        return ','.join(map(str, self.to_csv())) + '\n'