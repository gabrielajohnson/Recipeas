import re

from .models import User, Recipe

# Formats 00:00:00 time format into readable hours,minutes and seconds format
def format_duration(value):
    stringValue = str(value)
    if stringValue == "00:00:00":
        duration = "No Time Needed"
        return duration
    timeCounter = 0
    # regex pattern will match each set of numbers in 00:00:00
    patterns = ["(?<!:)(\d\d):", ":(\d\d):", ":(\d\d)$"]
    times = [" hours ", " minutes ", " seconds "]
    duration = ""
    # Iterates through each of the 3 sets of numbers and adds the corresponding
    # Time measure to end of string
    for pattern in patterns:
        p = re.compile(pattern)
        result = p.search(stringValue)
        intResult = int(result.group(1))
        if intResult > 0:
            string = str(intResult) + str(times[timeCounter])
            duration += string
        timeCounter += 1
    # Duration is readable string that can be printed to recipe template
    return duration

# Formats steps and ingredients by removing blank lines
def format_steps(value):
    stringValue = value
    stringValue = re.sub(r"^(?:[\t ]*(?:\r?\n|\r))+", "", stringValue, 0, re.MULTILINE)
    return stringValue

# Gets amount of ingredients in list
def get_ingredient_length(value):
    stringValue = value
    matches = re.findall(r".*\S.*", stringValue, re.MULTILINE)
    length = len(matches)
    return length

# Adds preptime and cooktime to get total time needed to make recipe
def get_total_time(prepTime, cookTime):
    prepTime = str(prepTime)
    cookTime = str(cookTime)
    cookingTimes = [prepTime, cookTime]
    timeCounter = 0
    patterns = ["(?<!:)(\d\d):", ":(\d\d):", ":(\d\d)$"]
    times = [" hours ", " minutes ", " seconds "]
    total = 0

    # Converts hours, minutes and seconds to minutes
    for time in cookingTimes:
        for pattern in patterns:
            p = re.compile(pattern)
            result = p.search(time)
            intResult = int(result.group(1))
            if timeCounter == 0:
                minutes = intResult*60
            elif timeCounter == 1:
                minutes = intResult
            elif timeCounter == 2:
                minutes = intResult/60
            # Adds converted time to total time
            total += minutes
            timeCounter += 1

        timeCounter = 0
    # total time returned in minutes and saved to recipe
    return total
