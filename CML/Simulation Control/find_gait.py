def act(obs, t, a, b, c):
    current_p = obs[:12]
    desired_p = np.zeros(12)
    v = a * np.sin(t * b) + c
    pos = [1, 10, 2, 11]
    neg = [4, 7, 5, 8]
    zero = [0, 3, 6, 9]
    desired_p[pos] = v
    desired_p[neg] = -v
    desired_p[zero] = 0

    delta_p = desired_p - current_p
    delta_p = np.clip(delta_p, -1, 1)
    return delta_p

def test_params(params, env, steps=100):
    ep_r = 0
    obs = env.reset()
    for t in range(steps):
        action = act(obs, t, *params)
        obs, r, done, info = env.step(action)
        ep_r += r
    return ep_r / len(envs)

def find_params(env, episodes):
    params = np.random.uniform(-1, 1, (episodes, 4))
    params[:,0] = 0
    for i in range(len(params)):
        params[i,0] = test_params(params[i,1:], env)
    p = np.argsort(params[:,0])[::-1]
    return params[p[0],1:]
