class Move:
    def __init__(self, id, game_id, from_pos, to_pos, piece):
        self.id = id
        self.game_id = game_id
        self.from_pos = from_pos
        self.to_pos = to_pos
        self.piece = piece
