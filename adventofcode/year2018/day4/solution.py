from collections import (Counter, defaultdict)
from functools import total_ordering
import logging
import re

from aocd.models import Puzzle


@total_ordering
class LogDay:
    def __init__(self, log_date):
        LOG_DATE_FORMAT = re.compile(r'(\d{4})-(\d{2})-(\d{2}) '
                                     r'(\d{2}):(\d{2})')
        m = re.match(LOG_DATE_FORMAT, log_date)
        (year, month, day, hour, minute) = map(int, m.groups())
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute

    def __eq__(self, other):
        return ((self.year, self.month, self.day, self.hour,
                 self.minute) == (other.year, other.month, other.day,
                                  other.hour, other.minute))

    def __lt__(self, other):
        return ((self.year, self.month, self.day, self.hour, self.minute) <
                (other.year, other.month, other.day, other.hour, other.minute))

    def midnight_minute(self):
        if self.hour == 0:
            return self.minute
        return None

    def date(self):
        return '%4d-%02d-%02d' % (self.year, self.month, self.day)


class LogEntry:
    def __init__(self, entry):
        LOG_FORMAT = re.compile(
            r'\[(.*?)\] '
            r'(wakes up|falls asleep|Guard #(\d+) begins shift)')
        m = re.match(LOG_FORMAT, entry)
        (datestamp, event, guard_no) = m.groups()

        self.entry = entry
        self.log_day = LogDay(datestamp)
        if guard_no is not None:
            self.guard_no = int(guard_no)
        else:
            self.guard_no = None
        self.is_beginning = (guard_no is not None)
        self.fell_asleep = (event == "falls asleep")
        self.woke_up = (event == "wakes up")

    def __eq__(self, other):
        return self.log_day == other.log_day

    def __lt__(self, other):
        return self.log_day < other.log_day


def parse_log_entry(entry):
    return LogEntry(entry)


def sorted_log_entries(log):
    return sorted([LogEntry(l) for l in log])


def generate_guard_sleep_logs(log):
    guard_sleep_minutes = defaultdict(lambda: defaultdict(list))
    current_guard = None
    sleeping_minute = None

    #  Generate the list of sleep minutes
    for entry in sorted_log_entries(log):
        logging.debug("Entry: %s" % entry.entry)

        if entry.guard_no:
            logging.debug("Began shift: %d" % entry.guard_no)
            if sleeping_minute and current_guard != entry.guard_no:
                guard_sleep_minutes[current_guard][entry.log_day.date()]. \
                    extend(range(sleeping_minute, 60))
            current_guard = entry.guard_no
            sleeping_minute = None

        if entry.fell_asleep:
            sleeping_minute = entry.log_day.midnight_minute()
            logging.debug("Fell asleep: %d at %d" %
                          (current_guard, sleeping_minute))

        if entry.woke_up:
            guard_sleep_minutes[current_guard][entry.log_day.date()].extend(
                range(sleeping_minute, entry.log_day.midnight_minute()))
            logging.debug("Woke up: %d at %d (fell at %d)" %
                          (current_guard, entry.log_day.midnight_minute(),
                           sleeping_minute))
            sleeping_minute = None

    logging.debug(guard_sleep_minutes)

    guard_sleep_logs = list()
    for guard, sleep_history in guard_sleep_minutes.items():
        guard_sleep_logs.append(GuardSleepLog(guard, sleep_history))

    return guard_sleep_logs


def sleepiest_guard_in_log(log):
    guard_sleep_logs = generate_guard_sleep_logs(log)
    return sorted(guard_sleep_logs,
                  key=lambda x: x.total_minutes(),
                  reverse=True)[0]


def sleepiest_guard_minute_in_log(log):
    guard_sleep_logs = generate_guard_sleep_logs(log)

    guard_no = None
    sleepy_minute = None
    max_occurrences = 0

    for guard_sleep_log in guard_sleep_logs:
        (minute, occurrences) = guard_sleep_log.sleepy_minute_tuple()
        if occurrences > max_occurrences:
            guard_no = guard_sleep_log.no
            max_occurrences = occurrences
            sleepy_minute = minute

    logging.debug("Sleepiest guard-minute: %s: minute %s, %s times".format(
        guard_no, sleepy_minute, occurrences))
    return (guard_no, sleepy_minute, occurrences)


class GuardSleepLog:
    def __init__(self, guard, sleep_history):
        self.no = guard
        self.sleep_history = sleep_history

    def sleepy_minute(self):
        return self.sleepy_minute_tuple()[0]

    def sleepy_minute_tuple(self):
        minute_counter = Counter()
        for _, minutes in self.sleep_history.items():
            minute_counter.update(minutes)
        return minute_counter.most_common(1)[0]

    def total_minutes(self):
        count = 0
        for _, minutes in self.sleep_history.items():
            count += len(minutes)
        return count


if __name__ == '__main__':
    puzzle = Puzzle(year=2018, day=4)
    guard_log = puzzle.input_data.split('\n')

    sleepy = sleepiest_guard_in_log(guard_log)
    print("Problem 1:", sleepy.no * sleepy.sleepy_minute())

    sleepy_guard_minute = sleepiest_guard_minute_in_log(guard_log)
    print("Problem 2:", sleepy_guard_minute[0] * sleepy_guard_minute[1])
