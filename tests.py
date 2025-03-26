import interpreter

def test_reset():
    assert interpreter.BrainfuckInterpreter("++!.").run() == chr(0)

def test_random():
    assert interpreter.BrainfuckInterpreter("?.").run() != chr(0) #probably

def test_module():
    assert interpreter.BrainfuckInterpreter("++{add5.bfm}>+++++{2}.").run() == chr(10)

def test_increment():
    assert interpreter.BrainfuckInterpreter("+++++.").run() == chr(5)

def test_decrement():
    assert interpreter.BrainfuckInterpreter("+++++----.").run() == chr(1)

def test_pointer_movement():
    assert interpreter.BrainfuckInterpreter("++>++++<-.").run() == chr(1)

def test_loop():
    assert interpreter.BrainfuckInterpreter("+++[>++++<-]>.").run() == chr(12)

def test_input_output():
    interpreter_instance = interpreter.BrainfuckInterpreter(",.", input_data="A")
    assert interpreter_instance.run() == "A"

def test_overflow():
    assert interpreter.BrainfuckInterpreter("-.").run() == chr(255)
    assert interpreter.BrainfuckInterpreter("+" * 256 + ".").run() == chr(0)

def test_nested_loops():
    assert interpreter.BrainfuckInterpreter("++[>++[>++<-]<-]>>.").run() == chr(8)

def test_large_program():
    program = ">" * 1000 + "+" * 255 + "."
    assert interpreter.BrainfuckInterpreter(program).run() == chr(255)