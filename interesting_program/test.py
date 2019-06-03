import sys
import io
import unittest
import importlib


def stub_stdin(testcase_inst, inputs):
    stdin = sys.stdin
    def cleanup():
        sys.stdin = stdin

    testcase_inst.addCleanup(cleanup)
    sys.stdin = io.StringIO(inputs)

def stub_stdout(testcase_inst):
    stderr = sys.stderr
    stdout = sys.stdout

    def cleanup():
        sys.stderr = stderr
        sys.stdout = stdout

    testcase_inst.addCleanup(cleanup)
    sys.stderr = io.StringIO()
    sys.stdout = io.StringIO()

def test_import(slf, file, result, input_value = None, second = False):
	if input is not None:
		stub_stdin(slf, input_value)
	stub_stdout(slf)
	if second:
		exec("importlib.reload(" + file + ")")
	else:
		exec("import " + file)
	slf.assertEqual(str(sys.stdout.getvalue()), result)

class Test(unittest.TestCase):
	def test(self):
		test_import(self, "fibonacci", "1\n1\n2\n3\n5\n8\n13\n21\n34\n55\n")
		test_import(self, "lcm", "120\n", "24\n30\n")
		test_import(self, "mcd", "6\n", "24\n30\n")
		test_import(self, "leap_year", "True\n", "2000\n")
		test_import(self, "calculator", ">>>3.0*5.0 = 15.0\n", "3*5\n")
		test_import(self, "calculator", ">>>4.5-3.5*2.0 = -2.5\n", "4.5-3.5*2\n",second = True)
unittest.main()
