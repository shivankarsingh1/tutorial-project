class Character:

    def __init__(self, name, mass, size, launch_power, unlock_score,
                 color, ability):
        self.name = name
        self.mass = mass
        self.size = size
        self.launch_power = launch_power
        self.unlock_score = unlock_score
        self.color = color
        self.ability = ability

    def is_unlocked(self, total_score_earned):
        return total_score_earned >= self.unlock_score

    def describe(self):
        return (f"mass {self.mass:g} | size {self.size:g} | "
                f"power {self.launch_power:g}")

ROCKO = Character("Rocko", 1.0, 1.0, 1.0, 0,
                  (140, 190, 240), "Balanced all-rounder.")
BOULDER = Character("Boulder", 2.0, 1.4, 0.75, 500,
                    (160, 140, 120),
                    "Heavy: massive impact damage, slower launch.")
SPLITTER = Character("Splitter", 0.8, 0.9, 1.05, 1500,
                     (235, 200, 120),
                     "Splits into three mid-flight for wider coverage.")

CHARACTERS = [ROCKO, BOULDER, SPLITTER]
CHARACTER_BY_NAME = {c.name: c for c in CHARACTERS}
