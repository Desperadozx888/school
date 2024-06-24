import math
import random
import sys
#ChowKeiren 7233450

class ActivitySimuEngine:
    def __init__(self, eventStats):
        self.eventStats = eventStats

    def random_time(self):
        hour = random.randint(0, 23)
        minute = random.randint(0, 59)
        second = random.randint(0, 59)
        return f"{hour:02d}-{minute:02d}-{second:02d}"

    def logs_generator(self, days, prefix):
        print(f"Stimulating Events for {days} Days")
        for i in range(days):
            event_log = []
            for event in self.eventStats:
                if event.eventType == 'C':
                    value = event.get_rand_value()
                    event_log.append(f"{self.random_time()}:{event.eventName}:{value:.2f}")
                elif event.eventType == 'D':
                    events = round(event.get_rand_value())
                    for _ in range(events):
                        event_log.append(f"{self.random_time()}:{event.eventName}:1")

            event_log.sort()
            with open(f"{prefix}_{i + 1}.txt", 'w') as file:
                for line in event_log:
                    file.write(line + '\n')

        print(f"Completed Events Stimulation for {days} Days\n")


class EventIdentifier:
    def __init__(self, eventName, eventType, minValue, maxValue, weight):
        self.eventName = eventName
        self.eventType = eventType
        self.minValue = minValue
        self.maxValue = maxValue
        self.weight = weight
        self.mean = (minValue + maxValue) / 2
        self.standardDev = (maxValue - minValue) / 2

    @classmethod
    def clone_events(cls, events):
        return [cls(event.eventName, event.eventType, event.minValue, event.maxValue, event.weight) for event in events]

    def get_rand_value(self):
        while True:
            value = self.mean + self.standardDev * random.gauss(0, 1)
            if self.eventType == 'D':
                value = round(value)
            if self.minValue <= value <= self.maxValue:
                return value

    def get_event_name(self):
        return self.eventName

    def get_mean(self):
        return self.mean

    def get_weight(self):
        return self.weight

    def get_standard_dev(self):
        return self.standardDev

    def set_mean(self, mean):
        self.mean = mean

    def set_standard_dev(self, standard_dev):
        self.standardDev = standard_dev


class AnalysisEngine:
    def __init__(self, eventStats):
        self.eventStats = eventStats

    def event_day_calculation(self, filename):
        event_counts = [0] * len(self.eventStats)

        with open(filename, 'r') as file:
            for line in file:
                delimited = line.strip().split(":")

                if len(delimited) != 3:
                    continue

                eventName = delimited[1]
                eventValue = float(delimited[2])
                for j, event in enumerate(self.eventStats):
                    if event.get_event_name() == eventName:
                        event_counts[j] += eventValue

        return event_counts

    def logs_processor(self, days, prefix):
        all_event_counts = []
        for i in range(days):
            event_counts = self.event_day_calculation(f"{prefix}_{i + 1}.txt")
            all_event_counts.append(event_counts)

            with open(f"{prefix}_{i + 1}_stats.txt", 'w') as file:
                for j, event in enumerate(self.eventStats):
                    file.write(f"{event.get_event_name()}:{event_counts[j]}\n")

        calculated_events = EventIdentifier.clone_events(self.eventStats)
        with open(f"total_{prefix}_stats.txt", 'w') as file, open(f"{prefix}_events.txt", 'w') as file1:
            for j, event in enumerate(self.eventStats):
                sum_counts = sum(counts[j] for counts in all_event_counts)
                mean = sum_counts / days

                sum_diffs = sum((counts[j] - mean) ** 2 for counts in all_event_counts)
                std = math.sqrt(sum_diffs / days)

                calculated_events[j].set_mean(mean)
                calculated_events[j].set_standard_dev(std)

                print(f"Stats generated for {event.get_event_name()}:\nMean: {mean:.2f}\nStandard Deviation: {std:.2f}\n")
                file.write(f"{event.get_event_name()}:{mean:.2f}:{std:.2f}\n")

                # Additional calculations
                max_value = int(mean + std)
                min_value = int(round(mean - std))

                cont_value = round(min_value + (max_value - min_value) * random.random(), 2)
                disc_value = random.randint(min_value, max_value + 1)

                print(f"Continuous Baseline of {event.get_event_name()}: {cont_value}")
                print(f"Discrete Baseline of {event.get_event_name()}: {disc_value}\n")
                print("========================================================================\n")
                file1.write(f"{event.get_event_name()}:C:{min_value}:{max_value}:{cont_value}\n")
                file1.write(f"{event.get_event_name()}:D:{min_value}:{max_value}:{disc_value}\n")

        print("Analysis of Events Completed\n")
        return calculated_events


class AlertEngine:
    def __init__(self, baseStats):
        self.baseStats = baseStats

    def alert_detector(self, days, prefix):
        analysis_engine = AnalysisEngine(self.baseStats)

        sum_weights = sum(event.get_weight() for event in self.baseStats)
        alert_limit = 2 * sum_weights
        print(f"Start alert analysis, detecting anomaly\nAnomaly threshold: {alert_limit}")
        alert = False

        for i in range(days):
            day_totals = analysis_engine.event_day_calculation(f"{prefix}_{i + 1}.txt")

            anomaly = 0
            for j, base_stat in enumerate(self.baseStats):
                temp = abs(
                    (day_totals[j] - base_stat.get_mean()) * base_stat.get_weight() / base_stat.get_standard_dev())
                anomaly += temp

            if anomaly > alert_limit:
                print(f"Day {i + 1}: Anomaly detected || weight: {anomaly:.2f}")
                alert = True
            else:
                print(f"Day {i + 1}: No Anomaly detected || weight: {anomaly:.2f}")

        if not alert:
            print("No Anomaly detected")


def read_event_text(filename):
    with open(filename, 'r') as file:
        counter = int(file.readline().strip())
        all_events = []
        for _ in range(counter):
            line = file.readline().strip()
            parts = line.split(":")

            if len(parts) != 6:
                print(f"Invalid line format: {line}")
                continue

            event_name, event_type, min_range_str, max_range_str, weight_str = parts[:-1]

            min_range_value = float(min_range_str) if min_range_str else 0
            max_range_value = float(max_range_str) if max_range_str else float('inf')
            weight_val = float(weight_str) if weight_str else 0

            all_events.append(EventIdentifier(event_name, event_type, min_range_value, max_range_value, weight_val))
        return all_events, counter


def read_stats_text(filename, event_types):
    with open(filename, 'r') as file:
        counter = int(file.readline().strip())
        for _ in range(counter):
            line = file.readline().strip()
            parts = line.split(":")

            if len(parts) < 3:
                print(f"Invalid line format (not enough data): {line}")
                continue

            event_name, mean_str, standard_dev_str = parts[:3]

            mean_value = float(mean_str)
            standard_dev_value = float(standard_dev_str)

            match_found = False
            for event in event_types:
                if event.get_event_name() == event_name:
                    event.set_mean(mean_value)
                    event.set_standard_dev(standard_dev_value)
                    match_found = True
                    break

            if not match_found:
                print(f"Error: Event name '{event_name}' in Stats.txt does not match any event in Events.txt.")
                sys.exit(-1)
        return counter


def main():
    if len(sys.argv) != 4:
        print("Correct usage: python main_program.py Events.txt Stats.txt Days")
        sys.exit(-1)

    event_input, events_count = read_event_text(sys.argv[1])
    stats_count = read_stats_text(sys.argv[2], event_input)
    num_of_days = int(sys.argv[3])

    # Check if the counts match
    if events_count != stats_count:
        print(
            f"Error: The number of events in Events.txt ({events_count}) does not match the number in Stats.txt ({stats_count}).")
        sys.exit(-1)

    event_input_activity_eng = ActivitySimuEngine(event_input)
    print("Generating Events from Stats.txt based on number of Days\n")
    event_input_activity_eng.logs_generator(num_of_days, "base_day")

    event_input_analysis_eng = AnalysisEngine(event_input)
    print("Analyzing Events from Stats.txt based on number of Days\n")
    base_stats = event_input_analysis_eng.logs_processor(num_of_days, "base_day")

    while True:
        line = input("Enter new Stats.txt and Days in the format (new Stats.txt Days || Or press 0 to quit): ")
        if line == "0":
            print("Exiting program")
            sys.exit(0)

        print(line)
        delimited = line.split(" ")

        if len(delimited) == 2:
            live_days = int(delimited[1])
            new_stats = EventIdentifier.clone_events(event_input)
            read_stats_text(delimited[0], new_stats)

            live_activity_engine = ActivitySimuEngine(new_stats)
            print("Generating Events from new Stats.txt based on number of Days\n")
            live_activity_engine.logs_generator(live_days, "live_day")

            live_activity_engine = AnalysisEngine(new_stats)
            print("Analyzing Events from new Stats.txt based on number of Days\n")
            live_activity_engine.logs_processor(live_days, "live_day")

            alert_engine = AlertEngine(base_stats)
            alert_engine.alert_detector(live_days, "live_day")
        else:
            print("Correct usage: newStats.txt Days")


if __name__ == "__main__":
    main()
