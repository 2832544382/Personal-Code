function [pts,interval,eev] = generateStraight(pt_start,pt_end,u,M)

    eev = ones(1,M+2);

    % use pdist to calcualte the distance between 2 points
    dist = pdist([pt_start(1), pt_start(2), pt_start(3); pt_end(1), pt_end(2), pt_end(3)]);

    pts = [linspace(pt_start(1),pt_end(1),M+2);...
        linspace(pt_start(2),pt_end(2),M+2);...
        linspace(pt_start(3),pt_end(3),M+2)];
    
    t_total = dist/u;
    interval = t_total/(M+2);
    eev = eev * u;
    
    pts = pts(:,2:M+1);
    eev = eev(:,2:M+1);
end