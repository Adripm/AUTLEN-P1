"""Automaton implementation."""
from typing import Collection

from queue import Queue

from automata.interfaces import (
    AbstractFiniteAutomaton,
    AbstractState,
    AbstractTransition,
)

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

    def to_deterministic(
        self,
    ) -> "FiniteAutomaton":
        # AFN-l to AFD

        from automata.automaton_evaluator import FiniteAutomatonEvaluator

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
        #Minimize AFD

        # TODO: reducir repetición de código

        from automata.automaton_evaluator import FiniteAutomatonEvaluator

        evaluator = FiniteAutomatonEvaluator(self)

        symbols: Collection[str] = tuple()
        states: Collection[State] = tuple()
        transitions: Collection[Transition] = tuple()

        # Construir primera clase de equivalencia
        eq = list()
        for state in self.states:
            if states.is_final:
                eq.append(1)
            else:
                eq.append(0)

        n_states = len(eq)
        expected = None

        while True:
            new_eq = [None for _ in range(n_states)] # List containing n_states 'None' items

            # Identificar inicio de clase
            eqclasses = list(set(eq)) # List of all unique classes present
            n_classes = len(eqclasses)
            expected = list() # List of expected results after transition for each equivalence class and symbol
            for eqclass,index in eq:
                if eqclass in eqclasses:
                    eqclasses.remove(eqclass)
                    new_eq[index] = eqclass

                    # Calculate expected results
                    state = self.states[index]
                    result = list()
                    for symbol in self.symbols:
                        evaluator.current_states = set(state)
                        evaluator.process_symbol(symbol)
                        result.append(eq[self.states.index(evaluator.current_states[0])])

                    expected.append(result)

            # for class, for state, comprobar si continuan en la misma clase
            for eqclass,index in new_eq:
                if eqclass is None:
                    expected_eqclass = eq[index]
                    expected_transition = expected[expected_eqclass]

                    # Calculate transition and compare with expected results
                    state = self.states[index]
                    result = list()
                    for symbol in self.symbols:
                        evaluator.current_states = set(state)
                        evaluator.process_symbol(symbol)
                        result.append(eq[self.states.index(evaluator.current_states[0])])

                    if result == expected_transition:
                        new_eq[index] = expected_eqclass
                    # else, remains empty

            # crear nuevas clases
            while None in new_eq:
                new_class = n_classes
                n_classes += 1

                index = new_eq.index(None)
                new_eq[index] = new_class

                # Expected class transition
                state = self.states[index]
                result = list()
                for symbol in self.symbols:
                    evaluator.current_states = set(state)
                    evaluator.process_symbol(symbol)
                    result.append(eq[self.states.index(evaluator.current_states[0])])
                expected.append(result)

                for eqclass,n_class in new_eq:
                    if eqclass is None:
                        # Check if matches expected transitions from new class
                        result = list()
                        for symbol in self.symbols:
                            evaluator.current_states = set(self.states[n_class])
                            evaluator.process_symbol(symbol)
                            result.append(eq[self.states.index(evaluator.current_states[0])])

                        if result == expected[-1]: # last element added to expected list will always be the new class
                            new_eq[n_class] = new_class

            if eq == new_eq:
                break # break loop
            else:
                eq = new_eq # continue

        # eq == new_eq
        # Clases de equivalencia completas
        # Construir nuevo autómata

        # Crear clases a partir de clases de equivalencia
        for unique_class in sorted(set(eq)):
            for eqclass,index in eq:
                to_merge = tuple()

                if unique_class == eqclass:
                    to_merge += (self.states[index],)

            states += (merge_states(to_merge),)

        # Crear transiciones a partir de las transiciones esperadas en la lista 'expected'
        for ts,ts_index in expected:
            for symbol,symbol_index in self.symbols:
                transitions = (Transition(initial_state=states[index], symbol=symbol, final_state=states[ts[symbol_index]]),)

        # Crear simbolos
        for transition in transitions:
            if transition.symbol not in symbols:
                symbols += (transition.symbol,)


        return FiniteAutomaton(
            initial_state=states[0], # should be correspondant to equivalence class 0 since they were added sorted in order
            states=states,
            symbols=symbols,
            transitions=transitions
        )
