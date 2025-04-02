# Eisenhower Matrix Task Manager

A Streamlit application that implements the Eisenhower Matrix for task management with Gmail integration.

## Features

- Organize tasks in four quadrants:
  - Urgent & Important (Do)
  - Not Urgent & Important (Schedule)
  - Not Urgent & Not Important (Eliminate)
  - Urgent & Not Important (Delegate)
- Add, edit, and delete tasks
- Gmail integration to import emails as tasks
- Persistent storage of tasks

## Updated Setup Instructions

### Local Development

```bash
# Install dependencies
pip install -r app/requirements.txt

# Run the app
streamlit run app/main.py
```

### Streamlit Cloud Deployment

1. Connect your GitHub repository to Streamlit Cloud
2. Select the app path as: `app/main.py`
3. Make sure to add your Google API credentials in Streamlit Cloud Secrets

The app is now organized entirely within the app folder for cleaner structure and easier deployment.

## Usage

1. **Connect to Gmail**: Use the sidebar to authenticate with Gmail
2. **Add Tasks**: Enter task details in any quadrant and click "Add Task"
3. **Import Emails**: After connecting to Gmail, use the sidebar to fetch and import emails as tasks
4. **Manage Tasks**: Edit, delete, or move tasks between quadrants
5. **Save Tasks**: Click the "Save Tasks" button to persist your tasks

## How the Eisenhower Matrix Works

The Eisenhower Matrix is a productivity tool for prioritizing tasks based on their urgency and importance:

- **Urgent & Important**: Tasks that need immediate attention
- **Not Urgent & Important**: Tasks that are important but can be scheduled
- **Urgent & Not Important**: Tasks that are urgent but can be delegated
- **Not Urgent & Not Important**: Tasks that can be eliminated or minimized 