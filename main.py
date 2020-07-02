import fnai.fn_sac as fn_sac
import fnai.fn_gym as fn_gym


env = fn_gym.FNGym(0.2, True)
print(env.observation_space)
print(env.action_space)
model = fn_sac.FNSAC('CnnPolicy', env, tensorboard_log='sac_fn_tensorboard')

for i in range(1000)
    model.learn(total_timesteps=100000)
    model.save(f'model_{i * 100000}')

