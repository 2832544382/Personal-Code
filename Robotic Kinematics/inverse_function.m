% File: inverse_function.m

function [th1 th2 th3 th4 th5] = inverse_function(all_par)

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
    D = (-(rw^2 + (zw - D1)^2 - L1^2 - L2^2)/(2*L1*L2));

    % if 1 - (D^2) < 0
    %     fprintf("D "+D)
    %     error('Invalid value for D');
    % end



    th3 = atan2(-sqrt(abs(1-D^2)), -D);
    
    
    %q2
    t = atan2(zw - D1,rw);
    al = atan2(L2*sin(th3) , L1 + L2*cos(th3));
    
    th2 = t - al;
    
    %q4
    th4 = phi - th3 - th2;
    
    %end effector position
    th5 = miu;
    
    par = [th1 th2 th3 th4 th5];
end