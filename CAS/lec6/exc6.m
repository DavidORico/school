x1 = -5:0.1:5;
x2 = -5:0.1:5;

[X1,X2] = meshgrid(x1, x2);
J = (X1 - 1).^2 + (X2 - 2).^2;
surf(X1, X2, J);

H = 2*eye(2);
f = [-2; -4];
x = quadprog(H,f);

hold on;
plot3(1, 2, 0, 'o','Color','b', 'MarkerSize', 20);

A = [1 0; -1 0; 0 1; 0 -1];
b = [5; 5; -3; 5];
x = quadprog(H,f,A,b);
plot3(x(1,1), x(2,1), (x(1,1) - 1)^2 + (x(2,1) - 2).^2, 'o','Color','b', 'MarkerSize', 20);