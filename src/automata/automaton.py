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
            if len(states) <= 0:
                return State(name='empty', is_final=False)

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

        # Queue will hold tuples of set of states and correspondant merged state
        state_tuple = (evaluator.current_states, merge_states(evaluator.current_states),)
        states += (state_tuple[1], )
        queue.put(state_tuple)

        while not queue.empty():
            state_tuple = queue.get()

            for symbol in symbols:
                evaluator.current_states = state_tuple[0]
                evaluator.process_symbol(symbol)

                new_state_tuple = (evaluator.current_states, merge_states(evaluator.current_states), )

                if new_state_tuple[1] not in states:
                    # If state not in states, add it
                    states += (new_state_tuple[1], )
                    queue.put(new_state_tuple)
                    # Add transition into new state
                    transitions += (Transition(initial_state=state_tuple[1], symbol=symbol, final_state=new_state_tuple[1]),)
                else:
                    # Add transition into already existing state
                    # This prevents from creating Transitions into equivalent States which are not the same object in memory
                    for state in states:
                        if state == new_state_tuple[1]:
                            transitions += (Transition(initial_state=state_tuple[1], symbol=symbol, final_state=state), )
                            break

        return FiniteAutomaton(
            initial_state = states[0],
            states = states,
            symbols = symbols,
            transitions = transitions
        )

    def to_minimized(
        self,
    ) -> "FiniteAutomaton":
    #Minimize AFDWW

        from automata.automaton_evaluator import FiniteAutomatonEvaluator

        symbols: Collection[str] = self.symbols
        states: Collection[State] = tuple()
        transitions: Collection[Transition] = tuple()
        
        #Se recorre el autómata y se guardan los estados transitados en un auxiliar.
        #Este se compara con el inicial para detectar los estados inaccesibles y eliminarlos.
        queue = Queue()
        evaluator = FiniteAutomatonEvaluator(self)

        queue.put(evaluator.current_states[0])

        while not queue.empty():
            state = queue.get()
            
            if state not in states:
                states += (state,)

                for symbol in symbols:
                    evaluator.proccess_symbol(symbol)
                    transitions += (Transition(initial_state=state, symbol=symbol, final_state=evaluator.current_states[0]),)

                    queue.put(evaluator.current_states[0])

        # Minimize symbols
        symbols = tuple()
        for transition in transitions:
            if transition.symbol not in symbols:
                symbols += (transition.symbol,)
        # States, transitions and symbols should be complete

        # Estados equivalentes
        # Construir la primera relación de equivalencia
        eq = [[], []]
        for state in states:
            if state.is_final:
                eq[1].append(state)
            else:
                eq[0].append(state)

        new_eq = None
        while True:
            # Calcular nueva relación de equivalencia new_eq
            for eq_class in eq:
                # All possible combinations of two items for eq_class
                pairs = [(a,b) for idx, a in enumerate(eq_class) for b in eq_class[idx + 1:]]
                for pair in pairs:
                    pass
                    # Comparar si son indistinguibles
                    # Si lo son, crear una nueva clase de equivalencia

            if new_eq == eq:
                break
            eq = new_eq

        return FiniteAutomaton(
            initial_state=None,
            states=None,
            symbols=None,
            transitions=None
        )
