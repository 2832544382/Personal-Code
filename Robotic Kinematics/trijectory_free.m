clear
close all

deg2rad = pi/180;

pose0 = inverse([5.2,0,0.5,0,0]);
pose1 = inverse([0,0,-1,-90*deg2rad,0]);
pose2 = inverse([1,1,1,0,0]);
pose3 = inverse([1,1,2,0,0]);
pose4 = inverse([2,1,2,0,0]);
pose5 = inverse([2,1,1,0,0]);

thetas = [pose0;pose1;pose2;pose3;pose4;pose5];

time_initial = 0;
time_final = 2;

%time_initial12 = 3;
%time_final12 = 6;

%time_initial23 = 6;
%time_final23 = 9;

%time_initial34 = 9;
%time_final34 = 12;

%time_initial45 = 12;
%time_final45 = 15;

% Assume initial and final are null
velocity_initial = 0;
velociti_final = 0;

plots_arm(thetas);

pose01 = plot_tri(time_initial, time_final, pose0, pose1);
pose12 = plot_tri(time_initial, time_final, pose1, pose2);
pose23 = plot_tri(time_initial, time_final, pose2, pose3);
pose34 = plot_tri(time_initial, time_final, pose3, pose4);
pose45 = plot_tri(time_initial, time_final, pose4, pose5);

figure(5);
set(5,'position',[1243 190 560 420])
xlabel('x (m)') ; ylabel('y (m)') ;zlabel('z (m)');
plot3(pose01(1,:),pose01(2,:),pose01(3,:),'-','Linewidth',1);
hold on
plot3(pose12(1,:),pose12(2,:),pose12(3,:),'-','Linewidth',1);
hold on
plot3(pose23(1,:),pose23(2,:),pose23(3,:),'-','Linewidth',1);
hold on
plot3(pose34(1,:),pose34(2,:),pose34(3,:),'-','Linewidth',1);
hold on
plot3(pose45(1,:),pose45(2,:),pose45(3,:),'-','Linewidth',1);
hold on

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

%plot arms
% there are 2 answers but here we only need one
function par = inverse(all_par)

    px = all_par(1);
    py = all_par(2);
    pz = all_par(3);
    phi = all_par(4);
    miu = all_par(5);

    p0e = all_par(1:3)' ;

    D1 = 0.5;
    L1 = 2;
    L2 = 3;
    L3 = 0.2;

    if norm(p0e) > L1 + L2 + L3 + D1
        error('desired position is out of the workspace')
    end

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
    %th32 = atan2(sqrt(1-D^2), -D); second awnser
    
    
    %q2
    t = atan2(zw - D1,rw);
    al = atan2(L2*sin(th3) , L1 + L2*cos(th3));
    
    %al2 = atan2(L2*sin(th32) , L1 + L2*cos(th32)); second awnser
    
    th2 = t - al;

    %th22 = t - al2; second awnser
    
    %q4
    th4 = phi - th3 - th2;
    %th42 = phi - th32 - th22; second awnser
    
    %end effector position
    th5 = miu;
    
    par = [th1 th2 th3 th4 th5];
end

function a = plots_arm(thetas)
    deg2rad = pi/180;
    depth12 = 0.5;
    link23 = 2;
    link34 = 3;
    link5e = 0.2;

    a = thetas;
    colors = [0,0,0; 
        0.7,0.7,0; 
        0.7,0,0.7; 
        0,0.7,0.7; 
        0.7,0,0;
        0,0,0.7];
    for draw = 1:6
        t12 = dh(0,90*deg2rad,depth12,a(draw,1));
        t23 = dh(link23,0,0,a(draw,2));
        t34 = dh(link34,0,0,a(draw,3));
        t45 = dh(0,90*deg2rad,0,a(draw,4)+90*deg2rad);
        t5e = dh(0,0,link5e,a(draw,5));

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
        ye = round(t1e(2,4),3);
        
        z1 = t12(3,4);
        z2 = t13(3,4);
        z3 = t14(3,4);
        z4 = t15(3,4);
        ze = t1e(3,4);

        figure(4)
        set(4,'position',[1243 190 560 420])

        plot3(xe,ye,ze,'rx');
        hold on
        plot3([0;x1],[0;y1],[0;z1],'ko-','Linewidth',2,'Color',colors(draw, :));
        hold on
        plot3([x1;x2],[y1;y2],[z1;z2],'ko-','Linewidth',2,'Color',colors(draw, :));
        hold on
        plot3([x2;x3],[y2;y3],[z2;z3],'ko-','Linewidth',2,'Color',colors(draw, :));
        hold on
        plot3([x3;x4],[y3;y4],[z3;z4],'ko-','Linewidth',2,'Color',colors(draw, :));
        hold on
        plot3([x4;xe],[y4;ye],[z4;ze],'ko-','Linewidth',2,'Color',colors(draw, :));
        hold on
        textscatter3(double(xe+0.3),double(ye),double(ze+0.1),string(draw-1));
        hold on
        xlabel('x (dm)') ; ylabel('y (dm)') ;zlabel('z (dm)');
        %xlim([-5.3 5.3]);
        %ylim([-5.3 5.3]);
        %zlim([-2 2.5]);
    end
end

%polynomial trijectory
function par = fowardee(q1, q2, q3, q4, q5)

    deg2rad = pi/180;
    
    %link length
    depth12 = 0.5;
    link23 = 2;
    link34 = 3;
    link5e = 0.2;

    xe = zeros(100, 1);
    ye = zeros(100, 1);
    ze = zeros(100, 1);

    for i = 1:100
      t12 = dh(0,90*deg2rad,depth12,q1(i));
      t23 = dh(link23,0,0,q2(i));
      t34 = dh(link34,0,0,q3(i));
      t45 = dh(0,90*deg2rad,0,q4(i)+90*deg2rad);
      t5e = dh(0,0,link5e,q5(i));  

      t1e = t12*t23*t34*t45*t5e;

      xe(i) = t1e(1,4);
      ye(i) = t1e(2,4);
      ze(i) = t1e(3,4);
    end
    
    par = [xe ye ze];

end

function a = ttt(ti, tf, thetai, thetaf)

% thetai = a0 + a1*ti + a2*ti^2 + a3*ti^3 --- ti = 0
% thetaf = a0 + a1*tf + a2*tf^2 + a3*tf^3; 
% velocityi = a1 + 2*a2*ti + 3*a3*ti^2; --- ti = 0 vi = 0
% velocityf = a1 + 2*a2*tf + 3*a3*tf^2; --- vf = 0

a0 = thetai;
a1 = 0;
a3 = (thetai - thetaf)/4;
a2 = -3*a3;

times = linspace(ti, tf, 100);
parameters = [a3 a2 a1 a0];
a = polyval(parameters, times);

end

function t = plot_tri(ti, tf, anglei, anglef)   

    q1 = ttt(ti, tf, anglei(1), anglef(1));
    q2 = ttt(ti, tf, anglei(2), anglef(2));
    q3 = ttt(ti, tf, anglei(3), anglef(3));
    q4 = ttt(ti, tf, anglei(4), anglef(4));
    q5 = ttt(ti, tf, anglei(5), anglef(5));

    pars = fowardee(q1,q2,q3,q4,q5);
    
    t = zeros(3,100);
    t(1, :) = pars(:, 1);
    t(2, :) = pars(:, 2);
    t(3, :) = pars(:, 3);

        
end

