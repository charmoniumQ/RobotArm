import multiprocessing
#import Queue
import time
import sys
from config import logs


class Process (multiprocessing.Process):
    '''This class creates a new process.'''
    def __init__(self, log_function, parallel=True):
        '''Creates a new Process class.
        
        log_function will be called with messages.
        if parallel is False,
        then your class will follow the structure of a Process,
        but it will not multithread. You can not call start().
        This is useful for testing classes in a single-threaded environment,
        before porting it to the multithreaded world

        Logs:
        logs.framework['process']['__init__']
            will log when __init__ is done.
        '''
        #TODO: modular
        multiprocessing.Process.__init__(self)
        self.log = log_function
        self.parallel = parallel
        self.actions_q = multiprocessing.Queue()
        self.quitting = multiprocessing.Event()
        self.delay(0)
        self.pause(False)
        if logs.framework['process']['__init__']:
            self.log('Setup succesful')

    def start(self):
        '''This is what actually forks out your process into a new one.

        The new thread will just call 'run' repeatedly.
        Do not call this if parallel is set.
        If called more than once,
        this will see if the process is already alive,
        and if it is, do nothing.

        Log messages:
        logs.framework['process']['double_start']
            will log if the start is called more than once.
        logs.framework['process']['start']
            will when this method is done (when somebody started your process)'''
        if not self.parallel:
            raise RuntimeError('This is thread is not set to run' +
                               'in self.parallel.')
        if self.is_alive():
            if logs.framework['process']['double_start']:
                self.log('Already started')
            return
        else:
            if logs.framework['process']['start']:
                self.log('Begining to loop')
            multiprocessing.Process.start(self)

    def run(self):
        '''Do setup, loop, then end.'''
        self.setup()
        self.loop()
        self.end()

    def setup(self):
        '''Setup, in the new thread,
(as opposed to __init__, which sets up the object, in the parent thread)

        Useful if you need to set up an object in the same environment as your thread.
        Useful for organizing things that aren't needed until the thread starts.

        logs:
        logs.framework['process']['pid']
            will log the pid, for debugging purposes'''
        self.loop_count = 0
        if logs.framework['process']['pid']:
            self.log(str(self.pid))

    def loop(self):
        '''Start the main loop (stops when quit is called)

        This will continually call _loop until quit is called
        (specifically, until self.is_quitting is True)
        
        logs:
        logs.framework['process']['loop_count']
            will log, each time a loop is completed, a counter '''
        while not self.is_quitting():
            self._loop()
            self.loop_count += 1
            if logs.framework['process']['loop_count']:
                self.log('Finished loop %d' % self.loop_count)

    def _loop(self):
        '''This is called a bunch, while the thread is started, but not quitted

        Don't override this method,
        if you want to do internal stuff,
        override _mode instead
        this calls self.process_queue(), to get inputs from outside world
        and self.mode(), to do internal business'''
        #TODO: combine this with loop?
        self.process_queue()
        self.mode()

    def process_queue(self):
        '''This gets strings from the self.actions_q, and calls self._do_action on them.

        This is what internally executes external messages

        logs:
        logs.framework['process']['actions']
            will tell the log what action is currently being executed'''
        while not self.actions_q.empty():
            action = self.actions_q.get()
            if logs.framework['process']['actions']:
                self.log('Doing: %s' % action)
            try:
                exec action in locals()
            except:
                self.error(action, sys.exc_info())

    def error(self, action, exc_info):
        '''This logs errors, if the log for that is on.

        logs:
        logs.framework['process']['error']
            will log when an error has occured
            You should probably always have this log on. (its kind of important)'''
        if logs.framework['process']['error']:
            self.log('Could not execute: ' + action)
            self.log('Error type: %s' % exc_info[0])
            self.log('Error value: %s' % exc_info[1])

    def mode(self):
        '''This calles _mode when appropriate

        logs:
        logs.framework['process']['mode']
            logs when paused or delayed'''
        if not (self.is_paused() or self.is_delayed()):
            self._mode()
        else:
            if logs.framework['process']['mode']:
                self.log('paused or delayed')

    def _mode(self):
        '''Put your internal stuff here.

        This will be called once every loop when not paused or delayed for a time.
        Override this method'''
        pass

    #  TODO: figure out property business
    #@property
    def idle(self):
        '''Tells you if there is nothing in the queue to be done.

        Most of the times, if self.idle(),
        then it is a good idea to self.quit(),
        unless you are waiting for something specific'''
        return self.actions_q.empty()

    #@property
    def is_delayed(self):
        '''Tells if it supposed to be delayed right now'''
        return self.delay_time_millis > time.time()

    #@delay.setter
    def delay(self, period):
        '''Will refrain from calling _mode for the duration of period'''
        self.delay_time_millis = time.time() + period

    #@property
    def pause(self, status=None):
        '''If this is called, I will refrain from calling _mode.

        call pause(True) to pause, pause(False) to unpause, and pause() to toggle

        logs:
        logs.framework['process']['pause']
            logs when paused.
            If you don't know why your process doesn't seem to be running,
            But it does try to process external stuff turn this logger on.'''
        if status == None:
            return self.pause(not self.is_paused())
        if logs.framework['process']['pause']:
            self.log('paused? ' + str(status))
        self.paused = status

    #@pause.setter
    def is_paused(self):
        '''Will tell you if I am paused'''
        return self.paused

    def do_action(self, action):
        '''This is how external processes can pass snippets of code (as strings)
to be exec'uted in local()'s, when the queue reader gets around to it.'''
        if logs.framework['process']['do_action']:
            self.log('Will do: %s' % action)
        if logs.framework['process']['idle'] and self.idle():
            self.log('Not idle')
        if self.parallel:
            self.actions_q.put(action)
        else:
            self._do_action(action)

    #@property
    def is_quitting(self):
        '''Will tell you if I inted to quit, or if I have already quit

        set by _quit'''
        return self.quitting.is_set()

    #@is_quitting.setter
    def quit(self):
        '''This should be called by external processes to ask this process to quit.

        This is a polite method, and it will let this process finish its business,
        (current loop, which includes processing everything on the queue),
        before quitting.
        Calling multiple times is safe.

        logs:
        logs.framework['process']['quit']
            will log when it intends to quit
        logs.framework['process']['double_quit']
            will log if quit has been called more than once'''
        if not self.quitting.is_set():
            if logs.framework['process']['quit']:
                self.log('Quitting...')
            self.quitting.set()
        else:
            if logs.framework['process']['double_quit']:
                self.log('Already quit')
        if not self.parallel:
            # then the loop won't be waiting for a certain signal
            self._quit()

    def _quit(self):
        '''This should be called by internal things if they want to quit.

        This is not polite, and it should only be called when the loop is done.
        Override this if you have delicate resources that must be quitted carefully.
        Call super._quit even if you are override this.'''
        try: self.actions_q.close()
        except: pass  # already destructed
        try: self.objects_q.close()
        except: pass

    def end(self):
        '''Called at the end of the loop. It destructs everything'''
        #TODO: why not just make this _quit?
        self._quit()

    def __del__(self):  # TODO: is del'ing necessary?
        print ("del'ing")
        try:
            self.quit()
        except:  # already partially destructed
            self._quit()
