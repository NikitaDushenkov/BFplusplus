import sys
import random
import requests

class BrainfuckInterpreter:
    def __init__(self, code, input_data=""):
        self.code = code
        self.input_data = input_data
        self.data = [0] * 30000
        self.data_pointer = 0
        self.code_pointer = 0
        self.input_pointer = 0
        self.bracket_map = self.build_bracket_map()
        self.modules = {}
    
    def error(self, message):
        r = requests.get('https://bofh-api.bombeck.io/v1/excuses/random/')
        if r.status_code != 200:
            raise SyntaxError("no internet sad" + message)
        else:
            raise SyntaxError(r.json()[0]['quote'] + " " + message)
    
    def build_bracket_map(self):
        stack = []
        bracket_map = {}
        for i, char in enumerate(self.code):
            if char == "[":
                stack.append(i)
            elif char == "]":
                if not stack:
                    self.error("Unmatched closing bracket at position {}".format(i))
                start = stack.pop()
                bracket_map[start] = i
                bracket_map[i] = start
        if stack:
            self.error("Unmatched opening bracket at position {}".format(stack.pop()))
        return bracket_map

    def run(self):
        output = []
        while self.code_pointer < len(self.code):
            command = self.code[self.code_pointer]
            if command == ">":
                self.data_pointer = (self.data_pointer + 1) % len(self.data)
            elif command == "<":
                self.data_pointer = (self.data_pointer - 1) % len(self.data)
            elif command == "+":
                self.data[self.data_pointer] = (self.data[self.data_pointer] + 1) % 256
            elif command == "-":
                self.data[self.data_pointer] = (self.data[self.data_pointer] - 1) % 256
            elif command == ".":
                output.append(chr(self.data[self.data_pointer]))
            elif command == ",":
                if self.input_pointer < len(self.input_data):
                    self.data[self.data_pointer] = ord(self.input_data[self.input_pointer])
                    self.input_pointer += 1
                else:
                    self.data[self.data_pointer] = 0
            elif command == "[":
                if self.data[self.data_pointer] == 0:
                    self.code_pointer = self.bracket_map[self.code_pointer]
            elif command == "]":
                if self.data[self.data_pointer] != 0:
                    self.code_pointer = self.bracket_map[self.code_pointer]
            elif command == "?":
                    self.data[self.data_pointer] = random.randint(0, 255)
            elif command == "!":
                self.data[self.data_pointer] = 0
            elif command == '{':
                end_index = self.code.find('}', self.code_pointer)
                if end_index == -1:
                    self.error("Unmatched '{'")
                module_name = self.code[self.code_pointer + 1:end_index]
                if module_name.isnumeric():
                    module_name = int(module_name)
                    if module_name in self.modules:
                        self.data[self.data_pointer] = ord(self.run_module(module_name))
                    else:
                        self.error(f"Module with ID {module_name} not found.")
                else:
                    self.load_module(module_name, self.data[self.data_pointer])
                    self.code_pointer = end_index
            self.code_pointer += 1
        return "".join(output)
    def load_module(self, module_name, module_index):
        try:
            with open(module_name, 'r') as module_file:
                module_code = module_file.read()
                self.modules[module_index] = module_code
        except FileNotFoundError:
            self.error(f"Module '{module_name}' not found.")

    def run_module(self, module_id):
        module_code = self.modules[module_id]
        input_char = chr(self.data[self.data_pointer])
        sub_interpreter = BrainfuckInterpreter(module_code, input_char)
        return sub_interpreter.run()
        



if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python interpreter.py <brainfuck_code> [input_data]")
        sys.exit(1)

    code = sys.argv[1]
    input_data = sys.argv[2] if len(sys.argv) > 2 else ""

    interpreter = BrainfuckInterpreter(code, input_data)
    print(interpreter.run())