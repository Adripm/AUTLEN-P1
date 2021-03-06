"""Test evaluation of automatas."""
import unittest
from abc import ABC

from automata.automaton import FiniteAutomaton
from automata.utils import AutomataFormat, deterministic_automata_isomorphism, write_dot
import os
import sys
import inspect

class TestTransform(ABC, unittest.TestCase):
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
        """Test that the transformed automaton is as the expected one."""
        transformed = automaton.to_deterministic()

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
            qf final

            --> q0
            q0 -0-> qf
        """

        automaton = AutomataFormat.read(automaton_str)

        expected_str = """
        Automaton:
            Symbols: 01

            q0
            qf final
            empty

            --> q0
            q0 -0-> qf
            q0 -1-> empty
            qf -0-> empty
            qf -1-> empty
            empty -0-> empty
            empty -1-> empty

        """

        expected = AutomataFormat.read(expected_str)

        self._check_transform(automaton, expected)

    def test_case2(self) -> None:
        """Test Case 2"""
        automaton_str = """
        Automaton:
            Symbols: 0123456789+-.

            q0
            q1
            q2
            q3
            q4
            q5 final

            --> q0
            q0 -+-> q1
            q0 ---> q1
            q0 --> q1

            q1 -0-> q1
            q1 -1-> q1
            q1 -2-> q1
            q1 -3-> q1
            q1 -4-> q1
            q1 -5-> q1
            q1 -6-> q1
            q1 -7-> q1
            q1 -8-> q1
            q1 -9-> q1

            q1 -.-> q2

            q2 -0-> q3
            q2 -1-> q3
            q2 -2-> q3
            q2 -3-> q3
            q2 -4-> q3
            q2 -5-> q3
            q2 -6-> q3
            q2 -7-> q3
            q2 -8-> q3
            q2 -9-> q3

            q1 -0-> q4
            q1 -1-> q4
            q1 -2-> q4
            q1 -3-> q4
            q1 -4-> q4
            q1 -5-> q4
            q1 -6-> q4
            q1 -7-> q4
            q1 -8-> q4
            q1 -9-> q4

            q4 -.-> q3

            q3 -0-> q3
            q3 -1-> q3
            q3 -2-> q3
            q3 -3-> q3
            q3 -4-> q3
            q3 -5-> q3
            q3 -6-> q3
            q3 -7-> q3
            q3 -8-> q3
            q3 -9-> q3

            q3 --> q5
        """

        expected_str = """
        Automaton:
            Symbols: 0123456789+-.

            q0q1
            q1
            q1q4
            q2
            q2q3q5 final
            q3q5 final
            empty

            --> q0q1
            q0q1 -+-> q1
            q0q1 ---> q1
            q0q1 -.-> q2
            q0q1 -0-> q1q4
            q0q1 -1-> q1q4
            q0q1 -2-> q1q4
            q0q1 -3-> q1q4
            q0q1 -4-> q1q4
            q0q1 -5-> q1q4
            q0q1 -6-> q1q4
            q0q1 -7-> q1q4
            q0q1 -8-> q1q4
            q0q1 -9-> q1q4

            q1 -.-> q2
            q1 -0-> q1q4
            q1 -1-> q1q4
            q1 -2-> q1q4
            q1 -3-> q1q4
            q1 -4-> q1q4
            q1 -5-> q1q4
            q1 -6-> q1q4
            q1 -7-> q1q4
            q1 -8-> q1q4
            q1 -9-> q1q4

            q1q4 -.-> q2q3q5
            q1q4 -0-> q1q4
            q1q4 -1-> q1q4
            q1q4 -2-> q1q4
            q1q4 -3-> q1q4
            q1q4 -4-> q1q4
            q1q4 -5-> q1q4
            q1q4 -6-> q1q4
            q1q4 -7-> q1q4
            q1q4 -8-> q1q4
            q1q4 -9-> q1q4

            q2 -0-> q3q5
            q2 -1-> q3q5
            q2 -2-> q3q5
            q2 -3-> q3q5
            q2 -4-> q3q5
            q2 -5-> q3q5
            q2 -6-> q3q5
            q2 -7-> q3q5
            q2 -8-> q3q5
            q2 -9-> q3q5

            q2q3q5 -0-> q3q5
            q2q3q5 -1-> q3q5
            q2q3q5 -2-> q3q5
            q2q3q5 -3-> q3q5
            q2q3q5 -4-> q3q5
            q2q3q5 -5-> q3q5
            q2q3q5 -6-> q3q5
            q2q3q5 -7-> q3q5
            q2q3q5 -8-> q3q5
            q2q3q5 -9-> q3q5

            q3q5 -0-> q3q5
            q3q5 -1-> q3q5
            q3q5 -2-> q3q5
            q3q5 -3-> q3q5
            q3q5 -4-> q3q5
            q3q5 -5-> q3q5
            q3q5 -6-> q3q5
            q3q5 -7-> q3q5
            q3q5 -8-> q3q5
            q3q5 -9-> q3q5

            q1 -+-> empty
            q1 ---> empty
            q1q4 -+-> empty
            q1q4 ---> empty
            q2 -+-> empty
            q2 ---> empty
            q2 -.-> empty
            q2q3q5 -+-> empty
            q2q3q5 ---> empty
            q2q3q5 -.-> empty
            q3q5 -+-> empty
            q3q5 ---> empty
            q3q5 -.-> empty

            empty -0-> empty
            empty -1-> empty
            empty -2-> empty
            empty -3-> empty
            empty -4-> empty
            empty -5-> empty
            empty -6-> empty
            empty -7-> empty
            empty -8-> empty
            empty -9-> empty
            empty -+-> empty
            empty ---> empty
            empty -.-> empty
        """

        automaton = AutomataFormat.read(automaton_str)
        expected = AutomataFormat.read(expected_str)

        self._check_transform(automaton, expected)

    def test_case3(self) -> None:
        """Test Case 3"""
        automaton_str = """
        Automaton:
            Symbols: 01

            q0
            q1
            q2
            q3
            q4
            q5
            q6 final
            q7

            --> q0
            q0 --> q1
            q0 --> q2
            q2 -0-> q4
            q1 -1-> q5
            q1 -1-> q3
            q5 --> q7
            q5 -0-> q4
            q5 -0-> q3
            q7 --> q6
            q4 -1-> q6
        """

        expected_str = """
        Automaton:
            Symbols: 01

            q0q1q2
            q3q5q6q7 final
            q4
            q3q4
            q6 final
            empty

            --> q0q1q2
            q0q1q2 -0-> q4
            q0q1q2 -1-> q3q5q6q7

            q4 -1-> q6
            q4 -0-> empty

            q3q5q6q7 -0-> q3q4
            q3q5q6q7 -1-> empty

            q3q4 -1-> q6
            q3q4 -0-> empty

            q6 -0-> empty
            q6 -1-> empty

            empty -0-> empty
            empty -1-> empty

        """

        automaton = AutomataFormat.read(automaton_str)
        expected = AutomataFormat.read(expected_str)

        self._check_transform(automaton, expected)

    def test_case4(self) -> None:
        """Test Case 4"""
        automaton_str = """
        Automaton:
            Symbols: 01

            q0
            q1
            qf final

            --> q0
            q0 -0-> q0
            q0 -1-> q0
            q0 -1-> q1

            q1 -1-> qf
        """

        expected_str = """
        Automaton:
            Symbols: 01

            q0
            q0q1
            q0q1qf final

            --> q0
            q0 -0-> q0
            q0 -1-> q0q1

            q0q1 -0-> q0
            q0q1 -1-> q0q1qf

            q0q1qf -1-> q0q1qf
            q0q1qf -0-> q0
        """


        automaton = AutomataFormat.read(automaton_str)
        expected = AutomataFormat.read(expected_str)

        self._check_transform(automaton, expected)

if __name__ == '__main__':
    unittest.main()
