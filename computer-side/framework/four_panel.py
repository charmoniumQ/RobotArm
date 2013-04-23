import Tkinter as tk
from framework import util

class FourPanel(util.GUIProcess):
    def __init__(self, root=None):
        # TODO: standardize master/root/parent lingo
        util.GUIProcess.__init__(self, root)
        self.elem = [[None, None],
                      [None, None]]
        for row in range(len(self.elem)):
            for col in range(len(self.elem[row])):
                self.elem[row][col] = tk.Label(self.root,
                    width=60,
                    height=20,
                    justify=tk.LEFT,
                    text='Label: (%d, %d)' % (row, col),
                    relief=tk.RIDGE,
                    anchor=tk.NW,
                    borderwidth=2,)
                self.elem[row][col].grid(row=row, column=col)

    def append(self, row, col, text):
        self.set(row, col, self.get(row, col) + text + '\n')

    def set(self, row, col, text):
        self.elem[row][col].config(text=text)

    def get(self, row, col):
        return self.elem[row][col].cget('text')

    def run(self):
        self.mainloop()

    def quit(self):
        print ('four panel quitting')
        util.GUIProcess.quit(self)

if __name__ == '__main__':
    f = FourPanel()
    f.append(1, 1, '\nhi')
    f.run()