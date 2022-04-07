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
    _url_tag = param.String()
    _headers = param.Dict(dict(Accept="application/vnd.github.v3+json"))

    @property
    def url_tag(self):
        """Compose the url to be requested."""
        return f"{self.url}/{self._url_tag}"

    @property
    def headers(self):
        """Generate the headers of the petition."""
        return self._headers

    def _alert(self, status_code):
        """Return an error warning when the requested url is not valid."""
        if status_code >= 400:
            raise ValueError(
                f"Organization {self._org_name} is not valid. Please, insert a valid organization name."
            )

    def _get_requests(self):
        """Return a request response given the url_tag and headers instance properties."""
        org = requests.get(
            f"{self.url_tag}",
            headers=self.headers,
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
        self._url_tag = f"orgs/{self._org_name}"
        # Request
        org = self._get_requests()
        # Check
        self._alert(org.status_code)
        # Get dictionary
        resp = org.json()
        # Get public repositories
        pub_repos = resp["public_repos"]
        return print(f"Number public repositories: {pub_repos}")

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
        self._url_tag = f"orgs/{self._org_name}/repos"
        self._headers["Type"] = "all"
        # Request
        org = self._get_requests()
        # Check
        self._alert(org.status_code)
        # Get dictionary
        resp = org.json()
        # Get max size
        max_size = index = -100
        for ix, repo in enumerate(resp):
            max_size = max(repo["size"], max_size)
            if max_size == repo["size"]:
                index = ix
        repo_name = resp[index]["name"]
        return print(
            f"Size biggest repository: {max_size * 1024} bytes\nName repository: {repo_name}"
        )

    def request_number_organization(self):
        """Return the number of organizations that are currently on GitHub."""
        # Parameters
        self._url_tag = f"search/users?q=type:org"
        # Request
        org = self._get_requests()
        # Get dictionary
        resp = org.json()
        total = resp["total_count"]
        return print(f"Number organizations on Github: {total}")
