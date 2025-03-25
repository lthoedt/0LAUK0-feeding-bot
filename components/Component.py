import threading
import queue

class Component:
    queue = None
    def __init__(self):
        self.queue = queue.Queue()
        def worker(component : Component):
            latestQueueItem = None
            while True:
                if not self.queue.empty():
                    latestQueueItem = self.queue.get()
                    pass

                if component.run(latestQueueItem):
                    latestQueueItem = None
                
        self.thread = threading.Thread(target=worker, daemon=True, args=(self,))
        self.thread.start()

    def use(self, queueItem : any) -> None:
        self.queue.put(queueItem)

    def run(self, queueItem : any) -> bool:
        raise NotImplementedError("run must be implemented")