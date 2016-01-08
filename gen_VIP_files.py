#!/usr/bin/python2.7

from abc import ABCMeta, abstractmethod
import argparse
import sys
import csv
import os

class UninitializedException(Exception): 
    pass

class BadArgumentException(Exception):
    pass

class VIPFile(object):
    """
    Base class for a specific VIPFile. A row of data from addresses/polling locations is passed into the write method must implement in subclass.
    """
    __metaclass__=ABCMeta
    def __init__(self):
        self.header = None
        self.output_filename = None
        self.output = None

    def open(self):
        if self.header == None or self.output_filename == None:
            raise UninitializedException('Must set header and name for VIP file')

        if not os.path.exists('data/'):
            os.makedirs('data/')

        self.output = open('data/%s' % self.output_filename, 'w') 
        self.output.write('%s\n' % self.header)

    def close(self):
        self.output.close()

    @abstractmethod
    def write(self, data_object):
        pass

class PrecinctVIPFile(VIPFile):
    """
    Precinct VIP file look at: https://github.com/votinginfoproject/csv-templates/blob/master/data_templates/db_templates/precinct.txt
    """
    def __init__(self):
        super(VIPFile, self)
        self.header = "name,number,locality_id,ward,mail_only,ballot_style_image_url,id"
        self.output_filename = "precinct.txt"
        self.number = 100000

    def write(self, data_object):
        name = '%s %s' % (data_object[2], data_object[3])# Not sure, using "City State"
        number = self.number # Not sure, just use ascending number with prefix
        self.number += 1
        locality_id = '' # Don't have it
        ward = '' # Don't have it
        mail_only = 'NO' # Always NO
        ballot_style_image_url = '' # Don't have it
        precinct_id = data_object[5] 
        self.output.write('%s,%s,%s,%s,%s,%s,%s\n' % (name, number, locality_id, ward, mail_only, ballot_style_image_url, precinct_id))

class PollingLocationVIPFile(VIPFile):
    """
    Polling Location VIP file look at: https://github.com/votinginfoproject/csv-templates/blob/master/data_templates/db_templates/polling_location.txt
    """
    def __init__(self):
        super(VIPFile, self)
        self.header = "address_location_name,address_line1,address_line2,address_line3,address_city,address_state,address_zip,directions,polling_hours,photo_url,id"
        self.output_filename = "polling_location.txt"

    def write(self, data_object):
        address_location_name = '' # Not sure keep blank
        address_line1 = data_object[6] 
        address_line2 = '' # Not sure keep blank
        address_line3 = '' # Not sure keep blank
        address_city = data_object[7] 
        address_state = data_object[8].split(' ')[0]
        address_zip = data_object[8].split(' ')[1]
        directions = '' # Not sure keep blank
        polling_hours = '' # Not sure keep blank
        photo_url = '' # Not sure keep blank
        polling_location_id = data_object[len(data_object)-1]
        self.output.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n' % (address_location_name, address_line1, address_line2, address_line3, address_city, 
                                                                  address_state, address_zip, directions, polling_hours, photo_url, polling_location_id))


class PrecinctPollingLocationVIPFile(VIPFile):
    """
    Precinct Polling Location VIP file look at: https://github.com/votinginfoproject/csv-templates/blob/master/data_templates/db_templates/precinct_polling_location.txt
    """
    def __init__(self):
        super(VIPFile, self)
        self.header = "precinct_id,polling_location_id"
        self.output_filename = "precinct_polling_location.txt"

    def write(self, data_object):
        precinct_id = data_object[5] 
        polling_location_id = data_object[len(data_object)-1]
        self.output.write('%s,%s\n' % (precinct_id, polling_location_id))


def generate_files(args):
    if not any([args.all, args.precinct, args.polling_location, args.precinct_polling_location]):
        raise BadArgumentException('Error: please specify --all or a specific file to generate.')

    # Setup VIP files we are generating this run
    vip_files = []
    a = PrecinctVIPFile()
    if args.all:
        vip_files.append(PrecinctVIPFile())
        vip_files.append(PollingLocationVIPFile())
        vip_files.append(PrecinctPollingLocationVIPFile())
    else:
        if args.precinct:
            vip_files.append(PrecinctVIPFile())
        if args.polling_location:
            vip_files.append(PollingLocationVIPFile())
        if args.precinct_polling_location:
            vip_files.append(PrecinctPollingLocationVIPFile())

    map(lambda vip: vip.open(), vip_files)

    with open(args.input_filename) as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        csvreader.next() # Skip header
        for row in csvreader:
            map(lambda vip: vip.write(row), vip_files)

    map(lambda vip: vip.close(), vip_files)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate VIP csv files. Will overwrite previous data. Output written to data/VIP_FILE')
    parser.add_argument('input_filename', metavar='INPUT_FILENAME', type=str, help='filename for precinct input data, the result of running merge.py')
    parser.add_argument('--all', action='store_true', help='generate precinct.txt, polling_location.txt, precinct_polling_location.txt')
    parser.add_argument('-p', '--precinct', action='store_true', help='generate precinct.txt')
    parser.add_argument('-pl', '--polling_location', action='store_true', help='filename for address data')
    parser.add_argument('-ppl', '--precinct_polling_location', action='store_true', help='filename for output data, defaults to out.txt')
    args = parser.parse_args()
    generate_files(args)
