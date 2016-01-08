#!/usr/bin/python2.7
"""
A script to merge a table of addresses with a table of polling places. Sample info from the Voting Information Project.
"""

import argparse
import csv
import os

PRECINCT_STATE_TO_ID_MAP = {
        'ARI': '004',
        'CAL': '006',
        'CON': '009',
        'FLO': '012',
        'GEO': '013',
        'ILL': '017',
        'MAS': '025',
        'MAI': '023',
        'MIN': '027',
        'NEWJ': '034',
        'NEWY': '036',
        'PEN': '042',
        'VIR': '051',
        'WIS': '055'
        }

def merge(args):
    precincts_file = open(args.precincts_filename)
    addresses_file = open(args.addresses_filename)

    if not os.path.exists('data/'):
        os.makedirs('data/')

    if args.output_filename:
        output_file = open('data/%s' % args.output_filename, 'w')
    else:
        output_file = open('data/out.txt', 'w')

    # Load precincts in memory
    (precinct_header, precinct_map) = _load_precincts(precincts_file)
    #print precinct_map

    # Go through addresses line by line and write out merged line
    #addresses_file.readline() # skip header
    addresses = csv.reader(addresses_file)
    raw_address_header = addresses.next()
    raw_address_header = map(lambda title: 'Add %s' % title, raw_address_header) # Prefix address headers with 'Add '
    address_header = ','.join(raw_address_header)
    output_file.write('%s,%s\n' % (address_header, precinct_header))
    for address in addresses:
        precinct_id = address[5].strip()
        try:
            output_line = '%s,%s\n' % (','.join(address).strip(), precinct_map[precinct_id])
            output_file.write(output_line)
        except KeyError:
            print 'WARNING: no precinct found for id %s' % precinct_id
            print 'SKIPPING: %s\n' % ','.join(address).strip()
    

    precincts_file.close()
    addresses_file.close()
    output_file.close()

def _load_precincts(precincts_fo):
    """
    Build a precinct map keying off of precinct id normalized into ###-### format.
    """
    precinct_map = {}
    precinct_header = precincts_fo.readline().strip() # Skip header
    for precinct_line in precincts_fo:
        precinct_parts = precinct_line.split(',')
        length = len(precinct_parts)
        if length < 5:
            print 'WARNING: malformed precinct line, excpection 5 lines  got : %s' % length
            print 'SKIPPING: %s\n' % precinct_line.strip()
            continue
        precinct_id = precinct_parts[len(precinct_parts)-1].strip() # Bad input, *assume* state/precinct id is last last column 
        precinct_id_parts = precinct_id.split('-')
        state_abrv = precinct_id_parts[0] 
        precinct_id = precinct_id.split('-')[len(precinct_id_parts) - 1] # Bad input, *assume* precinct id is last
        new_id = '%s-%s' % (PRECINCT_STATE_TO_ID_MAP[state_abrv], precinct_id)
        precinct_map[new_id] = precinct_line.strip()
    return (precinct_header, precinct_map)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Merge addresses with precincts. Output written to data/OUTPUTFILE. Overwrites previous output.')
    parser.add_argument('precincts_filename', metavar='PRECINCTS_FILENAME', type=str, help='filename for precinct data')
    parser.add_argument('addresses_filename', metavar='ADDRESSES_FILENAME', type=str, help='filename for address data')
    parser.add_argument('-o', '--output_filename', metavar='OUTPUT_FILENAME', type=str, help='filename for output data, defaults to out.txt')
    args = parser.parse_args()
    merge(args)
