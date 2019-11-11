import time

class Timer:
    def __init__(self):
        self.t_start = float(0)
        self.t_end = float(0)
        self.t_lap_start = float(0)

    def start(self):
        self.t_start = float(time.perf_counter())

    def restart(self):
        self.t_start = float(time.perf_counter())
        self.t_lap_start = float(time.perf_counter())

    def reset(self):
        self.t_start = float(time.perf_counter())
        self.t_lap_start = float(time.perf_counter())

    def stop(self):
        self.t_end = float(time.perf_counter())
    
    def peek_time(self, args=None):
        if args is not None:
            return float(time.perf_counter() - self.t_start) * args
        else:
            return float(time.perf_counter() - self.t_start)

    def lap_time(self, args=None):
        rtn_f = float(0)
        if args is not None:
            rtn_f = float(time.perf_counter() - self.t_lap_start) * args
        else:
            rtn_f = float(time.perf_counter() - self.t_lap_start)
        self.t_lap_start = float(time.perf_counter())
        return rtn_f

    def get_time(self, args=None):
        if args is not None:
            return float(self.t_end - self.t_start) * args
        else:
            return float(self.t_end - self.t_start)
