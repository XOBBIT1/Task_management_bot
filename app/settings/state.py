class UserState:
    def __init__(self):
        self.states = {}

    def set_state(self, user_id, state):
        self.states[user_id] = state

    def get_state(self, user_id):
        return self.states.get(user_id)

    def clear_state(self, user_id):
        if user_id in self.states:
            del self.states[user_id]
