u = 2;            % Speed of end effector in Cartesian space
M = 30;             % Number of samples

deg2rad = pi/180;

pose0 = inverse_function([5.2,0,0.5,0,0]);
pose1 = inverse_function([0,0,-1,-90*deg2rad,0]);
pose2 = inverse_function([1,1,1,0,0]);
pose3 = inverse_function([1,1,2,0,0]);
pose4 = inverse_function([2,1,2,0,0]);
pose5 = inverse_function([2,1,1,0,0]);

thetas = [pose1; pose2; pose3; pose4; pose5];

l1 = 2 ;
l2 = 3 ;
l3 = 0.2 ;
l4 = 2 ;
l5 = 2 ;


alpha = [0,90,0,0,90,0]'*pi/180;
a = [0,l1,l2,0,0,0]';
d = [0.5,0,0,0,0,l3]';

viapoints = [0,0,-1,-90*deg2rad,0;
            1,1,1,0,0;
            1,1,2,0,0;
            2,1,2,0,0;
            2,1,1,0,0;];

numRows = size(viapoints, 1);

time = zeros(1,M * (numRows - 1) + numRows);
point_set = zeros(5,M * (numRows - 1) + numRows);

q = zeros(1, 6);  % 初始化 q


for i = 1:size(viapoints, 1) - 1
    p_start_point = viapoints(i,:);
    p_end_point = viapoints(i+1,:);

    [pts,interval] = generateStraight(p_start_point,p_end_point,u,M);

    plot3(pts(1, :), pts(2, :), pts(3, :), '-o', 'LineWidth', 2);
    hold on;

    for j = (i-1)*(M+1)+1:i*(M+1)+1
        if j == 1
            time(j) = 0;
        else
            time(j) = time(j-1)+interval;
        end
    end


    ik_sample = zeros(5,M);
    frames_pos_samples = zeros(3,5+1,M);
    HT_samples = zeros(4,4,M);

    pose = viapoints(i,:);

    [q1,q2,q3,q4,q5] = inverse_function(p_start_point);

    q = ChooseNextJointPosition(q1,q2,q3,q4,q5,q);

    p_start_point = q;

    frames_pos = zeros(3,6);
    frames_pos0 = [0,0,0]';

    deg2rad = pi/180;
    depth12 = 0.5;
    link23 = 2;
    link34 = 3;
    link5e = 0.2;

    a = thetas;
    
    t12 = dh(0, 90*deg2rad, depth12, p_start_point(1));
    t23 = dh(link23, 0, 0, p_start_point(2));
    t34 = dh(link34, 0, 0, p_start_point(3));
    t45 = dh(0, 90*deg2rad, 0, p_start_point(4) + 90*deg2rad);
    t5e = dh(0, 0, link5e, p_start_point(5));

    frames_pos(:,1) = t12(1:3,4);
    frames_pos(:,2) = t23(1:3,4);
    frames_pos(:,3) = t34(1:3,4);
    frames_pos(:,4) = t45(1:3,4);
        
    
    HT = t5e;
    frames_pos_start(:,5+1) = p_start_point;

    for sample_point=1:M
        [q1,q2,q3,q4,q5] = inverse_function([pts(1, :), pts(2, :), pts(3, :),pose(4),0]);
        q = ChooseNextJointPosition(q1,q2,q3,q4,q5,q);
        ik_sample(:,sample_point) = q;

        t12 = dh(0, 90*deg2rad, depth12, q(1));
        t23 = dh(link23, 0, 0, q(2));
        t34 = dh(link34, 0, 0, q(3));
        t45 = dh(0, 90*deg2rad, 0, q(4) + 90*deg2rad);
        t5e = dh(0, 0, link5e, q(5));
    
        frames_pos(:,1) = t12(1:3,4);
        frames_pos(:,2) = t23(1:3,4);
        frames_pos(:,3) = t34(1:3,4);
        frames_pos(:,4) = t45(1:3,4);


        frames_pos = [frames_pos];


        frames_pos_start(:,5+1) = p_start_point;
        
        frames_pos(:,5+1) = pts(:,sample_point); % adjust end-effector position
        frames_pos_samples(:,:,sample_point) = frames_pos;
        HT_samples(:,:,sample_point) = HT;
    end

    [q1,q2,q3,q4,q5] = inverse_function([p_end_point(1),p_end_point(2),p_end_point(3),p_end_point(4),p_end_point(5)]);% Ensured to be effective
    q = ChooseNextJointPosition(q1,q2,q3,q4,q5,q);
    p_end_point = q;

    t12 = dh(0, 90*deg2rad, depth12, p_end_point(1));
    t23 = dh(link23, 0, 0, p_end_point(2));
    t34 = dh(link34, 0, 0, p_end_point(3));
    t45 = dh(0, 90*deg2rad, 0, p_end_point(4) + 90*deg2rad);
    t5e = dh(0, 0, link5e, p_end_point(5));

    frames_pos(:,1) = t12(1:3,4);
    frames_pos(:,2) = t23(1:3,4);
    frames_pos(:,3) = t34(1:3,4);
    frames_pos(:,4) = t45(1:3,4);

    HT_end = t5e;
    frames_pos = [frames_pos];
    frames_pos_end(:,5+1) = p_end_point; % adjust end-effector position
    point_set(:,(i-1)*(M+1)+1:i*(M+1)+1) = [p_start_point ik_sample p_end_point];    % save q
end

title('Generated Straight Line Trajectories');
xlabel('X');
ylabel('Y');
zlabel('Z');
grid on;

figure(2);
subplot(1,2,1);
for l=1:5
    plot(time, rad2deg(point_set(l, :)), '-'); % Use '-' for connecting lines
    hold on;
end
xlabel('Time');
ylabel('Joint positions');
legend('q1','q2','q3','q4','q5');
axis square

subplot(1,2,2);

time_trajectory = linspace(0, max(time), 100); % Adjust the number of points as needed
velocity_trajectory = u * ones(size(time_trajectory));

plot(time_trajectory, velocity_trajectory, '-');
title('Constant Velocity Trajectory');
xlabel('Time');
ylabel('Velocity of end-effector');
axis square

function par = fowardee(q1, q2, q3, q4, q5)

    deg2rad = pi/180;
    
    %link length
    depth12 = 0.5;
    link23 = 2;
    link34 = 3;
    link5e = 0.2;


    t12 = dh(0,90*deg2rad,depth12,q1);
    t23 = dh(link23,0,0,q2);
    t34 = dh(link34,0,0,q3);
    t45 = dh(0,90*deg2rad,0,q4+90*deg2rad);
    t5e = dh(0,0,link5e,q5);  
    
    t1e = t12*t23*t34*t45*t5e;
    
    xe = t1e(1,4);
    ye = t1e(2,4);
    ze = t1e(3,4);
    
    par = [xe ye ze];
end

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






