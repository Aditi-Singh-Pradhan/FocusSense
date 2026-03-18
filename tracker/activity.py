import pygetwindow as gw

class ActivityTracker:
    def __init__(self):
        #distinguish between different activities based on active window
        self.productive_apps = ["Visual Studio Code", "Brave Browser"]
        self.distacting_apps = ["Spotify", "YouTube"]

    def get_activity_window(self):
        try:
            window = gw.getActiveWindow()
            if window is None:
                return "Idle"
            return window.title
        except :
            return "Unknown"
        
    def categorize_app(self, title):
        title = title.lower()

        for app in self.productive_apps:
            if app.lower() in title:
                return "Productive", 1
            
        for app in self.distacting_apps:
            if app.lower() in title:
                return "Distracting",0

        return "Neutral", 0.5
    
    def get_activity_score(self):
        title = self.get_activity_window()
        category, score = self.categorize_app(title)
        
    
        return {
            "app":title,
            "category":category,
            "score":score
        }