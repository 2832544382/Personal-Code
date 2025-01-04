% Create an instance of SolidCube
center = [1.5, 1, 2];
sideLength = 0.3;

cube = SolidCube(center, sideLength);

% Draw the solid cube and print out information for each point


% 
% % Print the figure to an image file (e.g., PNG)
% print('solid_cube.png', '-dpng', '-r300');  % Adjust the filename and format as needed
% 

u = 0.1;            % Speed of end effector in Cartesian space
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

motionFlag = 0; 

time = zeros(1,M * (numRows - 1) + numRows);
point_set = zeros(5,M * (numRows - 1) + numRows);
velocity_set = zeros(1,M * (numRows - 1) + numRows);

row_size = size(point_set, 1);

num_points = size(numRows, 1);

t_i = 0; % time at pose i
t_f = 3; % time at pose f = i + 1

c_samples = 50; % cartesian samples between each pose
j_samples = 50; % joint samples to form our trajectory

poly = 10;

q = zeros(1, 6);  % 初始化 q

points = zeros(size(viapoints,1) * c_samples, 3);

figure;
hold on;

all_points = [];


for i=1:size(viapoints, 1) - 1
    p_start_point = viapoints(i,:);
    p_end_point = viapoints(i+1,:);

    path = choose_the_shortest_path(p_start_point,p_end_point,cube,30);

    all_points = [all_points, path];
    % Plot the path
    plot3(path(1, :), path(2, :), path(3, :), '-o', 'DisplayName', ['Path ', num2str(i)]);

    % Mark the start and end points
    scatter3(p_start_point(1), p_start_point(2), p_start_point(3), 'filled', 'Marker', 's', 'DisplayName', ['Start ', num2str(i)]);
    scatter3(p_end_point(1), p_end_point(2), p_end_point(3), 'filled', 'Marker', 'd', 'DisplayName', ['End ', num2str(i)]);
    plot3(all_points(1, :), all_points(2, :), all_points(3, :), '-x', 'DisplayName', 'Connected Paths');

end
cube.draw();

hold off;
grid on;
xlabel('X');
ylabel('Y');
zlabel('Z');
title('3D Paths Between Viapoints');
legend;
function path = choose_the_shortest_path(start,destination,cube,M)

    mini_distance_insert = inf;
    insertPoint = [1 ,1 ,1];
    mini_distance_exit = inf;
    exitPoint = [1 ,1 ,1];

     % Initialize arrays to store points
    intermediate_points = zeros(3, M);

    passes_through_q = false;

    x_point_start_to_destination = linspace(start(1), destination(1), M + 2);
    y_point_start_to_destination = linspace(start(2), destination(2), M + 2);
    z_point_start_to_destination = linspace(start(3), destination(3), M + 2);

    for i = 1:M

        point = [x_point_start_to_destination(i); y_point_start_to_destination(i); z_point_start_to_destination(i)];

        % Store intermediate point
        intermediate_points(:, i) = point;
        if cube.point_inside(point')
            passes_through_q = true;
            % Calculate the distance from the point to the destination
            dist_to_start = norm(point - start(1:3)')
            dist_to_destination = norm(point - destination(1:3)');

            % Update the minimum distance and insertion point
            if dist_to_start < mini_distance_insert
                mini_distance_insert = dist_to_start;
                insertPoint = [x_point_start_to_destination(i), y_point_start_to_destination(i), z_point_start_to_destination(i)];
                insertPoint = cube.closest_point_on_surface(point');
            end

            if dist_to_destination < mini_distance_exit
                mini_distance_exit = dist_to_destination;
                exitPoint = [x_point_start_to_destination(i), y_point_start_to_destination(i), z_point_start_to_destination(i)];
                exitPoint = cube.closest_point_on_surface(point');
            end
        end
    end


    % Create points along the trajectory from start to insertPoint
    x_point_start_to_insert = linspace(start(1), insertPoint(1), M);
    y_point_start_to_insert = linspace(start(2), insertPoint(2), M);
    z_point_start_to_insert = linspace(start(3), insertPoint(3), M);


    x_point_insert_to_exit = linspace(insertPoint(1), exitPoint(1), M);
    y_point_insert_to_exit = linspace(insertPoint(2), exitPoint(2), M);
    z_point_insert_to_exit = linspace(insertPoint(3), exitPoint(3), M);


    % Create points along the trajectory from insertPoint to exitPoint
    % Check if the straight path intersects with the cube
    if passes_through_q
        path = [x_point_start_to_insert; y_point_start_to_insert; z_point_start_to_insert];
        rightmostPoint = rightmost_point_on_surface(cube, insertPoint);
        plot3(rightmostPoint(1), rightmostPoint(2), rightmostPoint(3), 'r*', 'MarkerSize', 10);

        x_point_start_to_rightmost = linspace(start(1), rightmostPoint(1), M);
        y_point_start_to_rightmost = linspace(start(2), rightmostPoint(2), M);
        z_point_start_to_rightmost = linspace(start(3), rightmostPoint(3), M);

        x_point_end_to_rightmost = linspace(destination(1), rightmostPoint(1), M);
        y_point_end_to_rightmost = linspace(destination(2), rightmostPoint(2), M);
        z_point_end_to_rightmost = linspace(destination(3), rightmostPoint(3), M);

        plot3(x_point_start_to_rightmost, y_point_start_to_rightmost, z_point_start_to_rightmost, 'b-', 'LineWidth', 2);
        plot3(x_point_end_to_rightmost, y_point_end_to_rightmost, z_point_end_to_rightmost, 'b-', 'LineWidth', 2);

        % Connect start to rightmostPoint to destination
    else
        path = [x_point_start_to_destination; y_point_start_to_destination; z_point_start_to_destination];
    end

    % Combine the points to form the complete path
end


function avoidance = avoid_cube(insertPoint, exitPoint, cube)
    % Connect insert point to the rightmost point on the cube's surface and
    % then connect to the opposite surface while avoiding the cube

    % Find the rightmost point on the cube's surface on the same plane as
    % the insert point
    rightmostPoint = rightmost_point_on_surface(cube, insertPoint);

    % Find the two points on the opposite surface
    oppositePoints = find_opposite_surface_points(cube, rightmostPoint);

    % Combine the points to form the complete avoidance path
    avoidance = [insertPoint'; rightmostPoint'; oppositePoints'; exitPoint'];
end

function rightmostPoint = rightmost_point_on_surface(obj, point)
    % Calculate the rightmost point on the surface of the cube
    halfSide = 1.5 * obj.SideLength / 2;  % 调整倍数以改变离表面的距离

    % Find the rightmost point on the same plane as the insert point
    rightmostPoint = obj.Center;
    rightmostPoint(2) = obj.Center(2) + halfSide;  % 改变 Y 坐标
end

function oppositePoints = find_opposite_surface_points(obj, point)
    % Calculate two points on the opposite surface of the cube
    halfSide = obj.SideLength / 2;

    % Find the center of the opposite surface
    oppositeCenter = obj.Center;
    oppositeCenter(1) = obj.Center(1) - obj.SideLength;

    % Find two points on the opposite surface by offsetting from the center
    oppositePoint1 = oppositeCenter + [0, halfSide, 0];
    oppositePoint2 = oppositeCenter - [0, halfSide, 0];

    oppositePoints = [oppositePoint1'; oppositePoint2'];
end




