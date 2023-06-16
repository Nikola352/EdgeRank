import time

class Comment:
    def __init__(self, comment_csv: list):
        self.comment_id: str = comment_csv[0]
        self.status_id: str = comment_csv[1]
        self.parent_id: str = comment_csv[2]
        self.comment_message: str = comment_csv[3]
        self.author: str = comment_csv[4]
        self.date_published: time.struct_time = time.strptime(comment_csv[5], "%Y-%m-%d %H:%M:%S")
        self.num_reactions: int = int(comment_csv[6])
        self.num_likes: int = int(comment_csv[7])
        self.num_loves: int = int(comment_csv[8])
        self.num_wows: int = int(comment_csv[9])
        self.num_hahas: int = int(comment_csv[10])
        self.num_sads: int = int(comment_csv[11])
        self.num_angrys: int = int(comment_csv[12])
        self.num_special: int = int(comment_csv[13])
        

