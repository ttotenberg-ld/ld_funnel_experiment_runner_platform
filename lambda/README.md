# LaunchDarkly Platform Demo Experiment populator
Populates experiment data for the platform demo.

## To use:
1. `pip install -r /path/to/requirements.txt`
2. `python main.py`

## For Lambda URL:

Method: POST
Body: {
    "sdk_key": "sdk-abcd1234-5678-0987-abcdef123456",
    "num_iterations": 1548
}

Maximum number of iterations is 5000.
