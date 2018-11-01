#!/usr/bin/env python
#-*- coding: utf-8 -*-
""" OSM Lineup """

# Standard library imports
from csv import reader
from operator import itemgetter
from sys import argv

# Debug
# from pdb import set_trace as st

LINEUP_LIST = [ '4-4-2', '4-3-3', '3-5-2', '3-4-3', '5-3-2', '3-3-4' ]

def get_players():
    players = {}
    with open(argv[1], 'r') as csvfile:
        playersreader = reader(csvfile, delimiter=',', quotechar='|')
        next(playersreader)
        for player in playersreader:
            players.update( {player[0]: {
                "Position": player[1],
                "Atk": player[2],
                "Def": player[3],
                "Nationality": player[4],
                "Play": player[5] == 'True',
                }})
    return players

def increment_dict(dictionnary, key):
    if key in dictionnary:
        dictionnary[key] += 1
    else:
        dictionnary[key] = 0
    return dictionnary

class LineUp(object):
    def __init__(self, players):
        self.players = players
        self.rate_players()

    def rate_players(self):
        for player_name in self.players:
            if self.players[player_name]['Position'] == 'D':
                self.players[player_name]['Rate'] = int(self.players[player_name]['Def'])
            elif self.players[player_name]['Position'] == 'A':
                self.players[player_name]['Rate'] = int(self.players[player_name]['Atk'])
            else:
                self.players[player_name]['Rate'] = (
                    int(self.players[player_name]['Def']) + int(self.players[player_name]['Atk'])
                    ) / 2

    def get_top(self, n):
        sorted_players = {}
        players_copy = self.players.copy()
        nb_players = min(len(self.players), n)
        for i in range(nb_players):
            best_player_name = ''
            best_player_rate = 0
            for player_name in players_copy:
                if players_copy[player_name]['Rate'] > best_player_rate and players_copy[player_name]['Play']:
                    best_player_name = player_name
                    best_player_rate = players_copy[player_name]['Rate']
            best_player = { best_player_name: players_copy.pop(best_player_name)}
            sorted_players.update(best_player)
        return sorted_players

    def get_2nd_top(self, n):
        sorted_players = {}
        players_copy = self.players.copy()
        nb_players = min(len(self.players), n+1)
        for i in range(nb_players):
            best_player_name = ''
            best_player_rate = 0
            for player_name in players_copy:
                if players_copy[player_name]['Rate'] > best_player_rate and players_copy[player_name]['Play']:
                    best_player_name = player_name
                    best_player_rate = players_copy[player_name]['Rate']
            best_player = { best_player_name: players_copy.pop(best_player_name)}
            if i != n-1:
                sorted_players.update(best_player)
        return sorted_players

    def get_best_lineup(self, second=False):
        if second:
            top_players = self.get_2nd_top(10)
        else:
            top_players = self.get_top(10)
        nb_defenders = 0
        nb_midfielders = 0
        nb_attackers = 0
        rate_sum = float(0)
        nationality_dict = dict()
        for player_name in top_players:
            if top_players[player_name]['Position'] == 'D':
                nb_defenders+=1
            elif top_players[player_name]['Position'] == 'M':
                nb_midfielders+=1
            else:
                nb_attackers+=1
        print '-----------'
        print 'LINEUP : %s-%s-%s' % (nb_defenders, nb_midfielders, nb_attackers)
        print '-----------'
        print 'Defenders :'
        for player_name in top_players:
            if top_players[player_name]['Position'] == 'D':
                print('%s (D:%s)' % (player_name, top_players[player_name]['Rate']))
                rate_sum += top_players[player_name]['Rate']
                increment_dict(nationality_dict, top_players[player_name]['Nationality'])
        print '-----------'
        print 'Midfielders :'
        for player_name in top_players:
            if top_players[player_name]['Position'] == 'M':
                print('%s (A:%s, D:%s, %s)' % (player_name, top_players[player_name]['Atk'], top_players[player_name]['Def'], top_players[player_name]['Rate']))
                rate_sum += top_players[player_name]['Rate']
                increment_dict(nationality_dict, top_players[player_name]['Nationality'])
        print '-----------'
        print 'Attackers :'
        for player_name in top_players:
            if top_players[player_name]['Position'] == 'A':
                print('%s (A:%s)' % (player_name, top_players[player_name]['Rate']))
                rate_sum += top_players[player_name]['Rate']
                increment_dict(nationality_dict, top_players[player_name]['Nationality'])
        print '-----------'
        max_country = max(nationality_dict.iteritems(), key=itemgetter(1))[0]
        print 'OVERALL RATE = %s [%s]' % (rate_sum/10, nationality_dict[max_country])
        return [nb_defenders, nb_midfielders, nb_attackers]

    def get_squad(self, lineup, verbose=True):
        [nb_defenders, nb_midfielders, nb_attackers] = lineup.split('-')
        players_copy = self.players.copy()
        rate_sum = float(0)
        nationality_dict = dict()

        if verbose:
        	print '-----------'
        	print 'LINEUP : %s' % lineup
        	print '-----------'
        	print 'Defenders :'

        nb_players_left = int(nb_defenders)
        while nb_players_left > 0:
            best_player_name = ''
            best_player_rate = -1
            best_player_nationality = ''
            for player_name in self.players:
                if self.players[player_name]['Position'] == 'D' and player_name in players_copy:
                    if self.players[player_name]['Rate'] > best_player_rate and self.players[player_name]['Play']:
                        best_player_name = player_name
                        best_player_rate = self.players[player_name]['Rate']
                        best_player_nationality = self.players[player_name]['Nationality']
            try:
                players_copy.pop(best_player_name)
            except KeyError:
                return False
            if verbose:
            	print('%s (D:%s)' % (best_player_name, best_player_rate))
            nb_players_left -= 1
            rate_sum += best_player_rate
            increment_dict(nationality_dict, best_player_nationality)

        if verbose:
        	print '-----------'
        	print 'Midfielders :'

        nb_players_left = int(nb_midfielders)
        while nb_players_left > 0:
            best_player_name = ''
            best_player_rate = -1
            best_player_nationality = ''
            for player_name in self.players:
                if self.players[player_name]['Position'] == 'M' and player_name in players_copy:
                    if self.players[player_name]['Rate'] > best_player_rate and self.players[player_name]['Play']:
                        best_player_name = player_name
                        best_player_rate = self.players[player_name]['Rate']
                        best_player_nationality = self.players[player_name]['Nationality']
            try:
                players_copy.pop(best_player_name)
            except KeyError:
                return False
            if verbose:
                print('%s (A:%s, D:%s, %s)' % (best_player_name, self.players[best_player_name]['Atk'], self.players[best_player_name]['Def'], best_player_rate))
            nb_players_left -= 1
            rate_sum += best_player_rate
            increment_dict(nationality_dict, best_player_nationality)
                
        if verbose:
            print '-----------'
            print 'Attackers :'

        nb_players_left = int(nb_attackers)
        while nb_players_left > 0:
            best_player_name = ''
            best_player_rate = -1
            best_player_nationality = ''
            for player_name in self.players:
                if self.players[player_name]['Position'] == 'A' and player_name in players_copy:
                    if self.players[player_name]['Rate'] > best_player_rate and self.players[player_name]['Play']:
                        best_player_name = player_name
                        best_player_rate = self.players[player_name]['Rate']
                        best_player_nationality = self.players[player_name]['Nationality']
            try:
                players_copy.pop(best_player_name)
            except KeyError:
                return False
            if verbose:
                print('%s (A:%s)' % (best_player_name, best_player_rate))
            nb_players_left -= 1
            rate_sum += best_player_rate
            increment_dict(nationality_dict, best_player_nationality)

        max_country = max(nationality_dict.iteritems(), key=itemgetter(1))[0]
        if verbose:
            print '-----------'
            print 'OVERALL RATE = %s [%s]' % (rate_sum/10, nationality_dict[max_country])
        return rate_sum/10, nationality_dict[max_country]

if __name__ == '__main__':
    OSM = LineUp(get_players())
    OSM.get_best_lineup()
    # OSM.get_best_lineup(second=True)
    try:
        OSM.get_squad(argv[2])
    except:
        print('You could define a Lineup as a 2nd arg')
    for lineup in LINEUP_LIST:
        print('%s : %s' % (lineup, OSM.get_squad(lineup, verbose=False)))
