from djongo import models

class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'teams'
    
    def __str__(self):
        return self.name

class User(models.Model):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='members')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'users'
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Activity(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    points_per_unit = models.IntegerField()
    unit = models.CharField(max_length=20)  # e.g., 'minutes', 'reps', 'miles'
    
    class Meta:
        db_table = 'activities'
    
    def __str__(self):
        return self.name

class Workout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workouts')
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    duration_or_count = models.FloatField()  # duration in minutes or count/reps
    points_earned = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'workouts'
    
    def __str__(self):
        return f"{self.user} - {self.activity} - {self.points_earned} points"

class Leaderboard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    total_points = models.IntegerField(default=0)
    rank = models.IntegerField()
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'leaderboard'
        unique_together = ('user', 'team')
    
    def __str__(self):
        return f"{self.user} - {self.total_points} points"
