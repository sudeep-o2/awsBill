"""import boto3
import pandas as pd

def get_cost_values_for_services(services):
    # Initialize the Boto3 client for Cost Explorer
    client = boto3.client('ce', region_name='ap-south-1')  # Change the region_name as per your AWS region

    # Set the time period for which you want to retrieve cost data
    start_date = '2024-03-01'
    end_date = '2024-04-02'

    # Define the request parameters
    request_params = {
        'TimePeriod': {
            'Start': start_date,
            'End': end_date
        },
        'Granularity': 'DAILY',
        'Metrics': ['UnblendedCost']
    }

    # Retrieve the cost data for each service
    cost_data = {}
    for service in services:
        # Define the filter for the service
        service_filter = {
            "Dimensions": {
                "Key": "SERVICE",
                "Values": [service]
            }
        }
        # Update the filter in the request parameters
        request_params['Filter'] = service_filter

        # Retrieve the cost data
        response = client.get_cost_and_usage(**request_params)

        # Extract the cost data
        service_cost_data = []
        for result in response['ResultsByTime']:
            total_cost = result['Total']['UnblendedCost']['Amount']
            start_date = result['TimePeriod']['Start']
            end_date = result['TimePeriod']['End']
            service_cost_data.append({'Start Date': start_date, 'End Date': end_date, 'Total Cost': total_cost})

        # Store the cost data for the service
        cost_data[service] = service_cost_data

    return cost_data

def save_costs_to_excel(cost_data, excel_file):
    # Create a DataFrame from the cost data
    df = pd.DataFrame()
    for service, service_cost_data in cost_data.items():
        service_df = pd.DataFrame(service_cost_data)
        service_df['Service'] = service
        df = pd.concat([df, service_df], ignore_index=True)

    # Save the DataFrame to an Excel file
    df.to_excel(excel_file, index=False)
    print(f"Cost data saved to {excel_file}")

if __name__ == "__main__":
    # Define the services for which you want to retrieve costs
    services = ['Amazon Elastic Compute Cloud - Compute', 'Amazon Relational Database Service']
    # Fetch cost data for each service
    cost_data = get_cost_values_for_services(services)
    # Save cost data to Excel file
    save_costs_to_excel(cost_data, 'cost_data_for_services.xlsx')
"""

import boto3
import pandas as pd
from datetime import datetime, timedelta
import os

def get_cost_values_for_services(services, start_date, end_date):
    # Initialize the Boto3 client for Cost Explorer
    client = boto3.client('ce', region_name='ap-south-1')  

    # Define the request parameters
    request_params = {
        'TimePeriod': {
            'Start': start_date,
            'End': end_date
        },
        'Granularity': 'DAILY',
        'Metrics': ['UnblendedCost']
    }

    # Retrieve the cost data for each service
    cost_data = {}
    for service in services:
        # Define the filter for the service
        service_filter = {
            "Dimensions": {
                "Key": "SERVICE",
                "Values": [service]
            }
        }
        # Update the filter in the request parameters
        request_params['Filter'] = service_filter

        # Retrieve the cost data
        response = client.get_cost_and_usage(**request_params)

        # Extract the cost data
        service_cost_data = []
        for result in response['ResultsByTime']:
            total_cost = result['Total']['UnblendedCost']['Amount']
            start_date = result['TimePeriod']['Start']
            service_cost_data.append({'Date': start_date, 'Total Cost': total_cost})

        # Store the cost data for the service
        cost_data[service] = service_cost_data

    print(cost_data)
    return cost_data

def update_excel_with_costs(cost_data, excel_file):
    # Check if Excel file exists, if not create a new one
    if not os.path.isfile(excel_file):
        df = pd.DataFrame()
    else:
        # Read existing Excel file
        df = pd.read_excel(excel_file)

    # Update the DataFrame with new cost data
    for service, service_cost_data in cost_data.items():
        for data in service_cost_data:
            date = data['Date']
            total_cost = data['Total Cost']
            # If service column already exists, update it, else create a new one
            if service in df.columns:
                df.loc[0, service] = total_cost
            else:
                df[service] = ""
                df.loc[0, service] = total_cost

    # Save the DataFrame to the Excel file
    df.to_excel(excel_file, index=False)
    print(f"Cost data updated and saved to {excel_file}")


if __name__ == "__main__":
    # Define the services for which you want to retrieve costs
    services = ['Amazon Elastic Compute Cloud - Compute', 'Amazon Relational Database Service']
    # Set the time period for which you want to retrieve cost data
    #end_date = datetime.now().strftime('%Y-%m-%d')  # Today's date

    current_date = datetime.now()
    first_day_of_month = current_date.replace(day=1)
    start_date = first_day_of_month.strftime('%Y-%m-%d')

    end_date = datetime.now().strftime('%Y-%m-%d')

    # Fetch cost data for the specified services and time period
    cost_data = get_cost_values_for_services(services, start_date, end_date)
    # Define the path to the Excel file
    excel_file = "D:/downloads/aws1.xlsx"
    # Update Excel file with the new cost data
    update_excel_with_costs(cost_data, excel_file)




