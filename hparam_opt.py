import numpy as np
import gym
import json
import sys
import random
import numpy as np
import optuna
import fnai.fn_sac as fn_sac
import fnai.fn_gym as fn_gym

TXT_LOG_PATH = 'log.txt'

def fn_opt(trial: optuna.Trial) -> int:
    try:
        net_arch = trial.suggest_categorical('net_arch', ['CnnPolicy', 'LnCnnPolicy'])
        gamma = trial.suggest_categorical('gamma', [0.9, 0.95, 0.98, 0.99, 0.995, 0.999, 0.9999])
        learning_rate = trial.suggest_loguniform('lr', 1e-5, 1)
        batch_size = trial.suggest_categorical('batch_size', [16, 32, 64, 128, 256, 512])
        buffer_size = trial.suggest_categorical('buffer_size', [int(1e4), int(1e5), int(1e6)])
        learning_starts = trial.suggest_categorical('learning_starts', [0, 25, 50, 75, 100])
        gradient_steps = trial.suggest_categorical('gradient_steps', [5, 15, 20, 50, 100, 300])
        ent_coef = trial.suggest_categorical('ent_coef', ['auto', 0.5, 0.1, 0.05, 0.01, 0.0001])

        target_entropy = 'auto'
        if ent_coef == 'auto':
            target_entropy = trial.suggest_categorical('target_entropy', ['auto', -1, -10, -20, -50, -100])


        env = fn_gym.FNGym(0.2)
        model = fn_sac.FNSAC(net_arch, env,
                            gamma=gamma,
                            learning_rate=learning_rate,
                            batch_size=batch_size,
                            buffer_size=buffer_size,
                            learning_starts=learning_starts,
                            gradient_steps=gradient_steps,
                            ent_coef=ent_coef,
                            target_entropy=target_entropy
        )

        for train_count in range(10):
            model.learn(total_timesteps=200)
            trial.report(env.get_running_reward(), (train_count + 1) * 200)

            if trial.should_prune():
                raise optuna.TrialPruned()
    except KeyboardInterrupt:
        input('Keyboard Interrupt. Press any key to continue')
        raise ValueError("Exit Trial, Keyboard Interrupt")

    return env.get_running_reward()

def save_trials(study: optuna.Study, frozen_trial: optuna.trial.FrozenTrial) -> None:
    global TXT_LOG_PATH
    with open(TXT_LOG_PATH, 'a') as log_f:
        log_f.write(str(frozen_trial))
        log_f.write('\n')

if __name__ == '__main__':
    sampler = optuna.samplers.TPESampler(**optuna.samplers.TPESampler.hyperopt_parameters())
    study = optuna.create_study(sampler=sampler, direction='maximize')
    study.optimize(fn_opt, n_trials=500, callbacks=[save_trials], n_jobs=1)

    print("Best trial:")
    trial = study.best_trial

    print("  Value: ", trial.value)

    print("  Params: ")
    for key, value in trial.params.items():
        print("    {}: {}".format(key, value))
