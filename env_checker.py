import stable_baselines.common.env_checker as env_checker
import fnai.fn_gym as fn_gym


test_gym = fn_gym.FNGym(0.2, True)
env_checker.check_env(test_gym, warn=True, skip_render_check=True)