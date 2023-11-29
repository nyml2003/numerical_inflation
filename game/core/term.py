import numpy as np
from .constants import *


class Term:
    def __init__(self, mean, std):
        self.mean = mean
        self.std = std
        self.bias = TERM_PASSING_LINE / np.log1p(mean / std)

    def get_value(self):
        return np.random.normal(self.mean, self.std)

    def evaluate(self, value, level):
        if level == 0:
            return 0
        value = value // level
        if value < self.mean:
            return TERM_PASSING_LINE - np.log1p(np.abs(self.mean - value) / self.std) * self.bias
        else:
            return TERM_PASSING_LINE + np.log1p(np.abs(self.mean - value) / self.std) * self.bias


class Attack(Term):
    def __init__(self):
        super().__init__(50, 10)


class AttackPercent(Term):
    def __init__(self):
        super().__init__(20, 5)


class Defense(Term):
    def __init__(self):
        super().__init__(50, 10)


class DefensePercent(Term):
    def __init__(self):
        super().__init__(20, 5)


class Health(Term):
    def __init__(self):
        super().__init__(500, 100)


class HealthPercent(Term):
    def __init__(self):
        super().__init__(20, 5)


class CriticalRate(Term):
    def __init__(self):
        super().__init__(10, 2)


class CriticalDamage(Term):
    def __init__(self):
        super().__init__(50, 10)


def get_random_term():
    choice = np.random.choice(
        [
            'attack',
            'attack_percent',
            'defense',
            'defense_percent',
            'health',
            'health_percent',
            'critical_rate',
            'critical_damage',
        ]
    )
    if choice == 'attack':
        return 'attack', Attack().get_value()
    elif choice == 'attack_percent':
        return 'attack_percent', AttackPercent().get_value()
    elif choice == 'defense':
        return 'defense', Defense().get_value()
    elif choice == 'defense_percent':
        return 'defense_percent', DefensePercent().get_value()
    elif choice == 'health':
        return 'health', Health().get_value()
    elif choice == 'health_percent':
        return 'health_percent', HealthPercent().get_value()
    elif choice == 'critical_rate':
        return 'critical_rate', CriticalRate().get_value()
    elif choice == 'critical_damage':
        return 'critical_damage', CriticalDamage().get_value()
