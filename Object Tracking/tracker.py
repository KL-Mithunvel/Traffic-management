import math

class Tracker:
    def __init__(self):
        # Dictionary to store the center positions of detected objects
        self.center_points = {}
        # Counter for assigning unique IDs to new objects
        self.id_count = 0

    def update(self, objects_rect):
        # List to store bounding boxes and their corresponding IDs
        objects_bbs_ids = []

        # Calculate the center point of each detected object
        for rect in objects_rect:
            x, y, w, h = rect
            cx = (x + x + w) // 2
            cy = (y + y + h) // 2

            # Check if the object has already been detected
            same_object_detected = False
            for id, pt in self.center_points.items():
                distance = math.hypot(cx - pt[0], cy - pt[1])

                if distance < 35:
                    self.center_points[id] = (cx, cy)
                    objects_bbs_ids.append([x, y, w, h, id])
                    same_object_detected = True
                    break

            # Assign a new ID to a newly detected object
            if not same_object_detected:
                self.center_points[self.id_count] = (cx, cy)
                objects_bbs_ids.append([x, y, w, h, self.id_count])
                self.id_count += 1

        # Remove IDs that are no longer used
        new_center_points = {}
        for obj_bb_id in objects_bbs_ids:
            _, _, _, _, object_id = obj_bb_id
            center = self.center_points[object_id]
            new_center_points[object_id] = center

        # Update the dictionary with active IDs
        self.center_points = new_center_points.copy()
        return objects_bbs_ids
