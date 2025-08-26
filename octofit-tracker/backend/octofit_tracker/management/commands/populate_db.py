from django.core.management.base import BaseCommand
from octofit_tracker.models import Team, User, Activity, Workout, Leaderboard
from datetime import datetime, timedelta
import random

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting database population...'))

        # Clear existing data
        self.stdout.write('Clearing existing data...')
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()
        User.objects.all().delete()
        Activity.objects.all().delete()
        Team.objects.all().delete()

        # Create teams
        self.stdout.write('Creating teams...')
        team_marvel = Team.objects.create(
            name='Team Marvel',
            description='Earth\'s Mightiest Heroes fighting for fitness!'
        )
        team_dc = Team.objects.create(
            name='Team DC',
            description='Justice League members staying in superhero shape!'
        )

        # Create activities
        self.stdout.write('Creating activities...')
        activities_data = [
            {'name': 'Running', 'description': 'Outdoor or treadmill running', 'points_per_unit': 10, 'unit': 'minutes'},
            {'name': 'Push-ups', 'description': 'Classic upper body exercise', 'points_per_unit': 1, 'unit': 'reps'},
            {'name': 'Cycling', 'description': 'Bike riding or stationary cycling', 'points_per_unit': 8, 'unit': 'minutes'},
            {'name': 'Swimming', 'description': 'Pool or open water swimming', 'points_per_unit': 15, 'unit': 'minutes'},
            {'name': 'Yoga', 'description': 'Mind and body wellness', 'points_per_unit': 5, 'unit': 'minutes'},
            {'name': 'Weight Lifting', 'description': 'Strength training with weights', 'points_per_unit': 12, 'unit': 'minutes'},
            {'name': 'Squats', 'description': 'Lower body strength exercise', 'points_per_unit': 1, 'unit': 'reps'},
            {'name': 'Plank', 'description': 'Core strengthening exercise', 'points_per_unit': 2, 'unit': 'minutes'},
        ]

        activities = []
        for activity_data in activities_data:
            activity = Activity.objects.create(**activity_data)
            activities.append(activity)

        # Create Marvel superhero users
        marvel_heroes = [
            {'first_name': 'Tony', 'last_name': 'Stark', 'email': 'ironman@marvel.com'},
            {'first_name': 'Steve', 'last_name': 'Rogers', 'email': 'captain@marvel.com'},
            {'first_name': 'Natasha', 'last_name': 'Romanoff', 'email': 'blackwidow@marvel.com'},
            {'first_name': 'Bruce', 'last_name': 'Banner', 'email': 'hulk@marvel.com'},
            {'first_name': 'Thor', 'last_name': 'Odinson', 'email': 'thor@asgard.com'},
            {'first_name': 'Clint', 'last_name': 'Barton', 'email': 'hawkeye@marvel.com'},
            {'first_name': 'Wanda', 'last_name': 'Maximoff', 'email': 'scarletwitch@marvel.com'},
            {'first_name': 'Peter', 'last_name': 'Parker', 'email': 'spiderman@marvel.com'},
        ]

        # Create DC superhero users
        dc_heroes = [
            {'first_name': 'Clark', 'last_name': 'Kent', 'email': 'superman@dc.com'},
            {'first_name': 'Bruce', 'last_name': 'Wayne', 'email': 'batman@dc.com'},
            {'first_name': 'Diana', 'last_name': 'Prince', 'email': 'wonderwoman@dc.com'},
            {'first_name': 'Barry', 'last_name': 'Allen', 'email': 'flash@dc.com'},
            {'first_name': 'Arthur', 'last_name': 'Curry', 'email': 'aquaman@dc.com'},
            {'first_name': 'Hal', 'last_name': 'Jordan', 'email': 'greenlantern@dc.com'},
            {'first_name': 'Victor', 'last_name': 'Stone', 'email': 'cyborg@dc.com'},
            {'first_name': 'Oliver', 'last_name': 'Queen', 'email': 'greenarrow@dc.com'},
        ]

        self.stdout.write('Creating Marvel heroes...')
        marvel_users = []
        for hero_data in marvel_heroes:
            user = User.objects.create(team=team_marvel, **hero_data)
            marvel_users.append(user)

        self.stdout.write('Creating DC heroes...')
        dc_users = []
        for hero_data in dc_heroes:
            user = User.objects.create(team=team_dc, **hero_data)
            dc_users.append(user)

        all_users = marvel_users + dc_users

        # Create workout data
        self.stdout.write('Creating workout data...')
        base_date = datetime.now() - timedelta(days=30)
        
        for user in all_users:
            total_points = 0
            # Generate 10-20 workouts per user over the last 30 days
            num_workouts = random.randint(10, 20)
            
            for _ in range(num_workouts):
                activity = random.choice(activities)
                
                # Generate realistic workout data based on activity type
                if activity.unit == 'minutes':
                    duration_or_count = random.randint(15, 90)  # 15-90 minutes
                else:  # reps
                    duration_or_count = random.randint(10, 100)  # 10-100 reps
                
                points_earned = int(duration_or_count * activity.points_per_unit)
                total_points += points_earned
                
                # Random date within the last 30 days
                workout_date = base_date + timedelta(days=random.randint(0, 30))
                
                Workout.objects.create(
                    user=user,
                    activity=activity,
                    duration_or_count=duration_or_count,
                    points_earned=points_earned,
                    date=workout_date
                )

            # Create leaderboard entry
            Leaderboard.objects.create(
                user=user,
                team=user.team,
                total_points=total_points,
                rank=0  # Will be updated after all users are created
            )

        # Update leaderboard rankings
        self.stdout.write('Updating leaderboard rankings...')
        # Marvel team rankings
        marvel_leaderboard = Leaderboard.objects.filter(team=team_marvel).order_by('-total_points')
        for rank, entry in enumerate(marvel_leaderboard, 1):
            entry.rank = rank
            entry.save()

        # DC team rankings
        dc_leaderboard = Leaderboard.objects.filter(team=team_dc).order_by('-total_points')
        for rank, entry in enumerate(dc_leaderboard, 1):
            entry.rank = rank
            entry.save()

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully populated database with:\n'
                f'- {Team.objects.count()} teams\n'
                f'- {User.objects.count()} users\n'
                f'- {Activity.objects.count()} activities\n'
                f'- {Workout.objects.count()} workouts\n'
                f'- {Leaderboard.objects.count()} leaderboard entries'
            )
        )
