import time

class Share:
    def __init__(self, share_csv):
        self.status_id: str = share_csv[0]
        self.sharer: str = share_csv[1]
        self.date_shared: time.struct_time = time.strptime(share_csv[2], "%Y-%m-%d %H:%M:%S")