import time



# Cool down manager 

class Cooldown:
    def __init__(self, cooldown_time: int) -> None:
        self.keys = {} # {'nameOfuser': 'cooldowntime'}
        self._cooldown_time = cooldown_time
    def _is_in_cooldown_list(self, key) -> bool:
        return key in self.keys.keys()
    def is_in_cooldown(self, key) -> bool:
        if self._is_in_cooldown_list(key) == False:
            return False
       
        return self.keys[key] > time.time()
    def update_or_add(self, key):
        self.keys[key] = self._get_next_time()     
    def _get_next_time(self):   
        return time.time() + self._cooldown_time
