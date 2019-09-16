require.config({
　paths: {
    "jquery": "jquery.min",
    "com": "common.min"
  }
});

require(['jquery','com'], function ($,com){
  //登录注册切换
  $('#unauth_main').on('click','.switch',function(){
    var _this = this;
    setTimeout(function(){
      $(_this).closest('.switch_box').hide().siblings().show();
    },400);
    setTimeout(function(){
      $('#unauth_main').removeClass('switching');
    },600);

    $('#unauth_main').addClass('switching');
});
  //验证正则
  var regPhone = /^1[34578]\d{9}$/;
  var regPwd = /^[\w!@#$%^&*()]{4,16}$/;
  var regUser = /^\w{3,16}$/;
  //登录框对象
  var J_LoginUser = $('#userid');
  var J_LoginPsw = $('#J_LoginPsw');
  var is_auto = $('#is_auto');
  var J_LoginButton = $('#J_LoginButton');
  var loginTipCon = $('#loginTipCon');
  //注册框对象
  var J_RegistUser = $('#user_phone');
  var J_RegistPsw = $('#user_pwd');
  var repeat_pwd = $('#repeat_pwd');
  var J_RegButton = $('#J_RegButton');
  var agree = $('#agree');
  var regTipCon = $('#regTipCon');

  J_LoginUser.on('blur',function(){
    detect(regUser,$(this).val(),'请输入正确的用户名或手机号','请输入用户名或手机号',loginTipCon);
  });
  J_LoginPsw.on('blur',function(){
    detect(regPwd,$(this).val(),'密码必须是4-16位字母数字或符号','请输入密码',loginTipCon);
  });
  J_RegistUser.on('blur',function(){
    detect(regPhone,$(this).val(),'用户名必须是有效的手机号','请输入用户名',regTipCon);
  });
  J_RegistPsw.on('blur',function(){
    detect(regPwd,$(this).val(),'密码必须是4-16位字母数字或符号','请输入密码',regTipCon);
  });
  repeat_pwd.on('blur',function(){
    if($(this).val()!=J_RegistPsw.val()){
      regTipCon.text('两次输入的密码必须一致').parent().show();
    }else{
      regTipCon.empty().parent().hide();
    }
  });
 
  
  //检测输入内容
  function detect(regexp,val,text,air,tip){
    if(val.trim() == ''){
      tip.text(air).parent().show();
      return false;
    }else if(!regexp.test(val)){
      tip.text(text).parent().show();
      return false;
    }else{
      tip.parent().hide();
      return true;//user_login?userid=xxx&pwd=xx&remember_me=T
    }
  }
});
