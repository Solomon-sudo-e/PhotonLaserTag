
class GameParticipant:
    def __init__(self, row, equipment_id, user_id, codename, team):
        self.row = row
        self.team = team
        self.equipment_id = equipment_id
        self.user_id = user_id
        self.codename = codename
        self.score = 0
        self.tagged_base = False

    def __repr__(self):
        return (f"Codename: {self.codename}, Team: {self.team}, "
                f"EquipID: {self.equipment_id}, UserID: {self.user_id}, "
                f"Score: {self.score}, Tagged Base: {self.tagged_base}")
