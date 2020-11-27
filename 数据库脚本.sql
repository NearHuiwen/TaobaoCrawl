/*
Navicat MySQL Data Transfer

Source Server         : localhost_3306
Source Server Version : 80019
Source Host           : localhost:3306
Source Database       : taobao

Target Server Type    : MYSQL
Target Server Version : 80019
File Encoding         : 65001

Date: 2020-11-27 11:28:29
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for t_goods
-- ----------------------------
DROP TABLE IF EXISTS `t_goods`;
CREATE TABLE `t_goods` (
  `nid` varchar(50) COLLATE utf8mb4_general_ci NOT NULL COMMENT '商品ID',
  `search_word` varchar(30) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '搜索词',
  `title` varchar(255) COLLATE utf8mb4_general_ci NOT NULL COMMENT '商品标题',
  `pic_url` varchar(500) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '简介图片',
  `detail_url` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '商品详情网站地址',
  `view_price` float(10,2) NOT NULL COMMENT '商品价格（最低价）',
  `item_loc` varchar(30) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '商品来源地市',
  `view_sales` int DEFAULT NULL COMMENT '已有多少个人收到货',
  `comment_count` int unsigned DEFAULT NULL COMMENT '积累评论数',
  `nick` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '商家名称',
  `shop_link` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '商铺网站地址',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`nid`),
  UNIQUE KEY `detail_url` (`detail_url`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
SET FOREIGN_KEY_CHECKS=1;
