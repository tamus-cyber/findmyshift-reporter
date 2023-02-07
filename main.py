#!/usr/bin/env python3
"""Main program for FindMyShift Shift Reporter"""

import os
import sys
import json
import csv
import argparse
from loguru import logger
from dotenv import load_dotenv
from fms_lib import get_employees_without_shifts
load_dotenv()


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
    args = parser.parse_args()

    # Set up logging level using environment variable
    logger.configure(handlers=[{'sink': sys.stdout, 'level': os.getenv('LOG_LEVEL', 'INFO')}])

    logger.info('Starting FindMyShift Shift Reporter...')

    # Get API key and team ID from environment variable
    logger.info('Setting up environment variables...')
    api_key = os.getenv('API_KEY')
    team_id = os.getenv('TEAM_ID')

    # Get list of employees without shifts
    logger.info('Getting list of employees without shifts...')
    employees_without_shifts = get_employees_without_shifts(api_key, team_id, args.days)

    # Export as employees_without_shifts.[json|csv|html|text]
    logger.info('Exporting employees without shifts...')
    if not os.path.exists('outputs'):
        os.mkdir('outputs')
    save_to_file(   f'outputs/employees_without_shifts.{args.format}', \
                    employees_without_shifts, args.format)

    logger.success('Done')

if __name__ == '__main__':
    main()
