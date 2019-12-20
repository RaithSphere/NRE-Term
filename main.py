import curses

from zeep import Client
from zeep import xsd
from zeep.plugins import HistoryPlugin
import time
from datetime import datetime
import os

LDB_TOKEN = 'NULLTOKEN'
WSDL = 'http://lite.realtime.nationalrail.co.uk/OpenLDBWS/wsdl.aspx?ver=2017-10-01'

if LDB_TOKEN == '':
    raise Exception("Please configure your OpenLDBWS token in getDepartureBoardExample!")

history = HistoryPlugin()

client = Client(wsdl=WSDL, plugins=[history])

header = xsd.Element(
    '{http://thalesgroup.com/RTTI/2013-11-28/Token/types}AccessToken',
    xsd.ComplexType([
        xsd.Element(
            '{http://thalesgroup.com/RTTI/2013-11-28/Token/types}TokenValue',
            xsd.String()),
    ])
)
header_value = header(TokenValue=LDB_TOKEN)


def main(stdscr):
    res = client.service.GetDepartureBoard(numRows=10, crs='NAN', _soapheaders=[header_value])
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)
    stdscr.erase()

    while True:

        height, width = stdscr.getmaxyx()
        stdscr.addstr(1, width - 10, datetime.now().strftime('%H:%M:%S'))
        stdscr.border(0)
        stdscr.hline(height - 4, 1, curses.ACS_BSBS, width - 2)
        stdscr.addstr(height - 3, 2, "[A]", curses.A_BOLD)
        stdscr.addstr(height - 3, 6, "Arrivals")
        stdscr.addstr(height - 3, 15, "[D]", curses.A_BOLD)
        stdscr.addstr(height - 3, 19, "Departures")
        stdscr.addstr(height - 2, 2, "[Q]", curses.A_BOLD)
        stdscr.addstr(height - 2, 6, "Quit")
        stdscr.addstr(height - 2, width - 28, "Version 1.0 By RaithSphere")
        stdscr.addstr(1, 2, "Train info powered by National Rail")
        stdscr.addstr(1, width - 10, datetime.now().strftime('%H:%M:%S'))
        stdscr.hline(2, 1, curses.ACS_BSBS, width - 2)
        stdscr.refresh()

        stdscr.refresh()
        key = stdscr.getch()

        if key == ord('q'):
            break
        elif key == ord('d'):
            res2 = client.service.GetDepartureBoard(numRows=10, crs='NAN', _soapheaders=[header_value])
            stdscr.erase()
            stdscr.border(0)
            stdscr.addstr(3, 2, "Departure's from " + res2.locationName)
            stdscr.addstr(5, width - width + 5, "Time", curses.A_BOLD)
            stdscr.addstr(5, width - width + 15, "Destination", curses.A_BOLD)
            stdscr.addstr(5, width - 25, "Plat", curses.A_BOLD)
            stdscr.addstr(5, width - 15, "Expected", curses.A_BOLD)
            stdscr.hline(6, width - width + 5, curses.ACS_BSBS, 4)
            stdscr.hline(6, width - width + 15, curses.ACS_BSBS, 11)
            stdscr.hline(6, width - 25, curses.ACS_BSBS, 4)
            stdscr.hline(6, width - 15, curses.ACS_BSBS, 8)

            services = res2.trainServices.service

            i = 0
            while i < len(services):
                t = services[i]
                if not t.platform:
                    t.platform = "?"
                stdscr.addstr(7 + i, width - width + 5, t.std)
                stdscr.addstr(7 + i, width - width + 15, t.destination.location[0].locationName,
                              curses.color_pair(2) | curses.A_BOLD)
                stdscr.addstr(7 + i, width - 25, t.platform)
                if t.etd != "On time":
                    stdscr.addstr(7 + i, width - 15, t.etd, curses.A_STANDOUT)
                else:
                    stdscr.addstr(7 + i, width - 15, t.etd)
                i += 1

        elif key == ord('a'):
            res3 = client.service.GetArrivalBoard(numRows=10, crs='NAN', _soapheaders=[header_value])
            stdscr.erase()
            stdscr.border(0)
            stdscr.addstr(3, 2, "Arrivals's at " + res3.locationName)
            stdscr.addstr(5, width - width + 5, "Time", curses.A_BOLD)
            stdscr.addstr(5, width - width + 15, "Origin", curses.A_BOLD)
            stdscr.addstr(5, width - 25, "Plat", curses.A_BOLD)
            stdscr.addstr(5, width - 15, "Expected", curses.A_BOLD)
            stdscr.hline(6, width - width + 5, curses.ACS_BSBS, 4)
            stdscr.hline(6, width - width + 15, curses.ACS_BSBS, 11)
            stdscr.hline(6, width - 25, curses.ACS_BSBS, 4)
            stdscr.hline(6, width - 15, curses.ACS_BSBS, 8)

            services = res3.trainServices.service

            i = 0
            while i < len(services):
                t = services[i]
                if not t.platform:
                    t.platform = "?"
                stdscr.addstr(7 + i, width - width + 5, t.sta)
                stdscr.addstr(7 + i, width - width + 15, t.origin.location[0].locationName,
                              curses.color_pair(2) | curses.A_BOLD)
                stdscr.addstr(7 + i, width - 25, t.platform)
                if t.eta != "On time":
                    stdscr.addstr(7 + i, width - 15, t.eta, curses.A_STANDOUT)
                else:
                    stdscr.addstr(7 + i, width - 15, t.eta)
                i += 1

        stdscr.refresh()


curses.wrapper(main)
