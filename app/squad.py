from typing import Self

from player import Player


class Squad:

    def __init__(self, manager_id:int, squad_list: list[Player],chip ):
        self.manager_id = manager_id
        self.start_xi = squad_list[:11]
        self.bench = sorted(squad_list[11:], key = lambda x: x.actual_position)
        self.goalies = squad_list[0]
        self.defenders = [x for x in self.start_xi if x.actual_position==2]
        self.midfielders = [x for x in self.start_xi if x.actual_position==3]
        self.strikers = [x for x in self.start_xi if x.actual_position==4]
        self.chip = chip


    def players_by_position(self, position:int):
        if position == 1:
            return self.goalies
        elif position == 2:
            return self.defenders
        elif position == 3:
            return self.midfielders
        else:
            return self.strikers



    def compare_squad(self, squad_2: Self):
        #Compares two squads and puts common players at the start of the lists for all positions
        squad_1_layout = [self.bench, [self.goalies],]
        squad_2_layout = [squad_2.bench, [self.goalies],]

        for position in [2,3,4]:
            squad_1_players_in_pos = self.players_by_position(position)
            squad_2_players_in_pos = squad_2.players_by_position(position)

            common_players = self.get_common_players_position(squad_1_players_in_pos,squad_2_players_in_pos)



            squad_1_layout.append(sorted([y for y in squad_1_players_in_pos if y in common_players],key=common_players.index) + [x for x in squad_1_players_in_pos if x not in common_players])
            squad_2_layout.append(sorted([y for y in squad_2_players_in_pos if y in common_players],key=common_players.index) + [x for x in squad_2_players_in_pos if x not in common_players])


        return squad_1_layout, squad_2_layout
        

    def get_common_players_position(self, squad_1_position, squad_2_position):
        return list(set(squad_1_position).intersection(squad_2_position))