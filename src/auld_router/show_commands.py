#!/usr/local/bin/python3

import subprocess


def show_route():
    # Run the 'route' command and capture the output
    route_output = subprocess.check_output(['route', '-n', 'show', '-inet', '-gateway']).decode('utf-8')

    # Remove the first three lines
    route_output = '\n'.join(route_output.split('\n')[3:])

    # Find the column numbers for Destination, Gateway, Prio, Iface, and Flags
    header_row = route_output.split('\n')[0]
    columns = header_row.split()

    # Check if the required columns exist
    required_columns = ['Destination', 'Gateway', 'Prio', 'Iface', 'Flags']
    column_indices = [columns.index(col) for col in required_columns if col in columns]

    # Format column headers
    header_line = '{:<15} {:<10} {:<15} {}'.format('Destination', 'Interface', 'Gateway', 'Flags')
    underline_bar = '=' * len(header_line)

    # Filter out the specified columns while retaining spacing and excluding rows with "b" in Flags
    filtered_output = []
    for line in route_output.split('\n')[1:]:
        fields = line.split()

        # Check if all required columns are present in the line
        if len(fields) >= max(column_indices) + 1:
            dest = fields[column_indices[0]]
            gateway = fields[column_indices[1]]
            iface = fields[column_indices[3]]
            flags = fields[column_indices[4]]

            # Exclude rows with "b" in Flags
            if 'b' not in flags:
                formatted_line = '{:<15} {:<10} {:<15} {}'.format(dest, iface, gateway.rjust(15), flags)
                filtered_output.append(formatted_line)

    # Insert column headers and underline bar at the beginning of the output
    filtered_output.insert(0, underline_bar)
    filtered_output.insert(0, header_line)

    # Print the filtered and formatted output
    print('\n'.join(filtered_output))
