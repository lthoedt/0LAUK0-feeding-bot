# We can't import MainSystem here due to Python's limitations
# around circular imports
# from MainSystem import MainSystem

# Each state has an entry, do, and exit method
# To define behavior for each state, you can override the methods
class StateMethod:
    def entry(mainSystem):
        pass
    def do(mainSystem):
        pass
    def exit(mainSystem):
        pass

class ScanningState(StateMethod):
    def entry(mainSystem):
        pass
    def do(mainSystem):
        pass
    def exit(mainSystem):
        pass

class AcceptingBirdState(StateMethod):
    def entry(mainSystem):
        pass
    def do(mainSystem):
        mainSystem.door.open()
        pass
    def exit(mainSystem):
        pass

class DenyingBirdState(StateMethod):
    def entry(mainSystem):
        pass
    def do(mainSystem):
        mainSystem.door.close()
        pass
    def exit(mainSystem):
        pass