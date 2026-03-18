from core.behavior import BehaviorEngine

engine = BehaviorEngine()

# trial data

cv_data = {"face": 1, "head": 0.8, "blink": 0.02}

activity_data = { "score": 1}

score = engine.compute_focus_score(cv_data, activity_data)

print("Focus Score:", score)
