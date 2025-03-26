import threading
import queue

class Component:
    queue = None
    _result = None
    def __init__(self):
        self.queue = queue.Queue()
        def worker(component : Component):
            latestQueueItem = None
            while True:
                if not self.queue.empty():
                    latestQueueItem = self.queue.get()
                    pass
                
                # Run the component with the queue item, potentially null.
                # This call is blocking
                result = self.run(latestQueueItem)
                
                if result:
                    # Result is saved
                    self.setResult(result)
                    # Cached queue item is cleared
                    latestQueueItem = None
                
        self.thread = threading.Thread(target=worker, daemon=True, args=(self,))
        self.thread.start()

    def use(self, queueItem : any) -> None:
        self.queue.put(queueItem)

    def run(self, queueItem : any) -> any:
        raise NotImplementedError("run must be implemented")

    def getResult(self) -> any:
        result = self._result
        self._result = None
        return result

    def setResult(self, result : any) -> None:
        self._result = result