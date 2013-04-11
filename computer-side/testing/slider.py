from __future__ import print_function
import functools
import Tkinter as tk

from framework import controller
from framework import util
from core import robot
from config import logs
from config import robot_setup
from config import gui_options


def logger(name, message):
    print ('%s: %s' % (name, message))


class App (util.GUIProcess, controller.ControllerProcess):
    def __init__(self, master=None):
        util.GUIProcess.__init__(self, master)
        bot = robot.Robot(robot_setup.servos,
            functools.partial(logger, 'Robot'))
        controller.ControllerProcess.__init__(self, bot,
            functools.partial(logger, 'Controls'))
        print (str(self.bot))
        self.bot.start()
        controller.ControllerProcess.start(self)

        self.verbosity = logs.testing['slider']

        self.slider = {}
        for name, position in gui_options.names.items():
            caption = tk.Label(self.master, text='%s servo' % name)
            caption.grid(row=position, column=0)
            self.slider[name] = tk.Scale(self.master, from_=0, to=180,
                orient=tk.HORIZONTAL, sliderlength=8, length=600, takefocus=1,
                command=lambda _: self.do())
            self.slider[name].set(self.bot[name].read())
            self.slider[name].grid(row=position, column=1, pady=20)

    def do(self):
        for name, slider in self.slider.items():
            val = slider.get()
            if self.verbosity['name']:
                print(name)
            if self.verbosity['moving']:
                print(val)
            self.bot.direct_move(name, val)

    @staticmethod
    def main(*args, **kwargs):
        root = tk.Tk()
        app = App(root)
        root.mainloop()
        app.quit()

    def quit(self):
        # controller.ControllerProcess.quit(self)
        util.GUIProcess.quit(self)

if __name__ == '__main__':
    App.main()
