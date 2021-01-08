"""
Michael Patel
January 2021

Project description:
    To detect (and predict) an NBA player's prime seasons

File description:
    To define a Player object

"""
################################################################################
# Imports
from packages import *  # for Python packages and global directories


################################################################################
class Player:
    def __init__(self, url):
        self.url = url

        # html soup
        self.soup = self.get_html_soup(self.url)

        # player name
        self.name = self.get_name()

        # build a player df - raw stats
        self.raw_df = pd.DataFrame(columns=[
            "Season",
            "Age",
            "Team",
            "Points",
            "Rebounds",
            "Assists",
            "FT%",
            "eFG%",
            "PER",
            "TS%",
            "M_VALUE"
        ])

        # scrape html soup for data

        # build a player df - normalized stats
        self.norm_df = pd.DataFrame()

        # for each season, calculate M_VALUE

        # create a player directory
        self.directory = self.create_player_directory()

        # create a 3x3 plot of their stats

        # save CSV

    # get html soup
    @staticmethod
    def get_html_soup(url):
        http = urllib3.PoolManager()
        response = http.request("GET", url)
        page = response.data
        page = re.sub('<!--|-->', "", str(page))
        soup = BeautifulSoup(page, "html.parser")
        return soup

    # get player name
    def get_name(self):
        name = self.soup.title.text.strip()
        name, _ = name.split("Stats")
        name = name.replace("\\", "")
        name = name.strip()
        return name

    # create a player directory
    def create_player_directory(self):
        directory = os.path.join(RESULTS_DIR, self.name)
        if not os.path.exists(directory):
            os.makedirs(directory)

        return directory
