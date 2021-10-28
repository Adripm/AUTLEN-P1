"""Evaluation of automata."""
from typing import Set

from automata.automaton import FiniteAutomaton, State
from automata.interfaces import AbstractFiniteAutomatonEvaluator

from queue import Queue

class FiniteAutomatonEvaluator(
    AbstractFiniteAutomatonEvaluator[FiniteAutomaton, State],
):
    """Evaluator of an automaton."""

    def process_symbol(self, symbol: str) -> None:
        # If this symbol can be processed by any of the states, it does, else raises an Exception
        new_states: Set[State] = set()

        if symbol not in self.automaton.symbols:
            raise ValueError("Symbol \'"+(symbol)+"\' is not accepted by this automaton. Accepted symbols: "+str(self.automaton.symbols))

        for transition in self.automaton.transitions:
            if transition.initial_state in self.current_states and transition.symbol == symbol and transition.final_state not in new_states:
                new_states.add(transition.final_state)

        self._complete_lambdas(new_states)
        self.current_states = new_states

    def _complete_lambdas(self, set_to_complete: Set[State]) -> None:
        # Breadth-First Search
        queue = Queue()
        for item in set_to_complete:
            queue.put(item)

        while not queue.empty():
            state = queue.get()
            # For each state, search for lambda transitions and add them to the queue
            for transition in self.automaton.transitions:
                if transition.initial_state == state and transition.symbol == None and transition.final_state not in set_to_complete:
                    # Add to set completed with lambdas and push to queue
                    set_to_complete.add(transition.final_state)
                    queue.put(transition.final_state)
        return

    def is_accepting(self) -> bool:

        for state in self.current_states:
            if state.is_final:
                return True

        return False
