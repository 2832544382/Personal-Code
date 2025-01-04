        deg2rad = pi/180;

%task 3 positions

px = 1;
py = 1;
pz = 1;
phi = 0;
miu = 0;
p0e = [ px py pz ]' ;

D1 = 0.5;
L1 = 2;
L2 = 3;
L3 = 0.2;

if norm(p0e) > L1 + L2 + L3 + D1
    error('desired position is out of the workspace')
end

syms th1 th2 th3 th4 th5 l3x l3y l3z rw zw

%q1
th1 = atan2(py,px);

l3x = cos(phi) * L3;
l3z = sin(phi) * L3;
l3y = tan(th1) * l3x;

rw = sqrt(px^2+py^2) - sqrt(l3x^2 + l3y^2);
zw = pz - l3z;

%q3
D = -(rw^2 + (zw - D1)^2 - L1^2 - L2^2)/(2*L1*L2);
th3 = atan2(-sqrt(1-D^2), -D);
% second q3
th32 = atan2(sqrt(1-D^2), -D);


%q2
t = atan2(zw - D1,rw);
al = atan2(L2*sin(th3) , L1 + L2*cos(th3));
al2 = atan2(L2*sin(th32) , L1 + L2*cos(th32));

th2 = t - al;
th22 = t - al2;

%q4
th4 = phi - th3 - th2;
th42 = phi - th32 - th22;

%end effector position
th5 = miu;

t12 = dh(0,90*deg2rad,D1,th1);
t23 = dh(L1,0,0,th2);
t34 = dh(L2,0,0,th3);
t45 = dh(0,90*deg2rad,0,th4 + 90*deg2rad);
t5e = dh(0,0,L3,th5);

%second answer
t122 = dh(0,90*deg2rad,D1,th1);
t232 = dh(L1,0,0,th22);
t342 = dh(L2,0,0,th32);
t452 = dh(0,90*deg2rad,0,th42 + 90*deg2rad);
t5e2 = dh(0,0,L3,th5);


t1e = t12*t23*t34*t45*t5e;

t1e2 = t12*t23*t34*t45*t5e;

xe = round(t1e(1,4),3);
ye = round(t1e(2,4),3);
ze = round(t1e(3,4),3);

xe2 = round(t1e2(1,4),3);
ye2 = round(t1e2(2,4),3);
ze2 = round(t1e2(3,4),3);

%analytical solutions
%xe = L1*cos(th1)*cos(th2) + L2*cos(th1)*cos(th2+th3) + L3*cos(th1)*sin(th2+th3+th4);
%ye = L1*sin(th1)*cos(th2) + L2*sin(th1)*cos(th2+th3) + L3*sin(th1)*sin(th2+th3+th4);
%ze = D1 + L1*sin(th2) + L2*sin(th2+th3) - L3*cos(th2+th3+th4);

%DH function
function blank = dh(a, alpha, d, theta)
    blank = sym('zeros',[4,4]);
    row1 = [cos(theta) -cos(alpha)*sin(theta) sin(alpha)*sin(theta) a*cos(theta)];
    row2 = [sin(theta) cos(alpha)*cos(theta) -sin(alpha)*cos(theta) a*sin(theta)];
    row3 = [0 sin(alpha) cos(alpha) d];
    row4 = [0 0 0 1];

    blank(1,:) = row1;
    blank(2,:) = row2;
    blank(3,:) = row3;
    blank(4,:) = row4;
end

