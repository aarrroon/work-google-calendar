from datetime import date
import holidays

# Select country
uk_holidays = holidays.country_holidays('AU').items()

t2 = date.fromisoformat('2002-05-05')
t1 = date.fromisoformat('2002-06-05')

print((t2-t1).total_seconds())