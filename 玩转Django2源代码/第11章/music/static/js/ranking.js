require.config({
　paths: {
    "jquery": "jquery.min",
    "com": "common.min"
  }
});

require(['jquery','com'], function ($,com){
  var delayed = null;
  //侧栏显示隐藏
  $('#sideNav').on({'mouseenter':function(){
      $(this).addClass('hover').find('.sub-cate').show();
    },'mouseleave':function(){
      $(this).removeClass('hover').find('.sub-cate').hide();
    }
  },'.computer');
  //排行榜详情列表滑过
  $('.rank-list-table').on({
    'mouseenter':function(){
      $(this).addClass('hover');
    },
    'mouseleave':function(){
      $(this).removeClass('hover');
    }
  },'tr');
  $('.rank-list-table').on({
    'mouseenter':function(){
      if($(this).parent().hasClass('more-info-on')){
        clearTimeout(delayed);
      }else{
        $(this).parent().addClass('more-info-on');
      }
    }
  },'.more-btn');
  $('.rank-list-table').on({
    'mouseleave':function(){
      var _this = this;
      delayed = setTimeout(function(){
        $(_this).parent().removeClass('more-info-on');
      });
    }
  },'.more-info');
  $('.rank-list-table').on({
    'mouseenter':function(){
      if($(this).parent().hasClass('more-info-on')){
        clearTimeout(delayed);
      }
    },
    'click':function(){
      var $this = $(this);
      var id = $this.attr('data-rel');
      var name = $this.attr('data-name');
      var img = $this.attr('data-img');
      var artist = $this.attr('data-artist');
      if(com.addPk(id,name,img,artist)){
        $(this).addClass('btn-cansel').removeClass('btn-add');
      };
    }
  },'.btn-add');
});
