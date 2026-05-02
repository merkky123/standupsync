# StandupSync

**Automated Standup Summary Generator with Git Integration**

StandupSync is a Python-based tool that transforms your daily work notes into professional standup summaries. It automatically fetches your git commits, merges them with your manual notes, and generates formatted summaries in three different formats: Markdown, Slack, and Email.

## Features

- 📝 **Automated Summary Generation**: Converts work notes into structured standup updates
- 🔄 **Git Integration**: Automatically fetches and includes today's git commits
- 📊 **Metrics Tracking**: Tracks PRs, commits, issues resolved, and more
- 🎯 **Multiple Formats**: Generates Markdown, Slack, and Email-ready summaries
- ⚡ **Easy to Use**: Simple command-line interface

## How to Run

1. **Add your work notes** to `input/my_work_notes.txt`
   - Document your daily activities, accomplishments, and blockers
   - Use the provided template format for best results

2. **Run the script**:
   ```bash
   python src/generate_standup.py
   ```

3. **Find your summaries** in the `output/` folder:
   - `standup_YYYY-MM-DD.md` - Markdown format
   - `standup_YYYY-MM-DD_slack.txt` - Slack format
   - `standup_YYYY-MM-DD_email.txt` - Email format

## Bob Session Reports

This project was built with assistance from Bob, an AI coding assistant. Session reports documenting the development process can be found in the [bob_sessions](./bob_sessions) folder.

## Project Structure

```
StandupSync/
├── src/
│   └── generate_standup.py    # Main script
├── input/
│   └── my_work_notes.txt       # Your daily work notes
├── output/                     # Generated summaries
├── bob_sessions/               # Bob AI session reports
└── slash_commands/             # Custom slash commands
```

## Requirements

- Python 3.6 or higher
- Git (optional, for automatic commit tracking)

## IBM Hackathon Project

This project was created for the IBM hackathon to demonstrate automated workflow optimization and developer productivity tools.
