"""Evaluation of automata."""
from typing import Set

from automata.automaton import FiniteAutomaton, State
from automata.interfaces import AbstractFiniteAutomatonEvaluator

import queue

class FiniteAutomatonEvaluator(
    AbstractFiniteAutomatonEvaluator[FiniteAutomaton, State],
):
    """Evaluator of an automaton."""

    def process_symbol(self, symbol: str) -> None:

        raise NotImplementedError("This method must be implemented.")

    def _complete_lambdas(self, set_to_complete: Set[State]) -> None:
        # Breadth-First Search
        queue = Queue()
        for item in set_to_complete:
            queue.put(item)

        while not queue.empty():
            state = queue.get()
            # For each state, search for lambda transitions and add them to the queue
            for transition in self.transitions:
                if transition.initial_state == state and transition.symbol == None and transition.final_state not in set_to_complete:
                    # Add to set completed with lambdas and push to queue
                    set_to_complete.add(transition.final_state)
                    queue.put(transition.final_state)
                else:
                    continue
        return

    def is_accepting(self) -> bool:

        for state in self.current_states:
            if state.is_final:
                return True

        return False
