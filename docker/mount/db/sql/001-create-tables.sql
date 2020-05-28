---- drop ----
DROP TABLE IF EXISTS `IdeaInfo`;
DROP TABLE IF EXISTS `UserInfo`;
DROP TABLE IF EXISTS `Session`;
DROP TABLE IF EXISTS `LikeList`;

---- create ----
CREATE TABLE IF not exists IdeaInfo(
	title text, 
	idea_url text, 
	user_id text, 
	describe_data text, 
	tag text, 
	uuid text, 
	primary key(idea_url(256))
) DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

CREATE TABLE IF not exists UserInfo(
	user_id text, 
	role text, 
	primary key(user_id(256))
) DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

CREATE TABLE IF not exists Session(
	session text, 
	email text, 
	user_name text, 
	last_time datetime, 
	primary key(session(256))
) DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

CREATE TABLE IF not exists LikeList(
	user_id text, 
	uuid text, 
	reg_time datetime
) DEFAULT CHARSET=utf8 COLLATE=utf8_bin;



