create database sweethearts;
use sweethearts;

drop table if exists user;
create table user(
                     id int primary key auto_increment comment '主键',
                     user_name varchar(255) not null comment '用户名',
                     password varchar(255) not null comment '密码',
                     email varchar(255) not null comment '邮箱',
                     point int default 0 comment '积分',
                     sweetheart_id int default 0 comment '恋人ID'
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户表';

drop table if exists goods;
create table goods(
                      id int primary key auto_increment,
                      name varchar(255) not null,
                      price int not null,
                      des varchar(255) not null,
                      create_id int not null,
                      num int not null,
                      is_deleted int not null default 0 comment '0未删除 1删除'
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='商品表';

drop table if exists goods_user;
create table goods_user(
                      id int primary key auto_increment,
                      goods_id int not null,
                      owner_id int not null,
                      user_purchased_quantity int not null
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='商品用户表';

drop table if exists task;
create table task(
                     id int primary key auto_increment,
                     name varchar(255) not null,
                     price varchar(255) not null,
                     des varchar(255) not null,
                     create_id int not null,
                     sweetheart_id int not null,
                     is_finish int default 0
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='任务表';


