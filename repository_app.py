"""Module to extract GitHub data."""
import param
import requests


class RepositoryApp(param.Parameterized):
    """
    Class to extract, given an organization, the number of repositories, the size
    of the biggest repository, and the total number of organizations in GitHub.
    This class uses Github REST Api v3.

    Instance attributes:
        url: string defining the request link.
    """

    url = param.String("https://api.github.com")
    _org_name = param.String("GitHub")
    _repo_error = param.String("error")

    def _alert(self):
        """Return an error warning when the requested url is not valid."""
        return print(
            f"Organization {self._org_name} is not valid. Please, insert a valid organization name."
        )

    def _get_requests(self, add_string, **kwargs):
        """
        Return the requested url instance.

        This method returns a request response given the url instance attribute
        and the add_string argument.

        Args:
            add_string: completes the url string to be requested.
            kwargs: additional parameters to be introduced inside headers option.
        """
        org = requests.get(
            f"{self.url}" + add_string,
            headers=dict(Accept="application/vnd.github.v3+json", **kwargs),
        )
        return org

    def request_number_repositories(self, org_name):
        """
        Get the number of repositories in an organization.

        Given the name of an organization, this method returns the number of
        repositories the company has.

        Args:
            org_name: Name of the organization.
        """
        # Parameters
        self._org_name = org_name
        add_string = f"/orgs/{self._org_name}"
        # Request
        org = self._get_requests(add_string=add_string)
        # Check
        if org.status_code == 404:
            return self._alert()
        # Get dictionary
        resp = org.json()
        # Get public and private (if any) repositories
        pub_repos = resp["public_repos"]
        try:
            pri_repos = resp["total_private_repos"]
        except KeyError:
            pri_repos = None
        string = (
            f"Number public repositories: {pub_repos}\nNumber private repositories: {pri_repos}\nTotal: {pub_repos + pri_repos}"
            if pri_repos
            else f"Number public repositories: {pub_repos}"
        )
        return print(string)

    def request_biggest_repository(self, org_name):
        """
        Get the size of the biggest repository in an organization.

        Given the name of an organization, this method returns the size (in bytes)
        and name of its biggest repository.

        Args:
            org_name: Name of the organization.
        """
        # Parameters
        self._org_name = org_name
        add_string = f"/orgs/{self._org_name}/repos"
        kwargs = {"Type": "all"}
        # Request
        org = self._get_requests(add_string=add_string, **kwargs)
        # Check
        if org.status_code == 404:
            return self._alert()
        # Get dictionary
        resp = org.json()
        # Get max size
        max_size = index = -100
        for ix, repo in enumerate(resp):
            max_size = max(repo["size"], max_size)
            if max_size == repo["size"]:
                index = ix
        # size = max([repo['size'] for repo in resp])
        mult = 1024
        repo_name = resp[index]["name"]
        return print(
            f"Size biggest repository: {max_size * mult} bytes\nName repository: {repo_name}"
        )

    def request_number_organization(self):
        """Return the number of organizations that are currently on GitHub."""
        # Parameters
        add_string = f"/search/users?q=type:org"
        # Request
        org = self._get_requests(add_string=add_string)
        # Get dictionary
        resp = org.json()
        total = resp["total_count"]
        return print(f"Number organizations on Github: {total}")
