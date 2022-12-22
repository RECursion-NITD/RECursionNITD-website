import csv
from datetime import datetime, timedelta
import pytz
import copy
from difflib import SequenceMatcher


def search_event(qs, search_query: str) -> list:
    events_list = qs
    events_found = []
    for event in events_list:
        if SequenceMatcher(None, event.title.lower(), search_query.lower()).ratio() > 0.28:
            events_found.append([SequenceMatcher(None, event.title.lower(), search_query.lower()).ratio(), event])
        if SequenceMatcher(None, event.description.lower(), search_query.lower()).ratio() > 0.5:
            events_found.append([SequenceMatcher(None, event.description.lower(), search_query.lower()).ratio(), event])
    events_found.sort(key=lambda x: x[0], reverse=True)
    return [event[1] for event in events_found]
