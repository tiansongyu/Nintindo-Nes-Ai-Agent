try:
    import gym  # type: ignore
except ModuleNotFoundError:
    class _Box:
        def __init__(self, low, high, shape, dtype):
            self.low = low
            self.high = high
            self.shape = shape
            self.dtype = dtype

    class _Wrapper:
        def __init__(self, env):
            self.env = env
            self.action_space = getattr(env, "action_space", None)
            self.observation_space = getattr(env, "observation_space", None)

        def reset(self, *args, **kwargs):
            return self.env.reset(*args, **kwargs)

        def step(self, action):
            return self.env.step(action)

        def render(self, *args, **kwargs):
            render = getattr(self.env, "render", None)
            if render is not None:
                return render(*args, **kwargs)
            return None

    class _Spaces:
        Box = _Box

    class _GymCompat:
        Wrapper = _Wrapper
        spaces = _Spaces()

    gym = _GymCompat()

