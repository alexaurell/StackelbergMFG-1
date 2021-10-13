import mkvequation_reg as mkvequation
import fbsdesolver_reg_terminal as fbsdesolver
import tensorflow as tf
import numpy as np


print('\n\ntf.VERSION = ', tf.__version__, '\n\n')
print('\n\ntf.keras.__version__ = ', tf.keras.__version__, '\n\n')

# SEED FOR RANDOMNESS
n_seed = 1

def main():
    # PARAMETERS
    # Nt =        20 #100
    batch_size = 200

    T =         30.0
    I0, R0 = 0.1, 0.0 #1.e-2, 0.0
    S0 = 1.0 - I0 - R0
    m0 =        [S0,I0,R0] # initial distribution
    beta =      0.25
    gamma =     1./10
    kappa =     0.0
    cost_I =    0.5
    cost_lambda1 = 10.0
    ################### NEW #####################
    clog = 1.0
    beta_reg = [0.2, 1.0]
    lambda_goal = [1.0, 0.7]
    ################### NEW #####################
    valid_size = 800#2048 # 2*batch_size#4096
    n_maxstep = 5000
    # SAVE DATA TO FILE
    datafile_name = 'data/data_fbsdesolver_params.npz'
    np.savez(datafile_name,
                beta=beta, gamma=gamma, kappa=kappa,
                cost_I=cost_I, cost_lambda1=cost_lambda1, clog=clog, beta_reg=beta_reg,
                lambda_goal=lambda_goal, m0=m0,
                batch_size=batch_size, valid_size=valid_size, n_maxstep=n_maxstep)
    # SOLVE FBSDE USING NN
    tf.random.set_seed(n_seed) # ---------- TF2
    tf.keras.backend.set_floatx('float64') # To change all layers to have dtype float64 by default, useful when porting from TF 1.X to TF 2.0  # ---------- TF2
    print("========== BEGIN SOLVER MKV FBSDE ==========")
    mkv_equation = mkvequation.MckeanVlasovEquation(beta, gamma, kappa, cost_I, cost_lambda1, clog, beta_reg, lambda_goal)
    mkv_solver = fbsdesolver.SolverMKV1(mkv_equation, T, m0, batch_size, valid_size, n_maxstep) # ---------- TF2
    mkv_solver.train()
    # SAVE TO FILE
    print("SAVING FILES...")
    datafile_name = 'data/data_fbsdesolver_solution_final.npz'
    np.savez(datafile_name,
                prop_S_path  = mkv_solver.prop_S_path,
                prop_I_path  = mkv_solver.prop_I_path,
                prop_R_path  = mkv_solver.prop_R_path,
                t_path       = mkv_solver.t_path,
                loss_history = mkv_solver.loss_history,
                LAMBDA_path  = mkv_solver.LAMBDA_path,
                Y_path       = mkv_solver.Y_path)
#                 reg_cost_history = mkv_solver.reg_cost_history,
#                 target_cost_history = .target_cost_history)
                # y_real=y_real, x_path=x_path)
    print("========== END SOLVER MKV FBSDE ==========")


if __name__ == '__main__':
    np.random.seed(n_seed)
    main()
