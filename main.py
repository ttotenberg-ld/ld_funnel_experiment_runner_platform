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
FLAG_NAME = os.environ.get('FLAG_NAME')
FUNNEL_METRIC_1 = os.environ.get('FUNNEL_METRIC_1')
FUNNEL_METRIC_2 = os.environ.get('FUNNEL_METRIC_2')
FUNNEL_METRIC_3 = os.environ.get('FUNNEL_METRIC_3')
SECONDARY_CONVERSION_METRIC = os.environ.get('SECONDARY_CONVERSION_METRIC')
SECONDARY_NUMERIC_METRIC = os.environ.get('SECONDARY_NUMERIC_METRIC')
FUNNEL_1_PERCENT_CONVERTED = int(os.environ.get('FUNNEL_1_PERCENT_CONVERTED'))
FUNNEL_2_PERCENT_CONVERTED = int(os.environ.get('FUNNEL_2_PERCENT_CONVERTED'))
FUNNEL_3_TRUE_PERCENT_CONVERTED = int(os.environ.get('FUNNEL_3_TRUE_PERCENT_CONVERTED'))
FUNNEL_3_FALSE_PERCENT_CONVERTED = int(os.environ.get('FUNNEL_3_FALSE_PERCENT_CONVERTED'))
SECONDARY_CONVERSION_TRUE_PERCENT = int(os.environ.get('SECONDARY_CONVERSION_TRUE_PERCENT'))
SECONDARY_CONVERSION_FALSE_PERCENT = int(os.environ.get('SECONDARY_CONVERSION_FALSE_PERCENT'))
NUMBER_OF_ITERATIONS = int(os.environ.get('NUMBER_OF_ITERATIONS'))

print(f"SDK_KEY: {SDK_KEY}")

'''
Initialize the LaunchDarkly SDK
'''
ldclient.set_config(Config(SDK_KEY, private_attributes=["age"]))


'''
Create fake contexts for this data
'''
def create_contexts():
    num_contexts = NUMBER_OF_ITERATIONS
    contexts_array = []
    for i in range(num_contexts):
        context = create_multi_context()
        json.dumps(contexts_array.append(context))
        with open('data/contexts.json', 'w') as f:
            f.write(str(contexts_array))

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
Evaluate the flags for randomly generated users, and make the track() calls to LaunchDarkly
'''
def callLD():
    # Create the number of contexts you want to evaluate
    create_contexts()
    contexts = json.load(open("data/contexts.json"))

    # Primary loop to evaluate flags and send track events
    for i in contexts:

        loop_context = Context.from_dict(i)
        flag_variation = ldclient.get().variation(FLAG_NAME, loop_context, False)

        # Execute metrics 1 and 2 at the same percentage chance, because those should be the same regardless of the interrupted flow
        if execute_call_if_converted(FUNNEL_METRIC_1, FUNNEL_1_PERCENT_CONVERTED, loop_context):
            if execute_call_if_converted(FUNNEL_METRIC_2, FUNNEL_2_PERCENT_CONVERTED, loop_context):
                # Add a condition to check the flag now, to see if adding the extra step interrupts final conversion
                if flag_variation:
                    execute_call_if_converted(SECONDARY_CONVERSION_METRIC, SECONDARY_CONVERSION_TRUE_PERCENT, loop_context)
                    ldclient.get().track(SECONDARY_NUMERIC_METRIC, loop_context, metric_value=calc_numeric_value())
                    execute_call_if_converted(FUNNEL_METRIC_3, FUNNEL_3_TRUE_PERCENT_CONVERTED, loop_context)
                else:
                    execute_call_if_converted(SECONDARY_CONVERSION_METRIC, SECONDARY_CONVERSION_FALSE_PERCENT, loop_context)
                    ldclient.get().track(SECONDARY_NUMERIC_METRIC, loop_context, metric_value=calc_numeric_value())
                    execute_call_if_converted(FUNNEL_METRIC_3, FUNNEL_3_FALSE_PERCENT_CONVERTED, loop_context)


'''
Execute!
'''
callLD()


'''
Responsibly close the LD Client
'''
ldclient.get().close()