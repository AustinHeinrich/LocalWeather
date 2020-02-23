# based on the day of the year, gets the season the user is in
# returns a String saying what season it is (Summer, Winter, Autumn, Spring)

from datetime import date, datetime


seasons = {'Summer': (datetime(2000, 6, 21), datetime(2000, 9, 22)),
           'Autumn': (datetime(2000, 9, 23), datetime(2000, 12, 20)),
           'Spring': (datetime(2000, 3, 21), datetime(2000, 6, 20))}


# date - the current date i.e. a datetime.now() method
def get_season(date):
    for season, (season_start, season_end) in seasons.items():
        if season_start <= date <= season_end:
            return season
    else:
        return 'Winter'
