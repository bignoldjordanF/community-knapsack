from community_knapsack import PBSingleProblem, PBMultiProblem
from typing import List, Union
import csv


class PBWriter:
    """Writes .pb files containing participatory budgeting instances from PBSingleProblem
    or PBMultiProblem instances. The .pb files are in the format described by Stolicki et.
    al. (http://pabulib.org/format)."""

    def __init__(self, file_path: str):
        """
        Instantiates a writer object by taking the file path to which the .pb file should
        be written. This constructor does not do anything, and the write() method should be
        called to write problems to the file.

        :param file_path: The file path to the .pb file.
        """
        self.file_path: str = file_path

    def _write(self, problem: PBMultiProblem):
        """

        :param problem:
        :return:
        """
        # Prepare Meta
        meta_header: List[str] = ['key', 'value']
        budget: List[str] = ['budget', ','.join([str(b) for b in problem.budget])]

        # Assume scoring in all cases to simplify process:
        vote_type: List[str] = ['vote_type', 'scoring']

        # Prepare Projects
        projects_header: List[str] = ['project_id', 'cost']
        projects: List[List[str]] = []

        # The costs are comma-separated strings of costs in
        # each dimension in a multi-problem:
        for idx, pid in enumerate(problem.projects):
            project: List[str] = [str(pid), ','.join([str(dim[idx]) for dim in problem.costs])]
            projects.append(project)

        # Prepare Voters
        voters_header: List[str] = ['voter_id', 'vote', 'points']
        voters: List[List[str]] = []

        for idx, vid in enumerate(problem.voters):
            votes: List[str] = [
                str(problem.projects[p_idx])
                for p_idx, vote in enumerate(problem.utilities[idx])
                if vote > 0
            ]
            points: List[str] = [
                str(point) for point in problem.utilities[idx] if point > 0
            ]
            voter: List[str] = [str(vid), ','.join(votes), ','.join(points)]
            voters.append(voter)

        # Write .pb File:
        with open(self.file_path, 'w+', encoding='utf-8') as csv_file:
            writer: csv.writer = csv.writer(csv_file, delimiter=';')

            # Write Metadata
            writer.writerow(['META'])
            writer.writerow(meta_header)
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

    def write(self, problem: Union[PBSingleProblem, PBMultiProblem]):
        """

        :param problem:
        :return:
        """
        if isinstance(problem, PBSingleProblem):
            return self._write(PBMultiProblem(
                num_projects=problem.num_projects,
                num_voters=problem.num_voters,
                budget=[problem.budget],
                costs=[problem.costs],
                utilities=problem.utilities,
                projects=problem.projects,
                voters=problem.voters
            ))
        return self._write(problem)
