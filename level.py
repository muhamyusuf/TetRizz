class LevelManager:
    def __init__(self, score):
        self.score = score

    def get_level(self):
        if self.score < 1000:
            return 1
        elif 1000 <= self.score < 2000:
            return 2
        elif 2000 <= self.score < 3000:
            return 3
        else:
            return 4
        
    def reset(self):
        return 1;