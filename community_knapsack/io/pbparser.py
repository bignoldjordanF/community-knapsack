from community_knapsack import PBSingleProblem, \
    PBMultiProblem
from typing import List, Dict
from .. import pbutils

import os
import csv
import warnings


class PBParserError(Exception):
    """An exception raised when an error is encountered parsing a .pb file."""
    pass


class PBParser:
    """Parses .pb files containing participatory budgeting instances into PBProblem or
    PBMultiProblem instances for solving. The .pb files should be in the format described
    by Stolicki et. al. (http://pabulib.org/format)."""

    def __init__(self, file_path: str):
        """
        Instantiates a parser object and parses the .pb file argument into a PBMultiProblem or
        PBProblem object for solving. Please note that the .pb file should be in the format
        described by Stolicki et. al. (http://pabulib.org/format), or otherwise errors will
        occur during parsing.

        :param file_path: The file path to the .pb file.
        """
        self.file_path: str = file_path
        self._problem: PBMultiProblem = self.parse()

    def parse(self) -> PBMultiProblem:
        """
        This function is automatically called by the constructor and parses a .pb file into
        a PBMultiProblem instance for solving. You should only call this function if you
        wish to 'reparse' (re-read) the file. Otherwise, use the problem() or multi_problem()
        methods to retrieve the PBProblem or PBMultiProblem objects for solving.

        Reference Code: http://pabulib.org/code

        :return: A PBMultiProblem object containing the relevant data from the .pb file.
        """

        # Verify that the file exists:
        if not os.path.isfile(self.file_path):
            raise PBParserError(f'The path {self.file_path} does not contain a .pb file.')

        # The data is first parsed into dictionaries:
        _metadata: Dict[str, str] = {
            'budget': [],
            'vote_type': ''
        }
        _projects: Dict[str, Dict[str, str]] = {}
        _voters: Dict[str, Dict[str, str]] = {}

        # Parse the .pb file:
        with open(self.file_path, 'r', newline='', encoding='utf-8') as csv_file:
            # The current section and header is stored at all times:
            current_section: str = ''
            current_header: List[str] = []

            # Read the csv .pb file:
            csv_reader: csv.reader = csv.reader(csv_file, delimiter=';')
            for csv_row in csv_reader:
                row_name: str = csv_row[0].strip().lower()

                # Determine the current header and section:
                if row_name in ('meta', 'projects', 'votes'):
                    current_section = row_name
                    current_header = next(csv_reader)

                # Parse Metadata
                elif current_section == 'meta':
                    if row_name in _metadata:
                        _metadata[row_name] = csv_row[1].lower().strip()

                # Parse Projects
                elif current_section == 'projects':
                    _projects[row_name] = {'cost': '', 'selected': ''}
                    for column_idx, column_name in enumerate(current_header[1:]):
                        column_name = column_name.lower().strip()
                        if column_name in _projects[row_name]:
                            _projects[row_name][column_name] = \
                                csv_row[column_idx + 1].lower().strip()

                # Parse Voters
                elif current_section == 'votes':
                    _voters[row_name] = {'vote': '', 'points': ''}
                    for column_idx, column_name in enumerate(current_header[1:]):
                        column_name = column_name.lower().strip()
                        if column_name in _voters[row_name]:
                            _voters[row_name][column_name] = \
                                csv_row[column_idx + 1].lower().strip()

        # Obtain the budget(s) and ensure validity:
        budget: List[int] = []
        for str_budget in _metadata['budget'].split(','):
            if not str_budget.isdigit():
                raise PBParserError(f'A non-numeric or non-positive budget `{str_budget}` was found in the .pb file.')
            budget.append(int(str_budget))

        if not budget:
            raise PBParserError('There were zero budgets found in the .pb file.')

        # Obtain the vote type and ensure validity:
        vote_type: str = _metadata['vote_type']
        if vote_type not in ('approval', 'cumulative', 'scoring', 'ordinal'):
            raise PBParserError(f'The vote_type `{vote_type}` must be approval, cumulative, scoring or ordinal.')

        # Obtain the projects and ensure validity:
        projects: List[str] = []
        project_lookup: Dict[str, int] = {}

        costs: List[List[int]] = [[] for _ in range(len(budget))]
        selected: List[int] = []  # predefined allocation

        project_idx: int = 0
        for pid, data in _projects.items():
            # Add the project to the list:
            projects.append(pid)
            project_lookup[pid] = project_idx

            # Add the costs as long as they are positive integers:
            project_cost: List[int] = []
            for cost in data['cost'].split(','):
                if not cost.isdigit() or int(cost) <= 0:
                    raise PBParserError(f'The cost `{cost}` for project `{pid}` is not a positive integer.')
                project_cost.append(int(cost))

            # There must be exactly the same number of costs as budgets:
            if len(project_cost) != len(budget):
                raise PBParserError(f'There were a different number of costs than budgets for project `{pid}`.')

            # Add the cost to the cost list if valid:
            for dimension in range(len(costs)):
                costs[dimension].append(project_cost[dimension])

            # Add the selected value if exists and valid:
            if data['selected'] not in ('', '0', '1'):
                warnings.warn(f'An invalid `selected` `{data["selected"]}` value has been ignored for project {pid}.')

            if data['selected'] == '1':
                # N.B. The project index is added rather than the id such that
                # a value can be computed and a result returned:
                selected.append(project_idx)

            project_idx += 1

        # Obtain the voters and ensure validity:
        voters: List[str] = []
        utilities: List[List[int]] = []

        for vid, data in _voters.items():
            # Add the voter to the list:
            voters.append(vid)

            vote_split: List[str] = data['vote'].split(',')
            point_split: List[str] = data['points'].split(',')

            # Ensure that there are no duplicate votes:
            if len(set(vote_split)) != len(vote_split):
                raise PBParserError(f'Voter {vid} has voted for the same project more than once.')

            # Ensure len(points) == len(votes) in cumulative and scoring voting:
            if vote_type in ('cumulative', 'scoring') and len(point_split) != len(vote_split):
                raise PBParserError(f'Voter {vid} has `{len(point_split)}` points for '
                                    f'`{len(vote_split)}` project votes. They should be equal.')

            # Add the votes as long as the projects exist and points are valid:
            _votes: List[int] = []
            _points: List[int] = []
            for idx, vote in enumerate(vote_split):
                if not vote.isdigit() or vote not in project_lookup:
                    raise PBParserError(f'The project `{vote}` by voter {vid} does not exist in the file.')
                _votes.append(project_lookup[vote])

                if vote_type in ('cumulative', 'scoring'):
                    if not point_split[idx].isdigit():
                        raise PBParserError(f'The points value `{point_split[idx]}` for project {vote}'
                                            f' is not a positive integer.')
                    _points.append(int(point_split[idx]))

            # Convert them to utility values and append to list:
            utilities.append(pbutils.vote_to_utility(len(projects), vote_type, _votes, _points))

        print(budget)
        return PBMultiProblem(
            num_projects=len(projects),
            num_voters=len(voters),
            budget=budget,
            costs=costs,
            utilities=utilities,
            projects=projects,
            voters=voters,
        )

    def problem(self) -> PBSingleProblem:
        """
        Retrieves a single budget (typical) PBProblem object obtained from parsing the .pb file. This
        will always work for any valid .pb file, but note that it will remove any budgets after the first
        one found, and so will not produce valid solutions for multidimensional (multi-budget) instances.
        It is recommended to use multi_problem() if you are unsure, or you definitely have multiple budgets.

        :return: A PBProblem object containing the relevant data from the .pb file for solving.
        """
        multi_problem: PBMultiProblem = self.multi_problem()
        return PBSingleProblem(
            num_projects=multi_problem.num_projects,
            num_voters=multi_problem.num_voters,
            budget=multi_problem.budget[0],
            costs=multi_problem.costs[0],
            utilities=multi_problem.utilities,
            projects=multi_problem.projects,
            voters=multi_problem.voters
        )

    def multi_problem(self) -> PBMultiProblem:
        """
        Retrieves a multi-budget PBMultiProblem object obtained from parsing the .pb file. This will
        always work for any valid .pb file, but note that solving the problem exactly will be slower
        because the algorithms facilitate multiple budgets. It is recommended that problem() is used
        for typical problems who have definitely a single budget. You should use this function if
        you definitely have multiple budgets or are unsure.
        :return: A PBMultiProblem object containing the relevant data from the .pb file for solving.
        """
        return self._problem
