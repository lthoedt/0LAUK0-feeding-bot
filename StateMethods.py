from .MainSystem import MainSystem 

# Each state has an entry, do, and exit method
# To define behavior for each state, you can override the methods
class StateMethod:
    def entry(mainSystem : MainSystem):
        pass
    def do(mainSystem : MainSystem):
        pass
    def exit(mainSystem : MainSystem):
        pass

class ScannigState(StateMethod):
    def entry(mainSystem : MainSystem):
        pass
    def do(mainSystem : MainSystem):
        pass
    def exit(mainSystem : MainSystem):
        pass

class AcceptingBirdState(StateMethod):
    def entry(mainSystem : MainSystem):
        mainSystem.door.open()
        pass
    def do(mainSystem : MainSystem):
        pass
    def exit(mainSystem : MainSystem):
        pass

class DenyingBirdState(StateMethod):
    def entry(mainSystem : MainSystem):
        mainSystem.door.close()
        pass
    def do(mainSystem : MainSystem):
        pass
    def exit(mainSystem : MainSystem):
        pass