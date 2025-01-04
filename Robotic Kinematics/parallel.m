clear
close all

deg2rad = pi/180;

sa = 170; % arm 1
l = 130; % arm 2
r_platform = 130; % arm 2 to center of ee
r_base = 290; % outer radius

base_len = sqrt(3) * r_base;
half_len = base_len / 2;

    

% coordinate of each base
height = sqrt(base_len^2 - half_len^2);
half_height = height / 2;


% coordinate of platform
a = 0.2; x = 0; y = -50;
xc=x + half_len; yc= y + half_height; phi1 = a + pi/6; phi2 = a + 5*pi/6; phi3 = a + 3*pi/2; %each phi + 2/3pi

% inverse kinematic
% first arm
PP1 = [xc - r_platform*cos(phi1); yc - r_platform*sin(phi1)];
% first base
PB1 = [0; 0];
%th1
c1 = atan2(PP1(2), (PP1(1)));
d1 = acos((sa^2 - l^2 + PP1(1)^2 + PP1(2)^2) / (2 * sa * sqrt(PP1(1)^2 + PP1(2)^2)));
th1 = c1 + d1;
%th12 = c1 -d1; second answer
% M1
M1 = [sa * cos(th1); sa * sin(th1)];

% second arm
PP2 = [xc - r_platform*cos(phi2); yc - r_platform*sin(phi2)];
% second base
PB2 = [base_len; 0];
% th2

%c2 = atan2(PP2(2), PP2(1) - PB2(1));
%d2 = acos((sa^2 - l^2 + (PP2(1) - PB2(1))^2 + PP2(2)^2) / (2 * sa * sqrt((PP2(1) - PB2(1))^2 + PP2(2)^2)));
%th2 = pi -(c2 - d2);

c2 = atan2(PP2(2), PB2(1) -PP2(1));
d2 = acos((sa^2 - l^2 + (PB2(1) -PP2(1))^2 + PP2(2)^2) / (2 * sa * sqrt((PB2(1) -PP2(1))^2 + PP2(2)^2)));
th2 = c2 - d2;
%th22 = c2 + d2; second awnser

% M2
M2 = [ PB2(1) - sa * cos(th2); sa * sin(th2)]; 

% third arm
PP3 = [xc - r_platform*cos(phi3); yc - r_platform*sin(phi3)];
% third base
PB3 = [half_len; height];
c3 = atan2(PB3(2) - PP3(2), PB3(1) - PP3(1));
d3 = acos((sa^2 - l^2 + (PB3(1) - PP3(1))^2 + (PB3(2) - PP3(2))^2) / (2 * sa * sqrt((PB3(1) - PP3(1))^2 + (PB3(2) - PP3(2))^2)));
th3 = c3 + d3;
%th32 = c3 - d3; sencond answer
% M3
M3 = [PB3(1) - sa * cos(th3); PB3(2) - sa * sin(th3)]; 

figure(6)
set(6,'position',[1243 190 560 420])
xlabel('x (mm)') ; ylabel('y (mm)') ;
% plot bases
plot(PB1(1),PB1(2),'o','Linewidth',1,'Color',[0,0,0.7]);
hold on
plot(PB2(1), PB2(2),'o','LineWidth',1,'Color',[0,0,0.7]);
hold on
plot(PB3(1), PB3(2),'o','LineWidth',1,'Color',[0,0,0.7]);
hold on

% link bases
plot([PB1(1),PB2(1)], [PB1(2); PB2(2)],'--','Linewidth',1,'Color',[0,0,0]);
hold on
plot([PB1(1),PB3(1)], [PB1(2); PB3(2)],'--','Linewidth',1,'Color',[0,0,0]);
hold on
plot([PB2(1),PB3(1)], [PB2(2); PB3(2)],'--','Linewidth',1,'Color',[0,0,0]);
hold on

% plot joints
plot(M1(1),M1(2), 'o','Linewidth',1,'Color',[0,0.7,0]);
hold on
plot(PP1(1),PP1(2), 'o','Linewidth',1,'Color',[0.7,0,0]);
hold on

plot(M2(1),M2(2), 'o','Linewidth',1,'Color',[0,0.7,0]);
hold on
plot(PP2(1),PP2(2), 'o','Linewidth',1,'Color',[0.7,0,0]);
hold on

plot(M3(1),M3(2), 'o','Linewidth',1,'Color',[0,0.7,0]);
hold on
plot(PP3(1),PP3(2), 'o','Linewidth',1,'Color',[0.7,0,0]);
hold on

% plot platform
plot([PP1(1),PP2(1)], [PP1(2); PP2(2)],'-','Linewidth',1,'Color',[0.7,0,0.7]);
hold on
plot([PP1(1),PP3(1)], [PP1(2); PP3(2)],'-','Linewidth',1,'Color',[0.7,0,0.7]);
hold on
plot([PP2(1),PP3(1)], [PP2(2); PP3(2)],'-','Linewidth',1,'Color',[0.7,0,0.7]);
hold on

% plot arms
plot([PB1(1);M1(1)],[PB1(2);M1(2)], '-','Linewidth',1,'Color',[0,0.7,0.7]);
hold on
plot([M1(1);PP1(1)],[M1(2);PP1(2)], '-','Linewidth',1,'Color',[0.7,0.7,0]);
hold on

plot([PB2(1);M2(1)],[PB2(2);M2(2)], '-','Linewidth',1,'Color',[0,0.7,0.7]);
hold on
plot([M2(1);PP2(1)],[M2(2);PP2(2)], '-','Linewidth',1,'Color',[0.7,0.7,0]);
hold on

plot([PB3(1);M3(1)],[PB3(2);M3(2)], '-','Linewidth',1,'Color',[0,0.7,0.7]);
hold on
plot([M3(1);PP3(1)],[M3(2);PP3(2)], '-','Linewidth',1,'Color',[0.7,0.7,0]);
hold on

%work space
valid_points = [];

for a = -0.4*(180/pi):5:0.4*(180/pi) % Iterate over angles from 0 to 55 degrees with a step of 5 degree
    phi1 = a + pi/6; phi2 = a + 5*pi/6; phi3 = a + 3*pi/2;

    for i = 1:2:round(PB2(1))
        for j = 1:2:round(PB3(2)) 
        
            PP1 = [i - r_platform*cos(phi1); j - r_platform*sin(phi1)];
            PP2 = [i - r_platform*cos(phi2); j - r_platform*sin(phi2)];
            PP3 = [i - r_platform*cos(phi3); j - r_platform*sin(phi3)];

            dist1 = norm(PP1 - PB1);
            dist2 = norm(PP2 - PB2);
            dist3 = norm(PP3 - PB3);

            if(dist1<(sa+l) && dist1>(sa-l) && dist2<(sa+l) && dist2>(sa-l) && dist3<(sa+l) && dist3>(sa-l))
                valid_points = [valid_points; [i, j]];
            end
        end
    end
end

figure (7)
set(7,'position',[1243 190 560 420])
plot(PB1(1),PB1(2),'o','Linewidth',1);
hold on
plot(PB2(1), PB2(2), 'o', 'LineWidth', 1);
hold on
plot(PB3(1), PB3(2), 'o', 'LineWidth', 1);
% link bases
plot([PB1(1),PB2(1)], [PB1(2); PB2(2)],'--','Linewidth',1);
hold on
plot([PB1(1),PB3(1)], [PB1(2); PB3(2)],'--','Linewidth',1);
hold on
plot([PB2(1),PB3(1)], [PB2(2); PB3(2)],'--','Linewidth',1);
hold on
scatter(valid_points(:, 1), valid_points(:, 2), 'filled');
xlabel('X (mm)');
ylabel('Y (mm)');
title('Valid Points in 2D Space');
grid on;



