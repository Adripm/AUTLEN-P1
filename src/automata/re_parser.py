"""Conversion from regex to automata."""
from automata.automaton import FiniteAutomaton
from automata.re_parser_interfaces import AbstractREParser


class REParser(AbstractREParser):
    """Class for processing regular expressions in Kleene's syntax."""

    def _create_automaton_empty(
        self,
    ) -> FiniteAutomaton:

        initial_state = State(name='final', is_final=True)
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

        state1 = State(name='initial', is_final=False)
        state2 = State(name='final', is_final=True)
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

        state1 = State(name='initial', is_final=False)
        state2 = State(name='final', is_final=True)
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
        # raise NotImplementedError("This method must be implemented.")
        return None

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
