import csv
from typing import Dict, List, Optional, Union
from .pbproblem import PBProblem, PBResult
from . import pbfunc


class PBParser:
    def __init__(self, file_path: str):
        self._file_path: str = file_path
        self._problem: Optional[PBProblem] = None
        self._predefined: PBResult = PBResult(0, 0, 0.0, -1, -1)

    def problem(self) -> PBProblem:
        if self._problem:
            return self._problem

        num_projects: int = 0
        num_voters: int = 0
        budget: int = 0
        vote_type: str = ''

        project_lookup: Dict[int, int] = {}
        projects: List[int] = []

        voter_lookup: Dict[int, int] = {}
        voters: List[int] = []

        costs: List[int] = []
        utilities: List[List[int]] = []

        predefined: List[int] = []

        with open(self._file_path, 'r', newline='', encoding='utf-8') as csv_file:
            section: str = ''
            header: List[str] = []

            cur_project_idx: int = 0
            cur_voter_idx: int = 0

            reader: csv.reader = csv.reader(csv_file, delimiter=';')
            for row in reader:
                if str(row[0]).strip().lower() in ('meta', 'projects', 'votes'):
                    section = str(row[0]).strip().lower()
                    header = next(reader)
                elif section == 'meta':
                    if row[0].strip().lower() == 'budget':
                        budget = int(row[1].strip())
                    elif row[0].strip().lower() == 'num_projects':
                        num_projects = int(row[1].strip())
                    elif row[0].strip().lower() == 'num_voters':
                        num_voters = int(row[1].strip())
                    elif row[0].strip().lower() == 'vote_type':
                        vote_type = row[1].strip()
                elif section == 'projects':
                    project_id: int = int(row[0])
                    project_lookup[project_id] = cur_project_idx
                    projects.append(project_id)
                    for it, key in enumerate(header[1:]):
                        if key.strip() == 'cost':
                            costs.append(int(row[it + 1].strip()))
                        elif key.strip() == 'selected':
                            if row[it + 1].strip() == '1':
                                predefined.append(project_id)
                    cur_project_idx += 1
                elif section == 'votes':
                    voter_id: int = int(row[0])
                    voter_lookup[voter_id] = cur_voter_idx
                    voters.append(voter_id)

                    votes: List[int] = []
                    points: List[int] = []

                    for it, key in enumerate(header[1:]):
                        if key.strip() == 'vote':
                            votes = [int(pid) for pid in row[it+1].strip().split(',')]
                        elif key.strip() == 'points':
                            points = [int(p) for p in row[it+1].strip().split(',')]

                    utilities.append(pbfunc.votes_to_utility(vote_type, project_lookup, votes, points))
                    cur_voter_idx += 1

        values: List[int] = pbfunc.aggregate_utilitarian(
            num_projects=num_projects,
            utilities=utilities
        )
        predefined_value: int = sum(values[project_lookup[pid]] for pid in predefined)

        self._predefined: PBResult = PBResult(
            allocation=predefined,
            value=predefined_value,
            runtime=0.0,
            algorithm=-1,
            approximate=-1
        )

        self._problem = PBProblem(
            num_projects=num_projects,
            num_voters=num_voters,
            budget=budget,
            costs=costs,
            utilities=utilities,
            projects=projects,
            voters=voters
        )
        return self._problem

    def predefined(self):
        return self._predefined
