data = readmatrix("C:\Users\28325\OneDrive\Desktop\dissertation\program\tra.csv");
x = data(:, 1);
y = data(:, 2);
z = data(:, 3);

figure;
plot3(x, y, z, 'LineWidth', 1);
xlabel('X (mm)');
ylabel('Y (mm)');
zlabel('Z (mm)');
title('Learning Trajectory');
grid on;

sigma = 10;
x_smooth = smoothdata(x, 'gaussian', sigma);
y_smooth = smoothdata(y, 'gaussian', sigma);
z_smooth = smoothdata(z, 'gaussian', sigma);

output_filename = 'smoothed_trajectory.csv'; 
smoothed_data = [x_smooth, y_smooth, z_smooth]; 
writematrix(smoothed_data, output_filename);

figure;
plot3(x_smooth, y_smooth, z_smooth, 'LineWidth', 1);
xlabel('X (mm)');
ylabel('Y (mm)');
zlabel('Z (mm)');
title('Gaussian Smoothed Learning Trajectory');
grid on;

xq = linspace(1, length(x_smooth), length(x_smooth) * 10);
x_interp = interp1(1:length(x_smooth), x_smooth, xq, 'linear');
y_interp = interp1(1:length(y_smooth), y_smooth, xq, 'linear');
z_interp = interp1(1:length(z_smooth), z_smooth, xq, 'linear');

figure;
plot3(x_interp, y_interp, z_interp, 'LineWidth', 1);
xlabel('X (mm)');
ylabel('Y (mm)');
zlabel('Z (mm)');
title('Interpolated Smoothed Learning Trajectory');
grid on;

selected_x = x_interp(1:18:end);
selected_y = y_interp(1:18:end);
selected_z = z_interp(1:18:end);
selected_x(end) = [];
selected_y(end) = [];
selected_z(end) = [];

selected_x = [selected_x, x_interp(end)];
selected_y = [selected_y, y_interp(end)];
selected_z = [selected_z, z_interp(end)];

figure;
plot3(selected_x, selected_y, selected_z, 'LineWidth', 1);
xlabel('X (mm)');
ylabel('Y (mm)');
zlabel('Z (mm)');
title('Final Learning Trajectory');
grid on;


data = [
    266.72348988,  36.2682015,  -42.59713885;
    266.34998076,  33.15841745, -36.74426677;
    265.94138876,  28.70590075, -29.56248783;
    265.47188445,  23.26611677, -22.68328026;
    264.89312648,  16.64075361, -17.79870132;
    264.25102214,   9.37391091, -17.72658156;
    263.61167059,   2.42104011, -21.90523577;
    263.05546379,  -4.21604108, -28.706568;
    262.56979451,  -9.79070966, -36.04175349;
    261.48341846, -15.58042851, -42.57862686
];

x = data(:, 1);
y = data(:, 2);
z = data(:, 3);

figure;
plot3(x, y, z, '-', 'LineWidth',1); % '-o' 
xlabel('X (mm)');
ylabel('Y (mm)');
zlabel('Z (mm)');
title('Comparision Trajectory');
grid on;