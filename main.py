import argparse
import fnai.fn_sac as fn_sac
import fnai.fn_gym as fn_gym
from stable_baselines import SAC
from os import path

parser = argparse.ArgumentParser(description='Train the model')
parser.add_argument(nargs='?', default='none', dest='model_path',
    help='(optional) parameters to start training from')

args = parser.parse_args()




env = fn_gym.FNGym(0.2)
print(env.observation_space)
print(env.action_space)
model = fn_sac.FNSAC('CnnPolicy', env, tensorboard_log='sac_fn_tensorboard',
    learning_rate=0.0003, gradient_steps=50, batch_size=128)

if path.exists(args.model_path):
    print(f'Loading Model: {args.model_path}')
    model.load(args.model_path)
else:
    print('Using new model')

keep_training=True
log_num = 0
train_interval = 50000
manual_log_num = 0
while keep_training:
    try:
        model.learn(total_timesteps=train_interval)
        model.save(f'saved_models/model_auto_sac_{log_num}')
        log_num += 1
    except (KeyboardInterrupt, ValueError):
        print('Saving model...')
        model.save(f'saved_models/model_manuel_sac_{manual_log_num}')
        manual_log_num += 1
        response = input("Keep Training (N/n to stop):")
        if response.lower() == 'n':
            keep_training = False
