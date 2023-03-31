import csv
from typing import Dict, List, Optional
from .pbproblem import PBProblem, PBMultiProblem, PBResult
from . import pbfunc


class PBParser:
    def __init__(self, file_path: str):
        """
        Instantiates a PBParser object, but does not parse the file. A
        PBProblem instance can be extracted through the problem() method.

        :param file_path: The path to the .pb file.
        """
        self._file_path: str = file_path
        self._meta: Dict[str, str] = {}
        self._projects: Dict[str, Dict[str, str]] = {}
        self._voters: Dict[str, Dict[str, str]] = {}
        self._predefined: Optional[PBResult] = PBResult([], 0, 0.0, -1, -1)

    def _parse(self) -> None:
        """
        Parses a .pb file into meta, projects and voter dictionaries storing
        all the instance data.

        Reference: http://pabulib.org/code
        """
        with open(self._file_path, 'r', newline='', encoding='utf-8') as csv_file:
            section: str = ''
            header: List[str] = []
            reader: csv.reader = csv.reader(csv_file, delimiter=';')
            for row in reader:
                if row[0].strip().lower() in ('meta', 'projects', 'votes'):
                    section = row[0].strip().lower()
                    header = next(reader)
                # Metadata
                elif section == 'meta':
                    self._meta[row[0]] = row[1].strip()
                # Projects
                elif section == 'projects':
                    self._projects[row[0]] = {}
                    for it, key in enumerate(header[1:]):
                        self._projects[row[0]][key.strip()] = row[it + 1].strip()
                # Voters
                elif section == 'votes':
                    self._voters[row[0]] = {}
                    for it, key in enumerate(header[1:]):
                        self._voters[row[0]][key.strip()] = row[it + 1].strip()

    def problem(self) -> PBProblem:
        """
        Parses a .pb file and returns the instance as a PBProblem object for solving.
        The votes are represented as utility values in the returned problem, where
        utilities[v][p] is the utility voter v derives from project p.

        Reference: http://pabulib.org/code

        :return: A PBProblem object containing the PB instance for solving.
        """
        if not self._meta:
            self._parse()

        # Problem Metadata
        num_projects: int = len(self._projects)
        num_voters: int = len(self._voters)
        budget: int = int(self._meta['budget'])
        vote_type: str = self._meta['vote_type']

        # Project Data
        projects: List[int] = [int(pid) for pid in self._projects.keys()]
        costs: List[int] = [int(self._projects[pid]['cost']) for pid in self._projects.keys()]

        # Reverse Project Lookup (pid -> projects[idx])
        project_lookup: Dict[int, int] = {pid: idx for idx, pid in enumerate(projects)}

        # Voter Data
        voters: List[int] = [int(vid) for vid in self._voters.keys()]
        # voters_lookup: Dict[int, int] = {vid: idx for idx, vid in enumerate(voters)}

        # The utility values are derived from the votes, which may
        # be approval, cumulative, scoring or ordinal voting:
        utilities: List[List[int]] = [
            pbfunc.votes_to_utility(
                vote_type,
                project_lookup,
                [int(vote) for vote in self._voters[vid]['vote'].split(',')],
                [int(point) for point in self._voters[vid]['points'].split(',')]
                if 'points' in self._voters[vid] else []
            )
            for vid in self._voters.keys()
        ]

        # Predefined Greedy Allocation:
        values: List[int] = pbfunc.aggregate_utilitarian(num_projects, utilities)
        predefined: List[int] = [
            int(pid) for pid in self._projects
            if 'selected' in self._projects[pid] and
               self._projects[pid]['selected'] == '1'
        ]
        predefined_value: int = sum(values[project_lookup[pid]] for pid in predefined)
        self._predefined = PBResult(predefined, predefined_value, 0.0, -1, -1)

        return PBProblem(
            num_projects=num_projects,
            num_voters=num_voters,
            budget=budget,
            costs=costs,
            utilities=utilities,
            projects=projects,
            voters=voters
        )

    def predefined(self) -> PBResult:
        return self._predefined


class PBWriter:
    def __init__(self, file_path: str):
        self._file_path: str = file_path

    def write(self, problem: PBProblem):
        # Prepare Meta
        meta_header: List[str] = ['key', 'value']
        num_projects: List[str] = ['num_projects', str(problem.num_projects)]
        num_voters: List[str] = ['num_votes', str(problem.num_voters)]
        budget: List[str] = ['budget', str(problem.budget)]
        vote_type: List[str] = ['vote_type', 'scoring']

        # Prepare Projects
        projects_header: List[str] = ['project_id', 'cost']
        projects: List[List[str]] = []
        for idx, pid in enumerate(problem.projects):
            project: List[str] = [str(pid), str(problem.costs[idx])]
            projects.append(project)

        # Prepare Voters
        voters_header: List[str] = ['voter_id', 'vote', 'points']
        voters: List[List[str]] = []
        for idx, vid in enumerate(problem.voters):
            votes: List[str] = [str(problem.projects[p_idx]) for p_idx, vote in enumerate(problem.utilities[idx]) if vote > 0]
            points: List[str] = [str(vote) for vote in problem.utilities[idx] if vote > 0]
            voter: List[str] = [str(vid), ','.join(votes), ','.join(points)]
            voters.append(voter)

        with open(self._file_path, 'w+', encoding='utf-8') as csv_file:
            writer: csv.writer = csv.writer(csv_file, delimiter=';')

            # Write Metadata
            writer.writerow(['META'])
            writer.writerow(meta_header)
            writer.writerow(num_projects)
            writer.writerow(num_voters)
            writer.writerow(budget)
            writer.writerow(vote_type)

            # Write Projects
            writer.writerow(['PROJECTS'])
            writer.writerow(projects_header)
            for row in projects:
                writer.writerow(row)

            # Write Voters
            writer.writerow(['VOTES'])
            writer.writerow(voters_header)
            for row in voters:
                writer.writerow(row)
