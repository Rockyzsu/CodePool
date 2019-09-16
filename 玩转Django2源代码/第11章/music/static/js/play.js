require.config({
　paths: {
    "jquery": "jquery.min",
    "com": "common.min"
  }
});

require(['jquery','com',"jquery.jplayer"], function ($,com){
  //pk柱高度
  function pkCol(){
    var bar = $('.vote-bar-inner');
    var obj1 = bar.eq(0);
    var a = obj1.parent().prev().find('span').text();
    var obj2 = bar.eq(1);
    var b = obj2.parent().prev().find('span').text();
    com.pkTicket(obj1,obj2,a,b,140)
  }
  pkCol();
  //歌曲纠错
  $('#songCorr').on('click','li',function(){
    var temp = 'corr_' + $('#currentSong').attr('data-rel') + '_' + $(this).index();
    if(localStorage[temp]){
      com.msg('请勿重复提交！');
      return false;
    }
    localStorage[temp] = 1;
    com.loadOpen();
    setTimeout(function(){
      com.loadClose();
      com.msg('提交成功，感谢您的参与！');
    },300);
  });
  if(localStorage.playRule == 'none') localStorage.playRule = '';
  //播放顺序
  if($('#songlist').find('li').length>1){
    localStorage.playRule = localStorage.playRule || 'order';
  }else{
    localStorage.playRule = '';
  }
  if(localStorage.playRule){
    $('#playleixin').find('.'+localStorage.playRule).addClass('current').siblings().removeClass('current');
  }
  //下一首播放歌曲
  setNextPlay();
  var time = 0;
  if($('#lrc_content').length>0){
    getLyrics($('#lrc_content').val(),$('#lrc_list'));
    //定义播放器
    $("#jquery_jplayer_1").jPlayer({
        ready: function (event) {
            $(this).jPlayer("setMedia", {
                mp3: $("#jquery_jplayer_1").attr('data-url') //mp3的播放地址
            });
            $("#jquery_jplayer_1").jPlayer('play');
        },
        timeupdate: function (event) {
            time = event.jPlayer.status.currentTime;
        },
        play: function (event) {
            //点击开始方法调用lrc。start歌词方法 返回时间time
            $.lrc.start($('#lrc_content').val(), function () {
                return time;
            });
            $('.click_play').hide().next().show();
        },
        pause: function(){
          $('.click_pause').hide().prev().show();
        },
        ended: function (event) {
            // $("#lrc_list").removeAttr("style").html("<li>歌曲播放完毕！</li>");
            if(localStorage.playNext != null && localStorage.playNext.indexOf('.html') != -1){
              location.href = location.origin + localStorage.playNext;
            }
        },
        swfPath: "/js",  		//存放jplayer.swf的路径
        solution: "html, flash", //支持的页面
        supplied: "mp3", 	//支持的音频的格式
        wmode: "window"
    });
  }
  //播放
  $('.jp_img').on('click',function(){
    $("#jquery_jplayer_1").jPlayer('play');
  });
  $('.click_play').on('click',function(){
    $("#jquery_jplayer_1").jPlayer('play');
  });
  //暂停
  $('.click_pause').on('click',function(){
    $("#jquery_jplayer_1").jPlayer('pause');
    //$(this).hide().prev().show();
  });
  //显示高级点评
  $('#J_WriteAnchor,.J_Advanced').on('click',function(){
    $('#sidePanel').css('right',0);
    $(document).one('click',function(){
      $('#sidePanel').css('right','-1010px');
    });
    return false;
  });
  //隐藏高级点评
  $('#sidePanel').on('click','.side-panel-close',function(){
    $('#sidePanel').css('right','-1010px');
  });
  $('#sidePanel').on('click',function(event){
    event.stopPropagation();
  });
  $('#J_StarArea').on({
    'mouseenter':function(){
      $('#J_AdvancedScoreTip').hide();
    },'mouseleave':function(){
      if($('#countScore').val()==0)$('#J_AdvancedScoreTip').show();
    }
  });
  //高级点评打分
  $('.advanced-star,.short-review-star').on({
    'mouseenter':function(){
      var str = '';
      $(this).addClass('active').prevAll().addClass('active').end().nextAll().removeClass('active');
      switch($(this).index()){
        case 0:
          str = '很差';
          break;
        case 1:
          str = '较差';
          break;
        case 2:
          str = '一般';
          break;
        case 3:
          str = '推荐';
          break;
        case 4:
          str = '力荐';
          break;
        default:
          str = '';
          break;
      }
      $(this).parent().next().text(str);
    },
    'click':function(){
      var val = ($(this).prevAll().length+1)*2;
      var total = (''+$('#J_StarArea').find('.active').length * 0.4).length<3?$('#J_StarArea').find('.active').length * 0.4:($('#J_StarArea').find('.active').length * 0.4).toFixed(1);
      $(this).siblings().last().val(val);
      $('#countScore').val(total);
      $('#rateAverage').text(total);
      $('#averageStar').css('width',total*10+'%');
    }
  },'div');
  $('.advanced-star,.short-review-star').on({
    'mouseleave':function(){
      var val = $(this).find('input').val()/2;
      var str = '';
      if(val>0){
        $.each($(this).find('div'),function(i,e){
          if(i<val){
            $(e).addClass('active')
          }else{
            $(e).removeClass('active');
          }
        });
        switch(val){
          case 1:
            str = '很差';
            break;
          case 2:
            str = '较差';
            break;
          case 3:
            str = '一般';
            break;
          case 4:
            str = '推荐';
            break;
          case 5:
            str = '力荐';
            break;
          default:
            str = '';
            break;
        }
      }else{
        $(this).find('div').removeClass('active');
      }
      $(this).next().text(str);
    }
  });
  //高级点评提交
  $('#advReviewBtn').on('click',function(){
    var url = '/ajax_api_all_comment';
    var json = {};
    var str = '';
    var origin = location.origin;
    var isReview = location.href.indexOf('review') != -1;
    //歌曲id
    json.song_id = $('#currentSong').attr('data-rel');
    //封面
    json.cover = $('#coverScore').val();
    //作词
    json.lyrics = $('#lyricsScore').val();
    //作曲
    json.comsposer = $('#comsposerScore').val();
    //歌手演艺
    json.artist = $('#artistScore').val();
    //共鸣
    json.resonate = $('#resonateScore').val();
    //评论
    json.comment = $('#commentScore').val();
    //总分
    json.count = $('#countScore').val();
    if(json.cover == 0){
      $('#scoreTips').text('*请给封面评分！');
      return;
    }else if(json.lyrics == 0){
      $('#scoreTips').text('*请给作词评分！');
      return;
    }else if(json.comsposer == 0){
      $('#scoreTips').text('*请给作曲评分！');
      return;
    }else if(json.artist == 0){
      $('#scoreTips').text('*请给歌手演艺评分！');
      return;
    }else if(json.resonate == 0){
      $('#scoreTips').text('*请给共鸣评分！');
      return;
    }else if(json.comment.length < 10){
      $('#scoreTips').text('*评论不能少于10个字！');
      return;
    }
    com.loadOpen();
    $.ajax({
      url:url,
      type:'POST',
      async:false,
      data:json,
      timeout:10000,
      error:function(http,err){
        $('#scoreTips').text('系统错误！');
        com.loadClose();
      },
      success:function(data){
        com.loadClose();
        var dataJson = JSON.parse(data);
        if(dataJson.result == 'success'){
          if(isReview){
            location.reload();
          }else{
            window.open(origin+'/review_'+dataJson.song_id+'_1.html','_blank');
            $('#sidePanel').css('right','-1010px');
          }
        }else{
          $('#scoreTips').text('系统内部错误！');
        }
        /*if(data == 'success'){
          $('#scoreTips').text('点评成功！');
        }else{
          $('#scoreTips').text('系统内部错误！');
        }*/
      }
    });
  });
  //评论功能
  $('#comment').on({
    'focus':function(){
      if($(this).val() == '您对该歌曲的感受，分享更多内容可选择高级点评'){
        $(this).val('');
      }
    },
    'blur':function(){
      if($(this).val().trim() == ''){
        $(this).val('您对该歌曲的感受，分享更多内容可选择高级点评');
      }
    }
  });
  //发布评论
  $('#scoreBtn').on('click',function(){
    var url = '/ajax_api_all_comment';
    var json = {};
    var str = '';
    var $this = $(this);
    var origin = location.origin;
    var isReview = location.href.indexOf('review') != -1;
    //歌曲id
    json.song_id = $('#currentSong').attr('data-rel');
    //评分
    json.cover = json.lyrics = json.comsposer = json.artist = json.resonate = json.count = $('#defaultScore').val();
    //评论
    json.comment = $('#comment').val();
    if(json.cover == 0){
      $('#scoreTips2').text('*请先评分！');
      return;
    }else if(json.comment.length < 10 || json.comment.trim() == '您对该歌曲的感受，分享更多内容可选择高级点评'){
      $('#scoreTips2').text('*评论不能少于10个字！');
      return;
    }
    com.loadOpen();
    $.ajax({
      url:url,
      type:'POST',
      data:json,
      async:false,
      timeout:10000,
      error:function(http,err){
        console.error(http,err);
        $('#scoreTips2').text('系统错误！');
        com.loadClose();
      },
      success:function(data){
        var dataJson = JSON.parse(data);
        if(dataJson.result == 'success'){
          if(isReview){
            location.reload();
          }else{
            window.open(origin+'/review_'+dataJson.song_id+'_1.html','_blank');
          }
        }else{
          $('#scoreTips2').text('系统内部错误！');
        }
        com.loadClose();
      }
    });
  });
  //猜你喜欢的换一换功能
  $('#irefresh').on('click',function(){
    var $this = $(this);
    var id = $('#currentSong').attr('data-rel');
    com.loadOpen();
    $.ajax({
      url:'/ajax_api_index_change_like',
      type:'POST',
      timeout:10000,
      error:function(http,err){
        console.error(http,err);
        com.loadClose();
      },
      success:function(data){
        var json = JSON.parse(data);
        var html = '';
        $.each(json,function(i,e){
          if(i<3){
            html += '<li><a class="pic layz_load pic_po" href="/song_' + e.song_id + '.html" ' +
                    'target="play" title="' + e.song_name + '-' + e.song_artist + '">' +
                    '<img data-src="' + e.song_image + '" alt="' + e.song_name + '的封面"></a>' +
                    '<h4 class="title"><a href="/song_' + e.song_id + '.html" target="play" ' +
                    'title="' + e.song_name + '-' + e.song_artist + '">' + e.song_name + '</a></h4>' +
                    '<a href="singer-' + e.singer_id + '.html" target="_blank" ' +
                    'title="歌手-' + e.song_artist + '" class="meta">' + e.song_artist + '</a>' +
                    '<span class="compare-btn" data-rel="'+e.song_id+'" data-name="'+e.song_name+'" ' +
                    'data-img="'+e.song_image+'" data-artist="'+e.song_artist+'"><i></i>PK</span></li>';
          }
        });
        $this.parent().next().html(html);
        com.showImg();
        com.loadClose();
      }
    });
  });
  //PK
  $('#J_ToCompare').on('click',function(){
    var $cur = $('#currentSong');
    var id = $cur.attr('data-rel');
    var name = $cur.attr('data-name');
    var img = $cur.attr('data-img');
    var artist = $cur.attr('data-artist');
    com.addPk(id,name,img,artist);
    $('#J_WidgetCompare').show();
    $(document).one('click',function(){
      $('#J_WidgetCompare').hide();
    });
    return false;
  });
  $('#J_WidgetCompare').on('click','.close',function(){
    $('#J_WidgetCompare').hide();
  });
  $('#J_WidgetCompare').on('click','.compare-btn',function(){
    var $this = $(this);
    var id = $this.attr('data-rel');
    var name = $this.attr('data-name');
    var img = $this.attr('data-img');
    var artist = $this.attr('data-artist');
    com.addPk(id,name,img,artist);
  });
  $('#J_WidgetCompare').on('click',function(){
    return false;
  });
  $('#J_InterestList').on('click','.compare-btn',function(){
    var $this = $(this);
    var id = $this.attr('data-rel');
    var name = $this.attr('data-name');
    var img = $this.attr('data-img');
    var artist = $this.attr('data-artist');
    com.addPk(id,name,img,artist);
  });
  //关闭PK框
  $('#v3CompareClose').on('click',function(){
    $('#v3CompareBox').hide();
  });
  $('#v3CompareBox').on('click',function(event){
    event.stopPropagation();
  });
  //删除PK
  $('#v3CompareItems').on('click','.v3-compare-item-del',function(){
    $(this).closest('li').remove();
    $('#v3CompareNum').text($('#v3CompareNum').text()-1);
    $('#v3CompareParamBtn').attr('href','javascript:;').removeAttr('target');
  });
  //清空PK
  $('#v3CompareDelAll').on('click',function(){
    $('#v3CompareItems').empty();
    $('#v3CompareNum').text(0);
    $('#v3CompareParamBtn').attr('href','javascript:;').removeAttr('target');
  });
  //PK切换
  $('.pk-other-list').on('click','li',function(){
    $(this).addClass('active').siblings().removeClass('active');
    var div = $(this).find('.pk-other-pic');
    $('#songLink').prop('href','/song_'+div.attr('data-id')+'.html');
    $('#pkName').text(div.attr('data-name')).prop('href','/song_'+div.attr('data-id')+'.html');
    $('#pkSinger').text(div.attr('data-singer')).prop('href','singer-'+div.attr('data-singid')+'.html');
    $('#pkTicket').text(div.attr('data-ticket'));
    $('#pkImg').attr('src',div.attr('data-img'));
    $('.pk-more-btn').get(0).href = div.attr('data-pkurl');
    pkCol();
  });
  //显示隐藏回复
  $('.J_ShowRepy').on('click',function(){
    if($(this).attr('data-done')==0){
      $(this).attr('data-done',1);
      $(this).parent().next().show();
    }else{
      $(this).attr('data-done',0);
      $(this).parent().next().hide();
    }
  });
  //一级回复
  $('.comment-placeholder').on('focus','input',function(){
    $(this).closest('.comment-placeholder').hide().next().show().find('textarea').focus();
    $('#replyTips').empty();
  });
  $('.comment-poster').on('focus','textarea',function(){
    $('#replyTips').empty();
  });
  $('.comment-poster').on('blur','textarea',function(){
    if($(this).val()!=null && $.trim($(this).val())==''){
      $(this).closest('.comment-poster').hide().prev().show();
    }
  });
  //提交回复
  $('#J_CommentList').on('click','.sub_comment',function(){
    var $this = $(this);
    var url = '/ajax_api_reply';
    var json = {};
    //回复id
    json.score_id = $this.prev().val();
    //回复内容
    json.reply_content = $this.parent().prev().find('textarea').val();
    if(!json.reply_content || json.reply_content.length == 0){
      $('#replyTips').text('请写回复！');
      return;
    }else if(json.reply_content.length < 5){
      $('#replyTips').text('回复不能少于5个字！');
      return;
    }
    com.loadOpen();
    $.ajax({
      url:url,
      type:'POST',
      data:json,
      timeout:10000,
      error:function(http,err){
        console.error(http,err);
        $('#scoreTips2').text('系统错误！');
        com.loadClose();
      },
      success:function(data){
        var $div = $('<div class="reply-item">');
        var html = '';
        var dataJson = JSON.parse(data);
        if(dataJson.result == 'success'){
          $('#replyTips').text('');
          $this.parent().prev().find('textarea').val('');
          html += '<a href="javascript:;" class="user-face" taget="_blank"><img src="/static/user.jpg" width="30" height="30"></a>' +
                  '<div class="reply-user"><a href="javascript:;">匿名用户</a><em>' + dataJson.time + '</em></div>' +
                  '<p>' + json.reply_content + '</p>';
          $div.html(html);
          //插入新的回复
          $('.more-reply').before($div);
          //修改回复数量
          var $replayNum = $this.closest('.comment-expand').prev().find('.J_ShowRepy b');
          $replayNum.text(+$replayNum.text()+1);
          //隐藏回复框
          $this.parent().parent().hide().prev().show();
        }else{
          $('#replyTips').text('系统内部错误！');
        }
        com.loadClose();
      }
    });
  });
  //点赞
  $('#J_CommentList').on('click','.J_ReviewHelp',function(){
    var $this = $(this);
    var id = $this.next().val();
    com.loadOpen();
    $.ajax({
      url:'/ajax_api_reply_praise?score_id='+id,
      type:'GET',
      timeout:10000,
      error:function(http,err){
        console.error(http,err);
        com.loadClose();
      },
      success:function(data){
        var $numObj = $this.find('b');
        if(data == 'add'){
          $numObj.text(+$numObj.text()+1);
          $this.addClass('laud');
        }else if(data == 'reduce'){
          $numObj.text(+$numObj.text()-1);
          $this.removeClass('laud');
        }
        com.loadClose();
      }
    });
  });
  //二级回复
  // $('.reply-func').on('click','a',function(){
  //   var name = $(this).parent().prev().prev().find('a').text();
  //   $(this).parent().next().toggle().find('textarea').val('回复@'+name+'：');
  // });
  //想听(歌曲点赞)
  $('#J_WantBuy').on('click',function(){
    if(!$(this).hasClass('wanted')){
      $(this).addClass('wanted');
    }
  });
  //相关歌曲焦点切换
  new com.FocusSwitch($('#J_PartsList'),null,true,10000,$('#J_PartsPrev'),$('#J_PartsNext')).init();
  //添加歌曲
  $('#addSong').on('click',function(){
    $('#addSongBox').show();
    $(document).one('click',function(){
      $('.hotsearch').show();
      $('#sugboxid').empty().parent().hide();
      $('#addSongBox').hide();
    });
    return false;
  });
  $('#addSongBox').on('click',function(event){
    event.stopPropagation();
  });
  $('#addSongBox').on('click','.box_close',function(){
    $('.hotsearch').show();
    $('#sugboxid').empty().parent().hide();
    $('#addSongBox').hide();
  });
  //搜索添加歌曲
  $('#reSearch').on('click','span',function(){
    var $this = $(this);
    var key = $this.text();
    searchAddSong(key);
    return false;
  });
  $('#serbtn').on('click',function(){
    var $this = $(this);
    var key = $this.prev().val().trim();
    if(key != ''){
      searchAddSong(key);
    }
  });
  //加入播放列表
  $('#sugboxid').on('click','dd',function(){
    var $this = $(this);
    var json = {};
    var url = $this.attr('data-url');
    var id = $this.attr('data-id');
    var only = true;
    /*if(isNaN(url/1)){
      id = url.slice(url.indexOf('_')+1,url.indexOf('.'));
    }else{
      id = url;
    }*/
    json.song_id = id;
    json.song_name = $this.attr('data-name');
    json.song_artist = $this.attr('data-artist');
    $.each($('#songlist').find('li'),function(i,e){
      if($(e).attr('data-id')==id){
        only = false;
        return false;
      }
    });
    if(!only){
      com.msg('歌曲已经在播放列表中！');
      return false;
    }
    com.loadOpen();
    $.ajax({
      url:'/ajax_api_add_song',
      type:'POST',
      data:json,
      timeout:10000,
      error:function(http,err){
        console.error(http,err);
        com.loadClose();
      },
      success:function(data){
        var html = '';
        var num = +$('#songlist').find('li').last().find('.num').text();
        if(data == 'success'){
          html += '<li data-id="' + json.song_id + '">' +
                  '<span class="num">' + (num+1) + '</span>' +
                  '<a class="name" href="' + url + '" target="play">' + json.song_name + '</a>' +
                  '<a class="singer" href="javascript:;" target="_blank">' + json.song_artist + '</a>' +
                  '<span class="menu"><a class="del pling" href="javascript:void(0)">删除</a></span>';
          $('#songlist').append($(html));
          com.msg('添加歌曲成功！');
        }
        com.loadClose();
      }
    });
  });
  //从播放列表删除歌曲
  $('#songlist').on('click','.menu',function(){
    var $this = $(this);
    var $parent = $this.parent();
    if($parent.hasClass('current')){
      return false;
    }
    var id = $parent.attr('data-id');
    com.loadOpen();
    $.ajax({
      url:'ajax_api_delete_song?type=sing&song_id='+id,
      type:'GET',
      timeout:10000,
      error:function(http,err){
        console.error(http,err);
        com.loadClose();
      },
      success:function(data){
        if(data == 'success'){
          $parent.remove();
          $.each($('#songlist').find('li'),function(i,e){
            $(e).find('.num').text(i+1);
          });
          com.msg('删除歌曲成功！');
        }else{
          com.msg('删除失败！');
        }
        com.loadClose();
        setNextPlay();
      }
    });
  });
  //播放列表操作
  $('#playleixin').on('click','li',function(){
    var $this = $(this);
    var run = $this.attr('data-run');
    var songlist = $('#songlist');
    var id = songlist.find('.current').attr('data-id');
    var url = '';
    if($this.hasClass('current')){
      return;
    }
    if(run == 'next'){
      //播放下一首
      if(songlist.find('li').length>1){
        if(songlist.find('.current').next().length>0){
          url = songlist.find('.current').next().find('.name').attr('href');
        }else{
          url = songlist.find('li').eq(0).find('.name').attr('href');
        }
      }else{
        com.msg('歌曲列表中只有一首歌曲！');
        return false;
      }
      location.href = location.origin + '/' + url;
    }else if(run == 'cl_all'){
      if(songlist.find('li').length<=1)return;
      com.alert({
        content:'确定清空播放列表吗？',
        button:2,
        time:60000
      },function(){
        com.loadOpen();
        //清除全部
        $.ajax({
          url:'ajax_api_delete_song?type=all&song_id='+id,
          type:'GET',
          timeout:10000,
          error:function(http,err){
            console.error(http,err);
            com.loadClose();
          },
          success:function(data){
            if(data == 'success'){
              songlist.find('.current').find('.num').text('1').end().siblings().remove();
              localStorage.playRule = '';
              localStorage.playNext = '';
              com.msg('已清除全部歌曲！');
            }
            com.loadClose();
          }
        });
      });
    }else{
      if(songlist.find('li').length>1){
        localStorage.playRule = run;
      }else{
        localStorage.playRule = '';
      }
      $this.addClass('current').siblings().removeClass('current');
      setNextPlay();
    }
  });
  //分页
  if($('#pageBar').length>0){
    com.pages($('#curPage').val(),$('#countPage').val(),$('#pageBar'));
  }
  //歌词滚动
  (function($){
  	$.lrc = {
  		handle: null, /* 定时执行句柄 */
  		list: [], /* lrc歌词及时间轴数组 */
  		regex: /^[^\[]*((?:\s*\[\d+\:\d+(?:\.\d+)?\])+)([\s\S]*)$/, /* 提取歌词内容行 */
  		regex_time: /\[(\d+)\:((?:\d+)(?:\.\d+)?)\]/g, /* 提取歌词时间轴 */
  		regex_trim: /^\s+|\s+$/, /* 过滤两边空格 */
  		callback: null, /* 定时获取歌曲执行时间回调函数 */
  		interval: 0.3, /* 定时刷新时间，单位：秒 */
  		format: '<li>{html}</li>', /* 模板 */
  		prefixid: 'lrc', /* 容器ID */
  		hoverClass: 'hover', /* 选中节点的className */
  		hoverTop: 100, /* 当前歌词距离父节点的高度 */
  		duration: 0, /* 歌曲回调函数设置的进度时间 */
  		__duration: -1, /* 当前歌曲进度时间 */
  		/* 歌词开始自动匹配 */
  		start: function(txt, callback) {
  			if(typeof(txt) != 'string' || txt.length < 1 || typeof(callback) != 'function') return;
  			/* 停止前面执行的歌曲 */
  			this.stop();
  			this.callback = callback;
  			var item = null, item_time = null, html = '';
  			/* 分析歌词的时间轴和内容 */
  			txt = txt.split("\n");
  			for(var i = 0; i < txt.length; i++) {
  				item = txt[i].replace(this.regex_trim, '');
  				if(item.length < 1 || !(item = this.regex.exec(item))) continue;
  				while(item_time = this.regex_time.exec(item[1])) {
  					this.list.push([parseFloat(item_time[1])*60+parseFloat(item_time[2]), item[2]]);
  				}
  				this.regex_time.lastIndex = 0;
  			}

  			/* 有效歌词 */
  			if(this.list.length > 0) {
  				/* 对时间轴排序 */
  				this.list.sort(function(a,b){ return a[0]-b[0]; });
  				if(this.list[0][0] >= 0.1) this.list.unshift([this.list[0][0]-0.1, '']);
  				this.list.push([this.list[this.list.length-1][0]+1, '']);
  				for(var i = 0; i < this.list.length; i++)
  					html += this.format.replace(/\{html\}/gi, this.list[i][1]);

  				/* 赋值到指定容器 */
  				$('#'+this.prefixid+'_list').html(html).animate({ marginTop: 0 }, 100).show();
  				/* 隐藏没有歌词的层 */
  				$('#'+this.prefixid+'_nofound').hide();
  				/* 定时调用回调函数，监听歌曲进度 */
  				//this.handle = setInterval('$.lrc.jump($.lrc.callback());', this.interval*1000);
          this.handle = setInterval(function(){
            $.lrc.jump($.lrc.callback());
          }, this.interval*1000);
  			}else{ /* 没有歌词 */
  				$('#'+this.prefixid+'_list').hide();
  				$('#'+this.prefixid+'_nofound').show();
  			}
  		},
  		/* 跳到指定时间的歌词 */
  		jump: function(duration) {
  			if(typeof(this.handle) != 'number' || typeof(duration) != 'number' || !$.isArray(this.list) || this.list.length < 1) return this.stop();
  			if(duration < 0) duration = 0;
  			if(this.__duration == duration) return;
  			duration += 0.2;
  			this.__duration = duration;
  			duration += this.interval;

  			var left = 0, right = this.list.length-1, last = right
  				pivot = Math.floor(right/2),
  				tmpobj = null, tmp = 0, thisobj = this;

  			/* 二分查找 */
  			while(left <= pivot && pivot <= right) {
  				if(this.list[pivot][0] <= duration && (pivot == right || duration < this.list[pivot+1][0])) {
  					//if(pivot == right) this.stop();
  					break;
  				}else if( this.list[pivot][0] > duration ) { /* left */
  					right = pivot;
  				}else{ /* right */
  					left = pivot;
  				}
  				tmp = left + Math.floor((right - left)/2);
  				if(tmp == pivot) break;
  				pivot = tmp;
  			}

  			if(pivot == this.pivot) return;
  			this.pivot = pivot;
  			tmpobj = $('#'+this.prefixid+'_list').children().removeClass(this.hoverClass).eq(pivot).addClass(thisobj.hoverClass);
  			tmp = tmpobj.next().offset().top-tmpobj.parent().offset().top - this.hoverTop;
  			tmp = tmp > 0 ? tmp * -1 : 0;
        //改变歌词的marginTop值
        //this.animata(tmpobj.parent()[0]).animate({marginTop: tmp + 'px'}, this.interval*1000);
  			tmpobj.parent().parent().animate({scrollTop: -tmp + 'px'}, this.interval*1000);
        this.animata(tmpobj.parent()[0])
  		},
  		/* 停止执行歌曲 */
  		stop: function() {
  			if(typeof(this.handle) == 'number') clearInterval(this.handle);
  			this.handle = this.callback = null;
  			this.__duration = -1;
  			this.regex_time.lastIndex = 0;
  			this.list = [];
  		},
  		animata: function(elem) {
  			var f = j = 0, callback, _this={},
  				tween = function(t,b,c,d){ return -c*(t/=d)*(t-2) + b; }
  			_this.execution = function(key, val, t) {
  				var s = (new Date()).getTime(), d = t || 500,
  				    b = parseInt(elem.style[key]) || 0,
  				    c = val-b;
  				(function(){
  					var t = (new Date()).getTime() - s;
  					if(t>d){
  						t=d;
  						elem.style[key] = tween(t,b,c,d) + 'px';
  						++f == j && callback && callback.apply(elem);
  						return true;
  					}
  					elem.style[key] = tween(t,b,c,d)+'px';
  					setTimeout(arguments.callee, 10);
  				})();
  			}
  			_this.animate = function(sty, t, fn){
  				callback = fn;
  				for(var i in sty){
  					j++;
  					_this.execution(i,parseInt(sty[i]),t);
  				}
  			}
  			return _this;
  		}
  	};
  })(jQuery);

  //设置下一首歌曲链接
  function setNextPlay(){
    var run = localStorage.playRule;
    var random = 0;
    var songlist = $('#songlist');
    var liArr = songlist.find('li');
    var liCur = songlist.find('.current');
    if(run == 'order'){
      //顺序播放
      if(liArr.length>1){
        if(liCur.next().length>0){
          localStorage.playNext = liCur.next().find('.name').attr('href');
        }else{
          localStorage.playNext = liArr.eq(0).find('.name').attr('href');
        }
      }
    }else if(run == 'single'){
      //单曲播放
      localStorage.playNext = liCur.find('.name').attr('href');
    }else if(run == 'random'){
      //随机播放
      random = com.getRandom(liArr.length,liCur.index());
      localStorage.playNext = liArr.eq(random).find('.name').attr('href');
    }else{
      localStorage.playNext = '';
    }
  }
  //搜索歌曲
  function searchAddSong(key){
    var html = '';
    com.loadOpen();
    $.ajax({
      url:'/ajax_api_search?keyword=' + key,
      type:'GET',
      timeout:10000,
      error:function(http,err){
        console.error(http,err);
        com.loadClose();
      },
      success:function(data){
        var json = JSON.parse(data);
        if(json.length>0){
          html += '<dl class="sug-song clearfix"><dt>歌曲</dt>';
          $.each(json,function(i,e){
            if(i>8) return false;
            html += '<dd data-id="' + e.song_id +
                    '" data-name="' + e.song_name +
                    '" data-url="' + e.song_url +
                    '" data-artist="' + e.song_artist + '"><a href="javascript:;">' +
                    '<span class="songName">' + e.song_name + '</span>' +
                    '<span class="singerName"><i>-</i>' + e.song_artist + '</span><span class="madd-ico"></span></a></dd>';
          });
          html += '</dl>';
        }else{
          html = '<div style="padding:15px;text-align:center;">没有相关歌曲！</div>'
        }
        $('.hotsearch').hide();
        $('#sugboxid').html(html).parent().show();
        com.loadClose();
      }
    });
  }
  //获取歌词
  function getLyrics(str,con){
    var lyrics = str.split("\n");
    var list = [];
    var item_time;
    var item;
    var format = '<li>{html}</li>';
    var html = '';
    var regex = /^[^\[]*((?:\s*\[\d+\:\d+(?:\.\d+)?\])+)([\s\S]*)$/,
    regex_time = /\[(\d+)\:((?:\d+)(?:\.\d+)?)\]/g,
    regex_trim = /^\s+|\s+$/;
    for(var i = 0; i < lyrics.length; i++) {
      item = lyrics[i].replace(regex_trim, '');
      if(item.length < 1 || !(item = regex.exec(item))) continue;

      while(item_time = regex_time.exec(item[1])) {
        list.push([parseFloat(item_time[1])*60+parseFloat(item_time[2]), item[2]]);
      }
      regex_time.lastIndex = 0;
    }
    if(list.length > 0) {
      list.sort(function(a,b){ return a[0]-b[0]; });
      if(list[0][0] >= 0.1) list.unshift([list[0][0]-0.1, '']);
      list.push([list[list.length-1][0]+1, '']);
      for(var i = 0; i < list.length; i++)
        html += format.replace(/\{html\}/gi, list[i][1]);
      con.html(html);
    }else{
      con.html('该歌曲没有歌词');
      con.after($('<div style="line-height:400px;font-size:18px;color:#ccc;">该歌曲暂时没有歌词</div>'))
    }
  }
});
