s = tf('s');
num = 160*(s+2.5)*(s+0.7);
denum = ((s^2)+5*s+40)*((s^2)+0.03*s+0.06);
sys = tf(num, denum);
bool = isstable(sys);
p = num/denum;
zero_gain = 280/2.4;
bode(num/denum);