"""Automaton implementation."""
from typing import Collection

from queue import Queue

from automata.interfaces import (
    AbstractFiniteAutomaton,
    AbstractState,
    AbstractTransition,
    AbstractFiniteAutomatonEvaluator,
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

        #raise NotImplementedError('TODO: fix')

        symbols: Collection[str] = self.symbols
        states: Collection[State] = tuple() # Empty tuple
        transitions: Collection[Transition] = tuple()

        queue = Queue()
        evaluator = AbstractFiniteAutomatonEvaluator[self]

        initial_state = evaluator.current_states # TODO: current_states is not a state but a set of states
        queue.put(initial_state)
        states += (initial_state, )

        while not queue.empty():
            evaluating_state = queue.get()

            for symbol in symbols:
                evaluator.current_states = evaluating_state # TODO: FIX - New state is not in initial automaton
                evaluator.process_symbol(symbol)

                transitions += (Transition(initial_state=evaluating_state, symbol=symbol, final_state=evaluator.current_states), )

                if evaluator.current_states not in states:
                    states += (evaluator.current_states, )
                    queue.put(evaluator.current_states, )

        return FiniteAutomaton(
            initial_state = initial_state,
            states = states,
            symbols = symbols,
            transitions = transitions
        )

    def to_minimized(
        self,
    ) -> "FiniteAutomaton":
        raise NotImplementedError("This method must be implemented.")
