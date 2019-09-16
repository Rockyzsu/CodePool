define(['jquery'], function($){
  $('.rank-list').on('mouseenter','li',function(){
    $(this).addClass('current').siblings().removeClass('current');
  });
  //回到顶部
  $('#toHead').on('click',function(){
    $('html').animate({ scrollTop: 0 }, 'swing');
  });
  var top = $('html').scrollTop();
  if(top >= 500){
    $('#toHead').fadeIn();
  }else{
    $('#toHead').fadeOut();
  }

  //图片懒加载
  var checkTime = null; //显示图睛时间
  var timer = null; //节流时间
  showImg();
  $(window).on('scroll',function(){
    /*if($('.layz_load').length == 0){
      $(window).off('scroll');
      return;
    }*/
    if(timer){
      return;
    }
    timer = setTimeout(function(){
      clearTimeout(timer);
      timer = null;
      top = $('html').scrollTop();
      if(top >= 500){
        $('#toHead').fadeIn();
      }else{
        $('#toHead').fadeOut();
      }
      if(checkTime){
        clearTimeout(checkTime);
      }
      checkTime = setTimeout(showImg,100);
    },500);
  });

  //设置图片位置
  function setPicPo(wrap,img,full){
    var rW = wrap.width();
    var rH = wrap.height();
    var mW = img.width();
    var mH = img.height();
    var sW = 'auto',sH = 'auto',sT = 0,sL = 0;
    mW>=mH?!full?sW=rW:sH=rH:!full?sH=rH:sW=rW;
    wrap.css({
      position:'relative'
    });
    img.css({
      position:'absolute',
      width:sW+'px',
      height:sH+'px',
    });
    sT = (rH-img.height())/2;
    sL = (rW-img.width())/2;
    img.css({
      top:sT+'px',
      left:sL+'px'
    });
  }

  //显示图片
  function showImg(){
    $('.layz_load').each(function(i,e){
      var img = $(e).find('img');
      if(checkPosition(e)){
        img.attr('src',img.attr('data-src')).hide().on('load',function(){
          var box = img.parent();
          img.fadeIn().parent().removeClass('layz_load');
          if(box.hasClass('pic_po')){
            setPicPo(box,img,true);
          }
        });
      }
    });
  }

  //分页
  function pages(curPages,countPages,pageBar){
    var str = '';
    var i = 1,start,end;
    if(!countPages || countPages<=1){
      pageBar.empty();
      return;
    }
    if(curPages!=1){
      str += '<a href="javascript:;" class="prev" data-page="'+(curPages-1)+'"><i></i>上一页</a>';
    }
    if(countPages > 6){
      if(curPages == 1){
        str += '<span class="sel">'+1+'</span>';
      }else{
        str += '<a href="javascript:;" data-page="'+1+'">'+1+'</a>';
      }
      start = (curPages-2)>2?(curPages-2):2;
      end = (+curPages+2)<countPages-1?(+curPages+2):countPages-1;

      if(start>2){
        str += '<span>...</span>';
      }
      for(i = start;i <= end;i++){
        if(i == curPages){
          str += '<span class="sel">'+i+'</span>';
        }else{
          str += '<a href="javascript:;" data-page="'+i+'">'+i+'</a>';
        }
      }
      if(countPages - end > 1){
        str += '<span>...</span>';
      }
      if(curPages == countPages){
        str += '<span class="sel">' + countPages + '</span>';
      }else{
        str += '<a href="javascript:;" data-page="' + countPages + '">' + countPages + '</a>';
      }
    }else{
      for(;i <= countPages;i++){
        if(i == curPages){
          str += '<span class="sel">' + i + '</span>';
        }else{
          str += '<a href="javascript:;" data-page="' + i + '">' + i + '</a>';
        }
      }
    }
    if(curPages<countPages){
      str += '<a href="javascript:;" class="next" data-page="' + (+curPages+1) + '"><i></i>下一页</a>';
    }
    pageBar.html(str);
  }

  //检测图片位置
  function checkPosition(dom){
    var coords = dom.getBoundingClientRect();
    return ((coords.top > 0 || coords.top + coords.height>0) && coords.top <= (window.innerHeight || document.documentElement.clientHeight));
  }

  //增加PK
  function addPk(val,name,imgUrl,artist){
    var liArr = $('#v3CompareItems').find('li');
    var len = liArr.length;
    var li,close,a,img,span,input,pkUrl,b=true;
    $.each(liArr,function(i,e){
      if($(e).find('input').val()==val){
        b = false;
        return;
      }
    });
    if(!b){
      boxAlert('歌曲已经存在');
    }else{
      if(len>=2){
        boxAlert('最多只能PK2首歌曲');
        b = false;
      }else{
        li = $('<li>');
        close = $('<span class="v3-compare-item-del">关闭</span>');
        a = $('<a class="pic" target="play" title="'+name+'-'+artist+'" href="/song_'+val+'.html"></a>');
        img = $('<img alt="'+name+'的封面">');
        span = $('<span>'+name+'</span>');
        input = $('<input type="hidden">');
        input.val(val);
        img.attr('src',imgUrl);
        li.append(close).append(a.append(img).append(span)).append(input);
        $('#v3CompareItems').append(li);
        $('#v3CompareNum').text(len+1);
      }
      liArr = $('#v3CompareItems').find('li');
      if(liArr.length == 2){
        pkUrl = '/pk';
        $.each(liArr,function(i,e){
          var id = $(e).find('input').val();
          if(isNaN(id/1)){
            id = id.slice(id.indexOf('_')+1,id.indexOf('.'));
          }
          pkUrl += '_'+id;
        });
        pkUrl += '.html';
        $('#v3CompareParamBtn').attr({'href':pkUrl,'target':'_blank'});
      }
    }
    $('#v3CompareBox').show();
    return b;
  }
  //载入层
  function loadOpen(){
    $('#maskLoad').fadeIn(200);
  }
  function loadClose(){
    $('#maskLoad').fadeOut(200);
  }
  //tab标签切换
  function tabSwitch(tab,con,callback){
    tab.on('click','.t_c',function(){
      $(this).addClass('current').siblings().removeClass('current');
      con.find('.t_s').eq($(this).index()).addClass('current').siblings().removeClass('current').hide().end().show(0,function(){
        showImg();
      });
      if(typeof callback == 'function')callback();
    });
  }
  //焦点切换对象
  function FocusSwitch(wrap,focus,auto,time,leftBtn,rightBtn){
    this.w = wrap;
    this.f = focus;
    this.a = auto;
    this.now = 0;
    this.t = time;
    this.timer = null;
    this.lb = leftBtn;
    this.rb = rightBtn;
  }
  //获取随机数
  function getRandom(range,exclude){
    var num = Math.floor(Math.random()*range);
    if(num == exclude){
      return getRandom(range,exclude);
    }else{
      return num;
    }
  }
  //初始化焦点对象
  FocusSwitch.prototype.init = function(){
    var _this = this;
    var slide = this.w.find('.f_s');
    var len = slide.length;
    var w = slide.eq(0).width()*len;
    this.w.css({position:'relative',zIndex:0,overflow:'hidden'}).find('.f_w').css({position:'absolute',left:'0',width:w+'px',transition:'.5s'}).on({'mouseenter':function(){
      if(_this.a)clearInterval(_this.timer);
    },'mouseleave':function(){
      if(_this.a)_this.autoPlay();
    }});
    if(this.f!=null){
      if(this.f.find('.f_c').length > len){
        $.each(this.f.find('.f_c'),function(i,e){
          if(i>=len){
            $(e).remove();
          }
        });
      }
      this.f.css({position:'relative',zIindex:1}).on({'mouseenter':function(){
        if(_this.a)clearInterval(_this.timer);
      },'mouseleave':function(){
        if(_this.a)_this.autoPlay();
      }}).on('click','.f_c',function(){
        _this.now = $(this).index();
        _this.move();
      });
    }
    if(this.lb!=null){
      this.lb.on({
        'mouseenter':function(){
          if(_this.a)clearInterval(_this.timer);
        },
        'mouseleave':function(){
          if(_this.a)_this.autoPlay();
        },
        'click':function(){
          _this.now --;
          if(_this.now<0){
            _this.now = len-1;
          }
          _this.move();
        }
      });
    }
    if(this.rb!=null){
      this.rb.on({
        'mouseenter':function(){
          if(_this.a)clearInterval(_this.timer);
        },
        'mouseleave':function(){
          if(_this.a)_this.autoPlay();
        },
        'click':function(){
          _this.now ++;
          if(_this.now>=len){
            _this.now = 0;
          }
          _this.move();
        }
      });
    }
    if(this.a)this.autoPlay();
  };
  //焦点变化
  FocusSwitch.prototype.move = function(){
    var slide = this.w.find('.f_s');
    var w = slide.eq(0).width();
    this.w.find('.f_w').css({'left':-this.now*w+'px'});
    if(this.f!=null){
      this.f.find('.f_c').eq(this.now).addClass('active').siblings().removeClass('active');
    }
  };
  //自动切换焦点
  FocusSwitch.prototype.autoPlay = function(){
    var _this = this;
    var slide = this.w.find('.f_s');
    this.timer = setInterval(function(){
      if(_this.now>=slide.length-1){
        _this.now = 0;
      }else{
        _this.now++;
      }
      _this.move();
    },this.t||5000);
  };
  //pk支持分数
  function pkTicket(obj1,obj2,a,b,height){
    a = parseInt(a);
    b = parseInt(b);
    var aH = a / (a + b) * height;
    var bH = b / (a + b) * height;
    obj1.css('height',aH + 'px');
    obj2.css('height',bH + 'px');
  }
  var msgIndex = 9999;
  //弹框功能
  /*
  com.msg(str,option)
  str:要显示的字符
  option:设置属性
    option.time:设置自动关闭时间，默认5秒
  */
  function msg(){
    var inside  = {
      time:3000
    }
    var $msg = $('<div class="box_msg"><div class="con"></div></div>');
    $msg.find('.con').text(arguments[0]);
    $('body').append($msg);
    var w = $msg.width();
    var h = $msg.height();
    $msg.css({
      marginTop : -(h/2)+'px',
      marginLeft : -(w/2)+'px',
      zIndex : ++msgIndex
    });
    $msg.hide().fadeIn();
    if(arguments[1] && typeof arguments[1] == 'object'){
      $.each(arguments[1],function(i,e){
        inside[i] = e;
      });
    }
    setTimeout(function(){
      $msg.fadeOut(200,function(){
        $(this).remove();
      })
    },inside.time)
  }
  /*
  com.alert(option,callback)
  option:要显示的字符或设置对象
    option.time:自动关闭的时间，单位是毫秒，默认为0，即不自动关闭
    option.title:弹框标题
    option.content:弹框内容，可以包含html标签
    option.maskClose:点击遮罩层是否关闭，默认是false，即不关闭
    option.button:按钮数据，默认是1，即只有确定按钮，设置为2可以显示确定和取消两个按钮
  callback:点确定按钮时的回调函数
  */
  function boxAlert(option,callback){
    var set = {
      time : 0,
      title : '温馨提示',
      content : '',
      maskClose : false,
      button : 1
    };
    var html = '';
    var $mask = $('<div class="box_mask"></div>');
    var $wrap = $('<div class="box_wrap"></div>');
    if(option && typeof option == 'object'){
      $.each(option,function(i,e){
        set[i] = e;
      });
    }else{
      set.content = option;
    }
    html += '<div class="box_title">' + set.title + '</div>' +
            '<div class="box_content"><div class="box_in">' + set.content + '</div></div>' +
            '<div class="box_btn_wrap">';
    if(set.button == 1){
      html += '<button class="confirm_btn">确定</button>';
    }else if(set.button == 2){
      html += '<button class="confirm_btn">确定</button><button class="cancel_btn">取消</button>';
    }
    html += '</div><div class="box_close"></div>';
    $wrap.html(html);
    $('body').append([$mask,$wrap]);
    var w = $wrap.width();
    var h = $wrap.height();
    $mask.css('zIndex',msgIndex);
    msgIndex ++;
    $wrap.css({
      marginTop : -(h/2)+'px',
      marginLeft : -(w/2)+'px',
      zIndex:msgIndex
    });
    $mask.hide().fadeIn();
    $wrap.hide().fadeIn();
    if(set.maskClose){
      $mask.on('click',function(){
        removes($mask);
        removes($wrap);
      });
    }
    $wrap.on('click','.box_close,button',function(){
      removes($mask);
      removes($wrap);
      if($(this).hasClass('confirm_btn')&&callback)callback();
    });
    if(typeof set.time == 'number' && set.time>0){
      setTimeout(function(){
        removes($mask);
        removes($wrap);
      },set.time);
    }
    function removes(obj){
      obj.fadeOut(200,function(){
        obj.remove();
      })
    }
  }
  return {
    setPicPo:setPicPo,
    showImg:showImg,
    pages:pages,
    checkPosition:checkPosition,
    addPk:addPk,
    tabSwitch:tabSwitch,
    FocusSwitch:FocusSwitch,
    getRandom:getRandom,
    loadOpen:loadOpen,
    loadClose:loadClose,
    pkTicket:pkTicket,
    msg:msg,
    alert:boxAlert
  };
});
