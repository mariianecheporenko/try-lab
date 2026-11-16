"""Core parser and interpreter integration test."""

from src.interpreter import Interpreter
from src.parser import parse


def test_parse_and_execute_loop_program():
    source = """
    begin
        X := 0;
        Y := 0;
        while 3 > X do begin
            X := X + 1;
            Y := Y + 2
        end
    end
    """

    program = parse(source)
    interpreter = Interpreter(trace=False)
    final_state = interpreter.execute(program)

    assert final_state["X"] == 3
    assert final_state["Y"] == 6
