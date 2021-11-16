"""Test minimization of automatas."""
import unittest
from abc import ABC

from automata.automaton import FiniteAutomaton
from automata.utils import AutomataFormat, deterministic_automata_isomorphism, write_dot
import inspect
import os
import sys

class TestMinimize(ABC, unittest.TestCase):
    """Base class for string acceptance tests."""

    def _dot(self, aut, trans):
        dir = 'dots'
        imgs = 'imgs'

        testname = inspect.stack()[2][3]
        classname = self.__class__.__name__

        if not os.path.exists(dir):
            os.makedirs(dir)
        if not os.path.exists(imgs):
            os.makedirs(imgs)

        filename1 = dir+'/'+classname+'-'+testname+'-original.txt'
        filename2 = dir+'/'+classname+'-'+testname+'-result.txt'

        filename3 = imgs+'/'+classname+'-'+testname+'.jpg'

        with open(filename1, 'w') as file:
            file.write(write_dot(aut))
        with open(filename2, 'w') as file:
            file.write(write_dot(trans))

        os.system('gvpack -u '+filename2+' '+filename1+' | dot -Tjpg -o'+filename3)

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

        # self._dot(automaton, transformed) # Enable to generate images

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

    def test_case2(self) -> None:
        automaton_str="""
        Automaton:
            Symbols: 01

            q0
            q1
            q2
            q3 final

            --> q0
            q0 -0-> q1
            q1 -0-> q2
            q2 -0-> q1
            q1 -0-> q0

            q1 -1-> q1

            q0 -1-> q3
            q2 -1-> q3

            q3 -0-> q3
            q3 -1-> q3
        """

        expected_str="""
        Automaton:
            Symbols: 01

            q0
            q1
            q2 final

            --> q0
            q0 -0-> q1
            q0 -1-> q2

            q1 -0-> q0
            q1 -1-> q1

            q2 -0-> q2
            q2 -1-> q2
        """

        automaton = AutomataFormat.read(automaton_str)
        expected = AutomataFormat.read(expected_str)

        self._check_transform(automaton, expected)

    def test_case3(self) -> None:
        automaton_str = """
        Automaton:
            Symbols: 01

            q0
            q1
            q2
            q3
            q4 final
            q5 final

            --> q0
            q0 -0-> q1
            q0 -1-> q2

            q1 -0-> q3
            q1 -1-> q4

            q2 -0-> q3
            q2 -1-> q5

            q3 -0-> q3
            q3 -1-> q3

            q4 -0-> q4
            q4 -1-> q4

            q5 -0-> q5
            q5 -1-> q5
        """

        expected_str = """
        Automaton:
            Symbols: 01

            q0
            q1
            q2
            q3 final

            --> q0
            q0 -0-> q1
            q0 -1-> q1

            q1 -0-> q2
            q1 -1-> q3

            q2 -0-> q2
            q2 -1-> q2

            q3 -0-> q3
            q3 -1-> q3
        """

        automaton = AutomataFormat.read(automaton_str)
        expected = AutomataFormat.read(expected_str)

        self._check_transform(automaton, expected)

    def test_case4(self) -> None:
        automaton_str = """
        Automaton:
            Symbols: 01

            q0
            q1
            q2
            q3 final

            --> q0
            q0 -0-> q1
            q1 -0-> q2
            q2 -0-> q3

            q0 -1-> q0
            q1 -1-> q1
            q2 -1-> q2
            q3 -1-> q3
        """

        automaton = AutomataFormat.read(automaton_str)

        self._check_transform(automaton, automaton) # minimized version is the same

    def test_case5(self) -> None:
        automaton_str = """
        Automaton:
            Symbols: 01

            q0
            q1
            q2 final
            q3 final
            q4 final
            q5

            --> q0

            q0 -0-> q1
            q0 -1-> q2

            q1 -0-> q0
            q1 -1-> q3

            q2 -0-> q4
            q2 -1-> q5

            q3 -0-> q4
            q3 -1-> q5

            q4 -0-> q4
            q4 -1-> q5

            q5 -0-> q5
            q5 -1-> q5
        """

        expected_str = """
        Automaton:
            Symbols: 01

            q0
            q1 final
            q2

            --> q0

            q0 -0-> q0
            q0 -1-> q1

            q1 -0-> q1
            q1 -1-> q2

            q2 -0-> q2
            q2 -1-> q2
        """

        automaton = AutomataFormat.read(automaton_str)
        expected = AutomataFormat.read(expected_str)

        self._check_transform(automaton, expected)

if __name__ == '__main__':
    unittest.main()
