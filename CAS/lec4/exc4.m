% state feedback controller
A = [-0.4 0 -0.01; 1 0 0; -1.4 9.8 -0.02];
B = [6.3; 0; 9.8];
C = eye(3);
D = [0; 0; 0];
eigen_val = eig(A);
K = place(A, B, [-1 -5 -10]);

% LQR
sys = ss(A, B, C, D);
Q = diag(1./([pi/2, pi/2, 10].^2));
[K_lqr, S, e] = lqr(sys, Q, 1/((pi/2)^2));

% discretized LQR
sys_d = c2d(sys, 10*0.01);
[K_lqr_d, S, e] = lqr(sys_d, Q, 1/((pi/2)^2));