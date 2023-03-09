from asyncio import new_event_loop, set_event_loop, run_coroutine_threadsafe, Queue
from threading import Thread


class ThreadEventLoop:
    """
    Run Event Loop in different thread.
    """

    @property
    def loop(self):
        return self._loop

    def __init__(self):
        self._loop = new_event_loop()
        Thread(target=self._start_background, daemon=True).start()

    def _start_background(self):
        set_event_loop(self.loop)
        self._loop.run_forever()
