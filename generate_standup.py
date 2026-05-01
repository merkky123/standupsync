#!/usr/bin/env python3
"""
StandupSync - Automated Standup Summary Generator

This script reads your daily work notes and generates three formatted standup summaries:
1. Markdown format (for documentation and wikis)
2. Slack format (for team chat channels)
3. Email format (for formal communication)

Usage:
    python generate_standup.py

The script will:
- Read work notes from input/my_work_notes.txt
- Generate three formatted summaries
- Save them to the output/ folder with today's date in the filename
"""

# Import required libraries
import os  # For file path operations
from datetime import datetime  # For getting today's date
import re  # For text pattern matching (regular expressions)


def read_work_notes(file_path):
    """
    Read the work notes file and return its contents.
    
    Args:
        file_path (str): Path to the work notes file
        
    Returns:
        str: Contents of the work notes file
        
    Raises:
        FileNotFoundError: If the work notes file doesn't exist
    """
    try:
        # Open the file in read mode with UTF-8 encoding
        with open(file_path, 'r', encoding='utf-8') as file:
            # Read all contents and return
            return file.read()
    except FileNotFoundError:
        # If file doesn't exist, show helpful error message
        print(f"Error: Could not find work notes file at {file_path}")
        print("Please make sure the file exists and try again.")
        raise


def parse_work_notes(notes_content):
    """
    Parse the work notes and extract key information.
    
    This function analyzes the work notes to identify:
    - Accomplishments (completed tasks)
    - Blockers (things preventing progress)
    - Planned work (what's coming next)
    - Metrics (PRs, commits, issues, etc.)
    
    Args:
        notes_content (str): Raw content from work notes file
        
    Returns:
        dict: Parsed information organized by category
    """
    # Initialize a dictionary to store parsed information
    parsed_data = {
        'accomplishments': [],
        'blockers': [],
        'planned_work': [],
        'metrics': {
            'prs_created': 0,
            'prs_reviewed': 0,
            'issues_resolved': 0,
            'commits': 0
        }
    }
    
    # Split notes into lines for processing
    lines = notes_content.split('\n')
    
    # Track which section we're currently reading
    in_blockers_section = False
    in_notes_section = False
    
    # Process each line
    for line in lines:
        line = line.strip()  # Remove leading/trailing whitespace
        
        # Check if we're entering the BLOCKERS section
        if line.startswith('BLOCKERS:'):
            in_blockers_section = True
            in_notes_section = False
            continue
        
        # Check if we're entering the NOTES section
        if line.startswith('NOTES:'):
            in_notes_section = True
            in_blockers_section = False
            continue
        
        # Process blockers
        if in_blockers_section and line.startswith('-'):
            parsed_data['blockers'].append(line[2:])  # Remove "- " prefix
        
        # Look for accomplishments (lines with "Commit:" indicate completed work)
        if 'Commit:' in line or 'commit:' in line.lower():
            parsed_data['accomplishments'].append(line)
            parsed_data['metrics']['commits'] += 1
        
        # Look for PR mentions
        if 'PR #' in line or 'pr #' in line.lower():
            if 'created' in line.lower() or 'draft' in line.lower():
                parsed_data['metrics']['prs_created'] += 1
            if 'reviewed' in line.lower() or 'review' in line.lower():
                parsed_data['metrics']['prs_reviewed'] += 1
        
        # Look for resolved issues
        if 'issue #' in line.lower() and ('resolved' in line.lower() or 'fixed' in line.lower()):
            parsed_data['metrics']['issues_resolved'] += 1
        
        # Look for planned work (lines starting with "Tomorrow:")
        if line.lower().startswith('tomorrow:'):
            planned_text = line.split(':', 1)[1].strip()
            parsed_data['planned_work'].append(planned_text)
    
    return parsed_data


def generate_markdown_summary(notes_content, parsed_data, date_str):
    """
    Generate a Markdown-formatted standup summary.
    
    Args:
        notes_content (str): Original work notes content
        parsed_data (dict): Parsed information from work notes
        date_str (str): Today's date as a string
        
    Returns:
        str: Formatted Markdown summary
    """
    # Start building the Markdown document
    markdown = f"""# Daily Standup Summary
**Date:** {date_str}  
**Team Member:** [Your Name]

---

## 🎯 Yesterday's Accomplishments

### Feature Development
"""
    
    # Add accomplishments if any were found
    if parsed_data['accomplishments']:
        for accomplishment in parsed_data['accomplishments'][:5]:  # Limit to first 5
            markdown += f"- {accomplishment}\n"
    else:
        markdown += "- See detailed work notes for full activity log\n"
    
    markdown += """
---

## 📋 Today's Plan

"""
    
    # Add planned work if any was found
    if parsed_data['planned_work']:
        for i, task in enumerate(parsed_data['planned_work'], 1):
            markdown += f"{i}. {task}\n"
    else:
        markdown += "1. Continue work from yesterday\n2. Address any PR feedback\n3. Update documentation\n"
    
    markdown += """
---

## 🚧 Blockers & Dependencies

"""
    
    # Add blockers if any were found
    if parsed_data['blockers']:
        for blocker in parsed_data['blockers']:
            markdown += f"⚠️ {blocker}\n\n"
    else:
        markdown += "No blockers at this time.\n"
    
    markdown += """
---

## 📊 Metrics

"""
    
    # Add metrics
    metrics = parsed_data['metrics']
    markdown += f"""- **Pull Requests:** {metrics['prs_created']} created, {metrics['prs_reviewed']} reviewed
- **Issues Resolved:** {metrics['issues_resolved']}
- **Commits:** {metrics['commits']}
"""
    
    return markdown


def generate_slack_summary(notes_content, parsed_data, date_str):
    """
    Generate a Slack-formatted standup summary.
    
    Args:
        notes_content (str): Original work notes content
        parsed_data (dict): Parsed information from work notes
        date_str (str): Today's date as a string
        
    Returns:
        str: Formatted Slack message
    """
    # Start building the Slack message with emojis
    slack = f"""📅 *Daily Standup - {date_str}*

---

✅ *YESTERDAY'S WINS*

"""
    
    # Add accomplishments
    if parsed_data['accomplishments']:
        for accomplishment in parsed_data['accomplishments'][:3]:  # Limit to top 3
            slack += f"• {accomplishment}\n"
    else:
        slack += "• Completed various development tasks (see work notes for details)\n"
    
    slack += """
---

🎯 *TODAY'S FOCUS*

"""
    
    # Add planned work
    if parsed_data['planned_work']:
        for i, task in enumerate(parsed_data['planned_work'], 1):
            slack += f"{i}. {task}\n"
    else:
        slack += "1. Continue development work\n2. Code reviews and documentation\n"
    
    slack += """
---

"""
    
    # Add blockers if any
    if parsed_data['blockers']:
        slack += "⚠️ *BLOCKERS*\n\n"
        for blocker in parsed_data['blockers']:
            slack += f"🚨 {blocker}\n"
        slack += "\n---\n\n"
    
    # Add metrics
    metrics = parsed_data['metrics']
    slack += f"""📊 *Quick Stats*
PRs: {metrics['prs_created']} created, {metrics['prs_reviewed']} reviewed | Issues: {metrics['issues_resolved']} resolved | Commits: {metrics['commits']}

💬 _Questions or concerns? Drop a message in #dev-team_
"""
    
    return slack


def generate_email_summary(notes_content, parsed_data, date_str):
    """
    Generate an email-formatted standup summary.
    
    Args:
        notes_content (str): Original work notes content
        parsed_data (dict): Parsed information from work notes
        date_str (str): Today's date as a string
        
    Returns:
        str: Formatted email message
    """
    # Start building the email
    email = f"""Subject: Daily Standup Update - {date_str}

Hi Team,

Here's my standup update for today:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

YESTERDAY'S ACCOMPLISHMENTS

"""
    
    # Add accomplishments
    if parsed_data['accomplishments']:
        for accomplishment in parsed_data['accomplishments']:
            email += f"• {accomplishment}\n"
    else:
        email += "• Completed various development and collaboration tasks\n"
        email += "• See detailed work notes for complete activity log\n"
    
    email += """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TODAY'S PRIORITIES

"""
    
    # Add planned work
    if parsed_data['planned_work']:
        for i, task in enumerate(parsed_data['planned_work'], 1):
            email += f"{i}. {task}\n"
    else:
        email += "1. Continue work from yesterday\n"
        email += "2. Address any feedback on open pull requests\n"
        email += "3. Update documentation and Jira tickets\n"
    
    email += """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""
    
    # Add blockers if any
    if parsed_data['blockers']:
        email += "BLOCKERS & ASSISTANCE NEEDED\n\n"
        for blocker in parsed_data['blockers']:
            email += f"⚠️ {blocker}\n\n"
        email += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
    
    # Add metrics
    metrics = parsed_data['metrics']
    email += f"""METRICS SUMMARY

Pull Requests: {metrics['prs_created']} created, {metrics['prs_reviewed']} reviewed
Issues Resolved: {metrics['issues_resolved']}
Commits: {metrics['commits']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Please let me know if you have any questions or need additional details.

Best regards,
[Your Name]
"""
    
    return email


def save_summary(content, file_path):
    """
    Save a summary to a file.
    
    Args:
        content (str): The summary content to save
        file_path (str): Path where the file should be saved
    """
    try:
        # Create the output directory if it doesn't exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # Write the content to the file
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        
        print(f"✓ Saved: {file_path}")
    except Exception as e:
        print(f"✗ Error saving {file_path}: {str(e)}")


def main():
    """
    Main function that orchestrates the standup summary generation.
    
    This function:
    1. Reads the work notes file
    2. Parses the notes to extract key information
    3. Generates three different summary formats
    4. Saves each summary to the output folder
    """
    print("StandupSync - Generating Daily Standup Summaries")
    print("=" * 50)
    
    # Define file paths
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Define input and output paths relative to script location
    input_file = os.path.join(script_dir, 'input', 'my_work_notes.txt')
    output_dir = os.path.join(script_dir, 'output')
    
    # Get today's date in YYYY-MM-DD format
    today = datetime.now()
    date_str = today.strftime('%Y-%m-%d')
    date_display = today.strftime('%B %d, %Y')  # e.g., "May 01, 2026"
    
    print(f"\nDate: {date_display}")
    print(f"Reading work notes from: {input_file}")
    
    # Step 1: Read the work notes file
    try:
        notes_content = read_work_notes(input_file)
        print(f"✓ Successfully read work notes ({len(notes_content)} characters)")
    except FileNotFoundError:
        print("\n✗ Failed to read work notes. Exiting.")
        return
    
    # Step 2: Parse the work notes
    print("\nParsing work notes...")
    parsed_data = parse_work_notes(notes_content)
    print(f"✓ Found {len(parsed_data['accomplishments'])} accomplishments")
    print(f"✓ Found {len(parsed_data['blockers'])} blockers")
    print(f"✓ Found {parsed_data['metrics']['commits']} commits")
    
    # Step 3: Generate summaries in all three formats
    print("\nGenerating summaries...")
    
    # Generate Markdown summary
    markdown_summary = generate_markdown_summary(notes_content, parsed_data, date_display)
    markdown_file = os.path.join(output_dir, f'standup_{date_str}.md')
    save_summary(markdown_summary, markdown_file)
    
    # Generate Slack summary
    slack_summary = generate_slack_summary(notes_content, parsed_data, date_display)
    slack_file = os.path.join(output_dir, f'standup_{date_str}_slack.txt')
    save_summary(slack_summary, slack_file)
    
    # Generate Email summary
    email_summary = generate_email_summary(notes_content, parsed_data, date_display)
    email_file = os.path.join(output_dir, f'standup_{date_str}_email.txt')
    save_summary(email_summary, email_file)
    
    # Step 4: Summary complete
    print("\n" + "=" * 50)
    print("✓ All summaries generated successfully!")
    print(f"\nOutput files saved to: {output_dir}")
    print(f"  - {os.path.basename(markdown_file)}")
    print(f"  - {os.path.basename(slack_file)}")
    print(f"  - {os.path.basename(email_file)}")
    print("\nYou can now copy these summaries to your preferred communication channels.")


# This is the entry point of the script
# When you run "python generate_standup.py", this code executes
if __name__ == '__main__':
    main()

# Made with Bob
