"""
Behavior engine for computing focus score.

Combines computer vision signals and app activity data
to calculate a real-time focus score (0–100).
"""

class BehaviorEngine:
    def __init__(self):
        pass

    def compute_focus_score(self, cv_data, activity_data):                    # helper function to compute focus score based on CV data and activity data

        #factors from computer vision
        face = cv_data.get("face")        
        head = cv_data.get("head")   
        blink = cv_data.get("blink")
        app = activity_data 

        # normalise blink (for fatgiue detection)
        blink_score = max(0, 1 - blink * 10)

        # simple weighted average for focus score
        focus_score = (
            face * 0.4 + 
            head * 0.3 + 
            blink_score * 0.2 + 
            app * 0.1    
        )

        if not hasattr(self, "prev_score"):
            self.prev_score = focus_score

        focus_score = 0.7 * self.prev_score + 0.3 * focus_score
        self.prev_score = focus_score

        return round(focus_score * 100, 2)
        
