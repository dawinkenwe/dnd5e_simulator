from unittest import TestCase
from unittest.mock import patch

import unittest

from health_pool import HealthPool


class TestHealthPool(TestCase):
    def setUp(self):
        self.health_pool = HealthPool(max_hp=10, current_hp=10, temporary_hp=5, hit_die="1d6", num_hit_dice=1)

    def test_add_hp_greater_than_max(self):
        self.health_pool.add_hp(15)
        self.assertEqual(self.health_pool.current_hp, 10)

    def test_add_hp_stabilizes(self):
        self.health_pool.current_hp = -7
        self.health_pool.temporary_hp = 0
        self.health_pool.death_save_failures=2
        self.health_pool.add_hp(7)
        self.assertEqual(self.health_pool.current_hp, 7)
        self.assertEqual(self.health_pool.death_save_failures, 0)

    def test_add_temporary_hp_stabilizes(self):
        self.health_pool.current_hp = -7
        self.health_pool.temporary_hp = 0
        self.health_pool.death_save_failures=2
        self.health_pool.add_temporary_hp(7)
        self.assertEqual(self.health_pool.temporary_hp, 7)
        self.assertEqual(self.health_pool.death_save_failures, 0)

    def test_remove_hp_works_with_temporary_hp(self):
        self.health_pool.remove_hp(10)
        self.assertEqual(self.health_pool.current_hp, 5)
        self.assertEqual(self.health_pool.temporary_hp, 0)

    def test_remove_hp_when_down_adds_death_save_failure(self):
        self.health_pool.temporary_hp = 0
        self.health_pool.remove_hp(10)
        self.assertEqual(self.health_pool.is_conscious(), False)
        self.assertEqual(self.health_pool.death_save_failures, 0)
        self.health_pool.remove_hp(5)
        self.assertEqual(self.health_pool.death_save_failures, 1)

    def test_remove_hp_instant_kill(self):
        self.health_pool.temporary_hp = 0
        self.health_pool.remove_hp(19)
        self.assertEqual(self.health_pool.is_conscious(), False)
        self.assertEqual(self.health_pool.is_dead(), False)
        self.assertEqual(self.health_pool.current_hp, 0)
        self.health_pool.remove_hp(10)
        self.assertEqual(self.health_pool.is_dead(), True)

    def test_remove_hp_keeps_hp_at_zero(self):
        self.health_pool.temporary_hp=0
        self.health_pool.remove_hp(11)
        self.assertEqual(self.health_pool.current_hp, 0)

    def test_is_stabilized(self):
        # Success Case
        self.health_pool.death_save_successes = 3
        is_stabilized = self.health_pool.is_stabilized()
        self.assertEqual(is_stabilized, True)

        # Failure Case
        self.health_pool.death_save_successes = 2
        is_stabilized = self.health_pool.is_stabilized()
        self.assertEqual(is_stabilized, False)

    def test_is_dead(self):
        is_dead = self.health_pool.is_dead()
        self.assertEqual(is_dead, False)

        self.health_pool.death_save_failures = 3
        is_dead = self.health_pool.is_dead()
        self.assertEqual(is_dead, True)

    @patch('health_pool.roll_d20')
    def test_roll_death_save(self, roll_d20_mock):
        roll_d20_mock.return_value = 10
        self.health_pool.roll_death_save()
        self.assertEqual(self.health_pool.death_save_successes, 1)
        self.assertEqual(self.health_pool.death_save_failures, 0)
        roll_d20_mock.return_value = 9
        self.health_pool.roll_death_save()
        self.assertEqual(self.health_pool.death_save_failures, 1)

    @patch('health_pool.roll_d20')
    def test_roll_death_save_critical(self, roll_d20_mock):
        roll_d20_mock.return_value = 20
        self.health_pool.death_save_failures = 2
        self.health_pool.death_save_successes = 2
        self.health_pool.roll_death_save()
        self.assertEqual(self.health_pool.death_save_successes, 0)
        self.assertEqual(self.health_pool.death_save_failures, 0)
        self.assertEqual(self.health_pool.current_hp, 1)

    # TODO: Add hit die test cases. I got bored. Come back later.


if __name__ == '__main__':
    unittest.main()