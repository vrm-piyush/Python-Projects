# Alarm Clock Program

![alarm clock](image.png)

## Project Overview

The Alarm Clock Program is a simple Python application that allows users to set an alarm by entering the desired time in the format (HH:MM:SS AM/PM). When the set time is reached, the program triggers an alarm sound using the 'pygame' library and displays a wake-up message.

## Features

- **Time Input:**

  - Users can set an alarm by entering the desired time in a 12-hour format (HH:MM:SS AM/PM).

- **Validation:**

  - The program validates the format and components of the entered alarm time, providing feedback on any errors.

- **Alarm Sound:**

  - Utilizes the 'pygame' library to play an alarm sound when the set time is reached.

- **Wake-Up Message:**
  - Displays a wake-up message when the alarm is triggered.

## How to Use

1. **Run the Program:**

   - Execute the program and follow the on-screen prompts.

2. **Set Alarm:**

   - Enter the desired alarm time in the format (HH:MM:SS AM/PM).

3. **Validation:**

   - The program validates the entered time, providing feedback on any errors.

4. **Alarm Trigger:**
   - Once the set time is reached, an alarm sound is played, and a wake-up message is displayed.

## Example

```bash
cd AlarmClock
python alarm_clock.py
```

```python
Enter the time of the alarm to be set in 12-hour format (HH:MM:SS AM/PM): 08:30:00 AM

Setting alarm for 08:30:00 AM...
Wake Up!!
```

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/vrm-piyush/AlarmClock.git
   ```

2. Navigate to the project directory:

   ```bash
   cd AlarmClock
   ```

3. Install the required library:

   ```bash
   pip install pygame
   ```

4. Run the program:

   ```bash
   python alarm_clock.py
   ```

## Contribution Guidelines

Contributions are welcome! If you have ideas for improvements or encounter any issues, please open an [issue](https://github.com/vrm-piyush/AlarmClock/issues) or submit a pull request.

---
