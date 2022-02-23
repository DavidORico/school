x = [10; 0];
A = [1 1; 0 1];
B = [0; 1];
res = zeros(2, 41);

for k = 1:41
    x = A*x + B;
    res(:, k) = x;
end
figure(1);
plot(res');
e = eig(A);

x0 = [10; 0];
Q = [1 0; 0 0];
Q_spec = blkdiag(Q, Q, Q);
B_spec = [0 0 0; 0 0 0; 0 0 0; 1 0 0; 1 0 0; 1 1 0];
R = 1/10;
R_spec = blkdiag(R, R, R);
A_spec = [eye(2); A; A^2];

H = 2*(B_spec'*Q_spec*B_spec + R_spec);
f = 2*x0'*A_spec'*Q_spec*B_spec;
A_constraints = [1 0 0; -1 0 0; 0 1 0; 0 -1 0; 0 0 1; 0 0 -1];
b_constraints = ones(6, 1);
min_of_J = quadprog(H,f,A_constraints,b_constraints);

%MPC controller
x = [10; 0];
u = min_of_J(1,1);
u_res = zeros(1, 41);
for k = 1:41
    f = 2*x'*A_spec'*Q_spec*B_spec;
    min_of_J = quadprog(H,f,A_constraints,b_constraints);
    u = min_of_J(1,1);
    x = A*x + B*u;
    res(:, k) = x;
    u_res(:, k) = u;
end

figure(2);
plot(res');

figure(3);
plot(u_res');