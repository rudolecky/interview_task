import psycopg2

class Db:
    def init(self):
        self.conn = psycopg2.connect(
            host="db",
            database="postgres",
            user="postgres",
            password="password")
        self.cur = self.conn.cursor()
        
    def post_exec(self):
        self.conn.commit()
        self.cur.close()
        self.conn.close()

    def create_db(self):
        self.init()
        
        self.cur.execute("DROP TABLE IF EXISTS flats;")
        self.conn.commit()

        self.cur.execute("""CREATE TABLE flats(
                    flats_id SERIAL PRIMARY KEY,
                    title VARCHAR (50) NOT NULL,
                    image_url VARCHAR (100) NOT NULL);
                    """)
        self.post_exec()

    def insert(self, data: list[dict]):
        self.init()
        for row in data:
            self.cur.execute(f"INSERT INTO flats(title, image_url) VALUES(\'{row['title']}\', \'{row['url']}\');")
            
        self.post_exec()

    def select(self):
        output = []
        self.init()
        self.cur.execute("""SELECT * FROM flats""")
        res = self.cur.fetchall()
        self.post_exec()
        for row in res:
            output.append({"title": row[1], "url": row[2]})
        return output