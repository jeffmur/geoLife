# Joshua Sterner
# 11/25/2020

# Usage: Place this script into data directory next to the "Data" directory
# run $ python3 split_by_month.py 

from pathlib import Path

def split_trajectory(trajectory):
    rows = []
    month = None
    with trajectory.open() as t:
        [t.readline() for i in range(6)]
        for line in t:
            # year, month, day
            date = line.split(',')[5].split('-')
            next_month = (int(date[0]), int(date[1]))
            if month == None:
                month = next_month
            if month != next_month:
                yield month, rows
                month = next_month
                rows = []
            rows.append(line.strip())
        yield month, rows

def split_by_month(trajectories):
    data = {}
    trajectories = list(trajectories)
    trajectories.sort()
    for trajectory in trajectories:
        for month, rows in split_trajectory(trajectory):
            if month not in data:
                data[month] = rows
            else:
                data[month] = data[month] + rows
    return data

def main():
    output_dir = Path('user_by_month')
    output_dir.mkdir()
    for user_dir in Path('Data').glob('*'):
        user_id = user_dir.name
        user_output_dir = output_dir / Path(user_id)
        user_output_dir.mkdir()
        data = split_by_month((user_dir / Path('Trajectory')).glob('*'))
        for year, month in data.keys():
            rows = data[year, month]
            output_file = user_output_dir / Path(f'{year}_{month:02}.csv')
            with output_file.open(mode='w') as f:
                f.write('\n'.join(rows)+'\n')
            
if __name__ == '__main__':
    main()
