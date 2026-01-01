import math

def cast_ray(road_mask, start_pos, angle_deg, max_distance=200):
    x, y = start_pos
    angle_rad = math.radians(angle_deg)

    for dist in range(1, max_distance):
        test_x = int(x+math.cos(angle_rad) * dist)
        test_y = int(y-math.sin(angle_rad) * dist)

        # Outside screen → treat as off-road
        if not (0 <= test_x < road_mask.get_size()[0] and
                0 <= test_y < road_mask.get_size()[1]):
            return dist
        
        # If pixel is NOT road -> border hit
        if road_mask.get_at((test_x, test_y)) == 0:
            return dist
        
    return max_distance
        
