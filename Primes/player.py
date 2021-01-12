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
        self.raw_df = pd.DataFrame(
            columns=[
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
            ]
        )

        # scrape html soup for data

        # build a player df - normalized stats
        self.norm_df = pd.DataFrame()

        # for each season, calculate M_VALUE

        # calculate prime

        # create a player directory
        self.directory = self.create_player_directory()

        # create a 3x3 plot of their stats

        # save CSV

    # ----- HTML SOUP helper functions and SETUP ---- #
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

    # get table data rows
    def get_rows(self, table_type):
        if table_type == "regular season traditional":
            table = self.soup.find("table", {"id": "per_game"})  # "Per Game" table --> Regular Season
        elif table_type == "regular season advanced":
            table = self.soup.find("table", {"id": "advanced"})  # find "Advanced" table
        else:
            print("\nCannot find table: {}".format(table_type))
            sys.exit(1)

        if table is None:
            sys.exit(1)

        table_body = table.find("tbody")
        rows = table_body.find_all("tr")
        rows = list(rows)
        return rows

    # reads a particular stat value from html data
    @staticmethod
    def read_stat_from_table(row, feature):
        try:
            x = float(row.find("td", {"data-stat": feature}).text.strip())
            return x
        except AttributeError as e:
            if "attribute 'text'" in str(e):
                return float(0.0)

    # ----- STATS ----- #
    # get regular season and playoff stats
    def get_stats(self):
        # regular season
        self.get_regular_season_stats()

        # playoffs

    # ----- REGULAR SEASON STATS ----- #
    # get regular season stats
    def get_regular_season_stats(self):
        # get regular season traditional stats
        # traditional stats: Season, Age, Team, Points, Rebounds, Assists, FT%, eFG%
        self.get_regular_season_traditional_stats()

        # get regular season advanced stats
        # advanced stats: PER, TS%
        self.get_regular_season_advanced_stats()

    # get regular season - traditional - stats
    def get_regular_season_traditional_stats(self):
        rows = self.get_rows(table_type="regular season traditional")

        for i in range(len(rows)):
            try:
                row = rows[i]

                # Season
                season = row.find("th", {"data-stat": "season"})
                season = season.a  # get URL
                season = season.text.strip()
                self.raw_df.loc[i, "Season"] = season

                # Age
                age = row.find("td", {"data-stat": "age"}).text.strip()  # int, not float
                self.raw_df.loc[i, "Age"] = age

                # Team
                team = row.find("td", {"data-stat": "team_id"}).text.strip()  # str, not float
                self.raw_df.loc[i, "Team"] = team

                # Points
                points = self.read_stat_from_table(row, "pts_per_g")
                self.raw_df.loc[i, "Points"] = points

                # Rebounds
                rebounds = self.read_stat_from_table(row, "trb_per_g")
                self.raw_df.loc[i, "Rebounds"] = rebounds

                # Assists

            except AttributeError as ae:
                if "attribute 'a'" in str(ae):  # 'Season' is not a hyperlink
                    continue

    # get regular season - advanced - stats
    def get_regular_season_advanced_stats(self):
        print()
