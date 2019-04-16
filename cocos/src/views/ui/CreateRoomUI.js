// var UIBase = require("src/views/ui/UIBase.js")
// cc.loader.loadJs("src/views/ui/UIBase.js")
"use strict"
var CreateRoomUI = UIBase.extend({
	ctor:function() {
		this._super();
		this.resourceFilename = "res/ui/CreateRoomUI.json";
	},

	initUI:function(){
		this.limit_deal_idx = 0
		this.start_deal_idx = 0
		this.max_lose_score = 0
		
		this.createroom_panel = this.rootUINode.getChildByName("createroom_panel");
		this.select_score_panel = this.rootUINode.getChildByName("select_score_panel");
		this.initCreateRoomPanel()
		this.initSelectScorePanel()

		this.initCreateRoom()
		// create_btn
		this.updateCardDiamond()
	},

	updateCardDiamond:function(){
		var Text_9 = this.rootUINode.getChildByName("createroom_panel").getChildByName("Text_9");
		Text_9.setString("消耗8张房卡或100钻石，游戏开始后扣除");
	},

	initCreateRoomPanel:function(){
		var self = this
		var return_btn = ccui.helper.seekWidgetByName(this.createroom_panel, "return_btn")
		function return_btn_event(sender, eventType){
			if (eventType == ccui.Widget.TOUCH_ENDED) {
				self.hide()
			}
		}
		return_btn.addTouchEventListener(return_btn_event)

		var max_3_deal_chx = ccui.helper.seekWidgetByName(this.createroom_panel, "max_3_deal_chx")
		var unlimited_deal_chx = ccui.helper.seekWidgetByName(this.createroom_panel, "unlimited_deal_chx")
		this.deal_limited_chx_list = [max_3_deal_chx, unlimited_deal_chx]
		function limit_Deal_event(sender, eventType){
			if (eventType == ccui.CheckBox.EVENT_SELECTED || eventType == ccui.CheckBox.EVENT_UNSELECTED) {
				for (var i = 0; i < self.deal_limited_chx_list.length; i++) {
					if (sender != self.deal_limited_chx_list[i]) {
						self.deal_limited_chx_list[i].setSelected(false)
						self.deal_limited_chx_list[i].setTouchEnabled(true)
					}else{
						self.limit_deal_idx = i
                        sender.setSelected(true);
						sender.setTouchEnabled(false)
						cc.log("limit_deal_idx:", self.limit_deal_idx)
					}
				}
			}
		}
		max_3_deal_chx.addTouchEventListener(limit_Deal_event)
		unlimited_deal_chx.addTouchEventListener(limit_Deal_event)
		this.deal_limited_chx_list[0].setTouchEnabled(false)
		cc.log("limit_deal_idx:", this.limit_deal_idx)

		//start deal init
		this.start_deal_chx_list = []
		function start_Deal_event(sender, eventType){
			if (eventType == ccui.CheckBox.EVENT_SELECTED || eventType == ccui.CheckBox.EVENT_UNSELECTED) {
				for (var i = 0; i < self.start_deal_chx_list.length; i++) {
					if (sender != self.start_deal_chx_list[i]) {
						self.start_deal_chx_list[i].setSelected(false)
						self.start_deal_chx_list[i].setTouchEnabled(true)
					}else{
						self.start_deal_idx = i
                        sender.setSelected(true);
						sender.setTouchEnabled(false)
						cc.log("start_deal_idx:", self.start_deal_idx)
					}
				}
			}
		}
		for (var i = 0; i < 4; i++) {
			var start_deal_chx = ccui.helper.seekWidgetByName(this.createroom_panel, "start_deal_chx_" + String(i+1))
			this.start_deal_chx_list.push(start_deal_chx)
			start_deal_chx.addTouchEventListener(start_Deal_event)
		}
		this.start_deal_chx_list[0].setTouchEnabled(false)
		cc.log("start_deal_idx:", this.start_deal_idx)

		var Text_10 = ccui.helper.seekWidgetByName(this.createroom_panel, "Text_10")
		var score_select_btn = ccui.helper.seekWidgetByName(this.createroom_panel, "score_select_btn")
		function score_select_event(sender, eventType){
			if (eventType == ccui.Widget.TOUCH_ENDED) {
				self.select_score_panel.setVisible(true)
			}
		}
		score_select_btn.addTouchEventListener(score_select_event)

		//拖底
		var max_lose_chx = ccui.helper.seekWidgetByName(this.createroom_panel, "max_lose_chx")
		function max_lose_chx_event(sender, eventType){
			cc.log("max_lose_chx_event")
			cc.log(eventType)
			if (eventType == ccui.CheckBox.EVENT_SELECTED) {
				if (self.max_lose_score <= 0) {
					Text_10.setVisible(true)
					score_select_btn.setVisible(true)
					self.max_lose_score = 1
					Text_10.setString("当前拖底分数:" + String(self.max_lose_score * 50))
				}else{
					Text_10.setVisible(false)
					score_select_btn.setVisible(false)
					self.max_lose_score = 0
				}
			}
		}
		max_lose_chx.addTouchEventListener(max_lose_chx_event)

		// AA_chx
		var AA_chx = ccui.helper.seekWidgetByName(this.createroom_panel, "AA_chx")
		function AA_chx_event(sender, eventType){
			if (eventType == ccui.Widget.TOUCH_ENDED) {
				cc.log("暂时不计AA房卡")
			}
		}
		AA_chx.addTouchEventListener(AA_chx_event);
		AA_chx.setVisible(false);
		this.createroom_panel.getChildByName("Image_1").setVisible(false);
	},

	initSelectScorePanel:function(){
		var self = this;
		var Text_10 = ccui.helper.seekWidgetByName(this.createroom_panel, "Text_10")

		this.score_btn_list = []
		function score_btn_event(sender, eventType){
			if (eventType == ccui.Widget.TOUCH_ENDED) {
				for (var i = 0; i < self.score_btn_list.length; i++) {
					if (self.score_btn_list[i] == sender) {
						self.max_lose_score = i+1
						Text_10.setString("当前拖底分数:" + String(self.max_lose_score * 50))
						self.select_score_panel.setVisible(false)
					}
				}
			}
		}
		for (var i = 0; i < 3; i++) {
			var score_btn = ccui.helper.seekWidgetByName(this.select_score_panel, "score_btn_" + String(i+1))
			this.score_btn_list.push(score_btn)
			score_btn.addTouchEventListener(score_btn_event)
		}
	},

	initCreateRoom:function(){
		var self = this
		var create_btn = ccui.helper.seekWidgetByName(this.createroom_panel, "create_btn")
		function create_btn_event(sender, eventType){
			if (eventType == ccui.Widget.TOUCH_ENDED) {
				cutil.lock_ui();
				// var maxDealNum = 3
				// switch(self.limit_deal_idx){
				// 	case 0:
				// 		maxDealNum = 3;
				// 		break;
				// 	case 1:
				// 		maxDealNum = -1;
				// 		break;
				// 	default:
				// 		maxDealNum = 3;
				// 		break;

				// }
				// var startDealNum = 0
				// var diceAdd = 0
				// var isSameAdd = 0
				// switch(self.start_deal_idx){
				// 	case 0:
				// 		startDealNum = 2;
				// 		break;
				// 	case 1:
				// 		startDealNum = 3;
				// 		break;
				// 	case 2:
				// 		startDealNum = 2;
				// 		diceAdd = 8;
				// 		isSameAdd = 1;
				// 		break;
				// 	case 3:
				// 		startDealNum = 2;
				// 		diceAdd = 10;
				// 		isSameAdd = 1;
				// 		break;
				// 	default:
				// 		startDealNum = 2;
				// 		diceAdd = 0;
				// 		isSameAdd = 0;
				// 		break;
				// }

				// var maxLoseScore = self.max_lose_score
				h1global.entityManager.player().createRoom([self.limit_deal_idx, self.start_deal_idx, self.max_lose_score, 0]);
				self.hide()
			}
		}
		create_btn.addTouchEventListener(create_btn_event)
	}
});