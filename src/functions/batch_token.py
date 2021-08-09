def get_batch_token(conn, db_tables):
	from sqlalchemy import select

	session_data = db_tables["session_data"]

	sql_query = select([session_data]).where(session_data.c.name == "batch_token")

	return conn.execute(sql_query).fetchone()[1]


def record_batch_token(batch_token, conn, db_tables):
	from sqlalchemy import select

	session_data = db_tables["session_data"]

	sql_query = session_data.update().values(value=f"{batch_token}").where(session_data.c.name == "batch_token")
	conn.execute(sql_query)
