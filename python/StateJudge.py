import sys,os 

## << state monitor ##
sys.path.append('tools/')
from StateMonitor import StateMonitor
## state monitor >> ##

class StateJudge:
    monitor_switch = True
    state_site = []
    judge_times = 0
    state = 0
    judge_times = 0
    state_site_size = 20
    standup_b = 5
    falldown_b = -5
    
    ## << param using in fitting ##
    n_average_x = 210  # n * average_x
    x_data = 665       # (Xi)*(Xi) - n*average_x*average_x
    ## param using in fitting >> ##

    ## << state monitor ##
    state_monitor = None
    if monitor_switch == True:
            state_monitor = StateMonitor(1100)
    ## state monitor >> ##

    # @classmethod
    def __init__(self):
        if self.monitor_switch == True:
            self.state_monitor = StateMonitor(1100)

    @classmethod
    def setFPS(self, fps):
        self.state_site_size = int(2*fps)
        sum_x = 0
        sum_xx = 0
        for i in range(self.state_site_size):
            sum_x += i+1
            sum_xx += (i+1) * (i+1)
        
        average_x = sum_x/self.state_site_size
        square_average_x = average_x * average_x
        self.n_average_x = self.state_site_size *  average_x
        n_square_average_x = self.state_site_size * square_average_x
        self.x_data = sum_xx - n_square_average_x

    @classmethod
    def fitting(self):
        sum_y = 0
        sum_xy = 0
        for i in range(self.state_site_size):
            sum_y += self.state_site[i]
            sum_xy += self.state_site[i]*(i+1)

        average_y = sum_y/self.state_site_size

        b = (sum_xy - self.n_average_x * average_y)/self.x_data
        return b

    @classmethod
    def judge(self, top_x, top_y, down_x, down_y, img_h):
        site = top_y
        ## << state monitor ##
        if self.monitor_switch == True:
            self.state_monitor.monitor(top_x, top_y, down_x, down_y)
        ## state monitor >> ##
        judge_result = 0
        if self.judge_times < self.state_site_size:
            self.state_site.append(site)
            self.judge_times = self.judge_times + 1
            return 0
        elif self.judge_times >= self.state_site_size:
            self.state_site.pop(0)
            self.state_site.append(site)
        b = self.fitting()
        # print ("B: ",b)
        # print ("state_site_size: ", self.state_site_size)

        ## judge state ##
        if b >= self.standup_b:
            judge_result = -1
        elif b <= self.falldown_b:
            judge_result = 1
        
        ## state switch ##
        if judge_result == -1:
            self.state = -1
        elif judge_result == 1:
            self.state = 0
        return self.state