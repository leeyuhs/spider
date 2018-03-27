#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: lee

"""Train tickets query via CLI

Usage:
    tickets [-dgktz] <from> <to> <date>

Options:
    -h,--help         显示帮助菜单
    -g                高铁
    -t                特快
    -d                动车
    -k
    -z                直达快速

"""

import json
import requests
from docopt import docopt
import re
import stations
from prettytable import PrettyTable
from colorama import Fore


def cli():
    arguments = docopt(__doc__, version='Tickets 1.0')
    from_station = stations.get_telecode(arguments.get('<from>'))
    to_station = stations.get_telecode(arguments.get('<to>'))
    date = arguments.get('<date>')
    options = ''.join([key for key, value in arguments.items() if value is True])
    url = ('https://kyfw.12306.cn/otn/leftTicket'
           '/queryO?leftTicketDTO.train_date={}&'
           'leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&'
           'purpose_codes=ADULT').format(date, from_station, to_station)
   # print(url)
    r = requests.get(url)
    raw_trains = r.json()['data']['result']
    pt = PrettyTable()
    pt._set_field_names('车次 车站 时间 历时 一等 二等 软卧 硬卧 硬座 无座'.split())
    # print(trains)
    for raw_train in raw_trains:
        data_list = raw_train.split('|')
        train_no = data_list[3]
        initial = train_no[0].lower()
        if not options or initial in options:
            from_station_code = data_list[6]
            to_station_code = data_list[7]
            from_station_name = ''
            to_station_name = ''
            start_time = data_list[8]
            arrive_time = data_list[9]
            time_duration = data_list[10]
            first_class_seat = data_list[31] or '--'
            second_class_seat = data_list[30] or '--'
            soft_sleep = data_list[23] or '--'
            hard_sleep = data_list[28] or '--'
            hard_seat = data_list[29] or '--'
            no_seat = data_list[33] or '--'
            pt.add_row([
                train_no,
                '\n'.join([Fore.GREEN + stations.get_name(from_station_code) + Fore.RESET, Fore.RED + stations.get_name(to_station_code) + Fore.RESET]),
                '\n'.join([Fore.GREEN + start_time + Fore.RESET, Fore.RED + arrive_time + Fore.RESET]),
                time_duration,
                first_class_seat,
                second_class_seat,
                soft_sleep,
                hard_sleep,
                hard_seat,
                no_seat
            ])
    print(pt)

if __name__ == '__main__':
    cli()
