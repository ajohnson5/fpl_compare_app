class Player:
    def __init__(
        self,
        id: int,
        name: str,
        first_name: str,
        position: int,
        actual_position: int,
        points: int,
        team_name: str,
        is_captain: bool,
        multiplier: int,
        auto_sub: bool,
    ):
        self.id = id
        self.name = name
        self.first_name = first_name
        self.position = position
        self.actual_position = actual_position
        self.starting = position <= 11
        self.points = points
        self.actual_points = points * multiplier
        self.team_name = team_name
        self.is_captain = is_captain
        self.multiplier = multiplier
        self.auto_sub = auto_sub

        # self.stats = player_dict

    def __eq__(self, other):
        if self.id == other.id:
            return True
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.id, self.actual_position))

    def __bool__(self):
        return self.id is not None  # <--- added "return"
