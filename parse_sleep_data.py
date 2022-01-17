import os
import json

def load_secrets():
    with open('secrets.json') as f:
        secrets = json.load(f)
    
    return secrets

def load_sleep_data(data_dir):
    # get all the JSON files so they can be combined
    # each file contains a month of data
    json_files = os.listdir(data_dir)
    json_files = [f for f in json_files if f.endswith('.json')]
    json_files.sort()

    # each file contains a list of objects, combine all lists to bring all the data together
    data = []

    for json_file in json_files:
        with open(f'{data_dir}{json_file}') as f:
            data += json.load(f)

    return data

def write_sleep_data_to_csv(data):
    # save sleep data to csv, will write this to database in the future
    with open('data/nightly_sleep_data.csv', 'w') as outfile:
        # write the file header
        outfile.write('logId,dateOfSleep,startTime,endTime,duration,minutesToFallAsleep,minutesAsleep,minutesAwake,minutesAfterWakeup,timeInBed,efficiency,minutesDeepSleep,minutesLightSleep,minutesRemSleep\n')
        
        for d in data:
            # there is also classic type, but this doesn't have as much info and only happens on some nights, so just ignore this
            if d['type'] == 'stages':
                record = f"{d['logId']},{d['dateOfSleep']},{d['startTime']},{d['endTime']},{d['duration']},{d['minutesToFallAsleep']},{d['minutesAsleep']},{d['minutesAwake']},{d['minutesAfterWakeup']},{d['timeInBed']},{d['efficiency']},{d['levels']['summary']['deep']['minutes']},{d['levels']['summary']['light']['minutes']},{d['levels']['summary']['rem']['minutes']}"
                outfile.write(f'{record}\n')
        
        outfile.close()

def main():
    secrets = load_secrets()

    # baseDir should be "MyFitbitData/<name>/"
    sleep_data_dir = secrets['baseDir'] + 'Sleep/'
    sleep_data = load_sleep_data(sleep_data_dir)
    
    write_sleep_data_to_csv(sleep_data)

if __name__ == '__main__': main()
