clear
close all


deg2rad = pi/180;

%Lynxmotion joint angles
theta1 = 0;
theta2 = 0;
theta3 = 0;
theta4 = 0;
theta5 = 0;

%link length
depth12 = 0.5;
link23 = 2;
link34 = 3;
link5e = 0.2;

%get position

t12 = dh(0,90*deg2rad,depth12,theta1);
t23 = dh(link23,0,0,theta2);
t34 = dh(link34,0,0,theta3);
t45 = dh(0,90*deg2rad,0,theta4+90*deg2rad);
t5e = dh(0,0,link5e,theta5);

t13 = t12*t23;
t14 = t13*t34;
t15 = t14*t45;
t1e = t15*t5e;

x1 = t12(1,4);
x2 = t13(1,4);
x3 = t14(1,4);
x4 = t15(1,4);
xe = t1e(1,4);

y1 = t12(2,4);
y2 = t13(2,4);
y3 = t14(2,4);
y4 = t15(2,4);
ye = t1e(2,4);

z1 = t12(3,4);
z2 = t13(3,4);
z3 = t14(3,4);
z4 = t15(3,4);
ze = t1e(3,4);

%figure -- forward kinematic
%end effecter
figure(1);
set(1,'position',[1243 190 560 420])
plot3(x1,y1,z1,'rx');
hold on
plot3(x2,y2,z2,'rx');
hold on
plot3(x3,y3,z3,'rx');
hold on
plot3(x4,y4,z4,'rx');
hold on
plot3(xe,ye,ze,'rx');
hold on
plot3([0;x1],[0;y1],[0;z1],'ko-','Linewidth',2);
hold on
plot3([x1;x2],[y1;y2],[z1;z2],'ko-','Linewidth',2);
hold on
plot3([x2;x3],[y2;y3],[z2;z3],'ko-','Linewidth',2);
hold on
plot3([x3;x4],[y3;y4],[z3;z4],'ko-','Linewidth',2);
hold on
plot3([x4;xe],[y4;ye],[z4;ze],'ko-','Linewidth',2);
hold on
xlabel('x (dm)') ; ylabel('y (dm)') ;zlabel('z (dm)');

%workspace

q1 = 0:10*deg2rad:360*deg2rad-deg2rad;
q2 = 0:20*deg2rad:180*deg2rad-deg2rad;
q3 = -160*deg2rad:20*deg2rad:160*deg2rad-deg2rad;
q4 = -250*deg2rad:20*deg2rad:70*deg2rad-deg2rad;

size = length(q1)*length(q2)*length(q3)*length(q4);
plots = zeros(size, 3);
plot_index = 1;

for t1 = 1:length(q1)
    for t2 = 1:length(q2)
        for t3 = 1:length(q3)
            for t4 = 1:length(q4)

                tt01 = dh(0,0,depth12,0);
                tt12 = dh(0,90*deg2rad,0,q1(t1));
                tt23 = dh(link23,0,0,q2(t2));
                tt34 = dh(link34,0,0,q3(t3));
                tt45 = dh(0,-90*deg2rad,0,q4(t4));
                tt5e = dh(0,0,link5e,0);

                % Calculate the end-effector position
                tt02 = tt01*tt12;
                tt03 = tt02*tt23;
                tt04 = tt03*tt34;
                tt05 = tt04*tt45;
                tt0e = tt05*tt5e;

                % Extract the end-effector position from the final transformation matrix
                x = tt0e(1, 4);
                y = tt0e(2, 4);
                z = tt0e(3, 4);
                
                plots(plot_index, :) = [x, y, z];
                plot_index = plot_index + 1;
            end
        end
    end
end

figure (2)
set(2,'position',[1243 190 560 420])
plot(plots(:,1), plots(:,2), '.');
xlabel('x (m)') ; ylabel('y (m)') ;zlabel('z (m)');
hold on

figure (3)
set(3,'position',[1243 190 560 420])
plot3(plots(:,1), plots(:,2), plots(:,3), '.');
xlabel('x (m)') ; ylabel('y (m)') ;zlabel('z (m)');
hold on

axis equal

%DH function
function blank = dh(a, alpha, d, theta)
    blank = zeros(4,4);
    row1 = [round(cos(theta),8) round(-cos(alpha)*sin(theta), 8) round(sin(alpha)*sin(theta), 8) round(a*cos(theta), 8)];
    row2 = [round(sin(theta),8) round(cos(alpha)*cos(theta),8) round(-sin(alpha)*cos(theta),8) round(a*sin(theta),8)];
    row3 = [0 round(sin(alpha),8) round(cos(alpha),8) d];
    row4 = [0 0 0 1];

    blank(1,:) = row1;
    blank(2,:) = row2;
    blank(3,:) = row3;
    blank(4,:) = row4;
end













