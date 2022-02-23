u = pi/2;
y = 3*sin(u);

u = linspace(0, 2*pi, 50);
y = zeros(1, 50);
for i = 1:50
    y(i) = 3*sin(u(i));
end
plot(u, y)

v = [1 2]';
th = (2*pi)/3;
R = [cos(th) -sin(th); sin(th) cos(th)];
w = R*v;

