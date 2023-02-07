#!/usr/bin/env python
""" Python library for FindMyShift API to get the list of
    people who have not filled out their schedules"""

import logging
import datetime
import requests
from loguru import logger

BASE_URL = 'https://findmyshift.com/api/v1.4'

# Set default logger to NullHandler to prevent logging unless explicitly set
logger.configure(handlers=[{'sink': logging.NullHandler()}])

class Employee(dict):
    """Employee class"""

    def __init__(self, staff_id: str, display_name: str):
        self.staff_id = staff_id
        self.display_name = display_name
        dict.__init__(self, staff_id=staff_id, display_name=display_name)

    def __repr__(self):
        return f'Employee(staff_id={self.staff_id}, display_name={self.display_name})'

    def __str__(self):
        return f'{self.display_name} ({self.staff_id})'

    def __eq__(self, other):
        return self.staff_id == other.staff_id

    def __hash__(self):
        return hash(self.staff_id)


def get_employees(api_key: str, team_id: str) -> dict:
    """Use FindMyShift API to get the list of staff
    Args:
        api_key (str): API key
        team_id (str): Team ID
    Returns:
        dict: List of staff
    """

    # Make GET request to the FindMyShift API to get the list of staff
    response = requests.get(f'{BASE_URL}/staff/list', params={'apiKey': api_key, 'teamId': team_id})

    # Check if the request was successful
    if response.status_code == 200:
        employees = response.json()
        return employees

    # Raise an exception if the request was not successful
    raise Exception(response.text)


def get_shifts(api_key: str, team_id: str, days: int = 7, **kwargs) -> dict:
    """Use FindMyShift API to get the list of shifts
    Args:
        api_key (str): API key
        team_id (str, optional): Team ID
        from_date (str, optional): Start date
        to_date (str, optional): End date
        days (int, optional): Number of days to fetch. Defaults to 7.
    Returns:
        dict: List of shifts
    """

    # Get the start and end date from kwargs
    if not kwargs.get('from_date') and not kwargs.get('to_date'):
        today = datetime.date.today()
        from_date = today.strftime('%Y-%m-%d')
        to_date = (today + datetime.timedelta(days=days)).strftime('%Y-%m-%d')
        logger.debug(f'Defaulting to {from_date} to {to_date}')

    params = {
        'apiKey': api_key,
        'teamId': team_id,
        'from': from_date,
        'to': to_date,
        'publishedShifts': 'no' # Include unpublished shifts
    }

    # Make GET request to the FindMyShift API to get the list of shifts
    response = requests.get(f'{BASE_URL}/reports/shifts', params=params)

    # Check if the request was successful
    if response.status_code == 200:
        shifts = response.json()
        return shifts

    # Raise an exception if the request was not successful
    raise Exception(response.text)


def filter_employees(employees: list, shifts: list) -> list:
    """Filter the list of employees who have not filled out their schedules
    Args:
        employees (list): List of employees
        shifts (list): List of shifts
    Returns:
        list: List of employees who have not filled out their schedules
    """

    # Loop through the list of shifts and add the staff to the list of
    # employees who have not filled out their schedules
    employees_without_shifts = set()
    for employee in employees:
        # Check if the employee has a shift
        if employee['staffId'] not in shifts:
            # Add the employee to the list of employees who have not filled out their schedules
            employees_without_shifts.add(Employee(employee['staffId'], employee['displayName']))

    return list(employees_without_shifts)


def get_employees_without_shifts(api_key: str, team_id: str, days: int = 7) -> list:
    """Use FindMyShift API to get the list of employees who have not filled out their schedules
    Args:
        api_key (str): API key
        team_id (str): Team ID
        days (int, optional): Number of days to fetch. Defaults to 7.
    Returns:
        list: List of employees who have not filled out their schedules
    """

    # Get the list of employees who have not filled out their schedules
    logger.debug('Getting the list of employees...')
    employees = get_employees(api_key, team_id)

    # Get the list of shifts
    logger.debug('Getting the list of shifts...')
    shifts = get_shifts(api_key=api_key, team_id=team_id, days=days)

    # Filter employees who have not filled out their schedules
    logger.debug('Filtering employees who have not filled out their schedules...')
    employees_without_shifts = filter_employees(employees, shifts)

    return employees_without_shifts


if __name__ == '__main__':
    print('This is a library. Please import it and use it in your code.')
