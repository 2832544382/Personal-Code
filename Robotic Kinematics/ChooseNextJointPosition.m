function q = ChooseNextJointPosition(q1, q2, q3, q4, q5, lastq)
    % Find the best q set for the specific position
    % The q variables are deduced from inverse kinematics

    if isnan(lastq) % No last q: start position
        q = [q1, q2, q3, q4, q5]';
    else
        if length(q2) == 1
            q = [q1, q2, q3, q4, q5]';
        else
            temp = [q1, q2(1), q3(1), q4(1), q5; q1, q2(2), q3(2), q4(2), q5]';
            % Choose the column closer to the previous
            if rand > 0.5
                q = temp(:, 2);
            else
                q = temp(:, 3);
            end
        end
    end
end
