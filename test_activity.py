from tracker.activity import ActivityTracker
import time

tracker = ActivityTracker()

while True:
    data = tracker.get_activity_score()

    print(f"Active Window: {data['app']}, Category: {data['category']}, Score: {data['score']}")
    print("-" * 50)

    time.sleep(5)