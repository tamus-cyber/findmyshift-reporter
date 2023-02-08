#!/usr/bin/env python3
"""Main program for FindMyShift Shift Reporter"""

import os
import sys
import json
import csv
import argparse
from loguru import logger
from slack_sdk import WebClient
from dotenv import load_dotenv
from fms_lib import get_employees_without_shifts, get_employees
load_dotenv()


def send_to_slack(slack_token: str, slack_channel: str, data: dict, **kwargs):
    """Send data to Slack channel
    Args:
        slack_token (str): Slack token
        slack_channel (str): Slack channel
        data (dict): Data
    """
    # Convert dict to bulleted list
    bulleted_list = '\n'.join([f'- {employee["display_name"]}' for employee in data])
    slack_message = f'*Employees with empty FindMyShift:*\n{bulleted_list}'

    # Setup Slack client
    client = WebClient(token=slack_token)
    # Parse optional arguments
    username = kwargs.get('username', 'FMS Shift Reporter')
    icon_emoji = kwargs.get('icon_emoji', ':robot_face:')
    logger.debug(slack_message)
    # Send message to Slack channel
    response = client.chat_postMessage(channel=slack_channel, text=slack_message, \
                                       username=username, icon_emoji=icon_emoji)
    assert response["ok"] # nosec B101


def filter_employees(employees: list, blacklist: list, aliases: dict):
    """Filter employees
    Args:
        employees (list): List of employees
        blacklist (list): List of staff IDs to blacklist
        aliases (dict): Dictionary of aliases
    Returns:
        list: List of filtered employees
    """
    filtered_employees = []
    for employee in employees:
        if employee['staff_id'] in blacklist:
            continue
        if employee['staff_id'] in aliases:
            employee['display_name'] = aliases[employee['staff_id']]
        filtered_employees.append(employee)
    return filtered_employees


def save_to_file(filename: str, data: dict, output_format: str):
    """Save data to file
    Args:
        filename (str): Filename
        data (dict): Data
        format (str): Format to save data as (json, csv, html, txt)
    """
    supported_formats = ['json', 'csv', 'html', 'txt']
    if output_format not in supported_formats:
        raise ValueError(f'Invalid format: {output_format}. Supported formats: {supported_formats}')
    if output_format == 'csv':
        with open(filename, 'w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['staff_id', 'display_name'])
            for employee in data:
                writer.writerow([employee['staff_id'], employee['display_name']])
    else:
        with open(filename, 'w', encoding='utf-8') as file:
            if output_format == 'json':
                json.dump(data, file, indent=4)
            elif output_format == 'html':
                file.write('<table>')
                file.write('<tr><th>Employee Name</th></tr>')
                for employee in data:
                    file.write(f'<tr><td>{employee["display_name"]}</td></tr>')
                file.write('</table>')
            elif output_format == 'txt':
                for employee in data:
                    file.write(f'{employee["display_name"]}\n')


@logger.catch # Catch any errors
def main():
    """Main function"""

    # Parse command line arguments
    parser = argparse.ArgumentParser(description='FindMyShift Shift Reporter')
    parser.add_argument('-f', '--format', type=str, help='Output format', \
                        choices=['json', 'csv', 'html', 'txt'], default='json')
    parser.add_argument('-d', '--days', type=int, help='Number of days to fetch', default=7)
    parser.add_argument('-a', '--all', action='store_true', help='Get all employees')
    parser.add_argument('-s', '--slack', action='store_true', help='Send to Slack')
    args = parser.parse_args()

    # Set up logging level using environment variable
    logger.configure(handlers=[{'sink': sys.stdout, 'level': os.getenv('LOG_LEVEL', 'INFO')}])

    logger.info('Starting FindMyShift Shift Reporter...')

    # Get API keys and team ID from environment variable
    logger.info('Setting up environment variables...')
    api_key = os.getenv('API_KEY')
    team_id = os.getenv('TEAM_ID')

    # Load settings.json
    logger.info('Loading settings.json...')
    with open('settings.json', 'r', encoding='utf-8') as file:
        settings = json.load(file)

    blacklist = settings.get('blacklist', [])
    logger.debug(f'Blacklist: {blacklist}')
    aliases = settings.get('aliases', {})
    logger.debug(f'Aliases: {aliases}')

    # Export as [json|csv|html|text]
    if not os.path.exists('outputs'):
        os.mkdir('outputs')

    # If --all flag is set, get all employees
    if args.all:
        logger.info('Getting all employees...')
        all_employees = get_employees(api_key, team_id)
        # Convert to {staff_id: XX, display_name: 'XX'} format
        employees = [{ 'staff_id': employee['staffId'], 'display_name': employee['displayName'] } \
            for employee in all_employees]
        employees = filter_employees(employees, blacklist, aliases)
        logger.info('Exporting all employees...')
        save_to_file(f'outputs/all_employees.{args.format}', employees, args.format)
    else:
        # Get list of employees without shifts
        logger.info('Getting list of employees without shifts...')
        employees = get_employees_without_shifts(api_key, team_id, args.days)
        employees = filter_employees(employees, blacklist, aliases)
        logger.info('Exporting employees without shifts...')
        save_to_file(   f'outputs/employees_without_shifts.{args.format}', \
                        employees, args.format)

    if args.slack:
        logger.info('Sending to Slack...')
        slack_token = os.getenv('SLACK_TOKEN')
        slack_channel = os.getenv('SLACK_CHANNEL')
        slack_username = os.getenv('SLACK_USERNAME')
        slack_icon_emoji = os.getenv('SLACK_ICON_EMOJI')
        send_to_slack(  slack_token, slack_channel, employees, \
                        username=slack_username, icon_emoji=slack_icon_emoji)

    logger.success('Done')

if __name__ == '__main__':
    main()
