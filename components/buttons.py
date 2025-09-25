from gpiozero import Button

BUTTONS = [
    Button(9, pull_up=False, bounce_time=0.05),
    Button(11, pull_up=False, bounce_time=0.05),
    Button(10, pull_up=False, bounce_time=0.05),
    Button(5, pull_up=False, bounce_time=0.05)
]

TOGGLE_SWITCHES = [
    Button(26, pull_up=False, bounce_time=0.05),
    Button(19, pull_up=False, bounce_time=0.05),
    Button(13, pull_up=False, bounce_time=0.05),
    Button(20, pull_up=False, bounce_time=0.05)
]
