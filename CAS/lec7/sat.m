%observer
A = [0 1; 0 0];
B = [0; 1];
C = [1 0];

p = [-1 -5.0];
L = place(A',C',p).';

%observer with u0
A_new = [0 1 0; 0 0 1; 0 0 0];
B_new = [0 1 0];
C_new = [1 0 0];

p_new = [-1 -5 -10];
L_new = place(A_new', C_new', p_new);