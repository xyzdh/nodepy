import init
from nodepy.bind import Bind

if __name__ == '__main__':
    def callback_two(value, old_value):
        print("--------\n", "I'm a static method\n",
              value, "\n", old_value)
    class TEST():

        def __init__(self):
            self.var = Bind()
            self.var.bind(self.callback_one)
            self.var.bind(callback_two)

        def callback_one(self, value, old_value):
            print("--------\n", "I'm a normal method\n",
                  value, "\n", old_value)

        def condition(self, value, old_value):
            if old_value != None:
                return True

    test = TEST()

    test.var("will call <self.call_no_value>")