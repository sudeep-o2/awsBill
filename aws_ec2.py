import boto3

def get_ec2_cost_values():
    # Initialize the Boto3 client for Cost Explorer
    client = boto3.client('ce', region_name='ap-south-1')  # Change the region_name as per your AWS region

    # Set the time period for which you want to retrieve cost data
    start_date = '2024-03-01'
    end_date = '2024-04-02'

    # Define the filter for EC2 service
    ec2_filter = {
        "Dimensions": {
            "Key": "SERVICE",
            "Values": ["Amazon Elastic Compute Cloud - Compute"]
        }
    }

    # Define the request parameters
    request_params = {
        'TimePeriod': {
            'Start': start_date,
            'End': end_date
        },
        'Granularity': 'DAILY',
        'Metrics': ['UnblendedCost'],
       
        'Filter': ec2_filter
    }

    # Retrieve the cost data
    response = client.get_cost_and_usage(**request_params)

    print(response)

    # Extract and print the cost data
    for result in response['ResultsByTime']:
        total_cost = result['Total']['UnblendedCost']['Amount']
        print(f"Total cost for EC2 in {result['TimePeriod']['Start']} to {result['TimePeriod']['End']}: {total_cost}")

if __name__ == "__main__":
    get_ec2_cost_values()
