# -*- coding: utf-8 -*-

import KBEngine
from KBEDebug import *
import utility as util
import const
import random

class iRoomRules(object):

	def __init__(self):
		# 房间的牌堆
		self.tiles = []
		self.lucky_set = (const.CHAR1, const.CHAR5, const.CHAR9,
		                  const.BAMB1, const.BAMB5, const.BAMB9,
		                  const.DOT1, const.DOT5, const.DOT9, const.DRAGON_RED)
		self.meld_dict = dict()

	def initTiles(self):
		self.tiles = const.CHARACTER * 4 + const.BAMBOO * 4 + const.DOT * 4 + [const.WIND_EAST, const.WIND_SOUTH, const.WIND_WEST, const.WIND_NORTH] * 4 + [const.DRAGON_RED, const.DRAGON_GREEN, const.DRAGON_WHITE] * 4
		self.shuffle_tiles()
		#测试代码
		#1 连续出同一张牌，第二张牌不能碰
		# self.tiles = const.CHARACTER * 4 + const.BAMBOO * 4 + const.DOT * 4 + [const.WIND_EAST, const.WIND_SOUTH, const.WIND_WEST, const.WIND_NORTH] * 4 + [const.DRAGON_RED, const.DRAGON_GREEN] * 4
		# self.shuffle_tiles()
		# self.tiles.insert(0, const.DRAGON_WHITE)
		# self.tiles.insert(1, const.DRAGON_WHITE)
		# self.tiles.insert(2, const.DRAGON_WHITE)
		# self.tiles.insert(6, const.DRAGON_WHITE)

	def shuffle_tiles(self):
		random.shuffle(self.tiles)

	def swapTileToTop(self, tile):
		if tile in self.tiles:
			tileIdx = self.tiles.index(tile)
			self.tiles[0], self.tiles[tileIdx] = self.tiles[tileIdx], self.tiles[0]

	def winCount(self):
		pass

	def canOperationByKingTile(self, curIdx):
		"""打出财神后是否可以操作"""
		if self.discardKingTileIdx < 0:
			return True
		elif curIdx == self.discardKingTileIdx:
			return True
		return False

	def canOperationByTimesLimit(self, curIdx):
		"""萧山麻将同一家不能吃碰杠超过两次"""
		if curIdx is None:
			return True
		numList = [0] * 4
		for i, record in enumerate(self.players_list[curIdx].op_r):
			if record[2] != curIdx and record[0] in [const.OP_CHOW, const.OP_PONG, const.OP_EXPOSED_KONG]:
				numList[record[2]] += 1
		if numList[self.last_player_idx] >= 2:
			return False
		return True
		
	def can_cut_after_kong(self):
		return True

	def can_discard(self, tiles, t):
		if t in tiles:
			return True
		return False

	def can_chow(self, tiles, t, pIdx = None):
		if not self.canOperationByTimesLimit(pIdx):
			return False
		if not self.canOperationByKingTile(pIdx):
			return False
		if self.last_player_idx != (pIdx + 3)%4:
			return False
		if t == self.kingTile:
			return False
		if t >= 30:
			return False
		neighborTileNumList = [0, 0, 1, 0, 0]
		for i in range(len(tiles)):
			if (tiles[i] - t >= -2 and tiles[i] - t <= 2) and tiles[i] != self.kingTile:
				neighborTileNumList[tiles[i] - t + 2] += 1
		for i in range(0,3):
			tileNum = 0
			for j in range(i,i+3):
				if neighborTileNumList[j] > 0:
					tileNum += 1
				else:
					break
			if tileNum >= 3:
				return True
		return False

	def can_chow_one(self, tiles, tile_list, pIdx = None):
		""" 能吃 """
		if not self.canOperationByTimesLimit(pIdx):
			return False
		if not self.canOperationByKingTile(pIdx):
			return False
		if self.last_player_idx != (pIdx + 3)%4:
			return False
		if self.kingTile in tile_list:
			return False
		if tile_list[0] >= 30:
			return False
		if sum([1 for i in tiles if i == tile_list[1]]) >= 1 and sum([1 for i in tiles if i == tile_list[2]]) >= 1:
			sortLis = sorted(tile_list)
			if (sortLis[2] + sortLis[0])/2 == sortLis[1] and sortLis[2] - sortLis[0] == 2:
				return True
		return False

	def can_pong(self, tiles, t, pIdx = None):
		""" 能碰 """
		if not self.canOperationByTimesLimit(pIdx):
			DEBUG_MSG("can not pong can'tOperationByTimesLimit")
			return False
		if not self.canOperationByKingTile(pIdx):
			DEBUG_MSG("can not pong can'tOperationByKingTile")
			return False
		if self.getSerialSameTileNum() >= 2: #萧山麻将 上下家同时打出一张牌，上家未操作，下家打出也不行
			DEBUG_MSG("can not pong getSerialSameTileNum >= 2")
			return False
		if t == self.kingTile:
			return False
		return sum([1 for i in tiles if i == t]) >= 2

	def getSerialSameTileNum(self):
		"""
		获取上下家打出同一张牌的张数
		"""
		if len(self.op_record) <= 0 or self.op_record[-1][0] != const.OP_DISCARD:
			return 0

		playerDiscardList = []
		for i in range(0, len(self.op_record))[::-1]:
			if len(playerDiscardList) >= 2:
				break
			if self.op_record[i][0] == const.OP_DISCARD:
				playerDiscardList.append(self.op_record[i])

		if len(playerDiscardList) >= 2 and playerDiscardList[-1][3] == playerDiscardList[-2][3]: # A AA A 碰出打法会判断下家可以碰，但麻将不会有相同6张
			return 2
		return 1

	def can_exposed_kong(self, tiles, t, pIdx = None):
		""" 能明杠 """
		if not self.canOperationByTimesLimit(pIdx):
			return False
		if not self.canOperationByKingTile(pIdx):
			return False
		if t == self.kingTile:
			return False
		return util.get_count(tiles, t) == 3

	def can_self_exposed_kong(self, player, t):
		""" 自摸的牌能够明杠 """
		for op in player.op_r:
			if op[0] == const.OP_PONG and op[1][0] == t:
				return True
		return False

	def can_concealed_kong(self, tiles, t):
		""" 能暗杠 """
		if t == self.kingTile:
			return False
		return util.get_count(tiles, t) == 4

	# def can_win(self, tiles):
	# 	""" 能胡牌 """
	# 	if len(tiles) % 3 != 2:
	# 		return False

	# 	tiles = sorted(tiles)
	# 	chars, bambs, dots, dragon_red = self.classify_tiles(tiles)

	# 	c_need1 = util.meld_only_need_num(chars, self.meld_dict)
	# 	c_need2 = util.meld_with_pair_need_num(chars, self.meld_dict)
	# 	if c_need1 > dragon_red and c_need2 > dragon_red:
	# 		return False

	# 	b_need1 = util.meld_only_need_num(bambs, self.meld_dict)
	# 	b_need2 = util.meld_with_pair_need_num(bambs, self.meld_dict)
	# 	if b_need1 > dragon_red and b_need2 > dragon_red:
	# 		return False

	# 	d_need1 = util.meld_only_need_num(dots, self.meld_dict)
	# 	d_need2 = util.meld_with_pair_need_num(dots, self.meld_dict)
	# 	if d_need1 > dragon_red and d_need2 > dragon_red:
	# 		return False

	# 	if  c_need2 + b_need1 + d_need1 <= dragon_red or\
	# 		c_need1 + b_need2 + d_need1 <= dragon_red or\
	# 		c_need1 + b_need1 + d_need2 <= dragon_red:
	# 		return True
	# 	return False

	def first_hand_win(self, tiles):
		return sum([1 for t in tiles if t == const.DRAGON_RED]) == 4

	def cal_lucky_tile(self, win_tiles, lucky_tile):
		if lucky_tile == 1:
			# 一码全中
			if len(self.tiles) > 0:
				final = self.tiles[0]
				self.tiles = self.tiles[1:]
				return [final], 10 if final == const.DRAGON_RED else final%10
			else:
				return [], 0
		else:
			if util.get_count(win_tiles, const.DRAGON_RED) == 0:
				lucky_tile += 1

			final = min(len(self.tiles), lucky_tile)
			see_tiles = []
			count = 0
			for i in range(final):
				t = self.tiles[0]
				self.tiles = self.tiles[1:]
				see_tiles.append(t)
				if t in self.lucky_set:
					count += 1
			return see_tiles, count

	def classify_tiles(self, tiles):
		chars = []
		bambs = []
		dots  = []
		dragon_red = 0
		for t in tiles:
			if t in const.CHARACTER:
				chars.append(t)
			elif t in const.BAMBOO:
				bambs.append(t)
			elif t in const.DOT:
				dots.append(t)
			elif t == const.DRAGON_RED:
				dragon_red += 1
			else:
				DEBUG_MSG("iRoomRules classify tiles failed, no this tile %s"%t)
		return chars, bambs, dots, dragon_red

	def can_win(self, handTiles, idx):
		DEBUG_MSG("check can win")
		resultDesList = ["乱风","四道杠","天胡","地胡","双豪7","十风","7对","豪7","清一色","大对子","大吊车","财一飘","财二飘","暗杠杠开","明杠杠开","暴头","平胡"]
		resultList = [0]*len(resultDesList)
		""" 能胡牌 """
		if len(handTiles) % 3 != 2:
			return resultList

		handTiles = sorted(handTiles)
		
		finalDrawTile = self.players_list[idx].last_draw
		upTiles = self.players_list[idx].upTiles
		player_op_r = self.players_list[idx].op_r

		#kings, dragon_white, chars, bambs, dots, winds, dragon_red_green
		classifyList = util.classifyTiles(handTiles, self.kingTile)
		kingTilesNum = len(classifyList[0])
		dragonWhiteNum = len(classifyList[1])
		listButKing = []
		listButKingWhite = []
		for i in range(len(classifyList)):
			if i == 0:
				continue
			if i == 1:
				listButKing.extend(classifyList[i])
				continue
			listButKing.extend(classifyList[i])
			listButKingWhite.extend(classifyList[i])

		#乱风
		if util.checkCanWinAllWindDragon(handTiles, upTiles, self.kingTile):
			resultList[0] = 1
		#四道杠
		if util.checkCanWinFourKong(handTiles, upTiles):
			resultList[1] = 1
		#十风
		#player_op_r ==> op_r
		discardWindNum = util.getCanWinTenWindDragonNum(handTiles, player_op_r)
		if discardWindNum > 0:
			resultList[5] = discardWindNum

		#清一色 不必暴头
		isFlush = util.checkIsFlush(handTiles, upTiles, self.kingTile)

		#胡7对
		if util.checkCanWin7Pairs(listButKing, kingTilesNum, self.kingTile, finalDrawTile, isFlush):
			kongNum = util.getKongNum(listButKing)
			if kongNum == 1:
				resultList[7] = 1
			elif kongNum >1:
				resultList[4] = 1
			else:
				resultList[6] = 1
			#暴头
			if kingTilesNum > 0:
				resultList[15] = 1
		
	
		#/**必须先判断是不是7对，除了7对这种特殊情况，手牌如果有暗杠没杠是无法胡的**/
		if util.checkIsWin(listButKingWhite, kingTilesNum, dragonWhiteNum, self.kingTile, finalDrawTile, isFlush) or resultList[4] or resultList[6] or resultList[7]:
			#天胡 地胡
			discardNum = util.getDiscardNum(player_op_r)
			if discardNum <= 0 and len(handTiles) == 14:
				if self.dealer_idx == idx:	#天胡
					resultList[2] = 1
				else:
					resultList[3] = 1	#地胡
			#清一色
			if isFlush:
				resultList[8] = 1

			#是否 大对子
			if util.checkIsBigPair(listButKing, upTiles, self.kingTile, kingTilesNum):
				resultList[9] = 1

			#大吊车
			if len(handTiles) == 2:
				resultList[10] = 1
			
			#财飘
			throwKingNum = util.getDiscardSerialKingTileNum(player_op_r, handTiles, self.kingTile)
			if throwKingNum == 1:
				resultList[11] = 1
			elif throwKingNum == 2:
				resultList[12] = 1

			#杠开
			kongWinNum = util.getNearlyKongType(player_op_r)
			if kongWinNum == 1:
				resultList[13] = 1
			elif kongWinNum == 2:
				resultList[14] = 1
			#暴头
			if kingTilesNum > 0:
				resultList[15] = 1
			else:
				resultList[16] = 1
		
		DEBUG_MSG("can_win result:{0}".format(str(resultList)))
		return resultList

	def cal_multiple(self, resultList): # tips 10代表清牌 = 2^1024
		"""计算番数"""
		#"乱风","四道杠","天胡","地胡","双豪7","十风","7对","豪7","清一色","大对子","大吊车","财一飘","财二飘","暗杠杠开","明杠杠开","暴头","平胡"
		mutipleList = [10, 10, 10, 10, 10, 1, 3, 4, 3, 1, 1, 1, 2, 2, 1, 1, 0]

		#"乱风","四道杠","天胡","地胡","双豪7",
		specialList = resultList[0:5]
		if sum([1 for i in specialList if i>0]) > 0:
			return 10

		#十风  第十张后 每打出一张风 多加一番
		if resultList[5] > 0:
			return mutipleList[5] * resultList[5]

		#清豪7 = 清一色 + 7对
		if resultList[6] == 1 and resultList[8] == 1:
			return 10

		normalList = resultList[6:]
		normalMutList = mutipleList[len(normalList) * -1:]
		mutipleNum = 0
		for i in range(len(normalList)):
			if normalList[i] > 0:
				mutipleNum += normalMutList[i]
		return mutipleNum

