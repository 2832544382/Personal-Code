classdef SolidCube
    properties
        Center
        SideLength
    end
    
    methods
        function obj = SolidCube(center, sideLength)
            obj.Center = center;
            obj.SideLength = sideLength;
        end

        function closestPoint = closest_point_on_surface(obj,point)
            %Calculate the closet point on the cube's surface to the given
            %point

            %Find the point inside the cube
            insidePoint = max(min(point, obj.Center + obj.SideLength/2),obj.Center - obj.SideLength/2);

            %Calculate the distance from the input point to the inside
            %point
            distToInside = norm(point - insidePoint);

            % Calculate the closest point on the surface
            closestPoint = point;
            for i = 1:3
                % if abs(point(i) - obj.Center(i) + obj.SideLength(i)/2) < abs(point(i) - closestPoint(i))
                %     closestPoint(i) = obj.Center(i) + obj.SideLength(i)/2;
                % end
                % if abs(point(i) - obj.Center(i) - obj.SideLength(i)/2) < abs(point(i) - closestPoint(i))
                %     closestPoint(i) = obj.Center(i) - obj.SideLength(i)/2;
                % end
                halfSide = obj.SideLength / 2;
                closestPoint = point;

                closestPoint(1) = max(min(closestPoint(1), obj.Center(1) + halfSide), obj.Center(1) - halfSide);
                closestPoint(2) = max(min(closestPoint(2), obj.Center(2) + halfSide), obj.Center(2) - halfSide);
                closestPoint(3) = max(min(closestPoint(3), obj.Center(3) + halfSide), obj.Center(3) - halfSide);
            end
        end
        
        function inside = point_inside(obj, point)
            % Check if a point is inside the cube
            halfSide = obj.SideLength / 2;
            inside = all(abs(point - obj.Center) <= halfSide);
            % if inside
            %     disp(['Point [', num2str(point), '] is inside the cube.']);
            % else
            %     disp(['Point [', num2str(point), '] is outside the cube.']);
            % end
        end

        
        function draw(obj)
            hold on;
            
            % Define cube vertices
            vertices = [
                -1, -1, -1;
                -1, -1,  1;
                -1,  1, -1;
                -1,  1,  1;
                 1, -1, -1;
                 1, -1,  1;
                 1,  1, -1;
                 1,  1,  1;
            ];
        
            % Scale vertices based on side length
            vertices = obj.SideLength / 2 * vertices;
        
            % Translate vertices based on center
            vertices = bsxfun(@plus, vertices, obj.Center);
        
            % Define cube faces
            faces = [
                1, 2, 6, 5;
                2, 4, 8, 6;
                4, 3, 7, 8;
                3, 1, 5, 7;
                5, 6, 8, 7;
                1, 2, 4, 3;
            ];
        
            % Plot the cube
            patch('Vertices', vertices, 'Faces', faces, 'FaceColor', 'g');
            
            % Print out information for each point
            for i = 1:size(vertices, 1)
                point = vertices(i, :);
            end
            
            hold off;
            axis equal;
            grid on;
            xlabel('X');
            ylabel('Y');
            zlabel('Z');
            title('Solid Cube');
            
            % Set view to 3D
            view(3);
        end

        function edge = closest_edge_to_point(obj, point)
            % Find the closest edge on the cube to the given point
            
            % Get all edges of the cube
            edges = obj.get_all_edges();
            
            % Calculate distances from each edge to the point
            distances = vecnorm(edges - point', 2, 1);
            
            % Find the index of the closest edge
            [~, closestEdgeIndex] = min(distances);
            
            % Extract the closest edge
            edge = edges(:, closestEdgeIndex);
        end


        function edges = get_all_edges(obj)
            % Get all edges of the cube
            
            % Define cube vertices
            vertices = [
                -1, -1, -1;
                -1, -1,  1;
                -1,  1, -1;
                -1,  1,  1;
                 1, -1, -1;
                 1, -1,  1;
                 1,  1, -1;
                 1,  1,  1;
            ];
        
            % Scale vertices based on side length
            vertices = obj.SideLength / 2 * vertices;
        
            % Translate vertices based on center
            vertices = bsxfun(@plus, vertices, obj.Center);
            
            % Define cube edges
            edges = [
                vertices(1, :)', vertices(2, :)';
                vertices(2, :)', vertices(4, :)';
                vertices(4, :)', vertices(3, :)';
                vertices(3, :)', vertices(1, :)';
                
                vertices(5, :)', vertices(6, :)';
                vertices(6, :)', vertices(8, :)';
                vertices(8, :)', vertices(7, :)';
                vertices(7, :)', vertices(5, :)';
                
                vertices(1, :)', vertices(5, :)';
                vertices(2, :)', vertices(6, :)';
                vertices(3, :)', vertices(7, :)';
                vertices(4, :)', vertices(8, :)';
            ];
        end
    end
end
