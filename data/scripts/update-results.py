#!/usr/bin/env python

import csv
import simplejson as json

from candidate_map import candidate_map

C_PRECINCT = 2
C_OFFICE_ID = 3
C_OFFICE = 4
C_CANDIDATE_ID = 6
C_CANDIDATE = 7
C_PARTY_ID = 10
C_PRECINCTS_REPORTING = 11
C_PRECINCTS_TOTAL = 12
C_VOTES = 13
C_VOTES_PERCENTAGE = 14
C_VOTES_TOTAL = 15

results = {
    'total': {
        'candidates': {},
        'total_votes_first': 0,
        'total_votes_second': 0,
        'total_votes_third': 0
    },
    'precincts': {}
}

for i in candidate_map:
    c = candidate_map[i]
    c['first_choice'] = 0
    c['second_choice'] = 0
    c['third_choice'] = 0

with open('../workspace/localPrct.txt', 'r') as f:
    c = csv.reader(f, delimiter=';')
    for row in c:
        if row[C_OFFICE] == 'Mayor First Choice (Minneapolis)' \
                or row[C_OFFICE] == 'Mayor Second Choice (Minneapolis)' \
                or row[C_OFFICE] == 'Mayor Third Choice (Minneapolis)':

            candidate_id = row[C_CANDIDATE_ID]
            candidate_info = candidate_map[candidate_id]
            candidate_info['candidate_id'] = candidate_id

            try:
                precinct = results['precincts'][row[C_PRECINCT]]
            except KeyError:
                results['precincts'][row[C_PRECINCT]] = {
                    'candidates': {}
                }
                precinct = results['precincts'][row[C_PRECINCT]]

            candidates = precinct['candidates']
            candidates[candidate_id] = candidate_info
            candidate = candidates[candidate_id]

            total = results['total']
            try:
                totalCandidate = total['candidates'][candidate_id]
            except KeyError:
                total['candidates'][candidate_id] = candidate_info
                totalCandidate = total['candidates'][candidate_id]


            votes = int(row[C_VOTES])
            votes_total = int(row[C_VOTES_TOTAL])
            if row[C_OFFICE] == 'Mayor First Choice (Minneapolis)':
                candidate['first_choice'] = votes
                totalCandidate['first_choice'] += votes
                precinct['total_votes_first'] = votes_total
                total['total_votes_first'] += votes
            elif row[C_OFFICE] == 'Mayor Second Choice (Minneapolis)':
                candidate['second_choice'] = votes
                totalCandidate['second_choice'] += votes
                precinct['total_votes_second'] =  votes_total
                total['total_votes_second'] += votes
            elif row[C_OFFICE] == 'Mayor Third Choice (Minneapolis)':
                candidate['third_choice'] = votes
                totalCandidate['third_choice'] += votes
                precinct['total_votes_third'] =  votes_total
                total['total_votes_third'] += votes

print json.dumps(results, indent=4 * ' ')

