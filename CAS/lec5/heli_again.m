% state feedback controller
A = [-0.4 0 -0.01; 1 0 0; -1.4 9.8 -0.02];
B = [6.3; 0; 9.8];
C = [0 0 1];
D = 0;
eigen_val = eig(A);
K = place(A, B, [-1 -5 -10]);

% LQRI
sys = ss(A, B, C, D);
Q = diag(1./([pi/2, pi/2, 10, 1].^2));
[K_integrate,~,~] = lqi(sys, Q, 1/((pi/2)^2));

% discretized LQR
sample_time = 0.1;
sys_d = c2d(sys, sample_time);
[K_integrate_discretized,~,~] = lqi(sys_d, Q, 1/((pi/2)^2));