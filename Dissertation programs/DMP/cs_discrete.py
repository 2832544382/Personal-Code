import numpy as np

class Canonical_Discrete():
    def __init__(self, alpha_x=1.0, dt=0.01):
        self.x = 1.0
        self.alpha_x = alpha_x
        self.dt = dt
        self.dmp_type = type
        self.run_time = 1.0

        self.timesteps = round(self.run_time/self.dt)
        self.reset_state()

    def run(self, **kwargs): # run to goal state
        if 'tau' in kwargs:
            timesteps = int(self.timesteps / kwargs['tau'])
        else:
            timesteps = self.timesteps

        self.reset_state()
        self.x_track = np.zeros(timesteps)

        for t in range(timesteps):
            self.x_track[t] = self.x
            self.step_discrete(**kwargs)

        return self.x_track
    
    def reset_state(self): # reset state
        self.x = 1.0

    def step_discrete(self, tau=1.0):
        dx = -self.alpha_x*self.x*self.dt
        self.x += tau*dx
        return self.x