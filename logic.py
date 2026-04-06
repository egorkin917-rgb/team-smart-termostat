import time

class Logic:
    def __init__(self):
        # ПУНКТ 6: Настройки расписания
        self.day_temp = 22.0      # Днём 22°C
        self.night_temp = 18.0    # Ночью 18°C
        
        # ПУНКТ 7: Гистерезис
        self.hysteresis = 1.0     # ±1°C
        
        # ПУНКТ 8: Защита от частых включений
        self.min_off_time = 180   # 3 минуты
        
        # Состояние
        self.target = 22.0
        self.relay_on = False
        self.last_off_time = 0
        
        # ПУНКТ 9: Режимы
        self.mode = "AUTO"        # AUTO, MANUAL, OFF
        self.manual_time = 0
    
    # ПУНКТЫ 6, 7, 9: Основное решение
    def update(self, temp, hour):
        # ПУНКТ 6: Расписание день/ночь
        if 7 <= hour < 23:
            self.target = self.day_temp
        else:
            self.target = self.night_temp
        
        # ПУНКТ 9: Режим OFF
        if self.mode == "OFF":
            return False
        
        # ПУНКТ 9: Ручной режим
        if self.mode == "MANUAL":
            if time.time() > self.manual_time:
                self.mode = "AUTO"
            else:
                return True
        
        # ПУНКТ 7: Гистерезис
        if not self.relay_on:
            if temp < self.target - self.hysteresis:
                return True
        else:
            if temp > self.target + self.hysteresis:
                return False
            return True
        
        return False
    
    # ПУНКТ 8: Защита от частых включений
    def check_safety(self, want_on):
        now = time.time()
        if want_on and not self.relay_on:
            if now - self.last_off_time > self.min_off_time:
                return True
            return False
        return True
    
    def apply(self, new_state):
        if new_state != self.relay_on:
            self.relay_on = new_state
            if not new_state:
                self.last_off_time = time.time()
    
    # ПУНКТ 9: Управление режимами
    def manual_mode(self):
        self.mode = "MANUAL"
        self.manual_time = time.time() + 1800
    
    def off_mode(self):
        self.mode = "OFF"
    
    def auto_mode(self):
        self.mode = "AUTO"
    
    def get_mode_char(self):
        if self.mode == "AUTO":
            return "A"
        elif self.mode == "MANUAL":
            return "M"
        else:
            return "O"
