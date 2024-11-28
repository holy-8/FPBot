import sqlite3

import cfg


class Database:
    """
    Database manager class.\n
    Creates a file with name cfg.DB_FILE in the same directory.\n
    Default table name is "global", with rows INTEGER "discord_id", REAL "femboy_points".\n
    # Methods
    fetch_points(id, /) -- returns femboy_points of a user\n
    update_user(id, pts, /) -- adds femboy_points to a user\n
    leaderboard(p, p_size, /) -- returns a leaderboard sorted by femboy_points
    """
    def __init__(self, /) -> None:
        self.con = sqlite3.connect(cfg.DB_FILE)
        self.cur = self.con.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS global (discord_id INTEGER, femboy_points REAL)"
        )
        self.con.commit()

    def count_users(self, /) -> int:
        """
        Returns a total amount of users in the database.
        """
        r = self.cur.execute(
            "SELECT discord_id FROM global",
        )
        count = 0
        while _ := r.fetchone():
            count += 1
        return count

    def fetch_points(self, id: int, /) -> int:
        """
        Returns amount of femboy points a user with specified id has.\n
        If user doesn't exist, creates a user with 0 points and returns 0.
        """
        r = self.cur.execute(
            "SELECT femboy_points FROM global WHERE discord_id=?", (id,)
        )
        points = r.fetchone()
        if not points:
            self.con.execute(
                "INSERT INTO global VALUES(?, ?)", (id, 0,)
            )
            self.con.commit()
            return 0
        return points[0]

    def update_user(self, id: int, pts: float, /) -> None:
        """
        Adds a provided amount of femboy_points (pts) to the user with an id.\n
        If such user doesn't exist, creates a user with 0 points and adds the pts.
        """
        user_pts = self.fetch_points(id)
        self.cur.execute(
            "UPDATE global SET femboy_points=? WHERE discord_id=?", (user_pts + pts, id,)
        )
        self.con.commit()

    def leaderboard(self, p: int, p_size: int, /) -> list[tuple[int, float]]:
        """
        Returns a list users, sorted by femboy_points in descending order.\n
        Each user is a tuple of (discord_id, femboy_points).\n
        Parameters are p - page, and p_size - amount of users on each page.\n
        Raises ValueError is p (page) is less than 1.
        """
        if p < 1:
            raise ValueError("Page (p) must be greater than 0")
        r = self.cur.execute(
            "SELECT discord_id, femboy_points FROM global ORDER BY femboy_points DESC"
        )
        page = r.fetchmany(p_size)
        for _ in range(p - 1):
            page = r.fetchmany(p_size)
        return page
