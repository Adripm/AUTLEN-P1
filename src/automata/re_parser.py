"""Conversion from regex to automata."""
from automata.automaton import FiniteAutomaton, State, Transition
from automata.re_parser_interfaces import AbstractREParser


class REParser(AbstractREParser):
    """Class for processing regular expressions in Kleene's syntax."""

    # Utility
    # Returns the current state count as a string and plus ones
    def _add_state(self) -> str:
        self.state_counter+=1
        return 'state'+str(self.state_counter-1)

    def _create_automaton_empty(
        self,
    ) -> FiniteAutomaton:

        initial_state = State(name=self._add_state(), is_final=True)
        states: Collection[State] = {initial_state} # Contains only one state
        symbols: Collection[str] = {} # is empty
        transitions: Collection[Transition] = {} # is empty

        return FiniteAutomaton(
            initial_state = initial_state,
            states = states,
            symbols = symbols,
            transitions = transitions
        )

    def _create_automaton_lambda(
        self,
    ) -> FiniteAutomaton:

        state1 = State(name=self._add_state(), is_final=False)
        state2 = State(name=self._add_state(), is_final=True)
        transition1 = Transition(initial_state=state1, symbol=None, final_state=state2)

        initial_state = state1
        states: Collection[State] = {state1, state2}
        symbols: Collection[str] = {} # is empty
        transitions: Collection[Transition] = {transition1}

        return FiniteAutomaton(
            initial_state = initial_state,
            states = states,
            symbols = symbols,
            transitions = transitions
        )

    def _create_automaton_symbol(
        self,
        symbol: str,
    ) -> FiniteAutomaton:

        state1 = State(name=self._add_state(), is_final=False)
        state2 = State(name=self._add_state(), is_final=True)
        transition1 = Transition(initial_state=state1, symbol=symbol, final_state=state2)

        initial_state = state1
        states: Collection[State] = {state1, state2}
        symbols: Collection[str] = {symbol}
        transitions: Collection[Transition] = {transition1}

        return FiniteAutomaton(
            initial_state = initial_state,
            states = states,
            symbols = symbols,
            transitions = transitions
        )

    def _create_automaton_star(
        self,
        automaton: FiniteAutomaton,
    ) -> FiniteAutomaton:

        initial_state = State(name=self._add_state(), is_final=False)
        final_state = State(name=self._add_state(), is_final=True)

        states: Collection[State] = automaton.states
        symbols: Collection[str] = automaton.symbols
        transitions: Collection[Transition] = automaton.transitions

        # For each final state in inner automaton, connect to new final state with lambda transitions
        # Add transition to inner automaton initial state
        # Final states in inner automaton are no longer final
        for state in automaton.states:
            if state.is_final:
                state.is_final = False
                transitions.add(Transition(initial_state=state, symbol=None, final_state=final_state))
                transitions.add(Transition(initial_state=state, symbol=None, final_state=automaton.initial_state))

        # Add new states to automaton
        states.add(initial_state)
        states.add(final_state)

        # Add transition from new initial state to inner automaton initial state
        transitions.add(Transition(initial_state=initial_state, symbol=None, final_state=automaton.initial_state))

        # Add transition from new initial state to final state
        transitions.add(Transition(initial_state=initial_state, symbol=None, final_state=final_state))

        return FiniteAutomaton(
            initial_state = initial_state,
            states = states,
            symbols = symbols,
            transitions = transitions
        )

    def _create_automaton_union(
        self,
        automaton1: FiniteAutomaton,
        automaton2: FiniteAutomaton,
    ) -> FiniteAutomaton:
        # raise NotImplementedError("This method must be implemented.")
        return None

    def _create_automaton_concat(
        self,
        automaton1: FiniteAutomaton,
        automaton2: FiniteAutomaton,
    ) -> FiniteAutomaton:
        # raise NotImplementedError("This method must be implemented.")
        return None
