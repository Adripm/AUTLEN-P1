"""Test minimization of automatas."""
import unittest
from abc import ABC

from automata.automaton import FiniteAutomaton
from automata.utils import AutomataFormat, deterministic_automata_isomorphism, write_dot

class TestMinimize(ABC, unittest.TestCase):
    """Base class for string acceptance tests."""

    def _check_transform(
        self,
        automaton: FiniteAutomaton,
        expected: FiniteAutomaton,
    ) -> None:
        """Test that the minimized automaton is as expected."""

        transformed = automaton.to_minimized()

        equiv_map = deterministic_automata_isomorphism(
            expected,
            transformed,
        )

        self.assertTrue(equiv_map is not None)

    def test_case1(self) -> None:
        """Test Case 1."""
        automaton_str = """
        Automaton:
            Symbols: 01

            q0
            q1
            q2 final

            --> q0
            q0 -0-> q1
            q1 -0-> q0

            q0 -1-> q2
            q1 -1-> q2

            q2 -0-> q2
            q2 -1-> q2
        """

        expected_str = """
        Automaton:
            Symbols: 01

            q0
            q1 final

            --> q0
            q0 -0-> q0
            q0 -1-> q1

            q1 -0-> q1
            q1 -1-> q1
        """

        automaton = AutomataFormat.read(automaton_str)
        expected = AutomataFormat.read(expected_str)

        self._check_transform(automaton, expected)

    # def test_case2(self) -> None:
    #     pass
    #
    # def test_case3(self) -> None:
    #     pass
    #
    # def test_case4(self) -> None:
    #     pass

if __name__ == '__main__':
    unittest.main()
