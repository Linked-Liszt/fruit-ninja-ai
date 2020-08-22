import argparse
import fnai.fn_sac as fn_sac
import fnai.fn_gym as fn_gym
from stable_baselines import SAC 
from stable_baselines.common.policies import CnnLnLstmPolicy
from stable_baselines import PPO2
from os import path

parser = argparse.ArgumentParser(description='Train the model')
parser.add_argument(nargs='?', default='none', dest='model_path',
    help='(optional) parameters to start training from')

args = parser.parse_args()




env = fn_gym.FNGym(0.2)
print(env.observation_space)
print(env.action_space)
model = PPO2(CnnLnLstmPolicy, env, tensorboard_log='sac_fn_tensorboard', nminibatches=1)

if path.exists(args.model_path):
    print(f'Loading Model: {args.model_path}')
    model.load(args.model_path)
else:
    print('Using new model')

keep_training=True
log_num = 0
manual_log_num = 0
train_interval = 100000
while keep_training:
    try:
        model.learn(total_timesteps=train_interval)
        model.save(f'saved_models/model_auto_sac_{log_num}')
        log_num += 1
    except KeyboardInterrupt:
        print('Saving model...')
        model.save(f'saved_models/model_manuel_ppo_{manual_log_num}')
        manual_log_num += 1
        response = input("Keep Training (N/n to stop):")
        if response.lower() == 'n':
            keep_training = False

