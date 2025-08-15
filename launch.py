from datetime import datetime, timedelta
import os
from time import sleep
import subprocess




class Pomidor:
    weekend_breaks = [
        # Утро: 25/5
        ("08:25", "08:30"), ("08:55", "09:00"),
        ("09:25", "09:30"), ("09:55", "10:00"),
        ("10:25", "10:30"), ("10:55", "11:00"),
        ("11:25", "11:30"), ("11:55", "12:00"),

        # День: 50/10 + обед
        ("12:50", "14:00"),  # перерыв + обед

        ("14:50", "15:00"),
        ("15:50", "16:00"),
        ("16:55", "17:00"),  # короткий разгоняющий перерыв
        ("18:00", "18:30"),  # переход на лёгкие задачи

        # Вечер
        ("19:00", "20:00"),  # ужин + старт офлайн-зоны
    ]

    def to_dt(self, s):
        return datetime.strptime(s, "%H:%M")

    def __init__(self):
        self.weekend_breaks = [list(map(self.to_dt,  break_times)) for break_times in self.weekend_breaks]
        self.break_schelder = self.make_break_schelder()
        self.is_work = True
        self.dt = 1
        # self.off_screen = 'swaymsg "output DP-1 dpms off"'
        # self.on_screen = 'swaymsg "output DP-1 dpms on"'
        self.set_display_name()
        self.off_screen = f'xrandr --output {self.monitor_name} --off'
        self.on_screen = f'xrandr --output {self.monitor_name} --auto'

    def set_display_name(self):
        # Выполняем команду xrandr и получаем вывод
        output = subprocess.check_output('xrandr --listmonitors', shell=True, text=True)
        lines = output.strip().split('\n')
        
        # Ищем строку, содержащую информацию о мониторе
        for line in lines:
            if len(lines) > 1 and line.startswith(' 0:'):
                # Извлекаем название дисплея из строки
                self.monitor_name =  line.split()[-1]
                return
        
        raise Exception(f'Cant find monitor name:\n {output}')
    def system_work(self):
        if not self.is_work:
            print("time to work")
            self.is_work = True
            os.system(self.on_screen)

    def system_break(self):
        if self.is_work:
            print("time to break")
            self.is_work = False
            os.system(self.off_screen)
        
    def to_zero_day(self, date):
        date = date.replace(day=1, month=1,year=2000)
        return date

    def make_break_schelder(self):
        today = datetime.now()
        today = self.to_zero_day(today)
        today = today.replace(hour=0, minute=0, second=0, microsecond=0)
        hour = timedelta(hours=1)
        five = timedelta(minutes=5)
        half = timedelta(minutes=30)
        twenty_five = half - five
        schelder = []
        
        twenty_five_count = 24
        fourty_five_count = 6
        hour_count = int(24 - twenty_five_count*.5 - 6)
        # 25
        for _ in range(twenty_five_count):
            today += twenty_five
            start_break = today
            today += five
            end_break = today
            schelder.append((start_break, end_break))
        
        fours = timedelta(minutes=15)
        four_five = hour - fours
        # 45
        for _ in range(fourty_five_count):
            today += four_five
            start_break = today
            today += fours
            end_break = today
            schelder.append((start_break, end_break))
        one = timedelta(minutes=1)
        withoutone = hour - one
        for _ in range(hour_count):
            today += withoutone
            start_break = today
            today += one
            end_break = today
            schelder.append((start_break, end_break))
        
        
        eda_start = today.replace(hour=13, minute=0)
        eda_end = today.replace(hour=14, minute=0)
        schelder.append((eda_start, eda_end))

        eda_start = today.replace(hour=19, minute=0)
        eda_end = today.replace(hour=20, minute=0)
        schelder.append((eda_start, eda_end))
        
        forma = '%H:%M:%S'
        for i, delta in enumerate(schelder):
            print(f"{delta[0].strftime(forma)} -> {delta[1].strftime(forma)}")
            if i + 1 in (twenty_five_count, twenty_five_count+fourty_five_count, len(schelder) - 2):
                print()
        
        return schelder

    def is_break_time(self, delta):
        now = datetime.now()
        now = self.to_zero_day(now)
        delta = tuple(map(self.to_zero_day, delta))
        is_break = delta[0] <= now < delta[1] 
        return is_break

    def is_weekend(self):
        now = datetime.now()
        day_of_week = now.weekday()
        res = day_of_week >= 5
        return res

    def run(self):
        schedule = self.weekend_breaks if self.is_weekend() else self.break_schelder
        while True:
            for delta in schedule:
                if self.is_break_time(delta):
                    self.system_break()
                    break
                sleep(self.dt)
            else:
                self.system_work()
            sleep(self.dt)

def test_swaymsg():
    P = Pomidor()
    off_screen = P.off_screen
    on_screen = P.on_screen
    print(f"{off_screen = }")
    sleep(3)
    os.system(off_screen)
    sleep(5)
    os.system(on_screen)

def text_schelder():
    Ogurec = Pomidor()
    Ogurec.make_break_schelder()

def work():
    test_swaymsg()
    with open('/home/user/Files/Pomos/log', 'w') as f:
        f.write(f"POMODORO START at {datetime.now()}")
    print("POMODORO START")
    Ogurec = Pomidor()
    Ogurec.run()

def main():
    # text_schelder()
    work()

if __name__ == "__main__":
    main()
