import time

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
        mainSystem.door.open()
        pass
    def do(mainSystem):
        pass
    def exit(mainSystem):
        pass

class DenyingBirdState(StateMethod):
    # This maybe isnt nice as it is now static
    # But making these classes objects seems a bit wrong as well
    timeSinceLastDeniedBird = 0
    def entry(mainSystem):
        DenyingBirdState.resetTimeSinceLastDeniedBird()
        mainSystem.door.close()
        pass
    def do(mainSystem):
        pass
    def exit(mainSystem):
        pass

    def resetTimeSinceLastDeniedBird():
        DenyingBirdState.timeSinceLastDeniedBird = time.time()

    def secondsSinceLastDeniedBird():
        return time.time() - DenyingBirdState.timeSinceLastDeniedBird