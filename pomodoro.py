from datetime import datetime, timedelta
import os
from time import sleep
import subprocess




class Pomidor:
    breaks_dict = {
        'weekday': [
            ("20:05", "20:10"), ("20:25", "20:30"), ("20:45", "20:50"),("20:15", "20:20"), ("20:35", "20:40"), ("20:55", "21:00"),
            ("21:05", "21:10"), ("21:25", "20:30"), ("21:45", "20:50"),("21:15", "20:20"), ("21:35", "20:40"), ("21:55", "22:00"),
            ("22:05", "22:10"), ("22:25", "20:30"), ("22:45", "20:50"),("22:15", "20:20"), ("22:35", "20:40"), ("22:55", "23:00"),
            ("23:05", "23:10"), ("23:25", "20:30"), ("23:45", "20:50"),("23:15", "20:20"), ("23:35", "20:40"), ("23:55", "00:00"),
            
            ("00:05", "00:10"), ("00:25", "00:30"), ("00:45", "00:50"),("00:15", "00:20"), ("00:35", "00:40"), ("00:55", "01:00"),
            ("01:05", "00:10"), ("01:25", "00:30"), ("01:45", "00:50"),("01:15", "00:20"), ("01:35", "00:40"), ("01:55", "02:00"),
            ("02:05", "00:10"), ("02:25", "00:30"), ("02:45", "00:50"),("02:15", "00:20"), ("02:35", "00:40"), ("02:55", "03:00"),
            ("03:05", "00:10"), ("03:25", "00:30"), ("03:45", "00:50"),("03:15", "00:20"), ("03:35", "00:40"), ("03:55", "04:00"),
            ("04:05", "00:10"), ("04:25", "00:30"), ("04:45", "00:50"),("04:15", "00:20"), ("04:35", "00:40"), ("04:55", "05:00"),
            ("05:05", "00:10"), ("05:25", "00:30"), ("05:45", "00:50"),("05:15", "00:20"), ("05:35", "00:40"), ("05:55", "06:00"),

            ("08:25", "08:30"), ("08:55", "09:00"),
            ("09:25", "09:30"), ("09:55", "10:00"),
            ("10:25", "10:30"), ("10:55", "11:00"),
            ("11:25", "11:30"), ("11:55", "12:00"),

            ("12:30", "14:00"),
            ("14:50", "15:00"),
            ("15:50", "16:00"),
            ("16:30", "17:00"), # спорт
            ("17:50", "18:00"),
            ("18:30", "19:00"),
        ],
    }
    # poweeroff_timer = [
    #     ('21:00', '22:00')
    # ]
    def to_dt(self, s):
        return self.to_zero_day(datetime.strptime(s, "%H:%M"))

    def __init__(self):
        # self.weekend_breaks = [list(map(self.to_dt,  break_times)) for break_times in self.weekend_breaks]
        self.is_work = True
        self.dt = .1
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

    def is_break_time(self, delta):
        now = datetime.now()
        now = self.to_zero_day(now)
        # print(f"{delta = }")
        delta = tuple(map(self.to_dt, delta))
        is_break = delta[0] <= now < delta[1] 
        return is_break

    def what_day_type(self):
        now = datetime.now()
        day_of_week = now.weekday()
        res = day_of_week >= 5

        res = False
        day_type = 'weekend' if res else 'weekday'
        print(f"{day_type = }")
        return day_type

    def is_power_off_time(self):
        for delta in self.poweeroff_timer:
            if self.is_break_time(delta):
                return True
        else:
            return False

    def run(self):
        schedule = self.breaks_dict[self.what_day_type()]
        while True:
            for delta in schedule:
                print(delta)
                if self.is_break_time(delta):
                    self.system_break()
                    break
                sleep(self.dt)
            else:
                self.system_work()
            sleep(30)
            # if self.is_power_off_time():
            #     os.system('poweroff')

def test_swaymsg():
    P = Pomidor()
    off_screen = P.off_screen
    on_screen = P.on_screen
    print(f"{off_screen = }")
    sleep(1)
    os.system(off_screen)
    sleep(2)
    os.system(on_screen)
    return off_screen

def text_schelder():
    Ogurec = Pomidor()
    Ogurec.make_break_schelder()

def work():
    command = test_swaymsg()
    with open('/home/user/Files/utils/log', 'w') as f:
        f.write(f"POMODORO START at {datetime.now()} \n {command = }")
    print("POMODORO START")
    Ogurec = Pomidor()
    Ogurec.run()

def main():
    # return
    # text_schelder()
    work()
    # return

if __name__ == "__main__":
    main()
