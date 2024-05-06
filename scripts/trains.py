import trainline
import os
import datetime
import csv
import io

DEPARTURE_STATION = os.environ.get("DEPARTURE_STATION") or "Genève"
ARRIVAL_STATION = os.environ.get("ARRIVAL_STATION") or "Chambéry"

# Fetch next train from now to end of day
results = trainline.search(
    departure_station=DEPARTURE_STATION,
    arrival_station=ARRIVAL_STATION,
    from_date=datetime.datetime.now().strftime("%d/%m/%Y %H:%M"),
    to_date=datetime.datetime.now()
    .replace(hour=22, minute=59)
    .strftime("%d/%m/%Y %H:%M"),
    transportation_mean="train",
)

# Convert results CSV to JSON
trains = []

csv_data = results.csv()
csv_file = io.StringIO(csv_data)

csv_result = csv.DictReader(csv_file)

for row in csv_result:
    values = row[
        "departure_date;arrival_date;duration;number_of_segments;price;currency;transportation_mean;bicycle_reservation"
    ].split(";")
    train = {
        "departure_date": values[0],
        "arrival_date": values[1],
        "duration": values[2],
        "number_of_segments": values[3],
        "price": values[4],
    }

    trains.append(train)


# Display current date & time
print("📅 TODAY", datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
print("-------------------------")

print("🚉​​ Departure station: " + DEPARTURE_STATION)
print("🚉​​ Arrival station: " + ARRIVAL_STATION + "\n")

# Display next train
if len(trains) > 0:
    print("🚆🕒 Next train:")
    next_train = trains[0]
    departure_time = datetime.datetime.strptime(
        next_train["departure_date"], "%d/%m/%Y %H:%M"
    ).strftime("%H:%M")
    arrival_time = datetime.datetime.strptime(
        next_train["arrival_date"], "%d/%m/%Y %H:%M"
    ).strftime("%H:%M")
    duration = datetime.datetime.strptime(next_train["duration"], "%Hh%M")
    print(f"   Departure Time: {departure_time} ⏰")
    print(f"   Arrival Time: {arrival_time} 🕛")
    print(f"   Duration: {duration.strftime('%Hh%M')}")

# Display every other trains
if len(trains) > 1:
    print("\n✨ Other Trains:")
    for i, train in enumerate(trains[1:], start=1):
        departure_time = datetime.datetime.strptime(
            train["departure_date"], "%d/%m/%Y %H:%M"
        ).strftime("%H:%M")
        arrival_time = datetime.datetime.strptime(
            train["arrival_date"], "%d/%m/%Y %H:%M"
        ).strftime("%H:%M")
        duration = datetime.datetime.strptime(train["duration"], "%Hh%M")
        print(
            f"{i}. Departure: {departure_time} ⏰    Arrival: {arrival_time} 🕔    Duration: {duration.strftime('%Hh%M')}"
        )
