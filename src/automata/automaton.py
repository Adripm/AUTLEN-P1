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

    def to_deterministic(
        self,
    ) -> "FiniteAutomaton":
        # AFN-l to AFD

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

        # Minimization Algorithm details
        #######################################################################
        # -> build transition table
        # -> build first equivalence class
        # -- while neweq != eq:
        #       -> build specific transition table using equivalence classes
        #       -> mark start of each class
        #       -- for each empty in neweq:
        #               -- if transitions are equal:
        #                       -> mark in neweq as class
        #               -- else:
        #                       -> mark in neweq as empty
        #       -- while empty in neweq:
        #               -> create new class
        #               -> mark first empty as new class in neweq
        #               -- for each empty in neweq:
        #                       -- if transitions are equal:
        #                               -> mark in neweq as class
        #                       -- else:
        #                               -> mark in neqew as empty
        #######################################################################

        symbols: Collection[str] = tuple()
        states: Collection[State] = tuple()
        transitions: Collection[Transition] = tuple()

        # Construir la tabla de transiciones
        transitions_table = {}
        class_transitions_table = {} # used later
        for t in self.transitions:
            if t.initial_state not in transitions_table:
                transitions_table[t.initial_state] = {}
            transitions_table[t.initial_state][t.symbol] = t.final_state

        # Construir primera clase de equivalencia
        eq = {}
        for s in self.states:
            if s.is_final:
                eq[s] = 1
            else:
                eq[s] = 0

        class_indexes = {} # used later

        while True:
            # initialize new_eq
            new_eq = {}
            for s in self.states:
                new_eq[s] = None

            # Identificar inicio de clase
            unique_eqclasses = list(set(eq.values())) # List of all uinque classes present in eq
            next_class = len(unique_eqclasses)
            for s,cls in eq.items():
                if cls in unique_eqclasses:
                    unique_eqclasses.remove(cls)
                    new_eq[s] = cls
                    class_indexes[cls] = s

            # Calcular tabla de transiciones hacia clases
            class_transitions_table = {}
            for s,d in transitions_table.items():
                class_transitions_table[s] = {}
                for t,f in d.items():
                    class_transitions_table[s][t] = eq[f]

            # for each empty, check if remains in same class
            for s,cls in new_eq.items():
                if cls is None:
                    # check if remains in class
                    if class_transitions_table[s] == class_transitions_table[class_indexes[eq[s]]]:
                        # remains in class
                        new_eq[s] = eq[s]
                    # else, does not remain in class

            # next_class = len(unique_eqclasses)
            while None in new_eq:
                first = None
                for s,cls in new_eq.items():
                    if cls is None:
                        if first is None:
                            first = s
                            new_eq[s] = next_class
                        else:
                            # compare with next_class
                            if class_transitions_table[s] == class_transitions_table[first]:
                                # same class
                                new_eq[s] = next_class
                            pass
                next_class += 1

            if eq == new_eq:
                break # break loop
            else:
                eq = new_eq # continue

        # Clases de equivalencia completas
        # Construir nuevo automata finito a partir de clase de equivalencia 'eq' y tabla 'class_transitions_table'

        # simplificar clases fusionando estados que estén en la misma clase
        # es decir, eliminar duplicados
        for s in class_indexes.values():
            states += (s,)

        # set initial state
        initial_state = class_indexes[eq[self.initial_state]]

        # calculate transitions
        for s,d in class_transitions_table.items():
            if s in states:
                for symbol, f in d.items():
                    transitions += (Transition(initial_state=s, symbol=symbol, final_state=class_indexes[f]),)

                    if symbol not in symbols: # this may simplify unused symbols
                        symbols += (symbol, )

        print('Initial state: ',initial_state)
        print('States: ', states)
        print('Symbols: ', symbols)
        print('Transitions: ', transitions)

        return FiniteAutomaton(
            initial_state=initial_state,
            states=states,
            symbols=symbols,
            transitions=transitions
        )
