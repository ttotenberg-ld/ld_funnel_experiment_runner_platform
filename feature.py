from dotenv import load_dotenv  # pip install python-dotenv
import ldclient
from ldclient.config import Config
from ldclient.context import Context
import json
import names
import os
import random
import time
import uuid
from utils.create_context import create_multi_context


"""
Get environment variables
"""
load_dotenv()

SDK_KEY = os.environ.get("SDK_KEY")
NUMBER_OF_ITERATIONS = int(os.environ.get("NUMBER_OF_ITERATIONS"))


"""
Flag + experiment metrics
"""
flag_key = "my-flag-key"
metric_key_1 = "metric-key-1"
metric_key_2 = "metric-key-2"


"""
Metrics logic
"""
control_metric_1_range = [500, 1750]
control_metric_2_range = [0.04, 0.06]


t1_metric_1_range = [650, 2200]
t1_metric_2_range = [0.04, 0.05]


"""
Initialize the LaunchDarkly SDK
"""
ldclient.set_config(Config(SDK_KEY))


"""
It's just fun :)
"""


def show_banner():
    print()
    print("        ██       ")
    print("          ██     ")
    print("      ████████   ")
    print("         ███████ ")
    print("██ LAUNCHDARKLY █")
    print("         ███████ ")
    print("      ████████   ")
    print("          ██     ")
    print("        ██       ")
    print()


"""
Evaluate the flags for randomly generated users, and make the track() calls to LaunchDarkly
"""


def callLD():
    # Primary loop to evaluate flags and send track events
    for i in range(NUMBER_OF_ITERATIONS):
        context = create_multi_context()
        user_context = context.get_individual_context("user")
        context_name = user_context.get("name")
        print(f"USER: {context_name}")

        flag_detail = ldclient.get().variation_detail(flag_key, context, "unavailable")
        index = flag_detail.variation_index

        if index == 0:
            print("Serving Control")
            # Track Metric 1
            metric_1 = random.randint(
                control_metric_1_range[0],
                control_metric_1_range[1],
            )
            ldclient.get().track(metric_key_1, context, metric_value=metric_1)
            print(f"METRIC 1: {metric_1}")
            # Track Metric 2
            metric_2 = random.uniform(
                control_metric_2_range[0], control_metric_2_range[1]
            )
            ldclient.get().track(metric_key_2, context, metric_value=metric_2)
            print(f"METRIC 2: {metric_2}")

        elif index == 1:
            print("Serving Treatment 1")
            # Track Metric 1
            metric_1 = random.randint(
                t1_metric_1_range[0],
                t1_metric_1_range[1],
            )
            ldclient.get().track(metric_key_1, context, metric_value=metric_1)
            print(f"METRIC 1: {metric_1}")
            # Track Metric 2
            metric_2 = random.uniform(t1_metric_2_range[0], t1_metric_2_range[1])
            ldclient.get().track(metric_key_2, context, metric_value=metric_2)
            print(f"METRIC 2: {metric_2}")

        else:
            pass


"""
Execute!
"""
show_banner()
callLD()


"""
Responsibly close the LD Client
"""
ldclient.get().close()
