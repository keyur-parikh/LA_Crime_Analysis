import math
# Okay, I want to test whether my equation works. so lets run some mathematical tests


crime_area_1 = []
crime_area_2 = []
crimes = 100
for i in range(crimes):
    crime_1 = (100, 365)
    crime_2 = (70, 5)
    crime_area_1.append(crime_1)
    crime_area_2.append(crime_2)

#print(crime_area_1)
#print(crime_area_2)

# Function to assign weights based on time intervals
def get_time_weight(days):
    if days <= 7:
        return 1.2  # Crimes within the last week
    elif days <= 30:
        return 1.1  # Crimes within 1 week to 1 month
    else:
        return 1.0

def severity_factor(code):
    if code >= 85:
        return code * 2
    elif code >= 70:
        return code * 1.5
    else:
        return code

def crime_score(area, radius=1):
    total = 0
    for crime in area:
        crime_code = crime[0]
        days = crime[1]
        recency_weight = get_time_weight(days)
        severity = severity_factor(crime_code)
        total += severity * recency_weight

    return total/radius

crime_score_1 = crime_score(crime_area_1)
crime_score_2 = crime_score(crime_area_2)
#crime_score_3 = crime_score(crime_area_3)
#crime_score_4 = crime_score(crime_area_4)
#crime_score_5 = crime_score(crime_area_5)
#crime_score_6 = crime_score(crime_area_6)

print("Crime Score for Area 1 = ", crime_score_1)
print("Crime Score for Area 2 = ", crime_score_2)
#print("Crime Score for Area 3 = ", crime_score_3)
#print("Crime Score for Area 4 = ", crime_score_4)
#print("Crime Score for Area 5 = ", crime_score_5)

#print("Crime Score for Area 6 = ", crime_score_6)

print("Ratio of how much worse Area 5 is than Area 4 is", crime_score_1/ crime_score_2)