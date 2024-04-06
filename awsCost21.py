"""import boto3
import pandas as pd
from datetime import datetime
import os

def get_all_services():
    # Initialize the Boto3 client for Cost Explorer
    client = boto3.client('ce', region_name='ap-south-1')  # Change the region_name as per your AWS region

    # Get all available services
    response = client.get_dimension_values(
        Dimension='SERVICE',
        TimePeriod={
            'Start': datetime.now().strftime('%Y-%m-01'),
            'End': datetime.now().strftime('%Y-%m-%d')
        }
    )

    # Extract the list of service names
    services = [service['Value'] for service in response['DimensionValues']]

    return services

def get_current_day_cost_for_services(services):
    # Initialize the Boto3 client for Cost Explorer
    client = boto3.client('ce', region_name='ap-south-1')  # Change the region_name as per your AWS region

    # Get current date
    
    current_date = datetime.now().strftime('%Y-%m-%d')

    # Define the request parameters
    request_params = {
        'TimePeriod': {
            'Start': datetime.now().strftime('%Y-%m-01'),
            'End': datetime.now().strftime('%Y-%m-%d')
        },
        'Granularity': 'MONTHLY',
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
        total_cost = response['ResultsByTime'][0]['Total']['UnblendedCost']['Amount']

        # Store the cost data for the service
        cost_data[service] = total_cost

    return cost_data

def update_excel_with_costs(cost_data, excel_file):
    # Check if Excel file exists, if not create a new one
    if not os.path.isfile(excel_file):
        df = pd.DataFrame()
    else:
        # Read existing Excel file
        df = pd.read_excel(excel_file)

    # Update the DataFrame with new cost data
    for service, total_cost in cost_data.items():
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
    # Fetch all available services
    services = get_all_services()
    # Fetch current day's cost for each service
    cost_data = get_current_day_cost_for_services(services)
    # Define the path to the Excel file
    excel_file = "D:/downloads/aws1.xlsx"
    # Update Excel file with the current day's cost data
    update_excel_with_costs(cost_data, excel_file)"""

import boto3
import pandas as pd
from datetime import datetime
import os

def get_all_services():
    # Initialize the Boto3 client for Cost Explorer
    client = boto3.client('ce', region_name='ap-south-1')  # Change the region_name as per your AWS region

    print(client)

    # Get all available services
    response = client.get_dimension_values(
        Dimension='SERVICE',
        TimePeriod={
            'Start': datetime.now().strftime('%Y-%m-01'),
            'End': datetime.now().strftime('%Y-%m-%d')
        }
    )

    print(response)

    # Extract the list of service names
    services = [service['Value'] for service in response['DimensionValues']]

    print(services)

    return services

def get_current_day_cost_for_services(services):
    # Initialize the Boto3 client for Cost Explorer
    client = boto3.client('ce', region_name='ap-south-1')  # Change the region_name as per your AWS region

    # Get current date
    current_date = datetime.now().strftime('%Y-%m-%d')

    # Define the request parameters
    request_params = {
        'TimePeriod': {
            'Start': datetime.now().strftime('%Y-%m-01'),
            'End': datetime.now().strftime('%Y-%m-%d')
        },
        'Granularity': 'MONTHLY',
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

        print(response)

        # Extract the cost data
        total_cost = response['ResultsByTime'][0]['Total']['UnblendedCost']['Amount']

        # Store the cost data for the service
        cost_data[service] = total_cost

    print(cost_data)

    return cost_data

def update_excel_with_costs(cost_data, excel_file):
    # Get current date
    current_date = datetime.now().strftime('%Y-%m-%d')

    # Check if Excel file exists
    if os.path.isfile(excel_file):
        # Read existing Excel file
        df = pd.read_excel(excel_file)
    else:
        # Create a new DataFrame if the Excel file doesn't exist
        df = pd.DataFrame(columns=['Service', current_date])

    # Iterate over cost data and update or append rows
    for service, total_cost in cost_data.items():
        if service in df['Service'].values:
            # Update the existing row with the new cost data
            df.loc[df['Service'] == service, current_date] = total_cost
        else:
            # Create a new row for the service
            new_row = {'Service': service, current_date: total_cost}
            # Append the new row to the DataFrame
            df = df._append(new_row, ignore_index=True)

    # Save the DataFrame to the Excel file
    df.to_excel(excel_file, index=False)
    print(f"Cost data updated and saved to {excel_file}")



if __name__ == "__main__":
    # Fetch all available services
    services = get_all_services()
    # Fetch current day's cost for each service
    cost_data = get_current_day_cost_for_services(services)
    # Define the path to the Excel file
    excel_file ="D:/downloads/aws2.xlsx"
    # Update Excel file with the current day's cost data
    update_excel_with_costs(cost_data, excel_file)
