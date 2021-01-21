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

        # create a player directory
        self.directory = self.create_player_directory()

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
                assists = self.read_stat_from_table(row, "ast_per_g")
                self.raw_df.loc[i, "Assists"] = assists

                # FT%
                ft = self.read_stat_from_table(row, "ft_pct")
                self.raw_df.loc[i, "FT%"] = ft

                # eFG%
                efg = self.read_stat_from_table(row, "efg_pct")
                self.raw_df.loc[i, "eFG%"] = efg

            except AttributeError as ae:
                if "attribute 'a'" in str(ae):  # 'Season' is not a hyperlink
                    continue

    # get regular season - advanced - stats
    def get_regular_season_advanced_stats(self):
        rows = self.get_rows(table_type="regular season advanced")

        for i in range(len(rows)):
            try:
                row = rows[i]

                # PER
                per = self.read_stat_from_table(row, "per")
                self.raw_df.loc[i, "PER"] = per

                # TS%
                ts = self.read_stat_from_table(row, "ts_pct")
                self.raw_df.loc[i, "TS%"] = ts

            except AttributeError as ae:
                continue

    # ----- M_VALUE ----- #
    # normalize stats df
    @staticmethod
    def normalize(df):
        normalized_df = df.copy()

        for c in df.columns:
            # does not make sense to normalize: Season, Age, Team
            if c == "Season" or c == "Age" or c == "Team":
                normalized_df[c] = df[c]

            else:
                min_value = df[c].min()  # min
                max_value = df[c].max()  # max

                numerator = df[c] - min_value
                denominator = max_value - min_value

                # check if denomator is 0
                if denominator == 0.0:
                    normalized_df[c] = df[c]

                else:
                    normalized_value = numerator / denominator
                    normalized_df[c] = normalized_value
                    #normalized_df[c] = normalized_df[c].apply(lambda x: round(x, 4))

        return normalized_df

    # calculate M_VALUE for each season
    def calculate_m_value(self):
        # normalize stats first
        norm_df = self.normalize(self.raw_df)

        # weights
        w_pts = 0.1  # points
        w_reb = 0.1  # rebounds
        w_ast = 0.1  # assists
        w_ftp = 0.1  # FT%
        w_efg = 0.1  # eFG%
        w_per = 0.1  # PER
        w_tsp = 0.1  # TS%

        # calculate M_VALUE for each season
        for index, row in norm_df.iterrows():
            m_value = np.sum([
                w_pts * row["Points"],
                w_reb * row["Rebounds"],
                w_ast * row["Assists"],
                w_ftp * row["FT%"],
                w_efg * row["eFG%"],
                w_per * row["PER"],
                w_tsp * row["TS%"]
            ])

            m_value = np.round(m_value, decimals=4)
            self.raw_df.loc[index, "M_VALUE"] = m_value

    # ----- PRIME ----- #
    def find_prime(self, window_size):
        print()

    # ----- PLOTS ----- #
    def plot_stats(self):
        # use seaborn package for plots
        print()
