import csv
from typing import Dict, List, Optional
from .pbproblem import PBProblem, PBResult
from .pbfunc import aggregate_utilitarian


class PBParser:
    def __init__(self, file_path: str):
        self._file_path: str = file_path
        self._problem: Optional[PBProblem] = None
        self._predefined: Optional[PBResult] = None

    def problem(self) -> PBProblem:
        """
        Reference: http://pabulib.org/code

        :return:
        """
        if self._problem:
            return self._problem

        meta: Dict[str, str] = {}
        projects: Dict[int, Dict[str, str]] = {}
        voters: Dict[int, Dict[str, str]] = {}

        with open(self._file_path, 'r', newline='', encoding='utf-8') as csv_file:
            section: str = ''
            header: List[str] = []
            reader: csv.reader = csv.reader(csv_file, delimiter=';')
            for row in reader:
                if str(row[0]).strip().lower() in ['meta', 'projects', 'votes']:
                    section = str(row[0]).strip().lower()
                    header = next(reader)
                elif section == 'meta':
                    if row[0] in ('num_projects', 'num_votes', 'budget', 'vote_type'):
                        meta[row[0]] = row[1].strip()
                elif section == 'projects':
                    projects[int(row[0])] = {}
                    for it, key in enumerate(header[1:]):
                        if key.strip() in ('cost', 'selected'):
                            projects[int(row[0])][key.strip()] = row[it + 1].strip()
                elif section == 'votes':
                    voters[int(row[0])] = {}
                    for it, key in enumerate(header[1:]):
                        if key.strip() in ('vote', 'points'):
                            voters[int(row[0])][key.strip()] = row[it + 1].strip()

        num_projects: int = int(meta['num_projects'])
        project_list: List[int] = list(projects.keys())
        reverse_projects: Dict[int, int] = {pid: idx for idx, pid in enumerate(project_list)}
        cost_list: List[int] = [int(project['cost']) for project in projects.values()]

        num_voters: int = int(meta['num_votes'])
        voters_list: List[int] = list(voters.keys())
        reverse_voters: Dict[int, int] = {vid: idx for idx, vid in enumerate(voters_list)}
        all_utilities: List[List[int]] = [[0 for _ in range(num_projects)] for _ in range(num_voters)]

        for vid, vote_data in voters.items():
            for pid in vote_data['vote'].split(','):
                pid: int = int(pid)
                all_utilities[reverse_voters[vid]][reverse_projects[pid]] = 1

        self._problem = PBProblem(
            num_projects=num_projects,
            num_voters=num_voters,
            budget=int(meta['budget']),
            projects=project_list,
            costs=cost_list,
            utilities=all_utilities
        )

        values: List[int] = aggregate_utilitarian(num_projects, all_utilities)
        selected_pids: List[int] = [pid for pid, project in projects.items() if project['selected'] == '1']
        total_value: int = sum(values[reverse_projects[pid]] for pid in selected_pids)

        self._predefined = PBResult(selected_pids, total_value, 0, None, True)
        return self._problem

    def predefined_result(self) -> PBResult:
        return self._predefined
