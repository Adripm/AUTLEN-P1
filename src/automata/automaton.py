"""Automaton implementation."""
from typing import Collection

from queue import Queue

from automata.interfaces import (
    AbstractFiniteAutomaton,
    AbstractState,
    AbstractTransition,
)


class State(AbstractState):
    """State of an automaton."""

    # You can add new attributes and methods that you think that make your
    # task easier, but you cannot change the constructor interface.


class Transition(AbstractTransition[State]):
    """Transition of an automaton."""

    # You can add new attributes and methods that you think that make your
    # task easier, but you cannot change the constructor interface.


class FiniteAutomaton(
    AbstractFiniteAutomaton[State, Transition],
):
    """Automaton."""

    def __init__(
        self,
        *,
        initial_state: State,
        states: Collection[State],
        symbols: Collection[str],
        transitions: Collection[Transition],
    ) -> None:
        super().__init__(
            initial_state=initial_state,
            states=states,
            symbols=symbols,
            transitions=transitions,
        )

        # Add here additional initialization code.
        # Do not change the constructor interface

    ## TODO: Incluir estado sumidero ?
    def to_deterministic(
        self,
    ) -> "FiniteAutomaton":
        # AFN-l to AFD

        from automata.automaton_evaluator import FiniteAutomatonEvaluator

        # Auxiliar function
        def merge_states(states: Collection[State]) -> State:
            name = ''
            is_final = False
            for state in states:
                name += state.name
                if state.is_final:
                    is_final = True
            return State(name=name, is_final=is_final)

        symbols: Collection[str] = self.symbols
        states: Collection[State] = tuple() # Empty tuple
        transitions: Collection[Transition] = tuple()

        queue = Queue()
        evaluator = FiniteAutomatonEvaluator(self)

        initial_states = evaluator.current_states
        queue.put(initial_states)

        # Add initial state to states
        merged_initial_state = merge_states(initial_states)
        states += (merged_initial_state, )

        while not queue.empty():
            evaluating_states = queue.get() # Set of states
            merged_evaluating_state = merge_states(evaluating_states)

            for symbol in symbols:
                evaluator.current_states = evaluating_states
                evaluator.process_symbol(symbol)

                merged_final_state = merge_states(evaluator.current_states)

                transitions += (Transition(initial_state=merged_evaluating_state, symbol=symbol, final_state=merged_final_state), )

                if merged_final_state not in states:
                    states += (merged_final_state, )
                    queue.put(evaluator.current_states, )

        return FiniteAutomaton(
            initial_state = merged_initial_state,
            states = states,
            symbols = symbols,
            transitions = transitions
        )

    def to_minimized(
        self,
    ) -> "FiniteAutomaton":
        raise NotImplementedError("This method must be implemented.")
