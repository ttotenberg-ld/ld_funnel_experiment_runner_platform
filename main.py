from dotenv import load_dotenv #pip install python-dotenv
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


'''
Get environment variables
'''
load_dotenv()

SDK_KEY = os.environ.get('SDK_KEY')
NUMBER_OF_ITERATIONS = int(os.environ.get('NUMBER_OF_ITERATIONS'))


'''
Experiment variables
'''
flag_key = "config-ai-model"
funnel_metric_1 = "ai-analyze-clicked"
funnel_metric_2 = "financial-advisor-contacted"
ai_csat_positive_metric = "ai-csat-positive"
ai_csat_negative_metric = "ai-csat-negative"
ai_response_latency = "ai-response-latency"
ai_cost = "ai-analysis-cost"


'''
Metrics logic
'''
funnel_metric_1_percent_converted = 30

control_funnel_metric_2_percent_converted = 40
control_ai_csat_positive_percent_converted = 30
control_ai_csat_negative_percent_converted = 5
control_ai_response_latency_range = [50, 175]
control_ai_cost_range = [0.0020, 0.0040]


t1_funnel_metric_2_percent_converted = 23
t1_ai_csat_positive_percent_converted = 23
t1_ai_csat_negative_percent_converted = 11
t1_ai_response_latency_range = [65, 220]
t1_ai_cost_range = [0.0120, 0.0150]


t2_funnel_metric_2_percent_converted = 55
t2_ai_csat_positive_percent_converted = 36
t2_ai_csat_negative_percent_converted = 4
t2_ai_response_latency_range = [72, 389]
t2_ai_cost_range = [0.0015, 0.0025]


'''
Initialize the LaunchDarkly SDK
'''
ldclient.set_config(Config(SDK_KEY))


'''
It's just fun :)
'''
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


'''
Return the month duration they sign up for. Expecting most people to pick 12 months, with fewer on 24 or 36
'''
def calc_numeric_value():
    value = random.randint(1, 100)
    if value <= 43:
        return 12
    elif value <= 76:
        return 24
    else:
        return 36


'''
Conversion true or false calculator.
Pass in TRUE_PERCENT_CONVERTED or FALSE_PERCENT_CONVERTED, which refer to the true/false flag variation served
'''
def conversion_chance(chance_number):
    chance_calc = random.randint(1, 100)
    if chance_calc <= chance_number:
        return True
    else:
        return False


'''
Calculates whether the context will convert. If they do, executes the track call for that context.
'''
def execute_call_if_converted(metric, percent_chance, context):
    user_context = context.get_individual_context('user')
    context_name = user_context.get('name')
    if conversion_chance(int(percent_chance)):
        ldclient.get().track(metric, context)
        print(f"User {context_name} converted for {metric}")
        return True
    else:
        print(f"User {context_name} did NOT convert for {metric}")
        return False


'''
Calculates CSAT
'''
def calc_csat(positive_csat, negative_csat, context):
    value = random.randint(1, 100)
    if value <= positive_csat:
        print("CSAT: Positive")
        ldclient.get().track("ai-csat-positive", context)
    elif value <= negative_csat:
        print("CSAT: Negative")
        ldclient.get().track("ai-csat-negative", context)
    else:
        print("CSAT: None")

'''
Evaluate the flags for randomly generated users, and make the track() calls to LaunchDarkly
'''
def callLD():
    # Primary loop to evaluate flags and send track events
    for i in range(NUMBER_OF_ITERATIONS):
        context = create_multi_context()
        user_context = context.get_individual_context('user')
        context_name = user_context.get('name')
        print(f"USER: {context_name}")

        flag_detail = ldclient.get().variation_detail(flag_key, context, 'unavailable')
        index = flag_detail.variation_index

        # Execute funnel metric 1 at the same percentage chance, because that should be the same regardless of the model configuration
        if execute_call_if_converted(funnel_metric_1, funnel_metric_1_percent_converted, context):      
            if index == 0:
                print("Serving Control")
                # Track latency
                latency = random.randint(control_ai_response_latency_range[0], control_ai_response_latency_range[1])
                ldclient.get().track("ai-response-latency", context, metric_value=latency)
                print(f"LATENCY: {latency}ms")
                # Track cost
                cost = random.uniform(control_ai_cost_range[0], control_ai_cost_range[1])
                ldclient.get().track("ai-analysis-cost", context, metric_value=cost)
                # Track CSAT
                calc_csat(control_ai_csat_positive_percent_converted, control_ai_csat_negative_percent_converted, context)
                # Track funnel metric 2 if they convert
                execute_call_if_converted(funnel_metric_2, control_funnel_metric_2_percent_converted, context)

            elif index == 1:
                print("Serving Treatment 1")
                # Track latency
                latency = random.randint(t1_ai_response_latency_range[0], t1_ai_response_latency_range[1])
                ldclient.get().track("ai-response-latency", context, metric_value=latency)
                print(f"LATENCY: {latency}ms")
                # Track cost
                cost = random.uniform(t1_ai_cost_range[0], t1_ai_cost_range[1])
                ldclient.get().track("ai-analysis-cost", context, metric_value=cost)
                # Track CSAT
                calc_csat(t1_ai_csat_positive_percent_converted, t1_ai_csat_negative_percent_converted, context)
                # Track funnel metric 2 if they convert
                execute_call_if_converted(funnel_metric_2, t1_funnel_metric_2_percent_converted, context)

            elif index == 2:
                print("Serving Treatment 2")
                # Track latency
                latency = random.randint(t2_ai_response_latency_range[0], t2_ai_response_latency_range[1])
                ldclient.get().track("ai-response-latency", context, metric_value=latency)
                print(f"LATENCY: {latency}ms")
                # Track cost
                cost = random.uniform(t2_ai_cost_range[0], t2_ai_cost_range[1])
                ldclient.get().track("ai-analysis-cost", context, metric_value=cost)
                # Track CSAT
                calc_csat(t2_ai_csat_positive_percent_converted, t2_ai_csat_negative_percent_converted, context)
                # Track funnel metric 2 if they convert
                execute_call_if_converted(funnel_metric_2, t2_funnel_metric_2_percent_converted, context)
            else:
                pass


'''
Execute!
'''
show_banner()
callLD()


'''
Responsibly close the LD Client
'''
ldclient.get().close()