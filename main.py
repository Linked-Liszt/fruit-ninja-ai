import fnai.fn_sac as fn_sac
import fnai.fn_gym as fn_gym
from stable_baselines import SAC 


env = fn_gym.FNGym(0.2)
print(env.observation_space)
print(env.action_space)
model = fn_sac.FNSAC('CnnPolicy', env, tensorboard_log='sac_fn_tensorboard',
    learning_rate=0.003, gradient_steps=100, batch_size=128)

keep_training=True
log_num = 0
train_interval = 2000
while keep_training:
    try:
        model.learn(total_timesteps=train_interval)
        model.save(f'saved_models/model_auto_{log_num}')
    except KeyboardInterrupt:
        print('Saving model...')
        model.save(f'saved_models/model_manuel_{log_num}')
        response = input("Keep Training (N/n to stop):")
        if response.lower() == 'n':
            keep_training = False
    log_num += 1

