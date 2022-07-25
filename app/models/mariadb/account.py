from datetime import datetime
from typing import Any
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base

from models.mariadb.base_model import BaseModel
Base = declarative_base()

"""CREATE TABLE `account` (
    `acc_id` varchar(100) NOT NULL COMMENT '사용자 ID. BML에서 지정할당',
    `user_id` varchar(100) NOT NULL COMMENT '사용자명',
    `risk_limit` tinyint(3) unsigned NOT NULL DEFAULT 0 COMMENT 'risk 한도. 0-100 사이',
    `algorithm` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '전략과 비중을 key,value의 json으로 저장' CHECK (json_valid(`algorithm`)),
    `algorithm_count` tinyint(3) unsigned DEFAULT 0 COMMENT '실제 사용하는 전략의 개수',
    `base_currency` tinytext NOT NULL COMMENT '기준 통화',
    `initial_amount` float DEFAULT 0 COMMENT '초기 투자금',
    `created_at` datetime DEFAULT NULL,
    `updated_at` datetime DEFAULT NULL,
    PRIMARY KEY (`acc_id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"""    

class Account(Base, BaseModel):
    __tablename__ = 'account'
    acc_id = Column(String, primary_key=True)
    user_id = Column(String)
    risk_limit = Column(Integer)
    base_currency = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


    def __init__(self, **entries):
        self.__dict__.update(entries)
