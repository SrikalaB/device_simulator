import argparse
import sys
import simulator

parser = argparse.ArgumentParser()

parser.add_argument('-p', '--profile', required=True, help="Simulator Profile you want to run.[ Enter: LoadProfile or PvProfile]")

args = parser.parse_args()

if args.profile not in ["PvProfile", "LoadProfile"]:
    print("Entered profile is not available. Enter \"LoadProfile\" or \"PvProfile\"")
    sys.exit(1)

print("If you wish to stop simulation at any point - Press ctrl+C\n")
print(f'Starting {args.profile} simulation for device with identifier meter123. '
      'Reading will start at current time UTC and will be published at 1 min intervals')


simulator.start([{"device_identifier": "meter123", "profile": args.profile, "freq": 2}])

