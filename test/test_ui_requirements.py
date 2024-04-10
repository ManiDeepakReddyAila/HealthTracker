from streamlit.testing.v1 import AppTest

def test_set_targets_positive():
    """
    Requirement: The system shall allow users to set the target values for running metrics.

    Pre-condition: Ensure that the system is properly configured with the necessary components for setting target values, including a user interface with input fields and buttons.

    Steps to be followed:
    1. Set up the system with appropriate configurations.
    2. Navigate to the page or section where users can set target values for running metrics.
    3. Set the target value for the maximum heart rate using the designated input field.
    4. Submit the form or click on the button to apply the set target values.

    Expected Behavior:
    The system should allow users to set the target value for the maximum heart rate by inputting the desired value into the designated input field and applying it through form submission or button click.

    Actual Behavior:
    The system's response after the target value for the maximum heart rate has been set.

    Test Result:
    The test will pass if the system successfully sets the target value for the maximum heart rate and reflects the updated value correctly in the session state associated with the target value. Otherwise, it will fail.
    """
    at = AppTest.from_file("../src/pages/2_Running.py", default_timeout=30)
    at.run()
    at.number_input[1].set_value(170).run()
    at.button[0].click().run()
    assert at.session_state["maximum_heart_rate"] == 170

def test_set_targets_negative():
    """
    Requirement: The system shall allow users to set the target values for running metrics.

    Pre-condition: Ensure that the system is properly configured with the necessary components for setting target values, including a user interface with input fields and buttons.

    Steps to be followed:
    1. Set up the system with appropriate configurations.
    2. Navigate to the page or section where users can set target values for running metrics.
    3. Set the target value for the maximum heart rate using the designated input field.
    4. Submit the form or click on the button to apply the set target values.

    Expected Behavior:
    The system should allow users to set the target value for the maximum heart rate by inputting the desired value into the designated input field and applying it through form submission or button click.

    Actual Behavior:
    The system's response after the target value for the maximum heart rate has been set.

    Test Result:
    The test will pass if the system successfully sets the target value for the maximum heart rate and reflects the updated value correctly in the session state associated with the target value. Otherwise, it will fail.
    """
    at = AppTest.from_file("../src/pages/2_Running.py", default_timeout=30)
    at.run()
    at.number_input[1].set_value(170).run()
    at.button[0].click().run()
    at.number_input[1].increment().run()
    at.button[0].click().run()
    assert at.session_state["maximum_heart_rate"] == 171

def test_heart_rate_range():
    """
    Requirement: The system shall display a warning message if the user attempts to set a maximum heart rate target value outside the range 0, 220.

    Pre-condition: Ensure that the system is properly configured with the necessary components for setting target values, including a user interface with input fields and buttons.

    Steps to be followed:

    1. Set up the system with appropriate configurations.
    2. Navigate to the page or section where users can set target values for running metrics.
    3. Attempt to set a target value for the maximum heart rate that is below the predefined minimum threshold using the designated input field.
    4. Verify if a warning message is displayed indicating that the target value is below the minimum threshold.

    Expected Behavior:
    The system should display an error message to the user if they attempt to set a maximum heart rate target value outside the range 0,220.

    Actual Behavior:
    The system's response when the user attempts to set a maximum heart rate target value outside the range 0,220.

    Test Result:
    The test will pass if the system displays an error message as expected when the user sets a maximum heart rate target value outside the range pf 0, 220. Otherwise, it will fail.
    """
    at = AppTest.from_file("../src/pages/2_Running.py", default_timeout=30)

    at.run()

    at.number_input[1].set_value(-10).run()

    at.button[0].click().run()

    assert len(at.error) == 1
    assert "Please enter a number between 0 and 220." in at.error[0].value
