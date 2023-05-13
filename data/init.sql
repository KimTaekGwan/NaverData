CREATE TABLE if not exists `Crawling_Keywords` (
  `search_id` integer PRIMARY KEY,
  `type` varchar(255),
  `period` varchar(255),
  `start_date` timestamp,
  `end_date` timestamp,
  `device` varchar(255),
  `gender` varchar(255),
  `age` varchar(255),
  `created_at` timestamp
);

CREATE TABLE if not exists `Search_Shop` (
  `search_id` integer PRIMARY KEY,
  `keyword_id` integer,
  `sort` varchar(255),
  `created_at` timestamp
);

CREATE TABLE if not exists `Query_Keyword` (
  `query_ID` integer PRIMARY KEY,
  `keyword_id` integer,
  `add_keyword_id` integer,
  `keyword` varchar(255),
  `sort` varchar(255),
  `created_at` timestamp
);

CREATE TABLE if not exists `Search_Keyword` (
  `search_id` integer PRIMARY KEY,
  `query_id` integer,
  `sort` varchar(255),
  `created_at` timestamp
);

CREATE TABLE if not exists `Keywords_Top` (
  `keyword_id` integer PRIMARY KEY,
  `search_id` integer,
  `ranking` integer,
  `keyword` varchar(255),
  `type` varchar(255)
);

CREATE TABLE if not exists `Data_Product` (
  `search_id` integer,
  `product_id` integer PRIMARY KEY,
  `name` varchar(255),
  `lprice` integer,
  `hprice` integer,
  `link` varchar(255),
  `mallName` varchar(255),
  `maker` maker,
  `brand` varchar(255),
  `category1` varchar(255),
  `category2` varchar(255),
  `category3` varchar(255),
  `category4` varchar(255),
  `product_naver_id` integer,
  `score` float
);

CREATE TABLE if not exists `Crawling_store` (
  `search_id` integer PRIMARY KEY,
  `product_id` integer,
  `created_at` timestamp
);

CREATE TABLE if not exists `Data_Reviews` (
  `search_id` integer PRIMARY KEY,
  `review_id` integer,
  `user_id` varchar(255),
  `score` integer,
  `date` timestamp,
  `data` text,
  `emotion_text` varchar(255),
  `emotion_score` float
);

CREATE TABLE if not exists `Data_Posts` (
  `search_id` integer PRIMARY KEY,
  `post_id` integer,
  `title` varchar(255),
  `link` integer,
  `postdate` timestamp,
  `data` text COMMENT 'Description',
  `emotion_text` varchar(255),
  `emotion_score` float
);

CREATE TABLE if not exists `Keyword_Reviews` (
  `keyword_id` integer PRIMARY KEY,
  `review_id` integer,
  `ranking` integer,
  `keyword` integer,
  `emotion_text` varchar(255),
  `emotion_score` float
);

CREATE TABLE if not exists `Keyword_Posts` (
  `keyword_id` integer PRIMARY KEY,
  `post_id` integer,
  `ranking` integer,
  `keyword` integer,
  `emotion_text` varchar(255),
  `emotion_score` float
);